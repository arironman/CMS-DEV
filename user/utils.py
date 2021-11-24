from CMS.variables import *
from user.models import CustomUser as User


def get_input_field(field, url_keyword, field_type, options=None):
    '''
        Return the update input field according to input type\n
        input type - [text, dropdown]
    '''
    if field_type == 'text':
        input_field = f'<input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data">'

    elif field_type == 'dropdown':
        input_field = f'<input type="text" class="form-control" id="new-{url_keyword}" placeholder="New {field}" name="data">'

    return input_field



def check_valid_username(username):
    '''
        return True if the username is valid\n
        return False if the username is invalid
    '''
    avaibile_obj = User.objects.filter(username=username).exists()
    if avaibile_obj:
        return False
    else:
        if ' ' in username or username in NON_USERNAME_WORDS:
            # for handling spaces and non username words
            return False
        else:
            return True


def check_valid_email(email):
    '''
        Return True if the email is valid and available otherwise return False
    '''
    avaibile_obj = User.objects.filter(email=email).exists()
    if avaibile_obj:
        return False
    else:
        if ' ' in email or '@' not in email:
            # for handling spaces and non username words
            return False
        else:
            return True


def verification_email(email):
    '''
        used in update email to verify the email
    '''
    pass


def send_otp(email):
    '''
        used in update email to generate and send the otp to given mail
    '''
    pass
