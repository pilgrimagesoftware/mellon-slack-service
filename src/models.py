__author__ = "Paul Schifferer <paul@schifferers.net>"

# from app import db


# class User(Base):

#     __tablename__ = 'slack_user'

#     # User Name
#     name     = db.Column(db.String(128),  nullable=False)

#     # Identification Data: email & password
#     email    = db.Column(db.String(128),  nullable=False, unique=True)

#     # Authorisation Data: role & status
#     role     = db.Column(db.SmallInteger, nullable=False)
#     status   = db.Column(db.SmallInteger, nullable=False)

#     # New instance instantiation procedure
#     def __init__(self, name, email, password):

#         self.name     = name
#         self.email    = email
#         self.password = password

#     def __repr__(self):
#         return '<User %r>' % (self.name)
