from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3, os
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
                db.execute("INSERT INTO users (username,password,display_name,role,color,initials) VALUES (?,?,?,?,?,?)", u)
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
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
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
        users = [dict(r) for r in db.execute("SELECT * FROM users WHERE role='employee' ORDER BY display_name").fetchall()]
        projects = [dict(r) for r in db.execute("SELECT * FROM projects ORDER BY name").fetchall()]
    return templates.TemplateResponse("app.html", {"request": request, "user": dict(user), "users": users, "projects": projects, "is_ceo": is_ceo(user)})

@app.get("/api/tasks")
async def api_tasks(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        w = "" if is_ceo(user) else f"WHERE t.assignee_id={user['id']}"
        rows = db.execute(f"""SELECT t.*, u.display_name as assignee_name, u.color as assignee_color,
            u.initials as assignee_initials, p.name as project_name, p.color as project_color
            FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id LEFT JOIN projects p ON t.project_id=p.id {w}
            ORDER BY t.created_at DESC""").fetchall()
    return JSONResponse([dict(r) for r in rows])

@app.post("/api/tasks")
async def create_task(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    aid = data.get("assignee_id", user["id"]) if is_ceo(user) else user["id"]
    with get_db() as db:
        r = db.execute("INSERT INTO tasks (title,description,priority,status,assignee_id,project_id,due_date,created_by) VALUES (?,?,?,?,?,?,?,?)",
            (data["title"], data.get("description",""), data.get("priority","medium"), "todo", aid, data.get("project_id"), data.get("due_date"), user["id"]))
    return JSONResponse({"id": r.lastrowid, "ok": True})

@app.put("/api/tasks/{tid}")
async def update_task(request: Request, tid: int):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    data = await request.json()
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not task: return JSONResponse({"error": "not found"}, 404)
        if not is_ceo(user) and task["assignee_id"] != user["id"]:
            return JSONResponse({"error": "forbidden"}, 403)
        sets, vals = [], []
        for k in ["title","description","priority","status","assignee_id","project_id","due_date"]:
            if k in data: sets.append(f"{k}=?"); vals.append(data[k])
        if sets:
            sets.append("updated_at=?"); vals.append(datetime.now().isoformat()); vals.append(tid)
            db.execute(f"UPDATE tasks SET {','.join(sets)} WHERE id=?", vals)
    return JSONResponse({"ok": True})

@app.delete("/api/tasks/{tid}")
async def delete_task(request: Request, tid: int):
    user = current_user(request)
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    with get_db() as db:
        db.execute("UPDATE report_items SET task_id=NULL WHERE task_id=?", (tid,))
        db.execute("DELETE FROM tasks WHERE id=?", (tid,))
    return JSONResponse({"ok": True})

@app.get("/api/reports")
async def api_reports(request: Request, user_id: Optional[int]=None):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        w, p = [], []
        if not is_ceo(user): w.append("dr.user_id=?"); p.append(user["id"])
        elif user_id: w.append("dr.user_id=?"); p.append(user_id)
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
        w = "" if is_ceo(user) else f"AND t.assignee_id={user['id']}"
        rows = db.execute(f"""SELECT t.*, u.display_name as assignee_name, u.color as assignee_color,
            u.initials as assignee_initials, p.name as project_name, p.color as project_color
            FROM tasks t LEFT JOIN users u ON t.assignee_id=u.id LEFT JOIN projects p ON t.project_id=p.id
            WHERE t.due_date BETWEEN ? AND ? {w} ORDER BY t.due_date""", (start.isoformat(), end.isoformat())).fetchall()
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
    if not user or not is_ceo(user): return JSONResponse({"error": "forbidden"}, 403)
    data = await request.json()
    with get_db() as db:
        r = db.execute("INSERT INTO projects (name,color,description) VALUES (?,?,?)", (data["name"], data.get("color","#0B3D6B"), data.get("description","")))
    return JSONResponse({"ok": True, "id": r.lastrowid})

@app.get("/api/users")
async def api_users(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        users = db.execute("SELECT id,username,display_name,role,color,initials FROM users WHERE role='employee' ORDER BY display_name").fetchall()
    return JSONResponse([dict(u) for u in users])

@app.get("/api/projects/list")
async def api_projects_list(request: Request):
    user = current_user(request)
    if not user: return JSONResponse({"error": "unauthorized"}, 401)
    with get_db() as db:
        projects = db.execute("SELECT * FROM projects ORDER BY name").fetchall()
        result = []
        for p in projects:
            w = "" if is_ceo(user) else f"AND assignee_id={user['id']}"
            tc = db.execute(f"SELECT COUNT(*) as c FROM tasks WHERE project_id=? {w}", (p["id"],)).fetchone()["c"]
            dc = db.execute(f"SELECT COUNT(*) as c FROM tasks WHERE project_id=? AND status='done' {w}", (p["id"],)).fetchone()["c"]
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
    if not name or not username: return JSONResponse({"error": "missing fields"}, 400)
    initials = "".join([w[0] for w in name.split()[:2]]).upper() or username[:2].upper()
    with get_db() as db:
        exists = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if exists: return JSONResponse({"error": "username_taken"}, 409)
        r = db.execute("INSERT INTO users (username,password,display_name,role,color,initials) VALUES (?,?,?,?,?,?)",
            (username, data.get("password","1234"), name, "employee", data.get("color","#185FA5"), initials))
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
            sets.append("password=?"); vals.append(data["password"])
        if sets:
            vals.append(uid)
            db.execute(f"UPDATE users SET {','.join(sets)} WHERE id=?", vals)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
