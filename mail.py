from flask import render_template
from initialization import app
from flask_mail import Mail, Message


mail = Mail(app)

def send_mail(header="It's mesage from Py-blog", to=[], template="mail_template", **temp_vars):
    letter = Message(app.config["MAIL_LETTER_PREFIX"] + header, sender=app.config["MAIL_SENDER"], recipients=to)
    letter.body = render_template(template + ".txt", **temp_vars)
    letter.html = ""
    with app.app_context():
        mail.send(letter)
