#! python3

import requests, os, bs4, smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def xkcd_text():
    os.makedirs('xkcd', exist_ok=True)
    url = 'http://xkcd.com'
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
    return soup

def xkcd_img(soup):
    comicElem = soup.select('#comic img') 
    if comicElem == []:
        print('Could not find comic image.')
    else:
         comicUrl = 'http:' + comicElem[0].get('src')
         res = requests.get(comicUrl)
         res.raise_for_status()
         
         imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
         for chunk in res.iter_content(100000):
             imageFile.write(chunk)
         imageFile.close()

def img_path():
    files = os.listdir(path='xkcd')
    path = 'xkcd/' + files[0]
    return path

def email_img():
    email_send = ''
    email_pword = ''
    email_receive = ''
   
    img_data = open(img_path(), 'rb').read() 
    msg = MIMEMultipart()
    msg['Subject'] = 'Comic!'
    msg['From'] = email_send
    msg['To'] = email_receive
    msg.preamble = 'Comic!'
    image = MIMEImage(img_data, name=os.path.basename('comic'))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(email_send, email_pword)
    s.sendmail(email_send, email_receive, msg.as_string())
    s.quit()

def remove_img():
    path = img_path()
    os.remove(path)

xkcd_img(xkcd_text())
email_img()
remove_img()
