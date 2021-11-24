from user.models import CustomUser as User

# this method return the auth details
def auth_details(request):
    auth = request.user.is_authenticated

    params = {
        'auth':auth,
        }

    if auth:
        # fetching user data
        user = request.user

        params['user'] = user
    # params['auth'] = True
    return params
