import requests
import json
import random
import string
import datetime
import time

host = 'http://165.232.121.216/'
headers={'Content-type':'application/json', 'Accept':'application/json'}
project_names = [
    'Bears',
    'Bengals',
    'Bills',
    'Broncos',
    'Browns',
    'Buccaneers',
    'Cardinals',
    'Chargers',
    'Chiefs',
    'Colts',
    'Cowboys',
    'Dolphins',
    'Eagles',
    'Falcons',
    'Giants',
    'Jaguars',
    'Jets',
    'Lions',
    'Packers',
    'Panthers',
    'Patriots',
    'Raiders',
    'Rams',
    'Ravens',
    'Redskins',
    'Saints',
    'Seahawks',
    'Steelers',
    'Titans',
    'Vikings',
    'Hawks',
    'Celtics',
    'Hornets',
    'Bulls',
    'Cavaliers',
    'Mavericks',
    'Nuggets',
    'Pistons',
    'Warriors',
    'Rockets',
    'Pacers',
    'Clippers',
    'Lakers',
    'Heat',
    'Bucks',
    'Timberwolves',
    'Nets',
    'Knicks',
    'Magic',
    '76ers',
    'Suns',
    'Blazers',
    'Kings',
    'Spurs',
    'Supersonics',
    'Raptors',
    'Jazz',
    'Grizzlies',
    'Wizards',
	"DEADBEEF",
	"hackslash",
	"SQL Injectors",
	"Hexspeak",
	"The Brogrammers",
	"Bits Please",
	"SaaStar",
	"White Hats",
	"Did It All for the Cookies",
	"Bro Code",
	"Bug Squashers",
	"Hash it Out",
	"Trojan Horses",
	"Reboot Rebels",
	"Cyber Creepers",
	"Access Denied",
	"Brewing Java",
	"IllegalSkillsException",
    "Bug Squashers",
    "Hash it Out",
    "Google is my brain",
    "Division By Zero",
    "Making Waves",
    "Cyber tech squad",
    "Ambliguity",
    "Brains in Jars",
    "Enigma",
    "Masterminds",
    "Incognito",
    "Recursion",
    "Hello World",
    "Let us Code",
    "CodeBreakers",
    "Tech-Knights",
    "Require",
    "Heisenbug",
    "Ciphers",
    "Locus",
    "Pivot",
    "Deep Mind",
    "Blitzkrieg",
    "Terabyte",
    "Bits and Bytes",
    "qwerty",
    "Complexity",
    "Yoda",
    "NP COMPLETE",
    "Sandbox",
    "Fuzzy Logic"
]


class User:    
    def __init__(self, user_id, email, pwd):
        self.id = user_id
        self.email = email
        self.pwd = pwd

def get_random_string():
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(8))
    return result

def create_user():
    url = host+'api/auth/register/'
    email =  get_random_string()+'@gmail.com'
    pwd = get_random_string()
    data = {
        "first_name": get_random_string(),
        "last_name": get_random_string(),
        "email": email,
        "role": random.randint(1, 9),
        "password": pwd,
        "password2": pwd,
    }
    r = requests.post(url, json=data, headers=headers)
    print(r.status_code)
    
    data = json.loads(r.text)
    return User(data['id'], email, pwd)

users = [create_user() for i in range(10)]

def get_token(user):
    content = {
        "email": user.email,
        "password": user.pwd
    }
    url=host+'api/auth/token/'
    response = requests.post(url, json=content, headers=headers)
    data = json.loads(response.text)
    return data['token']

def random_date():
    d = random.randint(1, int(time.time()))
    return datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')

# def create_date():
    # start_dt = datetime.date(2007, 1, 1).toordinal()
    # end_dt = datetime.date(1998, 1, 1).toordinal()
    # return datetime.date.fromordinal(random.randint(end_dt, start_dt)).strftime("%Y-%m-%d")

for user in users:
    headers.update({"Authorization": "Bearer {}".format(get_token(user))})
    url = host + 'main/projects/create/'
    data = {
        'name': project_names.pop(random.randrange(len(project_names))),
        'users': [{
            'user': u.id,
            'role': random.randint(1, 9),
        } for u in users if u.email != user.email],
        'project_type': random.randint(1, 3),
        'date_start': random_date(),
        'date_end': random_date()
    }
    r = requests.post(url, json=data, headers=headers)
    print(r.text)
    if r.status_code == 500:
        break

