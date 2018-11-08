from run import *

class loginform(Form):
	username=TextField(
		'email',
		validators=[
			Email(),
			Required(),
			length(min=5,max=50)
			])
	password=PasswordField(
		'password',
		validators=[
		Required(),
		])