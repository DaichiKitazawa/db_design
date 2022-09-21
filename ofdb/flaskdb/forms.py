# from msilib.schema import RadioButton
from tokenize import String
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, length
from flaskdb.widgets import ButtonField


class SignUpForm(FlaskForm):
    username = StringField(
        "User Name",
        validators = [
            DataRequired(message="User Name is required."),
            length(max=64, message="User Name should be input within 64 characters."),
        ],
    )
    email = StringField(
        "Email",
        validators = [
            DataRequired(message="Email is required."),
        ],
    )
    password = PasswordField(
        "Password",
        validators = [
            DataRequired(message="Password is required."),
        ],
    )
    usertype = RadioField(
        "User Type",
        choices = [
            ("1","生徒"),
            ("2", "教師"),
        ],
        default = "1"
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("SignUp")
    
    def copy_from(self, user):
        self.username.data = user.username
        self.email.data = user.email
        self.password.data = user.password
        self.usertype.data = user.usertype

    def copy_to(self, user):
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.usertype = self.usertype.data
        
        

class LoginForm(FlaskForm):
    username = StringField(
        "User Name",
        validators = [
            DataRequired(message="User Name is required."),
            length(max=64, message="User Name should be input within 64 characters."),
        ],
    )
    email = StringField(
        "Email",
        validators = [
            DataRequired(message="Email is required."),
        ],
    )
    password = PasswordField(
        "Password",
        validators = [
            DataRequired(message="Password is required."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Login")

    def copy_from(self, user):
        self.username.data = user.username
        self.email.data = user.email
        self.password.data = user.password

    def copy_to(self, user):
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data

class AddGroupForm(FlaskForm):
    groupname = StringField(
        "Group Name",
        validators = [
            DataRequired(message="Group Name is required."),
        ],
    )
    theme = StringField(
        "Theme",
        validators = [
            DataRequired(message="Group Theme is required."),
        ],
    )
    groupcode = StringField(
        "Group Code",
        validators = [
            DataRequired(message="Group Code is required."),
            length(min=5, max=64, message="Group Code should be input within 64 characters."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Submit")
    
    def copy_from(self, group):
        self.groupname.data = group.groupname
        self.theme.data = group.theme
        self.groupcode.data = group.groupcode

    def copy_to(self, group):
        group.groupname = self.groupname.data
        group.theme = self.theme.data
        group.groupcode = self.groupcode.data

class AddItemForm(FlaskForm):
    itemname = StringField(
        "Item Name",
        validators = [
            DataRequired(message="Item Name is required."),
        ],
    )
    price = IntegerField(
        "Price",
        validators = [
            DataRequired(message="Price is required."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Submit")

    def copy_from(self, item):
        self.itemname.data = item.itemname
        self.price.data = item.price

    def copy_to(self, item):
        item.itemname = self.itemname.data
        item.price = self.price.data

class SearchItemForm(FlaskForm):
    itemname = StringField(
        "Item Name",
        validators = [
            DataRequired(message="Item Name is required."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Submit")

    def copy_from(self, item):
        self.itemname.data = item.itemname

    def copy_to(self, item):
        item.itemname = self.itemname.data
        
class SearchGroupForm(FlaskForm):
    groupcode = StringField(
        "Group Code",
        validators = [
            DataRequired(message="Group Code is required."),
        ],
    )
    cancel = ButtonField("Cancel")
    submit = SubmitField("Submit")

    def copy_from(self, item):
        self.groupcode.data = item.groupcode

    def copy_to(self, item):
        item.groupcode = self.groupcode.data

class AddCommentForm(FlaskForm):
    comment = StringField(
        "Comment",
        validators = [
            DataRequired(message="Comment is required."),
        ],
    )
    percent = IntegerField(
        "Prercent",
        validators = [
            DataRequired(message="Percent is required."),
        ],
    )
    
    cancel = ButtonField("Cancel")
    submit = SubmitField("Submit")
    
    def copy_from(self, com):
        self.comment.data = com.comment
        self.percent.data = com.percent

    def copy_to(self, com):
        com.comment = self.comment.data
        com.percent = self.percent.data

class JumpForm(FlaskForm):
    cancel = ButtonField("Cancel")
    submit = SubmitField("jump")

class CheckOutForm(FlaskForm):
    cancel = ButtonField("Cancel")
    submit = SubmitField("Checkout")


class JoinGroupForm(FlaskForm):
    cancel = ButtonField("Cancel")
    submit = SubmitField("Join")
