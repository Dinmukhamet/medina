import jwt
import time
import threading
import re
from django.core.mail import send_mail
from hub.settings import SECRET_KEY


def generate_token(email):
    exp = int(time.time()) + 60 * 5
    return jwt.encode({'email': email, 'exp': exp}, SECRET_KEY, algorithm='HS256')


def special_match(strg, search=re.compile(r'[^A-zА-я ]').search):
    return not bool(search(strg))



def run_in_thread(fn):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
    return run


@run_in_thread
def send_email(subject, from_email, email_to, message, request=None):
    send_mail(subject, message, from_email, [email_to])