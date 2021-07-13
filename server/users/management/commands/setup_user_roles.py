from django.core.management.base import BaseCommand
from server.users.models import Rol



class Command(BaseCommand):
    """Command to init roles and data user
    """
    def handle(self, *args, **kwargs):
        roles = [
            {
                "name":"Conductor",
                "description":"Conductor"
            },
            {
                "name":"Cliente",
                "description":"Cliente"
            },
        ]

        instance=[]
        for e in roles:
            instance.append(
                Rol(name=e["name"], description=e["description"]))
        
        # Save roles object
        Rol.objects.bulk_create(instance)

