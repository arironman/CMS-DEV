
CARD_COUNT = 5
BASE_URL = 'http://127.0.0.1:8000/'
# sign up
AUTH_URL_PREFIX = f'{BASE_URL}/auth-code/'
AUTH_MAIL_SUBJECT = 'Activate your Courier Delivery Management account.'

# forgot password
FG_PASSWORD_URL_PREFIX = f'{BASE_URL}/forgot-password/'
FG_PASSWORD_MAIL_SUBJECT = 'Re-Set your CMS account password.'

# new email verification
VERIFY_EMAIL_URL_PREFIX = f'{BASE_URL}/update/'
VERIFY_MAIL_SUBJECT = 'CMS Email Verification.'

ADMINS = [ 'CMS', 'anurag']

NON_USERNAME_WORDS = ['home', 'about-us', 'login', 'contact', 'logout', 'google-auth', 'forgot-password', 'username']


DOMAIN_NAME = 'ar.com'

# functions

# manage the page and next in url
def next_url(url, next='next=/'):
    if '?' in url:
        return url+'&'+next 
    else:
        return url+'?'+next

