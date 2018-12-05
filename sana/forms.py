from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo

class PNOForm(FlaskForm):
    pno = StringField('Enter your phone number: ', validators = [DataRequired(),
                                                                 Regexp('[1-9][0-9]{11}',
                                                                        message = 'Enter 12 digits')],
                                                                 render_kw = {'placeholder': '9891212345678'})
    submit = SubmitField('Login')

    def __repr__(self):
        return '<PNOForm: {}>'.format(self.pno)

class NameForm(FlaskForm):
    firstname = StringField('Enter your first name: ', validators = [DataRequired(),
                                                                     Regexp('[a-zA-Z]+',
                                                                            message = 'Only letters are accepted')],
                                                                     render_kw = {'placeholder': 'John'})
    lastname = StringField('Enter your last name: ', validators = [DataRequired(),
                                                                   Regexp('[a-zA-Z]+',
                                                                          message = 'Only letters are accepted')],
                                                                   render_kw = {'placeholder': 'Kennedy'})
    submit = SubmitField('Login')

    def __repr__(self):
        return '<NameForm: {}>'.format(self.pno)

class PasswordForm(FlaskForm):
    password = PasswordField('Enter your password: ', validators = [DataRequired(),
                                                                    Regexp('\\D{8,}',
                                                                           message = 'Enter 8 characters of alphanumeric type')])
    password2 = PasswordField('Enter your password: ', validators = [DataRequired(),
                                                                     EqualTo('password', message = "Passwords must match")])

    submit = SubmitField('Login')

    def __repr__(self):
        return '<PNOForm: {}>'.format(self.pno)

class LoginForm(FlaskForm):
    password = PasswordField('Enter your password: ', validators = [DataRequired()])
    submit = SubmitField('Login')

    def __repr__(self):
        return '<PNOForm: {}>'.format(self.pno)
