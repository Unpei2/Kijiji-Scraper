import smtplib
from email.mime.text import MIMEText


def send_email(email, password, body):
    msg = MIMEText(body)
    msg["Subject"] = "Car Listing Found"
    msg["From"] = email
    msg["To"] = email
    

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Email notification failed: username or password not accepted. Make sure you are using a Gmail App Password, not your regular password.")