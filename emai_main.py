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

email_dict = dict()

facebook_dict = dict()

for i in range(len(list(cities["Email"]))):
    email = cities["Email"][i]
    email_strip = str(email).strip()
    cities["Email"][i] = email_strip

for i in range(len(list(cities["Email"]))):
    email_dict[str(cities["What is your full name?"][i]).strip().lower()] = str(cities["Email"][i]).strip()

for i in range(len(list(cities["Is your facebook profile the same as your name?"]))):
    if str(cities["Is your facebook profile the same as your name?"][i]).strip().lower() == "yes":
        facebook_dict[str(cities["What is your full name?"][i]).strip().lower()] = \
            str(cities["What is your full name?"][i]).strip()
    else:
        facebook_dict[str(cities["What is your full name?"][i]).strip().lower()] \
            = str(cities["If not, what is your facebook profile name? (so matches can DM you)"][i]).strip()

print(cities["What is your full name?"])
print(cities["Email"])

print(email_dict)

print(facebook_dict)

match_list = []
with open("//Gaby's Matches.txt", mode='r', encoding='utf-8') as contacts_file:
    for a_contact in contacts_file:
        match_list.append(str(a_contact).split(" and "))

for i in range(len(match_list)):
    for j in range(len(match_list[i])):
        match_list[i][j] = match_list[i][j].replace("\ufeff", "").replace("\n", "").strip().lower()
#match_list.pop()

print(match_list)

message_list = []

message_object_list = []

for i in range(len(match_list)):
    try:
        for j in range(2):

            s = smtplib.SMTP(host='smtp.gmail.com', port=587)

            s.starttls()

            s.login(MY_ADDRESS, PASSWORD)

            with open("//Email Template.txt", 'r', encoding='utf-8') as template_file:
                template_file_content = template_file.read()

                email_text = Template(template_file_content)

                msg = MIMEMultipart()

                try:
                    message = email_text.substitute(PERSON1_NAME = toName(match_list[i][j]),
                                            PERSON2_NAME = toName(match_list[i][j+1]),
                                        PERSON2_FACEBOOK = facebook_dict[match_list[i][j+1]],
                                            PERSON2_EMAIL = email_dict[match_list[i][j+1]])
                except:
                    #traceback.print_exc()
                    message = email_text.substitute(PERSON1_NAME = toName(match_list[i][j]),
                                            PERSON2_NAME = toName(match_list[i][j - 1]),
                                            PERSON2_FACEBOOK = facebook_dict[match_list[i][j - 1]],
                                            PERSON2_EMAIL = email_dict[match_list[i][j - 1]])

                message_list.append(message)
#message = email_text.substitute(PERSON2_NAME="Jordan Simkovic")

#message = email_text.substitute(PERSON2_FACEBOOK="Jordan Simkovic")

#message = email_text.substitute(PERSON2_EMAIL="Jordan.Simkovic15@gmail.com")

#    print(message)

                msg['From'] = MY_ADDRESS
                msg['To'] = email_dict[match_list[i][j]]
                msg['Subject'] = "Your Matches Courtesy of the Frummers Only Team!"

    # add in the message body
                msg.attach(MIMEText(message, 'plain'))

                message_object_list.append(msg)

                s.send_message(msg)
                del msg

                s.quit()

    except:
        traceback.print_exc()
        continue

    # send the message via the server set up earlier.


    # Terminate the SMTP session and close the connection



for i in range(len(message_list)):
    message_list[i] = message_list[i].replace("\ufeff", "").replace("\n", "").strip()

print(message_list)

message_list_string = ""

for message in message_list:
    message_list_string += message + "\n"

print(message_list_string)

match_list_string = ""
for match in match_list:
    match_list_string += str(match) + "\n"

print(match_list_string)

#truth_list = []
#for msg in message_object_list:
#    for part in msg.walk():
#        if part.get_content_type() == 'text/plain':
#            print(part.get_payload(None, True))

with open("./test.txt", "w") as f:
    for msg in message_object_list:
        f.write("From: " + msg["from"] + "\n")
        f.write("To: " + msg["to"] + "\n")
        f.write("Subject: " + msg["subject"] + "\n")
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                f.write("Body:\n" + str(part.get_payload(None, True)) + "\n")
        f.write("-----------------------------------------------\n")
