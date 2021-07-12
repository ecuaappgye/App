from .models import BaseUser



def user_data(*, user)->BaseUser:
    return {
        "first_name":user.first_name
    }