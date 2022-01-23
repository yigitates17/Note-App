from models import User

user = User.query.all()
print(user)