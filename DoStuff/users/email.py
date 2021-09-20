from flask import url_for, current_app
from flask_mail import Message

from DoStuff import mail
from threading import Thread

#asynchorniczne wysyłanie maili przydaję się gdy mamy obsłużyć bardzo duzo requestow o reset i nasza apka by wtedy
# bardzo by zwolniła a tak myk

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()



def send_reset_email(user):
    token = user.get_secret_token()
    send_email("Password Reset Request", sender='john.wiskers@yahoo.com', recipients=[user.email],
               text_body="To reset your password, visit the following link {} \n\n If You did not make this request"
                         " then simply ignore this mail".format(
                   url_for('users.reset_token',
                           token=token,
                           _external=True)))
