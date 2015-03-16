from email.mime.text import MIMEText
from subprocess import Popen, PIPE


# send an email using sendmail
def sendmail(sender, recipient, subject, body):
    msg = MIMEText(body)
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(bytes(msg.as_string(), 'UTF-8'))
