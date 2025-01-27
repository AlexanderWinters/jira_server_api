import os
import csv
import smtplib
from email.mime.text import MIMEText


file = input("Enter file name: ")
delimiter = ";"
smtp_server = "<smtp server address>"
login = "<login>"
password = "<password>"
fromaddr = "<from address>"

with open(file) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=delimiter)
    for row in reader:
        name = row['displayName']
        key = row['password']
        email = row['emailAddress']

        text = "Username: " + name + "\nPassword: " + key

        message = MIMEText(text, "plain")
        message["Subject"] = "subject"
        message["From"] = fromaddr
        message["To"] = email

        # Send the email
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()  # Secure the connection
            server.login(login, password)
            server.sendmail(fromaddr, email, message.as_string())

