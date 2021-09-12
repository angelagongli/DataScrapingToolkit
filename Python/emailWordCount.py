import sys
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

sender_email = "angelagongli+sender@gmail.com"
receiver_email = "angelagongli+recipient@gmail.com"
password = input("Enter your password and then hit return: ")

# Create MIMEMultipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Cc"] = sender_email
message["Subject"] = "Word Count"

body = f"""Hi, {receiver_email}!\n\n
I just want you to know that according to the command line utility wc,
the file I am sending you contains a total of {sys.argv[2]} words.\n\n
Thank you!\n\n
Best,\n
{sender_email}"""
# bodyHTML = f"""\
# <html>
#     <body>
#         <p>Hi, {receiver_email}!</p>
#         <p>I just want you to know that according to the command line utility wc,\
#             the file I am sending you contains a total of <em>{sys.argv[2]}</em> words.</p>
#         <p>Thank you!</p>
#         <p>Best,</p>
#         <p>{sender_email}</p>
#     </body>
# </html>
# """

# Add body to email
message.attach(MIMEText(body, "plain"))
# message.attach(MIMEText(bodyHTML, "html"))

filename = sys.argv[1]

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename={filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
