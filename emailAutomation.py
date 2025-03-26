import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional, Union

class EmailAutoSender:
    SMTP_CONFIG = {
        'qq': {
            "name": "QQ邮箱",
            "smtp_server": "smtp.qq.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": 25
        },
        "163": {
            "name": "163邮箱",
            "smtp_server": "smtp.163.com",
            "ssl_port": 465,
            "tls_port": 994,
            "port": 25
        },
        'gmail': {
            "name": "Gmail",
            "smtp_server": "smtp.gmail.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": ''
        },
        'outlook': {
            "name": "Outlook",
            "smtp_server": "smtp.office365.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": 25
        },
        'Yahoo': {
            "name": "Yahoo",
            "smtp_server": "smtp.mail.yahoo.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": 25
        },
        'iCloud': {
            "name": "iCloud",
            "smtp_server": "smtp.mail.me.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": ''
        },
        'Sina': {
            "name": "Sina",
            "smtp_server": "smtp.sina.com",
            "ssl_port": 465,
            "tls_port": '',
            "port": 25
        },
        'mxhichina': {
            "name": "阿里云企业邮箱",
            "smtp_server": "smtp.mxhichina.com",
            "ssl_port": 465,
            "tls_port": 587,
            "port": ''
        }
    }
    def __init__(self,
        username: str,
        password: str,
        service: str = 'custom',
        host: Optional[str] = None,
        port: Optional[int] = None,
        use_ssl: bool = True,
        timeout: int = 10000):
        self.username = username
        self.password = password
        self.timeout = timeout
        self.service = service

        # 自动匹配服务商配置
        if service.lower() in self.SMTP_CONFIG:
            config = self.SMTP_CONFIG[service.lower()]
            self.host = config['smtp_server']
            self.port = config['ssl_port'] if use_ssl else config['tls_port']
        else:
            if not host or not port:
                raise ValueError("自定义服务商必须指定 host 和 port！")
            self.host = host
            self.port = port

        self.use_ssl = use_ssl
        self.context = ssl.create_default_context()

    # List of email services with their SMTP server and ports
    def send_email(self,
            to_emails: Union[str, List[str]],
            subject: str,
            content: str,
            is_html: bool = False,
            attachments: Optional[List[str]] = None,
            cc_emails: Optional[Union[str, List[str]]] = None):
        # 规范化收件人和抄送人格式
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails] if cc_emails else None

        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        if cc_emails:
            msg['Cc'] = ', '.join(cc_emails)

        # 添加正文（HTML 或纯文本）
        body_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(content, body_type, 'utf-8'))

        # 添加附件
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    part.add_header('Content-Disposition', 'attachment', filename=file_path.split('/')[-1])
                    msg.attach(part)

        try:
            # 建立连接并发送
            if self.use_ssl:
                try:
                    with smtplib.SMTP_SSL(
                            host=self.host,
                            port=self.port,
                            timeout=self.timeout,
                            context=self.context
                    ) as server:
                        server.login(self.username, self.password)
                        server.sendmail(self.username, to_emails + (cc_emails or []), msg.as_string())
                except (smtplib.SMTPException, ConnectionRefusedError):
                    # Fallback to TLS if SSL fails
                    with smtplib.SMTP(
                            host=self.host,
                            port=self.SMTP_CONFIG[self.service]['tls_port'],
                            timeout=self.timeout
                    ) as server:
                        server.starttls(context=self.context)  # 显式启用 TLS
                        server.login(self.username, self.password)
                        server.sendmail(self.username, to_emails + (cc_emails or []), msg.as_string())
            else:
                with smtplib.SMTP(
                        host=self.host,
                        port=self.port,
                        timeout=self.timeout
                ) as server:
                    server.starttls(context=self.context)  # 显式启用 TLS
                    server.login(self.username, self.password)
                    server.sendmail(self.username, to_emails + (cc_emails or []), msg.as_string())
            print("邮件发送成功！")
            return True
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            return False

username = input('pralse input your email username:')
password = input('please input your email password:')
toEmail = input('please input the email address you want to send:')

# 示例2：发送带附件的HTML邮件（QQ邮箱）
sender_mail = EmailAutoSender(
    username=username,
    password=password,  # QQ邮箱需用授权码
    service='qq'
)
sender_mail.send_email(
    to_emails=[toEmail],
    subject='HTML邮件',
    content='Hello, World! Welcome to Python Programming',
    is_html=False,
    attachments=[],
    cc_emails=''
)

