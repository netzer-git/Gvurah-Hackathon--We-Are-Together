from datetime import datetime
from we_are_together import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(150), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    need1 = db.Column(db.String(100), nullable=False)
    need2 = db.Column(db.String(100), nullable=True)
    need3 = db.Column(db.String(100), nullable=True)
    need4 = db.Column(db.String(100), nullable=True)
    need5 = db.Column(db.String(100), nullable=True)
    manager = db.Column(db.Integer, nullable=False)
    join1 = db.Column(db.Integer, nullable=True)
    join2 = db.Column(db.Integer, nullable=True)
    join3 = db.Column(db.Integer, nullable=True)
    join4 = db.Column(db.Integer, nullable=True)
    join5 = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Project('{self.id}', '{self.project_name}', '{self.creation_date}', '{self.categories}'" \
               f", '{self.description}', '{self.needs}', '{self.manager}')"

    def join_update(self, join_num, user_id, delete=False):
        if not delete:
            if join_num == 1:
                if self.join1 is None:
                    self.join1 = user_id
                elif self.join2 is None:
                    self.join2 = user_id
                elif self.join3 is None:
                    self.join3 = user_id
                elif self.join4 is None:
                    self.join4 = user_id
                elif self.join5 is None:
                    self.join5 = user_id
        else:
            if self.join1 == user_id:
                self.join1 = None
            elif self.join2 == user_id:
                self.join2 = None
            elif self.join3 == user_id:
                self.join3 = None
            elif self.join4 == user_id:
                self.join4 = None
            elif self.join5 == user_id:
                self.join5 = None
        db.session.commit()

    def user_in_project(self, user_id):
        is_user_in_project = False
        if self.join1 == user_id:
            is_user_in_project = True
        elif self.join2 == user_id:
            is_user_in_project = True
        elif self.join3 == user_id:
            is_user_in_project = True
        elif self.join4 == user_id:
            is_user_in_project = True
        elif self.join5 == user_id:
            is_user_in_project = True

        return is_user_in_project

    def is_full(self):
        full1 = not self.need1 or (self.need1 and self.join1)
        full2 = not self.need2 or (self.need2 and self.join2)
        full3 = not self.need3 or (self.need3 and self.join3)
        full4 = not self.need4 or (self.need4 and self.join4)
        full5 = not self.need5 or (self.need5 and self.join5)
        return full1 and full2 and full3 and full4 and full5

    def get_dict_of_partners(self):
        dict_of_partners = {}
        if self.join1:
            dict_of_partners[self.need1] = User.query.get(self.join1).username
        if self.join2:
            dict_of_partners[self.need2] = User.query.get(self.join2).username
        if self.join3:
            dict_of_partners[self.need3] = User.query.get(self.join3).username
        if self.join4:
            dict_of_partners[self.need4] = User.query.get(self.join4).username
        if self.join5:
            dict_of_partners[self.need5] = User.query.get(self.join5).username
        return dict_of_partners















