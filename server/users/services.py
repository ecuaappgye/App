from server.users.selectors import user_by_id
from .models import BaseUser


def user_create(*,
    first_name,
    last_name, 
    email, 
    password)->BaseUser:
    
    user = BaseUser.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    return user

def user_update_profile(*, user_id:int, data)->BaseUser:
    user = user_by_id(id=user_id)
    return user

