from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kw):
    app = current_app._get_current_object()
    msg = Message(app.config['BLOG-EMAIL-SUBJECT-PREFIX']) + subject,
                  sender=app.config['BLOG-MAIL-SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kw) 
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_email,
                 args=[app, msg])
    thr.start()
    return thr
