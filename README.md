# 🚗 AutoCare – Car Service Booking & Management System

AutoCare is a full-stack web application designed to simplify car service booking and customer management.

The application provides a professional frontend for customers to explore services, create an account, log in, book vehicle services, and send enquiries. A Flask backend handles the application logic and connects the system to a MySQL database for storing and retrieving information.

---

## 📌 Project Overview

AutoCare was developed to demonstrate the integration of:

- Frontend web development
- Python Flask backend
- MySQL database integration
- User authentication
- Session management
- Form handling
- Dynamic data retrieval
- Admin dashboard

The project focuses on creating a simple but complete web application with a professional user interface and real database connectivity.

---

## ✨ Features

### 👤 User Features

- User registration
- User login and logout
- Secure password hashing
- Session-based authentication
- View available car services
- Book a car service
- View service bookings
- Submit contact enquiries

### 🔧 Service Booking

Users can provide:

- Customer name
- Phone number
- Email
- Vehicle brand
- Vehicle model
- Vehicle registration number
- Service type
- Preferred service date
- Preferred service time
- Additional message

Booking information is stored in the MySQL database.

### 📊 Admin Dashboard

The admin dashboard provides an overview of:

- Total service bookings
- Pending bookings
- Customer messages
- Service booking details
- Customer information
- Vehicle information
- Contact enquiries

### 🔐 Authentication

The application includes:

- User registration
- Login validation
- Password hashing
- Flask sessions
- Logout functionality
- Protected booking pages

Passwords are stored as hashed values instead of plain text.

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3

### Backend

- Python
- Flask

### Database

- MySQL
- MySQL Connector/Python

### Security

- Werkzeug Password Hashing
- Flask Sessions

---

## 📂 Project Structure

```text
car_service_booking/
│
├── app.py
│
├── README.md
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── services.html
│   ├── about.html
│   ├── contact.html
│   ├── book_service.html
│   ├── bookings.html
│   ├── login.html
│   ├── register.html
│   └── admin.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── images/
        ├── hero.jpg
        ├── service-general.jpg
        ├── service-oil.jpg
        ├── service-brake.jpg
        ├── service-ac.jpg
        └── service-detailing.jpg
