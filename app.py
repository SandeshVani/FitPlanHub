
# Main application file


from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from model import User, Plan, Subscription, Follow
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt(app)


# helper functions
def logged_in():
    return 'user_id' in session

def check_trainer():
    return session.get('role') == 'trainer'


# home page - public
@app.route('/')
def index():
    plans = Plan.get_all()
    
    # for adding trainer name to each plan
    plan_list = []
    for p in plans:
        trainer = User.get_by_id(p.trainer_id)
        tname = trainer.username if trainer else 'Unknown'
        plan_list.append({
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'duration': p.duration,
            'trainer': tname
        })
    
    return render_template('index.html', plans=plan_list)


# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form.get('username')
        mail = request.form.get('email')
        pw = request.form.get('password')
        role = request.form.get('role')

        # checking if email already used or not
        existing = User.get_by_email(mail)
        if existing:
            flash('Email already registered')
            return redirect(url_for('signup'))

        # hashing password for security and save user
        hashed = bcrypt.generate_password_hash(pw).decode('utf-8')
        User.add_user(uname, mail, hashed, role)

        flash('Account created! Please login')
        return redirect(url_for('login'))

    return render_template('signup.html')


# login page  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('email')
        pw = request.form.get('password')

        user = User.get_by_email(mail)

        # for verifying password with hashed password
        if user and bcrypt.check_password_hash(user.password_hash, pw):
            # saving info to session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            # for redirecting based on role (user or trainer)
            if user.role == 'trainer':
                return redirect(url_for('trainer_home'))
            else:
                return redirect(url_for('feed'))
        else:
            flash('Wrong email or password')
            return redirect(url_for('login'))

    return render_template('login.html')


# logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully')
    return redirect(url_for('index'))


# user feed will shows plans from trainers that user follows
@app.route('/feed')
def feed():
    if not logged_in():
        return redirect(url_for('login'))

    uid = session['user_id']
    
    # for getting trainers that user follows
    followed = Follow.get_trainers(uid)
    # for getting plans user has bought  
    bought = Subscription.user_plans(uid)
    
    # getting plans from followed trainers
    if len(followed) > 0:
        plans = Plan.get_by_trainer_list(followed)
    else:
        plans = []

    # showing the feed data
    feed_items = []
    for p in plans:
        trainer = User.get_by_id(p.trainer_id)
        feed_items.append({
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'duration': p.duration,
            'trainer': trainer.username,
            'trainer_id': trainer.id,
            'owned': p.id in bought
        })

    return render_template('feed.html', plans=feed_items)


# for browsing all plans
@app.route('/browse')
def browse():
    if not logged_in():
        return redirect(url_for('login'))

    uid = session['user_id']
    plans = Plan.get_all()
    bought = Subscription.user_plans(uid)

    items = []
    for p in plans:
        trainer = User.get_by_id(p.trainer_id)
        items.append({
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'duration': p.duration,
            'trainer': trainer.username,
            'trainer_id': trainer.id,
            'owned': p.id in bought
        })

    return render_template('browse.html', plans=items)


# if someone wants to see a single plan
@app.route('/plan/<int:pid>')
def view_plan(pid):
    if not logged_in():
        return redirect(url_for('login'))

    plan = Plan.get_by_id(pid)
    if plan is None:
        flash('Plan not found')
        return redirect(url_for('browse'))

    trainer = User.get_by_id(plan.trainer_id)
    has_access = Subscription.check(session['user_id'], pid)

    return render_template('plan.html', plan=plan, trainer=trainer, has_access=has_access)


# subscribing to plan
@app.route('/buy/<int:pid>')
def buy_plan(pid):
    if not logged_in():
        return redirect(url_for('login'))

    uid = session['user_id']
    
    # checking if user has already bought or not
    if Subscription.check(uid, pid):
        flash('You already own this plan')
    else:
        Subscription.add(uid, pid)
        flash('Purchase successful!')

    return redirect(url_for('view_plan', pid=pid))


# trainers profile
@app.route('/trainer/<int:tid>')
def trainer_page(tid):
    if not logged_in():
        return redirect(url_for('login'))

    trainer = User.get_by_id(tid)
    if trainer is None or trainer.role != 'trainer':
        flash('Trainer not found')
        return redirect(url_for('browse'))

    plans = Plan.get_by_trainer(tid)
    following = Follow.check(session['user_id'], tid)

    return render_template('trainer.html', trainer=trainer, plans=plans, following=following)


# for following a trainer
@app.route('/follow/<int:tid>')
def do_follow(tid):
    if not logged_in():
        return redirect(url_for('login'))

    uid = session['user_id']
    if not Follow.check(uid, tid):
        Follow.add(uid, tid)
        flash('Now following!')

    return redirect(url_for('trainer_page', tid=tid))


# for unfollowing a trainer
@app.route('/unfollow/<int:tid>')
def do_unfollow(tid):
    if not logged_in():
        return redirect(url_for('login'))

    Follow.remove(session['user_id'], tid)
    flash('Unfollowed')

    return redirect(url_for('trainer_page', tid=tid))


# list of followed trainers
@app.route('/following')
def following():
    if not logged_in():
        return redirect(url_for('login'))

    trainer_ids = Follow.get_trainers(session['user_id'])
    trainers = []
    for tid in trainer_ids:
        t = User.get_by_id(tid)
        if t:
            trainers.append(t)

    return render_template('following.html', trainers=trainers)


# trainer dashboard
@app.route('/dashboard')
def trainer_home():
    if not logged_in() or not check_trainer():
        return redirect(url_for('login'))

    plans = Plan.get_by_trainer(session['user_id'])
    return render_template('dashboard.html', plans=plans)


# creating new plan
@app.route('/create', methods=['GET', 'POST'])
def create():
    if not logged_in() or not check_trainer():
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        price = request.form.get('price')
        days = request.form.get('duration')

        Plan.add_plan(title, desc, price, days, session['user_id'])
        flash('Plan created!')
        return redirect(url_for('trainer_home'))

    return render_template('create.html')


# editing plan
@app.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit(pid):
    if not logged_in() or not check_trainer():
        return redirect(url_for('login'))

    plan = Plan.get_by_id(pid)
    
    # checking ownership
    if plan is None or plan.trainer_id != session['user_id']:
        flash('Not allowed')
        return redirect(url_for('trainer_home'))

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        price = request.form.get('price')
        days = request.form.get('duration')

        Plan.modify(pid, title, desc, price, days)
        flash('Plan updated!')
        return redirect(url_for('trainer_home'))

    return render_template('edit.html', plan=plan)


# deleting plan
@app.route('/delete/<int:pid>')
def delete(pid):
    if not logged_in() or not check_trainer():
        return redirect(url_for('login'))

    plan = Plan.get_by_id(pid)
    if plan and plan.trainer_id == session['user_id']:
        Plan.remove(pid)
        flash('Plan deleted')

    return redirect(url_for('trainer_home'))


if __name__ == '__main__':
    app.run(debug=True)