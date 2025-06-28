# 🎓 Student Leave Management System

A comprehensive Django web application for managing student leave requests in educational institutions. This system supports both undergraduate and postgraduate programs with role-based access control for students, teachers, and administrators.

## ✨ Features

### 👨‍🎓 **Student Features**
- Apply for leave requests with date ranges and detailed reasons
- Single-day and multi-day leave applications
- View leave history with pagination (6 entries per page)
- Update profile information and upload profile pictures
- Real-time status tracking of leave applications
- User-friendly dashboard with leave summaries

### 👨‍🏫 **Teacher Features**
- Review and approve/reject pending leave requests
- Add review messages for students
- View leave summaries for all students in their class
- Access to past leave request history
- Paginated request management (5 requests per page)
- Dashboard with student leave statistics

### 👨‍💼 **Admin Features**
- Full Django admin interface
- Manage users, classes, and leave requests
- System-wide oversight and control
- User role management (Student/Teacher/Admin)

## 🏗️ Technology Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Authentication**: Custom User Model with role-based permissions
- **File Handling**: Pillow for image processing
- **Additional Libraries**: django-widget-tweaks, crispy-bootstrap5

## 📊 Database Models

### Class Model
- Supports UG (1st-3rd year) and PG (1st-2nd year) programs
- Multiple course offerings including:
  - **UG Courses**: BCA-AI, BBA-AV, B.Com (Co-operation & Finance), B.Sc (Electronics, Biotechnology), B.A English, BSW
  - **PG Courses**: M.Sc CS, MA HRM, M.Com Finance, M.Sc Electronics, M.Sc Biotechnology, MA English
- Batch system (A/B batches)
- Validation for course-level compatibility
- Smart validation preventing UG courses in PG programs and vice versa

### CustomUser Model
- Extends Django's AbstractUser
- Role-based permissions (Student/Teacher/Admin)
- Profile pictures and contact information
- Class association for students
- Phone number field for contact details

### LeaveRequest Model
- Date range management (from_date to to_date)
- Status tracking (Pending/Approved/Rejected)
- Review messages and audit trail
- Teacher approval workflow
- Automatic timestamp for application date
- Single-day leave support

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Alw04j/student_leave_system.git
   cd student_leave_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 🎯 Usage Guide

### For Students
1. **Login**: Access student login at `/login/student/`
2. **Dashboard**: View leave history and status
3. **Apply Leave**: Navigate to "Apply Leave" to submit new requests
   - Choose single-day or multi-day leave
   - Select dates (cannot be in the past)
   - Provide detailed reason
4. **Profile**: Update personal information and profile picture

### For Teachers
1. **Login**: Access teacher login at `/login/teacher/`
2. **Dashboard**: View student leave summaries
3. **Manage Requests**: Review pending applications at `/leave-requests/`
   - Approve/reject with review messages
   - View student details and leave history
4. **Past Requests**: Access reviewed applications at `/past-requests/`

### For Administrators
1. **Admin Panel**: Access Django admin at `/admin/`
2. **User Management**: Create and manage users
3. **Class Management**: Set up academic classes and batches
4. **System Monitoring**: Oversee all leave activities

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The system uses SQLite by default for development. For production, configure MySQL or PostgreSQL in `settings.py`.

### Static and Media Files
- Static files are served from `/static/`
- Media files (profile pictures) are stored in `/media/profiles/`
- Use `python manage.py collectstatic` for production

## 🔒 Security Features

- **CSRF Protection**: Enabled for all forms
- **Role-Based Access Control**: Students, Teachers, and Admins
- **Secure Password Validation**: Django's built-in validators
- **Session Management**: Configurable session timeouts
- **File Upload Validation**: Image files only for profiles
- **Access Denied Pages**: Proper error handling for unauthorized access

## 🎨 User Interface Features

- **Responsive Design**: Bootstrap 5 for mobile-friendly interface
- **Clean Templates**: Well-organized template structure
- **Form Validation**: Client and server-side validation
- **Pagination**: Optimized performance for large datasets
- **Profile Management**: Image upload and user details
- **Modern UI**: Professional appearance with Bootstrap components

## 🚀 Deployment

### PythonAnywhere (Recommended for Students)
1. Create account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload project files via Git or file upload
3. Configure virtual environment
4. Set up MySQL database
5. Configure WSGI file
6. Deploy and access via custom subdomain

### Other Hosting Options
- **Railway**: Easy deployment with Git integration
- **Render**: Free tier available
- **Heroku**: Classic Django hosting platform
- **DigitalOcean**: VPS hosting for advanced users

## 📁 Project Structure

```
student_leave_system/
├── core/                     # Main Django application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic and views
│   ├── forms.py             # Form definitions and validation
│   ├── admin.py             # Django admin configuration
│   ├── urls.py              # URL routing
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── dashboard_student.html
│   ├── dashboard_teacher.html
│   ├── apply_leave.html
│   ├── manage_requests.html
│   └── ...                 # Other templates
├── media/                   # User uploads (profile pictures)
├── leave_mgmt/             # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## 🔄 Key Workflows

### Leave Application Process
1. Student logs in and navigates to "Apply Leave"
2. Fills leave application form with dates and reason
3. System validates dates (no past dates, logical date ranges)
4. Leave request is saved with "pending" status
5. Teacher receives notification in their dashboard
6. Teacher reviews and approves/rejects with message
7. Student can view updated status in their dashboard

### User Management
1. Admin creates users through Django admin
2. Users are assigned roles (Student/Teacher)
3. Students are assigned to specific classes
4. Teachers are associated with classes for leave management
5. Users can update their profiles and contact information

## 🎓 College Project Features

This project demonstrates:
- **Django Framework Mastery**: Models, Views, Templates, Forms
- **Database Design**: Proper relationships and constraints
- **User Authentication**: Custom user model and role-based access
- **File Handling**: Image upload and processing
- **Form Validation**: Client and server-side validation
- **Responsive Design**: Mobile-friendly interface
- **Security Best Practices**: CSRF, authentication, authorization
- **Code Organization**: Clean, maintainable structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Alwin Jojy**
- GitHub: [@Alw04j](https://github.com/Alw04j)
- Email: alwinjojy2020@gmail.com

## 🙏 Acknowledgments

- Django framework and community for the excellent web framework
- Bootstrap team for the responsive CSS framework
- College faculty for project requirements and guidance
- Open source contributors and the Python community
- Django Crispy Forms for enhanced form styling

## 📞 Support

For support, email alwinjojy2020@gmail.com or create an issue in the GitHub repository.

---

**Note**: This is a college mini project developed for educational purposes. The system demonstrates modern web development practices using Django framework and can be used as a foundation for real-world leave management systems.

**Last Updated**: December 2024
**Version**: 1.0.0
