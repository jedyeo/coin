import serial
import os
import xlsxwriter
import time
from gtts import gTTS
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


##########
# Serial port configuration
##########

ser = serial.Serial(
 port='COM8',
 baudrate=115200,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS
)
ser.isOpen()

##########
# Audio config
##########

welcome = gTTS('Lets go find coins', lang='en')
welcome.save("welcome.mp3")
os.system('welcome.mp3')
coinFound = gTTS('Coin collected', lang='en')
coinFound.save("coinfound.mp3")
perimeter = gTTS('Perimeter hit', lang='en')
perimeter.save("perimeter.mp3")
#os.system('coinfound.mp3')

###########
# .xlsx declarations
###########

# open a .xlsx
workbook=xlsxwriter.Workbook('demo.xlsx')
worksheet=workbook.add_worksheet()

# Formats
title = workbook.add_format({'bold': True, 'bg_color': '#7aadf9', 'border': 1})
datum = workbook.add_format({'bg_color': '#9ec4ff', 'border':1})

# Headings and format of headings
worksheet.write('A1', 'Coin (#)', title)
worksheet.write('B1', 'Time (s)', title)
worksheet.set_column('A:B',10)

##########
# Email stuff
##########

server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.starttls()
server.login( 'brandonbwanakocha@gmail.com', 'some_secret' )
def SendMail():
    msg = MIMEMultipart()
    msg['Subject'] = 'Coin Collection - Summary'
    msg['From'] = 'brandonbwanakocha@gmail.com'
    msg['To'] = 'brendonbk81@gmail.com'

    text = MIMEText("Dear Customer, \n\n Attached is a summary of the coin operation.")
    msg.attach(text)
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("demo.xlsx","rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="demo.xlsx"')
    msg.attach(part)
    thankyou = MIMEText("Thank you for your business.")
    msg.attach(thankyou)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('brandonbwanakocha@gmail.com', 'some_secret')
    s.sendmail('brandonbwanakocha@gmail.com', 'brendonbk81@gmail.com', msg.as_string())
    s.quit()

##########
# Arrays and Variables
##########

count = 0
n = []
data = []

##########
# Main Program
##########

print('Ready. t=0 is now')
start = int(time.time())

# Data collection loop
# For the real project, make time y var (int) and coin # x var (int)
# .readline() method waits for serial input
# coin_n.append(count) (coin #)
# t.append(int(time.time())-start)
while 1:
    garbage=int(ser.read().decode())
    if (garbage == 1):
        count+=1
        n.append(int(time.time())-start)
        data.append(count)
        print('Coin %s collected' % str(count))
        os.system("coinfound.mp3")
        if (count == 10):
            print('HALFWAY THERE')
            os.system("coinSong.mp3")
    if (garbage == 2):
        print('Perimeter hit')
        os.system("perimeter.mp3")
    if (count>=19):      # Change this for num of readings we expect
        break


# Write count and data
worksheet.write_column('B2', n)
worksheet.write_column('A2', data)

# Create new scatterplot object
sc = workbook.add_chart({'type': 'scatter'})

# Configure data :)
sc.add_series({
    'name':'=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$21',
    'values': '=Sheet1!$B$2:$B$21',
})

# Chart title, axes, and style
sc.set_title({'name': 'Coins Found (#) vs. Time (s)'})
sc.set_x_axis({'name': 'Coin (#)'})
sc.set_y_axis({'name': 'Time (s)'})
sc.set_style(11)

# Insert chart into worksheet
worksheet.insert_chart('D2', sc)

# Data processing complete
# Play done message
tts = gTTS('Coin collection done', lang='en')
tts.save("done.mp3")
time.sleep(5)
os.system('done.mp3')
os.system('rave.mp3')

#Fin
print('Data collection completed. Closing workbook.')
workbook.close()

SendMail()
