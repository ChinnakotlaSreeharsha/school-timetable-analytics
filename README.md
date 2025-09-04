# 🎓 School Timetable Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://djangoproject.com)
[![HTML](https://img.shields.io/badge/HTML-5-orange.svg)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-3-blue.svg)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

> **Professional-grade timetable management system for educational institutions with real-time analytics and modern UI/UX**

## 🌟 Overview

The **School Timetable Management System** is a comprehensive web application designed to streamline academic scheduling for educational institutions. Built with Django and featuring a modern, responsive interface, this system provides administrators with powerful tools to manage classes, teachers, subjects, and classroom allocations efficiently.

### ✨ Key Highlights

- **🎨 Modern UI/UX**: Professional design with smooth animations and glassmorphism effects
- **📊 Real-Time Analytics**: Live data visualization with Chart.js integration
- **📱 Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **⚡ Performance Optimized**: Fast loading with efficient database queries
- **🔐 Secure Authentication**: Role-based access control with logout confirmation
- **🎯 User-Centric Design**: Intuitive interface designed for educational administrators

## 🚀 Features

### 📋 Core Functionality
- **Class Management**: Create, edit, and organize academic classes by grade levels
- **Teacher Administration**: Manage teaching staff with employee ID tracking
- **Subject Catalog**: Comprehensive subject management with course codes
- **Classroom Allocation**: Room booking and capacity management
- **Time Slot Scheduling**: Flexible period management with break times

### 📊 Advanced Analytics
- **Weekly Schedule Distribution**: Visual representation of class schedules across weekdays
- **Subject Distribution Analysis**: Real-time breakdown of active subjects
- **Teacher Workload Monitoring**: Track teaching assignments and load balancing
- **Classroom Utilization**: Monitor room occupancy and optimization opportunities

### 🎨 User Experience
- **Interactive Dashboard**: Clean, professional interface with hover effects
- **Modal-Based Analytics**: On-demand chart viewing with smooth transitions
- **Toast Notifications**: Real-time system status updates
- **Confirmation Dialogs**: Safety checks for critical operations like logout
- **Responsive Grid System**: Adaptive layouts for various screen sizes

### 🔧 Technical Features
- **Django Admin Integration**: Full backend administrative interface
- **Template-Based Architecture**: Modular HTML template system
- **Real-Time Data Binding**: Live backend data integration
- **Chart.js Visualization**: Professional data visualization
- **FontAwesome Icons**: Modern iconography throughout the interface

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Django 4.0+**: Web framework
- **SQLite/PostgreSQL**: Database management
- **Django Templates**: Server-side rendering

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript ES6+**: Interactive functionality
- **Chart.js**: Data visualization
- **FontAwesome**: Icon library
- **Space Grotesk Font**: Professional typography

### Development Tools
- **Git**: Version control
- **VS Code**: Development environment
- **Chrome DevTools**: Debugging and optimization

## 📦 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
Git
```

### Quick Start
```bash
# Clone the repository
git clone https://github.com/ChinnakotlaSreeharsha/school-timetable-analytics.git
cd school-timetable-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Access Points
- **Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Timetable View**: http://localhost:8000/timetable/

## 🎯 Usage Guide

### 1. Initial Setup
1. Access the Django Admin panel (`/admin/`)
2. Create your first school classes
3. Add teachers with their specializations
4. Define subjects with course codes
5. Set up classrooms with capacity information
6. Configure time periods and break schedules

### 2. Dashboard Navigation
- **Statistics Cards**: Click to view detailed breakdowns
- **Analytics Button**: Access real-time charts and visualizations
- **Class Cards**: Quick access to individual class timetables
- **Admin Link**: Direct access to administrative functions

### 3. Timetable Management
- Navigate to individual class timetables
- View weekly schedules in grid format
- Access detailed time slot information
- Manage conflicts and overlapping schedules

### 4. Analytics Dashboard
- **Weekly Distribution**: See class load across weekdays
- **Subject Analysis**: Monitor subject variety and distribution
- **Teacher Workload**: Balance teaching assignments
- **Room Utilization**: Optimize classroom usage

## 📸 Screenshots

### Dashboard Overview
```
🎯 Clean, professional interface with:
- Live statistics cards with hover effects
- On-demand analytics viewing
- Streamlined class navigation
- Professional branding and typography
```

### Real-Time Analytics
```
📊 Comprehensive data visualization:
- Interactive charts with Chart.js
- Live backend data integration
- Multiple visualization types (bar, doughnut, line)
- Professional color schemes
```

### Timetable Grid
```
📅 Intuitive scheduling interface:
- Weekly grid layout
- Color-coded subjects
- Teacher and room information
- Conflict detection and resolution
```

## 🔧 Configuration

### Database Setup
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or sqlite3
        'NAME': 'school_timetable',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Analytics Data Configuration
```python
# Context variables for real-time analytics
context = {
    'weekly_schedule_data': {
        'Monday': class_count_monday,
        'Tuesday': class_count_tuesday,
        # ... etc
    },
    'subject_distribution_data': {
        'Mathematics': math_subject_count,
        'Science': science_subject_count,
        # ... etc
    },
    'teacher_workload_data': {
        'Teacher Name': assigned_classes_count,
        # ... etc
    },
    'room_occupancy_data': {
        '9AM': occupancy_percentage,
        # ... etc
    }
}
```

## 📚 API Documentation

### Model Structure
```python
# Core Models
Class:
    - name: CharField
    - grade_level: IntegerField
    - academic_year: CharField
    - total_students: IntegerField

Teacher:
    - user: OneToOneField(User)
    - employee_id: CharField
    - specialization: CharField

Subject:
    - name: CharField
    - code: CharField
    - credits: IntegerField

Classroom:
    - name: CharField
    - room_number: CharField
    - capacity: IntegerField
    - room_type: CharField

TimeSlot:
    - class_ref: ForeignKey(Class)
    - teacher: ForeignKey(Teacher)
    - subject: ForeignKey(Subject)
    - classroom: ForeignKey(Classroom)
    - day_of_week: CharField
    - period: ForeignKey(Period)
```

### Key Views
```python
# Dashboard view with analytics data
def dashboard_view(request):
    # Returns comprehensive dashboard with real-time data

# Class timetable view
def class_timetable_view(request, class_id):
    # Returns detailed timetable for specific class

# Analytics data API
def analytics_data_view(request):
    # Returns JSON data for chart visualization
```

## 🤝 Contributing

We welcome contributions to improve the School Timetable Management System! Here's how you can help:

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guidelines for Python code
- Write clear, commented code
- Add tests for new functionality
- Update documentation as needed
- Ensure responsive design compatibility

### Areas for Contribution
- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **New Features**: Enhance functionality
- 📚 **Documentation**: Improve guides and examples
- 🎨 **UI/UX**: Design improvements
- ⚡ **Performance**: Optimization opportunities
- 🧪 **Testing**: Unit and integration tests

## 📋 Roadmap

### Phase 1: Enhanced Features
- [ ] Email notifications for schedule changes
- [ ] PDF export functionality for timetables
- [ ] Advanced conflict resolution algorithms
- [ ] Multi-school support

### Phase 2: Mobile App
- [ ] React Native mobile application
- [ ] Push notifications
- [ ] Offline synchronization
- [ ] Mobile-optimized analytics

### Phase 3: Advanced Analytics
- [ ] Predictive analytics for scheduling
- [ ] Machine learning recommendations
- [ ] Advanced reporting dashboard
- [ ] Integration with academic systems

### Phase 4: Collaboration Features
- [ ] Real-time collaboration tools
- [ ] Comment system for schedule changes
- [ ] Version control for timetables
- [ ] Audit logs and change tracking

## 🐛 Issue Reporting

Found a bug or have a feature request? Please use the GitHub Issues page:

1. **Search existing issues** first
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Environment details (Python version, Django version)
   - Steps to reproduce
   - Expected vs. actual behavior
   - Screenshots if applicable

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Chinnakotla Sree Harsha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👨‍💻 Developer

**Chinnakotla Sree Harsha**
- 🌐 Portfolio: [myportfolio-i3gd.onrender.com](https://myportfolio-i3gd.onrender.com)
- 📧 Contact: [Contact Form](https://myportfolio-i3gd.onrender.com/contact/)
- 💼 LinkedIn: [Professional Profile](https://www.linkedin.com/in/chinnakotla-sree-harsha/)
- 🐙 GitHub: [@ChinnakotlaSreeharsha](https://github.com/ChinnakotlaSreeharsha)

### About the Developer
**Data Analyst & Full-Stack Developer** with expertise in:
- **Backend Development**: Python, Django, REST APIs
- **Frontend Development**: HTML5, CSS3, JavaScript, React
- **Data Analysis**: Statistical Modeling, Machine Learning
- **Database Management**: PostgreSQL, MySQL, SQLite
- **Cloud Deployment**: AWS, Heroku, Digital Ocean

## 🙏 Acknowledgments

- **Django Community** for the excellent web framework
- **Chart.js Team** for powerful visualization library  
- **FontAwesome** for comprehensive icon library
- **Google Fonts** for the Space Grotesk typography
- **Educational Institutions** for inspiration and requirements
- **Open Source Community** for tools and libraries

## 📈 Project Statistics

- **Lines of Code**: 2,500+ (HTML: 75.4%, Python: 24.6%)
- **Files**: 15+ template and Python files
- **Features**: 20+ core functionalities
- **Database Tables**: 8 main models
- **Responsive Breakpoints**: 3 device categories
- **Browser Support**: Chrome, Firefox, Safari, Edge

## 🔗 Related Projects

- [Django Admin Dashboard](https://github.com/example/django-admin)
- [Educational Management System](https://github.com/example/edu-system)
- [School Analytics Platform](https://github.com/example/school-analytics)

---

<div align="center">
  <p><strong>Built with ❤️ by Chinnakotla Sree Harsha</strong></p>
  <p>Professional timetable management for modern educational institutions</p>
  
  [![GitHub stars](https://img.shields.io/github/stars/ChinnakotlaSreeharsha/school-timetable-analytics.svg?style=social&label=Star)](https://github.com/ChinnakotlaSreeharsha/school-timetable-analytics)
  [![GitHub forks](https://img.shields.io/github/forks/ChinnakotlaSreeharsha/school-timetable-analytics.svg?style=social&label=Fork)](https://github.com/ChinnakotlaSreeharsha/school-timetable-analytics/fork)
  [![GitHub watchers](https://img.shields.io/github/watchers/ChinnakotlaSreeharsha/school-timetable-analytics.svg?style=social&label=Watch)](https://github.com/ChinnakotlaSreeharsha/school-timetable-analytics)
</div>

---

**⭐ Star this repository if you find it helpful!**
