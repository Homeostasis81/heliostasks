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
        projects = [dict(r) for r in db.execute("SELECT * FROM projects ORDER BY name").fetchall()]
    user_dict = dict(user)
    return templates.TemplateResponse("app.html", {"request": request, "user": user_dict, "users": users, "projects": projects, "is_ceo": is_ceo(user), "is_manager": user["role"] == "manager", "user_role": user["role"]})

@app.get("/api/tasks")
async def api_tasks(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        rows = db.execute("""SELECT t.*, u.display_name as assignee_name, u.color as assignee_color,
            u.initials as assignee_initials, p.name as project_name, p.color as project_color
            FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id LEFT JOIN projects p ON t.project_id=p.id
            ORDER BY t.created_at DESC""").fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/tasks")
async def create_task(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    aid = data.get("assignee_id", user["id"])
    with get_db() as db:
        r = db.execute("INSERT INTO tasks (title,description,priority,status,assignee_id,project_id,due_date,created_by) VALUES (?,?,?,?,?,?,?,?)",
            (data["title"], data.get("description",""), data.get("priority","medium"), "todo", aid, data.get("project_id"), data.get("due_date"), user["id"]))
        tid = r.lastrowid
    log_action(user["id"], "task", tid, "created", {"title": data["title"], "assignee_id": aid})
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
    if changes:
        log_action(user["id"], "task", tid, "updated", changes)
    return JSONResponse({"ok": True})

@app.delete("/api/tasks/{tid}")
async def delete_task(request: Request, tid: int):
    user = current_user(request)
    if not user or user["role"] not in ("ceo","manager"): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        task = db.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()
        db.execute("UPDATE report_items SET task_id=NULL WHERE task_id=?", (tid,))
        db.execute("DELETE FROM tasks WHERE id=?", (tid,))
    log_action(user["id"], "task", tid, "deleted", {"title": task["title"] if task else None})
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
    return JSONResponse({"month":m,"year":y,"tasks":[dict(r) for r in rows]})

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
    with get_db() as db:
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
        my_overdue = db.execute("SELECT COUNT(*) as c FROM tasks WHERE assignee_id=? AND status!='done' AND due_date<?",
                                (user["id"], today)).fetchone()["c"]
        my_today = db.execute("SELECT COUNT(*) as c FROM tasks WHERE assignee_id=? AND status!='done' AND due_date=?",
                              (user["id"], today)).fetchone()["c"]
        my_active = db.execute("SELECT COUNT(*) as c FROM tasks WHERE assignee_id=? AND status NOT IN ('done')",
                               (user["id"],)).fetchone()["c"]
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
    return JSONResponse({
        "overdue": my_overdue, "today": my_today, "active": my_active,
        "has_report_today": has_report_today, "team_no_report": team_no_report
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
