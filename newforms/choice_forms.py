from django.utils.safestring import mark_safe
from django import forms

DATA_CLASSIFICATION = (('Cat 1','Cat 1'),('Cat 2','Cat 2'),
	('Cat 3','Cat 3'),('Unsure','Unsure'))
DEV_ENVIRONMENT = (('UTdirect','UTdirect'), ('Pype','Pype'), 
	('Java','Java'), ('3rd Party','3rd Party'))
DEVELOPMENT_ENVIRONMENT = (('Production','Production'),
	('Development','Development'), ('Testing','Testing'))
READY_TO_SCAN = (('Yes','Yes'), ('No','No'), ('Not Sure','Not Sure'))
YES_NO = (('Yes','Yes'),('No','No'))
FORM_CHOICES = (('Application','Application'),('Servers','Servers'),
	('Unit','Unit'),('Physical','Physical'),('Other','Other'))
ACCEPTANCE = (('I Agree', 'I Agree'),('I Disagree', 'I Disagree'))

class ChoiceForm(forms.Form):
	choices = forms.ChoiceField(widget=forms.RadioSelect, choices = FORM_CHOICES, required=True,
		label='Please select the which of the following choices best matches the type of Engagement Request you are seeking',)


class ApplicationForm(forms.Form):
	url = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}), required=False)
	credentials = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Credentials - priviledged and non-priviledged", required=False)
	data_classification = forms.ChoiceField(choices = DATA_CLASSIFICATION)
	dev_environment = forms.ChoiceField(
		choices = DEV_ENVIRONMENT, label="Development Environment", required=False)
	links = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Link(s) to Blacklist", required=False)
	auto_emails = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Automated email(s)", required=False)
	batch_files = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Batch file(s)", required=False)
	notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		required=False)
	timeline = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Timeline / Urgency")


class ServersForm(forms.Form):
	hostnames = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	credentials = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Credentials - priviledged and non-priviledged", required=False)
	certificates = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	os = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Operating System(s)")
	data_classification = forms.ChoiceField(choices = DATA_CLASSIFICATION, required=False)
	dev_environment = forms.ChoiceField( choices = DEVELOPMENT_ENVIRONMENT,
		label="Development Environment", required=False)
	notes = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		required=False)
	timeline = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		required=False)
	ready_to_scan = forms.ChoiceField(choices = READY_TO_SCAN, required=False)


class UnitForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	dep_head_eid = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Department Head / Sponsor EID")
	timeline = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Timeline / Urgency")


class PhysicalForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	timeline = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	location = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	time = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	when_to_meet = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))


class OtherForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
	timeline = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))


class SecurityExceptionReportForm(forms.Form):
	standard = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}), 
		label="Standard/Policy/Guideline for which an exception is being reported")
	noncompliance = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Describe the non-compliance")
	justify_noncompliance = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Briefly justify the non-compliance")
	data = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Data, departments and customers that might be put at risk by the exception")
	assessment = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Provide an assessment of the risk associated with non-compliance")
	manage = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Describe what is being done to mitigate (manage) risk")
	metrics = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Provide metrics to evaluate the success of risk management")
	school = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="The college, school, or unit which initially reported the exception")
	systems = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="List the system(s) by MAC address (include both wired and wireless interfaces) associated with this report")
	data_classification = forms.ChoiceField(choices = DATA_CLASSIFICATION)
	duration = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label="Anticipated duration for the exception")
	eid = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label=mark_safe('EID for approving <a href="http://www.utexas.edu/its/glossary/iso#GL_Owner">IT owner</a> (for example, the IT Manager or Department Head)'))

# ****************************************************************************
# START OF CUSTOM MAC ADDRESS FORM FIELD
# ****************************************************************************
class MacAddressWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput()] * 6 
        super(MacAddressWidget, self).__init__(widgets, attrs)
        
    def format_output(self, widgets):
        return mark_safe(' : '.join(widgets)+' ')
        
    def decompress(self, value):
        if value:
            return value
        return ''


class MacAddressField(forms.MultiValueField):
    widget = MacAddressWidget( attrs={'size':2})
    
    def __init__(self, *args, **kwargs):
        fields = [forms.CharField(label='') ] * 6
        super(MacAddressField, self).__init__(fields, *args, **kwargs)
    
    def compress(self, value):
        if value:
            return ':'.join(value)
        return ''
# ****************************************************************************
# END OF CUSTOM MAC ADDRESS FORM FIELD 
# ****************************************************************************

# ****************************************************************************
# START OF CUSTOM TIME FORM FIELD
# ****************************************************************************
class TimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput()] * 3 
        super(TimeWidget, self).__init__(widgets, attrs)
        
    def format_output(self, widgets):
        return mark_safe(' / '.join(widgets)+' ')
        
    def decompress(self, value):
        if value:
            return value
        return ''


class TimeField(forms.MultiValueField):
    widget = TimeWidget( attrs={'size':2})
    
    def __init__(self, *args, **kwargs):
        fields = [forms.CharField(label='') ] * 3
        super(TimeField, self).__init__(fields, *args, **kwargs)
    
    def compress(self, value):
        if value:
            return '/'.join(value)
        return ''
# ****************************************************************************
# END OF CUSTOM TIME FORM FIELD 
# ****************************************************************************


class StolenEquipmentNotificationForm(forms.Form):
	callback = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label='Call Back Number - where you want to be contacted about this report. ')
	casenumber = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label='Law Enforcement Case Number (if available)')
	description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label='Device Description (include UT asset tag number, if applicable)')
	wired_mac = MacAddressField(required=False,
		label='Wired MAC Address (e.g., 00:14:13:ed:54:43) - This field is not required but it will be very helpful.')
	wireless_mac = MacAddressField(required=False,
		label='Wireless MAC Address (e.g., 00:14:13:ed:54:43) - This field is not required but it will be very helpful.')
	date = TimeField(required=False,
		label='Last date the device was connected to the UT network (wired or wireless): (MM/DD/YYYY)')
	location = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label='Location/Building where device was stolen')
	eid = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
		label='EID of Primary User of Device')
	is_cat_1 = forms.ChoiceField( choices = YES_NO,
		label="Is there Category-I data stored on this device?")
	encrypted = forms.ChoiceField( choices = YES_NO,
		label="Is the data on this device encrypted?")


class SpecialTrustForm(forms.Form):
	# eid = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}),
	# 	label= 'hello')
	acceptance = forms.ChoiceField(widget=forms.RadioSelect, choices = ACCEPTANCE,
		label='')




