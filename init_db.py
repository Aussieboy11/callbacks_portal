import re
import sys

import os
from auditions import settings
# from django.core.management import setup_environ
# setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auditions.settings")
from auditions.models import *


#group_names = ['Roaring 20', 'the Katzenjammers', 'the Tigerlilies', 'the Tigressions', 'the Wildcats', 'the Tigertones', 'the Footnotes', 'the Nassoons']
group_names = ['the Nassoons', 
			'Roaring 20', 
			'the Tigertones', 
			'the Katzenjammers', 
			'the Wildcats',
			'the Footnotes',
			'the Tigerlilies',
			'the Tigressions',
			'Old NasSoul',
			'Shere Khan']

admins = [('Yacob Yonas', 'yyonas', 'the Nassoons', True),
			('Joel Simwinga', 'simwinga', 'the Tigertones', False),
			('Abigail Kelly', 'amkelly', 'the Katzenjammers', False),
			('Rachel Klebanov', 'rachelhk', 'the Wildcats', False),
			('Ryan Fauber', 'rfauber', 'the Footnotes', False),
			('Brian Lax', 'blax', 'Roaring 20', False),
			('Sonia Skoularikis', 'sskoular', 'the Tigressions', False),
			('David Li', 'heli', 'Old NasSoul', False),
			('Elizabeth Banes', 'ebanes', 'the Tigerlilies', False),
			('Christopher Kranenburg', 'ckranenb', 'Shere Khan', False)]
callbackee = [()]


# for group in group_names:
# 	new_group = Group(name=group, selections_confirmed=False)
# 	new_group.save()

for num in range(8):
	new_group = Group(name=group_names[num], selections_confirmed=False, acaprez=True)
	new_group.save()

new_group = Group(name=group_names[8], selections_confirmed=False, acaprez=False)
new_group.save()

new_group = Group(name=group_names[9], selections_confirmed=False, acaprez=False)
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