import email
import imaplib
import os
import smtplib
import time
import pyglet
import speech_recognition as sr
from bs4 import BeautifulSoup
from gtts import gTTS
from email.message import EmailMessage


#project name: Voice based Email for blind :.
# Author: Manya Mehta
def say(txt):
    tts = gTTS(text=txt, lang='en')
    ttsname = ("name.mp3")
    tts.save(ttsname)

    music = pyglet.media.load(ttsname, streaming=False)
    music.play()

    time.sleep(music.duration)
    os.remove(ttsname)

def listen(txt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(txt)
        audio = r.listen(source)
        print("ok done!!")

    try:
        text = r.recognize_google(audio)
        print("You said : " + text)
        return text

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    #fetch project name
say("Project: Voice based Email for blind")

#login from os
login = os.getlogin
print ("You are logging from : "+login())
msg = EmailMessage()
msg['From'] = 'sharmahimanshi1501@gmail.com'
id = 'sharmahimanshi1501@gmail.com'
pswrd = 'mahavirsharma'
username = 'sharmahimanshi1501@gmail.com'
password = 'mahavirsharma'

#choices
print ("1. composed a mail.")
say("option 1. composed a mail.")

print ("2. Check your inbox")
say("option 2. Check your inbox")

#this is for input choices
say("Your choice ")

#voice recognition part
text = listen("Your choice:")

#choices details
if text == '1' or text == 'One' or text == 'one':
    say("Your Subject: ")
    msg['Subject'] = listen("Your Subject: ")#recognize subject
    say("Your message: ")
    text1 = listen("Your message :")#recognize message
    msg.set_content(text1)
    msg['To'] = 'bhumikasaxena1@gmail.com'

    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)    #host and port area
    mail.login(username, password) #login part
    mail.send_message(msg) #send part
    print ("Congrates! Your mail has send. ")
    say("Congrates! Your mail has send. ")
    mail.close()   
    
if text == '2' or text == 'tu' or text == 'two' or text == 'Tu' or text == 'to' or text == 'To' :
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993) #this is host and port area.... ssl security
    mail.login(username, password)  #login
    stat, total = mail.select('Inbox')  #total number of mails in inbox
    total = str(total)
    print ("Number of mails in your inbox :"+str(total))
    say("Total mails are :"+str(total))
    
    #unseen mails
    unseen = mail.search(None, 'UnSeen') # unseen count
    print ("Number of UnSeen mails :"+str(unseen))
    say("Your Unseen mail :"+str(unseen))
    
    #search mails
    result, data = mail.uid('search', None, "ALL")
    inbox_item_list = data[0].split()
    mail_no = listen("Which mail do you want to fetch, please say the number")
    mail_no = listen("Please say the number")
    new = inbox_item_list[mail_no-1]
    old = inbox_item_list[0]
    result2, email_data = mail.uid('fetch', mail_no, '(RFC822)') #fetch
    raw_email = email_data[0][1].decode("utf-8") #decode
    email_message = email.message_from_string(raw_email)
    print ("From: "+email_message['From'])
    print ("Subject: "+str(email_message['Subject']))
    say("From: " + email_message['From'] + " And Your subject: " + str(email_message['Subject']))

    #Body part of mails
    stat, total1 = mail.select('Inbox')
    stat, data1 = mail.fetch(total1[0], "(UID BODY[TEXT])")
    msg = data1[0][1]
    soup = BeautifulSoup(msg, "html.parser")
    txt = soup.get_text()
    print ("Body :"+txt)
    say("Body: "+txt)
    mail.close()
    mail.logout()
