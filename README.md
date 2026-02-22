# 🎓 Student Result & Performance Management System

A full-featured **Django** web application for managing student results and analyzing academic performance — with role-based dashboards for **Admin**, **Faculty**, and **Students**.

Built with **Django 6**, **Bootstrap 5**, and **Chart.js**.

---

## ✨ Features

| Role | Features |
|---|---|
| **Admin** | Upload CSV results, manual entry, view all students, performance analytics with charts |
| **Faculty** | View assigned subjects, class performance charts, class topper display |
| **Student** | View subject-wise marks, grade card, performance charts, pass/fail status |

### 📊 Analytics
- Bar charts for subject-wise averages
- Doughnut chart for pass/fail ratio
- Per-student radar/bar performance charts
- Top 5 & bottom 5 student tables

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/rohankumarrawat/student-result-management.git
cd student-result-management
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django djangorestframework django-crispy-forms crispy-bootstrap5 django-import-export pandas
```

### 4. Apply Migrations

```bash
python manage.py makemigrations student_management
python manage.py migrate
```

### 5. Create Test Users

```bash
python manage.py shell < create_users.py
```

This creates the following default accounts:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Faculty | `faculty1` | `faculty123` |
| Student | `student1` | `student123` |

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📁 Project Structure

```
student-result-management/
├── student_result/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── student_management/      # Main Django app
│   ├── models.py            # User, StudentProfile, Subject, Result
│   ├── views.py             # All view logic
│   ├── urls.py              # URL routing
│   ├── forms.py             # Result entry form
│   └── templates/
│       ├── base.html        # Base layout (Bootstrap 5 sidebar)
│       ├── login.html       # Login page
│       ├── admin/           # Admin templates
│       │   ├── dashboard.html
│       │   ├── upload_csv.html
│       │   ├── manual_entry.html
│       │   └── performance.html
│       ├── student/
│       │   └── dashboard.html
│       └── faculty/
│           └── dashboard.html
├── static/                  # Static assets
├── create_users.py          # Script to seed test users
├── .gitignore
└── README.md
```

---

## 📋 CSV Upload Format

When uploading results via CSV, use this column structure:

```
roll_number, student_name, subject_code, subject_name, marks
101, Student One, CS101, Computer Science, 85
```

---

## 🗃️ Database Models

- **User** — Custom user model with `role` field (`admin`, `faculty`, `student`)
- **StudentProfile** — Links student user to a `roll_number`
- **Subject** — Subject with `name`, `code`, and `faculty` (FK to User)
- **Result** — Links `StudentProfile` + `Subject` + `marks`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6 + Python 3 |
| Frontend | Bootstrap 5 (CDN) + Bootstrap Icons |
| Charts | Chart.js (CDN) |
| Database | SQLite (dev) |
| Data Processing | Pandas |

---

## 🔐 URL Routes

| URL | View | Access |
|---|---|---|
| `/` | Redirect by role | All |
| `/login/` | Login page | Public |
| `/logout/` | Logout | Authenticated |
| `/admin-dashboard/` | Admin home | Admin |
| `/admin-dashboard/upload-csv/` | Upload CSV | Admin |
| `/admin-dashboard/manual-entry/` | Manual entry | Admin |
| `/admin-dashboard/performance/` | Analytics | Admin |
| `/faculty-dashboard/` | Faculty home | Faculty |
| `/student-dashboard/` | Student home | Student |

---

## 📸 Screenshots

> Login → Admin Dashboard → Performance Analytics → Student Grade Card → Faculty Class View

---

## 📦 Deployment Notes

For production:
1. Set `DEBUG = False` in `settings.py`
2. Set `ALLOWED_HOSTS` to your domain
3. Use `python manage.py collectstatic`
4. Switch to PostgreSQL for the database
5. Use Gunicorn + Nginx for serving

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License — feel free to use this for your college projects!

---

*Built with ❤️ using Django & Bootstrap 5*
