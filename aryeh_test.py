import re
import sys

import os
from auditions import settings
# from django.core.management import setup_environ
# setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auditions.settings")
from auditions.models import *
from django.template import Context
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

all_callbackees = []
their_callbacks = []
#emails_sent
for callbackee in Callbackee.objects.filter(net_id='aryehnc'):
	print 'here'
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