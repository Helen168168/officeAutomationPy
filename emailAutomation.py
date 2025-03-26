import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# List of email services with their SMTP server and ports
emailServerPortlist = [
    {
        "name": "QQ邮箱",
        "smtp_server": "smtp.qq.com",
        "ssl_port": 465,
        "tls_port": 587,
        "port": 25
    },
    {
        "name": "163邮箱",
        "smtp_server": "smtp.163.com",
        "ssl_port": 465,
        "tls_port": 994,
        "port": 25
    },
    {
        "name": "Gmail",
        "smtp_server": "smtp.gmail.com",
        "ssl_port": 465,
        "tls_port": 587,
        "port": ''
    },
    {
        "name": "Outlook",
        "smtp_server": "smtp.office365.com",
        "ssl_port": "-",
        "tls_port": 587,
        "port": 25
    },
    {
        "name": "Yahoo",
        "smtp_server": "smtp.mail.yahoo.com",
        "ssl_port": 465,
        "tls_port": 587,
        "port": 25
    }
]

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.qq.com', 25)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

senderEmail = input('Please enter your email: ')
senderPassword = input('Please enter your password: ')
recipientEmail = input('Please enter the recipient email: ')
subject = input('Please enter the subject: ')
emailContent = input('Please enter the email content: ')

# Example usage
send_email(senderEmail, senderPassword, recipientEmail, subject, emailContent)