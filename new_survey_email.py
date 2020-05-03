import inspect
import traceback

import pandas
import xlrd
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import colorama
from colorama import Fore, Style

def toName(name_lower):
    name_lower_list = name_lower.split(" ")
    name_upper = ""
    for nm in name_lower_list:
        name_upper += nm.capitalize() + " "
    return name_upper.strip()

MY_ADDRESS = 'frummerscadre@gmail.com'
PASSWORD = ''

file_name = '//Frummers Only Shadchan (Responses).xlsx'
travel_df = pandas.read_excel(file_name)
cities = travel_df.to_dict()
print(cities.keys())
print(cities["What is your full name?"])
print(cities["Email"])


email_dict = dict()

facebook_dict = dict()

for i in range(len(list(cities["Email"]))):
    email = cities["Email"][i]
    email_strip = str(email).strip()
    cities["Email"][i] = email_strip

for i in range(len(list(cities["Email"]))):
    email_dict[str(cities["What is your full name?"][i]).strip().lower()] = str(cities["Email"][i]).strip()

message_object_list = []

s = smtplib.SMTP(host='smtp.gmail.com', port=587)

s.set_debuglevel(1)

s.starttls()

s.login(MY_ADDRESS, PASSWORD)

for i in range(78, 150):

    try:

        with open("//new_survey_email_template.txt", 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()

            email_text = Template(template_file_content)

            msg = MIMEMultipart()

            message = email_text.substitute(PERSON1_NAME = cities["What is your full name?"][i])

            msg['From'] = MY_ADDRESS
            msg['To'] = cities["Email"][i]
            msg['Subject'] = "Thank You and Feedback Form Available Now!"

            msg.attach(MIMEText(message, 'plain'))

            message_object_list.append(msg)

            s.send_message(msg)

            del msg

    except:
        traceback.print_exc()
        continue

s.quit()

with open("//new_survey_email_test.txt", "w") as f:
    for msg in message_object_list:
        f.write("From: " + msg["from"] + "\n")
        f.write("To: " + msg["to"] + "\n")
        f.write("Subject: " + msg["subject"] + "\n")
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                f.write("Body:\n" + str(part.get_payload(None, True)) + "\n")
        f.write("-----------------------------------------------\n")