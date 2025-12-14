# User, Plan, Subscription, Follow classes

from dbmanager import DBManager

# database connection
db = DBManager(
    host='localhost',
    user='root',
    password='Qawsedrftg@1',
    dbname='fit_plan_hub'
)


class User:
    ## It Represents a user or trainer
    
    def __init__(self, id, username, email, password_hash, role):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def add_user(uname, mail, pw_hash, user_role='user'):
        
        # for inserting new user into database
        
        sql = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
        db.run(sql, (uname, mail, pw_hash, user_role))

    @staticmethod
    def get_by_email(mail):
        
        # for finding user by email
        
        sql = "SELECT * FROM users WHERE email = %s"
        rows = db.fetch(sql, (mail,))
        if rows and len(rows) > 0:
            return User(**rows[0])
        return None

    @staticmethod
    def get_by_id(uid):
        
        # for finding user by their id
        
        sql = "SELECT * FROM users WHERE id = %s"
        rows = db.fetch(sql, (uid,))
        if rows and len(rows) > 0:
            return User(**rows[0])
        return None

    @staticmethod
    def all_trainers():
        
        # for getting the list of all trainers
        sql = "SELECT * FROM users WHERE role = 'trainer'"
        rows = db.fetch(sql)
        result = []
        for r in rows:
            result.append(User(**r))
        return result


class Plan:
    ## It represents a fitness plan
    
    def __init__(self, id, title, description, price, duration, trainer_id):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.duration = duration
        self.trainer_id = trainer_id

    @staticmethod
    def add_plan(title, desc, price, days, tid):
        
        # creating new plan
        
        sql = "INSERT INTO plans (title, description, price, duration, trainer_id) VALUES (%s, %s, %s, %s, %s)"
        db.run(sql, (title, desc, price, days, tid))

    @staticmethod
    def get_by_id(pid):

        ## finding plans with plan id
        
        sql = "SELECT * FROM plans WHERE id = %s"
        rows = db.fetch(sql, (pid,))
        if rows and len(rows) > 0:
            return Plan(**rows[0])
        return None

    @staticmethod
    def get_by_trainer(tid):
        
        # for showing all plans by a trainer
        
        sql = "SELECT * FROM plans WHERE trainer_id = %s"
        rows = db.fetch(sql)
        if rows is None:
            rows = []
        # need to pass trainer id
        rows = db.fetch(sql, (tid,))
        plans = []
        for r in rows:
            plans.append(Plan(**r))
        return plans

    @staticmethod
    def get_all():

        # for showing all plans
        
        sql = "SELECT * FROM plans"
        rows = db.fetch(sql)
        if rows is None:
            return []
        plans = []
        for r in rows:
            plans.append(Plan(**r))
        return plans

    @staticmethod  
    def modify(pid, title, desc, price, days):
        
        # for updating any existing plan
        
        sql = "UPDATE plans SET title=%s, description=%s, price=%s, duration=%s WHERE id=%s"
        db.run(sql, (title, desc, price, days, pid))

    @staticmethod
    def remove(pid):
        
        # for updating any existing plan
        
        sql = "DELETE FROM plans WHERE id = %s"
        db.run(sql, (pid,))

    @staticmethod
    def get_by_trainer_list(trainer_ids):
        
        # for getting plans from multiple trainers at once by passing list of trainers
        
        if not trainer_ids or len(trainer_ids) == 0:
            return []
            
        # sql query with placeholders
        ph = ','.join(['%s'] * len(trainer_ids))
        sql = f"SELECT * FROM plans WHERE trainer_id IN ({ph})"
        rows = db.fetch(sql, tuple(trainer_ids))
        if rows is None:
            return []
        plans = []
        for r in rows:
            plans.append(Plan(**r))
        return plans


class Subscription:
    ## Tracks which user having which plan
    
    def __init__(self, id, user_id, plan_id, subscribed_at):
        self.id = id
        self.user_id = user_id
        self.plan_id = plan_id
        self.subscribed_at = subscribed_at

    @staticmethod
    def add(uid, pid):
        sql = "INSERT INTO subscriptions (user_id, plan_id) VALUES (%s, %s)"
        db.run(sql, (uid, pid))

    @staticmethod
    def check(uid, pid):
        # for checking if user has this plan
        sql = "SELECT * FROM subscriptions WHERE user_id = %s AND plan_id = %s"
        rows = db.fetch(sql, (uid, pid))
        if rows and len(rows) > 0:
            return True
        return False

    @staticmethod
    def user_plans(uid):
        # getting all plan ids user has bought
        sql = "SELECT plan_id FROM subscriptions WHERE user_id = %s"
        rows = db.fetch(sql, (uid,))
        if rows is None:
            return []
        ids = []
        for r in rows:
            ids.append(r['plan_id'])
        return ids


class Follow:
    ## Tracks which user follows which trainer
    
    def __init__(self, id, user_id, trainer_id, followed_at):
        self.id = id
        self.user_id = user_id
        self.trainer_id = trainer_id
        self.followed_at = followed_at

    @staticmethod
    def add(uid, tid):
        sql = "INSERT INTO follows (user_id, trainer_id) VALUES (%s, %s)"
        db.run(sql, (uid, tid))

    @staticmethod
    def remove(uid, tid):
        sql = "DELETE FROM follows WHERE user_id = %s AND trainer_id = %s"
        db.run(sql, (uid, tid))

    @staticmethod
    def check(uid, tid):
        sql = "SELECT * FROM follows WHERE user_id = %s AND trainer_id = %s"
        rows = db.fetch(sql, (uid, tid))
        if rows and len(rows) > 0:
            return True
        return False

    @staticmethod
    def get_trainers(uid):
        # trainers that user follows
        sql = "SELECT trainer_id FROM follows WHERE user_id = %s"
        rows = db.fetch(sql, (uid,))
        if rows is None:
            return []
        ids = []
        for r in rows:
            ids.append(r['trainer_id'])
        return ids