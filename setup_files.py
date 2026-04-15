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
.collab-stack{display:inline-flex;align-items:center;margin-left:-3px}
.collab-stack .avatar-xs{margin-left:-6px}
.collab-stack .avatar-xs:first-child{margin-left:0}
.collab-more{font-size:9px;color:var(--text-muted);margin-left:4px;font-weight:600}
.sdot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:4px}
.overdue{color:var(--accent-red)!important;font-weight:500}

/* === Filters === */
.filters{display:flex;gap:6px;margin-bottom:14px;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:2px 0;align-items:center}
.filters::-webkit-scrollbar{display:none}
.fbtn{padding:6px 14px;font-size:11px;border:1px solid var(--border);border-radius:20px;background:transparent;cursor:pointer;color:var(--text-muted);font-family:inherit;transition:all .15s;white-space:nowrap;flex-shrink:0}
.fbtn:hover{border-color:var(--text-muted);color:var(--text-secondary)}
.fbtn.active{background:var(--gold);color:var(--bg-deep);border-color:var(--gold);font-weight:600}
.fbtn.toggle{margin-left:auto;display:inline-flex;align-items:center;gap:6px}
.fbtn.toggle::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--text-muted)}
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

/* === Collaborators picker === */
.collab-picker{display:flex;flex-wrap:wrap;gap:6px;padding:8px;background:var(--bg-surface);border:1px solid var(--border);border-radius:var(--radius);max-height:160px;overflow-y:auto}
.collab-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 10px 5px 5px;background:var(--bg-card);border:1px solid var(--border);border-radius:20px;font-size:12px;cursor:pointer;transition:all .15s;color:var(--text-secondary)}
.collab-chip:hover{border-color:var(--gold-border)}
.collab-chip.selected{background:var(--gold-dim);border-color:var(--gold-border);color:var(--text-primary)}
.collab-chip.disabled{opacity:.4;cursor:not-allowed}
.collab-chip .avatar-sm{width:18px;height:18px;font-size:8px}
.collab-empty{padding:10px;color:var(--text-muted);font-size:12px;text-align:center;width:100%}

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
<title>Helios Marine — Tasks</title>
<link rel="stylesheet" href="/static/style.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
<div class="app">
    <div class="topbar">
        <div class="logo">
            <img src="/static/logo.png" alt="Helios">
            <div class="logo-divider"></div>
            <span class="logo-label" id="brand-label">Tasks</span>
        </div>
        <div class="user-info">
            <button class="notif-btn" id="notif-btn" onclick="toggleNotifications(event)" title="Известия">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                <span class="notif-badge" id="notif-badge" style="display:none">0</span>
            </button>
            <button onclick="toggleLang()" id="lang-btn" style="background:none;border:1px solid var(--border);color:var(--text-secondary);padding:5px 10px;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">EN</button>
            <div class="avatar-sm" style="background:{{user.color}}">{{user.initials}}</div>
            <span class="user-name">{{user.display_name}}</span>
            {% if is_ceo %}<span class="user-badge" id="role-badge">CEO</span>{% elif is_manager %}<span class="user-badge" id="role-badge">MANAGER</span>{% endif %}
            <a href="/logout" class="logout-btn" title="Изход">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            </a>
        </div>
    </div>
    <div id="notif-popup" class="notif-popup">
        <div class="notif-header" id="notif-header">Известия</div>
        <div id="notif-list" class="notif-list"></div>
    </div>

    <div class="nav">
        <button class="nav-btn active" onclick="switchView('kanban',this)" data-i18n="nav_kanban">Канбан</button>
        <button class="nav-btn" onclick="switchView('list',this)" data-i18n="nav_list">Списък</button>
        <button class="nav-btn" onclick="switchView('calendar',this)" data-i18n="nav_calendar">Календар</button>
        <button class="nav-btn" onclick="switchView('projects',this)" data-i18n="nav_projects">Проекти</button>
        <button class="nav-btn" onclick="switchView('reports',this)" data-i18n="nav_reports">Отчети</button>
        <button class="nav-btn" onclick="switchView('leave',this)" data-i18n="nav_leave">Отпуск</button>
        {% if is_ceo or is_manager %}<button class="nav-btn" onclick="switchView('dashboard',this)" data-i18n="nav_dashboard">Табло</button>{% endif %}
        {% if is_ceo %}<button class="nav-btn" onclick="switchView('admin',this)" data-i18n="nav_admin">Админ</button>{% endif %}
    </div>

    <div id="kanban" class="view active">
        <div class="filters">
            <button class="fbtn active" onclick="filterTasks('all',this)" data-i18n="all">Всички</button>
            <button class="fbtn" onclick="filterTasks('critical',this)" data-i18n="critical">Критични</button>
            <button class="fbtn" onclick="filterTasks('high',this)" data-i18n="high">Високи</button>
            <button class="fbtn" onclick="filterTasks('overdue',this)" data-i18n="overdue">Просрочени</button>
            <button class="fbtn toggle" id="only-mine-btn-k" onclick="toggleOnlyMine('k')" data-i18n="only_mine">Само моите</button>
        </div>
        <div class="kanban" id="kanban-board"></div>
    </div>

    <div id="list" class="view">
        <div class="filters">
            <button class="fbtn active" onclick="filterListProj(0,this)" data-i18n="all_projects">Всички проекти</button>
            {% for p in projects %}<button class="fbtn" onclick="filterListProj({{p.id}},this)">{{p.name}}</button>{% endfor %}
            <button class="fbtn toggle" id="only-mine-btn-l" onclick="toggleOnlyMine('l')" data-i18n="only_mine">Само моите</button>
        </div>
        <div class="table-wrap">
        <table class="ltbl">
            <thead><tr><th data-i18n="th_task">Задача</th><th class="hide-mobile" data-i18n="th_project">Проект</th><th data-i18n="th_assignee">Изпълнител</th><th class="hide-mobile" data-i18n="th_priority">Приоритет</th><th data-i18n="th_status">Статус</th><th class="hide-mobile" data-i18n="th_deadline">Срок</th></tr></thead>
            <tbody id="list-tbody"></tbody>
        </table>
        </div>
    </div>

    <div id="calendar" class="view">
        <div class="cal-header">
            <button class="cal-nav" onclick="changeMonth(-1)">‹</button>
            <div class="cal-title" id="cal-title">—</div>
            <button class="cal-nav" onclick="changeMonth(1)">›</button>
        </div>
        <div class="filters" style="margin-bottom:10px">
            <button class="fbtn toggle" id="only-mine-btn-c" onclick="toggleOnlyMine('c')" data-i18n="only_mine">Само моите</button>
        </div>
        <div class="cal-grid">
            <div class="cal-days" id="cal-days"></div>
            <div class="cal-cells" id="cal-cells"></div>
        </div>
    </div>

    <div id="projects" class="view"><div id="projects-list"></div></div>

    <div id="reports" class="view">
        {% if not is_ceo and not is_manager %}
        <div class="rpt-form">
            <div class="rpt-form-title" data-i18n="report_today">Отчет за днес</div>
            <div id="report-items"></div>
            <button class="btn-outline btn-sm" onclick="addReportItem()" data-i18n="add_task">+ Задача</button>
            <label class="rpt-label" data-i18n="notes">Бележки</label>
            <textarea id="report-note" rows="2" class="rpt-input" placeholder="" data-i18n-ph="notes_ph"></textarea>
            <div style="margin-top:14px"><button class="btn-primary" onclick="saveReport()" data-i18n="save_report">Запази отчет</button></div>
        </div>
        {% endif %}
        <div class="sect-title" data-i18n="recent_reports">Последни отчети</div>
        <div id="reports-list"></div>
    </div>

    <div id="leave" class="view">
        <div id="leave-content"></div>
    </div>

    {% if is_ceo or is_manager %}
    <div id="dashboard" class="view">
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-label" data-i18n="all_tasks">Всички задачи</div><div class="stat-value" id="stat-total">—</div><div class="stat-sub"><span id="stat-done">—</span> <span data-i18n="done">завършени</span></div></div>
            <div class="stat-card"><div class="stat-label" data-i18n="completion">Завършеност</div><div class="stat-value" id="stat-pct">—</div><div class="stat-sub" data-i18n="overall">общо</div></div>
            <div class="stat-card"><div class="stat-label" data-i18n="overdue_label">Просрочени</div><div class="stat-value" id="stat-overdue" style="color:var(--accent-red)">—</div><div class="stat-sub" data-i18n="needs_attention">изискват внимание</div></div>
            <div class="stat-card"><div class="stat-label" data-i18n="critical_label">Критични</div><div class="stat-value" id="stat-critical" style="color:var(--accent-amber)">—</div><div class="stat-sub" data-i18n="active">активни</div></div>
        </div>
        <div class="sect-title" data-i18n="status_distribution">Статус разпределение</div>
        <div class="chart-legend"><span><i style="background:#58a6ff"></i><span data-i18n="todo">За правене</span></span><span><i style="background:#d29922"></i><span data-i18n="progress">В процес</span></span><span><i style="background:#a37cf0"></i><span data-i18n="review">Преглед</span></span><span><i style="background:#3fb950"></i><span data-i18n="completed">Завършени</span></span></div>
        <div class="chart-wrap"><canvas id="status-chart"></canvas></div>
        <div class="sect-title" data-i18n="team">Екип</div>
        <div class="team-grid" id="team-grid"></div>
    </div>
    {% endif %}

    {% if is_ceo %}
    <div id="admin" class="view">
        <div class="sect-title" data-i18n="employees">Служители</div>
        <div id="admin-users-list"></div>
        <div style="margin-top:14px"><button class="btn-primary" onclick="openAddUser()" data-i18n="add_employee">+ Добави служител</button></div>
        <div class="sect-title" style="margin-top:24px" data-i18n="projects_admin">Проекти</div>
        <div id="admin-projects-list"></div>
        <div style="margin-top:14px"><button class="btn-primary" onclick="openAddProject()" data-i18n="add_project">+ Добави проект</button></div>
        <div class="sect-title" style="margin-top:24px" data-i18n="leave_balances">Годишни отпуски</div>
        <div id="admin-balances-list"></div>
        <div class="sect-title" style="margin-top:24px" data-i18n="db_backups">Резервни копия на базата</div>
        <div id="admin-backups-list"></div>
        <div style="margin-top:14px"><button class="btn-primary" onclick="createBackup()" data-i18n="create_backup">+ Създай резервно копие</button></div>
    </div>
    {% endif %}
</div>

<button class="fab" onclick="openTaskModal()" id="fab" title="Нова задача">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
</button>

<div class="modal-overlay" id="modal-overlay">
    <div class="modal">
        <div class="modal-header">
            <h3 id="modal-title">—</h3>
            <button class="modal-close" onclick="closeModal()">×</button>
        </div>
        <div id="modal-body"></div>
    </div>
</div>

<script>
const USERS = {{ users | tojson }};
const ALL_USERS = {{ all_users | tojson }};
const PROJECTS = {{ projects | tojson }};
const IS_CEO = {{ 'true' if is_ceo else 'false' }};
const IS_MANAGER = {{ 'true' if is_manager else 'false' }};
const USER_ID = {{ user.id }};
const USER_NAME = "{{ user.display_name }}";
const USER_ROLE = "{{ user_role }}";
const IS_PRIVILEGED = IS_CEO || IS_MANAGER;

const I18N = {
  bg: {
    nav_kanban:'Канбан', nav_list:'Списък', nav_calendar:'Календар', nav_projects:'Проекти', nav_reports:'Отчети', nav_leave:'Отпуск', nav_dashboard:'Табло', nav_admin:'Админ',
    all:'Всички', critical:'Критични', high:'Високи', overdue:'Просрочени', all_projects:'Всички проекти', only_mine:'Само моите',
    th_task:'Задача', th_project:'Проект', th_assignee:'Изпълнител', th_priority:'Приоритет', th_status:'Статус', th_deadline:'Срок',
    todo:'За правене', progress:'В процес', review:'Преглед', completed:'Завършени', done:'завършени',
    report_today:'Отчет за днес', add_task:'+ Задача', notes:'Бележки', notes_ph:'Преки наблюдения, проблеми...', save_report:'Запази отчет', recent_reports:'Последни отчети',
    all_tasks:'Всички задачи', completion:'Завършеност', overall:'общо', overdue_label:'Просрочени', needs_attention:'изискват внимание', critical_label:'Критични', active:'активни',
    status_distribution:'Статус разпределение', team:'Екип',
    employees:'Служители', add_employee:'+ Добави служител', projects_admin:'Проекти', add_project:'+ Добави проект',
    leave_balances:'Годишни отпуски', db_backups:'Резервни копия на базата', create_backup:'+ Създай резервно копие',
    notifications:'Известия', tasks_overdue:'Просрочени задачи', tasks_today:'Задачи за днес', no_report_today:'Не сте изпратили отчет днес', team_no_report:'без отчет днес', pending_leave:'отпуски за одобрение', no_notifications:'Няма нови известия',
    new_task:'Нова задача', edit_task:'Редактирай задача', title:'Заглавие', description:'Описание', priority:'Приоритет', project:'Проект', deadline:'Краен срок', assignee:'Изпълнител', status:'Статус', collaborators:'Сътрудници', add_collaborators:'(Добави повече участници)', no_collaborators:'Няма налични потребители',
    save:'Запази', cancel:'Отказ', delete:'Изтрий', save_changes:'Запази промените', confirm_delete:'Сигурен ли си? Действието е необратимо.', confirm_delete_user:'Изтрий този служител?', confirm_delete_proj:'Изтрий този проект?',
    add_employee_t:'Добави служител', name:'Име', username_field:'Потребителско име', password:'Парола', color:'Цвят', role:'Роля', employee:'Служител', manager_role:'Мениджър',
    add_project_t:'Добави проект', edit_employee:'Редактирай служител', edit_project:'Редактирай проект',
    leave_my_balance:'Моят годишен отпуск', leave_remaining:'остават', leave_used:'използвани', leave_total:'общо', leave_request:'Заявка за отпуск', leave_my_requests:'Моите заявки', leave_pending_approval:'Чакащи одобрение', leave_team:'Екип', leave_balances_team:'Балансите на екипа',
    leave_type:'Тип отпуск', leave_paid:'Платен', leave_sick:'Болничен', leave_unpaid:'Неплатен', leave_other:'Друг', leave_start:'От дата', leave_end:'До дата', leave_reason:'Причина (по избор)', leave_submit:'Подай заявка', leave_days:'раб. дни',
    leave_status_pending:'Чака', leave_status_approved:'Одобрен', leave_status_rejected:'Отказан', leave_approve:'Одобри', leave_reject:'Откажи', leave_decision_note:'Бележка (по избор)', leave_cancel:'Откажи', leave_for:'За', leave_no_requests:'Няма заявки', leave_assign_other:'Възложи на (CEO)',
    notif_pending_leave_t:'Чакащи отпуски',
    cal_holiday:'Празник', cal_weekend:'Уикенд',
    leave_history:'История', leave_no_history:'Няма история', leave_only_pending_can_cancel:'Само чакащи заявки могат да бъдат отказани',
    leave_set_balance:'Определи балансa', leave_save:'Запази',
    backup_created:'Резервно копие създадено', backup_failed:'Грешка при създаване на резервно копие', confirm_create_backup:'Създай резервно копие сега?',
    audit_history:'История', audit_loading:'Зарежда...', audit_no_history:'Няма история', audit_created:'създал', audit_updated:'променил', audit_deleted:'изтрил', audit_priority:'приоритет', audit_status:'статус', audit_assignee:'изпълнител', audit_project:'проект', audit_due:'срок', audit_title:'заглавие', audit_description:'описание', audit_collaborators:'сътрудници',
    months:['Януари','Февруари','Март','Април','Май','Юни','Юли','Август','Септември','Октомври','Ноември','Декември'],
    weekdays:['ПОН','ВТО','СРЯ','ЧЕТ','ПЕТ','СЪБ','НЕД'],
    bg_holidays:{'01-01':'Нова година','03-03':'Освобождението','05-01':'Ден на труда','05-06':'Гергьовден','05-24':'Кирил и Методий','09-06':'Съединение','09-22':'Независимост','11-01':'Будители','12-24':'Бъдни вечер','12-25':'Коледа','12-26':'Коледа'},
    pri:{critical:'Критичен',high:'Висок',medium:'Среден',low:'Нисък'}, st:{todo:'За правене',progress:'В процес',review:'Преглед',done:'Завършена'},
    me_label:'Аз', created_by:'Създадена от',
    change_my_password:'Смени паролата ми', current_password:'Текуща парола', new_password:'Нова парола', confirm_new_password:'Потвърди нова парола', password_changed:'Паролата е сменена успешно', password_mismatch:'Паролите не съвпадат', password_too_short:'Паролата трябва да бъде поне 4 символа', wrong_old_password:'Грешна текуща парола',
  },
  en: {
    nav_kanban:'Kanban', nav_list:'List', nav_calendar:'Calendar', nav_projects:'Projects', nav_reports:'Reports', nav_leave:'Leave', nav_dashboard:'Dashboard', nav_admin:'Admin',
    all:'All', critical:'Critical', high:'High', overdue:'Overdue', all_projects:'All projects', only_mine:'Only mine',
    th_task:'Task', th_project:'Project', th_assignee:'Assignee', th_priority:'Priority', th_status:'Status', th_deadline:'Due',
    todo:'To do', progress:'In progress', review:'Review', completed:'Completed', done:'completed',
    report_today:"Today's report", add_task:'+ Task', notes:'Notes', notes_ph:'Direct observations, issues...', save_report:'Save report', recent_reports:'Recent reports',
    all_tasks:'All tasks', completion:'Completion', overall:'overall', overdue_label:'Overdue', needs_attention:'need attention', critical_label:'Critical', active:'active',
    status_distribution:'Status distribution', team:'Team',
    employees:'Employees', add_employee:'+ Add employee', projects_admin:'Projects', add_project:'+ Add project',
    leave_balances:'Annual leave balances', db_backups:'Database backups', create_backup:'+ Create backup',
    notifications:'Notifications', tasks_overdue:'Overdue tasks', tasks_today:'Tasks for today', no_report_today:"You haven't sent today's report", team_no_report:'no report today', pending_leave:'leave requests pending', no_notifications:'No new notifications',
    new_task:'New task', edit_task:'Edit task', title:'Title', description:'Description', priority:'Priority', project:'Project', deadline:'Deadline', assignee:'Assignee', status:'Status', collaborators:'Collaborators', add_collaborators:'(Add more participants)', no_collaborators:'No users available',
    save:'Save', cancel:'Cancel', delete:'Delete', save_changes:'Save changes', confirm_delete:'Are you sure? This action is irreversible.', confirm_delete_user:'Delete this employee?', confirm_delete_proj:'Delete this project?',
    add_employee_t:'Add employee', name:'Name', username_field:'Username', password:'Password', color:'Color', role:'Role', employee:'Employee', manager_role:'Manager',
    add_project_t:'Add project', edit_employee:'Edit employee', edit_project:'Edit project',
    leave_my_balance:'My annual leave', leave_remaining:'remaining', leave_used:'used', leave_total:'total', leave_request:'Request leave', leave_my_requests:'My requests', leave_pending_approval:'Pending approval', leave_team:'Team', leave_balances_team:'Team balances',
    leave_type:'Leave type', leave_paid:'Paid', leave_sick:'Sick', leave_unpaid:'Unpaid', leave_other:'Other', leave_start:'Start date', leave_end:'End date', leave_reason:'Reason (optional)', leave_submit:'Submit request', leave_days:'work days',
    leave_status_pending:'Pending', leave_status_approved:'Approved', leave_status_rejected:'Rejected', leave_approve:'Approve', leave_reject:'Reject', leave_decision_note:'Note (optional)', leave_cancel:'Cancel', leave_for:'For', leave_no_requests:'No requests', leave_assign_other:'Assign to (CEO)',
    notif_pending_leave_t:'Pending leave',
    cal_holiday:'Holiday', cal_weekend:'Weekend',
    leave_history:'History', leave_no_history:'No history', leave_only_pending_can_cancel:'Only pending requests can be cancelled',
    leave_set_balance:'Set balance', leave_save:'Save',
    backup_created:'Backup created', backup_failed:'Backup failed', confirm_create_backup:'Create backup now?',
    audit_history:'History', audit_loading:'Loading...', audit_no_history:'No history', audit_created:'created', audit_updated:'updated', audit_deleted:'deleted', audit_priority:'priority', audit_status:'status', audit_assignee:'assignee', audit_project:'project', audit_due:'due', audit_title:'title', audit_description:'description', audit_collaborators:'collaborators',
    months:['January','February','March','April','May','June','July','August','September','October','November','December'],
    weekdays:['MON','TUE','WED','THU','FRI','SAT','SUN'],
    bg_holidays:{'01-01':'New Year','03-03':'Liberation Day','05-01':'Labour Day','05-06':"St. George's Day",'05-24':'Cyril & Methodius','09-06':'Unification','09-22':'Independence','11-01':'Awakeners','12-24':'Christmas Eve','12-25':'Christmas','12-26':'Christmas'},
    pri:{critical:'Critical',high:'High',medium:'Medium',low:'Low'}, st:{todo:'To do',progress:'In progress',review:'Review',done:'Done'},
    me_label:'Me', created_by:'Created by',
    change_my_password:'Change my password', current_password:'Current password', new_password:'New password', confirm_new_password:'Confirm new password', password_changed:'Password changed successfully', password_mismatch:'Passwords do not match', password_too_short:'Password must be at least 4 characters', wrong_old_password:'Wrong current password',
  }
};
let lang = localStorage.getItem('helios_lang') || 'bg';
function t(key){ return I18N[lang][key] || key; }
function applyI18n(){
  document.documentElement.lang = lang;
  document.getElementById('lang-btn').textContent = lang === 'bg' ? 'EN' : 'BG';
  document.querySelectorAll('[data-i18n]').forEach(el=>{ const v = t(el.getAttribute('data-i18n')); if(typeof v==='string') el.textContent = v; });
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{ const v = t(el.getAttribute('data-i18n-ph')); if(typeof v==='string') el.placeholder = v; });
  document.getElementById('notif-header').textContent = t('notifications');
  if (currentMonth!==undefined) renderCalendar();
  if (allTasks.length) { renderKanban(); renderList(); }
  loadProjects(); loadNotifications();
  applyOnlyMineButtons();
  if (document.getElementById('reports').classList.contains('active')) loadReports();
  if (document.getElementById('admin') && document.getElementById('admin').classList.contains('active')) loadAdmin();
  if (document.getElementById('leave').classList.contains('active')) loadLeaveView();
  if (document.querySelector('#dashboard.active')) loadDashboard();
}
function toggleLang(){ lang = lang === 'bg' ? 'en' : 'bg'; localStorage.setItem('helios_lang', lang); applyI18n(); }

let allTasks = [], currentFilter='all', currentProjFilter=0, statusChart, currentMonth=new Date().getMonth(), currentYear=new Date().getFullYear();
let leaveCalCache = {};

// === Only-Mine state ===
let onlyMine = localStorage.getItem('helios_only_mine_'+USER_ID) === '1';
function applyOnlyMineButtons(){
  ['k','l','c'].forEach(suffix=>{
    const b = document.getElementById('only-mine-btn-'+suffix);
    if (b){ b.classList.toggle('active', onlyMine); b.textContent = t('only_mine'); }
  });
}
function toggleOnlyMine(suffix){
  onlyMine = !onlyMine;
  localStorage.setItem('helios_only_mine_'+USER_ID, onlyMine ? '1' : '0');
  applyOnlyMineButtons();
  renderKanban(); renderList(); renderCalendar();
}
function isMine(task){
  if (task.created_by === USER_ID) return true;
  if (task.assignee_id === USER_ID) return true;
  if (task.collaborators && task.collaborators.some(c=>c.id===USER_ID)) return true;
  return false;
}

function switchView(v, el){
  document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(x=>x.classList.remove('active'));
  document.getElementById(v).classList.add('active');
  el.classList.add('active');
  if(v==='dashboard') loadDashboard();
  if(v==='reports') loadReports();
  if(v==='calendar') renderCalendar();
  if(v==='projects') loadProjects();
  if(v==='admin') loadAdmin();
  if(v==='leave') loadLeaveView();
  // FAB visible always (any user can create tasks)
  document.getElementById('fab').style.display='flex';
}

async function loadTasks(){
  const r = await fetch('/api/tasks');
  allTasks = await r.json();
  if (!Array.isArray(allTasks)) allTasks = [];
  allTasks.forEach(t=>{ if(!t.collaborators) t.collaborators=[]; });
  renderKanban(); renderList();
}

function pri_badge(p){ const m={critical:'b-crit',high:'b-high',medium:'b-med',low:'b-low'}; return `<span class="badge ${m[p]}">${(t('pri')[p]||p).toUpperCase()}</span>`; }
function st_dot(s){ const c={todo:'#58a6ff',progress:'#d29922',review:'#a37cf0',done:'#3fb950'}; return `<span class="sdot" style="background:${c[s]}"></span>${t('st')[s]||s}`; }
function due_fmt(d){ if(!d) return '—'; const dd=new Date(d), today=new Date(); today.setHours(0,0,0,0); const cls=dd<today?' overdue':''; return `<span class="${cls}">${dd.getDate()}/${dd.getMonth()+1}</span>`; }
function collab_stack_html(collabs){
  if (!collabs || !collabs.length) return '';
  const max = 3;
  const visible = collabs.slice(0, max);
  let html = '<span class="collab-stack">';
  visible.forEach(c=>{ html += `<span class="avatar-xs" style="background:${c.color}" title="${c.display_name}">${c.initials}</span>`; });
  html += '</span>';
  if (collabs.length > max) html += `<span class="collab-more">+${collabs.length - max}</span>`;
  return html;
}

function renderKanban(){
  const cols = {todo:[],progress:[],review:[],done:[]};
  let tasks = allTasks;
  if (onlyMine) tasks = tasks.filter(isMine);
  tasks.forEach(t=>{
    if(currentFilter==='critical' && t.priority!=='critical') return;
    if(currentFilter==='high' && t.priority!=='high') return;
    if(currentFilter==='overdue'){ if(!t.due_date) return; const d=new Date(t.due_date); d.setHours(0,0,0,0); const today=new Date(); today.setHours(0,0,0,0); if(d>=today || t.status==='done') return; }
    cols[t.status]?.push(t);
  });
  const titles = {todo:'TODO',progress:t('progress').toUpperCase(),review:t('review').toUpperCase(),done:'DONE'};
  document.getElementById('kanban-board').innerHTML = ['todo','progress','review','done'].map(s=>{
    const ts = cols[s];
    return `<div class="kcol"><div class="kcol-h">${titles[s]}<span class="kcol-n">${ts.length}</span></div>${ts.map(x=>`
      <div class="kcard" onclick="openEditTask(${x.id})">
        <div class="kcard-top">${pri_badge(x.priority)}<span class="proj-pill" style="color:${x.project_color};background:${x.project_color}22">${x.project_name||'—'}</span></div>
        <div class="kcard-title">${escapeHtml(x.title)}</div>
        <div class="kcard-meta">
          <div class="kcard-assignee">
            <div class="avatar-sm" style="background:${x.assignee_color||'#666'}">${x.assignee_initials||'?'}</div>
            <span>${x.assignee_name?escapeHtml(x.assignee_name):'—'}</span>
            ${collab_stack_html(x.collaborators)}
          </div>
          <span>${due_fmt(x.due_date)}</span>
        </div>
      </div>`).join('')}</div>`;
  }).join('');
}

function escapeHtml(s){ if(s==null) return ''; return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

function renderList(){
  let tasks = allTasks;
  if (onlyMine) tasks = tasks.filter(isMine);
  if (currentProjFilter) tasks = tasks.filter(t=>t.project_id===currentProjFilter);
  document.getElementById('list-tbody').innerHTML = tasks.map(x=>`
    <tr onclick="openEditTask(${x.id})" style="cursor:pointer">
      <td class="td-title">${escapeHtml(x.title)} ${collab_stack_html(x.collaborators)}</td>
      <td class="hide-mobile"><span class="proj-pill" style="color:${x.project_color};background:${x.project_color}22">${x.project_name||'—'}</span></td>
      <td><div style="display:flex;align-items:center;gap:6px"><div class="avatar-sm" style="background:${x.assignee_color||'#666'}">${x.assignee_initials||'?'}</div><span>${x.assignee_name?escapeHtml(x.assignee_name):'—'}</span></div></td>
      <td class="hide-mobile">${pri_badge(x.priority)}</td>
      <td>${st_dot(x.status)}</td>
      <td class="hide-mobile">${due_fmt(x.due_date)}</td>
    </tr>`).join('');
}

function filterTasks(f, el){ currentFilter=f; document.querySelectorAll('#kanban .filters .fbtn:not(.toggle)').forEach(b=>b.classList.remove('active')); el.classList.add('active'); renderKanban(); }
function filterListProj(p, el){ currentProjFilter=p; document.querySelectorAll('#list .filters .fbtn:not(.toggle)').forEach(b=>b.classList.remove('active')); el.classList.add('active'); renderList(); }

// === Calendar ===
function changeMonth(d){ currentMonth+=d; if(currentMonth<0){currentMonth=11;currentYear--} else if(currentMonth>11){currentMonth=0;currentYear++} renderCalendar(); }
async function renderCalendar(){
  document.getElementById('cal-title').textContent = `${t('months')[currentMonth]} ${currentYear}`;
  document.getElementById('cal-days').innerHTML = t('weekdays').map((d,i)=>`<div class="cal-day-name${i>=5?' cal-weekend-name':''}">${d}</div>`).join('');
  const r = await fetch(`/api/calendar?month=${currentMonth+1}&year=${currentYear}`);
  const d = await r.json();
  let lr = [];
  try { const lrr = await fetch(`/api/leave/calendar?month=${currentMonth+1}&year=${currentYear}`); if (lrr.ok) lr = await lrr.json(); } catch(e){}
  const key = `${currentYear}-${currentMonth+1}`;
  leaveCalCache[key] = lr;
  const first = new Date(currentYear, currentMonth, 1);
  const last = new Date(currentYear, currentMonth+1, 0);
  const startDay = (first.getDay() + 6) % 7;
  let cells = [];
  for(let i=0;i<startDay;i++) cells.push('<div class="cal-cell empty"></div>');
  const today = new Date(); today.setHours(0,0,0,0);
  const holidays = t('bg_holidays');
  let visibleTasks = d.tasks || [];
  if (onlyMine) visibleTasks = visibleTasks.filter(isMine);
  for(let day=1;day<=last.getDate();day++){
    const date = new Date(currentYear, currentMonth, day);
    const isToday = date.getTime()===today.getTime();
    const isWeekend = date.getDay()===0 || date.getDay()===6;
    const mmdd = String(currentMonth+1).padStart(2,'0')+'-'+String(day).padStart(2,'0');
    const isHoliday = !!holidays[mmdd];
    const dayTasks = visibleTasks.filter(t=>{ if(!t.due_date) return false; const td=new Date(t.due_date); return td.getDate()===day && td.getMonth()===currentMonth && td.getFullYear()===currentYear; });
    const dayLeaves = lr.filter(l=>{
      const sd = new Date(l.start_date), ed = new Date(l.end_date);
      const cur = new Date(currentYear, currentMonth, day);
      return cur>=sd && cur<=ed;
    });
    let leaveDots = '';
    if (dayLeaves.length){
      const mx = 4;
      leaveDots = '<div class="cal-leave-dots">';
      dayLeaves.slice(0,mx).forEach(l=>{
        const op = l.status==='pending' ? '0.5' : '1';
        leaveDots += `<span class="cal-leave-dot" style="background:${l.color};opacity:${op}" title="${l.display_name} — ${l.leave_type}"></span>`;
      });
      if (dayLeaves.length>mx) leaveDots += `<span class="cal-leave-more">+${dayLeaves.length-mx}</span>`;
      leaveDots += '</div>';
    }
    const cls = ['cal-cell'];
    if (isToday) cls.push('today');
    if (isWeekend) cls.push('cal-weekend');
    if (isHoliday) cls.push('cal-holiday');
    const dateHtml = isToday ? `<span class="cal-date"><span class="today-num">${day}</span></span>` : `<span class="cal-date">${day}</span>`;
    const holidayLabel = isHoliday ? `<div class="cal-holiday-label">${holidays[mmdd]}</div>` : '';
    cells.push(`<div class="${cls.join(' ')}" onclick="showDayTasks(${day})">${dateHtml}${holidayLabel}${leaveDots}<div class="cal-tasks">${dayTasks.slice(0,3).map(t=>{
      const isOver = new Date(t.due_date) < today && t.status!=='done';
      const lblColor = isOver ? '#f85149' : (t.assignee_color || '#888');
      return `<div class="cal-task" style="border-left:2px solid ${lblColor}"><span class="cal-task-text">${escapeHtml(t.title.substring(0,16))}${t.title.length>16?'...':''}</span></div>`;
    }).join('')}${dayTasks.length>3?`<div class="cal-more">+${dayTasks.length-3}</div>`:''}</div></div>`);
  }
  document.getElementById('cal-cells').innerHTML = cells.join('');
}

async function showDayTasks(day){
  let tasks = allTasks.filter(t=>{ if(!t.due_date) return false; const td=new Date(t.due_date); return td.getDate()===day && td.getMonth()===currentMonth && td.getFullYear()===currentYear; });
  if (onlyMine) tasks = tasks.filter(isMine);
  const dateLabel = `${day} ${t('months')[currentMonth]} ${currentYear}`;
  const key = `${currentYear}-${currentMonth+1}`;
  const lr = leaveCalCache[key] || [];
  const dayLeaves = lr.filter(l=>{
    const sd = new Date(l.start_date), ed = new Date(l.end_date);
    const cur = new Date(currentYear, currentMonth, day);
    return cur>=sd && cur<=ed;
  });
  let leaveBlock = '';
  if (dayLeaves.length){
    leaveBlock = `<div style="margin-bottom:14px"><div class="rpt-label" style="margin-top:0">${t('nav_leave')}</div>${dayLeaves.map(l=>{
      const op = l.status==='pending' ? '0.55' : '1';
      const tlabel = t('leave_'+l.leave_type) || l.leave_type;
      return `<div style="display:flex;align-items:center;gap:8px;padding:6px 0;opacity:${op}">
        <span class="avatar-sm" style="background:${l.color}">${l.initials}</span>
        <div style="flex:1;font-size:13px"><span style="font-weight:500">${escapeHtml(l.display_name)}</span>
        <span style="font-size:11px;color:var(--text-muted);margin-left:6px">${tlabel}${l.status==='pending'?' ('+t('leave_status_pending')+')':''}</span></div>
      </div>`;
    }).join('')}</div>`;
  }
  let body = leaveBlock;
  if (!tasks.length && !dayLeaves.length) body += `<div class="empty-state">${lang==='bg'?'Няма задачи':'No tasks'}</div>`;
  else if (tasks.length) body += `<div class="day-tasks">${tasks.map(x=>`
    <div class="rpt-card" onclick="closeModal();openEditTask(${x.id})">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <div style="font-size:14px;font-weight:500">${escapeHtml(x.title)}</div>
        ${pri_badge(x.priority)}
      </div>
      <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-muted)">
        <span>${st_dot(x.status)}</span>
        <span>${x.assignee_name?escapeHtml(x.assignee_name):'—'}</span>
      </div>
    </div>`).join('')}</div>`;
  document.getElementById('modal-title').textContent = dateLabel;
  document.getElementById('modal-body').innerHTML = body;
  document.getElementById('modal-overlay').classList.add('show');
}

function loadProjects(){
  fetch('/api/projects/list').then(r=>r.json()).then(data=>{
    document.getElementById('projects-list').innerHTML = data.map(p=>{
      const pct = p.total_tasks ? Math.round(p.done_tasks/p.total_tasks*100) : 0;
      return `<div class="proj-card"><div class="proj-head"><div style="display:flex;align-items:center;gap:8px"><span class="proj-dot" style="background:${p.color}"></span><span class="proj-name">${escapeHtml(p.name)}</span></div><span class="proj-pct">${pct}%</span></div><div class="proj-bar"><div class="proj-fill" style="width:${pct}%;background:${p.color}"></div></div><div class="proj-stats"><span>${p.total_tasks} ${t('all')}</span><span>${p.done_tasks} ${t('done')}</span></div></div>`;
    }).join('');
  });
}

// === Reports ===
let reportItems=[];
async function loadReports(){
  if (!IS_CEO && !IS_MANAGER){ reportItems=[]; document.getElementById('report-items').innerHTML=''; addReportItem(); }
  const r = await fetch('/api/reports'); const data = await r.json();
  document.getElementById('reports-list').innerHTML = data.map(r=>{
    const totalH = r.items.reduce((s,i)=>s+(i.hours||0),0);
    const dateStr = new Date(r.report_date).toLocaleDateString(lang==='bg'?'bg-BG':'en-US',{day:'numeric',month:'long',year:'numeric'});
    return `<div class="rpt-card">
      <div class="rpt-head">
        <div class="rpt-name"><div class="avatar-sm" style="background:${r.color}">${r.initials}</div><span>${escapeHtml(r.display_name)}</span><span style="color:var(--text-muted);font-size:11px">${dateStr}</span></div>
        <span class="rpt-hours-total">${totalH}h</span>
      </div>
      ${r.items.map(i=>`<div class="rpt-line"><div class="rpt-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg></div><div class="rpt-line-text">${escapeHtml(i.description)}</div><span class="rpt-line-hrs">${i.hours||0}h</span></div>`).join('')}
      ${r.notes.map(n=>`<div class="rpt-note">${escapeHtml(n.note)}</div>`).join('')}
    </div>`;
  }).join('');
}

function addReportItem(){
  reportItems.push({description:'',hours:'',task_id:''});
  renderReportItems();
}
function removeReportItem(i){ reportItems.splice(i,1); renderReportItems(); }
function updateRpt(i,field,val){ reportItems[i][field]=val; }
function renderReportItems(){
  const myTasks = allTasks.filter(t=> t.assignee_id===USER_ID || (t.collaborators && t.collaborators.some(c=>c.id===USER_ID)));
  document.getElementById('report-items').innerHTML = reportItems.map((it,i)=>`
    <div class="rpt-item-row">
      <div class="rpt-item-fields">
        <select onchange="updateRpt(${i},'task_id',this.value)">
          <option value="">— ${lang==='bg'?'Без задача':'No task'} —</option>
          ${myTasks.map(t=>`<option value="${t.id}" ${it.task_id==t.id?'selected':''}>${escapeHtml(t.title)}</option>`).join('')}
        </select>
        <div class="rpt-row-inner">
          <input type="text" placeholder="${lang==='bg'?'Какво направихте...':'What you did...'}" value="${escapeHtml(it.description)}" oninput="updateRpt(${i},'description',this.value)">
          <input type="number" placeholder="ч" min="0" max="24" step="0.5" value="${it.hours}" oninput="updateRpt(${i},'hours',parseFloat(this.value)||0)">
          <button class="modal-close" onclick="removeReportItem(${i})" style="font-size:18px;padding:2px 6px">×</button>
        </div>
      </div>
    </div>`).join('');
}
async function saveReport(){
  const items = reportItems.filter(i=>i.description.trim()).map(i=>({description:i.description.trim(),hours:i.hours||0,task_id:i.task_id||null}));
  const note = document.getElementById('report-note').value.trim();
  if(!items.length){ alert(lang==='bg'?'Добавете поне една задача':'Add at least one task'); return; }
  await fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items,note})});
  reportItems=[]; document.getElementById('report-note').value=''; renderReportItems(); addReportItem(); loadReports(); loadNotifications();
}

// === Dashboard ===
async function loadDashboard(){
  const r = await fetch('/api/dashboard'); const d = await r.json();
  if (d.error) return;
  document.getElementById('stat-total').textContent = d.total;
  document.getElementById('stat-done').textContent = d.done;
  document.getElementById('stat-pct').textContent = d.total? Math.round(d.done/d.total*100)+'%':'0%';
  document.getElementById('stat-overdue').textContent = d.overdue;
  document.getElementById('stat-critical').textContent = d.critical;
  if(statusChart) statusChart.destroy();
  statusChart = new Chart(document.getElementById('status-chart'),{type:'bar',data:{labels:[t('todo'),t('progress'),t('review'),t('completed')],datasets:[{data:[d.by_status.todo,d.by_status.progress,d.by_status.review,d.by_status.done],backgroundColor:['#58a6ff','#d29922','#a37cf0','#3fb950'],borderRadius:6,barThickness:34}]},options:{plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#8b949e',font:{size:11}},grid:{display:false}},y:{ticks:{color:'#8b949e',font:{size:11}},grid:{color:'rgba(48,54,61,0.5)'},beginAtZero:true}},maintainAspectRatio:false}});
  document.getElementById('team-grid').innerHTML = d.team.map(e=>{
    const pct = e.total_tasks ? Math.round(e.done_tasks/e.total_tasks*100):0;
    return `<div class="team-card"><div class="team-avatar" style="background:${e.color}">${e.initials}</div><div class="team-name">${escapeHtml(e.display_name)}</div><div class="team-info">${e.done_tasks}/${e.total_tasks} ${t('done')}</div><div class="progress-bar"><div class="progress-fill" style="width:${pct}%;background:${e.color}"></div></div><div class="team-rpt ${e.has_report_today?'has-rpt':'no-rpt'}">${e.hours_today||0}h ${lang==='bg'?'днес':'today'}</div></div>`;
  }).join('');
}

// === Modal ===
function closeModal(){ document.getElementById('modal-overlay').classList.remove('show'); }
document.getElementById('modal-overlay').addEventListener('click',e=>{ if(e.target.id==='modal-overlay') closeModal(); });

// === Collaborator picker ===
function renderCollabPicker(selectedIds, assigneeId){
  // Show all users except the current assignee
  const available = ALL_USERS.filter(u => u.id !== assigneeId);
  if (!available.length) return `<div class="collab-empty">${t('no_collaborators')}</div>`;
  return available.map(u=>{
    const sel = selectedIds.includes(u.id);
    const meLabel = u.id===USER_ID ? ' ('+t('me_label')+')' : '';
    return `<div class="collab-chip ${sel?'selected':''}" data-uid="${u.id}" onclick="toggleCollab(${u.id})">
      <span class="avatar-sm" style="background:${u.color}">${u.initials}</span>
      <span>${escapeHtml(u.display_name)}${meLabel}</span>
    </div>`;
  }).join('');
}

function toggleCollab(uid){
  const chip = document.querySelector(`.collab-chip[data-uid="${uid}"]`);
  if (!chip) return;
  chip.classList.toggle('selected');
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

// === Task modals ===
function openTaskModal(){
  // Default assignee is the current user; defaults: today's date
  const todayStr = new Date().toISOString().split('T')[0];
  const defaultAssignee = USER_ID;
  document.getElementById('modal-title').textContent = t('new_task');
  document.getElementById('modal-body').innerHTML = `
    <label>${t('title')}</label><input type="text" id="t-title" class="modal-input">
    <label>${t('description')}</label><textarea id="t-desc" rows="2" class="modal-input"></textarea>
    <label>${t('assignee')}</label>
    <select id="t-assignee" class="modal-input" onchange="refreshCollabPickerFor(parseInt(this.value))">
      ${ALL_USERS.map(u=>`<option value="${u.id}" ${u.id===defaultAssignee?'selected':''}>${escapeHtml(u.display_name)}${u.id===USER_ID?' ('+t('me_label')+')':''}</option>`).join('')}
    </select>
    <label>${t('collaborators')} <span style="color:var(--text-muted);font-weight:400;text-transform:none;letter-spacing:0">${t('add_collaborators')}</span></label>
    <div class="collab-picker" id="collab-picker">${renderCollabPicker([], defaultAssignee)}</div>
    <label>${t('priority')}</label>
    <select id="t-pri" class="modal-input"><option value="critical">${t('pri').critical}</option><option value="high">${t('pri').high}</option><option value="medium" selected>${t('pri').medium}</option><option value="low">${t('pri').low}</option></select>
    <label>${t('project')}</label>
    <select id="t-proj" class="modal-input">${PROJECTS.map(p=>`<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('')}</select>
    <label>${t('deadline')}</label><input type="date" id="t-due" class="modal-input" value="${todayStr}">
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveNewTask()">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}

async function saveNewTask(){
  const title = document.getElementById('t-title').value.trim();
  if(!title){ alert(t('title')); return; }
  const aid = parseInt(document.getElementById('t-assignee').value);
  const collabs = getSelectedCollabs().filter(id => id !== aid);
  await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
    title, description:document.getElementById('t-desc').value.trim(),
    priority:document.getElementById('t-pri').value, status:'todo',
    assignee_id: aid,
    project_id: parseInt(document.getElementById('t-proj').value),
    due_date: document.getElementById('t-due').value || null,
    collaborators: collabs
  })});
  closeModal(); loadTasks(); loadNotifications();
}

function openEditTask(tid){
  const x = allTasks.find(t=>t.id===tid); if(!x) return;
  const canDelete = IS_PRIVILEGED || x.created_by === USER_ID;
  const collabIds = (x.collaborators||[]).map(c=>c.id);
  const aid = x.assignee_id || USER_ID;
  document.getElementById('modal-title').textContent = t('edit_task');
  const creatorBlock = x.creator_name ? `<div style="font-size:11px;color:var(--text-muted);margin-bottom:10px">${t('created_by')}: ${escapeHtml(x.creator_name)}</div>` : '';
  document.getElementById('modal-body').innerHTML = `
    ${creatorBlock}
    <label>${t('title')}</label><input type="text" id="e-title" class="modal-input" value="${escapeHtml(x.title)}">
    <label>${t('description')}</label><textarea id="e-desc" rows="2" class="modal-input">${escapeHtml(x.description||'')}</textarea>
    <label>${t('assignee')}</label>
    <select id="e-assignee" class="modal-input" onchange="refreshCollabPickerFor(parseInt(this.value))">
      ${ALL_USERS.map(u=>`<option value="${u.id}" ${u.id===aid?'selected':''}>${escapeHtml(u.display_name)}${u.id===USER_ID?' ('+t('me_label')+')':''}</option>`).join('')}
    </select>
    <label>${t('collaborators')} <span style="color:var(--text-muted);font-weight:400;text-transform:none;letter-spacing:0">${t('add_collaborators')}</span></label>
    <div class="collab-picker" id="collab-picker">${renderCollabPicker(collabIds.filter(id=>id!==aid), aid)}</div>
    <label>${t('status')}</label>
    <select id="e-status" class="modal-input"><option value="todo" ${x.status==='todo'?'selected':''}>${t('st').todo}</option><option value="progress" ${x.status==='progress'?'selected':''}>${t('st').progress}</option><option value="review" ${x.status==='review'?'selected':''}>${t('st').review}</option><option value="done" ${x.status==='done'?'selected':''}>${t('st').done}</option></select>
    <label>${t('priority')}</label>
    <select id="e-pri" class="modal-input"><option value="critical" ${x.priority==='critical'?'selected':''}>${t('pri').critical}</option><option value="high" ${x.priority==='high'?'selected':''}>${t('pri').high}</option><option value="medium" ${x.priority==='medium'?'selected':''}>${t('pri').medium}</option><option value="low" ${x.priority==='low'?'selected':''}>${t('pri').low}</option></select>
    <label>${t('project')}</label>
    <select id="e-proj" class="modal-input">${PROJECTS.map(p=>`<option value="${p.id}" ${x.project_id===p.id?'selected':''}>${escapeHtml(p.name)}</option>`).join('')}</select>
    <label>${t('deadline')}</label><input type="date" id="e-due" class="modal-input" value="${x.due_date||''}">
    <div style="margin-top:14px"><button class="btn-outline btn-sm" onclick="loadTaskAudit(${x.id})">${t('audit_history')}</button></div>
    <div id="audit-${x.id}" style="display:none"></div>
    <div class="modal-actions">${canDelete?`<button class="btn-danger" onclick="deleteTask(${x.id})">${t('delete')}</button>`:''}<button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveEditTask(${x.id})">${t('save_changes')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}

async function loadTaskAudit(tid){
  const wrap = document.getElementById('audit-'+tid);
  if (wrap.style.display==='block'){ wrap.style.display='none'; return; }
  wrap.style.display='block';
  wrap.innerHTML = `<div class="audit-list"><div class="audit-item">${t('audit_loading')}</div></div>`;
  const r = await fetch(`/api/audit/task/${tid}`); const data = await r.json();
  if (!data.length){ wrap.innerHTML = `<div class="audit-list"><div class="audit-item">${t('audit_no_history')}</div></div>`; return; }
  wrap.innerHTML = `<div class="audit-list">${data.map(a=>{
    const dt = new Date(a.created_at);
    const when = dt.toLocaleDateString(lang==='bg'?'bg-BG':'en-US',{day:'numeric',month:'short'})+', '+dt.toLocaleTimeString(lang==='bg'?'bg-BG':'en-US',{hour:'2-digit',minute:'2-digit'});
    let actionLabel = t('audit_'+a.action) || a.action;
    let detail = '';
    if (a.details && a.action==='updated'){
      const labels = [];
      Object.keys(a.details).forEach(k=>{
        if (k==='collaborators'){
          const ch = a.details[k];
          let parts = [];
          if (ch.added && ch.added.length) parts.push('+'+ch.added.length);
          if (ch.removed && ch.removed.length) parts.push('-'+ch.removed.length);
          labels.push(t('audit_'+k)+' ('+parts.join(', ')+')');
        } else {
          labels.push(t('audit_'+k) || k);
        }
      });
      detail = labels.join(', ');
    }
    return `<div class="audit-item">${a.display_name?`<span class="avatar-xs" style="background:${a.color};border:none">${a.initials}</span>`:''}<div style="flex:1"><span class="audit-who">${escapeHtml(a.display_name||'?')}</span> <span class="audit-action">${actionLabel}</span>${detail?`<div class="audit-detail">${escapeHtml(detail)}</div>`:''}</div><span class="audit-when">${when}</span></div>`;
  }).join('')}</div>`;
}

async function saveEditTask(tid){
  const aid = parseInt(document.getElementById('e-assignee').value);
  const collabs = getSelectedCollabs().filter(id => id !== aid);
  await fetch(`/api/tasks/${tid}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({
    title:document.getElementById('e-title').value.trim(),
    description:document.getElementById('e-desc').value.trim(),
    priority:document.getElementById('e-pri').value,
    status:document.getElementById('e-status').value,
    assignee_id: aid,
    project_id: parseInt(document.getElementById('e-proj').value),
    due_date: document.getElementById('e-due').value || null,
    collaborators: collabs
  })});
  closeModal(); loadTasks(); loadNotifications();
}

async function deleteTask(tid){
  if(!confirm(t('confirm_delete'))) return;
  const r = await fetch(`/api/tasks/${tid}`,{method:'DELETE'});
  if (r.status===403){ alert(lang==='bg'?'Нямате право да изтриете тази задача':'You do not have permission to delete this task'); return; }
  closeModal(); loadTasks(); loadNotifications();
}

// === Notifications ===
async function loadNotifications(){
  try{
    const r = await fetch('/api/notifications'); const d = await r.json();
    const items = [];
    if (d.overdue>0) items.push({icon:'⚠️',color:'#f85149',label:t('tasks_overdue'),count:d.overdue,onclick:()=>{document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.nav-btn').forEach(b=>{if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes('kanban'))b.classList.add('active')});switchView('kanban',document.querySelector('.nav-btn'));filterTasks('overdue',document.querySelector('#kanban .filters .fbtn:nth-child(4)'));toggleNotifications()}});
    if (d.today>0) items.push({icon:'📅',color:'#d29922',label:t('tasks_today'),count:d.today});
    if (!d.has_report_today && !IS_CEO && !IS_MANAGER) items.push({icon:'📝',color:'#58a6ff',label:t('no_report_today'),count:'!',onclick:()=>{switchView('reports',document.querySelectorAll('.nav-btn')[4]);toggleNotifications()}});
    if (d.team_no_report>0) items.push({icon:'👥',color:'#a37cf0',label:t('team_no_report'),count:d.team_no_report});
    if (d.pending_leave>0) items.push({icon:'🏖️',color:'#3fb950',label:t('notif_pending_leave_t'),count:d.pending_leave,onclick:()=>{const navs=document.querySelectorAll('.nav-btn');for(const b of navs){if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes('leave')){switchView('leave',b);break;}}toggleNotifications()}});
    const total = items.reduce((s,i)=>s+(typeof i.count==='number'?i.count:1),0);
    const badge = document.getElementById('notif-badge');
    if (total>0){ badge.textContent = total>99?'99+':total; badge.style.display='flex'; } else { badge.style.display='none'; }
    document.getElementById('notif-list').innerHTML = items.length? items.map((it,idx)=>`<div class="notif-item" data-idx="${idx}"><div class="notif-icon" style="background:${it.color}22;color:${it.color}">${it.icon}</div><div class="notif-content"><span>${it.label}</span><span class="notif-count" style="color:${it.color}">${it.count}</span></div></div>`).join('') : `<div class="notif-empty">${t('no_notifications')}</div>`;
    document.querySelectorAll('.notif-item').forEach(el=>{ const i=parseInt(el.getAttribute('data-idx')); if(items[i].onclick) el.onclick=items[i].onclick; });
  }catch(e){}
}
function toggleNotifications(e){ if(e)e.stopPropagation(); document.getElementById('notif-popup').classList.toggle('show'); }
document.addEventListener('click',e=>{ const p=document.getElementById('notif-popup'),b=document.getElementById('notif-btn'); if(p&&b&&!p.contains(e.target)&&!b.contains(e.target))p.classList.remove('show'); });
setInterval(loadNotifications,60000);

// === Admin ===
async function loadAdmin(){
  const r = await fetch('/api/users?include_all=1'); const data = await r.json();
  document.getElementById('admin-users-list').innerHTML = data.map(u=>{
    if (u.role==='ceo') return `<div class="admin-card"><div class="admin-card-left"><div class="avatar-sm" style="background:${u.color};width:30px;height:30px">${u.initials}</div><div><div class="admin-name">${escapeHtml(u.display_name)} <span class="user-badge">CEO</span></div><div class="admin-sub">@${u.username}</div></div></div><div class="admin-card-actions"><button class="btn-outline btn-sm" onclick="openChangeMyPassword()">${t('change_my_password')}</button></div></div>`;
    return `<div class="admin-card"><div class="admin-card-left"><div class="avatar-sm" style="background:${u.color};width:30px;height:30px">${u.initials}</div><div><div class="admin-name">${escapeHtml(u.display_name)}${u.role==='manager'?` <span class="user-badge">${t('manager_role').toUpperCase()}</span>`:''}</div><div class="admin-sub">@${u.username}</div></div></div><div class="admin-card-actions"><button class="btn-outline btn-sm" onclick="openEditUser(${u.id},'${escapeHtml(u.display_name)}','${u.username}','${u.color}','${u.role}')">${lang==='bg'?'Редакт.':'Edit'}</button><button class="btn-outline btn-sm" onclick="resetUserPass(${u.id})">${lang==='bg'?'Нова парола':'New pass'}</button><button class="btn-danger btn-sm" style="margin:0" onclick="deleteUser(${u.id})">${t('delete')}</button></div></div>`;
  }).join('');
  const pr = await fetch('/api/projects/list'); const pd = await pr.json();
  document.getElementById('admin-projects-list').innerHTML = pd.map(p=>`<div class="admin-card"><div class="admin-card-left"><span class="proj-dot" style="background:${p.color};width:14px;height:14px"></span><div><div class="admin-name">${escapeHtml(p.name)}</div><div class="admin-sub">${p.total_tasks} ${t('all').toLowerCase()}, ${p.done_tasks} ${t('done')}</div></div></div><div class="admin-card-actions"><button class="btn-outline btn-sm" onclick="openEditProj(${p.id},'${escapeHtml(p.name)}','${p.color}','${escapeHtml(p.description||'')}')">${lang==='bg'?'Редакт.':'Edit'}</button><button class="btn-danger btn-sm" style="margin:0" onclick="deleteProj(${p.id})">${t('delete')}</button></div></div>`).join('');
  loadBalancesAdmin();
  loadBackups();
}
async function loadBalancesAdmin(){
  const year = new Date().getFullYear();
  const ur = await fetch('/api/users'); const users = await ur.json();
  const rows = await Promise.all(users.map(async u=>{
    const br = await fetch(`/api/leave/balance/${u.id}?year=${year}`); const b = await br.json();
    return { user: u, bal: b };
  }));
  document.getElementById('admin-balances-list').innerHTML = rows.map(({user,bal})=>`
    <div class="admin-card">
      <div class="admin-card-left">
        <div class="avatar-sm" style="background:${user.color};width:30px;height:30px">${user.initials}</div>
        <div><div class="admin-name">${escapeHtml(user.display_name)}</div>
        <div class="admin-sub">${bal.used}/${bal.total} ${lang==='bg'?'дни използвани':'days used'} · ${bal.remaining} ${lang==='bg'?'остават':'remaining'}</div></div>
      </div>
      <div class="admin-card-actions">
        <input type="number" id="bal-${user.id}" value="${bal.total}" min="0" max="60" style="width:60px;padding:6px;background:var(--bg-surface);border:1px solid var(--border);border-radius:6px;color:var(--text-primary);font-family:inherit;font-size:12px">
        <button class="btn-outline btn-sm" onclick="saveBalance(${user.id})">${t('leave_save')}</button>
      </div>
    </div>`).join('');
}
async function saveBalance(uid){
  const v = parseInt(document.getElementById('bal-'+uid).value)||0;
  await fetch(`/api/leave/balance/${uid}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({year:new Date().getFullYear(),paid_total:v})});
  loadBalancesAdmin();
}
function openChangeMyPassword(){
  document.getElementById('modal-title').textContent = t('change_my_password');
  document.getElementById('modal-body').innerHTML = `
    <label>${t('current_password')}</label><input type="password" id="cmp-old" class="modal-input">
    <label>${t('new_password')}</label><input type="password" id="cmp-new" class="modal-input">
    <label>${t('confirm_new_password')}</label><input type="password" id="cmp-confirm" class="modal-input">
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveMyPassword()">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}
async function saveMyPassword(){
  const oldp = document.getElementById('cmp-old').value;
  const newp = document.getElementById('cmp-new').value;
  const conf = document.getElementById('cmp-confirm').value;
  if (newp !== conf){ alert(t('password_mismatch')); return; }
  if (newp.length < 4){ alert(t('password_too_short')); return; }
  const r = await fetch('/api/me/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({old_password:oldp,new_password:newp})});
  if (r.ok){ alert(t('password_changed')); closeModal(); }
  else if (r.status===403){ alert(t('wrong_old_password')); }
  else { alert(lang==='bg'?'Грешка':'Error'); }
}
function openAddUser(){
  document.getElementById('modal-title').textContent = t('add_employee_t');
  document.getElementById('modal-body').innerHTML = `<label>${t('name')}</label><input type="text" id="u-name" class="modal-input"><label>${t('username_field')}</label><input type="text" id="u-user" class="modal-input"><label>${t('password')}</label><input type="text" id="u-pass" class="modal-input" value="1234"><label>${t('role')}</label><select id="u-role" class="modal-input"><option value="employee" selected>${t('employee')}</option><option value="manager">${t('manager_role')}</option></select><label>${t('color')}</label><input type="color" id="u-color" class="modal-input" value="#185FA5"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveUser()">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}
async function saveUser(){
  const name=document.getElementById('u-name').value.trim(); const user=document.getElementById('u-user').value.trim();
  if(!name||!user){ alert(t('name')+'/'+t('username_field')); return; }
  await fetch('/api/users',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({display_name:name,username:user,password:document.getElementById('u-pass').value,color:document.getElementById('u-color').value,role:document.getElementById('u-role').value})});
  closeModal(); location.reload();
}
function openEditUser(id, name, user, color, role){
  document.getElementById('modal-title').textContent = t('edit_employee');
  document.getElementById('modal-body').innerHTML = `<label>${t('name')}</label><input type="text" id="u-name" class="modal-input" value="${name}"><label>${t('username_field')}</label><input type="text" id="u-user" class="modal-input" value="${user}"><label>${t('role')}</label><select id="u-role" class="modal-input"><option value="employee" ${role==='employee'?'selected':''}>${t('employee')}</option><option value="manager" ${role==='manager'?'selected':''}>${t('manager_role')}</option></select><label>${t('password')} (${lang==='bg'?'празно = без промяна':'leave empty to keep'})</label><input type="text" id="u-pass" class="modal-input" placeholder="••••"><label>${t('color')}</label><input type="color" id="u-color" class="modal-input" value="${color}"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="updateUser(${id})">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}
async function updateUser(id){
  const data={display_name:document.getElementById('u-name').value.trim(),username:document.getElementById('u-user').value.trim(),color:document.getElementById('u-color').value,role:document.getElementById('u-role').value};
  const p=document.getElementById('u-pass').value.trim(); if(p) data.password=p;
  await fetch(`/api/users/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  closeModal(); location.reload();
}
async function resetUserPass(id){
  const r=await fetch(`/api/users/${id}/reset-password`,{method:'POST'}); const d=await r.json();
  alert((lang==='bg'?'Нова парола: ':'New password: ')+d.new_password);
}
async function deleteUser(id){
  if(!confirm(t('confirm_delete_user'))) return;
  await fetch(`/api/users/${id}`,{method:'DELETE'}); loadAdmin();
}
function openAddProject(){
  document.getElementById('modal-title').textContent = t('add_project_t');
  document.getElementById('modal-body').innerHTML = `<label>${t('name')}</label><input type="text" id="p-name" class="modal-input"><label>${lang==='bg'?'Описание':'Description'}</label><textarea id="p-desc" rows="2" class="modal-input"></textarea><label>${t('color')}</label><input type="color" id="p-color" class="modal-input" value="#0B3D6B"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="saveProject()">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}
async function saveProject(){
  await fetch('/api/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('p-name').value.trim(),color:document.getElementById('p-color').value,description:document.getElementById('p-desc').value.trim()})});
  closeModal(); location.reload();
}
function openEditProj(id, name, color, desc){
  document.getElementById('modal-title').textContent = t('edit_project');
  document.getElementById('modal-body').innerHTML = `<label>${t('name')}</label><input type="text" id="p-name" class="modal-input" value="${name}"><label>${lang==='bg'?'Описание':'Description'}</label><textarea id="p-desc" rows="2" class="modal-input">${desc}</textarea><label>${t('color')}</label><input type="color" id="p-color" class="modal-input" value="${color}"><div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="updateProj(${id})">${t('save')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}
async function updateProj(id){
  await fetch(`/api/projects/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:document.getElementById('p-name').value.trim(),color:document.getElementById('p-color').value,description:document.getElementById('p-desc').value.trim()})});
  closeModal(); location.reload();
}
async function deleteProj(id){
  if(!confirm(t('confirm_delete_proj'))) return;
  await fetch(`/api/projects/${id}`,{method:'DELETE'}); loadAdmin();
}

// === Backups ===
async function loadBackups(){
  const r = await fetch('/api/backups'); const data = await r.json();
  if (!Array.isArray(data)) return;
  const fmt = (b)=>{ const kb = b/1024; if (kb<1024) return kb.toFixed(0)+' KB'; return (kb/1024).toFixed(1)+' MB'; };
  document.getElementById('admin-backups-list').innerHTML = data.length? data.map(b=>{
    const dt = new Date(b.created*1000);
    const when = dt.toLocaleDateString(lang==='bg'?'bg-BG':'en-US',{day:'numeric',month:'short',year:'numeric'})+' '+dt.toLocaleTimeString(lang==='bg'?'bg-BG':'en-US',{hour:'2-digit',minute:'2-digit'});
    return `<div class="backup-row"><div><div class="backup-name">${b.name}</div><div class="backup-size">${when} · ${fmt(b.size)}</div></div><div class="backup-actions"><a href="/api/backups/download/${b.name}" class="btn-outline btn-sm" style="text-decoration:none;display:inline-flex;align-items:center">${lang==='bg'?'Свали':'Download'}</a></div></div>`;
  }).join('') : `<div class="empty-state">${lang==='bg'?'Няма резервни копия':'No backups'}</div>`;
}
async function createBackup(){
  if (!confirm(t('confirm_create_backup'))) return;
  const r = await fetch('/api/backups/create',{method:'POST'}); const d = await r.json();
  if (d.ok){ alert(t('backup_created')+': '+d.name); loadBackups(); } else { alert(t('backup_failed')); }
}

// === Leave ===
async function loadLeaveView(){
  const wrap = document.getElementById('leave-content');
  let html = '';
  // My balance
  try {
    const br = await fetch('/api/leave/balance'); const bal = await br.json();
    html += `<div class="rpt-form"><div class="rpt-form-title">${t('leave_my_balance')} ${bal.year}</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:8px">
        <div style="text-align:center;padding:12px;background:var(--bg-surface);border-radius:10px"><div style="font-size:22px;font-weight:700;color:var(--accent-green)">${bal.remaining}</div><div style="font-size:11px;color:var(--text-muted);margin-top:2px">${t('leave_remaining')}</div></div>
        <div style="text-align:center;padding:12px;background:var(--bg-surface);border-radius:10px"><div style="font-size:22px;font-weight:700">${bal.used}</div><div style="font-size:11px;color:var(--text-muted);margin-top:2px">${t('leave_used')}</div></div>
        <div style="text-align:center;padding:12px;background:var(--bg-surface);border-radius:10px"><div style="font-size:22px;font-weight:700;color:var(--gold)">${bal.total}</div><div style="font-size:11px;color:var(--text-muted);margin-top:2px">${t('leave_total')}</div></div>
      </div>
      <div style="margin-top:14px;text-align:right"><button class="btn-primary btn-sm" onclick="openLeaveRequest()">+ ${t('leave_request')}</button></div>
    </div>`;
  } catch(e){}
  // Pending
  if (IS_PRIVILEGED){
    try{
      const pr = await fetch('/api/leave/requests?status=pending'); const pdata = await pr.json();
      if (Array.isArray(pdata) && pdata.length){
        html += `<div class="sect-title">${t('leave_pending_approval')}</div>`;
        html += pdata.map(r=>renderLeaveRow(r,true)).join('');
      }
    }catch(e){}
  }
  // My requests + history
  try{
    const mr = await fetch('/api/leave/requests'+(IS_PRIVILEGED?`?user_id=${USER_ID}`:'')); const mdata = await mr.json();
    html += `<div class="sect-title">${t('leave_my_requests')}</div>`;
    if (Array.isArray(mdata) && mdata.length){
      html += mdata.map(r=>renderLeaveRow(r,false)).join('');
    } else {
      html += `<div class="empty-state">${t('leave_no_requests')}</div>`;
    }
  }catch(e){}
  wrap.innerHTML = html;
}

function renderLeaveRow(r, allowDecide){
  const tlabel = t('leave_'+r.leave_type) || r.leave_type;
  const sLabel = t('leave_status_'+r.status);
  const sColor = {pending:'#d29922', approved:'#3fb950', rejected:'#f85149'}[r.status];
  const sd = new Date(r.start_date), ed = new Date(r.end_date);
  const dRange = `${sd.getDate()}/${sd.getMonth()+1}` + (r.start_date===r.end_date?'':` – ${ed.getDate()}/${ed.getMonth()+1}`);
  const reasonLine = r.reason ? `<div style="font-size:12px;color:var(--text-secondary);margin-top:6px;font-style:italic">"${escapeHtml(r.reason)}"</div>` : '';
  const noteLine = r.decision_note ? `<div style="font-size:11px;color:var(--text-muted);margin-top:4px">${escapeHtml(r.decision_note)}</div>` : '';
  let actions = '';
  if (allowDecide && r.status==='pending'){
    actions = `<div style="margin-top:8px;display:flex;gap:6px"><button class="btn-primary btn-sm" onclick="decideLeave(${r.id},'approved')">${t('leave_approve')}</button><button class="btn-danger btn-sm" style="margin:0" onclick="decideLeave(${r.id},'rejected')">${t('leave_reject')}</button></div>`;
  }
  if (r.user_id===USER_ID && r.status==='pending'){
    actions += `<div style="margin-top:8px"><button class="btn-outline btn-sm" onclick="cancelLeave(${r.id})">${t('leave_cancel')}</button></div>`;
  }
  return `<div class="rpt-card">
    <div class="rpt-head">
      <div class="rpt-name"><div class="avatar-sm" style="background:${r.color}">${r.initials}</div><span>${escapeHtml(r.display_name)}</span><span style="color:var(--text-muted);font-size:11px">${tlabel}</span></div>
      <span style="font-size:11px;font-weight:600;color:${sColor};background:${sColor}22;padding:3px 10px;border-radius:20px">${sLabel}</span>
    </div>
    <div style="display:flex;gap:14px;font-size:12px;color:var(--text-secondary)">
      <span>📅 ${dRange}</span>
      <span>⏱ ${r.working_days} ${t('leave_days')}</span>
    </div>
    ${reasonLine}${noteLine}${actions}
  </div>`;
}

function openLeaveRequest(){
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('modal-title').textContent = t('leave_request');
  document.getElementById('modal-body').innerHTML = `
    <label>${t('leave_type')}</label>
    <select id="lr-type" class="modal-input"><option value="paid">${t('leave_paid')}</option><option value="sick">${t('leave_sick')}</option><option value="unpaid">${t('leave_unpaid')}</option><option value="other">${t('leave_other')}</option></select>
    ${IS_CEO?`<label>${t('leave_assign_other')}</label><select id="lr-user" class="modal-input"><option value="">— ${t('me_label')} —</option>${USERS.map(u=>`<option value="${u.id}">${escapeHtml(u.display_name)}</option>`).join('')}</select>`:''}
    <label>${t('leave_start')}</label><input type="date" id="lr-start" class="modal-input" value="${today}">
    <label>${t('leave_end')}</label><input type="date" id="lr-end" class="modal-input" value="${today}">
    <label>${t('leave_reason')}</label><textarea id="lr-reason" rows="2" class="modal-input"></textarea>
    <div class="modal-actions"><button class="btn-outline" onclick="closeModal()">${t('cancel')}</button><button class="btn-primary" onclick="submitLeave()">${t('leave_submit')}</button></div>`;
  document.getElementById('modal-overlay').classList.add('show');
}

async function submitLeave(){
  const data = {
    leave_type: document.getElementById('lr-type').value,
    start_date: document.getElementById('lr-start').value,
    end_date: document.getElementById('lr-end').value,
    reason: document.getElementById('lr-reason').value.trim()
  };
  const ut = document.getElementById('lr-user');
  if (ut && ut.value) data.user_id = parseInt(ut.value);
  const r = await fetch('/api/leave/requests',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const d = await r.json();
  if (d.error){ alert(d.error+(d.remaining!==undefined?` (${lang==='bg'?'остават':'remaining'}: ${d.remaining}, ${lang==='bg'?'искани':'requested'}: ${d.requested||''})`:'')); return; }
  closeModal(); loadLeaveView(); loadNotifications();
}

async function decideLeave(lid, decision){
  let note = '';
  if (decision==='rejected'){
    note = prompt(t('leave_decision_note')) || '';
  }
  const r = await fetch(`/api/leave/requests/${lid}/decide`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({decision,note})});
  const d = await r.json();
  if (d.error){ alert(d.error); return; }
  loadLeaveView(); loadNotifications();
}

async function cancelLeave(lid){
  if (!confirm(t('confirm_delete'))) return;
  const r = await fetch(`/api/leave/requests/${lid}`,{method:'DELETE'});
  const d = await r.json();
  if (d.error){ alert(d.error); return; }
  loadLeaveView(); loadNotifications();
}

// === Init ===
applyI18n();
loadTasks();
renderCalendar();
loadProjects();
loadNotifications();
</script>
</body>
</html>
'''

LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAMgAAAAoCAYAAAC7HLUcAAAAcUlEQVR42u3TUQkAQAhEQSPa8bpYSwvcn+DXLEyBhRdhZmZmZmZ2uHrZwJ9AQCAgEBAICAQEAgIBgYBAQCCAQEAgIBAQCAgEBAICAYGAQEAgTgCBgEBAICAQEAgIBAQCAgGBAAIBgcA2EDMzMzMzs8MN19j77oPXHtUAAAAASUVORK5CYII="
BOAT_B64 = "iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAACW0lEQVR42u3UQQ2AMBBE0apACzJwgDi8YKs9YYCwh2HfS8bApv1jAAAAAAAAAAAAAAAAAAAAAAAAAPzMfR3TFYCIWD1zDSAiVqIFCBZARaxEC4iKlWgBUbESLUCwACpiJVpAVKxECxAsgIpYiRYQFSvRAqJiJVqAYAFUxEq0gKhYiRYgWIBYiRbQPlaiBUTFSrQAwQLESrSA9rESLSAqVqIFCBYgVqIFtI+VaAGCBYiVaAHtYyVaIFZTtADBEiyge6xEC8RKtADBEiygfaxEC8RKtACxEi1AsAQLxEq0ALESLUCwBAvESrQAsRItECuxEi0QLMECxEq0QKxMtECsRAsQLMECsTLRArESLUCwBAvEykQLxEq0ALESLRAsEywQK9ECxEq0QLBMsECsRAvEykQLxMpECwRLsECsTLRArEy0+Ni2n9PM3k9FBMtMsBAtM7ESLDPBQrDMBAvRMhMrwTITLETLTKwQLDPBEi0zsUKwzAQL0TITK8EyEywEy0ywEC0zsRIsM8FCtMzECsEyEyzRMhMrBMtMsPBoTawQLDPBQrDMBEu0zMQKwTITLETLTKwEy0ywEC0zsUKwzARLtMzECsEyEywEy0ywRMtMrBAsM8FCtMzESrDMBAvRMhMrBMsEC9EyEysEy0ywECwTLETLTKwQLDPBQrRMrBAsM8FCtMzECsEywUK0zMQKwTITLATLBAvRMhMrBMtMsBAtEysEy0ywEC0zvxDBMsFCtMzECsEywQLBMsFCtMzECsEywQLRMrFCsMwEC9EysQLBMsFCtMzECsEywepmAd8tyjQNIr1OAAAAAElFTkSuQmCC"
