from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3, os, hashlib, secrets, shutil, threading, time, json
from datetime import datetime, date, timedelta
from contextlib import contextmanager
from typing import Optional

from setup_files import setup_files
setup_files()

app = FastAPI(title="Helios Tasks")
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", "helios-tasks-secret-2026"))
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
DB_PATH = os.environ.get("DB_PATH", "helios_tasks.db")
BACKUP_DIR = os.environ.get("BACKUP_DIR", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# === Password hashing ===
def hash_password(password: str) -> str:
    """PBKDF2-SHA256 with random salt. Format: pbkdf2$iterations$salt_hex$hash_hex"""
    salt = secrets.token_bytes(16)
    iterations = 100000
    h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
    return f"pbkdf2${iterations}${salt.hex()}${h.hex()}"

def verify_password(password: str, stored: str) -> bool:
    """Verify password against stored hash. Supports both hashed and legacy plain text."""
    if not stored:
        return False
    if stored.startswith("pbkdf2$"):
        try:
            _, iters, salt_hex, hash_hex = stored.split("$")
            h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), int(iters))
            return secrets.compare_digest(h.hex(), hash_hex)
        except Exception:
            return False
    # Legacy plain text comparison (will be migrated on next login)
    return stored == password

def is_hashed(stored: str) -> bool:
    return bool(stored) and stored.startswith("pbkdf2$")

# === Backup system ===
def backup_db():
    """Create a timestamped backup of the database. Keeps last 30 daily backups."""
    if not os.path.exists(DB_PATH):
        return None
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"helios_tasks_{ts}.db")
        # Use SQLite backup API for safe online backup
        src = sqlite3.connect(DB_PATH)
        dst = sqlite3.connect(backup_path)
        src.backup(dst)
        src.close()
        dst.close()
        # Cleanup old backups - keep only last 30
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("helios_tasks_") and f.endswith(".db")])
        if len(backups) > 30:
            for old in backups[:-30]:
                try:
                    os.remove(os.path.join(BACKUP_DIR, old))
                except Exception:
                    pass
        return backup_path
    except Exception as e:
        print(f"Backup error: {e}")
        return None

def backup_loop():
    """Run backup once a day in background."""
    while True:
        time.sleep(24 * 60 * 60)
        backup_db()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def log_action(user_id, entity_type, entity_id, action, details=None):
    """Record an action in the audit log."""
    try:
        with get_db() as db:
            db.execute("INSERT INTO audit_log (user_id, entity_type, entity_id, action, details) VALUES (?,?,?,?,?)",
                       (user_id, entity_type, entity_id, action, json.dumps(details) if details else None))
    except Exception as e:
        print(f"Audit log error: {e}")

# === Bulgarian holidays + working days ===
def orthodox_easter(year):
    """Calculate Orthodox Easter date for given year."""
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19*c + 15) % 30
    e = (2*a + 4*b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    julian = date(year, month, day)
    return julian + timedelta(days=13)

def bg_holidays(year):
    """Return set of Bulgarian holiday dates for the year."""
    holidays = {
        date(year, 1, 1), date(year, 3, 3), date(year, 5, 1), date(year, 5, 6),
        date(year, 5, 24), date(year, 9, 6), date(year, 9, 22), date(year, 11, 1),
        date(year, 12, 24), date(year, 12, 25), date(year, 12, 26),
    }
    easter = orthodox_easter(year)
    holidays.add(easter - timedelta(days=2))  # Good Friday
    holidays.add(easter - timedelta(days=1))  # Holy Saturday
    holidays.add(easter)
    holidays.add(easter + timedelta(days=1))  # Easter Monday
    return holidays

def working_days_between(start_date, end_date):
    """Count working days (Mon-Fri, excluding BG holidays) in range inclusive."""
    if isinstance(start_date, str): start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str): end_date = date.fromisoformat(end_date)
    if end_date < start_date: return 0
    holidays = bg_holidays(start_date.year) | bg_holidays(end_date.year)
    count = 0
    d = start_date
    while d <= end_date:
        if d.weekday() < 5 and d not in holidays:
            count += 1
        d += timedelta(days=1)
    return count

def get_or_create_balance(db, user_id, year, default=20):
    """Get leave balance for user, creating with default if missing."""
    row = db.execute("SELECT * FROM leave_balances WHERE user_id=? AND year=?", (user_id, year)).fetchone()
    if row: return dict(row)
    db.execute("INSERT INTO leave_balances (user_id, year, paid_total) VALUES (?,?,?)", (user_id, year, default))
    return {"user_id": user_id, "year": year, "paid_total": default}

def compute_balance(db, user_id, year):
    """Return {total, used, remaining} for paid leave in year."""
    bal = get_or_create_balance(db, user_id, year)
    used = db.execute("""SELECT COALESCE(SUM(working_days),0) as s FROM leave_requests
        WHERE user_id=? AND leave_type='paid' AND status='approved'
        AND strftime('%Y', start_date)=?""", (user_id, str(year))).fetchone()["s"]
    return {"total": bal["paid_total"], "used": used, "remaining": bal["paid_total"] - used}

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            color TEXT DEFAULT '#0B3D6B',
            initials TEXT DEFAULT 'XX',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, color TEXT DEFAULT '#0B3D6B',
            description TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, description TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'medium',
            status TEXT NOT NULL DEFAULT 'todo',
            assignee_id INTEGER, project_id INTEGER, due_date DATE,
            created_by INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assignee_id) REFERENCES users(id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS task_collaborators (
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (task_id, user_id),
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_collab_user ON task_collaborators(user_id);
        CREATE TABLE IF NOT EXISTS daily_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL, report_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS report_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL, description TEXT NOT NULL,
            hours REAL DEFAULT 0, task_id INTEGER,
            FOREIGN KEY (report_id) REFERENCES daily_reports(id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        );
        CREATE TABLE IF NOT EXISTS report_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL, note TEXT NOT NULL,
            FOREIGN KEY (report_id) REFERENCES daily_reports(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS report_visibility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            UNIQUE(manager_id, employee_id),
            FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            entity_type TEXT NOT NULL,
            entity_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_log(entity_type, entity_id);
        CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            working_days INTEGER NOT NULL DEFAULT 0,
            reason TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            approved_by INTEGER,
            decided_at TIMESTAMP,
            decision_note TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
        );
        CREATE INDEX IF NOT EXISTS idx_leave_user ON leave_requests(user_id);
        CREATE INDEX IF NOT EXISTS idx_leave_dates ON leave_requests(start_date, end_date);
        CREATE TABLE IF NOT EXISTS leave_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            paid_total INTEGER NOT NULL DEFAULT 20,
            UNIQUE(user_id, year),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)
        if not db.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
            users_data = [
                ('drago','helios2026','Драго','ceo','#0B3D6B','ДР'),
                ('ivan','1234','Иван','employee','#185FA5','ИВ'),
                ('maria','1234','Мария','employee','#D4A843','МА'),
                ('petar','1234','Петър','employee','#1D9E75','ПЕ'),
                ('georgi','1234','Георги','employee','#D85A30','ГЕ'),
                ('elena','1234','Елена','employee','#534AB7','ЕЛ'),
            ]
            for u in users_data:
                username, password, name, role, color, initials = u
                db.execute("INSERT INTO users (username,password,display_name,role,color,initials) VALUES (?,?,?,?,?,?)",
                           (username, hash_password(password), name, role, color, initials))
            projs = [('Omega #3','#0B3D6B',''),('Omega #4','#1D9E75',''),('Omega #2','#D4A843',''),('Склад','#D85A30',''),('Общо','#534AB7','')]
            for p in projs:
                db.execute("INSERT INTO projects (name,color,description) VALUES (?,?,?)", p)
            today = date.today()
            td = timedelta
            seeds = [
                ('Монтаж на палуба','critical','progress',2,1,today+td(days=4)),
                ('Проверка OBC зарядни','high','todo',3,1,today+td(days=2)),
                ('Инвентаризация секция Б','medium','todo',4,4,today+td(days=6)),
                ('Подготовка документи','low','review',5,2,today+td(days=9)),
                ('Тест електрическа система','critical','done',6,3,today+td(days=1)),
                ('Поръчка липсващи крепежи','high','progress',2,4,today+td(days=3)),
                ('Лакиране корпус','medium','todo',3,1,today+td(days=8)),
                ('Качване данни в системата','low','done',4,5,today+td(days=5)),
                ('Преглед доставка от Италия','high','progress',5,4,today+td(days=2)),
                ('Настройка навигация','medium','review',6,3,today+td(days=7)),
                ('Монтаж хардуер борд','high','todo',2,2,today+td(days=5)),
                ('Тест водоустойчивост','critical','progress',3,1,today+td(days=3)),
            ]
            for s in seeds:
                db.execute("INSERT INTO tasks (title,priority,status,assignee_id,project_id,due_date,created_by) VALUES (?,?,?,?,?,?,1)", s)
            yd = today - td(days=1)
            rpt_data = [
                (2,[('Монтаж на палуба — секция А завършена',4,1),('Поръчка крепежи — изпратена',1.5,6)],'Чакам потвърждение от доставчик'),
                (3,[('Тест водоустойчивост — 3 цикъла',5,12),('Документация на резултатите',1.5,None)],'Открит малък теч на стик 7'),
                (4,[('Инвентаризация секция Б — 60%',6,3)],'Разбъркан рафт, отнема повече време'),
                (5,[('Преглед документи от Италия',3,9),('Координация с куриер',1.5,None)],'Доставката закъснява с 2 дни'),
                (6,[('Финален тест ел. система',4,5),('Настройка GPS модул',2,10)],'Omega #2 готова за навигация'),
            ]
            for uid, items, note in rpt_data:
                r = db.execute("INSERT INTO daily_reports (user_id,report_date) VALUES (?,?)", (uid, yd))
                rid = r.lastrowid
                for desc, hrs, tid in items:
                    db.execute("INSERT INTO report_items (report_id,description,hours,task_id) VALUES (?,?,?,?)", (rid,desc,hrs,tid))
                if note:
                    db.execute("INSERT INTO report_notes (report_id,note) VALUES (?,?)", (rid, note))
        # Migration: ensure task_collaborators exists for older DBs
        db.execute("""CREATE TABLE IF NOT EXISTS task_collaborators (
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (task_id, user_id),
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_collab_user ON task_collaborators(user_id)")

init_db()

# Initial backup on startup, then daily in background
backup_db()
threading.Thread(target=backup_loop, daemon=True).start()

def current_user(request: Request):
    uid = request.session.get("user_id")
    if not uid: return None
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

def is_ceo(user): return user and user["role"] == "ceo"
def is_privileged(user): return user and user["role"] in ("ceo","manager")

def get_task_collaborators(db, task_id):
    rows = db.execute("""SELECT u.id, u.display_name, u.color, u.initials
        FROM task_collaborators tc JOIN users u ON tc.user_id=u.id
        WHERE tc.task_id=? ORDER BY u.display_name""", (task_id,)).fetchall()
    return [dict(r) for r in rows]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse("/app" if current_user(request) else "/login", 302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and verify_password(password, user["password"]):
            # Auto-migrate plain text passwords to hashed format on successful login
            if not is_hashed(user["password"]):
                db.execute("UPDATE users SET password=? WHERE id=?", (hash_password(password), user["id"]))
            request.session["user_id"] = user["id"]
            return RedirectResponse("/app", 302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Грешно потребителско име или парола"})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", 302)

@app.get("/app", response_class=HTMLResponse)
async def main_app(request: Request):
    user = current_user(request)
    if not user: return RedirectResponse("/login", 302)
    with get_db() as db:
        users = [dict(r) for r in db.execute("SELECT * FROM users WHERE role!='ceo' ORDER BY role DESC, display_name").fetchall()]
        all_users = [dict(r) for r in db.execute("SELECT id, username, display_name, role, color, initials FROM users ORDER BY role DESC, display_name").fetchall()]
        projects = [dict(r) for r in db.execute("SELECT * FROM projects ORDER BY name").fetchall()]
    user_dict = dict(user)
    return templates.TemplateResponse("app.html", {"request": request, "user": user_dict, "users": users, "all_users": all_users, "projects": projects, "is_ceo": is_ceo(user), "is_manager": user["role"] == "manager", "user_role": user["role"]})

@app.get("/api/tasks")
async def api_tasks(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        rows = db.execute("""SELECT t.*, u.display_name as assignee_name, u.color as assignee_color,
            u.initials as assignee_initials, p.name as project_name, p.color as project_color,
            cu.display_name as creator_name
            FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id LEFT JOIN projects p ON t.project_id=p.id
            LEFT JOIN users cu ON t.created_by=cu.id
            ORDER BY t.created_at DESC""").fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["collaborators"] = get_task_collaborators(db, r["id"])
            result.append(d)
    return JSONResponse(result)

@app.post("/api/tasks")
async def create_task(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    aid = data.get("assignee_id", user["id"])
    collaborators = data.get("collaborators", []) or []
    with get_db() as db:
        r = db.execute("INSERT INTO tasks (title,description,priority,status,assignee_id,project_id,due_date,created_by) VALUES (?,?,?,?,?,?,?,?)",
            (data["title"], data.get("description",""), data.get("priority","medium"), "todo", aid, data.get("project_id"), data.get("due_date"), user["id"]))
        tid = r.lastrowid
        seen = set()
        for cid in collaborators:
            try: cid = int(cid)
            except (TypeError, ValueError): continue
            if cid == aid or cid in seen: continue
            seen.add(cid)
            db.execute("INSERT OR IGNORE INTO task_collaborators (task_id, user_id) VALUES (?,?)", (tid, cid))
    log_action(user["id"], "task", tid, "created", {"title": data["title"], "assignee_id": aid, "collaborators": list(seen)})
    return JSONResponse({"id": tid, "ok": True})

@app.put("/api/tasks/{tid}")
async def update_task(request: Request, tid: int):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not task: return JSONResponse({"error": "not found"}, 404)
        sets, vals = [], []
        changes = {}
        for k in ["title","description","priority","status","assignee_id","project_id","due_date"]:
            if k in data:
                sets.append(f"{k}=?"); vals.append(data[k])
                if str(task[k]) != str(data[k]):
                    changes[k] = {"from": task[k], "to": data[k]}
        if sets:
            sets.append("updated_at=?"); vals.append(datetime.now().isoformat()); vals.append(tid)
            db.execute(f"UPDATE tasks SET {','.join(sets)} WHERE id=?", vals)
        if "collaborators" in data:
            new_collabs = set()
            for cid in (data.get("collaborators") or []):
                try: cid = int(cid)
                except (TypeError, ValueError): continue
                new_collabs.add(cid)
            new_assignee = data.get("assignee_id", task["assignee_id"])
            if new_assignee in new_collabs:
                new_collabs.discard(new_assignee)
            existing = {r["user_id"] for r in db.execute("SELECT user_id FROM task_collaborators WHERE task_id=?", (tid,)).fetchall()}
            to_add = new_collabs - existing
            to_remove = existing - new_collabs
            for cid in to_add:
                db.execute("INSERT OR IGNORE INTO task_collaborators (task_id, user_id) VALUES (?,?)", (tid, cid))
            for cid in to_remove:
                db.execute("DELETE FROM task_collaborators WHERE task_id=? AND user_id=?", (tid, cid))
            if to_add or to_remove:
                changes["collaborators"] = {"added": list(to_add), "removed": list(to_remove)}
    if changes:
        log_action(user["id"], "task", tid, "updated", changes)
    return JSONResponse({"ok": True})

@app.delete("/api/tasks/{tid}")
async def delete_task(request: Request, tid: int):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        task = db.execute("SELECT title, created_by FROM tasks WHERE id=?", (tid,)).fetchone()
        if not task: return JSONResponse({"error": "not found"}, 404)
        if not (is_privileged(user) or task["created_by"] == user["id"]):
            return JSONResponse({"error": "forbidden"}, 403)
        db.execute("UPDATE report_items SET task_id=NULL WHERE task_id=?", (tid,))
        db.execute("DELETE FROM task_collaborators WHERE task_id=?", (tid,))
        db.execute("DELETE FROM tasks WHERE id=?", (tid,))
    log_action(user["id"], "task", tid, "deleted", {"title": task["title"]})
    return JSONResponse({"ok": True})

@app.get("/api/reports")
async def api_reports(request: Request, user_id: Optional[int]=None):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        w, p = [], []
        if user["role"] == "ceo":
            if user_id: w.append("dr.user_id=?"); p.append(user_id)
        elif user["role"] == "manager":
            visible = db.execute("SELECT employee_id FROM report_visibility WHERE manager_id=?", (user["id"],)).fetchall()
            visible_ids = [v["employee_id"] for v in visible] + [user["id"]]
            if user_id:
                if user_id not in visible_ids:
                    return JSONResponse([])
                w.append("dr.user_id=?"); p.append(user_id)
            else:
                placeholders = ",".join(["?"]*len(visible_ids))
                w.append(f"dr.user_id IN ({placeholders})"); p.extend(visible_ids)
        else:
            w.append("dr.user_id=?"); p.append(user["id"])
        wc = ("WHERE "+" AND ".join(w)) if w else ""
        rows = db.execute(f"SELECT dr.*, u.display_name, u.color, u.initials FROM daily_reports dr JOIN users u ON dr.user_id=u.id {wc} ORDER BY dr.report_date DESC, u.display_name", p).fetchall()
        result = []
        for r in rows:
            items = db.execute("SELECT ri.*, t.title as task_title FROM report_items ri LEFT JOIN tasks t ON ri.task_id=t.id WHERE ri.report_id=?", (r["id"],)).fetchall()
            notes = db.execute("SELECT * FROM report_notes WHERE report_id=?", (r["id"],)).fetchall()
            result.append({**dict(r), "items": [dict(i) for i in items], "notes": [dict(n) for n in notes]})
    return JSONResponse(result)

@app.post("/api/reports")
async def create_report(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    rd = data.get("report_date", date.today().isoformat())
    with get_db() as db:
        ex = db.execute("SELECT id FROM daily_reports WHERE user_id=? AND report_date=?", (user["id"], rd)).fetchone()
        if ex:
            rid = ex["id"]
            db.execute("DELETE FROM report_items WHERE report_id=?", (rid,))
            db.execute("DELETE FROM report_notes WHERE report_id=?", (rid,))
        else:
            r = db.execute("INSERT INTO daily_reports (user_id,report_date) VALUES (?,?)", (user["id"], rd))
            rid = r.lastrowid
        for item in data.get("items", []):
            db.execute("INSERT INTO report_items (report_id,description,hours,task_id) VALUES (?,?,?,?)",
                (rid, item["description"], item.get("hours",0), item.get("task_id")))
        if data.get("note"):
            db.execute("INSERT INTO report_notes (report_id,note) VALUES (?,?)", (rid, data["note"]))
    return JSONResponse({"ok": True, "id": rid})

@app.get("/api/calendar")
async def api_calendar(request: Request, month: Optional[int]=None, year: Optional[int]=None):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    today = date.today()
    m, y = month or today.month, year or today.year
    start = date(y, m, 1)
    end = date(y+(m//12), (m%12)+1, 1) - timedelta(days=1)
    with get_db() as db:
        rows = db.execute("""SELECT t.*, u.display_name as assignee_name, u.color as assignee_color,
            u.initials as assignee_initials, p.name as project_name, p.color as project_color
            FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id LEFT JOIN projects p ON t.project_id=p.id
            WHERE t.due_date BETWEEN ? AND ? ORDER BY t.due_date""", (start.isoformat(), end.isoformat())).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["collaborators"] = get_task_collaborators(db, r["id"])
            result.append(d)
    return JSONResponse({"month":m,"year":y,"tasks":result})

@app.get("/api/dashboard")
async def api_dashboard(request: Request):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    today = date.today()
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) as c FROM tasks").fetchone()["c"]
        done = db.execute("SELECT COUNT(*) as c FROM tasks WHERE status='done'").fetchone()["c"]
        overdue = db.execute("SELECT COUNT(*) as c FROM tasks WHERE due_date<? AND status!='done'", (today.isoformat(),)).fetchone()["c"]
        critical = db.execute("SELECT COUNT(*) as c FROM tasks WHERE priority='critical' AND status!='done'").fetchone()["c"]
        by_status = {s: db.execute("SELECT COUNT(*) as c FROM tasks WHERE status=?", (s,)).fetchone()["c"] for s in ['todo','progress','review','done']}
        emps = db.execute("SELECT * FROM users WHERE role='employee' ORDER BY display_name").fetchall()
        team = []
        for e in emps:
            et = db.execute("SELECT COUNT(*) as c FROM tasks WHERE assignee_id=?", (e["id"],)).fetchone()["c"]
            ed = db.execute("SELECT COUNT(*) as c FROM tasks WHERE assignee_id=? AND status='done'", (e["id"],)).fetchone()["c"]
            rpt = db.execute("SELECT id FROM daily_reports WHERE user_id=? AND report_date=?", (e["id"], today.isoformat())).fetchone()
            rh = 0
            if rpt: rh = db.execute("SELECT COALESCE(SUM(hours),0) as h FROM report_items WHERE report_id=?", (rpt["id"],)).fetchone()["h"]
            team.append({**dict(e), "total_tasks":et, "done_tasks":ed, "has_report_today":rpt is not None, "hours_today":rh})
    return JSONResponse({"total":total,"done":done,"overdue":overdue,"critical":critical,"by_status":by_status,"team":team})

@app.post("/api/projects")
async def create_project(request: Request):
    user = current_user(request)
    if not user or user["role"] not in ("ceo","manager","employee"): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    with get_db() as db:
        r = db.execute("INSERT INTO projects (name,color,description) VALUES (?,?,?)", (data["name"], data.get("color","#0B3D6B"), data.get("description","")))
    return JSONResponse({"ok": True, "id": r.lastrowid})

@app.get("/api/users")
async def api_users(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    include_all = request.query_params.get("include_all") == "1"
    with get_db() as db:
        if include_all:
            users = db.execute("SELECT id,username,display_name,role,color,initials FROM users ORDER BY role DESC, display_name").fetchall()
        else:
            users = db.execute("SELECT id,username,display_name,role,color,initials FROM users WHERE role!='ceo' ORDER BY role DESC, display_name").fetchall()
    return JSONResponse([dict(u) for u in users])

@app.get("/api/projects/list")
async def api_projects_list(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        projects = db.execute("SELECT * FROM projects ORDER BY name").fetchall()
        result = []
        for p in projects:
            tc = db.execute("SELECT COUNT(*) as c FROM tasks WHERE project_id=?", (p["id"],)).fetchone()["c"]
            dc = db.execute("SELECT COUNT(*) as c FROM tasks WHERE project_id=? AND status='done'", (p["id"],)).fetchone()["c"]
            result.append({**dict(p), "total_tasks":tc, "done_tasks":dc})
    return JSONResponse(result)

# === Admin endpoints (CEO only) ===

@app.post("/api/users")
async def create_user(request: Request):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    name = data.get("display_name","").strip()
    username = data.get("username","").strip().lower()
    role = data.get("role","employee")
    if role not in ("employee","manager"): role = "employee"
    if not name or not username: return JSONResponse({"error": "missing fields"}, 400)
    initials = "".join([w[0] for w in name.split()[:2]]).upper() or username[:2].upper()
    with get_db() as db:
        exists = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if exists: return JSONResponse({"error": "username_taken"}, 409)
        r = db.execute("INSERT INTO users (username,password,display_name,role,color,initials) VALUES (?,?,?,?,?,?)",
            (username, hash_password(data.get("password","1234")), name, role, data.get("color","#185FA5"), initials))
    return JSONResponse({"ok": True, "id": r.lastrowid})

@app.put("/api/users/{uid}")
async def update_user(request: Request, uid: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    with get_db() as db:
        u = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        if not u: return JSONResponse({"error": "not found"}, 404)
        sets, vals = [], []
        for k in ["display_name","username","color"]:
            if k in data and data[k]: sets.append(f"{k}=?"); vals.append(data[k])
        if "display_name" in data and data["display_name"]:
            name = data["display_name"].strip()
            initials = "".join([w[0] for w in name.split()[:2]]).upper()
            sets.append("initials=?"); vals.append(initials)
        if "password" in data and data["password"]:
            sets.append("password=?"); vals.append(hash_password(data["password"]))
        if "role" in data and data["role"] in ("employee","manager") and u["role"] != "ceo":
            sets.append("role=?"); vals.append(data["role"])
            if data["role"] != "manager":
                db.execute("DELETE FROM report_visibility WHERE manager_id=?", (uid,))
        if sets:
            vals.append(uid)
            db.execute(f"UPDATE users SET {','.join(sets)} WHERE id=?", vals)
    return JSONResponse({"ok": True})

@app.post("/api/users/{uid}/reset-password")
async def reset_password(request: Request, uid: int):
    """Generate and set a new random temporary password. Returns it once for CEO to share."""
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        u = db.execute("SELECT id FROM users WHERE id=?", (uid,)).fetchone()
        if not u: return JSONResponse({"error": "not found"}, 404)
        new_pass = secrets.token_urlsafe(8)[:10]
        db.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pass), uid))
    log_action(user["id"], "user", uid, "reset_password")
    return JSONResponse({"ok": True, "new_password": new_pass})

@app.post("/api/me/change-password")
async def change_my_password(request: Request):
    """Allow any logged-in user to change their own password by providing old + new."""
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    old_pass = data.get("old_password","")
    new_pass = data.get("new_password","").strip()
    if len(new_pass) < 4: return JSONResponse({"error": "password_too_short"}, 400)
    if not verify_password(old_pass, user["password"]):
        return JSONResponse({"error": "wrong_old_password"}, 403)
    with get_db() as db:
        db.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pass), user["id"]))
    log_action(user["id"], "user", user["id"], "self_change_password")
    return JSONResponse({"ok": True})

@app.get("/api/visibility/{manager_id}")
async def get_visibility(request: Request, manager_id: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        rows = db.execute("SELECT employee_id FROM report_visibility WHERE manager_id=?", (manager_id,)).fetchall()
    return JSONResponse([r["employee_id"] for r in rows])

@app.put("/api/visibility/{manager_id}")
async def set_visibility(request: Request, manager_id: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    employee_ids = data.get("employee_ids", [])
    with get_db() as db:
        db.execute("DELETE FROM report_visibility WHERE manager_id=?", (manager_id,))
        for eid in employee_ids:
            db.execute("INSERT OR IGNORE INTO report_visibility (manager_id, employee_id) VALUES (?,?)", (manager_id, eid))
    return JSONResponse({"ok": True})

@app.delete("/api/users/{uid}")
async def delete_user(request: Request, uid: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        u = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
        if not u or u["role"] == "ceo": return JSONResponse({"error": "cannot delete"}, 403)
        db.execute("UPDATE tasks SET assignee_id=NULL WHERE assignee_id=?", (uid,))
        db.execute("DELETE FROM task_collaborators WHERE user_id=?", (uid,))
        db.execute("DELETE FROM users WHERE id=?", (uid,))
    return JSONResponse({"ok": True})

@app.put("/api/projects/{pid}")
async def update_project(request: Request, pid: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    with get_db() as db:
        sets, vals = [], []
        for k in ["name","color","description"]:
            if k in data: sets.append(f"{k}=?"); vals.append(data[k])
        if sets:
            vals.append(pid)
            db.execute(f"UPDATE projects SET {','.join(sets)} WHERE id=?", vals)
    return JSONResponse({"ok": True})

@app.delete("/api/projects/{pid}")
async def delete_project(request: Request, pid: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        db.execute("UPDATE tasks SET project_id=NULL WHERE project_id=?", (pid,))
        db.execute("DELETE FROM projects WHERE id=?", (pid,))
    return JSONResponse({"ok": True})

# === Audit log ===
@app.get("/api/audit/{entity_type}/{entity_id}")
async def get_audit(request: Request, entity_type: str, entity_id: int):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        rows = db.execute("""SELECT al.*, u.display_name, u.color, u.initials
            FROM audit_log al LEFT JOIN users u ON al.user_id=u.id
            WHERE al.entity_type=? AND al.entity_id=? ORDER BY al.created_at DESC LIMIT 50""",
            (entity_type, entity_id)).fetchall()
    return JSONResponse([{**dict(r), "details": json.loads(r["details"]) if r["details"] else None} for r in rows])

# === Notifications (badge counts) ===
@app.get("/api/notifications")
async def api_notifications(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    today = date.today().isoformat()
    with get_db() as db:
        my_overdue = db.execute("""SELECT COUNT(DISTINCT t.id) as c FROM tasks t
            LEFT JOIN task_collaborators tc ON tc.task_id=t.id
            WHERE (t.assignee_id=? OR tc.user_id=?) AND t.status!='done' AND t.due_date<?""",
            (user["id"], user["id"], today)).fetchone()["c"]
        my_today = db.execute("""SELECT COUNT(DISTINCT t.id) as c FROM tasks t
            LEFT JOIN task_collaborators tc ON tc.task_id=t.id
            WHERE (t.assignee_id=? OR tc.user_id=?) AND t.status!='done' AND t.due_date=?""",
            (user["id"], user["id"], today)).fetchone()["c"]
        my_active = db.execute("""SELECT COUNT(DISTINCT t.id) as c FROM tasks t
            LEFT JOIN task_collaborators tc ON tc.task_id=t.id
            WHERE (t.assignee_id=? OR tc.user_id=?) AND t.status NOT IN ('done')""",
            (user["id"], user["id"])).fetchone()["c"]
        has_report_today = db.execute("SELECT id FROM daily_reports WHERE user_id=? AND report_date=?",
                                      (user["id"], today)).fetchone() is not None
        team_no_report = 0
        if user["role"] in ("ceo","manager"):
            visible_ids = []
            if user["role"] == "ceo":
                visible_ids = [u["id"] for u in db.execute("SELECT id FROM users WHERE role='employee'").fetchall()]
            else:
                visible_ids = [v["employee_id"] for v in db.execute("SELECT employee_id FROM report_visibility WHERE manager_id=?", (user["id"],)).fetchall()]
            for eid in visible_ids:
                r = db.execute("SELECT id FROM daily_reports WHERE user_id=? AND report_date=?", (eid, today)).fetchone()
                if not r: team_no_report += 1
        # Pending leave requests requiring my decision
        pending_leave = 0
        if user["role"] == "ceo":
            pending_leave = db.execute("SELECT COUNT(*) as c FROM leave_requests WHERE status='pending'").fetchone()["c"]
        elif user["role"] == "manager":
            visible = [v["employee_id"] for v in db.execute(
                "SELECT employee_id FROM report_visibility WHERE manager_id=?", (user["id"],)).fetchall()]
            if visible:
                placeholders = ",".join(["?"]*len(visible))
                pending_leave = db.execute(f"""SELECT COUNT(*) as c FROM leave_requests
                    WHERE status='pending' AND user_id IN ({placeholders})""", visible).fetchone()["c"]
    return JSONResponse({
        "overdue": my_overdue, "today": my_today, "active": my_active,
        "has_report_today": has_report_today, "team_no_report": team_no_report,
        "pending_leave": pending_leave
    })

# === Backups (CEO only) ===
@app.get("/api/backups")
async def list_backups(request: Request):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    files = []
    if os.path.exists(BACKUP_DIR):
        for f in sorted(os.listdir(BACKUP_DIR), reverse=True):
            if f.startswith("helios_tasks_") and f.endswith(".db"):
                fp = os.path.join(BACKUP_DIR, f)
                files.append({"name": f, "size": os.path.getsize(fp), "created": os.path.getmtime(fp)})
    return JSONResponse(files)

@app.post("/api/backups/create")
async def create_backup(request: Request):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    path = backup_db()
    if not path: return JSONResponse({"error": "backup_failed"}, 500)
    return JSONResponse({"ok": True, "name": os.path.basename(path)})

@app.get("/api/backups/download/{name}")
async def download_backup(request: Request, name: str):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    # Sanitize: only allow our backup naming pattern
    if not (name.startswith("helios_tasks_") and name.endswith(".db") and "/" not in name and "\\" not in name):
        return JSONResponse({"error": "invalid"}, 400)
    fp = os.path.join(BACKUP_DIR, name)
    if not os.path.exists(fp): return JSONResponse({"error": "not_found"}, 404)
    return FileResponse(fp, filename=name, media_type="application/octet-stream")

# === Leave requests ===
VALID_LEAVE_TYPES = ("paid", "sick", "unpaid", "other")

def _can_manage_leave_for(user, target_user_id, db):
    """True if `user` can approve/reject leave of target_user_id."""
    if is_ceo(user): return True
    if user["role"] == "manager":
        r = db.execute("SELECT 1 FROM report_visibility WHERE manager_id=? AND employee_id=?",
                       (user["id"], target_user_id)).fetchone()
        return r is not None
    return False

@app.get("/api/leave/requests")
async def list_leave_requests(request: Request, user_id: Optional[int] = None, status: Optional[str] = None):
    """
    For CEO: all requests (optionally filter by user_id or status).
    For Manager: self + employees they have visibility on.
    For Employee: only own requests.
    """
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        where = []
        params = []
        if user["role"] == "ceo":
            if user_id: where.append("lr.user_id=?"); params.append(user_id)
        elif user["role"] == "manager":
            visible = [v["employee_id"] for v in db.execute(
                "SELECT employee_id FROM report_visibility WHERE manager_id=?", (user["id"],)).fetchall()]
            visible_ids = visible + [user["id"]]
            if user_id:
                if user_id not in visible_ids: return JSONResponse([])
                where.append("lr.user_id=?"); params.append(user_id)
            else:
                placeholders = ",".join(["?"]*len(visible_ids))
                where.append(f"lr.user_id IN ({placeholders})"); params.extend(visible_ids)
        else:
            where.append("lr.user_id=?"); params.append(user["id"])
        if status:
            where.append("lr.status=?"); params.append(status)
        wc = ("WHERE " + " AND ".join(where)) if where else ""
        rows = db.execute(f"""SELECT lr.*, u.display_name, u.color, u.initials,
            a.display_name as approver_name
            FROM leave_requests lr
            JOIN users u ON lr.user_id=u.id
            LEFT JOIN users a ON lr.approved_by=a.id
            {wc} ORDER BY
              CASE lr.status WHEN 'pending' THEN 0 WHEN 'approved' THEN 1 ELSE 2 END,
              lr.start_date DESC""", params).fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/leave/requests")
async def create_leave_request(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    leave_type = data.get("leave_type")
    start = data.get("start_date")
    end = data.get("end_date")
    reason = data.get("reason", "").strip()
    target_user_id = data.get("user_id", user["id"])
    if leave_type not in VALID_LEAVE_TYPES:
        return JSONResponse({"error": "invalid_type"}, 400)
    if not start or not end:
        return JSONResponse({"error": "missing_dates"}, 400)
    try:
        sd = date.fromisoformat(start)
        ed = date.fromisoformat(end)
    except Exception:
        return JSONResponse({"error": "bad_date"}, 400)
    if ed < sd: return JSONResponse({"error": "end_before_start"}, 400)
    # Only CEO can file on behalf of others
    if target_user_id != user["id"] and not is_ceo(user):
        return JSONResponse({"error": "forbidden"}, 403)
    wd = working_days_between(sd, ed)
    # Check balance for paid leave
    if leave_type == "paid" and wd > 0:
        with get_db() as db:
            bal = compute_balance(db, target_user_id, sd.year)
            if wd > bal["remaining"]:
                return JSONResponse({"error": "insufficient_balance", "remaining": bal["remaining"], "requested": wd}, 400)
    with get_db() as db:
        # Auto-approve if CEO creates for anyone, or for non-paid types where company often just records
        auto_approve = is_ceo(user) and target_user_id != user["id"]
        status = "approved" if auto_approve else "pending"
        r = db.execute("""INSERT INTO leave_requests
            (user_id, leave_type, start_date, end_date, working_days, reason, status, approved_by, decided_at)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (target_user_id, leave_type, start, end, wd, reason, status,
             user["id"] if auto_approve else None,
             datetime.now().isoformat() if auto_approve else None))
        lid = r.lastrowid
    log_action(user["id"], "leave", lid, "created" if not auto_approve else "created_approved",
               {"type": leave_type, "days": wd, "target": target_user_id})
    return JSONResponse({"ok": True, "id": lid, "working_days": wd, "status": status})

@app.post("/api/leave/requests/{lid}/decide")
async def decide_leave(request: Request, lid: int):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    decision = data.get("decision")  # "approved" or "rejected"
    note = data.get("note", "").strip()
    if decision not in ("approved", "rejected"):
        return JSONResponse({"error": "invalid_decision"}, 400)
    with get_db() as db:
        req = db.execute("SELECT * FROM leave_requests WHERE id=?", (lid,)).fetchone()
        if not req: return JSONResponse({"error": "not_found"}, 404)
        if req["status"] != "pending":
            return JSONResponse({"error": "already_decided"}, 400)
        if not _can_manage_leave_for(user, req["user_id"], db):
            return JSONResponse({"error": "forbidden"}, 403)
        # Re-verify balance at decision time for paid
        if decision == "approved" and req["leave_type"] == "paid":
            sd = date.fromisoformat(req["start_date"])
            bal = compute_balance(db, req["user_id"], sd.year)
            if req["working_days"] > bal["remaining"]:
                return JSONResponse({"error": "insufficient_balance", "remaining": bal["remaining"]}, 400)
        db.execute("UPDATE leave_requests SET status=?, approved_by=?, decided_at=?, decision_note=? WHERE id=?",
                   (decision, user["id"], datetime.now().isoformat(), note, lid))
    log_action(user["id"], "leave", lid, decision, {"note": note})
    return JSONResponse({"ok": True})

@app.delete("/api/leave/requests/{lid}")
async def cancel_leave(request: Request, lid: int):
    """Users can cancel their own pending requests. CEO/managers can cancel anyone's."""
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        req = db.execute("SELECT * FROM leave_requests WHERE id=?", (lid,)).fetchone()
        if not req: return JSONResponse({"error": "not_found"}, 404)
        # Allow owner to cancel own pending request; CEO/manager with visibility can cancel any status
        is_owner = req["user_id"] == user["id"]
        can_manage = _can_manage_leave_for(user, req["user_id"], db)
        if not (is_owner or can_manage):
            return JSONResponse({"error": "forbidden"}, 403)
        if is_owner and not can_manage and req["status"] != "pending":
            return JSONResponse({"error": "already_decided"}, 400)
        db.execute("DELETE FROM leave_requests WHERE id=?", (lid,))
    log_action(user["id"], "leave", lid, "cancelled")
    return JSONResponse({"ok": True})

@app.get("/api/leave/balance")
async def my_balance(request: Request, year: Optional[int] = None):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    y = year or date.today().year
    with get_db() as db:
        bal = compute_balance(db, user["id"], y)
    return JSONResponse({**bal, "year": y})

@app.get("/api/leave/balance/{uid}")
async def user_balance(request: Request, uid: int, year: Optional[int] = None):
    """CEO/manager can view a specific user's balance."""
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    y = year or date.today().year
    with get_db() as db:
        if not (is_ceo(user) or _can_manage_leave_for(user, uid, db) or user["id"] == uid):
            return JSONResponse({"error": "forbidden"}, 403)
        bal = compute_balance(db, uid, y)
    return JSONResponse({**bal, "year": y, "user_id": uid})

@app.put("/api/leave/balance/{uid}")
async def set_balance(request: Request, uid: int):
    """CEO only: set total paid leave for a user in a year."""
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    y = data.get("year", date.today().year)
    total = int(data.get("paid_total", 20))
    with get_db() as db:
        db.execute("""INSERT INTO leave_balances (user_id, year, paid_total) VALUES (?,?,?)
            ON CONFLICT(user_id, year) DO UPDATE SET paid_total=excluded.paid_total""",
            (uid, y, total))
    log_action(user["id"], "leave_balance", uid, "updated", {"year": y, "total": total})
    return JSONResponse({"ok": True})

@app.get("/api/leave/calendar")
async def leave_calendar(request: Request, month: int, year: int):
    """Return approved leave dates for users the requester can see, to show on calendar."""
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    from calendar import monthrange
    start = date(year, month, 1)
    end = date(year, month, monthrange(year, month)[1])
    with get_db() as db:
        if is_ceo(user):
            visible_ids = [u["id"] for u in db.execute("SELECT id FROM users").fetchall()]
        elif user["role"] == "manager":
            visible = [v["employee_id"] for v in db.execute(
                "SELECT employee_id FROM report_visibility WHERE manager_id=?", (user["id"],)).fetchall()]
            visible_ids = visible + [user["id"]]
        else:
            visible_ids = [user["id"]]
        if not visible_ids: return JSONResponse([])
        placeholders = ",".join(["?"]*len(visible_ids))
        rows = db.execute(f"""SELECT lr.id, lr.user_id, lr.leave_type, lr.start_date, lr.end_date, lr.status,
                u.display_name, u.color, u.initials
            FROM leave_requests lr JOIN users u ON lr.user_id=u.id
            WHERE lr.status IN ('approved','pending')
              AND lr.user_id IN ({placeholders})
              AND NOT (lr.end_date < ? OR lr.start_date > ?)""",
            (*visible_ids, start.isoformat(), end.isoformat())).fetchall()
    return JSONResponse([dict(r) for r in rows])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
