# FitPlanHub

A simple fitness platform where trainers can create and sell workout plans. Users can browse plans, purchase them, and follow their favorite trainers.

---

## Features

- User & Trainer signup/login
- Password hashing with bcrypt
- Trainers can create, edit, delete plans
- Users can browse and buy plans
- Follow/unfollow trainers
- Personalized feed from followed trainers
- Access control (preview vs full details)

---

## Tech Used

- Python Flask
- MySQL
- HTML/CSS
- Flask-Bcrypt

---

## Setup

1. Create database in MySQL:
   CREATE DATABASE fit_plan_hub;

2. Run SQL to create tables (users, plans, subscriptions, follows)

3. Install requirements:
   pip install flask flask-bcrypt pymysql

4. Update password in model.py

5. Run app:
   python app.py

6. Open browser:
   http://127.0.0.1:5000

---

## How to Use

When you open the app, you will see the home page with all available plans. You can signup as either a trainer or a regular user.

If you signup as a trainer, you will be taken to your dashboard after login. From there you can create new fitness plans by adding a title, description, price and duration. You can also edit or delete your existing plans anytime.

If you signup as a user, you will see your personalized feed after login. You can browse all available plans and see a preview of each plan including title, trainer name and price. To see full details of any plan, you need to purchase it first. The payment is simulated so no real money involved.

You can also visit any trainer's profile and follow them. Once you follow a trainer, their plans will appear in your feed. You can unfollow anytime from their profile or from your following list.

---

## Pages

- Home: /
- Signup: /signup
- Login: /login
- Feed: /feed
- Browse Plans: /browse
- Plan Details: /plan/id
- Trainer Profile: /trainer/id
- Following List: /following
- Trainer Dashboard: /dashboard
- Create Plan: /create
- Edit Plan: /edit/id
---

## Author

Sandesh Vani
