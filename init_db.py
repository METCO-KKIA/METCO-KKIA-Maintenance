import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('data.db')
c = conn.cursor()

# ✅ 1. جدول تخزين السجلات المعدلة (PM و Asset)
c.execute('''
CREATE TABLE IF NOT EXISTS maintenance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    sheet_name TEXT,
    row_index INTEGER,
    data TEXT,
    timestamp TEXT,
    before_images TEXT,
    after_images TEXT,
    report_images TEXT,
    cm_images TEXT,
    notes_text TEXT,
    notes_images TEXT
)
''')

# ✅ 2. جدول ملفات ZIP + تاريخ الإنشاء
c.execute('''
CREATE TABLE IF NOT EXISTS zip_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    created_at TEXT
)
''')

# ✅ 3. ملفات Excel للبحث (PM و Asset)
c.execute('''
CREATE TABLE IF NOT EXISTS pm_excel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    upload_date TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS asset_excel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    upload_date TEXT
)
''')

# ✅ 4. ملف Excel موحد (صيانه.xlsx، CM TKT، PM TKT)
c.execute('''
CREATE TABLE IF NOT EXISTS maintenance_excel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    updated_at TEXT
)
''')

# ✅ 5. جدول Excel اليومي (اختياري)
c.execute('''
CREATE TABLE IF NOT EXISTS daily_excel_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    updated_at TEXT
)
''')

# ✅ 5.1 جدول uploaded_excels لحفظ ملفات Excel المرفوعة
c.execute('''
CREATE TABLE IF NOT EXISTS uploaded_excels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    filename TEXT,
    data BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


# ✅ 6. جدول المستخدمين مع كل الصلاحيات الحديثة
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    company TEXT,
    facility TEXT,
    last_login TEXT,
    last_modified TEXT,
    is_active INTEGER DEFAULT 1,
    can_upload_pm INTEGER DEFAULT 0,
    can_upload_asset INTEGER DEFAULT 0,
    can_delete_excel INTEGER DEFAULT 0,
    can_generate_reports INTEGER DEFAULT 0,
    can_edit_records INTEGER DEFAULT 0,
    can_view_zip INTEGER DEFAULT 0,
    can_add_users INTEGER DEFAULT 0
)
''')

# ✅ 7. جدول صلاحيات إضافية مرنة لكل مستخدم
c.execute('''
CREATE TABLE IF NOT EXISTS user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    permission TEXT
)
''')

# ✅ 8. جدول تسجيل الأنشطة
c.execute('''
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    timestamp TEXT
)
''')

# ✅ 9. جدول تخزين ملف Google credentials.json
c.execute('''
CREATE TABLE IF NOT EXISTS credentials_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    content BLOB,
    uploaded_at TEXT
)
''')

# ✅ 10. إنشاء المستخدم الافتراضي Ar إذا لم يكن موجودًا
c.execute("SELECT id FROM users WHERE username = 'Ar'")
if not c.fetchone():
    hashed_pw = generate_password_hash("ArP@$$w0rd2531")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO users (
            first_name, last_name, email, username, password, role, company, facility,
            last_login, last_modified, is_active,
            can_upload_pm, can_upload_asset, can_delete_excel,
            can_generate_reports, can_edit_records, can_view_zip, can_add_users
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'Default', 'Admin', 'admin@metco.local', 'Ar', hashed_pw, 'admin',
        'METCO', 'HQ', now, now, 1,
        1, 1, 1, 1, 1, 1, 1
    ))

    user_id = c.lastrowid
    full_permissions = [
        'upload_pm', 'upload_asset', 'delete_excel', 'generate_reports',
        'view_edit', 'view_edit_asset', 'view_dashboard', 'can_add_users'
    ]
    for perm in full_permissions:
        c.execute("INSERT INTO user_permissions (user_id, permission) VALUES (?, ?)", (user_id, perm))

    print("✅ تم إنشاء المستخدم Ar بكامل الصلاحيات.")

# ✅ 10. إنشاء المستخدم الافتراضي Ar إذا لم يكن موجودًا
# ... (كما هو)

# ✅ 11. جدول رسائل الشات
c.execute('''
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# ✅ Commit وإنهاء الاتصال
conn.commit()
conn.close()
print("✅ تم إنشاء قاعدة البيانات data.db بكل الجداول والتعديلات بنجاح.")
