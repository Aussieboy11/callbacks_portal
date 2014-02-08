from django.db import models



#group table
class Group(models.Model):
	name = models.CharField(max_length=40)
	selections_confirmed = models.NullBooleanField()
	acaprez = models.NullBooleanField()
	def __unicode__(self):
		return u"%s" % (self.group_name)

#callbackee
class Callbackee(models.Model):
	first_name = models.CharField(max_length = 23)
	last_name = models.CharField(max_length = 23)
	net_id = models.CharField(max_length = 23)
	first_callback_conflict = models.NullBooleanField()
	second_callback_conflict = models.NullBooleanField()
	third_callback_conflict = models.NullBooleanField()
	decisions_made = models.NullBooleanField()
	email_sent = models.NullBooleanField()
	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)

#callbacks
class Callbacks(models.Model):
	callbackee = models.ForeignKey(Callbackee)
	group = models.ForeignKey(Group)
	accepted = models.NullBooleanField()
	#maybe email sent successfully


#admin
#there must at all times be one site admin
class Admin(models.Model):
	first_name = models.CharField(max_length = 23)
	last_name = models.CharField(max_length = 23)
	net_id = models.CharField(max_length = 23)
	group = models.ForeignKey(Group)
	site_admin = models.NullBooleanField()
	def __unicode__(self):
		return u"%s %s" % (self.first_name, self.last_name)



#callback submission deadline
#group submission deadline
#callback times (first second third)
class Time_Utils(models.Model):
	key = models.TextField()
	value = models.DateField(null=True, blank=True)
#how to use datetime objects
#can you save datetime objects


