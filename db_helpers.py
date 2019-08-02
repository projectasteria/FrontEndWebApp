from app import db,User

def get_user(username):
    #Returns None if user is not found in the database
    user =db.session.query(User).filter_by(username=username).first()
    return user

def get_email(user):
    return user.email

def get_name(user):
    return user.first_name,user.last_name

def add_user(username,password,email,first_name,last_name):
    if get_user(username) is None:
        new_user=User(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
    else:
        # SETUP LOGGING 
