from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import models
from auditions.models import *
from django.template.loader import get_template
from django.http import QueryDict
from django.template import Context, loader, RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.utils import simplejson
import urllib
import re
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import os

# send_mail('Your callback', 'Here is the message.', settings.EMAIL_HOST_USER,
#     ['to@example.com'], fail_silently=False)

MAX_NUM_CALLBACKS = 20
DEBUG = False


	# if not settings.DEBUG:
	# 	try: # ADDED TRY HERE... ORIGINAL IN WHAT IS GOING ON... SEEMED TO FIX IT. 1 of 1           
	# 		n = request.session['netid']  
	# 		if request.session['netid'] is None:
	# 			return check_login(request, '/')
	# 	except:
	# 		return check_login(request, '/')
	# 	netid = request.session['netid']
	# else:
	# 	netid = 'dev'

##what about a home page that will map you to the right page for you



# Adapted from Luke Paulsen's code.
def check_login(request, redirect):
	cas_url = "https://fed.princeton.edu/cas/"
	service_url = 'http://' + urllib.quote(request.META['HTTP_HOST'] + request.META['PATH_INFO'])
	service_url = re.sub(r'ticket=[^&]*&?', '', service_url)
	service_url = re.sub(r'\?&?$|&$', '', service_url)
	if "ticket" in request.GET:
		val_url = cas_url + "validate?service=" + service_url + '&ticket=' + urllib.quote(request.GET['ticket'])
		r = urllib.urlopen(val_url).readlines() #returns 2 lines
		if len(r) == 2 and re.match("yes", r[0]) != None:
			request.session['netid'] = r[1].strip()
			return HttpResponseRedirect(redirect)
		else:
			return HttpResponse("FAILURE")
	else:
		login_url = cas_url + 'login?service=' + service_url
		return HttpResponseRedirect(login_url)


def logout(request):
	request.session['netid'] = None
	return HttpResponseRedirect("https://fed.princeton.edu/cas/logout")


##FIX DUPLICATE NETID ENTRIES

def add_remove_callbackee(request):
	#first,last, net_id, add=1 for add, remove=0, group
	data = request.POST
	datadict = data.dict()
	#acces dict with datadict['object name']
	error = False
	delete_not_found = False

	#MAKE SURE TO CHECK THAT YOU ARE A VALID USER
	try:
		if request.session['netid'] is None:
			return check_login(request, '/group_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/group_admin')
	admin = Admin.objects.filter(net_id=netid)
	if len(admin) is 0:
		print admin
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	admin = admin[0]



	if (datadict['add']=='1'):
		#add
		blah = 4
		#look for existing?
		try:
			existing_callbackee = Callbackee.objects.get(net_id = datadict['net_id'])	
			print "in try"
		except:
			new_callbackee_entry = Callbackee(first_name=datadict['first'],
								last_name=datadict['last'],
								net_id = datadict['net_id'],
								decisions_made = False,
								email_sent = False
								)
			new_callbackee_entry.save()
			existing_callbackee = new_callbackee_entry
			print "in exception"
		if (len(Callbacks.objects.filter(group = Group.objects.get(name=datadict['group']))) >= MAX_NUM_CALLBACKS):
			error = True
			pass
		#look for existing

		#DONT ADD CALLBACK IF ONE ALREADY EXISTS
		existing_callbacks = Callbacks.objects.filter(callbackee=existing_callbackee,
							group = Group.objects.get(name=datadict['group']))
		if len(existing_callbacks) is not 0:
			error = True
			pass
		new_callback_entry = Callbacks(callbackee=existing_callbackee,
										group = Group.objects.get(name=datadict['group']),
										accepted = None)
		new_callback_entry.save()
	else:
		#remove
		blah = 4
		try:
			existing_callbackee = Callbackee.objects.get(net_id = datadict['net_id'])	
		except:
			error = True
			delete_not_found = True
		if error is False:
			existing_callbackee.delete()



	#things to send back, submission confirmed?, reason? too many, duplicate
	#return HttpResponse("haha")
	#talk about common errors
	to_json = {}
	to_json['error_bool'] = error
	to_json['delete_not_found'] = delete_not_found
	# c = Context({'callbackee': existing_callbackee, 'group': Group.objects.get(name=datadict['group'])})    
	# html_content = render_to_string('email_for_callbackee.html', c)

	# email = EmailMultiAlternatives('yo', '')
	# email.attach_alternative(html_content, "text/html")
	# email.to = ['yyonas@princeton.edu']
	# email.send()
	return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')

def group_admin(request):
	#things to know
	#user name
	#get group from that
	#get list of current callbacks

	##IF THEY ALRADY CONFIRMED SELECTION
	##THEN THEY SHOULD GO RIGHT TO VIEW THEIR RESULTS
	try:
		if request.session['netid'] is None:
			return check_login(request, '/group_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/group_admin')
	admin = Admin.objects.filter(net_id=netid)

	if len(admin) is 0:
		print admin
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	admin = admin[0]
	if (admin.group.selections_confirmed == True):
		return HttpResponseRedirect('/group_results')
	c={}
	c['admin'] = admin
	existing = Callbacks.objects.filter(group = admin.group)
	t = get_template("group_admin_page.html")
	c['existing'] = existing
	c.update(csrf(request))
    # ... view code here
	return render_to_response("group_admin_page.html", c)

def callbackee_make_selections(request):
	#things to know
	#user name
	try:
		if request.session['netid'] is None:
			return check_login(request, '/make_selections')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/make_selections')
	callbackee = Callbackee.objects.filter(net_id=netid)
	c = {}
	c['user'] = callbackee[0]
	if len(callbackee) is 0:
		#no callbackee with this name
		return render_to_response("callbackee_error.html", c)
	##THIS ASSUMES THAT WE ALWAYS MAKE SURE THAT  A NETID
	##CAN ONLY APPEAR ONCE
	callbackee = callbackee[0]
	callbacks = Callbacks.objects.filter(callbackee=callbackee)
	if callbackee.decisions_made is True:
		return callbackee_view_selections(request)
	c['callbacks'] = callbacks
	c['netid'] = netid
	#non-acaprez callbacks
	non_acaprez_callbacks = Callbacks.objects.filter(callbackee=callbackee, group__acaprez=False)
	c['non_acaprez_callbacks'] = non_acaprez_callbacks
	print(len(non_acaprez_callbacks))
	c.update(csrf(request))
	return render_to_response("callbackee_make_selections.html", c)

def callbackee_save_selections(request):

	##check if it is too late to make the changes

	# netid = getNetID(request)
	try:
		if request.session['netid'] is None:
			return check_login(request, '/make_selections')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/make_selections')
	callbackee = Callbackee.objects.filter(net_id=netid)
	c = {}
	if len(callbackee) is 0:
		#no callbackee with this name
		return render_to_response("callbackee_error.html", c)
	##THIS ASSUMES THAT WE ALWAYS MAKE SURE THAT  A NETID
	##CAN ONLY APPEAR ONCE
	callbackee = callbackee[0]
	data = request.GET
	datadict = data.dict()
	#save choices to a set
	groups_chosen = set()
	groups_chosen.add(datadict['first_choice'])
	groups_chosen.add(datadict['second_choice'])
	if (datadict['non_acaprez_choice'] != 'None'):
		groups_chosen.add(datadict['non_acaprez_choice'])
	callbacks = Callbacks.objects.filter(callbackee=callbackee)
	for callback in callbacks:
		if callback.group.name in groups_chosen:
			callback.accepted = True
			callback.save()
		else:
			callback.accepted = False
			callback.save()

	##also do conflicts here

	if ('conflict_with_first' in datadict.keys()):
		callbackee.first_callback_conflict = True
	else:
		callbackee.first_callback_conflict = False

	if ('conflict_with_second' in datadict.keys()):
		callbackee.second_callback_conflict = True
	else:
		callbackee.second_callback_conflict = False

	if ('conflict_with_third' in datadict.keys()):
		callbackee.third_callback_conflict = True
	else:
		callbackee.third_callback_conflict = False
	callbackee.decisions_made = True
	callbackee.save()
	return HttpResponseRedirect('/view_selections')

def callbackee_view_selections(request):
	#should have the ability to go modify changes if the time isn't too late
	# netid = getNetID(request)
	try:
		if request.session['netid'] is None:
			return check_login(request, '/view_selections')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/view_selections')
	callbackee = Callbackee.objects.filter(net_id=netid)
	c = {}
	print netid
	if len(callbackee) is 0:
		print callbackee
		#no callbackee with this name
		return render_to_response("callbackee_error.html", c)
	##THIS ASSUMES THAT WE ALWAYS MAKE SURE THAT  A NETID
	##CAN ONLY APPEAR ONCE
	callbackee = callbackee[0]
	accepted = Callbacks.objects.filter(callbackee=callbackee, accepted=True)
	rejected = Callbacks.objects.filter(callbackee=callbackee, accepted=False)
	decisions_made = callbackee.decisions_made
	c = {}
	c['user'] = callbackee
	c['accepted'] = accepted
	c['rejected'] = rejected
	c['decisions_made'] = decisions_made
	return render_to_response("callbackee_view_selections.html", c)


def confirm_groups_selections(request):
	try:
		if request.session['netid'] is None:
			return check_login(request, '/group_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/group_admin')
	admin = Admin.objects.filter(net_id=netid)
	if len(admin) is 0:
		print admin
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	admin = admin[0]
	if (admin.group.selections_confirmed is True):
		##here we need to render our page that talks about
		##all of the callbacks they have given
		pass
	data = request.GET
	datadict = data.dict()
	group = admin.group
	group.selections_confirmed = True
	group.save()
	return HttpResponseRedirect('/group_results')

def send_callbackee_emails(request):
	try:
		if request.session['netid'] is None:
			return check_login(request, '/site_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/site_admin')
	admin = Admin.objects.filter(net_id=netid, site_admin=True)
	if len(admin) is 0:
		print admin
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	admin = admin[0]
	#zip together callbackee with every group they got called back to
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
	return HttpResponseRedirect('/site_admin')


def site_admin(request):
	try:
		if request.session['netid'] is None:
			return check_login(request, '/site_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/site_admin')
	admin = Admin.objects.filter(net_id=netid, site_admin=True)
	if len(admin) is 0:
		print admin
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	groups = Group.objects.all()
	admin = admin[0]
	c = {}
	c.update(csrf(request))
	c['groups'] = groups
	#find out if every group has successfully confirmed
	groups_not_confirmed = Group.objects.filter(selections_confirmed=False)
	if (len(groups_not_confirmed) == 0):
		all_groups_confirmed = True
	else:
		all_groups_confirmed = False
	c['all_groups_confirmed'] = all_groups_confirmed
	callbackees_not_emailed = Callbackee.objects.filter(email_sent=False)
	if (len(callbackees_not_emailed) == 0):
		all_emails_sent = True
	else:
		all_emails_sent = False
	c['all_emails_sent'] = all_emails_sent
	c['admin'] = admin
	return render_to_response('site_admin.html', c)

def view_groups_results(request):
	try:
		if request.session['netid'] is None:
			return check_login(request, '/site_admin')
	
		netid = request.session['netid']
	except:
		return check_login(request, '/site_admin')
	admin = Admin.objects.filter(net_id=netid)
	if len(admin) is 0:
		#no callbackee with this name
		return render_to_response("group_admin_error.html")
	admin = admin[0]
	c = {}
	c['admin'] = admin
	##accepted, rejected, question marks
	callbacks_accepted = Callbacks.objects.filter(group=admin.group,
												accepted=True)
	c['callbacks_accepted'] = callbacks_accepted
	callbacks_rejected = Callbacks.objects.filter(group=admin.group,
												accepted = False)
	c['callbacks_rejected'] = callbacks_rejected
	callbacks_questioning = Callbacks.objects.filter(group=admin.group,
												accepted=None)
	c['callbacks_questioning'] = callbacks_questioning
	return render_to_response('group_results.html', c)








