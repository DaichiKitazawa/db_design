import email
from flask import Blueprint, request, session, render_template, redirect, flash, url_for, jsonify
import datetime
import pickle

from flaskdb import apps, db, da
from sqlalchemy import func
from flaskdb.models import User, Group, Join, Comment
from flaskdb.forms import LoginForm,SignUpForm, AddGroupForm, SearchGroupForm, JoinGroupForm, AddCommentForm, JumpForm

app = Blueprint("app", __name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("/index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    
    if form.validate_on_submit():
        user = User()
        form.copy_to(user)
        db.session.add(user)
        db.session.commit()
        
        flash("User was added.", "info")
        return redirect(url_for("app.signup"))
    
    return render_template("signup.html", form=form)

@app.route("/initdb", methods=["GET", "POST"])
def initdb():
    db.drop_all()
    db.create_all()
    
    admin = User(username="admin", email="test", password="password", usertype="1")
    test = Group(owner_id="1", groupname="testname", theme="testtheme", groupcode="testcode")
    # test1 = Join(user_id="1", group_id="1",)
    # user = User(username="user", password="password")
    
    db.session.add(admin)
    db.session.add(test)
    # db.session.add(test1)
    # db.session.add(user)
    db.session.commit()
    return "initidb() method was executed. "

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data, password=form.password.data).first()

        if user is None or user.password != form.password.data:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("app.login"))

        session["username"] = user.username
        session["glist"] = []
        session["cart"] = []
        
        
        return redirect(url_for("app.index"))

    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    session.pop("cart", None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("app.index"))


@app.route("/addgroup", methods=["GET", "POST"])
def addgroup():
    group_code = []
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = AddGroupForm()

    if form.validate_on_submit():
        group = Group()
        form.copy_to(group)
        user = User.query.filter_by(username=session["username"]).first()
        group.owner_id = user.id
        db.session.add(group)
        db.session.commit()

        flash("Group was added.", "info")
        return redirect(url_for("app.addgroup"))

    return render_template("addgroup.html", form=form)


@app.route("/searchgroup", methods=["GET", "POST"])
def searchgroup():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = SearchGroupForm()
    session["glist"] = []
    
    if form.validate_on_submit():
        grouplist = Group.query.filter(Group.groupcode.like("%" + form.groupcode.data + "%")).all()
        grouplist = pickle.dumps(grouplist)
        session["grouplist"] = grouplist
        return redirect(url_for("app.searchgroup"))

    if "grouplist" in session:
        grouplist = session["grouplist"]
        grouplist = pickle.loads(grouplist)
        session.pop("grouplist", None)
    else:
        # grouplist = Group.query.all()
        grouplist = []
    
    return render_template("search_group.html", form=form, grouplist=grouplist)



@app.route("/groupcheck", methods=["GET", "POST"])
def groupcheck():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = JoinGroupForm()

    if request.args.get("group_id") is not None:
        group_id = request.args.get("group_id")
        group = Group.query.filter_by(id = group_id).first()
        if group is not None:
            session["glist"].append(group.to_dict())
            session.modified = True
            session["groupid"]=group.id

            item2 = Group()
            item2.from_dict(group.to_dict())

            return redirect(url_for("app.groupcheck")) # comment out and reload the page

    return render_template("groupcheck.html", form=form)



@app.route("/joingroup", methods=["GET", "POST"])
def joingroup():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))
    
    form = JumpForm()
    
    if "glist" in session:
        glist = session["glist"]
        username = session["username"]
        
        for group in glist:
            user = User.query.filter_by(username=username).first()
            join = Join(user_id=user.id, group_id=group["id"])
            db.session.add(join)

        if len(glist) > 0:
            db.session.commit()
            
        session.modified = True

    return render_template("joingroup.html", form=form, glist=glist)

@app.route("/room", methods=["GET", "POST"])
def room():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = AddCommentForm()
    
    if "groupid" in session:
        # group_id = request.args.get("group_id")
        group_id = session["groupid"]
        group = Group.query.filter_by(id = group_id).first()
        if group is not None:
            session["glist"].append(group.to_dict())
            session.modified = True

            item2 = Group()
            item2.from_dict(group.to_dict())
            
            if form.validate_on_submit():
                com = Comment()
                form.copy_to(com)
                create_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                user = User.query.filter_by(username=session["username"]).first()
                com.user_id = user.id
                com.group_id = group.id
                com.create_date = create_date
                db.session.add(com)
                db.session.commit()
                
                return redirect(url_for("app.room")) # comment out and reload the page
    # else:
    #     return redirect(url_for("app.login"))
    # select works.user_id, works.group_id, works.comment, works.percent 
    # from works 
    # inner join(
        # select user_id, max(create_date) create_date 
        # from works group by user_id ) t1 
    # on works.user_id = t1.user_id and works.create_date = t1.create_date;
    comlist = Comment.query.filter_by(group_id=group.id).all()
    # m = Comment.query(Comment.user_id, func.max(Comment.create_date).label('create_date')).filter_by(group_id=group.id).group_by(Comment.user_id) 
    # comlist = Comment.query(Comment.user_id, Comment.group_id, Comment.comment, Comment.percent).filter_by(group_id=group.id).join(m, and_(Comment.user_id==m.user_id, Comment.create_date==m.create_date))
    return render_template("room.html", form=form, comlist=comlist)




# @app.route("ingroup", methods=["GET", "POST"])
# def ingroup():
#     if not "username" in session:
#         flash("Log in is required.", "danger")
#         return redirect(url_for("app.login"))
    
#     # select users.id, users.username, groups.groupname, groups.theme 
#     # from users, groups, group_users 
#     # where users.id = group_users.user_id 
#     # and groups.id = group_users.group_id 
#     # and users.id = 1 ;
    
#     user = User.query.filter_by(username=session["username"]).first()
#     sql = Joined.query(User.id, User.username, Group.groupname, Group.theme).filter( User.id==Join.user_id, Group.id==Join.group_id, User.id==user).all()
#     sql = pickle.dumps(sql)
#     session["sql"] = sql
#     session.pop("sql", None)
    
#     return render_template("ingroup.html", sql = sql)

# @app.route("/commnet", methods=["GET", "POST"])
# def comment():
#     if not "username" in session:
#         flash("Log in is required.", "danger")
#         return redirect(url_for("app.login"))
    
#     form = AddCommentForm()
    
#     if form.validate_on_submit():
#         com = Comment()
#         form.copy_to(com)
#         user = User.query.fulter_by(username=session["username"]).first()
#         com.user_id = user.id
        