import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dns.resolver
import getpass

def get_smtp_server(email):
	domain = email.split("@")[1]
	records = dns.resolver.resolve(domain, "MX")
	mx_record = records[0].exchange.to_text()
	return mx_record

# Set up argument parser
parser = argparse.ArgumentParser(description="Send an HTML email.")
parser.add_argument("-s", "--sender", nargs=2, required=True, help="The sender's email address and password")
parser.add_argument("-su", "--surname", required=False, help="The sender's email address seen by the receiver")
parser.add_argument("-r", "--receiver", required=True, help="The receiver's email address")
parser.add_argument("-f", "--file", required=True, help="Path to the HTML file to be sent")
parser.add_argument("-sub", "--subject", required=False, help="Subject of the email")

args = parser.parse_args()

sender_email = args.sender[0]
password = args.sender[1]
receiver_email = args.receiver
html_file = args.file
email_subject = args.subject if args.subject else "HTML Email"

# Read the HTML file
with open(html_file, "r") as file:
	html_content = file.read()

# Create a multipart message
message = MIMEMultipart()

if args.surname:
	message["From"] = args.surname
else:
	message["From"] = sender_email

message["To"] = receiver_email
message["Subject"] = email_subject

# Set the HTML content to the message
message.attach(MIMEText(html_content, "html"))

try:
	# Get the SMTP server
	smtp_server = get_smtp_server(sender_email)
	smtp_port = 587 # Default port for SMTP

	# Connect to the SMTP server and send the email
	with smtplib.SMTP("smtp.gmail.com", 587) as server:
		server.starttls()
		server.login(sender_email, password)
		server.send_message(message)
	print("Email sent successfully!")
except smtplib.SMTPAuthenticationError:
    print("Error: Authentication failed. Please check your email and password.")
except smtplib.SMTPConnectError:
    print("Error: Unable to connect to the SMTP server. Please check the server address and port.")
except smtplib.SMTPRecipientsRefused:
    print("Error: The recipient's email address was refused. Please check the recipient's email address.")
except smtplib.SMTPSenderRefused:
    print("Error: The sender's email address was refused. Please check the sender's email address.")
except smtplib.SMTPDataError:
    print("Error: The SMTP server refused to accept the message data.")
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Commande par défaut
# ./venv/bin/python mail_sender.py -s abelio.supor@gmail.com rlyfbavqgymtbqgr -r mathis.sigier@abelio.io -f ../templates_mails_html/abelio_mail.html -sub "Aurevoir At Home" -su "Support Abelio"