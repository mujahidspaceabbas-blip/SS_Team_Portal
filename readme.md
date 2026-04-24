# 🏭 SS TEAM PORTAL v5.0

![Version](https://img.shields.io/badge/version-5.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.0%2B-red)

Advanced Employee Attendance Management System with Biometric Security, GPS Verification, and Admin Controls.

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Admin Guide](#admin-guide)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Version History](#version-history)

---

## ✨ Features

### 🔐 Security Features
- **Device Fingerprinting** - Unique device identification
- **PIN Authentication** - 4-digit secure PIN login
- **GPS Verification** - Location-based access control
- **Brute Force Protection** - Auto-lockout after 3 failed attempts
- **Audit Logging** - Complete action tracking

### 📊 Attendance Management
- **IN/OUT Marking** - Biometric-verified clock in/out
- **Work Duration Calculation** - Automatic hour tracking
- **Attendance Reports** - Department-wise analytics
- **Leave Management** - Request and approval system

### 🎨 Modern UI
- **Glassmorphism Design** - Modern frosted glass effect
- **Smooth Animations** - 0.3-0.6s transitions
- **Dark Theme** - Easy on the eyes
- **Responsive Layout** - Works on all devices

### 👨‍💼 Admin Dashboard
- **Real-time Alerts** - High/Medium/Low priority system
- **Device Management** - Register and reset devices
- **GPS Controls** - Authorized admin-only geofence setting
- **Leave Approvals** - Streamlined request processing
- **Audit Trail** - Complete admin action history

### 🔧 System Features
- **SQLite Database** - Embedded, no external DB needed
- **Auto-migration** - Database schema updates automatically
- **Environment Config** - Secure .env configuration
- **Role-based Access** - Permission-based admin controls

---

## 🚀 Quick Start

### Minimum Requirements
- Python 3.8+
- pip or conda
- 100MB disk space

### One-Command Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/ss-team-portal.git
cd ss-team-portal

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your settings
nano .env

# 4. Install & run
pip install streamlit pandas python-dotenv
streamlit run ss_team_portal_v5.py
```

Access at: **http://localhost:8501**

---

## 📦 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/ss-team-portal.git
cd ss-team-portal
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install streamlit pandas python-dotenv
```

### Step 4: Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

### Step 5: Run Application
```bash
streamlit run ss_team_portal_v5.py
```

---

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in the project root:

```env
# Office Location
OFFICE_LAT=30.124458
OFFICE_LON=71.386285
OFFICE_KM=96

# Admin Authentication
ADMIN_PASS=YourStrongPassword123!

# Database
DB_PATH=ss_portal.db
```

### Admin Permissions

Edit `ADMIN_PERMISSIONS` in the code:

```python
ADMIN_PERMISSIONS = {
    "admin": {
        "gps_control": True,      # Can modify GPS settings
        "device_reset": True,     # Can reset devices
        "alerts": True            # Can manage alerts
    }
}
```

### Employee Data

Modify `EMPS` dictionary for your employees:

```python
EMPS = {
    "John Doe": {
        "dept": "Engineering",
        "desig": "Manager",
        "pin": "1234",
        "col": "#6366f1"
    }
}
```

---

## 👥 Usage

### Employee Workflow

#### 1. Login
- Select name from dropdown
- Enter 4-digit PIN
- (Optional) Set GPS location
- Click "VERIFY & ENTER"

#### 2. Mark Attendance
- **IN**: Click "▲ MARK IN" button
- **OUT**: Click "▼ MARK OUT" button
- System auto-calculates work hours

#### 3. Request Leave
- Go to "📝 LEAVE" tab
- Select date and leave type
- Add reason
- Submit request
- Admin approves/rejects

#### 4. View History
- Check "📊 HISTORY" tab
- See all past attendance records
- Export as CSV if needed

### Employee Credentials

Default test users:
```
Employee: Saba        | PIN: 1122
Employee: Tahreem     | PIN: 2233
Employee: Zaheer      | PIN: 3344
Employee: Hamza       | PIN: 4455
Employee: Mujahid     | PIN: 5566
Employee: Irtiqa      | PIN: 6677
Employee: Khushal     | PIN: 7788
Employee: Abdul Haiey | PIN: 8899
```

---

## 🛡️ Admin Guide

### Admin Login

1. Click "🛡 ADMIN" button
2. Enter admin username (e.g., "admin")
3. Enter admin password
4. Click "🔐 ENTER"

### Admin Credentials
- Username: `admin`
- Password: Check `.env` file (ADMIN_PASS)

### Admin Features

#### 🚨 Alerts Tab
- View HIGH, MEDIUM, and INFO alerts
- Click "Clear All HIGH" to dismiss
- See full details of security incidents

#### 📊 Reports Tab
- Filter by department
- View attendance records
- Export as CSV for further analysis

#### 📱 Devices Tab
- See registered device fingerprints
- Reset unauthorized devices
- Track device security status

#### 📋 Requests Tab
- Approve/Reject leave requests
- One-click approval/rejection
- Automatic status updates

#### ⚙️ Settings Tab (GPS Control)
- Change office GPS coordinates
- Modify geofence radius (km)
- View change history/audit log
- Only authorized admins can access

---

## 🔒 Security

### Best Practices

✅ **DO:**
- Keep `.env` file secure (never commit to Git)
- Use strong passwords (12+ characters)
- Enable branch protection on GitHub
- Regularly review audit logs
- Backup database files
- Use HTTPS in production
- Rotate admin credentials periodically

❌ **DON'T:**
- Hardcode secrets in source code
- Share `.env` files via email/chat
- Use weak passwords
- Commit database files
- Run in HTTP mode on internet
- Disable authentication
- Ignore security alerts

### Security Features

1. **Device Fingerprinting**
   - Unique device ID generation
   - Prevents device spoofing
   - Auto-flags unauthorized devices

2. **Brute Force Protection**
   - Max 3 failed login attempts
   - Admin alert on lockout
   - Automatic cooldown

3. **GPS Verification**
   - Location-based access control
   - Configurable geofence radius
   - Prevents remote login abuse

4. **Audit Trail**
   - All admin actions logged
   - Timestamp on every event
   - Complete action history

---

## 🐛 Troubleshooting

### Installation Issues

**Q: "ModuleNotFoundError: No module named 'streamlit'"**
```bash
pip install streamlit pandas python-dotenv
```

**Q: "dotenv module not found"**
```bash
pip install python-dotenv
```

### Runtime Issues

**Q: "ADMIN_PASS not reading from .env"**
- Ensure `.env` file exists in project root
- Check `load_dotenv()` is called
- Verify syntax: `ADMIN_PASS=value` (no quotes needed)

**Q: "GPS not updating"**
- Check admin has `gps_control` permission
- Verify values in .env exist
- Restart application after changes

**Q: "Database is locked"**
- Close all instances
- Delete `ss_portal.db`
- Restart application (recreates DB)

**Q: "Can't access admin panel"**
- Verify username is in `ADMIN_PERMISSIONS`
- Check password matches `.env` ADMIN_PASS
- Clear browser cache and try again

### Performance Issues

**Q: "App is loading slowly"**
- Check database file size (`ls -lh ss_portal.db`)
- Consider archiving old records
- Check system resources (CPU, RAM)

**Q: "Animations are stuttering"**
- Update Streamlit: `pip install --upgrade streamlit`
- Use modern browser (Chrome/Firefox)
- Close other applications

---

## 📊 Database Schema

### Tables Created

**attendance** - Daily attendance records
```
id, name, dept, desig, att_date, in_time, out_time, 
status, device_fp, geo_ok, created_at
```

**devices** - Registered device fingerprints
```
id, name, fp, registered_at
```

**alerts** - Security alerts and notifications
```
id, level, name, type, detail, fp, seen, ts
```

**leave_requests** - Leave applications
```
id, name, req_date, leave_type, reason, status, ts
```

**gps_settings** - Office location and geofence
```
id, latitude, longitude, radius_km, updated_by, updated_at
```

**admin_logs** - Admin action audit trail
```
id, admin, action, details, ts
```

---

## 🔄 Version History

### v5.0 (Latest)
- ✅ Smooth transition animations (0.3-0.6s)
- ✅ Modern color palette (Indigo + Pink)
- ✅ Admin GPS control with permissions
- ✅ Environment variables (.env) support
- ✅ Audit logging system
- ✅ Role-based access control

### v4.0
- Glassmorphism UI design
- Device fingerprinting
- GPS verification system
- Initial feature set

---

## 📝 License

MIT License - Free to use and modify

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 💬 Support

### Getting Help
- Check [Troubleshooting](#troubleshooting) section
- Review [CHANGELOG.md](CHANGELOG.md) for updates
- Open GitHub issue with detailed description

### Report Issues
Include:
- Streamlit version (`streamlit --version`)
- Python version (`python --version`)
- Steps to reproduce
- Expected vs actual behavior

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Python SQLite Guide](https://docs.python.org/3/library/sqlite3.html)
- [CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/animation)

---

## 📞 Contact

For enterprise support or custom development:
- Email: support@example.com
- Website: www.example.com

---

**Made with ❤️ for efficient SS team management**