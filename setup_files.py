import os, base64

def setup_files():
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    text_files = {"static/style.css": CSS, "templates/login.html": LOGIN, "templates/app.html": APP}
    for path, content in text_files.items():
        with open(path, "w", encoding="utf-8") as f: f.write(content)
    bin_files = {"static/logo.png": LOGO_B64, "static/boat.png": BOAT_B64}
    for path, b64data in bin_files.items():
        if not os.path.exists(path):
            with open(path, "wb") as f: f.write(base64.b64decode(b64data))

CSS = r'''/* === Helios Marine Tasks — Dark Premium Theme === */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root{
  --bg-deep:#0d1117;
  --bg-card:#161b22;
  --bg-card-hover:#1c2129;
  --bg-surface:#21262d;
  --border:#30363d;
  --border-light:rgba(255,255,255,.06);
  --text-primary:#e6edf3;
  --text-secondary:#8b949e;
  --text-muted:#484f58;
  --gold:#c6a350;
  --gold-dim:rgba(198,163,80,.15);
  --gold-border:rgba(198,163,80,.2);
  --navy:#16385f;
  --accent-red:#f85149;
  --accent-green:#3fb950;
  --accent-blue:#58a6ff;
  --accent-amber:#d29922;
  --radius:10px;
  --radius-lg:14px;
}

*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;background:var(--bg-deep);color:var(--text-primary);min-height:100vh;-webkit-font-smoothing:antialiased}
.app{max-width:1100px;margin:0 auto;padding:0 16px 100px}

/* === Topbar === */
.topbar{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--border-light);margin-bottom:4px}
.logo{display:flex;align-items:center;gap:10px}
.logo img{height:24px;opacity:.9}
.logo-divider{width:1px;height:20px;background:var(--border)}
.logo-label{font-size:12px;font-weight:500;color:var(--text-muted);letter-spacing:1.5px;text-transform:uppercase}
.user-info{display:flex;align-items:center;gap:10px}
.user-name{font-size:13px;font-weight:500;color:var(--text-secondary)}
.user-badge{font-size:10px;color:var(--gold);background:var(--gold-dim);padding:3px 10px;border-radius:20px;font-weight:600;letter-spacing:.5px}
.logout-btn{color:var(--text-muted);padding:6px;display:flex;border-radius:8px;transition:all .15s;text-decoration:none}
.logout-btn:hover{color:var(--accent-red);background:rgba(248,81,73,.08)}

/* === Notifications === */
.notif-btn{position:relative;background:none;border:none;color:var(--text-secondary);padding:6px;cursor:pointer;border-radius:8px;display:flex;align-items:center;transition:all .15s}
.notif-btn:hover{color:var(--gold);background:var(--bg-surface)}
.notif-badge{position:absolute;top:0;right:0;background:var(--accent-red);color:white;font-size:10px;font-weight:600;border-radius:10px;min-width:16px;height:16px;display:flex;align-items:center;justify-content:center;padding:0 4px;border:2px solid var(--bg-deep)}
.notif-popup{position:absolute;top:50px;right:16px;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;width:280px;max-width:calc(100vw - 32px);z-index:90;box-shadow:0 8px 32px rgba(0,0,0,.4);overflow:hidden;display:none}
.notif-popup.show{display:block;animation:slideDown .18s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
.notif-header{padding:12px 16px;border-bottom:1px solid var(--border-light);font-size:13px;font-weight:600;color:var(--text-primary)}
.notif-list{padding:6px 0}
.notif-item{padding:10px 16px;display:flex;align-items:center;gap:10px;font-size:13px;color:var(--text-secondary);cursor:pointer;transition:background .12s}
.notif-item:hover{background:var(--bg-surface)}
.notif-icon{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.notif-content{flex:1;display:flex;justify-content:space-between;align-items:center;gap:8px}
.notif-count{font-weight:600;color:var(--text-primary)}
.notif-empty{padding:24px 16px;text-align:center;color:var(--text-muted);font-size:12px}

/* === Audit log === */
.audit-list{max-height:240px;overflow-y:auto;background:var(--bg-deep);border-radius:8px;padding:8px;margin-top:8px}
.audit-item{padding:8px 10px;border-bottom:1px solid var(--border-light);font-size:11px;color:var(--text-secondary);display:flex;gap:8px;align-items:flex-start}
.audit-item:last-child{border-bottom:none}
.audit-when{color:var(--text-muted);font-size:10px;white-space:nowrap}
.audit-who{color:var(--gold);font-weight:600}
.audit-action{color:var(--text-secondary)}
.audit-detail{color:var(--text-muted);font-size:10px;margin-top:2px}

/* === Backups === */
.backup-row{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;background:var(--bg-card);border:1px solid var(--border-light);border-radius:8px;margin-bottom:6px;font-size:12px}
.backup-name{color:var(--text-secondary);font-family:monospace;font-size:11px}
.backup-size{color:var(--text-muted);font-size:10px}
.backup-actions{display:flex;gap:6px}

/* === Nav === */
.nav{display:flex;gap:2px;padding:8px 0;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav-btn{padding:8px 14px;font-size:12px;font-weight:500;background:none;border:none;cursor:pointer;color:var(--text-muted);border-radius:8px;transition:all .15s;font-family:inherit;white-space:nowrap;flex-shrink:0}
.nav-btn:hover{color:var(--text-secondary);background:var(--bg-surface)}
.nav-btn.active{color:var(--gold);background:var(--gold-dim)}

/* === Views === */
.view{display:none;animation:fadeIn .2s ease}
.view.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* === Badges === */
.badge{display:inline-flex;align-items:center;font-size:10px;font-weight:600;padding:3px 8px;border-radius:6px;letter-spacing:.3px}
.b-crit{background:rgba(248,81,73,.12);color:#f85149;border:1px solid rgba(248,81,73,.15)}
.b-high{background:rgba(210,153,34,.12);color:#d29922;border:1px solid rgba(210,153,34,.15)}
.b-med{background:rgba(88,166,255,.12);color:#58a6ff;border:1px solid rgba(88,166,255,.15)}
.b-low{background:rgba(63,185,80,.12);color:#3fb950;border:1px solid rgba(63,185,80,.15)}
.proj-pill{font-size:10px;padding:3px 8px;border-radius:6px;font-weight:500;white-space:nowrap}
.avatar-sm{width:22px;height:22px;border-radius:7px;display:inline-flex;align-items:center;justify-content:center;font-size:9px;font-weight:600;color:white;flex-shrink:0}
.avatar-xs{width:18px;height:18px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:8px;font-weight:600;color:white;flex-shrink:0;border:1.5px solid var(--bg-card)}
.collab-stack{display:inline-flex;align-items:center;margin-left:4px;vertical-align:middle}
.collab-stack .avatar-xs{margin-left:-6px}
.collab-stack .avatar-xs:first-child{margin-left:0}
.collab-more{font-size:9px;color:var(--text-muted);margin-left:4px;font-weight:600}
.collab-picker{display:flex;flex-wrap:wrap;gap:6px;padding:8px;background:var(--bg-deep,#0d1117);border:1px solid var(--border);border-radius:10px;max-height:160px;overflow-y:auto}
.collab-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 10px 5px 5px;background:var(--bg-card);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;transition:all .15s;color:var(--text-secondary);user-select:none}
.collab-chip:hover{border-color:var(--gold)}
.collab-chip.selected{background:rgba(198,163,80,.15);border-color:var(--gold);color:var(--text-primary)}
.collab-chip .avatar-sm{width:18px;height:18px;font-size:8px}
.collab-empty{padding:10px;color:var(--text-muted);font-size:12px;text-align:center;width:100%}
.sdot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:4px}
.overdue{color:var(--accent-red)!important;font-weight:500}

/* === Filters === */
.filters{display:flex;gap:6px;margin-bottom:14px;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:2px 0}
.filters::-webkit-scrollbar{display:none}
.fbtn{padding:6px 14px;font-size:11px;border:1px solid var(--border);border-radius:20px;background:transparent;cursor:pointer;color:var(--text-muted);font-family:inherit;transition:all .15s;white-space:nowrap;flex-shrink:0}
.fbtn:hover{border-color:var(--text-muted);color:var(--text-secondary)}
.fbtn.active{background:var(--gold);color:var(--bg-deep);border-color:var(--gold);font-weight:600}
.fbtn.toggle{margin-left:auto}
.fbtn.toggle::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--text-muted);margin-right:6px;vertical-align:middle}
.fbtn.toggle.active::before{background:var(--bg-deep)}

/* === Kanban === */
.kanban{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.kcol{background:var(--bg-card);border-radius:var(--radius-lg);padding:12px;min-height:200px;border:1px solid var(--border-light)}
.kcol-h{font-size:11px;font-weight:600;letter-spacing:1px;color:var(--text-muted);margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;text-transform:uppercase}
.kcol-n{background:var(--bg-surface);border-radius:6px;min-width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:11px;color:var(--text-secondary);padding:0 6px}
.kcard{background:var(--bg-surface);border-radius:var(--radius);padding:12px;margin-bottom:8px;border:1px solid var(--border-light);cursor:pointer;transition:all .15s}
.kcard:hover{border-color:var(--gold-border);transform:translateY(-2px);box-shadow:0 4px 20px rgba(0,0,0,.3)}
.kcard-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.kcard-title{font-size:13px;font-weight:500;margin-bottom:8px;line-height:1.4;color:var(--text-primary)}
.kcard-meta{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--text-muted)}
.kcard-assignee{display:flex;align-items:center;gap:6px}

/* === List Table === */
.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius-lg);border:1px solid var(--border-light)}
.ltbl{width:100%;border-collapse:collapse;font-size:13px}
.ltbl th{text-align:left;padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.8px;color:var(--text-muted);border-bottom:1px solid var(--border);text-transform:uppercase;background:var(--bg-card)}
.ltbl td{padding:10px 14px;border-bottom:1px solid var(--border-light);color:var(--text-primary)}
.ltbl tr{transition:background .1s}
.ltbl tr:hover{background:var(--bg-card)}
.td-title{font-weight:500;max-width:280px}

/* === Calendar === */
.cal-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.cal-title{font-size:18px;font-weight:600;color:var(--text-primary)}
.cal-nav{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:7px 12px;cursor:pointer;display:flex;align-items:center;color:var(--text-secondary);transition:all .15s}
.cal-nav:hover{background:var(--bg-surface);color:var(--gold)}
.cal-grid{background:var(--bg-card);border-radius:var(--radius-lg);border:1px solid var(--border-light);overflow:hidden}
.cal-days{display:grid;grid-template-columns:repeat(7,1fr);border-bottom:1px solid var(--border)}
.cal-day-name{padding:10px;text-align:center;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px}
.cal-cells{display:grid;grid-template-columns:repeat(7,1fr)}
.cal-cell{min-height:90px;border-right:1px solid var(--border-light);border-bottom:1px solid var(--border-light);padding:6px;cursor:pointer;transition:background .15s}
.cal-cell:nth-child(7n){border-right:none}
.cal-cell:hover{background:var(--bg-surface)}
.cal-cell.empty{background:rgba(0,0,0,.15);cursor:default}
.cal-cell.today{background:rgba(198,163,80,.04)}
.cal-cell.cal-weekend{background:rgba(139,148,158,.04)}
.cal-cell.cal-holiday{background:rgba(248,81,73,.06)}
.cal-cell.cal-holiday.cal-weekend{background:rgba(248,81,73,.08)}
.cal-day-name.cal-weekend-name{color:rgba(139,148,158,.6)}
.cal-holiday-label{font-size:9px;color:#f85149;font-weight:600;line-height:1.2;padding:1px 3px;text-transform:uppercase;letter-spacing:.3px;margin-bottom:2px}

/* Leave indicators in calendar */
.cal-leave-dots{display:flex;gap:3px;align-items:center;margin-bottom:3px;flex-wrap:wrap}
.cal-leave-dot{display:inline-block;width:8px;height:8px;border-radius:50%;flex-shrink:0}
.cal-leave-more{font-size:9px;color:var(--text-muted);font-weight:600;line-height:1}
.cal-date{font-size:12px;font-weight:500;color:var(--text-muted);display:block;margin-bottom:3px;padding:2px 4px}
.today-num{background:var(--gold);color:var(--bg-deep);border-radius:6px;width:24px;height:24px;display:inline-flex;align-items:center;justify-content:center;font-weight:600}
.cal-tasks{display:flex;flex-direction:column;gap:2px}
.cal-task{padding:2px 6px;border-radius:4px;font-size:10px;line-height:1.3;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;background:var(--bg-surface)}
.cal-task-text{color:var(--text-secondary)}
.cal-more{font-size:10px;color:var(--text-muted);padding:2px 4px}

/* === Projects === */
.proj-card{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:16px;margin-bottom:10px;transition:border-color .15s}
.proj-card:hover{border-color:var(--gold-border)}
.proj-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.proj-dot{width:10px;height:10px;border-radius:3px;display:inline-block;flex-shrink:0}
.proj-name{font-size:15px;font-weight:600;color:var(--text-primary)}
.proj-pct{font-size:13px;font-weight:500;color:var(--gold)}
.proj-bar{height:4px;background:var(--bg-surface);border-radius:2px;overflow:hidden;margin-bottom:8px}
.proj-fill{height:100%;border-radius:2px;transition:width .5s}
.proj-stats{font-size:12px;color:var(--text-muted);display:flex;gap:16px}

/* === Reports === */
.rpt-form{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:18px;margin-bottom:16px}
.rpt-form-title{font-size:15px;font-weight:600;margin-bottom:14px;color:var(--text-primary)}
.rpt-label{font-size:11px;font-weight:500;color:var(--text-muted);display:block;margin:12px 0 4px;letter-spacing:.3px;text-transform:uppercase}
.rpt-input{width:100%;padding:9px 12px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);font-size:13px;font-family:inherit;color:var(--text-primary);outline:none;transition:border .2s}
.rpt-input:focus{border-color:var(--gold-border)}
.rpt-item-row{margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid var(--border-light)}
.rpt-item-fields{display:flex;flex-direction:column;gap:8px}
.rpt-item-fields select{padding:8px 10px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);font-size:12px;font-family:inherit;color:var(--text-primary);outline:none}
.rpt-row-inner{display:flex;gap:8px;align-items:center}
.rpt-row-inner input[type="text"]{flex:1;padding:8px 10px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);font-size:12px;font-family:inherit;color:var(--text-primary);outline:none}
.rpt-row-inner input[type="number"]{padding:8px 10px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);font-size:12px;font-family:inherit;color:var(--text-primary);outline:none;width:70px}
.sect-title{font-size:14px;font-weight:600;color:var(--text-primary);margin:18px 0 10px}
.rpt-card{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius);padding:14px;margin-bottom:8px;transition:border-color .15s}
.rpt-card:hover{border-color:var(--gold-border)}
.rpt-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.rpt-name{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:500}
.rpt-hours-total{font-size:11px;font-weight:600;color:var(--gold);background:var(--gold-dim);padding:3px 10px;border-radius:20px}
.rpt-line{display:flex;align-items:flex-start;gap:8px;padding:4px 0;font-size:12px}
.rpt-check{width:16px;height:16px;border-radius:5px;background:var(--accent-green);flex-shrink:0;display:flex;align-items:center;justify-content:center;margin-top:1px}
.rpt-line-text{flex:1;color:var(--text-secondary);line-height:1.4}
.rpt-line-hrs{font-size:11px;color:var(--text-muted);white-space:nowrap}
.rpt-note{font-size:12px;color:var(--text-secondary);margin-top:10px;padding:10px 12px;background:var(--bg-surface);border-radius:var(--radius);border-left:3px solid var(--gold)}

/* === Dashboard === */
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}
.stat-card{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:14px;position:relative;overflow:hidden}
.stat-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.stat-card:nth-child(1)::after{background:var(--gold)}
.stat-card:nth-child(2)::after{background:var(--accent-green)}
.stat-card:nth-child(3)::after{background:var(--accent-red)}
.stat-card:nth-child(4)::after{background:var(--accent-amber)}
.stat-label{font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.8px;font-weight:600}
.stat-value{font-size:28px;font-weight:700;margin-top:4px}
.stat-sub{font-size:11px;color:var(--text-muted);margin-top:2px}
.chart-legend{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:8px;font-size:12px;color:var(--text-muted)}
.chart-legend span{display:flex;align-items:center;gap:5px}
.chart-legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
.chart-wrap{position:relative;height:200px;margin-bottom:18px}
.team-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.team-card{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:14px;text-align:center;transition:border-color .15s}
.team-card:hover{border-color:var(--gold-border)}
.team-avatar{width:40px;height:40px;border-radius:10px;margin:0 auto 8px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;color:white}
.team-name{font-size:13px;font-weight:500}
.team-info{font-size:11px;color:var(--text-muted);margin-top:3px}
.team-rpt{font-size:10px;margin-top:4px;padding:3px 8px;border-radius:6px;display:inline-block;font-weight:500}
.has-rpt{color:var(--accent-green);background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.15)}
.no-rpt{color:var(--accent-red);background:rgba(248,81,73,.08);border:1px solid rgba(248,81,73,.12)}
.progress-bar{height:3px;background:var(--bg-surface);border-radius:2px;margin-top:8px;overflow:hidden}
.progress-fill{height:100%;border-radius:2px}

/* === Admin === */
.admin-card{background:var(--bg-card);border:1px solid var(--border-light);border-radius:var(--radius);padding:14px 16px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;transition:border-color .15s}
.admin-card:hover{border-color:var(--gold-border)}
.admin-card-left{display:flex;align-items:center;gap:12px}
.admin-name{font-size:14px;font-weight:500;color:var(--text-primary)}
.admin-sub{font-size:12px;color:var(--text-muted)}
.admin-card-actions{display:flex;gap:6px}

/* === FAB === */
.fab{position:fixed;bottom:24px;right:24px;width:52px;height:52px;border-radius:14px;background:var(--gold);color:var(--bg-deep);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 24px rgba(198,163,80,.25);transition:all .15s;z-index:50}
.fab:hover{transform:translateY(-2px) scale(1.05);box-shadow:0 8px 32px rgba(198,163,80,.35)}
.fab:active{transform:scale(.95)}

/* === Modal === */
.modal-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);z-index:100;align-items:flex-start;justify-content:center;padding:60px 16px;overflow-y:auto}
.modal-overlay.show{display:flex}
.modal{background:var(--bg-card);border:1px solid var(--border);border-radius:16px;padding:0;width:100%;max-width:440px;overflow:hidden;animation:slideUp .25s ease-out}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.modal-header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid var(--border-light)}
.modal-header h3{font-size:16px;font-weight:600;color:var(--text-primary)}
.modal-close{background:none;border:none;font-size:22px;cursor:pointer;color:var(--text-muted);padding:4px 6px;line-height:1;border-radius:6px;transition:all .15s}
.modal-close:hover{color:var(--text-primary);background:var(--bg-surface)}
#modal-body{padding:16px 20px 20px}
#modal-body label{display:block;font-size:11px;font-weight:500;color:var(--text-muted);margin:12px 0 4px;letter-spacing:.3px;text-transform:uppercase}
#modal-body label:first-child{margin-top:0}
.modal-input{width:100%;padding:10px 12px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);font-size:14px;font-family:inherit;color:var(--text-primary);outline:none;transition:border .2s}
.modal-input:focus{border-color:var(--gold-border);box-shadow:0 0 0 3px rgba(198,163,80,.06)}
textarea.modal-input{resize:vertical}
.modal-actions{display:flex;gap:8px;margin-top:18px;justify-content:flex-end}

/* === Buttons === */
.btn-primary{padding:10px 22px;background:var(--gold);color:var(--bg-deep);border:none;border-radius:var(--radius);font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s;letter-spacing:.3px}
.btn-primary:hover{filter:brightness(1.1);transform:translateY(-1px)}
.btn-outline{padding:10px 22px;background:transparent;border:1px solid var(--border);border-radius:var(--radius);font-size:13px;cursor:pointer;font-family:inherit;color:var(--text-secondary);transition:all .15s}
.btn-outline:hover{border-color:var(--text-muted);color:var(--text-primary);background:var(--bg-surface)}
.btn-sm{padding:6px 12px!important;font-size:11px!important}
.btn-danger{padding:10px 22px;background:rgba(248,81,73,.08);color:var(--accent-red);border:1px solid rgba(248,81,73,.15);border-radius:var(--radius);font-size:13px;cursor:pointer;font-family:inherit;margin-right:auto;transition:all .15s}
.btn-danger:hover{background:rgba(248,81,73,.15)}

/* === Misc === */
.empty-state{text-align:center;padding:50px 20px;color:var(--text-muted);font-size:14px}
.day-tasks .rpt-card{cursor:pointer}

/* ==================
   MOBILE
   ================== */
@media(max-width:768px){
  .app{padding:0 12px 100px}
  .topbar{padding:10px 0;gap:6px}
  .logo img{height:20px}
  .logo-divider{height:16px}
  .logo-label{font-size:10px;letter-spacing:1px}
  .user-name{display:none}
  .user-info{gap:4px}
  .nav-btn{padding:8px 12px;font-size:12px;min-height:36px}
  .kanban{grid-template-columns:1fr!important;gap:8px}
  .kcol{min-height:auto}
  .stats-grid{grid-template-columns:repeat(2,1fr)}
  .team-grid{grid-template-columns:repeat(2,1fr)}
  .cal-cell{min-height:62px;padding:3px}
  .cal-date{font-size:11px}
  .cal-task{font-size:9px;padding:1px 3px}
  .cal-task-text{font-size:9px}
  .cal-holiday-label{display:none}
  .cal-cell.cal-holiday::after{content:'•';position:absolute;top:2px;right:4px;color:#f85149;font-size:14px;line-height:1;font-weight:bold}
  .cal-cell{position:relative}
  .today-num{width:22px;height:22px;font-size:11px;border-radius:6px}
  .hide-mobile{display:none!important}
  .td-title{max-width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .modal-overlay{padding:0;align-items:flex-end}
  .modal{max-width:100%;border-radius:16px 16px 0 0;max-height:90vh;overflow-y:auto}
  .fab{bottom:18px;right:18px;width:52px;height:52px;border-radius:14px}
  .rpt-row-inner{flex-wrap:wrap}
  .admin-card{flex-direction:column;align-items:flex-start}
  .admin-card-actions{width:100%}
  .admin-card-actions .btn-sm{flex:1;text-align:center}
  .notif-popup{right:8px;width:calc(100vw - 16px);max-width:320px}
  .notif-btn{padding:8px;min-width:36px;min-height:36px}
  .btn-primary,.btn-outline,.btn-danger{min-height:42px;font-size:14px}
  .btn-sm{min-height:32px!important}
  .modal-input{font-size:16px;padding:11px 12px}
  .stat-value{font-size:24px}
  .kcard{padding:12px}
  .kcard-title{font-size:14px}
}
@media(max-width:480px){
  .stats-grid{gap:6px}
  .stat-card{padding:10px}
  .stat-value{font-size:22px}
  .team-grid{gap:6px}
  .team-card{padding:10px}
  .cal-day-name{font-size:10px;padding:6px 2px}
  .cal-cell{min-height:54px}
  .cal-task-text{font-size:8px}
  .cal-task{padding:1px 2px}
  .nav{gap:0}
  .nav-btn{padding:8px 10px}
}
@media(min-width:769px) and (max-width:1024px){
  .kanban{grid-template-columns:repeat(2,1fr)!important}
}

/* iOS safe areas (notch, home indicator) */
@supports(padding:max(0px)){
  .app{padding-bottom:max(100px,env(safe-area-inset-bottom));padding-left:max(12px,env(safe-area-inset-left));padding-right:max(12px,env(safe-area-inset-right))}
  .fab{bottom:max(18px,env(safe-area-inset-bottom))}
}
'''

LOGIN = r'''<!DOCTYPE html>
<html lang="bg">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#0d1117">
<title>Helios Marine — Tasks</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;min-height:100vh;background:#0d1117;color:#e6edf3;display:flex;align-items:center;justify-content:center;overflow:hidden;position:relative}
body::before{content:'';position:absolute;top:-50%;right:-50%;width:100%;height:100%;background:radial-gradient(circle,rgba(198,163,80,.06) 0%,transparent 60%);pointer-events:none}
.login-wrap{position:relative;z-index:1;width:90%;max-width:400px}
.brand{text-align:center;margin-bottom:2rem}
.brand img{height:36px;opacity:.95;margin-bottom:12px}
.brand-sub{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:rgba(198,163,80,.6);font-weight:400}
.card{background:rgba(22,27,34,.8);backdrop-filter:blur(20px);border:1px solid rgba(198,163,80,.12);border-radius:16px;padding:2rem;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(198,163,80,.3),transparent)}
.card-title{font-size:18px;font-weight:600;margin-bottom:6px}
.card-sub{font-size:13px;color:#8b949e;margin-bottom:20px}
.field{margin-bottom:14px}
.field label{display:block;font-size:11px;font-weight:500;color:#8b949e;margin-bottom:5px;letter-spacing:.5px;text-transform:uppercase}
.field input{width:100%;padding:11px 14px;background:rgba(13,17,23,.6);border:1px solid rgba(255,255,255,.08);border-radius:10px;font-size:14px;color:#e6edf3;font-family:inherit;outline:none;transition:all .2s}
.field input:focus{border-color:rgba(198,163,80,.4);box-shadow:0 0 0 3px rgba(198,163,80,.08)}
.field input::placeholder{color:#484f58}
.btn-login{width:100%;padding:12px;background:linear-gradient(135deg,#c6a350,#a8893e);color:#0d1117;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;letter-spacing:.5px;transition:all .2s;margin-top:6px}
.btn-login:hover{filter:brightness(1.1);transform:translateY(-1px)}
.btn-login:active{transform:translateY(0)}
.error{color:#f85149;font-size:13px;text-align:center;margin-top:12px;padding:8px 12px;background:rgba(248,81,73,.08);border-radius:8px;border:1px solid rgba(248,81,73,.15)}
.hint{font-size:11px;color:#484f58;text-align:center;margin-top:16px;line-height:1.8}
.hint b{color:#8b949e;font-weight:500}
.boat-bg{position:fixed;bottom:-10%;right:-5%;width:55%;max-width:600px;opacity:.04;pointer-events:none;z-index:0}
@media(max-width:480px){.card{padding:1.5rem}.brand img{height:28px}.boat-bg{width:90%;bottom:-5%;right:-15%}}
</style>
</head>
<body>
<img src="/static/boat.png" class="boat-bg" alt="">
<div class="login-wrap">
    <div class="brand">
        <img src="/static/logo.png" alt="Helios Marine">
        <div class="brand-sub">Task management</div>
    </div>
    <div class="card">
        <div class="card-title" id="welcome-text">Добре дошъл</div>
        <div class="card-sub" id="subtitle-text">Влез в системата за управление на задачи</div>
        <form method="POST" action="/login">
            <div class="field">
                <label id="user-label">Потребител</label>
                <input type="text" name="username" id="user-input" placeholder="Потребителско име" required autofocus>
            </div>
            <div class="field">
                <label id="pass-label">Парола</label>
                <input type="password" name="password" id="pass-input" placeholder="Парола" required>
            </div>
            <button type="submit" class="btn-login" id="login-btn">Вход</button>
        </form>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
    <div style="text-align:center;margin-top:14px"><button onclick="toggleLang()" id="lang-toggle" style="background:none;border:1px solid rgba(198,163,80,.2);color:rgba(198,163,80,.7);padding:6px 14px;border-radius:8px;font-size:11px;font-weight:600;letter-spacing:.5px;cursor:pointer;font-family:inherit">EN</button></div>
</div>
<script>
const TXT = {
  bg: {welcome:'Добре дошъл', subtitle:'Влез в системата за управление на задачи', user:'Потребител', userPh:'Потребителско име', pass:'Парола', passPh:'Парола', btn:'Вход', toggle:'EN'},
  en: {welcome:'Welcome', subtitle:'Sign in to the task management system', user:'Username', userPh:'Username', pass:'Password', passPh:'Password', btn:'Sign in', toggle:'BG'}
};
let lang = localStorage.getItem('helios_lang') || 'bg';
function applyLang() {
  const x = TXT[lang];
  document.getElementById('welcome-text').textContent = x.welcome;
  document.getElementById('subtitle-text').textContent = x.subtitle;
  document.getElementById('user-label').textContent = x.user;
  document.getElementById('user-input').placeholder = x.userPh;
  document.getElementById('pass-label').textContent = x.pass;
  document.getElementById('pass-input').placeholder = x.passPh;
  document.getElementById('login-btn').textContent = x.btn;
  document.getElementById('lang-toggle').textContent = x.toggle;
  document.documentElement.lang = lang;
}
function toggleLang() { lang = lang === 'bg' ? 'en' : 'bg'; localStorage.setItem('helios_lang', lang); applyLang(); }
applyLang();
</script>
</body>
</html>
'''

APP = r'''<!DOCTYPE html>
<html lang="bg">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<meta name="theme-color" content="#0d1117">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>Helios Marine — Tasks</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<div class="app" id="app">
  <header class="topbar">
    <div class="logo">
      <img src="/static/logo.png" alt="Helios Marine">
      <div class="logo-divider"></div>
      <span class="logo-label">Tasks</span>
    </div>
    <div class="user-info">
      <button id="lang-btn" class="notif-btn" title="Language" onclick="setLanguage(LANG==='bg'?'en':'bg')" style="font-size:11px;font-weight:600;letter-spacing:.5px;min-width:32px">EN</button>
      <button id="notif-btn" class="notif-btn" title="Известия">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>
        <span id="notif-badge" class="notif-badge" style="display:none">0</span>
      </button>
      <button id="pass-btn" class="notif-btn" title="Смени паролата" onclick="openChangePasswordModal()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
      </button>
      <span class="user-name">{{ user.display_name }}</span>
      <span class="user-badge">{% if is_ceo %}CEO{% elif is_manager %}Мениджър{% else %}Служител{% endif %}</span>
      <a href="/logout" class="logout-btn" title="Изход">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
      </a>
    </div>
  </header>

  <nav class="nav" id="main-nav">
    <button class="nav-btn active" data-view="kanban">Kanban</button>
    <button class="nav-btn" data-view="list">Списък</button>
    <button class="nav-btn" data-view="calendar">Календар</button>
    <button class="nav-btn" data-view="projects">Проекти</button>
    <button class="nav-btn" data-view="reports">{% if is_ceo or is_manager %}Отчети{% else %}Дневен отчет{% endif %}</button>
    <button class="nav-btn" data-view="leave">Отпуски</button>
    {% if is_ceo %}<button class="nav-btn" data-view="dashboard">Dashboard</button>{% endif %}
    {% if is_ceo %}<button class="nav-btn" data-view="admin">Админ</button>{% endif %}
  </nav>

  <main>
    <div id="v-kanban" class="view active"></div>
    <div id="v-list" class="view"></div>
    <div id="v-calendar" class="view"></div>
    <div id="v-projects" class="view"></div>
    <div id="v-reports" class="view"></div>
    <div id="v-leave" class="view"></div>
    <div id="v-dashboard" class="view"></div>
    <div id="v-admin" class="view"></div>
  </main>

  <button class="fab" id="fab-add" title="Нова задача">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
  </button>
</div>

<div class="modal-overlay" id="modal-overlay">
  <div class="modal" id="modal">
    <div class="modal-header">
      <h3 id="modal-title"></h3>
      <button class="modal-close" id="modal-close">&times;</button>
    </div>
    <div id="modal-body"></div>
  </div>
</div>

<div id="notif-popup" class="notif-popup">
  <div class="notif-header">Известия</div>
  <div id="notif-list" class="notif-list"></div>
</div>

<script>
const IS_CEO = {{ "true" if is_ceo else "false" }};
const IS_MANAGER = {{ "true" if is_manager else "false" }};
const USER_ROLE = "{{ user_role }}";
const USER_ID = {{ user.id }};
const USERS = {{ users | tojson }};
const ALL_USERS = {{ all_users | tojson }};
const PROJECTS = {{ projects | tojson }};

// === I18N ===
const I18N = {
  bg: {
    // Roles
    role_ceo: 'CEO', role_manager: 'Мениджър', role_employee: 'Служител',
    // Nav
    nav_kanban: 'Kanban', nav_list: 'Списък', nav_calendar: 'Календар',
    nav_projects: 'Проекти', nav_reports_full: 'Отчети', nav_reports_self: 'Дневен отчет',
    nav_dashboard: 'Dashboard', nav_admin: 'Админ',
    // Priority/Status
    pri_critical: 'Критичен', pri_high: 'Висок', pri_medium: 'Среден', pri_low: 'Нисък',
    st_todo: 'Нови', st_progress: 'В работа', st_review: 'За преглед', st_done: 'Готови',
    // Filters
    f_all: 'Всички', only_mine: 'Само моите',
    // Collaborators
    collaborators: 'Сътрудници', add_collaborators_hint: 'Добави хора, които също участват',
    no_users_available: 'Няма налични потребители',
    creator_label: 'Създател',
    // Modals
    new_task: 'Нова задача', edit_task: 'Редактиране',
    title: 'Заглавие', description: 'Описание', project: 'Проект', priority: 'Приоритет',
    status: 'Статус', assignee: 'Отговорник', due_date: 'Краен срок', myself: 'Себе си',
    new_project: 'Нов проект', name: 'Име', color: 'Цвят',
    new_employee: 'Нов служител', edit: 'Редактиране',
    name_cyrillic: 'Име (кирилица)', username_latin: 'Потребителско име (латиница)',
    password: 'Парола', new_password_blank: 'Нова парола (празно = без промяна)',
    new_password_placeholder: 'Нова парола...', role: 'Роля',
    forgot_password: 'Забравена парола?', generate_new_password: 'Генерирай нова парола',
    sure_reset_password: 'Сигурен ли си, че искаш да генерираш нова парола за',
    old_password_will_not_work: 'Старата парола вече няма да работи.',
    new_password_generated: 'Нова парола генерирана',
    give_password_to: 'Дай тази парола на', not_shown_again: 'Тя няма да бъде показана отново.',
    suggest_change_first_login: 'Препоръка: помоли служителя да я смени при първи вход.',
    change_password: 'Смяна на парола', current_password: 'Текуща парола',
    new_password: 'Нова парола', repeat_new_password: 'Повтори новата парола',
    pass_min_4: 'Поне 4 символа', pass_too_short: 'Новата парола трябва да е поне 4 символа',
    pass_no_match: 'Двете нови пароли не съвпадат', wrong_old_pass: 'Грешна текуща парола',
    pass_changed: 'Паролата е сменена успешно.', error_occurred: 'Възникна грешка',
    visibility_for: 'Видимост на отчети —', visibility_help: 'Избери чии отчети може да вижда този мениджър:',
    no_employees: 'Няма служители',
    // Buttons
    cancel: 'Откажи', save: 'Запази', add: 'Добави', delete: 'Изтрий',
    create: 'Създай', sure: 'Сигурен ли си?', close: 'Затвори',
    download: 'Свали', visibility: 'Видимост', open_history: 'История на промените',
    no_history: 'Няма история',
    // Reports
    fill_daily_report: 'Попълни дневен отчет', select_task: '— Избери задача —',
    what_did_you_do: 'Какво направи...', more_row: '+ Още ред',
    notes_problems: 'Бележки / проблеми', something_important: 'Нещо важно...',
    submit_report: 'Изпрати отчет', no_reports_yet: 'Все още няма отчети',
    add_at_least_one: 'Добави поне един ред',
    hours_total: 'ч общо', hours_short: 'ч', tasks: 'задачи', done_count: 'готови',
    in_progress_count: 'в работа', overdue_count: 'просрочени',
    // Projects
    new_project_btn: '+ Нов проект', no_tasks_in_project: 'Няма задачи в този проект.',
    add_task_btn: '+ Добави задача', new_task_btn: '+ Нова задача',
    tasks_total: 'задачи общо', percent_done: '% завършен',
    // Admin
    employees: 'Служители', projects_admin: 'Проекти', new_employee_btn: '+ Нов служител',
    backups: 'Бекъпи на базата', create_backup_now: 'Създай бекъп сега',
    no_backups_yet: 'Все още няма бекъпи. Системата автоматично прави дневни бекъпи.',
    showing_backups: 'Показани 10 от', backups_count: 'бекъпа',
    delete_user_warn: 'Задачите му ще останат без отговорник.',
    delete_project_warn: 'Изтриване на проект',
    username_taken: 'Потребителското име вече съществува!',
    fill_name_username: 'Попълни име и потребителско име',
    delete_employee: 'Изтриване на',
    // Dashboard
    total: 'Общо', done: 'Готови', overdue: 'Просрочени', critical: 'Критични',
    team: 'Екип', has_report: 'днес', no_report: 'Няма отчет',
    employee_workload: 'натовареност', team_member_tasks: 'задачи /',
    // Notifications
    notifications: 'Известия', overdue_tasks: 'Просрочени задачи',
    due_today: 'Срок днес', active_tasks: 'Активни задачи',
    no_report_today: 'Не си попълнил отчет днес', team_no_report: 'Без отчет днес',
    all_under_control: 'Всичко е под контрол',
    // Calendar
    legend_holiday: 'Празник', legend_weekend: 'Уикенд', legend_today: 'Днес',
    months: ['Януари','Февруари','Март','Април','Май','Юни','Юли','Август','Септември','Октомври','Ноември','Декември'],
    days: ['Пн','Вт','Ср','Чт','Пт','Сб','Нд'],
    // Holiday names
    h_new_year: 'Нова година', h_liberation: 'Освобождение', h_labour: 'Ден на труда',
    h_george: 'Гергьовден', h_letters: 'Ден на буквите', h_unification: 'Съединение',
    h_independence: 'Независимост', h_enlighteners: 'Народни будители',
    h_christmas_eve: 'Бъдни вечер', h_christmas: 'Рождество',
    h_good_friday: 'Разпети петък', h_holy_saturday: 'Велика събота',
    h_easter: 'Великден', h_easter_monday: 'Велики понеделник',
    // Audit log actions
    a_created: 'Създадена', a_updated: 'Промяна', a_deleted: 'Изтрита',
    a_reset_password: 'Парола сменена',
    f_title: 'заглавие', f_description: 'описание', f_priority: 'приоритет',
    f_status: 'статус', f_assignee_id: 'отговорник', f_project_id: 'проект',
    f_due_date: 'срок',
    // Login + topbar
    welcome: 'Добре дошъл', logout: 'Изход',
    notif_title: 'Известия',
    // Leave
    nav_leave: 'Отпуски',
    leave_title: 'Отпуски',
    leave_balance: 'Годишен баланс',
    leave_used: 'Ползвани',
    leave_remaining: 'Оставащи',
    leave_days: 'дни',
    leave_request: 'Заявка за отпуск',
    new_leave_request: '+ Нова заявка',
    leave_type: 'Тип отпуск',
    leave_paid: 'Платен',
    leave_sick: 'Болничен',
    leave_unpaid: 'Неплатен',
    leave_other: 'Друго',
    leave_start: 'От',
    leave_end: 'До',
    leave_reason: 'Причина / бележка',
    leave_reason_ph: 'Незадължително...',
    leave_working_days: 'работни дни',
    leave_status_pending: 'Чака одобрение',
    leave_status_approved: 'Одобрен',
    leave_status_rejected: 'Отхвърлен',
    leave_pending_approval: 'За одобрение',
    leave_my_requests: 'Моите заявки',
    leave_team_requests: 'Заявки на екипа',
    leave_all_requests: 'Всички заявки',
    leave_no_requests: 'Няма заявки',
    leave_approve: 'Одобри',
    leave_reject: 'Отхвърли',
    leave_cancel: 'Откажи заявка',
    leave_approved_by: 'Одобрено от',
    leave_rejected_by: 'Отхвърлено от',
    leave_decision_note: 'Бележка',
    leave_decision_note_ph: 'Бележка към решението (незадължително)',
    leave_submit: 'Подай заявка',
    leave_insufficient: 'Недостатъчни оставащи дни',
    leave_remaining_colon: 'Оставащи:',
    leave_requested_colon: 'Заявени:',
    leave_end_before_start: 'Крайната дата е преди началната',
    leave_confirm_cancel: 'Сигурен ли си, че искаш да откажеш тази заявка?',
    leave_sure_reject: 'Отхвърли ли заявката?',
    leave_pending_notif: 'Заявки за одобрение',
    leave_set_balance: 'Настрой баланс',
    leave_balance_for: 'Баланс за',
    leave_year: 'Година',
    leave_total_days: 'Общо дни',
  },
  en: {
    role_ceo: 'CEO', role_manager: 'Manager', role_employee: 'Employee',
    nav_kanban: 'Kanban', nav_list: 'List', nav_calendar: 'Calendar',
    nav_projects: 'Projects', nav_reports_full: 'Reports', nav_reports_self: 'Daily report',
    nav_dashboard: 'Dashboard', nav_admin: 'Admin',
    pri_critical: 'Critical', pri_high: 'High', pri_medium: 'Medium', pri_low: 'Low',
    st_todo: 'To do', st_progress: 'In progress', st_review: 'Review', st_done: 'Done',
    f_all: 'All', only_mine: 'Only mine',
    collaborators: 'Collaborators', add_collaborators_hint: 'Add other people involved',
    no_users_available: 'No users available',
    creator_label: 'Creator',
    new_task: 'New task', edit_task: 'Edit task',
    title: 'Title', description: 'Description', project: 'Project', priority: 'Priority',
    status: 'Status', assignee: 'Assignee', due_date: 'Due date', myself: 'Myself',
    new_project: 'New project', name: 'Name', color: 'Color',
    new_employee: 'New employee', edit: 'Edit',
    name_cyrillic: 'Display name', username_latin: 'Username',
    password: 'Password', new_password_blank: 'New password (blank = no change)',
    new_password_placeholder: 'New password...', role: 'Role',
    forgot_password: 'Forgot password?', generate_new_password: 'Generate new password',
    sure_reset_password: 'Are you sure you want to reset password for',
    old_password_will_not_work: 'The old password will no longer work.',
    new_password_generated: 'New password generated',
    give_password_to: 'Give this password to', not_shown_again: 'It will not be shown again.',
    suggest_change_first_login: 'Tip: ask the user to change it on first login.',
    change_password: 'Change password', current_password: 'Current password',
    new_password: 'New password', repeat_new_password: 'Repeat new password',
    pass_min_4: 'At least 4 characters', pass_too_short: 'New password must be at least 4 characters',
    pass_no_match: 'New passwords do not match', wrong_old_pass: 'Wrong current password',
    pass_changed: 'Password changed successfully.', error_occurred: 'An error occurred',
    visibility_for: 'Report visibility —', visibility_help: 'Select whose reports this manager can see:',
    no_employees: 'No employees',
    cancel: 'Cancel', save: 'Save', add: 'Add', delete: 'Delete',
    create: 'Create', sure: 'Are you sure?', close: 'Close',
    download: 'Download', visibility: 'Visibility', open_history: 'Change history',
    no_history: 'No history',
    fill_daily_report: 'Fill daily report', select_task: '— Select task —',
    what_did_you_do: 'What did you do...', more_row: '+ Add row',
    notes_problems: 'Notes / issues', something_important: 'Anything important...',
    submit_report: 'Submit report', no_reports_yet: 'No reports yet',
    add_at_least_one: 'Add at least one row',
    hours_total: 'h total', hours_short: 'h', tasks: 'tasks', done_count: 'done',
    in_progress_count: 'in progress', overdue_count: 'overdue',
    new_project_btn: '+ New project', no_tasks_in_project: 'No tasks in this project.',
    add_task_btn: '+ Add task', new_task_btn: '+ New task',
    tasks_total: 'total tasks', percent_done: '% done',
    employees: 'Employees', projects_admin: 'Projects', new_employee_btn: '+ New employee',
    backups: 'Database backups', create_backup_now: 'Create backup now',
    no_backups_yet: 'No backups yet. The system creates daily backups automatically.',
    showing_backups: 'Showing 10 of', backups_count: 'backups',
    delete_user_warn: 'Their tasks will remain without an assignee.',
    delete_project_warn: 'Delete project',
    username_taken: 'Username already exists!',
    fill_name_username: 'Fill in name and username',
    delete_employee: 'Delete',
    total: 'Total', done: 'Done', overdue: 'Overdue', critical: 'Critical',
    team: 'Team', has_report: 'today', no_report: 'No report',
    employee_workload: 'workload', team_member_tasks: 'tasks /',
    notifications: 'Notifications', overdue_tasks: 'Overdue tasks',
    due_today: 'Due today', active_tasks: 'Active tasks',
    no_report_today: 'You have not filled a report today', team_no_report: 'No report today',
    all_under_control: 'All under control',
    legend_holiday: 'Holiday', legend_weekend: 'Weekend', legend_today: 'Today',
    months: ['January','February','March','April','May','June','July','August','September','October','November','December'],
    days: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    h_new_year: 'New Year', h_liberation: 'Liberation Day', h_labour: 'Labour Day',
    h_george: "St. George's Day", h_letters: 'Cyrillic Alphabet Day', h_unification: 'Unification',
    h_independence: 'Independence Day', h_enlighteners: 'Enlighteners Day',
    h_christmas_eve: 'Christmas Eve', h_christmas: 'Christmas',
    h_good_friday: 'Good Friday', h_holy_saturday: 'Holy Saturday',
    h_easter: 'Easter', h_easter_monday: 'Easter Monday',
    a_created: 'Created', a_updated: 'Updated', a_deleted: 'Deleted',
    a_reset_password: 'Password reset',
    f_title: 'title', f_description: 'description', f_priority: 'priority',
    f_status: 'status', f_assignee_id: 'assignee', f_project_id: 'project',
    f_due_date: 'due date',
    welcome: 'Welcome', logout: 'Logout',
    notif_title: 'Notifications',
    // Leave
    nav_leave: 'Leave',
    leave_title: 'Leave',
    leave_balance: 'Annual balance',
    leave_used: 'Used',
    leave_remaining: 'Remaining',
    leave_days: 'days',
    leave_request: 'Leave request',
    new_leave_request: '+ New request',
    leave_type: 'Leave type',
    leave_paid: 'Paid',
    leave_sick: 'Sick',
    leave_unpaid: 'Unpaid',
    leave_other: 'Other',
    leave_start: 'From',
    leave_end: 'To',
    leave_reason: 'Reason / note',
    leave_reason_ph: 'Optional...',
    leave_working_days: 'working days',
    leave_status_pending: 'Pending',
    leave_status_approved: 'Approved',
    leave_status_rejected: 'Rejected',
    leave_pending_approval: 'For approval',
    leave_my_requests: 'My requests',
    leave_team_requests: 'Team requests',
    leave_all_requests: 'All requests',
    leave_no_requests: 'No requests',
    leave_approve: 'Approve',
    leave_reject: 'Reject',
    leave_cancel: 'Cancel request',
    leave_approved_by: 'Approved by',
    leave_rejected_by: 'Rejected by',
    leave_decision_note: 'Note',
    leave_decision_note_ph: 'Decision note (optional)',
    leave_submit: 'Submit request',
    leave_insufficient: 'Insufficient remaining days',
    leave_remaining_colon: 'Remaining:',
    leave_requested_colon: 'Requested:',
    leave_end_before_start: 'End date is before start date',
    leave_confirm_cancel: 'Are you sure you want to cancel this request?',
    leave_sure_reject: 'Reject the request?',
    leave_pending_notif: 'Pending requests',
    leave_set_balance: 'Set balance',
    leave_balance_for: 'Balance for',
    leave_year: 'Year',
    leave_total_days: 'Total days',
  }
};

let LANG = localStorage.getItem('helios_lang') || 'bg';
let T = I18N[LANG];

function t(key) { return T[key] || key; }

function setLanguage(lang) {
  if (!I18N[lang]) return;
  LANG = lang;
  T = I18N[lang];
  MONTHS = T.months;
  DAYS = T.days;
  localStorage.setItem('helios_lang', lang);
  applyStaticTranslations();
  switchView(curView);
  loadNotifications();
}

function applyStaticTranslations() {
  // Topbar role badge
  const roleBadge = document.querySelector('.user-badge');
  if (roleBadge) roleBadge.textContent = USER_ROLE === 'ceo' ? t('role_ceo') : USER_ROLE === 'manager' ? t('role_manager') : t('role_employee');
  // Nav buttons
  const navMap = {kanban: 'nav_kanban', list: 'nav_list', calendar: 'nav_calendar', projects: 'nav_projects', leave: 'nav_leave', dashboard: 'nav_dashboard', admin: 'nav_admin'};
  document.querySelectorAll('.nav-btn').forEach(btn => {
    const v = btn.dataset.view;
    if (navMap[v]) btn.textContent = t(navMap[v]);
    if (v === 'reports') btn.textContent = (IS_CEO || IS_MANAGER) ? t('nav_reports_full') : t('nav_reports_self');
  });
  // Notifications header
  const notifHeader = document.querySelector('.notif-header');
  if (notifHeader) notifHeader.textContent = t('notif_title');
  // Tooltips
  const fab = document.getElementById('fab-add');
  if (fab) fab.title = t('new_task');
  const passBtn = document.getElementById('pass-btn');
  if (passBtn) passBtn.title = t('change_password');
  const notifBtn = document.getElementById('notif-btn');
  if (notifBtn) notifBtn.title = t('notifications');
  // Lang button label
  const langBtn = document.getElementById('lang-btn');
  if (langBtn) langBtn.textContent = LANG === 'bg' ? 'EN' : 'BG';
  document.documentElement.lang = LANG;
}

// Legacy aliases - many existing functions reference these
const PL_KEYS = ['critical','high','medium','low'];
const SL_KEYS = ['todo','progress','review','done'];
const PL = new Proxy({}, {
  get(_, k) { return t('pri_' + k); },
  ownKeys() { return PL_KEYS; },
  getOwnPropertyDescriptor() { return {enumerable: true, configurable: true}; }
});
const SL = new Proxy({}, {
  get(_, k) { return t('st_' + k); },
  ownKeys() { return SL_KEYS; },
  getOwnPropertyDescriptor() { return {enumerable: true, configurable: true}; }
});
const SC = {todo:'#8b949e',progress:'#58a6ff',review:'#d29922',done:'#3fb950'};
let MONTHS = T.months;
let DAYS = T.days;

let allTasks = [];
let curView = 'kanban';
let kFilter = 'all';
let onlyMine = localStorage.getItem('helios_only_mine_'+USER_ID) === '1';
function isMine(task){
  if (task.created_by === USER_ID) return true;
  if (task.assignee_id === USER_ID) return true;
  if (task.collaborators && task.collaborators.some(c => c.id === USER_ID)) return true;
  return false;
}
function toggleOnlyMine(){
  onlyMine = !onlyMine;
  localStorage.setItem('helios_only_mine_'+USER_ID, onlyMine ? '1' : '0');
  if (curView === 'kanban') renderKanban();
  else if (curView === 'list') renderList();
  else if (curView === 'calendar') loadCalendar();
}
let calMonth, calYear;

const now = new Date();
calMonth = now.getMonth() + 1;
calYear = now.getFullYear();

document.querySelectorAll('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => switchView(btn.dataset.view));
});
document.getElementById('fab-add').addEventListener('click', openTaskModal);
document.getElementById('modal-close').addEventListener('click', closeModal);
document.getElementById('modal-overlay').addEventListener('click', e => {
  if (e.target === e.currentTarget) closeModal();
});
document.getElementById('notif-btn').addEventListener('click', e => {
  e.stopPropagation();
  const popup = document.getElementById('notif-popup');
  popup.classList.toggle('show');
});
document.addEventListener('click', e => {
  const popup = document.getElementById('notif-popup');
  const btn = document.getElementById('notif-btn');
  if (popup && !popup.contains(e.target) && !btn.contains(e.target)) {
    popup.classList.remove('show');
  }
});
applyStaticTranslations();
loadTasks();
loadNotifications();
setInterval(loadNotifications, 60000);

async function loadNotifications() {
  try {
    const res = await fetch('/api/notifications');
    const n = await res.json();
    const total = (n.overdue||0) + (n.team_no_report||0) + (n.pending_leave||0) + (!n.has_report_today && USER_ROLE === 'employee' ? 1 : 0);
    const badge = document.getElementById('notif-badge');
    if (total > 0) { badge.textContent = total > 99 ? '99+' : total; badge.style.display = 'flex'; }
    else { badge.style.display = 'none'; }
    
    const list = document.getElementById('notif-list');
    let html = '';
    if (n.overdue > 0) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('kanban')">
        <div class="notif-icon" style="background:rgba(248,81,73,.15);color:#f85149">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        </div>
        <div class="notif-content"><span>${t('overdue_tasks')}</span><span class="notif-count" style="color:#f85149">${n.overdue}</span></div>
      </div>`;
    }
    if (n.today > 0) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('calendar')">
        <div class="notif-icon" style="background:rgba(210,153,34,.15);color:#d29922">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <div class="notif-content"><span>${t('due_today')}</span><span class="notif-count" style="color:#d29922">${n.today}</span></div>
      </div>`;
    }
    if (n.active > 0) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('list')">
        <div class="notif-icon" style="background:rgba(88,166,255,.15);color:#58a6ff">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
        </div>
        <div class="notif-content"><span>${t('active_tasks')}</span><span class="notif-count">${n.active}</span></div>
      </div>`;
    }
    if (USER_ROLE === 'employee' && !n.has_report_today) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('reports')">
        <div class="notif-icon" style="background:rgba(198,163,80,.15);color:#c6a350">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
        </div>
        <div class="notif-content"><span style="color:#c6a350">${t('no_report_today')}</span></div>
      </div>`;
    }
    if ((USER_ROLE === 'ceo' || USER_ROLE === 'manager') && n.team_no_report > 0) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('reports')">
        <div class="notif-icon" style="background:rgba(198,163,80,.15);color:#c6a350">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
        </div>
        <div class="notif-content"><span>${t('team_no_report')}</span><span class="notif-count" style="color:#c6a350">${n.team_no_report}</span></div>
      </div>`;
    }
    if ((USER_ROLE === 'ceo' || USER_ROLE === 'manager') && n.pending_leave > 0) {
      html += `<div class="notif-item" onclick="document.getElementById('notif-popup').classList.remove('show');switchView('leave')">
        <div class="notif-icon" style="background:rgba(88,166,255,.15);color:#58a6ff">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        </div>
        <div class="notif-content"><span>${t('leave_pending_notif')}</span><span class="notif-count" style="color:#58a6ff">${n.pending_leave}</span></div>
      </div>`;
    }
    if (!html) html = `<div class="notif-empty">${t('all_under_control')}</div>`;
    list.innerHTML = html;
  } catch(e) { console.error(e); }
}

function switchView(v) {
  curView = v;
  document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('v-' + v).classList.add('active');
  document.querySelector(`.nav-btn[data-view="${v}"]`).classList.add('active');
  if (v === 'kanban') renderKanban();
  else if (v === 'list') renderList();
  else if (v === 'calendar') loadCalendar();
  else if (v === 'projects') loadProjects();
  else if (v === 'reports') loadReports();
  else if (v === 'leave') loadLeave();
  else if (v === 'dashboard') loadDashboard();
  else if (v === 'admin') loadAdmin();
}

async function loadTasks() {
  const res = await fetch('/api/tasks');
  allTasks = await res.json();
  renderKanban();
}

function badgeClass(pr) { return pr==='critical'?'b-crit':pr==='high'?'b-high':pr==='medium'?'b-med':'b-low'; }
function isOverdue(t) { return t.due_date && new Date(t.due_date) < new Date() && t.status !== 'done'; }

function collabStackHtml(collabs) {
  if (!collabs || !collabs.length) return '';
  const max = 3;
  const visible = collabs.slice(0, max);
  let html = '<span class="collab-stack">';
  visible.forEach(c => { html += `<span class="avatar-xs" style="background:${c.color}" title="${c.display_name}">${c.initials}</span>`; });
  html += '</span>';
  if (collabs.length > max) html += `<span class="collab-more">+${collabs.length - max}</span>`;
  return html;
}

function taskCard(t) {
  const od = isOverdue(t);
  return `<div class="kcard" onclick="openEditTask(${t.id})">
    <div class="kcard-top">
      <span class="badge ${badgeClass(t.priority)}">${PL[t.priority]}</span>
      <span class="proj-pill" style="background:${t.project_color||'#8b949e'}18;color:${t.project_color||'#8b949e'}">${t.project_name||'—'}</span>
    </div>
    <div class="kcard-title">${t.title}</div>
    <div class="kcard-meta">
      <span class="kcard-assignee"><span class="avatar-sm" style="background:${t.assignee_color||'#8b949e'}">${t.assignee_initials||'?'}</span>${t.assignee_name||'—'}${collabStackHtml(t.collaborators)}</span>
      <span class="${od?'overdue':''}">${t.due_date||'—'}</span>
    </div>
  </div>`;
}

function renderKanban() {
  let tasks = allTasks;
  if (onlyMine) tasks = tasks.filter(isMine);
  if (kFilter !== 'all') tasks = tasks.filter(t => t.priority === kFilter);
  let html = `<div class="filters">${['all','critical','high','medium','low'].map(f =>
    `<button class="fbtn ${kFilter===f?'active':''}" onclick="kFilter='${f}';renderKanban()">${f==='all'?t('f_all'):PL[f]}</button>`
  ).join('')}<button class="fbtn toggle ${onlyMine?'active':''}" onclick="toggleOnlyMine()">${t('only_mine')}</button></div><div class="kanban">`;
  ['todo','progress','review','done'].forEach(s => {
    const ft = tasks.filter(t => t.status === s);
    html += `<div class="kcol"><div class="kcol-h"><span>${SL[s]}</span><span class="kcol-n">${ft.length}</span></div>`;
    ft.forEach(t => html += taskCard(t));
    html += `</div>`;
  });
  html += `</div>`;
  document.getElementById('v-kanban').innerHTML = html;
}

function renderList() {
  let tasks = allTasks;
  if (onlyMine) tasks = tasks.filter(isMine);
  const sorted = [...tasks].sort((a,b) => ({critical:0,high:1,medium:2,low:3})[a.priority] - ({critical:0,high:1,medium:2,low:3})[b.priority]);
  let html = `<div class="filters"><button class="fbtn toggle ${onlyMine?'active':''}" onclick="toggleOnlyMine()">${t('only_mine')}</button></div>`;
  html += `<div class="table-wrap"><table class="ltbl"><thead><tr>
    <th>Задача</th><th class="hide-mobile">${t('project')}</th><th>${t('priority')}</th>
    <th class="hide-mobile">${t('assignee')}</th><th class="hide-mobile">Срок</th><th>${t('status')}</th></tr></thead><tbody>`;
  sorted.forEach(t => {
    html += `<tr onclick="openEditTask(${t.id})" style="cursor:pointer">
      <td class="td-title">${t.title}${collabStackHtml(t.collaborators)}</td>
      <td class="hide-mobile"><span class="proj-pill" style="background:${t.project_color||'#8b949e'}18;color:${t.project_color||'#8b949e'}">${t.project_name||'—'}</span></td>
      <td><span class="badge ${badgeClass(t.priority)}">${PL[t.priority]}</span></td>
      <td class="hide-mobile"><span class="kcard-assignee"><span class="avatar-sm" style="background:${t.assignee_color||'#8b949e'}">${t.assignee_initials||'?'}</span>${t.assignee_name||''}</span></td>
      <td class="hide-mobile ${isOverdue(t)?'overdue':''}">${t.due_date||'—'}</td>
      <td><span class="sdot" style="background:${SC[t.status]}"></span><span class="hide-mobile">${SL[t.status]}</span></td></tr>`;
  });
  html += `</tbody></table></div>`;
  document.getElementById('v-list').innerHTML = html;
}

async function loadCalendar() {
  const [res, leaveRes] = await Promise.all([
    fetch(`/api/calendar?month=${calMonth}&year=${calYear}`),
    fetch(`/api/leave/calendar?month=${calMonth}&year=${calYear}`)
  ]);
  const data = await res.json();
  data.leave = await leaveRes.json();
  if (onlyMine && data.tasks) data.tasks = data.tasks.filter(isMine);
  renderCalendar(data);
}

// Calculate Orthodox Easter (Sunday) for a given year - Meeus algorithm
function orthodoxEaster(year) {
  const a = year % 4, b = year % 7, c = year % 19;
  const d = (19*c + 15) % 30;
  const e = (2*a + 4*b - d + 34) % 7;
  const month = Math.floor((d + e + 114) / 31);
  const day = ((d + e + 114) % 31) + 1;
  // Convert from Julian to Gregorian (add 13 days for 1900-2099)
  const julianDate = new Date(year, month - 1, day);
  julianDate.setDate(julianDate.getDate() + 13);
  return julianDate;
}

function getBulgarianHolidays(year) {
  // Fixed holidays
  const holidays = {
    [`${year}-01-01`]: t('h_new_year'),
    [`${year}-03-03`]: t('h_liberation'),
    [`${year}-05-01`]: t('h_labour'),
    [`${year}-05-06`]: t('h_george'),
    [`${year}-05-24`]: t('h_letters'),
    [`${year}-09-06`]: t('h_unification'),
    [`${year}-09-22`]: t('h_independence'),
    [`${year}-11-01`]: t('h_enlighteners'),
    [`${year}-12-24`]: t('h_christmas_eve'),
    [`${year}-12-25`]: t('h_christmas'),
    [`${year}-12-26`]: t('h_christmas'),
  };
  // Easter-based holidays
  const easter = orthodoxEaster(year);
  const goodFriday = new Date(easter); goodFriday.setDate(easter.getDate() - 2);
  const holySaturday = new Date(easter); holySaturday.setDate(easter.getDate() - 1);
  const easterMonday = new Date(easter); easterMonday.setDate(easter.getDate() + 1);
  const fmt = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  holidays[fmt(goodFriday)] = t('h_good_friday');
  holidays[fmt(holySaturday)] = t('h_holy_saturday');
  holidays[fmt(easter)] = t('h_easter');
  holidays[fmt(easterMonday)] = t('h_easter_monday');
  return holidays;
}

function renderCalendar(data) {
  const firstDay = new Date(calYear, calMonth-1, 1);
  const lastDay = new Date(calYear, calMonth, 0);
  let startDow = firstDay.getDay(); startDow = startDow===0?6:startDow-1;
  const totalDays = lastDay.getDate();
  const todayStr = new Date().toISOString().split('T')[0];
  const holidays = getBulgarianHolidays(calYear);
  const byDate = {};
  data.tasks.forEach(t => { if(!byDate[t.due_date]) byDate[t.due_date]=[]; byDate[t.due_date].push(t); });
  // Expand leave entries into per-day map
  const leaveByDate = {};
  (data.leave||[]).forEach(lv => {
    const sd = new Date(lv.start_date), ed = new Date(lv.end_date);
    const cur = new Date(sd);
    while (cur <= ed) {
      const k = `${cur.getFullYear()}-${String(cur.getMonth()+1).padStart(2,'0')}-${String(cur.getDate()).padStart(2,'0')}`;
      if (!leaveByDate[k]) leaveByDate[k] = [];
      leaveByDate[k].push(lv);
      cur.setDate(cur.getDate()+1);
    }
  });
  let html = `<div class="filters" style="margin-bottom:10px"><button class="fbtn toggle ${onlyMine?'active':''}" onclick="toggleOnlyMine()">${t('only_mine')}</button></div>
  <div class="cal-header">
    <button class="cal-nav" onclick="calMonth--;if(calMonth<1){calMonth=12;calYear--;}loadCalendar()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button>
    <span class="cal-title">${MONTHS[calMonth-1]} ${calYear}</span>
    <button class="cal-nav" onclick="calMonth++;if(calMonth>12){calMonth=1;calYear++;}loadCalendar()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></button>
  </div><div class="cal-grid"><div class="cal-days">${DAYS.map((d,i)=>`<div class="cal-day-name${i>=5?' cal-weekend-name':''}">${d}</div>`).join('')}</div><div class="cal-cells">`;
  for(let i=0;i<startDow;i++) html+=`<div class="cal-cell empty"></div>`;
  for(let d=1;d<=totalDays;d++){
    const ds=`${calYear}-${String(calMonth).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    const dateObj = new Date(calYear, calMonth-1, d);
    const dow = dateObj.getDay();
    const isWeekend = dow === 0 || dow === 6;
    const holidayName = holidays[ds];
    const isToday=ds===todayStr;
    const dt=byDate[ds]||[];
    const lvs=leaveByDate[ds]||[];
    const cellClasses = ['cal-cell'];
    if(isToday) cellClasses.push('today');
    if(isWeekend) cellClasses.push('cal-weekend');
    if(holidayName) cellClasses.push('cal-holiday');
    // Build leave dots (up to 3) + count badge if more
    let leaveDots = '';
    if(lvs.length) {
      const shown = lvs.slice(0,3);
      leaveDots = `<div class="cal-leave-dots">${shown.map(lv => `<span class="cal-leave-dot" style="background:${LEAVE_TYPE_COLORS[lv.leave_type]};${lv.status==='pending'?'opacity:.5':''}" title="${lv.display_name} — ${LEAVE_TYPE_LABELS()[lv.leave_type]}"></span>`).join('')}${lvs.length>3?`<span class="cal-leave-more">+${lvs.length-3}</span>`:''}</div>`;
    }
    html+=`<div class="${cellClasses.join(' ')}" onclick="showDayTasks('${ds}')" ${holidayName?`title="${holidayName}"`:''}>
      <span class="cal-date ${isToday?'today-num':''}">${d}</span>
      ${holidayName?`<div class="cal-holiday-label">${holidayName}</div>`:''}
      ${leaveDots}
      <div class="cal-tasks">`;
    dt.slice(0,3).forEach(ti=>{html+=`<div class="cal-task" style="border-left:2px solid ${SC[ti.status]}"><span class="cal-task-text">${ti.title.length>16?ti.title.substring(0,16)+'...':ti.title}</span></div>`;});
    if(dt.length>3) html+=`<div class="cal-more">+${dt.length-3}</div>`;
    html+=`</div></div>`;
  }
  html+=`</div></div>`;
  // Legend
  html+=`<div style="display:flex;gap:14px;margin-top:10px;font-size:11px;color:#8b949e;flex-wrap:wrap">
    <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;border-radius:2px;background:rgba(248,81,73,.12);border:1px solid rgba(248,81,73,.2)"></span>${t('legend_holiday')}</span>
    <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;border-radius:2px;background:rgba(139,148,158,.12)"></span>${t('legend_weekend')}</span>
    <span style="display:flex;align-items:center;gap:6px"><span style="width:10px;height:10px;border-radius:2px;background:rgba(198,163,80,.08)"></span>${t('legend_today')}</span>
    <span style="display:flex;align-items:center;gap:6px"><span class="cal-leave-dot" style="background:${LEAVE_TYPE_COLORS.paid}"></span>${t('leave_paid')}</span>
    <span style="display:flex;align-items:center;gap:6px"><span class="cal-leave-dot" style="background:${LEAVE_TYPE_COLORS.sick}"></span>${t('leave_sick')}</span>
    <span style="display:flex;align-items:center;gap:6px"><span class="cal-leave-dot" style="background:${LEAVE_TYPE_COLORS.unpaid}"></span>${t('leave_unpaid')}</span>
  </div>`;
  document.getElementById('v-calendar').innerHTML=html;
}
window.showDayTasks=function(ds){
  const dt=allTasks.filter(t=>t.due_date===ds); if(!dt.length) return;
  const d=new Date(ds);
  openModal(`${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`,
    `<div class="day-tasks">${dt.map(t=>`<div class="rpt-card" onclick="closeModal();openEditTask(${t.id})" style="cursor:pointer">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <span class="badge ${badgeClass(t.priority)}">${PL[t.priority]}</span><span class="sdot" style="background:${SC[t.status]}"></span></div>
      <div style="font-weight:500;font-size:14px;margin-bottom:4px">${t.title}</div>
      <div style="font-size:12px;color:#8b949e;display:flex;justify-content:space-between"><span>${t.assignee_name||'—'}</span><span>${t.project_name||'—'}</span></div>
    </div>`).join('')}</div>`);
};

async function loadProjects(){
  const res=await fetch('/api/projects/list'); const projects=await res.json();
  let html='';
  projects.forEach(p=>{
    const pct=p.total_tasks?Math.round(p.done_tasks/p.total_tasks*100):0;
    html+=`<div class="proj-card" onclick="showProjectTasks(${p.id},'${p.name.replace(/'/g,"\\'")}','${p.color}')" style="cursor:pointer"><div class="proj-head"><div style="display:flex;align-items:center;gap:8px">
      <span class="proj-dot" style="background:${p.color}"></span><span class="proj-name">${p.name}</span></div>
      <span class="proj-pct">${pct}%</span></div>
      <div class="proj-bar"><div class="proj-fill" style="width:${pct}%;background:${p.color}"></div></div>
      <div class="proj-stats"><span>${p.total_tasks} ${t('tasks')}</span><span style="color:#3fb950">${p.done_tasks} ${t('done_count')}</span></div></div>`;
  });
  html+=`<button class="btn-outline" onclick="openProjectModal()" style="margin-top:8px">${t('new_project_btn')}</button>`;
  document.getElementById('v-projects').innerHTML=html;
}

window.showProjectTasks=function(pid, pname, pcolor){
  const projTasks = allTasks.filter(t => t.project_id === pid);
  if(!projTasks.length){
    openModal(pname, `<div style="color:#8b949e;font-size:13px;padding:10px 0">${t('no_tasks_in_project')}</div>
      <div class="modal-actions"><button class="btn-primary" onclick="closeModal();openTaskModal();setTimeout(()=>{const s=document.getElementById('nt-proj');if(s)s.value='${pid}';},50)">${t('add_task_btn')}</button></div>`);
    return;
  }
  // Group by status
  const groups = {todo:[],progress:[],review:[],done:[]};
  projTasks.forEach(t => groups[t.status].push(t));
  let html = `<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #30363d">
    <span class="proj-dot" style="background:${pcolor}"></span>
    <span style="font-size:12px;color:#8b949e">${projTasks.length} ${t('tasks_total')}</span></div>`;
  ['todo','progress','review','done'].forEach(st => {
    if(!groups[st].length) return;
    html += `<div style="font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:#8b949e;font-weight:600;margin:12px 0 6px;display:flex;align-items:center;gap:6px"><span class="sdot" style="background:${SC[st]}"></span>${SL[st]} (${groups[st].length})</div>`;
    groups[st].forEach(t => {
      const od = isOverdue(t);
      html += `<div class="rpt-card" onclick="closeModal();openEditTask(${t.id})" style="cursor:pointer;margin-bottom:6px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
          <span class="badge ${badgeClass(t.priority)}">${PL[t.priority]}</span>
          <span style="font-size:11px;color:${od?'#f85149':'#8b949e'}">${t.due_date||'—'}</span>
        </div>
        <div style="font-weight:500;font-size:14px;margin-bottom:4px;color:#e6edf3">${t.title}</div>
        <div style="font-size:12px;color:#8b949e;display:flex;align-items:center;gap:6px">
          <span class="avatar-sm" style="background:${t.assignee_color||'#8b949e'}">${t.assignee_initials||'?'}</span>
          <span>${t.assignee_name||'—'}</span>
        </div></div>`;
    });
  });
  html += `<div class="modal-actions" style="margin-top:16px;border-top:1px solid #30363d;padding-top:12px">
    <button class="btn-outline" onclick="closeModal()">${t('close')}</button>
    <button class="btn-primary" onclick="closeModal();openTaskModal();setTimeout(()=>{const s=document.getElementById('nt-proj');if(s)s.value='${pid}';},50)">${t('new_task_btn')}</button></div>`;
  openModal(pname, html);
};

async function loadReports(){
  const el=document.getElementById('v-reports'); let html='';
  if(!IS_CEO){
    const myTasks=allTasks.filter(t=>t.assignee_id===USER_ID && t.status!=='done');
    html+=`<div class="rpt-form"><div class="rpt-form-title">${t('fill_daily_report')}</div>
      <div id="rpt-items"><div class="rpt-item-row"><div class="rpt-item-fields">
        <select class="rpt-task-sel"><option value="">${t('select_task')}</option>${myTasks.map(t=>`<option value="${t.id}">${t.title}</option>`).join('')}</select>
        <div class="rpt-row-inner"><input type="text" class="rpt-desc" placeholder="${t('what_did_you_do')}">
        <input type="number" class="rpt-hrs" value="4" min="0" max="16" step="0.5" style="width:70px">
        <span style="font-size:12px;color:#8b949e">ч</span></div></div></div></div>
      <button class="btn-outline btn-sm" onclick="addReportItem()" style="margin-bottom:8px">${t('more_row')}</button>
      <div class="rpt-label">${t('notes_problems')}</div>
      <input type="text" id="rpt-note" placeholder="${t('something_important')}" class="rpt-input">
      <button class="btn-primary" onclick="submitReport()" style="margin-top:12px;width:100%">${t('submit_report')}</button></div>`;
  }
  if(IS_CEO || IS_MANAGER){
    html+=`<div class="filters" id="rpt-filters">
      <button class="fbtn active" onclick="filterReports(null,this)">${t('f_all')}</button>
      ${USERS.map(u=>`<button class="fbtn" onclick="filterReports(${u.id},this)">${u.display_name}</button>`).join('')}</div>`;
  }
  html+=`<div id="rpt-list"></div>`;
  el.innerHTML=html;
  const res=await fetch('/api/reports'); renderReportList(await res.json());
}
function renderReportList(reports){
  const grouped={};
  reports.forEach(r=>{if(!grouped[r.report_date])grouped[r.report_date]=[];grouped[r.report_date].push(r);});
  let html='';
  Object.keys(grouped).sort().reverse().forEach(dt=>{
    const d=new Date(dt);
    html+=`<div class="sect-title">${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}</div>`;
    grouped[dt].forEach(r=>{
      const totalH=r.items.reduce((s,i)=>s+i.hours,0);
      html+=`<div class="rpt-card" data-uid="${r.user_id}"><div class="rpt-head">
        <div class="rpt-name"><span class="avatar-sm" style="background:${r.color}">${r.initials}</span>${r.display_name}</div>
        <div class="rpt-hours-total">${totalH}${t('hours_short')}</div></div>`;
      r.items.forEach(it=>{html+=`<div class="rpt-line"><span class="rpt-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><span class="rpt-line-text">${it.description}</span><span class="rpt-line-hrs">${it.hours}${t('hours_short')}</span></div>`;});
      r.notes.forEach(n=>{html+=`<div class="rpt-note">${n.note}</div>`;});
      html+=`</div>`;
    });
  });
  if(!reports.length) html=`<div class="empty-state">${t('no_reports_yet')}</div>`;
  document.getElementById('rpt-list').innerHTML=html;
}
window.filterReports=async function(uid,btn){
  document.querySelectorAll('#rpt-filters .fbtn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const res=await fetch(uid?`/api/reports?user_id=${uid}`:'/api/reports');
  renderReportList(await res.json());
};
window.addReportItem=function(){
  const myTasks=allTasks.filter(t=>t.assignee_id===USER_ID && t.status!=='done');
  const row=document.createElement('div'); row.className='rpt-item-row';
  row.innerHTML=`<div class="rpt-item-fields"><select class="rpt-task-sel"><option value="">${t('select_task')}</option>${myTasks.map(t=>`<option value="${t.id}">${t.title}</option>`).join('')}</select>
    <div class="rpt-row-inner"><input type="text" class="rpt-desc" placeholder="${t('what_did_you_do')}"><input type="number" class="rpt-hrs" value="2" min="0" max="16" step="0.5" style="width:70px"><span style="font-size:12px;color:#8b949e">ч</span></div></div>`;
  document.getElementById('rpt-items').appendChild(row);
};
window.submitReport=async function(){
  const rows=document.querySelectorAll('.rpt-item-row'); const items=[];
  rows.forEach(row=>{const desc=row.querySelector('.rpt-desc').value.trim();const hrs=parseFloat(row.querySelector('.rpt-hrs').value)||0;const tid=row.querySelector('.rpt-task-sel').value||null;
    if(desc) items.push({description:desc,hours:hrs,task_id:tid?parseInt(tid):null});});
  if(!items.length){alert(t('add_at_least_one'));return;}
  const note=document.getElementById('rpt-note').value.trim();
  await fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items,note,report_date:new Date().toISOString().split('T')[0]})});
  loadReports();
};

// === LEAVE ===
const LEAVE_TYPE_LABELS = () => ({paid: t('leave_paid'), sick: t('leave_sick'), unpaid: t('leave_unpaid'), other: t('leave_other')});
const LEAVE_TYPE_COLORS = {paid: '#58a6ff', sick: '#f85149', unpaid: '#8b949e', other: '#c6a350'};
const LEAVE_STATUS_LABELS = () => ({pending: t('leave_status_pending'), approved: t('leave_status_approved'), rejected: t('leave_status_rejected')});
const LEAVE_STATUS_COLORS = {pending: '#d29922', approved: '#3fb950', rejected: '#8b949e'};

async function loadLeave() {
  const el = document.getElementById('v-leave');
  const canManage = IS_CEO || IS_MANAGER;
  // Fetch balance for self and all requests visible
  const [balRes, reqRes] = await Promise.all([
    fetch('/api/leave/balance'),
    fetch('/api/leave/requests')
  ]);
  const bal = await balRes.json();
  const reqs = await reqRes.json();
  const typeLabels = LEAVE_TYPE_LABELS();
  const statusLabels = LEAVE_STATUS_LABELS();

  let html = `<div class="stats-grid" style="grid-template-columns:repeat(3,1fr);max-width:540px;margin-bottom:18px">
    <div class="stat-card"><div class="stat-label">${t('leave_balance')}</div><div class="stat-value">${bal.total}</div><div class="stat-sub">${bal.year}</div></div>
    <div class="stat-card"><div class="stat-label">${t('leave_used')}</div><div class="stat-value" style="color:#d29922">${bal.used}</div></div>
    <div class="stat-card"><div class="stat-label">${t('leave_remaining')}</div><div class="stat-value" style="color:#3fb950">${bal.remaining}</div></div>
  </div>`;

  html += `<button class="btn-primary" onclick="openLeaveRequestModal()" style="margin-bottom:18px">${t('new_leave_request')}</button>`;

  // Pending section for CEO/manager
  const pending = reqs.filter(r => r.status === 'pending' && r.user_id !== USER_ID);
  if (canManage && pending.length > 0) {
    html += `<div class="sect-title" style="margin-top:8px">${t('leave_pending_approval')} <span style="color:#d29922;margin-left:6px;font-size:11px">${pending.length}</span></div>`;
    pending.forEach(r => { html += leaveRequestCard(r, true, typeLabels, statusLabels); });
  }

  // My requests
  const mine = reqs.filter(r => r.user_id === USER_ID);
  html += `<div class="sect-title" style="margin-top:18px">${t('leave_my_requests')}</div>`;
  if (!mine.length) {
    html += `<div style="color:#8b949e;font-size:13px;padding:12px">${t('leave_no_requests')}</div>`;
  } else {
    mine.forEach(r => { html += leaveRequestCard(r, false, typeLabels, statusLabels); });
  }

  // Team requests (already approved/rejected others) for managers and CEO
  const teamOther = reqs.filter(r => r.user_id !== USER_ID && r.status !== 'pending');
  if (canManage && teamOther.length > 0) {
    html += `<div class="sect-title" style="margin-top:18px">${t('leave_team_requests')}</div>`;
    teamOther.forEach(r => { html += leaveRequestCard(r, false, typeLabels, statusLabels); });
  }

  el.innerHTML = html;
}

function leaveRequestCard(r, showActions, typeLabels, statusLabels) {
  const typeColor = LEAVE_TYPE_COLORS[r.leave_type];
  const statusColor = LEAVE_STATUS_COLORS[r.status];
  const canCancel = r.user_id === USER_ID && r.status === 'pending';
  const isMine = r.user_id === USER_ID;
  const dateRange = r.start_date === r.end_date ? r.start_date : `${r.start_date} → ${r.end_date}`;
  const reasonHtml = r.reason ? `<div style="font-size:12px;color:#8b949e;margin-top:6px;font-style:italic">"${r.reason}"</div>` : '';
  const noteHtml = r.decision_note ? `<div style="font-size:11px;color:#8b949e;margin-top:4px">${t('leave_decision_note')}: ${r.decision_note}</div>` : '';
  const approverHtml = r.approver_name && r.status !== 'pending' ?
    `<div style="font-size:11px;color:#8b949e;margin-top:2px">${r.status==='approved'?t('leave_approved_by'):t('leave_rejected_by')}: ${r.approver_name}</div>` : '';

  return `<div class="admin-card" style="flex-direction:column;align-items:stretch;gap:8px;padding:14px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:200px">
        ${!isMine ? `<span class="avatar-sm" style="background:${r.color}">${r.initials}</span>` : ''}
        <div>
          ${!isMine ? `<div class="admin-name" style="font-size:13px">${r.display_name}</div>` : ''}
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:2px">
            <span style="display:inline-flex;align-items:center;gap:4px;background:${typeColor}22;color:${typeColor};padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">${typeLabels[r.leave_type]}</span>
            <span style="color:#e6edf3;font-size:13px;font-weight:500">${dateRange}</span>
            <span style="color:#8b949e;font-size:11px">${r.working_days} ${t('leave_working_days')}</span>
          </div>
        </div>
      </div>
      <span style="background:${statusColor}22;color:${statusColor};padding:4px 10px;border-radius:10px;font-size:11px;font-weight:600;white-space:nowrap">${statusLabels[r.status]}</span>
    </div>
    ${reasonHtml}
    ${approverHtml}
    ${noteHtml}
    ${showActions || canCancel ? `<div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap">
      ${showActions ? `<button class="btn-primary btn-sm" onclick="decideLeave(${r.id},'approved')">${t('leave_approve')}</button>
        <button class="btn-danger btn-sm" onclick="decideLeave(${r.id},'rejected')">${t('leave_reject')}</button>` : ''}
      ${canCancel ? `<button class="btn-outline btn-sm" onclick="cancelLeaveRequest(${r.id})">${t('leave_cancel')}</button>` : ''}
    </div>` : ''}
  </div>`;
}

window.openLeaveRequestModal = function() {
  const today = new Date().toISOString().split('T')[0];
  const typeLabels = LEAVE_TYPE_LABELS();
  openModal(t('leave_request'), `
    <label>${t('leave_type')}</label>
    <select id="lr-type" class="modal-input">
      <option value="paid">${typeLabels.paid}</option>
      <option value="sick">${typeLabels.sick}</option>
      <option value="unpaid">${typeLabels.unpaid}</option>
      <option value="other">${typeLabels.other}</option>
    </select>
    <label>${t('leave_start')}</label>
    <input type="date" id="lr-start" class="modal-input" value="${today}">
    <label>${t('leave_end')}</label>
    <input type="date" id="lr-end" class="modal-input" value="${today}">
    <label>${t('leave_reason')}</label>
    <textarea id="lr-reason" class="modal-input" rows="2" placeholder="${t('leave_reason_ph')}"></textarea>
    <div id="lr-msg" style="font-size:12px;color:#f85149;margin-top:8px;display:none"></div>
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="submitLeaveRequest()">${t('leave_submit')}</button></div>
  `);
};

window.submitLeaveRequest = async function() {
  const leave_type = document.getElementById('lr-type').value;
  const start_date = document.getElementById('lr-start').value;
  const end_date = document.getElementById('lr-end').value;
  const reason = document.getElementById('lr-reason').value.trim();
  const msg = document.getElementById('lr-msg');
  msg.style.display = 'none';
  if (!start_date || !end_date) { msg.textContent = t('leave_end_before_start'); msg.style.display = 'block'; return; }
  if (end_date < start_date) { msg.textContent = t('leave_end_before_start'); msg.style.display = 'block'; return; }
  const r = await fetch('/api/leave/requests', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({leave_type, start_date, end_date, reason})});
  const d = await r.json();
  if (d.error === 'insufficient_balance') {
    msg.textContent = `${t('leave_insufficient')}. ${t('leave_remaining_colon')} ${d.remaining}, ${t('leave_requested_colon')} ${d.requested}`;
    msg.style.display = 'block';
    return;
  }
  if (d.error) { msg.textContent = t('error_occurred'); msg.style.display = 'block'; return; }
  closeModal();
  loadLeave();
  loadNotifications();
};

window.decideLeave = async function(id, decision) {
  let note = '';
  if (decision === 'rejected') {
    if (!confirm(t('leave_sure_reject'))) return;
    note = prompt(t('leave_decision_note_ph')) || '';
  }
  const r = await fetch(`/api/leave/requests/${id}/decide`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({decision, note})});
  const d = await r.json();
  if (d.error === 'insufficient_balance') {
    alert(`${t('leave_insufficient')} (${t('leave_remaining_colon')} ${d.remaining})`);
    return;
  }
  loadLeave();
  loadNotifications();
};

window.cancelLeaveRequest = async function(id) {
  if (!confirm(t('leave_confirm_cancel'))) return;
  await fetch(`/api/leave/requests/${id}`, {method:'DELETE'});
  loadLeave();
  loadNotifications();
};

async function loadDashboard(){
  const res=await fetch('/api/dashboard'); const d=await res.json();
  const el=document.getElementById('v-dashboard');
  let html=`<div class="stats-grid">
    <div class="stat-card"><div class="stat-label">${t('total')}</div><div class="stat-value">${d.total}</div></div>
    <div class="stat-card"><div class="stat-label">${t('done')}</div><div class="stat-value" style="color:#3fb950">${d.done}</div><div class="stat-sub">${d.total?Math.round(d.done/d.total*100):0}%</div></div>
    <div class="stat-card"><div class="stat-label">${t('overdue')}</div><div class="stat-value" style="color:#f85149">${d.overdue}</div></div>
    <div class="stat-card"><div class="stat-label">${t('critical')}</div><div class="stat-value" style="color:#d29922">${d.critical}</div></div></div>
  <div class="chart-legend">
    <span><i style="background:#8b949e"></i>Нови ${d.by_status.todo}</span><span><i style="background:#58a6ff"></i>В работа ${d.by_status.progress}</span>
    <span><i style="background:#d29922"></i>${t('st_review')} ${d.by_status.review}</span><span><i style="background:#3fb950"></i>${t('st_done')} ${d.by_status.done}</span></div>
  <div class="chart-wrap"><canvas id="dChart"></canvas></div>
  <div class="sect-title">Екип</div><div class="team-grid">`;
  d.team.forEach(e=>{
    const pct=e.total_tasks?Math.round(e.done_tasks/e.total_tasks*100):0;
    html+=`<div class="team-card"><div class="team-avatar" style="background:${e.color}">${e.initials}</div>
      <div class="team-name">${e.display_name}</div><div class="team-info">${e.total_tasks} задачи / ${e.done_tasks} готови</div>
      <div class="team-rpt ${e.has_report_today?'has-rpt':'no-rpt'}">${e.has_report_today?e.hours_today+'ч днес':'Няма отчет'}</div>
      <div class="progress-bar"><div class="progress-fill" style="width:${pct}%;background:${e.color}"></div></div></div>`;
  });
  html+=`</div>`;
  el.innerHTML=html;
  if(window._dc) window._dc.destroy();
  window._dc=new Chart(document.getElementById('dChart'),{type:'doughnut',
    data:{labels:[t('st_todo'),t('st_progress'),t('st_review'),t('st_done')],datasets:[{data:[d.by_status.todo,d.by_status.progress,d.by_status.review,d.by_status.done],backgroundColor:['#8b949e','#58a6ff','#d29922','#3fb950'],borderWidth:0,borderColor:'#161b22'}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{display:false}}}});
}

// === MODALS ===
function openModal(title,bodyHtml){document.getElementById('modal-title').textContent=title;document.getElementById('modal-body').innerHTML=bodyHtml;document.getElementById('modal-overlay').classList.add('show');}
function closeModal(){document.getElementById('modal-overlay').classList.remove('show');}

window.openChangePasswordModal = function() {
  openModal(t('change_password'), `
    <label>${t('current_password')}</label>
    <input type="password" id="cp-old" class="modal-input" autocomplete="current-password">
    <label>${t('new_password')}</label>
    <input type="password" id="cp-new" class="modal-input" autocomplete="new-password" placeholder="${t('pass_min_4')}">
    <label>${t('repeat_new_password')}</label>
    <input type="password" id="cp-new2" class="modal-input" autocomplete="new-password">
    <div id="cp-msg" style="font-size:12px;color:#f85149;margin-top:8px;display:none"></div>
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="submitChangePassword()">${t('save')}</button></div>
  `);
};

window.submitChangePassword = async function() {
  const oldP = document.getElementById('cp-old').value;
  const newP = document.getElementById('cp-new').value;
  const newP2 = document.getElementById('cp-new2').value;
  const msg = document.getElementById('cp-msg');
  msg.style.display = 'none';
  if (newP.length < 4) { msg.textContent = t('pass_too_short'); msg.style.display = 'block'; return; }
  if (newP !== newP2) { msg.textContent = t('pass_no_match'); msg.style.display = 'block'; return; }
  const r = await fetch('/api/me/change-password', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({old_password: oldP, new_password: newP})});
  const d = await r.json();
  if (d.error === 'wrong_old_password') { msg.textContent = t('wrong_old_pass'); msg.style.display = 'block'; return; }
  if (d.ok) {
    closeModal();
    setTimeout(() => alert(t('pass_changed')), 200);
  } else {
    msg.textContent = t('error_occurred'); msg.style.display = 'block';
  }
};

function renderCollabPicker(selectedIds, assigneeId){
  const available = ALL_USERS.filter(u => u.id !== assigneeId);
  if (!available.length) return `<div class="collab-empty">${t('no_users_available')}</div>`;
  return available.map(u=>{
    const sel = selectedIds.includes(u.id);
    const meLabel = u.id===USER_ID ? ' ('+t('myself')+')' : '';
    return `<div class="collab-chip ${sel?'selected':''}" data-uid="${u.id}" onclick="this.classList.toggle('selected')">
      <span class="avatar-sm" style="background:${u.color}">${u.initials}</span>
      <span>${u.display_name}${meLabel}</span>
    </div>`;
  }).join('');
}
function getSelectedCollabs(){
  return Array.from(document.querySelectorAll('.collab-chip.selected')).map(c=>parseInt(c.getAttribute('data-uid')));
}
function refreshCollabPickerFor(assigneeId){
  const picker = document.getElementById('collab-picker');
  if (!picker) return;
  const sel = getSelectedCollabs().filter(id => id !== assigneeId);
  picker.innerHTML = renderCollabPicker(sel, assigneeId);
}

function openTaskModal(){
  const whoOptions = ALL_USERS.map(u=>`<option value="${u.id}" ${u.id===USER_ID?'selected':''}>${u.display_name}${u.id===USER_ID?' ('+t('myself')+')':''}</option>`).join('');
  openModal(t('new_task'),`
    <label>${t('title')}</label><input type="text" id="nt-title" placeholder="" class="modal-input">
    <label>${t('description')}</label><textarea id="nt-desc" placeholder="" class="modal-input" rows="2"></textarea>
    <label>${t('project')}</label><select id="nt-proj" class="modal-input">${PROJECTS.map(p=>`<option value="${p.id}">${p.name}</option>`).join('')}</select>
    <label>${t('priority')}</label><select id="nt-pri" class="modal-input"><option value="critical">Критичен</option><option value="high">Висок</option><option value="medium" selected>Среден</option><option value="low">Нисък</option></select>
    <label>${t('assignee')}</label><select id="nt-who" class="modal-input" onchange="refreshCollabPickerFor(parseInt(this.value))">${whoOptions}</select>
    <label>${t('collaborators')} <span style="color:var(--text-muted);font-weight:400;text-transform:none;letter-spacing:0;font-size:11px">(${t('add_collaborators_hint')})</span></label>
    <div class="collab-picker" id="collab-picker">${renderCollabPicker([], USER_ID)}</div>
    <label>${t('due_date')}</label><input type="date" id="nt-due" class="modal-input" value="${new Date(Date.now()+7*86400000).toISOString().split('T')[0]}">
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveNewTask()">${t('add')}</button></div>`);
}
window.saveNewTask=async function(){
  const title=document.getElementById('nt-title').value.trim(); if(!title) return;
  const aid=parseInt(document.getElementById('nt-who').value);
  const collabs=getSelectedCollabs().filter(id=>id!==aid);
  const data={title,description:document.getElementById('nt-desc').value,project_id:parseInt(document.getElementById('nt-proj').value),priority:document.getElementById('nt-pri').value,due_date:document.getElementById('nt-due').value,assignee_id:aid,collaborators:collabs};
  await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  closeModal(); await loadTasks(); switchView(curView);
};
window.openEditTask=function(id){
  const task=allTasks.find(x=>x.id===id); if(!task) return;
  const canDelete = IS_CEO || IS_MANAGER || task.created_by === USER_ID;
  const aid = task.assignee_id || USER_ID;
  const whoOpts = ALL_USERS.map(u=>`<option value="${u.id}" ${u.id===aid?'selected':''}>${u.display_name}${u.id===USER_ID?' ('+t('myself')+')':''}</option>`).join('');
  const collabIds = (task.collaborators||[]).map(c=>c.id).filter(id=>id!==aid);
  const creatorLine = task.creator_name ? `<div style="font-size:11px;color:var(--text-muted);margin-bottom:10px">${t('creator_label')}: ${task.creator_name}</div>` : '';
  openModal(t('edit'),`
    ${creatorLine}
    <label>${t('title')}</label><input type="text" id="et-title" value="${task.title}" class="modal-input">
    <label>${t('description')}</label><textarea id="et-desc" class="modal-input" rows="2">${task.description||''}</textarea>
    <label>${t('project')}</label><select id="et-proj" class="modal-input">${PROJECTS.map(p=>`<option value="${p.id}" ${p.id===task.project_id?'selected':''}>${p.name}</option>`).join('')}</select>
    <label>${t('priority')}</label><select id="et-pri" class="modal-input">${Object.keys(PL).map(k=>`<option value="${k}" ${k===task.priority?'selected':''}>${PL[k]}</option>`).join('')}</select>
    <label>${t('status')}</label><select id="et-st" class="modal-input">${Object.keys(SL).map(k=>`<option value="${k}" ${k===task.status?'selected':''}>${SL[k]}</option>`).join('')}</select>
    <label>${t('assignee')}</label><select id="et-who" class="modal-input" onchange="refreshCollabPickerFor(parseInt(this.value))">${whoOpts}</select>
    <label>${t('collaborators')} <span style="color:var(--text-muted);font-weight:400;text-transform:none;letter-spacing:0;font-size:11px">(${t('add_collaborators_hint')})</span></label>
    <div class="collab-picker" id="collab-picker">${renderCollabPicker(collabIds, aid)}</div>
    <label>${t('due_date')}</label><input type="date" id="et-due" class="modal-input" value="${task.due_date||''}">
    <div style="margin-top:14px"><button class="btn-outline btn-sm" onclick="showTaskHistory(${task.id})">${t('open_history')}</button><div id="audit-container"></div></div>
    <div class="modal-actions">${canDelete?`<button class="btn-danger" onclick="deleteTask(${task.id})">${t('delete')}</button>`:''}<button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveEditTask(${task.id})">${t('save')}</button></div>`);
};

window.showTaskHistory = async function(tid) {
  const container = document.getElementById('audit-container');
  if (container.innerHTML) { container.innerHTML = ''; return; }
  const res = await fetch(`/api/audit/task/${tid}`);
  const log = await res.json();
  if (!log.length) { container.innerHTML = `<div style="font-size:11px;color:#8b949e;padding:8px 0">${t('no_history')}</div>`; return; }
  const actionLabels = {created:t('a_created'), updated:t('a_updated'), deleted:t('a_deleted'), reset_password:t('a_reset_password')};
  const fieldLabels = {title:t('f_title'), description:t('f_description'), priority:t('f_priority'), status:t('f_status'), assignee_id:t('f_assignee_id'), project_id:t('f_project_id'), due_date:t('f_due_date'), collaborators:t('collaborators')};
  let html = '<div class="audit-list">';
  log.forEach(e => {
    const dt = new Date(e.created_at);
    const when = `${dt.toLocaleDateString('bg-BG')} ${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}`;
    let detailStr = '';
    if (e.details && e.action === 'updated') {
      detailStr = Object.keys(e.details).map(k => `${fieldLabels[k]||k}`).join(', ');
    }
    html += `<div class="audit-item">
      <span class="avatar-sm" style="background:${e.color||'#8b949e'};width:18px;height:18px;font-size:8px">${e.initials||'?'}</span>
      <div style="flex:1">
        <div><span class="audit-who">${e.display_name||'—'}</span> <span class="audit-action">${actionLabels[e.action]||e.action}</span></div>
        ${detailStr?`<div class="audit-detail">${detailStr}</div>`:''}
      </div>
      <span class="audit-when">${when}</span>
    </div>`;
  });
  html += '</div>';
  container.innerHTML = html;
};
window.saveEditTask=async function(id){
  const aid=parseInt(document.getElementById('et-who').value);
  const collabs=getSelectedCollabs().filter(uid=>uid!==aid);
  const data={title:document.getElementById('et-title').value.trim(),description:document.getElementById('et-desc').value,project_id:parseInt(document.getElementById('et-proj').value),priority:document.getElementById('et-pri').value,status:document.getElementById('et-st').value,due_date:document.getElementById('et-due').value,assignee_id:aid,collaborators:collabs};
  await fetch(`/api/tasks/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  closeModal(); await loadTasks(); switchView(curView);
};
window.deleteTask=async function(id){
  if(!confirm(t('sure')))return;
  const r=await fetch(`/api/tasks/${id}`,{method:'DELETE'});
  if(r.status===403){alert('Нямате право да изтриете тази задача / Not allowed');return;}
  closeModal();await loadTasks();switchView(curView);
};
window.openProjectModal=function(){openModal(t('new_project'),`<label>${t('name')}</label><input type="text" id="np-name" class="modal-input" placeholder=""><label>${t('color')}</label><input type="color" id="np-color" class="modal-input" value="#c6a350"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveProject()">${t('create')}</button></div>`);};
window.saveProject=async function(){const name=document.getElementById('np-name').value.trim();if(!name)return;await fetch('/api/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,color:document.getElementById('np-color').value})});closeModal();location.reload();};

// === ADMIN ===
async function loadAdmin(){
  const[uRes,pRes,bRes]=await Promise.all([fetch('/api/users'),fetch('/api/projects/list'),fetch('/api/backups')]);
  const users=await uRes.json(),projs=await pRes.json(),backups=await bRes.json();
  let html=`<div class="sect-title" style="display:flex;justify-content:space-between;align-items:center"><span>${t('employees')}</span><button class="btn-outline btn-sm" onclick="openAddUser()">${t('new_employee_btn')}</button></div>`;
  users.forEach(u=>{
    const roleBadge = u.role==='manager' ? `<span style="font-size:10px;color:#c6a350;background:rgba(198,163,80,.15);padding:2px 8px;border-radius:10px;font-weight:600;margin-left:6px">${t('role_manager')}</span>` : '';
    const visBtn = u.role==='manager' ? `<button class="btn-outline btn-sm" onclick="openVisibility(${u.id},'${u.display_name.replace(/'/g,"\\'")}')">${t('visibility')}</button>` : '';
    html+=`<div class="admin-card"><div class="admin-card-left"><span class="avatar-sm" style="background:${u.color}">${u.initials}</span><div><div class="admin-name">${u.display_name}${roleBadge}</div><div class="admin-sub">@${u.username}</div></div></div>
      <div class="admin-card-actions">${visBtn}<button class="btn-outline btn-sm" onclick="openLeaveBalance(${u.id},'${u.display_name.replace(/'/g,"\\'")}')">${t('leave_balance')}</button><button class="btn-outline btn-sm" onclick="openEditUser(${u.id},'${u.display_name.replace(/'/g,"\\'")}','${u.username}','${u.color}','${u.role}')">Редактирай</button><button class="btn-danger btn-sm" onclick="deleteUser(${u.id},'${u.display_name.replace(/'/g,"\\'")}')">${t('delete')}</button></div></div>`;
  });
  html+=`<div class="sect-title" style="display:flex;justify-content:space-between;align-items:center;margin-top:24px"><span>${t('projects_admin')}</span><button class="btn-outline btn-sm" onclick="openProjectModal()">${t('new_project_btn')}</button></div>`;
  projs.forEach(p=>{
    html+=`<div class="admin-card"><div class="admin-card-left"><span class="proj-dot" style="background:${p.color}"></span><div><div class="admin-name">${p.name}</div><div class="admin-sub">${p.total_tasks} ${t('tasks')} / ${p.done_tasks} ${t('done_count')}</div></div></div>
      <div class="admin-card-actions"><button class="btn-outline btn-sm" onclick="openEditProject(${p.id},'${p.name.replace(/'/g,"\\'")}','${p.color}')">Редактирай</button><button class="btn-danger btn-sm" onclick="deleteProject(${p.id},'${p.name.replace(/'/g,"\\'")}')">${t('delete')}</button></div></div>`;
  });
  html+=`<div class="sect-title" style="display:flex;justify-content:space-between;align-items:center;margin-top:24px"><span>${t('backups')}</span><button class="btn-outline btn-sm" onclick="createBackup()">${t('create_backup_now')}</button></div>`;
  if(!backups.length){
    html+=`<div style="font-size:12px;color:#8b949e;padding:12px">${t('no_backups_yet')}</div>`;
  } else {
    backups.slice(0,10).forEach(b=>{
      const dt = new Date(b.created*1000);
      const when = `${dt.toLocaleDateString('bg-BG')} ${String(dt.getHours()).padStart(2,'0')}:${String(dt.getMinutes()).padStart(2,'0')}`;
      const sizeKB = (b.size/1024).toFixed(1);
      html+=`<div class="backup-row"><div><div class="backup-name">${b.name}</div><div class="backup-size">${when} · ${sizeKB} KB</div></div>
        <div class="backup-actions"><a href="/api/backups/download/${b.name}" class="btn-outline btn-sm" download>${t('download')}</a></div></div>`;
    });
    if(backups.length>10) html+=`<div style="font-size:11px;color:#8b949e;padding:6px;text-align:center">${t('showing_backups')} ${backups.length} ${t('backups_count')}</div>`;
  }
  document.getElementById('v-admin').innerHTML=html;
}
window.createBackup = async function() {
  const r = await fetch('/api/backups/create', {method:'POST'});
  const d = await r.json();
  if (d.ok) loadAdmin();
};
window.openAddUser=function(){openModal(t('new_employee'),`<label>${t('name_cyrillic')}</label><input type="text" id="nu-name" class="modal-input" placeholder=""><label>${t('username_latin')}</label><input type="text" id="nu-user" class="modal-input" placeholder=""><label>${t('password')}</label><input type="text" id="nu-pass" class="modal-input" value="1234"><label>${t('role')}</label><select id="nu-role" class="modal-input"><option value="employee">${t('role_employee')}</option><option value="manager">${t('role_manager')}</option></select><label>${t('color')}</label><input type="color" id="nu-color" class="modal-input" value="#58a6ff"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveNewUser()">${t('add')}</button></div>`);};
window.saveNewUser=async function(){const name=document.getElementById('nu-name').value.trim(),username=document.getElementById('nu-user').value.trim();if(!name||!username){alert(t('fill_name_username'));return;}const res=await fetch('/api/users',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({display_name:name,username,password:document.getElementById('nu-pass').value||'1234',role:document.getElementById('nu-role').value,color:document.getElementById('nu-color').value})});const data=await res.json();if(data.error==='username_taken'){alert(t('username_taken'));return;}closeModal();location.reload();};
window.openEditUser=function(id,name,username,color,role){openModal(t('edit'),`<label>${t('name')}</label><input type="text" id="eu-name" class="modal-input" value="${name}"><label>${t('username_latin')}</label><input type="text" id="eu-user" class="modal-input" value="${username}"><label>${t('new_password_blank')}</label><input type="text" id="eu-pass" class="modal-input" placeholder="${t('new_password_placeholder')}"><label>${t('role')}</label><select id="eu-role" class="modal-input"><option value="employee" ${role==='employee'?'selected':''}>${t('role_employee')}</option><option value="manager" ${role==='manager'?'selected':''}>${t('role_manager')}</option></select><label>${t('color')}</label><input type="color" id="eu-color" class="modal-input" value="${color}"><div style="margin-top:14px;padding:10px;background:#161b22;border:1px solid #30363d;border-radius:8px"><div style="font-size:11px;color:#8b949e;margin-bottom:6px">${t('forgot_password')}</div><button class="btn-outline btn-sm" onclick="resetUserPassword(${id},'${name.replace(/'/g,"\\'")}')">${t('generate_new_password')}</button></div><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveEditUser(${id})">${t('save')}</button></div>`);};
window.resetUserPassword = async function(id, name) {
  if (!confirm(`${t('sure_reset_password')} "${name}"? ${t('old_password_will_not_work')}`)) return;
  const r = await fetch(`/api/users/${id}/reset-password`, {method:'POST'});
  const d = await r.json();
  if (d.new_password) {
    openModal(t('new_password_generated'), `
      <div style="text-align:center;padding:10px 0">
        <div style="font-size:13px;color:#8b949e;margin-bottom:14px">${t('give_password_to')} ${name}. ${t('not_shown_again')}</div>
        <div style="font-size:24px;font-weight:600;color:#c6a350;background:#161b22;padding:16px;border-radius:10px;border:1px solid rgba(198,163,80,.3);font-family:monospace;letter-spacing:2px">${d.new_password}</div>
        <div style="font-size:11px;color:#8b949e;margin-top:12px">${t('suggest_change_first_login')}</div>
      </div>
      <div class="modal-actions"><button class="btn-primary" onclick="closeModal()">${t('close')}</button></div>
    `);
  }
};
window.saveEditUser=async function(id){const data={display_name:document.getElementById('eu-name').value.trim(),username:document.getElementById('eu-user').value.trim(),color:document.getElementById('eu-color').value,role:document.getElementById('eu-role').value};const pass=document.getElementById('eu-pass').value.trim();if(pass)data.password=pass;await fetch(`/api/users/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});closeModal();location.reload();};
window.deleteUser=async function(id,name){if(!confirm(`${t('delete_employee')} "${name}"? ${t('delete_user_warn')}`))return;await fetch(`/api/users/${id}`,{method:'DELETE'});location.reload();};
window.openEditProject=function(id,name,color){openModal(t('edit'),`<label>${t('name')}</label><input type="text" id="ep-name" class="modal-input" value="${name}"><label>${t('color')}</label><input type="color" id="ep-color" class="modal-input" value="${color}"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveEditProject(${id})">${t('save')}</button></div>`);};
window.saveEditProject=async function(id){await fetch(`/api/projects/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('ep-name').value.trim(),color:document.getElementById('ep-color').value})});closeModal();location.reload();};
window.deleteProject=async function(id,name){if(!confirm(`${t('delete_project_warn')} "${name}"?`))return;await fetch(`/api/projects/${id}`,{method:'DELETE'});location.reload();};

window.openVisibility=async function(managerId, managerName){
  const [usersRes, visRes] = await Promise.all([fetch('/api/users'), fetch(`/api/visibility/${managerId}`)]);
  const users = await usersRes.json();
  const visible = await visRes.json();
  const employees = users.filter(u => u.role === 'employee');
  const checks = employees.map(u => `<label style="display:flex;align-items:center;gap:10px;padding:10px;background:#161b22;border:1px solid #30363d;border-radius:8px;margin-bottom:6px;cursor:pointer"><input type="checkbox" class="vis-cb" data-id="${u.id}" ${visible.includes(u.id)?'checked':''} style="width:18px;height:18px;cursor:pointer"><span class="avatar-sm" style="background:${u.color}">${u.initials}</span><span style="color:#e6edf3;font-size:13px">${u.display_name}</span></label>`).join('');
  const checksHtml = checks || `<div style="color:#8b949e;font-size:13px">${t('no_employees')}</div>`;
  openModal(`${t('visibility_for')} ${managerName}`, `
    <div style="font-size:12px;color:#8b949e;margin-bottom:12px">${t('visibility_help')}</div>
    ${checksHtml}
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveVisibility(${managerId})">${t('save')}</button></div>
  `);
};
window.saveVisibility=async function(managerId){
  const checked = Array.from(document.querySelectorAll('.vis-cb:checked')).map(cb => parseInt(cb.dataset.id));
  await fetch(`/api/visibility/${managerId}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({employee_ids: checked})});
  closeModal();
};

window.openLeaveBalance = async function(uid, name) {
  const year = new Date().getFullYear();
  const r = await fetch(`/api/leave/balance/${uid}?year=${year}`);
  const bal = await r.json();
  openModal(`${t('leave_balance_for')} ${name}`, `
    <label>${t('leave_year')}</label>
    <input type="number" id="lb-year" class="modal-input" value="${year}" min="2020" max="2099">
    <label>${t('leave_total_days')}</label>
    <input type="number" id="lb-total" class="modal-input" value="${bal.total}" min="0" max="60">
    <div style="display:flex;gap:12px;margin-top:12px;font-size:12px;color:#8b949e">
      <span>${t('leave_used')}: <b style="color:#d29922">${bal.used}</b></span>
      <span>${t('leave_remaining')}: <b style="color:#3fb950">${bal.remaining}</b></span>
    </div>
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveLeaveBalance(${uid})">${t('save')}</button></div>
  `);
};

window.saveLeaveBalance = async function(uid) {
  const year = parseInt(document.getElementById('lb-year').value);
  const paid_total = parseInt(document.getElementById('lb-total').value);
  await fetch(`/api/leave/balance/${uid}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({year, paid_total})});
  closeModal();
};
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</body>
</html>
'''

LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAH0B9ADASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAIIBwkEBQYDAf/EAF8QAQABAgQBBgULCxAJBQADAQABAgMEBQYRBwgSEyFTkjE3QVGxFBgiM1ZhcXJ1s9IJMjhzdIGRlJWytBUWIzQ1NkJSYnaCk6GjwtMkJUNGVFWEwdEXg4WixCZjw+H/xAAbAQEBAAMBAQEAAAAAAAAAAAAAAQQFBgIDB//EADYRAQABBAADBQUFCAMAAAAAAAABAgMEEQUxQRIhUWGxBhNxgcEUMoKh8CIjQkNSkdHhJKKy/9oADAMBAAIRAxEAPwCrFm1a6Gj9jo+tj+DHmS6K12dHdgse0W/ix6E1eUOitdnR3YOitdnR3YTFEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwEOitdnR3YOitdnR3YTAQ6K12dHdg6K12dHdhMBDorXZ0d2DorXZ0d2EwELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehNCx7Rb+LHoTQAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAELHtFv4sehMEABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB//Z"

BOAT_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAN7B9ADASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAEHAgYDBAUICf/EAHQQAAIBAgQDAwYFDQkHDQ0DDQABAgMEBQYHERIhMUFRYQgTInGBkRQyUqHRFRYXI0JVYpKUlbHS0xhTVFZXcoKTwSQzQ4OWosM0REZjdYSFo7LC1OHwJTU2RUdkc3SGs9Xj8SYoN2a0OGV2pKXExeInWOT/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+MgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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"

