"""
╔══════════════════════════════════════════════════════════════╗
║    SS TEAM PORTAL v6.0 — Complete Upgrade                    ║
║    • PIN Hashing (SHA-256)  • Employee DB (CRUD)             ║
║    • Monthly Reports        • 5 Beautiful Themes             ║
║    • GPS Auto-detect        • Connection Pooling             ║
║    • Pagination             • Overtime Tracking              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import sqlite3
import hashlib
import math
from datetime import datetime, date, timedelta
import pandas as pd
import os
import json
from dotenv import load_dotenv
import calendar

load_dotenv()

# ─── CONFIG ────────────────────────────────────────────────────
OFFICE_LAT  = float(os.getenv("OFFICE_LAT", "30.124458"))
OFFICE_LON  = float(os.getenv("OFFICE_LON", "71.386285"))
OFFICE_KM   = float(os.getenv("OFFICE_KM", "96"))
ADMIN_PASS  = os.getenv("ADMIN_PASS", "admin123")
DB_PATH     = os.getenv("DB_PATH", "ss_portal.db")
SHIFT_START = int(os.getenv("SHIFT_START_HOUR", "8"))
SHIFT_END   = int(os.getenv("SHIFT_END_HOUR", "18"))
OVERTIME_HOURS = float(os.getenv("OVERTIME_HOURS", "8"))
PAGE_SIZE   = 15

DEPARTMENTS = ["", "WIP", "Cutting", "Sewing", "Washing", "Finishing & Packing", "Warehouse"]
DESIGNATIONS = ["Team Lead", "Computer Operator", "Executive Office", "Supervisor", "Manager", "Other"]
LEAVE_TYPES = ["Sick Leave", "Casual Leave", "Short Leave", "Out Miss Correction"]

ADMIN_PERMISSIONS = {
    "admin": {"gps_control": True, "device_reset": True, "alerts": True, "emp_manage": True},
}

# ─── 5 BEAUTIFUL THEMES ────────────────────────────────────────
THEMES = {
    "🌌 Midnight Indigo": {
        "primary": "#6366f1",
        "primary_dark": "#4f46e5",
        "accent": "#ec4899",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#0f172a",
        "card_bg": "#1e293b",
        "text_primary": "#f1f5f9",
        "text_secondary": "#cbd5e1",
        "border": "rgba(99,102,241,0.25)",
        "glow": "99,102,241",
        "sidebar_bg": "linear-gradient(160deg, #0f172a 0%, #1e293b 100%)",
        "header_bg": "linear-gradient(90deg, #0f172a, #1e293b)",
        "card_grad": "linear-gradient(135deg, rgba(99,102,241,0.1), rgba(236,72,153,0.06))",
        "btn_grad": "linear-gradient(135deg, #6366f1, #4f46e5)",
        "btn_hover": "linear-gradient(135deg, #ec4899, #db2777)",
        "logo_grad": "linear-gradient(135deg,#6366f1,#ec4899)",
    },
    "🌿 Forest Emerald": {
        "primary": "#10b981",
        "primary_dark": "#059669",
        "accent": "#34d399",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#0a1628",
        "card_bg": "#0f2027",
        "text_primary": "#ecfdf5",
        "text_secondary": "#a7f3d0",
        "border": "rgba(16,185,129,0.25)",
        "glow": "16,185,129",
        "sidebar_bg": "linear-gradient(160deg, #0a1628 0%, #0d2318 100%)",
        "header_bg": "linear-gradient(90deg, #0a1628, #0d2318)",
        "card_grad": "linear-gradient(135deg, rgba(16,185,129,0.1), rgba(52,211,153,0.05))",
        "btn_grad": "linear-gradient(135deg, #10b981, #059669)",
        "btn_hover": "linear-gradient(135deg, #34d399, #10b981)",
        "logo_grad": "linear-gradient(135deg,#10b981,#34d399)",
    },
    "🔥 Crimson Blaze": {
        "primary": "#ef4444",
        "primary_dark": "#dc2626",
        "accent": "#f97316",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#1a0a0a",
        "card_bg": "#2d1515",
        "text_primary": "#fef2f2",
        "text_secondary": "#fca5a5",
        "border": "rgba(239,68,68,0.25)",
        "glow": "239,68,68",
        "sidebar_bg": "linear-gradient(160deg, #1a0a0a 0%, #2d1515 100%)",
        "header_bg": "linear-gradient(90deg, #1a0a0a, #2d1515)",
        "card_grad": "linear-gradient(135deg, rgba(239,68,68,0.1), rgba(249,115,22,0.06))",
        "btn_grad": "linear-gradient(135deg, #ef4444, #dc2626)",
        "btn_hover": "linear-gradient(135deg, #f97316, #ea580c)",
        "logo_grad": "linear-gradient(135deg,#ef4444,#f97316)",
    },
    "💜 Royal Violet": {
        "primary": "#a855f7",
        "primary_dark": "#9333ea",
        "accent": "#e879f9",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#0d0a1a",
        "card_bg": "#1a1030",
        "text_primary": "#faf5ff",
        "text_secondary": "#e9d5ff",
        "border": "rgba(168,85,247,0.25)",
        "glow": "168,85,247",
        "sidebar_bg": "linear-gradient(160deg, #0d0a1a 0%, #1a1030 100%)",
        "header_bg": "linear-gradient(90deg, #0d0a1a, #1a1030)",
        "card_grad": "linear-gradient(135deg, rgba(168,85,247,0.1), rgba(232,121,249,0.06))",
        "btn_grad": "linear-gradient(135deg, #a855f7, #9333ea)",
        "btn_hover": "linear-gradient(135deg, #e879f9, #d946ef)",
        "logo_grad": "linear-gradient(135deg,#a855f7,#e879f9)",
    },
    "🌊 Ocean Cyan": {
        "primary": "#06b6d4",
        "primary_dark": "#0891b2",
        "accent": "#38bdf8",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "dark_bg": "#020e1a",
        "card_bg": "#0c1f30",
        "text_primary": "#ecfeff",
        "text_secondary": "#a5f3fc",
        "border": "rgba(6,182,212,0.25)",
        "glow": "6,182,212",
        "sidebar_bg": "linear-gradient(160deg, #020e1a 0%, #0c1f30 100%)",
        "header_bg": "linear-gradient(90deg, #020e1a, #0c1f30)",
        "card_grad": "linear-gradient(135deg, rgba(6,182,212,0.1), rgba(56,189,248,0.06))",
        "btn_grad": "linear-gradient(135deg, #06b6d4, #0891b2)",
        "btn_hover": "linear-gradient(135deg, #38bdf8, #06b6d4)",
        "logo_grad": "linear-gradient(135deg,#06b6d4,#38bdf8)",
    },
}

# ─── UTILITY FUNCTIONS ─────────────────────────────────────────
def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.strip().encode()).hexdigest()

def calc_dist(la1, lo1, la2, lo2):
    R = 6371
    d = math.pi / 180
    a = (math.sin((la2-la1)*d/2)**2 + math.cos(la1*d) * math.cos(la2*d) * math.sin((lo2-lo1)*d/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def calc_hrs(t_in, t_out):
    if not t_in or not t_out or t_out in ("Out Miss", "Corrected", "--", ""):
        return "--"
    try:
        a = list(map(int, t_in.split(":")))
        b = list(map(int, t_out.split(":")))
        diff = (b[0]*3600 + b[1]*60 + (b[2] if len(b)>2 else 0)) - (a[0]*3600 + a[1]*60 + (a[2] if len(a)>2 else 0))
        if diff < 0:
            return "--"
        return f"{diff//3600}h {(diff%3600)//60}m"
    except:
        return "--"

def calc_hrs_float(t_in, t_out):
    if not t_in or not t_out or t_out in ("Out Miss", "Corrected", "--", ""):
        return 0.0
    try:
        a = list(map(int, t_in.split(":")))
        b = list(map(int, t_out.split(":")))
        diff = (b[0]*3600 + b[1]*60) - (a[0]*3600 + a[1]*60)
        return max(diff / 3600, 0)
    except:
        return 0.0

def now_time():
    return datetime.now().strftime("%H:%M:%S")

def today_str():
    return date.today().isoformat()

def get_server_fp():
    if "fp_seed" not in st.session_state:
        import random
        st.session_state.fp_seed = str(random.randint(100000, 999999))
    raw = "streamlit_v6_" + st.session_state.fp_seed
    h = hashlib.sha256(raw.encode()).hexdigest().upper()
    return "FP" + h[:10]

def get_theme():
    t = st.session_state.get("theme_name", "🌌 Midnight Indigo")
    return THEMES.get(t, THEMES["🌌 Midnight Indigo"])

# ─── DATABASE ──────────────────────────────────────────────────
@st.cache_resource
def get_db_connection():
    """Single persistent connection (cached)"""
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def get_con():
    return get_db_connection()

def init_db():
    con = get_con()
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS employees (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL UNIQUE,
        dept       TEXT,
        desig      TEXT,
        pin_hash   TEXT NOT NULL,
        color      TEXT DEFAULT '#6366f1',
        active     INTEGER DEFAULT 1,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT NOT NULL,
        dept       TEXT,
        desig      TEXT,
        att_date   TEXT NOT NULL,
        in_time    TEXT,
        out_time   TEXT DEFAULT 'Out Miss',
        status     TEXT DEFAULT 'Out Miss',
        device_fp  TEXT,
        geo_ok     INTEGER DEFAULT 0,
        overtime_h REAL DEFAULT 0,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS devices (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        fp            TEXT NOT NULL,
        registered_at TEXT,
        UNIQUE(name, fp)
    );

    CREATE TABLE IF NOT EXISTS alerts (
        id     INTEGER PRIMARY KEY AUTOINCREMENT,
        level  TEXT,
        name   TEXT,
        type   TEXT,
        detail TEXT,
        fp     TEXT,
        seen   INTEGER DEFAULT 0,
        ts     TEXT
    );

    CREATE TABLE IF NOT EXISTS leave_requests (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT,
        req_date   TEXT,
        leave_type TEXT,
        reason     TEXT,
        status     TEXT DEFAULT 'Pending',
        ts         TEXT
    );

    CREATE TABLE IF NOT EXISTS login_fails (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT UNIQUE NOT NULL,
        count INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS gps_settings (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude   REAL,
        longitude  REAL,
        radius_km  REAL,
        updated_by TEXT,
        updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS admin_logs (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        admin   TEXT,
        action  TEXT,
        details TEXT,
        ts      TEXT
    );
    """)
    con.commit()
    _migrate_employees(cur, con)

def _migrate_employees(cur, con):
    """Migrate old hardcoded EMPS dict to DB (run once)"""
    LEGACY_EMPS = {
        "Saba":        {"dept": "WIP",                "desig": "Team Lead",          "pin": "1122", "col": "#00d4ff"},
        "Tahreem":     {"dept": "Cutting",            "desig": "Computer Operator",  "pin": "2233", "col": "#00e676"},
        "Zaheer":      {"dept": "Cutting",            "desig": "Computer Operator",  "pin": "3344", "col": "#ff5252"},
        "Hamza":       {"dept": "Sewing",             "desig": "Executive Office",   "pin": "4455", "col": "#ffaa00"},
        "Mujahid":     {"dept": "Washing",            "desig": "Supervisor",         "pin": "5566", "col": "#bf5af2"},
        "Irtiqa":      {"dept": "Washing",            "desig": "Computer Operator",  "pin": "6677", "col": "#40c4ff"},
        "Khushal":     {"dept": "Finishing & Packing","desig": "Supervisor",         "pin": "7788", "col": "#69f0ae"},
        "Abdul Haiey": {"dept": "Warehouse",          "desig": "Computer Operator",  "pin": "8899", "col": "#ff6e40"},
    }
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for name, data in LEGACY_EMPS.items():
        try:
            cur.execute(
                "INSERT OR IGNORE INTO employees(name,dept,desig,pin_hash,color,created_at) VALUES(?,?,?,?,?,?)",
                (name, data["dept"], data["desig"], hash_pin(data["pin"]), data["col"], ts)
            )
        except:
            pass
    con.commit()

# ─── EMPLOYEE DB FUNCTIONS ─────────────────────────────────────
def db_get_employees(active_only=True):
    con = get_con()
    if active_only:
        rows = con.execute("SELECT * FROM employees WHERE active=1 ORDER BY name").fetchall()
    else:
        rows = con.execute("SELECT * FROM employees ORDER BY name").fetchall()
    return [dict(r) for r in rows]

def db_get_employee(name):
    con = get_con()
    row = con.execute("SELECT * FROM employees WHERE name=?", (name,)).fetchone()
    return dict(row) if row else None

def db_add_employee(name, dept, desig, pin, color):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    con.execute(
        "INSERT INTO employees(name,dept,desig,pin_hash,color,created_at) VALUES(?,?,?,?,?,?)",
        (name.strip(), dept, desig, hash_pin(pin), color, ts)
    )
    con.commit()

def db_update_employee(old_name, name, dept, desig, pin, color, active):
    con = get_con()
    if pin:
        con.execute(
            "UPDATE employees SET name=?,dept=?,desig=?,pin_hash=?,color=?,active=? WHERE name=?",
            (name.strip(), dept, desig, hash_pin(pin), color, int(active), old_name)
        )
    else:
        con.execute(
            "UPDATE employees SET name=?,dept=?,desig=?,color=?,active=? WHERE name=?",
            (name.strip(), dept, desig, color, int(active), old_name)
        )
    con.commit()

def db_delete_employee(name):
    con = get_con()
    con.execute("UPDATE employees SET active=0 WHERE name=?", (name,))
    con.commit()

# ─── DEVICE FUNCTIONS ──────────────────────────────────────────
def db_get_device(name):
    con = get_con()
    row = con.execute("SELECT fp FROM devices WHERE name=?", (name,)).fetchone()
    return row["fp"] if row else None

def db_register_device(name, fp):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    try:
        con.execute("INSERT INTO devices(name,fp,registered_at) VALUES(?,?,?)", (name, fp, ts))
        con.commit()
    except sqlite3.IntegrityError:
        pass

def db_reset_device(name):
    con = get_con()
    con.execute("DELETE FROM devices WHERE name=?", (name,))
    con.commit()

# ─── ALERT FUNCTIONS ───────────────────────────────────────────
def db_log_alert(level, name, atype, detail, fp=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    con.execute("INSERT INTO alerts(level,name,type,detail,fp,ts) VALUES(?,?,?,?,?,?)",
                (level, name, atype, detail, fp, ts))
    con.commit()

def db_get_alerts(level=None):
    con = get_con()
    if level:
        rows = con.execute("SELECT * FROM alerts WHERE level=? ORDER BY ts DESC", (level,)).fetchall()
    else:
        rows = con.execute("SELECT * FROM alerts ORDER BY ts DESC LIMIT 300").fetchall()
    return [dict(r) for r in rows]

def db_clear_alerts(level=None):
    con = get_con()
    if level:
        con.execute("DELETE FROM alerts WHERE level=?", (level,))
    else:
        con.execute("DELETE FROM alerts")
    con.commit()

# ─── LOGIN FAIL FUNCTIONS ──────────────────────────────────────
def db_get_fails(name):
    con = get_con()
    row = con.execute("SELECT count FROM login_fails WHERE name=?", (name,)).fetchone()
    return row["count"] if row else 0

def db_set_fails(name, count):
    con = get_con()
    con.execute("INSERT OR REPLACE INTO login_fails(name,count) VALUES(?,?)", (name, count))
    con.commit()

# ─── ATTENDANCE FUNCTIONS ──────────────────────────────────────
def db_mark_in(name, in_time, fp, geo_ok):
    emp = db_get_employee(name) or {}
    today = date.today().isoformat()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    row = con.execute("SELECT id FROM attendance WHERE name=? AND att_date=?", (name, today)).fetchone()
    if not row:
        con.execute(
            "INSERT INTO attendance(name,dept,desig,att_date,in_time,out_time,status,device_fp,geo_ok,created_at) VALUES(?,?,?,?,?,'Out Miss','Out Miss',?,?,?)",
            (name, emp.get("dept"), emp.get("desig"), today, in_time, fp, int(geo_ok), ts)
        )
        con.commit()

def db_mark_out(name, out_time):
    today = date.today().isoformat()
    con = get_con()
    row = con.execute("SELECT in_time FROM attendance WHERE name=? AND att_date=?", (name, today)).fetchone()
    overtime = 0.0
    if row and row["in_time"]:
        total_h = calc_hrs_float(row["in_time"], out_time)
        overtime = max(total_h - OVERTIME_HOURS, 0)
    con.execute(
        "UPDATE attendance SET out_time=?, status='Present', overtime_h=? WHERE name=? AND att_date=?",
        (out_time, overtime, name, today)
    )
    con.commit()

def db_get_today(name):
    today = date.today().isoformat()
    con = get_con()
    row = con.execute("SELECT * FROM attendance WHERE name=? AND att_date=?", (name, today)).fetchone()
    return dict(row) if row else None

def db_get_history(name, page=0):
    con = get_con()
    offset = page * PAGE_SIZE
    rows = con.execute(
        "SELECT * FROM attendance WHERE name=? ORDER BY att_date DESC LIMIT ? OFFSET ?",
        (name, PAGE_SIZE, offset)
    ).fetchall()
    total = con.execute("SELECT COUNT(*) as c FROM attendance WHERE name=?", (name,)).fetchone()["c"]
    return [dict(r) for r in rows], total

def db_get_all_att(dept_filter=None, page=0):
    con = get_con()
    offset = page * PAGE_SIZE
    if dept_filter:
        rows = con.execute(
            "SELECT * FROM attendance WHERE dept=? ORDER BY att_date DESC LIMIT ? OFFSET ?",
            (dept_filter, PAGE_SIZE, offset)
        ).fetchall()
        total = con.execute("SELECT COUNT(*) as c FROM attendance WHERE dept=?", (dept_filter,)).fetchone()["c"]
    else:
        rows = con.execute(
            "SELECT * FROM attendance ORDER BY att_date DESC LIMIT ? OFFSET ?",
            (PAGE_SIZE, offset)
        ).fetchall()
        total = con.execute("SELECT COUNT(*) as c FROM attendance").fetchone()["c"]
    return [dict(r) for r in rows], total

def db_get_monthly_summary(name, year, month):
    con = get_con()
    prefix = f"{year}-{month:02d}"
    rows = con.execute(
        "SELECT * FROM attendance WHERE name=? AND att_date LIKE ? ORDER BY att_date",
        (name, f"{prefix}%")
    ).fetchall()
    return [dict(r) for r in rows]

def db_get_all_monthly_summary(year, month):
    con = get_con()
    prefix = f"{year}-{month:02d}"
    rows = con.execute(
        "SELECT * FROM attendance WHERE att_date LIKE ? ORDER BY name, att_date",
        (f"{prefix}%",)
    ).fetchall()
    return [dict(r) for r in rows]

# ─── LEAVE FUNCTIONS ───────────────────────────────────────────
def db_add_leave(name, req_date, leave_type, reason):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    con.execute("INSERT INTO leave_requests(name,req_date,leave_type,reason,ts) VALUES(?,?,?,?,?)",
                (name, req_date, leave_type, reason, ts))
    con.commit()

def db_get_leaves(name=None, status=None):
    con = get_con()
    q = "SELECT * FROM leave_requests WHERE 1=1"
    params = []
    if name:   q += " AND name=?";   params.append(name)
    if status: q += " AND status=?"; params.append(status)
    q += " ORDER BY ts DESC"
    rows = con.execute(q, params).fetchall()
    return [dict(r) for r in rows]

def db_update_leave(lid, status):
    con = get_con()
    con.execute("UPDATE leave_requests SET status=? WHERE id=?", (status, lid))
    if status == "Approved":
        row = con.execute("SELECT name, req_date, leave_type FROM leave_requests WHERE id=?", (lid,)).fetchone()
        if row:
            n, d, lt = row["name"], row["req_date"], row["leave_type"]
            emp = db_get_employee(n) or {}
            att_row = con.execute("SELECT id FROM attendance WHERE name=? AND att_date=?", (n, d)).fetchone()
            if att_row:
                if lt == "Out Miss Correction":
                    con.execute("UPDATE attendance SET out_time='Corrected', status='Present' WHERE name=? AND att_date=?", (n, d))
                else:
                    con.execute("UPDATE attendance SET status=? WHERE name=? AND att_date=?", (lt, n, d))
            else:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                con.execute(
                    "INSERT INTO attendance(name,dept,desig,att_date,status,created_at) VALUES(?,?,?,?,?,?)",
                    (n, emp.get("dept"), emp.get("desig"), d, lt, ts)
                )
    con.commit()

# ─── GPS FUNCTIONS ─────────────────────────────────────────────
def db_get_gps_settings():
    con = get_con()
    row = con.execute("SELECT latitude,longitude,radius_km FROM gps_settings ORDER BY id DESC LIMIT 1").fetchone()
    if row:
        return {"lat": row["latitude"], "lon": row["longitude"], "radius": row["radius_km"]}
    return {"lat": OFFICE_LAT, "lon": OFFICE_LON, "radius": OFFICE_KM}

def db_update_gps_settings(lat, lon, radius, admin_name):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    con.execute("INSERT INTO gps_settings(latitude,longitude,radius_km,updated_by,updated_at) VALUES(?,?,?,?,?)",
                (lat, lon, radius, admin_name, ts))
    con.execute("INSERT INTO admin_logs(admin,action,details,ts) VALUES(?,?,?,?)",
                (admin_name, "GPS_UPDATE", f"Lat:{lat} Lon:{lon} R:{radius}km", ts))
    con.commit()

def db_log_admin_action(admin, action, details):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = get_con()
    con.execute("INSERT INTO admin_logs(admin,action,details,ts) VALUES(?,?,?,?)",
                (admin, action, details, ts))
    con.commit()

def db_get_admin_logs():
    con = get_con()
    rows = con.execute("SELECT * FROM admin_logs ORDER BY ts DESC LIMIT 100").fetchall()
    return [dict(r) for r in rows]

# ─── THEME CSS ─────────────────────────────────────────────────
def inject_theme_css():
    t = get_theme()
    p = t["primary"]
    pd = t["primary_dark"]
    acc = t["accent"]
    bg = t["dark_bg"]
    cbg = t["card_bg"]
    tp = t["text_primary"]
    ts_ = t["text_secondary"]
    brd = t["border"]
    glow = t["glow"]
    cg = t["card_grad"]
    bg_grad = t["btn_grad"]
    bh = t["btn_hover"]
    lg = t["logo_grad"]
    sb = t["sidebar_bg"]
    hb = t["header_bg"]

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;700;900&display=swap');

    * {{ margin:0; padding:0; box-sizing:border-box; }}

    :root {{
        --p:    {p};
        --pd:   {pd};
        --acc:  {acc};
        --succ: {t['success']};
        --warn: {t['warning']};
        --dng:  {t['danger']};
        --bg:   {bg};
        --cbg:  {cbg};
        --tp:   {tp};
        --ts:   {ts_};
        --brd:  {brd};
        --glow: {glow};
    }}

    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
        background: {bg} !important;
        color: {tp} !important;
        font-family: 'Exo 2', 'Segoe UI', sans-serif !important;
        min-height: 100vh;
    }}

    ::-webkit-scrollbar {{ width:8px; }}
    ::-webkit-scrollbar-track {{ background: rgba({glow},0.05); border-radius:8px; }}
    ::-webkit-scrollbar-thumb {{ background: {bg_grad}; border-radius:8px; }}

    [data-testid="stSidebar"] {{
        background: {sb} !important;
        border-right: 1.5px solid {brd} !important;
    }}
    [data-testid="stSidebar"] * {{ color: {tp} !important; }}

    [data-testid="metric-container"] {{
        background: {cg} !important;
        border: 1.5px solid {brd} !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0 4px 24px rgba({glow},0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: sUp 0.5s ease-out;
    }}
    [data-testid="metric-container"]:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba({glow},0.2) !important;
    }}
    [data-testid="stMetricValue"] {{ color: {p} !important; font-size:2rem !important; font-weight:900 !important; font-family:'Rajdhani',sans-serif !important; }}
    [data-testid="stMetricLabel"] {{ color: {ts_} !important; font-size:0.72rem !important; text-transform:uppercase; letter-spacing:2px; font-weight:700; }}

    input, textarea, select, [data-baseweb="select"] {{
        background: rgba(0,0,0,0.3) !important;
        border: 1.5px solid {brd} !important;
        color: {tp} !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }}
    input:focus, textarea:focus {{
        border-color: {p} !important;
        box-shadow: 0 0 16px rgba({glow},0.35) !important;
    }}

    .stButton > button {{
        background: {bg_grad} !important;
        color: #fff !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 10px !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 11px !important;
        padding: 12px 24px !important;
        transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
        box-shadow: 0 4px 16px rgba({glow},0.3);
        font-family:'Rajdhani',sans-serif !important;
    }}
    .stButton > button:hover {{
        background: {bh} !important;
        box-shadow: 0 8px 32px rgba({glow},0.5) !important;
        transform: translateY(-3px);
    }}
    .stButton > button:active {{ transform: scale(0.97); }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(0,0,0,0.25) !important;
        border-radius: 12px !important;
        padding: 5px !important;
        border: 1.5px solid {brd} !important;
        gap: 4px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: {ts_} !important;
        border-radius: 9px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Rajdhani', sans-serif !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {cg} !important;
        color: {p} !important;
        border: 1.5px solid {brd} !important;
    }}

    [data-testid="stDataFrame"] {{
        border: 1.5px solid {brd} !important;
        border-radius: 10px !important;
    }}

    .ss-card {{
        background: {cg};
        border: 1.5px solid {brd};
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 14px;
        animation: sUp 0.5s ease-out;
    }}
    .ss-card:hover {{
        border-color: {p};
        box-shadow: 0 8px 32px rgba({glow},0.15);
        transition: all 0.3s ease;
    }}

    .ss-banner-ok   {{ background:rgba(16,185,129,0.1);border:1.5px solid rgba(16,185,129,0.35);color:#10b981;border-radius:10px;padding:13px 16px;font-size:13px;margin-bottom:12px;font-weight:600;animation:sDown 0.4s ease-out; }}
    .ss-banner-warn {{ background:rgba(239,68,68,0.1);border:1.5px solid rgba(239,68,68,0.35);color:#ef4444;border-radius:10px;padding:13px 16px;font-size:13px;margin-bottom:12px;font-weight:600;animation:sDown 0.4s ease-out,shake 0.5s ease 0.4s; }}
    .ss-banner-info {{ background:rgba({glow},0.1);border:1.5px solid {brd};color:{p};border-radius:10px;padding:13px 16px;font-size:13px;margin-bottom:12px;font-weight:600;animation:sDown 0.4s ease-out; }}

    .chip-green {{ background:rgba(16,185,129,0.15);color:#10b981;border:1.5px solid rgba(16,185,129,0.4);border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;display:inline-block; }}
    .chip-red   {{ background:rgba(239,68,68,0.15);color:#ef4444;border:1.5px solid rgba(239,68,68,0.4);border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;display:inline-block; }}
    .chip-amber {{ background:rgba(245,158,11,0.15);color:#f59e0b;border:1.5px solid rgba(245,158,11,0.4);border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;display:inline-block; }}
    .chip-blue  {{ background:rgba({glow},0.15);color:{p};border:1.5px solid {brd};border-radius:20px;padding:4px 12px;font-size:11px;font-weight:700;display:inline-block; }}

    .ss-alert-hi {{ background:rgba(239,68,68,0.1);border:1.5px solid rgba(239,68,68,0.3);border-radius:10px;padding:14px;margin-bottom:10px;animation:sDown 0.4s ease-out,pulseRed 2s ease-in-out 0.4s infinite; }}
    .ss-alert-md {{ background:rgba(245,158,11,0.1);border:1.5px solid rgba(245,158,11,0.3);border-radius:10px;padding:14px;margin-bottom:10px; }}
    .ss-alert-lo {{ background:rgba(16,185,129,0.1);border:1.5px solid rgba(16,185,129,0.3);border-radius:10px;padding:14px;margin-bottom:10px; }}

    .theme-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 14px;
        border-radius: 20px;
        border: 1.5px solid {brd};
        background: {cg};
        font-size: 12px;
        font-weight: 700;
        color: {p};
        cursor: pointer;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }}

    @keyframes sUp   {{ from{{opacity:0;transform:translateY(18px)}} to{{opacity:1;transform:translateY(0)}} }}
    @keyframes sDown {{ from{{opacity:0;transform:translateY(-18px)}} to{{opacity:1;transform:translateY(0)}} }}
    @keyframes pulseRed {{ 0%,100%{{box-shadow:0 0 12px rgba(239,68,68,0.2)}} 50%{{box-shadow:0 0 28px rgba(239,68,68,0.45)}} }}
    @keyframes shake {{ 0%,100%{{transform:translateX(0)}} 25%{{transform:translateX(-4px)}} 75%{{transform:translateX(4px)}} }}
    @keyframes glowPulse {{ 0%,100%{{text-shadow:0 0 8px rgba({glow},0.3)}} 50%{{text-shadow:0 0 18px rgba({glow},0.6)}} }}
    </style>
    """, unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in": False,
        "current_user": None,
        "admin_logged_in": False,
        "admin_name": None,
        "device_fp": None,
        "gps_lat": None,
        "gps_lon": None,
        "gps_ok": False,
        "gps_dist": None,
        "page": "attendance",
        "login_error": "",
        "theme_name": "🌌 Midnight Indigo",
        "hist_page": 0,
        "att_page": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ─── THEME SELECTOR ────────────────────────────────────────────
def render_theme_selector():
    t = get_theme()
    with st.expander("🎨 Choose Theme", expanded=False):
        cols = st.columns(len(THEMES))
        for i, (tname, tdata) in enumerate(THEMES.items()):
            with cols[i]:
                selected = "✓ " if st.session_state.theme_name == tname else ""
                if st.button(
                    f"{selected}{tname}",
                    key=f"theme_{i}",
                    use_container_width=True,
                    help=tname
                ):
                    st.session_state.theme_name = tname
                    st.rerun()

# ─── HEADER ────────────────────────────────────────────────────
def render_header():
    t = get_theme()
    hi_alerts = len(db_get_alerts("HIGH"))
    sec_status = f"🔴 {hi_alerts} ALERT{'S' if hi_alerts>1 else ''}" if hi_alerts > 0 else "🟢 SECURE"
    p = t["primary"]
    hb = t["header_bg"]
    lg = t["logo_grad"]
    glow = t["glow"]

    st.markdown(f"""
    <div style="background:{hb};border-bottom:1.5px solid {t['border']};
                padding:14px 22px;display:flex;align-items:center;
                justify-content:space-between;margin-bottom:18px;border-radius:14px;
                animation:sDown 0.5s ease-out">
        <div style="display:flex;align-items:center;gap:14px">
            <div style="width:42px;height:42px;border-radius:11px;
                        background:{lg};display:flex;align-items:center;
                        justify-content:center;font-size:13px;font-weight:900;color:#fff;
                        box-shadow:0 0 22px rgba({glow},0.45);font-family:'Rajdhani',sans-serif">SS</div>
            <div>
                <div style="font-size:15px;font-weight:900;color:{t['text_primary']};
                            letter-spacing:2px;font-family:'Rajdhani',sans-serif">SS TEAM PORTAL</div>
                <div style="font-size:9px;color:{t['text_secondary']};font-family:monospace;
                            margin-top:2px;letter-spacing:1px">🔐 ADVANCED SECURITY v6.0</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px">
            <div style="font-family:monospace;font-size:11px;
                        color:{'#ef4444' if hi_alerts else '#10b981'};
                        background:rgba({glow},0.08);padding:7px 14px;border-radius:20px;
                        border:1.5px solid {t['border']};font-weight:700;letter-spacing:1px">
                {sec_status}
            </div>
            <div style="font-family:monospace;font-size:11px;color:{p};
                        background:rgba({glow},0.08);padding:7px 14px;border-radius:20px;
                        border:1.5px solid {t['border']};font-weight:700">
                {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── GPS AUTO-DETECT JAVASCRIPT ────────────────────────────────
GPS_JS = """
<script>
function autoGPS() {
    if (!navigator.geolocation) {
        document.getElementById('gps_status').innerText = 'GPS not supported';
        return;
    }
    document.getElementById('gps_status').innerText = 'Detecting...';
    navigator.geolocation.getCurrentPosition(function(pos) {
        document.getElementById('gps_status').innerText =
            'Lat: ' + pos.coords.latitude.toFixed(6) + '  Lon: ' + pos.coords.longitude.toFixed(6);
        document.getElementById('auto_lat').value = pos.coords.latitude;
        document.getElementById('auto_lon').value = pos.coords.longitude;
    }, function(err) {
        document.getElementById('gps_status').innerText = 'GPS denied — enter manually';
    });
}
</script>
<div style="margin:10px 0">
    <button onclick="autoGPS()" style="background:linear-gradient(135deg,#10b981,#059669);
        color:#fff;border:none;padding:9px 18px;border-radius:9px;font-size:12px;
        font-weight:700;cursor:pointer;letter-spacing:1px;font-family:Rajdhani,sans-serif">
        📍 AUTO-DETECT GPS
    </button>
    <div id="gps_status" style="font-family:monospace;font-size:11px;color:#a7f3d0;
        margin-top:8px;padding:8px 12px;background:rgba(16,185,129,0.1);
        border-radius:8px;border:1px solid rgba(16,185,129,0.3)">
        GPS not detected yet
    </div>
</div>
<input type="hidden" id="auto_lat" value="">
<input type="hidden" id="auto_lon" value="">
"""

# ─── LOGIN PAGE ────────────────────────────────────────────────
def page_attendance():
    if not st.session_state.logged_in:
        render_login()
    else:
        render_dashboard()

def render_login():
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    t = get_theme()
    p = t["primary"]
    lg = t["logo_grad"]
    glow = t["glow"]

    with col2:
        render_theme_selector()
        st.markdown(f"""
        <div style="text-align:center;margin:24px 0 28px">
            <div style="width:58px;height:58px;border-radius:15px;
                        background:{lg};display:flex;align-items:center;
                        justify-content:center;font-size:22px;font-weight:900;color:#fff;
                        margin:0 auto 16px;box-shadow:0 0 30px rgba({glow},0.5);
                        font-family:'Rajdhani',sans-serif;animation:glowPulse 2s ease-in-out infinite">SS</div>
            <div style="font-size:20px;font-weight:900;color:{t['text_primary']};
                        letter-spacing:3px;font-family:'Rajdhani',sans-serif">SECURE LOGIN</div>
            <div style="font-size:10px;color:{t['text_secondary']};font-family:monospace;
                        margin-top:7px;letter-spacing:1.5px">🔐 DEVICE + PIN VERIFIED</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        dev_fp = get_server_fp()
        st.session_state.device_fp = dev_fp

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:rgba({glow},0.08);border-radius:12px;padding:16px;
                        text-align:center;border:1.5px solid {t['border']}">
                <div style="font-size:24px;margin-bottom:8px">📱</div>
                <div style="font-size:9px;font-family:monospace;color:{t['text_secondary']};
                            font-weight:700;letter-spacing:1px">DEVICE<br>FINGERPRINT</div>
                <div style="font-size:9px;font-weight:800;margin-top:7px;
                            font-family:monospace;color:#10b981">✓ READY</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:rgba({glow},0.08);border-radius:12px;padding:16px;
                        text-align:center;border:1.5px solid {t['border']}">
                <div style="font-size:24px;margin-bottom:8px">📍</div>
                <div style="font-size:9px;font-family:monospace;color:{t['text_secondary']};
                            font-weight:700;letter-spacing:1px">GPS<br>LOCATION</div>
                <div style="font-size:9px;font-weight:800;margin-top:7px;font-family:monospace;
                            color:{'#10b981' if st.session_state.gps_ok else '#f59e0b'}">
                    {'✓ VERIFIED' if st.session_state.gps_ok else '⏳ WAITING'}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        emps = db_get_employees(active_only=True)
        emp_names = ["-- Select Employee --"] + [e["name"] for e in emps]
        name = st.selectbox("👤 Employee", emp_names, key="login_name")
        pin  = st.text_input("🔑 PIN", type="password", max_chars=6, key="login_pin", placeholder="4-digit PIN")

        with st.expander("📍 GPS Location", expanded=False):
            st.components.v1.html(GPS_JS, height=110)
            gps_settings = db_get_gps_settings()
            gc1, gc2 = st.columns(2)
            with gc1:
                lat_in = st.number_input("Latitude", value=gps_settings["lat"], format="%.6f", key="inp_lat")
            with gc2:
                lon_in = st.number_input("Longitude", value=gps_settings["lon"], format="%.6f", key="inp_lon")
            if st.button("📍 Confirm Location", key="gps_btn", use_container_width=True):
                st.session_state.gps_lat  = lat_in
                st.session_state.gps_lon  = lon_in
                st.session_state.gps_ok   = True
                dist = calc_dist(lat_in, lon_in, gps_settings["lat"], gps_settings["lon"])
                st.session_state.gps_dist = dist
                st.success(f"✓ GPS confirmed — {dist:.1f} km from office")

        if st.session_state.login_error:
            st.markdown(f'<div class="ss-banner-warn">❌ {st.session_state.login_error}</div>', unsafe_allow_html=True)
            st.session_state.login_error = ""

        if st.button("🔐 VERIFY & ENTER", key="login_btn", use_container_width=True):
            do_login(name, pin, dev_fp)

        st.markdown(f"""
        <div style="font-size:9px;color:{t['text_secondary']};text-align:center;
                    margin-top:14px;font-family:monospace;line-height:1.9;letter-spacing:0.5px">
            Device locked to your account — PIN hashed with SHA-256<br>
            <span style="color:#ef4444">⚠ Unauthorized access triggers admin alerts</span>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def do_login(name, pin, fp):
    if name == "-- Select Employee --":
        st.session_state.login_error = "Please select an employee"
        return

    emp = db_get_employee(name)
    if not emp:
        st.session_state.login_error = "Employee not found"
        return

    if hash_pin(pin) != emp["pin_hash"]:
        fails = db_get_fails(name) + 1
        db_set_fails(name, fails)
        if fails >= 3:
            db_log_alert("HIGH", name, "BRUTE_FORCE", f"{fails} failed PIN attempts", fp)
            st.session_state.login_error = f"Too many attempts ({fails}). Admin alerted."
        else:
            st.session_state.login_error = f"Wrong PIN ({fails}/3 attempts)"
        return

    registered_fp = db_get_device(name)
    if registered_fp and registered_fp != fp:
        db_log_alert("HIGH", name, "DEVICE_MISMATCH", "Login from unregistered device", fp)
        st.session_state.login_error = "🚨 DEVICE MISMATCH — Admin alerted."
        return

    if not registered_fp:
        db_register_device(name, fp)
        db_log_alert("INFO", name, "NEW_DEVICE", "New device registered", fp)

    db_set_fails(name, 0)

    if st.session_state.gps_ok and st.session_state.gps_dist is not None:
        gps_settings = db_get_gps_settings()
        if st.session_state.gps_dist > gps_settings["radius"]:
            db_log_alert("HIGH", name, "GEO_VIOLATION",
                         f"Login from {st.session_state.gps_dist:.1f}km away", fp)

    # Shift time check
    now_h = datetime.now().hour
    if now_h < SHIFT_START - 2 or now_h > SHIFT_END + 2:
        db_log_alert("MED", name, "ODD_HOURS", f"Login at {now_time()} (outside shift)", fp)

    st.session_state.logged_in    = True
    st.session_state.current_user = name
    db_log_alert("INFO", name, "LOGIN", "Successful login", fp)
    st.rerun()

# ─── DASHBOARD ─────────────────────────────────────────────────
def render_dashboard():
    name = st.session_state.current_user
    emp  = db_get_employee(name) or {}
    fp   = st.session_state.device_fp or get_server_fp()
    t    = get_theme()
    p    = t["primary"]
    glow = t["glow"]

    hi_count = len([a for a in db_get_alerts("HIGH") if a["name"] == name])

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;padding:16px 18px;
                background:{t['card_grad']};border-radius:13px;
                border:1.5px solid {t['border']};margin-bottom:16px;animation:sDown 0.5s ease-out">
        <div style="width:50px;height:50px;border-radius:50%;display:flex;
                    align-items:center;justify-content:center;font-size:15px;
                    font-weight:900;color:{emp.get('color','#6366f1')};
                    border:2.5px solid {emp.get('color','#6366f1')};background:rgba(0,0,0,0.3);
                    box-shadow:0 0 18px {emp.get('color','#6366f1')}60;
                    font-family:'Rajdhani',sans-serif">
            {name[:2].upper()}
        </div>
        <div style="flex:1">
            <div style="font-size:15px;font-weight:900;color:{t['text_primary']};
                        font-family:'Rajdhani',sans-serif;letter-spacing:1px">{name}</div>
            <div style="font-size:11px;color:{t['text_secondary']};font-family:monospace;margin-top:2px">
                {emp.get('dept','—')} • {emp.get('desig','—')}</div>
        </div>
        <div style="font-size:9px;font-family:monospace;color:{p};
                    background:rgba({glow},0.1);padding:7px 12px;border-radius:9px;
                    border:1px solid {t['border']};font-weight:700">
            🔒 {fp[:12]}...
        </div>
    </div>
    """, unsafe_allow_html=True)

    if hi_count > 0:
        st.markdown(f'<div class="ss-banner-warn">⚠ {hi_count} security alert(s) on your account</div>', unsafe_allow_html=True)
    elif st.session_state.gps_ok and st.session_state.gps_dist:
        gps_settings = db_get_gps_settings()
        if st.session_state.gps_dist > gps_settings["radius"]:
            st.markdown(f'<div class="ss-banner-warn">📍 You are {st.session_state.gps_dist:.1f}km from office</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ss-banner-ok">✓ All security checks passed</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ss-banner-ok">✓ Device verified</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📸 SCAN", "📊 MONTHLY", "📝 LEAVE", "📋 HISTORY"])
    with tab1: render_scan_tab(name, fp)
    with tab2: render_monthly_tab(name)
    with tab3: render_leave_tab(name)
    with tab4: render_history_tab(name)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08)'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT", key="logout_btn", use_container_width=True):
        db_log_alert("INFO", name, "LOGOUT", "Session ended", fp)
        for k in ["logged_in","current_user","gps_ok","gps_dist","gps_lat","gps_lon","hist_page"]:
            if k in st.session_state:
                if k in ("logged_in","gps_ok"): st.session_state[k] = False
                elif k in ("gps_dist","gps_lat","gps_lon"): st.session_state[k] = None
                elif k in ("hist_page",): st.session_state[k] = 0
                else: st.session_state[k] = None
        st.rerun()

# ─── SCAN TAB ──────────────────────────────────────────────────
def render_scan_tab(name, fp):
    today = db_get_today(name)
    in_done  = today is not None
    out_done = today is not None and today["out_time"] not in ("Out Miss", None, "")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("IN TIME",  today["in_time"] if today else "--")
    c2.metric("OUT TIME", today["out_time"] if today and today["out_time"] != "Out Miss" else "--")
    c3.metric("HOURS",    calc_hrs(today["in_time"], today["out_time"]) if today else "--")

    overtime = 0.0
    if today and today.get("overtime_h"):
        overtime = today["overtime_h"]
    c4.metric("OVERTIME", f"{overtime:.1f}h" if overtime > 0 else "--")

    st.markdown("<br>", unsafe_allow_html=True)
    t = get_theme()
    glow = t["glow"]

    status_icon = "🟢" if (in_done and out_done) else ("🟡" if in_done else "⚪")
    status_msg  = "Both IN & OUT recorded" if (in_done and out_done) else ("IN marked — awaiting OUT" if in_done else "Ready to mark attendance")

    st.markdown(f"""
    <div style="background:{t['card_grad']};border:1.5px solid {t['border']};
                border-radius:14px;padding:28px;text-align:center;margin-bottom:20px">
        <div style="font-size:52px;margin-bottom:12px">{status_icon}</div>
        <div style="font-size:14px;font-weight:900;color:{t['text_primary']};
                    font-family:'Rajdhani',sans-serif;letter-spacing:1px">BIOMETRIC VERIFICATION</div>
        <div style="font-size:11px;color:{t['text_secondary']};font-family:monospace;margin-top:6px">{status_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    col_in, col_out = st.columns(2)
    with col_in:
        if st.button("▲ MARK IN", key="btn_in", disabled=in_done, use_container_width=True):
            gps_settings = db_get_gps_settings()
            if st.session_state.gps_ok and st.session_state.gps_dist and st.session_state.gps_dist > gps_settings["radius"]:
                db_log_alert("HIGH", name, "GPS_BLOCK_IN", f"Mark IN blocked ({st.session_state.gps_dist:.1f}km)", fp)
                st.error(f"🚫 Too far from office: {st.session_state.gps_dist:.1f}km")
            else:
                now_h = datetime.now().hour
                if now_h < SHIFT_START - 2:
                    st.warning(f"⚠ Marking IN {SHIFT_START - now_h}h before shift start")
                db_mark_in(name, now_time(), fp, st.session_state.gps_ok)
                st.success(f"✓ Welcome {name}! IN: {now_time()}")
                st.rerun()
    with col_out:
        if st.button("▼ MARK OUT", key="btn_out", disabled=(not in_done or out_done), use_container_width=True):
            t_out = now_time()
            db_mark_out(name, t_out)
            total_h = calc_hrs_float(today["in_time"], t_out) if today else 0
            ot_msg = f" | Overtime: {total_h - OVERTIME_HOURS:.1f}h" if total_h > OVERTIME_HOURS else ""
            st.success(f"✓ Goodbye {name}! OUT: {t_out}{ot_msg}")
            st.rerun()

# ─── MONTHLY TAB ───────────────────────────────────────────────
def render_monthly_tab(name):
    t = get_theme()
    p = t["primary"]
    glow = t["glow"]

    now = datetime.now()
    col_y, col_m = st.columns(2)
    with col_y:
        year = st.selectbox("Year", list(range(now.year - 2, now.year + 1))[::-1], index=0, key="emp_year")
    with col_m:
        month = st.selectbox("Month", list(range(1, 13)), index=now.month - 1,
                             format_func=lambda m: calendar.month_name[m], key="emp_month")

    recs = db_get_monthly_summary(name, year, month)
    leaves_app = db_get_leaves(name=name, status="Approved")

    total_days   = calendar.monthrange(year, month)[1]
    present      = [r for r in recs if r["status"] == "Present"]
    out_miss     = [r for r in recs if r["status"] == "Out Miss"]
    leave_month  = [l for l in leaves_app if l["req_date"].startswith(f"{year}-{month:02d}")]
    total_hours  = sum(calc_hrs_float(r["in_time"], r["out_time"]) for r in present)
    total_ot     = sum(r.get("overtime_h") or 0 for r in recs)
    avg_hours    = total_hours / len(present) if present else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("✅ Present",  len(present))
    c2.metric("⚠ Out Miss", len(out_miss))
    c3.metric("🏖 Leaves",  len(leave_month))
    c4.metric("⏱ Total Hrs", f"{total_hours:.1f}h")
    c5.metric("⚡ Overtime", f"{total_ot:.1f}h")

    st.markdown(f"""
    <div class="ss-card">
        <div style="font-size:13px;font-weight:700;color:{p};
                    font-family:'Rajdhani',sans-serif;letter-spacing:1px;margin-bottom:14px">
            📊 {calendar.month_name[month]} {year} — Attendance Summary
        </div>
    """, unsafe_allow_html=True)

    # Simple chart using columns
    if recs:
        daily_data = []
        for r in recs:
            h = calc_hrs_float(r["in_time"], r["out_time"])
            daily_data.append({"Date": r["att_date"][8:], "Hours": round(h, 1), "Status": r["status"]})

        if daily_data:
            df_chart = pd.DataFrame(daily_data).set_index("Date")
            st.bar_chart(df_chart["Hours"], height=180)

    st.markdown('</div>', unsafe_allow_html=True)

    # Status breakdown
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px">
        <div style="background:{t['card_grad']};border:1.5px solid {t['border']};
                    border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px;font-weight:900;color:{p};
                        font-family:'Rajdhani',sans-serif">{len(present)}/{total_days}</div>
            <div style="font-size:10px;color:{t['text_secondary']};margin-top:4px;letter-spacing:1px">ATTENDANCE RATE</div>
            <div style="font-size:11px;color:#10b981;font-weight:700;margin-top:6px">
                {(len(present)/total_days*100):.0f}%</div>
        </div>
        <div style="background:{t['card_grad']};border:1.5px solid {t['border']};
                    border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px;font-weight:900;color:{p};
                        font-family:'Rajdhani',sans-serif">{avg_hours:.1f}h</div>
            <div style="font-size:10px;color:{t['text_secondary']};margin-top:4px;letter-spacing:1px">AVG HOURS/DAY</div>
            <div style="font-size:11px;color:{'#f59e0b' if avg_hours < OVERTIME_HOURS else '#10b981'};font-weight:700;margin-top:6px">
                {'BELOW' if avg_hours < OVERTIME_HOURS else 'GOOD'} TARGET</div>
        </div>
        <div style="background:{t['card_grad']};border:1.5px solid {t['border']};
                    border-radius:10px;padding:14px;text-align:center">
            <div style="font-size:22px;font-weight:900;color:#f59e0b;
                        font-family:'Rajdhani',sans-serif">{total_ot:.1f}h</div>
            <div style="font-size:10px;color:{t['text_secondary']};margin-top:4px;letter-spacing:1px">OVERTIME TOTAL</div>
            <div style="font-size:11px;color:#f59e0b;font-weight:700;margin-top:6px">THIS MONTH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if recs:
        data = [{"Date": r["att_date"], "In": r["in_time"] or "--",
                 "Out": r["out_time"] if r["out_time"] != "Out Miss" else "—",
                 "Status": r["status"], "Hours": calc_hrs(r["in_time"], r["out_time"]),
                 "OT": f"{r.get('overtime_h') or 0:.1f}h"} for r in recs]
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    else:
        st.info(f"No records for {calendar.month_name[month]} {year}")

# ─── LEAVE TAB ─────────────────────────────────────────────────
def render_leave_tab(name):
    st.markdown('<div class="ss-card">', unsafe_allow_html=True)
    req_date   = st.date_input("📅 Leave Date", value=date.today())
    leave_type = st.selectbox("📋 Leave Type", LEAVE_TYPES)
    reason     = st.text_area("✍️ Reason", placeholder="Please explain your reason...")
    if st.button("📤 SUBMIT REQUEST", use_container_width=True):
        if not reason.strip():
            st.warning("Please enter a reason")
        else:
            db_add_leave(name, str(req_date), leave_type, reason.strip())
            st.success("✓ Leave request submitted!")
            st.rerun()
    my_leaves = db_get_leaves(name=name)
    if my_leaves:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**Recent Requests**")
        for r in my_leaves[:5]:
            badge = {"Pending":"🟡","Approved":"🟢","Rejected":"🔴"}.get(r["status"],"⚪")
            st.markdown(f"`{r['req_date']}` | {r['leave_type']} | {badge} {r['status']}")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── HISTORY TAB ───────────────────────────────────────────────
def render_history_tab(name):
    page = st.session_state.hist_page
    recs, total = db_get_history(name, page)
    total_pages = max((total - 1) // PAGE_SIZE, 0)

    leaves_app = db_get_leaves(name=name, status="Approved")
    all_recs, _ = db_get_history(name, 0)
    out_miss = len([r for r in all_recs if r["status"] == "Out Miss"])
    present  = len([r for r in all_recs if r["status"] == "Present"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PRESENT",  present)
    c2.metric("OUT MISS", out_miss)
    c3.metric("LEAVES",   len(leaves_app))
    c4.metric("TOTAL",    total)

    if recs:
        data = [{"Date": r["att_date"], "In": r["in_time"] or "--",
                 "Out": r["out_time"] if r["out_time"] != "Out Miss" else "—",
                 "Status": r["status"], "Hours": calc_hrs(r["in_time"], r["out_time"]),
                 "OT": f"{r.get('overtime_h') or 0:.1f}h"} for r in recs]
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.button("◀ Prev", disabled=(page == 0), key="hist_prev"):
                st.session_state.hist_page -= 1; st.rerun()
        with p2:
            st.markdown(f"<div style='text-align:center;font-size:12px;padding:10px'>Page {page+1} / {total_pages+1}</div>", unsafe_allow_html=True)
        with p3:
            if st.button("Next ▶", disabled=(page >= total_pages), key="hist_next"):
                st.session_state.hist_page += 1; st.rerun()

# ─── ADMIN PAGE ────────────────────────────────────────────────
def page_admin():
    if not st.session_state.admin_logged_in:
        render_admin_login()
    else:
        render_admin_panel()

def render_admin_login():
    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    t = get_theme()
    with col2:
        render_theme_selector()
        st.markdown("""
        <div style="text-align:center;margin-bottom:24px">
            <div style="width:58px;height:58px;border-radius:15px;
                        background:linear-gradient(135deg,#ef4444,#dc2626);
                        display:flex;align-items:center;justify-content:center;
                        font-size:24px;font-weight:900;color:#fff;margin:0 auto 14px;
                        box-shadow:0 0 30px rgba(239,68,68,0.5)">🛡</div>
            <div style="font-size:20px;font-weight:900;color:#f1f5f9;letter-spacing:3px;
                        font-family:'Rajdhani',sans-serif">ADMIN CONSOLE</div>
            <div style="font-size:10px;color:#ef4444;font-family:monospace;
                        margin-top:7px;letter-spacing:1.5px">🔐 RESTRICTED ACCESS</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        admin_id = st.text_input("👤 Admin ID", placeholder="admin")
        pwd = st.text_input("🔑 Password", type="password")
        if st.button("🔐 ENTER CONSOLE", use_container_width=True):
            if pwd == ADMIN_PASS and admin_id in ADMIN_PERMISSIONS:
                st.session_state.admin_logged_in = True
                st.session_state.admin_name = admin_id
                db_log_admin_action(admin_id, "LOGIN", "Admin panel accessed")
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
        st.markdown('</div>', unsafe_allow_html=True)

def render_admin_panel():
    t = get_theme()
    p = t["primary"]
    all_att, _ = db_get_all_att()
    today = today_str()
    td_att  = [r for r in all_att if r["att_date"] == today]
    hi_al   = len(db_get_alerts("HIGH"))
    pend_r  = len(db_get_leaves(status="Pending"))

    st.markdown(f"""
    <div style="margin-bottom:18px;animation:sDown 0.5s ease-out">
        <div style="font-size:18px;font-weight:900;color:{t['text_primary']};
                    letter-spacing:2px;font-family:'Rajdhani',sans-serif">ADMIN CONSOLE</div>
        <div style="font-size:10px;color:{t['text_secondary']};font-family:monospace;margin-top:4px">
            {datetime.now().strftime('%A, %B %d %Y | %H:%M:%S')} | Admin: {st.session_state.admin_name}</div>
    </div>
    """, unsafe_allow_html=True)

    render_theme_selector()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("✅ Present",  len([r for r in td_att if r["status"]=="Present"]))
    c2.metric("⚠ Out Miss", len([r for r in td_att if r["status"]=="Out Miss"]))
    c3.metric("🔴 Alerts",  hi_al)
    c4.metric("📋 Requests", pend_r)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🚨 ALERTS", "📊 REPORTS", "👥 EMPLOYEES", "📱 DEVICES", "📋 REQUESTS", "⚙️ SETTINGS"])
    with tab1: admin_alerts(db_get_alerts())
    with tab2: admin_reports()
    with tab3: admin_employees()
    with tab4: admin_devices()
    with tab5: admin_requests()
    with tab6: admin_settings()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08)'>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT", use_container_width=True):
        db_log_admin_action(st.session_state.admin_name, "LOGOUT", "Session ended")
        st.session_state.admin_logged_in = False
        st.session_state.admin_name = None
        st.rerun()

def admin_alerts(all_al):
    hi  = [a for a in all_al if a["level"] == "HIGH"]
    med = [a for a in all_al if a["level"] == "MED"]
    inf = [a for a in all_al if a["level"] == "INFO"]

    if not all_al:
        st.success("✓ No alerts. System is secure.")
        return

    col_cl1, col_cl2 = st.columns(2)
    with col_cl1:
        if st.button("🗑 Clear HIGH Alerts", key="clear_hi"):
            db_clear_alerts("HIGH")
            db_log_admin_action(st.session_state.admin_name, "ALERT_CLEAR", "Cleared HIGH alerts")
            st.rerun()
    with col_cl2:
        if st.button("🗑 Clear ALL Alerts", key="clear_all"):
            db_clear_alerts()
            db_log_admin_action(st.session_state.admin_name, "ALERT_CLEAR", "Cleared all alerts")
            st.rerun()

    if hi:
        st.markdown(f"#### 🔴 HIGH RISK ({len(hi)})")
        for a in hi:
            st.markdown(f"""
            <div class="ss-alert-hi">
                <strong style="color:#ef4444">{a['name']}</strong>
                <span style="font-size:11px;color:#fca5a5;margin-left:8px">{a['type']}</span>
                <div style="font-size:11px;color:#cbd5e1;margin-top:5px">{a['detail']}</div>
                <div style="font-size:10px;color:#94a3b8;margin-top:3px;font-family:monospace">{a['ts']}</div>
            </div>""", unsafe_allow_html=True)

    if med:
        st.markdown(f"#### 🟡 MEDIUM ({len(med)})")
        for a in med:
            st.markdown(f"<div class='ss-alert-md'><strong>{a['name']}</strong> | {a['type']} — {a['detail']}</div>", unsafe_allow_html=True)

    if inf:
        st.markdown(f"#### 🟢 INFO ({len(inf)})")
        data = [{"Time": a["ts"][:16], "Name": a["name"], "Type": a["type"], "Detail": a["detail"]} for a in inf[:25]]
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

def admin_reports():
    t = get_theme()
    st.markdown("#### 📊 Attendance Reports")

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        dept = st.selectbox("Department", DEPARTMENTS, key="rep_dept")
    with col_r2:
        now = datetime.now()
        rep_year = st.selectbox("Year", list(range(now.year - 2, now.year + 1))[::-1], key="rep_year")
    with col_r3:
        rep_month = st.selectbox("Month", list(range(1, 13)), index=now.month - 1,
                                 format_func=lambda m: calendar.month_name[m], key="rep_month")

    # Monthly summary for all employees
    monthly_recs = db_get_all_monthly_summary(rep_year, rep_month)
    if monthly_recs:
        emp_summary = {}
        for r in monthly_recs:
            n = r["name"]
            if n not in emp_summary:
                emp_summary[n] = {"name": n, "dept": r["dept"], "present": 0,
                                  "out_miss": 0, "total_hours": 0.0, "overtime": 0.0}
            if r["status"] == "Present":
                emp_summary[n]["present"] += 1
                emp_summary[n]["total_hours"] += calc_hrs_float(r["in_time"], r["out_time"])
            elif r["status"] == "Out Miss":
                emp_summary[n]["out_miss"] += 1
            emp_summary[n]["overtime"] += r.get("overtime_h") or 0

        summary_data = []
        for v in emp_summary.values():
            if not dept or v["dept"] == dept:
                summary_data.append({
                    "Name": v["name"], "Dept": v["dept"],
                    "Present": v["present"], "Out Miss": v["out_miss"],
                    "Total Hrs": f"{v['total_hours']:.1f}",
                    "Overtime": f"{v['overtime']:.1f}h",
                    "Avg/Day": f"{v['total_hours']/max(v['present'],1):.1f}h",
                })

        if summary_data:
            st.markdown(f"**{calendar.month_name[rep_month]} {rep_year} — Employee Summary**")
            df = pd.DataFrame(summary_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Chart
            chart_df = pd.DataFrame([(r["Name"], r["Present"]) for r in summary_data],
                                     columns=["Employee", "Days Present"])
            st.bar_chart(chart_df.set_index("Employee"), height=200)

            csv = df.to_csv(index=False).encode()
            st.download_button(f"⬇ Export {calendar.month_name[rep_month]} Report",
                               csv, f"report_{rep_year}_{rep_month:02d}.csv", "text/csv")
    else:
        st.info(f"No records for {calendar.month_name[rep_month]} {rep_year}")

    st.markdown("---")
    st.markdown("#### 📋 Full Attendance Log")
    page = st.session_state.att_page
    recs, total = db_get_all_att(dept if dept else None, page)
    total_pages = max((total - 1) // PAGE_SIZE, 0)

    if recs:
        data = [{"Name": r["name"], "Dept": r["dept"], "Date": r["att_date"],
                 "In": r["in_time"] or "--",
                 "Out": r["out_time"] if r["out_time"] != "Out Miss" else "—",
                 "Status": r["status"], "OT": f"{r.get('overtime_h') or 0:.1f}h"} for r in recs]
        df_full = pd.DataFrame(data)
        st.dataframe(df_full, use_container_width=True, hide_index=True)

        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.button("◀ Prev", key="att_prev", disabled=(page == 0)):
                st.session_state.att_page -= 1; st.rerun()
        with p2:
            st.markdown(f"<div style='text-align:center;font-size:12px;padding:10px'>Page {page+1} / {total_pages+1} ({total} records)</div>", unsafe_allow_html=True)
        with p3:
            if st.button("Next ▶", key="att_next", disabled=(page >= total_pages)):
                st.session_state.att_page += 1; st.rerun()

        csv_full = df_full.to_csv(index=False).encode()
        st.download_button("⬇ Export CSV", csv_full, f"attendance_{today_str()}.csv", "text/csv")

def admin_employees():
    """Full employee CRUD management"""
    t = get_theme()
    p = t["primary"]

    tab_list, tab_add = st.tabs(["👥 Employee List", "➕ Add Employee"])

    with tab_list:
        emps = db_get_employees(active_only=False)
        if not emps:
            st.info("No employees found")
            return

        for emp in emps:
            with st.expander(f"{'✅' if emp['active'] else '❌'} {emp['name']} — {emp['dept']}", expanded=False):
                c1, c2 = st.columns([3, 1])
                with c1:
                    new_name  = st.text_input("Name",  value=emp["name"],  key=f"en_{emp['id']}")
                    new_dept  = st.selectbox("Dept",   DEPARTMENTS[1:], index=max(0, DEPARTMENTS[1:].index(emp["dept"])) if emp["dept"] in DEPARTMENTS else 0, key=f"ed_{emp['id']}")
                    new_desig = st.selectbox("Designation", DESIGNATIONS, index=DESIGNATIONS.index(emp["desig"]) if emp["desig"] in DESIGNATIONS else 0, key=f"edes_{emp['id']}")
                    new_color = st.color_picker("Color", value=emp.get("color","#6366f1"), key=f"ec_{emp['id']}")
                    new_pin   = st.text_input("New PIN (leave blank to keep)", type="password", key=f"ep_{emp['id']}", max_chars=6)
                    new_active= st.checkbox("Active", value=bool(emp["active"]), key=f"ea_{emp['id']}")
                with c2:
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                    if st.button("💾 Save", key=f"esave_{emp['id']}", use_container_width=True):
                        db_update_employee(emp["name"], new_name, new_dept, new_desig, new_pin if new_pin else None, new_color, new_active)
                        db_log_admin_action(st.session_state.admin_name, "EMP_UPDATE", f"Updated {emp['name']}")
                        st.success(f"✓ {new_name} updated!")
                        st.rerun()
                    if st.button("🗑 Deactivate", key=f"edel_{emp['id']}", use_container_width=True):
                        db_delete_employee(emp["name"])
                        db_log_admin_action(st.session_state.admin_name, "EMP_DEACTIVATE", f"Deactivated {emp['name']}")
                        st.warning(f"Employee {emp['name']} deactivated")
                        st.rerun()

    with tab_add:
        st.markdown('<div class="ss-card">', unsafe_allow_html=True)
        a_name  = st.text_input("Full Name", key="add_name")
        a_dept  = st.selectbox("Department", DEPARTMENTS[1:], key="add_dept")
        a_desig = st.selectbox("Designation", DESIGNATIONS, key="add_desig")
        a_pin   = st.text_input("PIN (4-6 digits)", type="password", key="add_pin", max_chars=6)
        a_color = st.color_picker("Profile Color", value="#6366f1", key="add_color")

        if st.button("➕ ADD EMPLOYEE", use_container_width=True, key="add_emp_btn"):
            if not a_name.strip():
                st.warning("Enter employee name")
            elif not a_pin or len(a_pin) < 4:
                st.warning("PIN must be 4-6 digits")
            elif db_get_employee(a_name.strip()):
                st.error(f"Employee '{a_name}' already exists")
            else:
                db_add_employee(a_name.strip(), a_dept, a_desig, a_pin, a_color)
                db_log_admin_action(st.session_state.admin_name, "EMP_ADD", f"Added {a_name}")
                st.success(f"✓ {a_name} added successfully!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def admin_devices():
    emps = db_get_employees(active_only=True)
    for emp in emps:
        fp = db_get_device(emp["name"])
        c1, c2 = st.columns([4, 1])
        with c1:
            status = "<span class='chip-green'>✓ Registered</span>" if fp else "<span class='chip-red'>✗ No Device</span>"
            st.markdown(f"**{emp['name']}** | {emp['dept']} {status}", unsafe_allow_html=True)
            if fp:
                st.caption(f"FP: {fp}")
        with c2:
            if fp and st.button("Reset", key=f"reset_{emp['name']}"):
                db_reset_device(emp["name"])
                db_log_admin_action(st.session_state.admin_name, "DEVICE_RESET", f"Reset device: {emp['name']}")
                st.rerun()

def admin_requests():
    pend = db_get_leaves(status="Pending")
    if not pend:
        st.success("✓ No pending leave requests")
        return
    for r in pend:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{r['name']}** | `{r['req_date']}` | {r['leave_type']}")
            st.caption(r["reason"])
        with c2:
            if st.button("✅", key=f"app_{r['id']}"):
                db_update_leave(r["id"], "Approved")
                db_log_admin_action(st.session_state.admin_name, "LEAVE_APPROVE", f"Approved: {r['name']}")
                st.rerun()
            if st.button("❌", key=f"rej_{r['id']}"):
                db_update_leave(r["id"], "Rejected")
                db_log_admin_action(st.session_state.admin_name, "LEAVE_REJECT", f"Rejected: {r['name']}")
                st.rerun()

def admin_settings():
    admin_perms = ADMIN_PERMISSIONS.get(st.session_state.admin_name, {})
    t = get_theme()

    st.markdown("#### 📍 GPS / Geofence Settings")
    if not admin_perms.get("gps_control"):
        st.error("❌ No GPS control permission")
        return

    st.markdown('<div class="ss-banner-info">📍 Office location and attendance geofence radius.</div>', unsafe_allow_html=True)
    gps_settings = db_get_gps_settings()
    col1, col2, col3 = st.columns(3)
    with col1:
        new_lat = st.number_input("Latitude",    value=gps_settings["lat"],    format="%.6f", key="admin_lat")
    with col2:
        new_lon = st.number_input("Longitude",   value=gps_settings["lon"],    format="%.6f", key="admin_lon")
    with col3:
        new_rad = st.number_input("Radius (km)", value=gps_settings["radius"], min_value=0.1, key="admin_radius")
    if st.button("💾 Save GPS Settings", use_container_width=True):
        db_update_gps_settings(new_lat, new_lon, new_rad, st.session_state.admin_name)
        st.success(f"✓ GPS updated: {new_lat}, {new_lon} (radius: {new_rad}km)")

    st.markdown("---")
    st.markdown("#### ⚙️ Shift Settings")
    st.markdown('<div class="ss-banner-info">Shift hours are configured via .env file (SHIFT_START_HOUR, SHIFT_END_HOUR, OVERTIME_HOURS).</div>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Shift Start", f"{SHIFT_START}:00")
    sc2.metric("Shift End",   f"{SHIFT_END}:00")
    sc3.metric("OT Threshold", f"{OVERTIME_HOURS}h")

    st.markdown("---")
    st.markdown("#### 📋 Admin Action Log")
    logs = db_get_admin_logs()
    if logs:
        log_data = [{"Time": l["ts"][:16], "Admin": l["admin"], "Action": l["action"], "Details": l["details"]} for l in logs[:20]]
        st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True)

# ─── MAIN ──────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="SS Team Portal v6.0",
        page_icon="🏭",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    init_db()
    init_session()
    inject_theme_css()
    render_header()

    with st.sidebar:
        st.markdown("### 🏭 SS TEAM PORTAL")
        st.markdown(f"**v6.0** — {st.session_state.theme_name}")
        st.markdown("---")
        if st.button("👤 Attendance", use_container_width=True):
            st.session_state.page = "attendance"; st.rerun()
        if st.button("🛡 Admin", use_container_width=True):
            st.session_state.page = "admin"; st.rerun()
        st.markdown("---")
        st.markdown("**Theme**")
        for tname in THEMES:
            if st.button(tname, use_container_width=True, key=f"sb_theme_{tname}"):
                st.session_state.theme_name = tname; st.rerun()

    n1, n2 = st.columns(2)
    with n1:
        if st.button("👤 ATTENDANCE", use_container_width=True,
                     type="primary" if st.session_state.page == "attendance" else "secondary"):
            st.session_state.page = "attendance"; st.rerun()
    with n2:
        if st.button("🛡 ADMIN", use_container_width=True,
                     type="primary" if st.session_state.page == "admin" else "secondary"):
            st.session_state.page = "admin"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.page == "attendance":
        page_attendance()
    else:
        page_admin()

if __name__ == "__main__":
    main()