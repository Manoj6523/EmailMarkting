import requests 
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Specify the URL
url = "https://www.citdindia.org"

# Fetch the web page content
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Check for HTTP errors
    webpage_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(webpage_content, "html.parser")
text = soup.get_text()  # Extract only the text content

# Find all email addresses using a regular expression
email_list = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

# Display the results
if email_list:
    print("Email Addresses found:")
    for email in email_list:
        print(email)
else:
    print("No email addresses found.")

# Option to add custom email addresses
custom_emails = input("Enter additional email addresses separated by commas (or press Enter to skip): ")
if custom_emails.strip():
    custom_email_list = [email.strip() for email in custom_emails.split(',')]
    email_list.extend(custom_email_list)

# Remove duplicates
email_list = list(set(email_list))

# Allow user to modify the email list
print("\nCurrent email list:")
for i, email in enumerate(email_list, start=1):
    print(f"{i}. {email}")

print("\nYou can modify the email list.")
print("Enter the number of the email you want to remove, or type 'done' to finish.")

while True:
    user_input = input("Enter your choice: ").strip()
    if user_input.lower() == 'done':
        break
    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(email_list):
            removed_email = email_list.pop(index)
            print(f"Removed: {removed_email}")
            print("Updated email list:")
            for i, email in enumerate(email_list, start=1):
                print(f"{i}. {email}")
        else:
            print("Invalid number. Try again.")
    else:
        print("Invalid input. Enter a number or 'done'.")

# Send custom emails to the modified list
# Gmail SMTP configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "enter email from which you need to send the message"  # Replace with your email
app_password = "enter the email app password, in gmail you can set the password from security settings"  # Replace with your app password

subject = "Greetings from Your Script"
body = "Hello,\n\nThis is a test email sent using a Python script.\n\nBest regards,\nYour Script"
attachment_path = input("Enter the file path of the image you want to attach (or press Enter to skip): ").strip()

try:
    # Set up the SMTP server connection
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade to secure connection
        server.login(sender_email, app_password)  # Log in to the SMTP server

        for recipient_email in email_list:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Attach an image if provided
            if attachment_path:
                try:
                    with open(attachment_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split('/')[-1]}')
                        msg.attach(part)
                except Exception as e:
                    print(f"Could not attach file: {e}")

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email}")

except Exception as e:
    print(f"An error occurred while sending emails: {e}")

