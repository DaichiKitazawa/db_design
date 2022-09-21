from flaskdb import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    usertype = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<User %r>" % self.id

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    groupname = db.Column(db.String(128), nullable=False)
    theme = db.Column(db.String(256), nullable=False)
    groupcode = db.Column(db.String(64), unique=True, nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<Group %r>" % self.id
    
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    itemname = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<Item %r>" % self.id

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<Order %r>" % self.id

class Join(db.Model):
    __tablename__ = "group_users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<Join %r>" % self.id
    
class Comment(db.Model):
    __tablename__ = "works"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    comment = db.Column(db.String(1024), nullable=False)
    percent = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.String, nullable=False)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' }

    def from_dict(self, d):
        { setattr(self, k, v) for k, v in d.items() }

    def __repr__(self):
        return "<Comment %r>" % self.id
    
