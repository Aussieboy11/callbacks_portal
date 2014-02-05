import re
import sys


from auditions import settings
from django.core.management import setup_environ
setup_environ(settings)
from auditions.models import *


#group_names = ['Roaring 20', 'the Katzenjammers', 'the Tigerlilies', 'the Tigressions', 'the Wildcats', 'the Tigertones', 'the Footnotes', 'the Nassoons']
group_names = ['the Nassoons']
admins = [('Yacob Yonas', 'yyonas', 'the Nassoons', True)]
callbackee = [()]


for group in group_names:
	new_group = Group(name=group, selections_confirmed=False)
	new_group.save()

for admin in admins:
	new_admin = Admin(first_name=admin[0].split()[0],
					last_name = admin[0].split()[1],
					net_id = admin[1],
					group = Group.objects.get(name=admin[2]),
					site_admin = admin[3])
	new_admin.save()

utils = ['group_deadline',
		'callbackee_deadline']

for util in utils:
	time_util = Time_Utils(key=util, value="1990-01-01")
	time_util.save()