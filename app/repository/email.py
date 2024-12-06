import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.schemas.email import EmailSend

async def send_email(email_data: EmailSend):
    sender_email = "majidkhan0899@gmail.com"
    receiver_email = email_data.recipient
    password = "ffzv xgoh exbr yyqb"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = email_data.subject
    msg.attach(MIMEText(email_data.message, 'plain'))

    # Send the email asynchronously
    try:
        await aiosmtplib.send(
            msg,
            hostname="smtp.gmail.com",
            port=465,
            username=sender_email,
            password=password,
            use_tls=True
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
