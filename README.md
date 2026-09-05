# Task 1 — URL Shortener

This is a **URL Shortener web application** built using Flask and PostgreSQL. It converts long URLs into short, unique links and redirects users to the original URL.

## Features

* Shorten long URLs
* Generate unique 6-character short codes
* Store URLs in PostgreSQL
* Redirect short URLs to the original URLs

## Tech Stack

* Python
* Flask
* PostgreSQL
* Flask-SQLAlchemy
* HTML/CSS/JavaScript

## 📸 Screenshot

Here’s a preview of the URL Shortener:

<img width="838" height="756" alt="Screenshot 2026-09-05 140853" src="https://github.com/user-attachments/assets/3727a5bb-9deb-42b4-9948-b19c1dcaac7b" />

## ▶️ Run Locally

1. Install the required dependencies:

2. Create a `.env` file and add your PostgreSQL password:
db_password=YOUR_POSTGRES_PASSWORD

3. Create a PostgreSQL database named `url_shortener`.

4. Run the application:
python app.py

5. Open `http://127.0.0.1:5000` in your browser.

---

# Task 4 — Job Board Platform

This is a **Job Board Platform REST API** built using Django and PostgreSQL. It allows employers to post jobs and manage applications while candidates can search and apply for jobs.

## Features

* Candidate and employer registration
* Token-based authentication
* Post and search jobs
* Filter jobs by location and salary
* Apply for jobs
* Upload resumes
* Track application status
* Employer and candidate notifications

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Django ORM

## 📸 Screenshot

Here’s a preview of the URL Shortener:

<img width="946" height="1145" alt="Screenshot 2026-09-05 162952" src="https://github.com/user-attachments/assets/74041d92-1651-435d-a597-f114d9a8bbe3" />


## ▶️ Run Locally

1. Install the required dependencies:

2. Apply database migrations:
python manage.py migrate

3. Run the application:
python manage.py runserver

4. Open `http://127.0.0.1:8000` in your browser.

## 🙋‍♀️ Author

Meenakshi418
