from flask_mail import Message
from mail import mail
from initialization import app


msg = Message('leters header', sender='zhdanov.ph@gmail.com', recipients=['zhdanov.ph@gmail.com'])
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
    mail.send(msg)


