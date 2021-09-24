from flask import url_for, current_app
from flask_mail import Message
from app import mail
from threading import Thread


def send_async_email(app, msg):
    """
    Function runs in a background thread invoked via the Thread class in the last line of send_email() function,
    when the process of sending completes the thread will end and clean itself up.

    Not only msg argument would be send into thread, also application instance would be send to thread.

    Flask uses application context to avoid passes arguments across functions. The reason of that many extensions
    need to know the application instance is because they have their configuration stored in the DoStuff.config.
    This is situation with mail (from Dostuff import mail). The mail.send() methods needs to access the configuration
    values from the email server, and that can be only done by knowing what the application is. The application
    context that is created with the `with app.app_context()` call makes the application instance accessible via
    the current_app variable from Flask.
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body):
    """
    Asynchronous function, the task of sending the email is scheduled to happen in the background, freeing the
    send_email() to return immediately so the application can continue running concurrently with the email being sent.

    Flask current_app variable eliminates the need of importing the application instance as a global variable.

    To access into real application instance that is stored inside the proxy object, and pass as the `app` argument
    The `current_app._get_current_object()` expression extracts the actual application instance from inside the
    proxy object, so that is what is pass to thread as an argument.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_reset_email(user):
    """
    Function responsible for sending a resetting password token. Connected with reset_password() func. located in
    users.routes. Token variable logic coded in DoStuff/models.py.
    """
    token = user.get_secret_token()
    send_email("Password Reset Request",
               sender='john.wiskers@yahoo.com',
               recipients=[user.email],
               text_body="To reset your password, visit the following link {} \n\n If You did not make this request"
                         "then simply ignore this mail".format(
                                                                url_for('users.reset_token',
                                                                        token=token,
                                                                        _external=True)))
