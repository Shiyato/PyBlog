from flask import render_template
from initialization import app
from flask_mail import Mail, Message
from threading import Thread


mail = Mail(app)

def send_asyn_letter(app, letter):
    with app.app_context():
        mail.send(letter)

def send_mail(header="It's mesage from Py-blog", to=[], template="mail_template", **temp_vars):
    letter = Message(app.config["MAIL_LETTER_PREFIX"] + header, sender=app.config["MAIL_SENDER"], recipients=to)
    letter.body = render_template(template + ".txt", **temp_vars)
    letter.html = render_template(template + ".htlm", **temp_vars)
    thread = Thread(target=send_asyn_letter, args=[app, letter] )
    thread.start()
    return thread

