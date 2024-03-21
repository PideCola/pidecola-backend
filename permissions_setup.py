from django.contrib.auth.models import Group, Permission
from permissions_settings import admin_permissions, driver_permissions, user_permissions

ADMIN = 'admin'
USER = 'user'
DRIVER = 'driver'

g = None

if Group.objects.filter(name=ADMIN).exists():
    g = Group.objects.get(name=ADMIN)
else:
    g = Group(name=ADMIN)
    g.save()


permissions = [Permission.objects.get(codename=p) for p in admin_permissions]
g.permissions.add(*permissions)
g.save()

if Group.objects.filter(name=USER).exists():
    g = Group.objects.get(name=USER)
else:
    g = Group(name=USER)
    g.save()


permissions = [Permission.objects.get(codename=p) for p in user_permissions]
g.permissions.add(*permissions)
g.save()

if Group.objects.filter(name=DRIVER).exists():
    g = Group.objects.get(name=DRIVER)
else:
    g = Group(name=DRIVER)
    g.save()


permissions = [Permission.objects.get(codename=p) for p in driver_permissions]
g.permissions.add(*permissions)
g.save()
