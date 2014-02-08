import re
import sys

import os
from auditions import settings
# from django.core.management import setup_environ
# setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auditions.settings")
from auditions.models import *
from django.template import Context


# #group_names = ['Roaring 20', 'the Katzenjammers', 'the Tigerlilies', 'the Tigressions', 'the Wildcats', 'the Tigertones', 'the Footnotes', 'the Nassoons']
# group_names = ['the Nassoons', 'the Tigertones']
# admins = [('Yacob Yonas', 'yyonas', 'the Nassoons', True),
# 			('Alan Southworth', 'asouthwo', 'the Tigertones', False),
# 			('Aryeh Nussbaum Cohen', 'aryehnc', 'the Tigertones', False)]
# callbackee = [()]


# for group in group_names:
# 	new_group = Group(name=group, selections_confirmed=False)
# 	new_group.save()

# for admin in admins:
# 	new_admin = Admin(first_name=admin[0].split()[0],
# 					last_name = admin[0].split()[1],
# 					net_id = admin[1],
# 					group = Group.objects.get(name=admin[2]),
# 					site_admin = admin[3])
# 	new_admin.save()

# utils = ['group_deadline',
# 		'callbackee_deadline']

# for util in utils:
# 	time_util = Time_Utils(key=util, value="1990-01-01")
# 	time_util.save()
all_callbackees = []
their_callbacks = []
#emails_sent
for callbackee in Callbackee.objects.filter(email_sent=False):
	all_callbackees.append(callbackee)
	current_callbacks = Callbacks.objects.filter(callbackee=callbackee)
	their_callbacks.append(current_callbacks)
zipped = zip(all_callbackees, their_callbacks)
# c = Context({'callbackee': existing_callbackee, 'group': Group.objects.get(name=datadict['group'])})    
# html_content = render_to_string('email_for_callbackee.html', c)

# email = EmailMultiAlternatives('yo', '')
# email.attach_alternative(html_content, "text/html")
# email.to = ['yyonas@princeton.edu']
# email.send()
for callbackee, callbacks in zipped:
	c = Context({'callbackee': callbackee, 'callbacks': callbacks})    
	html_content = render_to_string('email_for_callbackee.html', c)

	email = EmailMultiAlternatives('Callbacks from Acaprez', '')
	email.attach_alternative(html_content, "text/html")
	email_address = ''
	email_address += callbackee.net_id
	email_address += '@princeton.edu'
	email.to = [email_address]
	email.send()
	callbackee.email_sent = True
	callbackee.save()