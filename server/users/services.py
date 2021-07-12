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