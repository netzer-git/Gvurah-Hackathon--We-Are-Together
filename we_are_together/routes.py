import os
from flask import render_template, url_for, flash, redirect, request
from we_are_together import app, db, bcrypt, category_dict
from we_are_together.forms import RegistrationForm, LoginForm, EnterProject
from we_are_together.models import User, Project
from flask_login import login_user, current_user, logout_user, login_required


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route("/")
@app.route("/home")
def home():
    first_four_projects = Project.query.limit(4)
    return render_template('home.html', title="Home", first_four_projects=first_four_projects)


@app.route("/projects")
def projects():
    project_filter = request.args.get('project_filter', None)
    project_filter_by_str = request.args.get('project_filter_by_str', None)

    #Project.query.filter(Project.project_name.contains(project_filter_by_str))

    if project_filter == (0 or None):
        defined_projects = Project.query.all()
    else:
        defined_projects = Project.query.filter_by(category=project_filter)
    return render_template('projects.html', title='Projects', projects=defined_projects,
                           category_dict=category_dict)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/create_project", methods=['GET', 'POST'])
@login_required
def create_project():
    form = EnterProject()
    if form.validate_on_submit():
        project = Project(project_name=form.project_name.data, category=form.category.data,
                          description=form.project_description.data, manager=current_user.id,
                          need1=form.need1.data, need2=form.need2.data,
                          need3=form.need3.data, need4=form.need4.data, need5=form.need5.data)
        db.session.add(project)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_project.html', title='Create Project', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/view_project", methods=['GET', 'POST'])
def view_project():
    if current_user.is_authenticated:
        current_id = current_user.id
    else:
        current_id = 0
    project_id = request.args.get('project_id', None)
    current_project = Project.query.get(project_id)
    user_join_num = request.args.get('user_join_num', None)
    if user_join_num == "-1":
        current_project.join_update(user_join_num, current_id, delete=True)
    elif user_join_num:
        current_project.join_update(int(user_join_num), current_id)
    already_in = current_project.user_in_project(current_id)
    dict_of_partners = current_project.get_dict_of_partners()
    return render_template('view_project.html', title='View Project', current_project=current_project,
                           category_dict=category_dict, already_in=already_in, project_full=current_project.is_full(),
                           dict_of_partners=dict_of_partners)
