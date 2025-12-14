# FitPlanHub

Fitness platform where trainers create workout plans and users can purchase them.

## Features

- User & Trainer signup/login
- Password hashing with bcrypt(python)
- Trainers can create, edit, delete plans
- Users can browse and buy plans
- Users can Follow/unfollow trainers
- Personalized feed for users from followed trainers
- Access control (preview vs full details)

## Tech Used

- Python
- Flask
- MySQL
- SQL
- HTML/CSS
- Flask-Bcrypt (for password hashing)

## Setup

1. Create MYSQL database:
use : CREATE DATABASE fit_plan_hub;

2. Run SQL to create tables (users, plans, subscriptions, follows)

3. Install requirements (in terminal):
use : pip install flask flask-bcrypt pymysql

4.Update password in model.py
Run:
python app.py

5. Open: http://127.0.0.1:5000

## Pages

Home:	/
Signup:	/signup
Login:	/login
Feed:	/feed
Browse:	/browse
Plan Details:	/plan/id
Trainer Profile:	/trainer/id
Dashboard:	/dashboard

## Author
Sandesh Vani

