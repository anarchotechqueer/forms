from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib import messages
from django.template import RequestContext

from datetime import datetime
import time
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from timelib import strtotime

from django.core.mail import send_mail
from ted import TEDConnection
import csv
import MySQLdb
from fpdf import FPDF, HTMLMixin

from newforms.choice_forms import *

from SpecialTrustDBAccess import *

# ---------------- Global Vars ---------------- 
SERVICE_EID = "4679mutd"
SERVICE_PASS = "+zyuwda3::4q-rbo#3;c:y(z=pvgz0%iv51to(k"

MYSQL_HOST = "mysqldb02.its.utexas.edu" 
MYSQL_USER = "iso65_post" 
MYSQL_PASS = "paus9Wu.ZIn" 
MYSQL_DB = "iso65_post"
# ---------------- Global Vars ---------------- 

def choices_form(request):
    if request.method == 'GET':
        form = ChoiceForm()
    else:
        form = ChoiceForm(request.POST)

        if form.is_valid():
            form_url = str(form.cleaned_data['choices']).lower() + '_form.html'
            
            return HttpResponseRedirect(form_url)  
    
    return render(request, 'forms/choice_form.html', {
        'form': form,
    })    

def application_form(request):    
    if request.method == 'GET':
        form = ApplicationForm()
    else:
        form = ApplicationForm(request.POST) 

        if form.is_valid():
            url = form.cleaned_data['url']
            credentials = form.cleaned_data['credentials']
            data_classification = form.cleaned_data['data_classification']
            dev_environment = form.cleaned_data['dev_environment']
            links = form.cleaned_data['links']
            auto_emails = form.cleaned_data['auto_emails']
            batch_files = form.cleaned_data['batch_files']
            notes = form.cleaned_data['notes']
            timeline = form.cleaned_data['timeline']

            message = 'Type of submission: Application.\n'+ \
            '\nURL:'+url+ \
            '\nCredentials: '+credentials +\
            '\nData Classification: '+data_classification + \
            '\nDevelopment Environment: ' + dev_environment + \
            '\nLinks: '+links+ \
            '\nAutomated Emails: '+auto_emails+ \
            '\nBatch files: '+batch_files+ \
            '\nNotes: '+notes+ \
            '\nTimeline: '+timeline

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu'], fail_silently=False)

            return render_to_response('submit.html')
  
    return render(request, 'forms/application_form.html', {
        'form': form,
    })

def servers_form(request):
    if request.method == 'GET':
        form = ServersForm()
    else:
        form = ServersForm(request.POST)

        if form.is_valid():
            hostnames = form.cleaned_data['hostnames']
            credentials = form.cleaned_data['credentials']
            certificates = form.cleaned_data['certificates']
            os = form.cleaned_data['os']
            data_classification = form.cleaned_data['data_classification']
            dev_environment = form.cleaned_data['dev_environment']
            notes = form.cleaned_data['notes']
            timeline = form.cleaned_data['timeline']
            ready_to_scan = form.cleaned_data['ready_to_scan']

            message = 'Type of submission: Servers.\n'+ \
            '\nHostnames: '+hostnames+ \
            '\nCredentials: '+credentials +\
            '\nCertificates: '+certificates+ \
            '\nOperating Systems: '+os+ \
            '\nData Classification: '+data_classification + \
            '\nDev Environment: '+ dev_environment + \
            '\nNotes: '+notes+ \
            '\nTimeline: '+timeline+ \
            '\nReady to Scan?'+ready_to_scan

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu'], fail_silently=False)

            return render_to_response('submit.html')
 
    return render(request, 'forms/servers_form.html', {
        'form': form,
    })

def unit_form(request):
    if request.method == 'GET':
        form = UnitForm()
    else:
        form = UnitForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']
            dep_head_eid = form.cleaned_data['dep_head_eid']
            timeline = form.cleaned_data['timeline']

            message = 'Type of submission: Unit.\n'+\
            '\nDescription: '+description+ \
            '\nDepartment Head / Sponsor EID: '+ dep_head_eid + \
            '\nTimeline: '+timeline

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu'], fail_silently=False)

            return render_to_response('submit.html')
 
    return render(request, 'forms/unit_form.html', {
        'form': form,
    })

def physical_form(request):
    if request.method == 'GET':
        form = PhysicalForm()
    else:
        form = PhysicalForm(request.POST) 

        if form.is_valid():
            description = form.cleaned_data['description']
            timeline = form.cleaned_data['timeline']
            location = form.cleaned_data['location']
            time = form.cleaned_data['time']
            when_to_meet = form.cleaned_data['when_to_meet']

            message = 'Type of submission: Physical.\n'+ \
            '\nDescription: '+description+ \
            '\nTimeline: '+timeline+ \
            '\nLocation: '+location+ \
            '\nTime: '+time+ \
            '\nWhen to meet: '+ when_to_meet

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu'], fail_silently=False)

            return render_to_response('submit.html')
 
    return render(request, 'forms/physical_form.html', {
        'form': form,
    })

def other_form(request):
    if request.method == 'GET':
        form = OtherForm()
    else:
        form = OtherForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']
            timeline = form.cleaned_data['timeline']

            message = 'Type of submission: Other.\n'+ \
            '\nDescription: '+description+ \
            '\nTimeline: '+timeline

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu'], fail_silently=False)

            return render_to_response('submit.html')            
 
    return render(request, 'forms/other_form.html', {
        'form': form,
    })

def security_exception_report_form(request):
    if request.method == 'GET':
        form = SecurityExceptionReportForm()
    else:
        form = SecurityExceptionReportForm(request.POST) # Bind data from request.POST into a PostForm
 
        if form.is_valid():

            mail = request.META['HTTP_UTLOGIN_EMAIL']
            
            standard = form.cleaned_data['standard']
            noncompliance = form.cleaned_data['noncompliance'] 
            justify_noncompliance = form.cleaned_data['justify_noncompliance'] 
            data = form.cleaned_data['data']
            assessment = form.cleaned_data['assessment'] 
            manage = form.cleaned_data['manage'] 
            metrics = form.cleaned_data['metrics'] 
            school = form.cleaned_data['school'] 
            systems = form.cleaned_data['systems']
            data_classification = form.cleaned_data['data_classification'] 
            duration = form.cleaned_data['duration']
            eid = form.cleaned_data['eid']

            message = '[Security Exception Report] Submission\n'+ \
            "\nStandard/Policy/Guideline for which an exception is being reported: "+ standard + \
            "\nDescribe the non-compliance:  "+ noncompliance + \
            "\nBriefly justify the non-compliance:  "+ justify_noncompliance + \
            "\nData, departments and customers that might be put at risk by the exception: "+ data + \
            "\nProvide an assessment of the risk associated with non-compliance: "+ assessment + \
            "\nDescribe what is being done to mitigate (manage) risk: "+ manage + \
            "\nProvide metrics to evaluate the success of risk management: "+ metrics + \
            "\nThe college, school, or unit which initially reported the exception: "+school + \
            "\nList the system(s) by MAC address (include both wired and wireless interfaces) associated with this report: "+systems + \
            "\nData Classification: "+data_classification + \
            "\nAnticipated duration for the exception: "+duration + \
            "\nEID for approving IT owner (for example, the IT Manager or Department Head): "+eid

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu', mail], fail_silently=False)

            return render_to_response('submit.html')
 
    return render(request, 'forms/exception_form.html', {
        'form': form,
    })

def stolen_equipment_notification_form(request):
    if request.method == 'GET':
        form = StolenEquipmentNotificationForm()
    else:
        form = StolenEquipmentNotificationForm(request.POST) # Bind data from request.POST into a PostForm
 
        if form.is_valid():

            mail = request.META['HTTP_UTLOGIN_EMAIL']

            callback = form.cleaned_data['callback']
            casenumber = form.cleaned_data['casenumber']
            description = form.cleaned_data['description']
            wired_mac = form.cleaned_data['wired_mac']
            wireless_mac = form.cleaned_data['wireless_mac']
            date = form.cleaned_data['date']
            location = form.cleaned_data['location']
            eid = form.cleaned_data['eid']
            is_cat_1 = form.cleaned_data['is_cat_1']
            encrypted = form.cleaned_data['encrypted']

            message = '[Stolen Equipment Notification] submission\n' + \
            "\nCall Back Number: " + callback +\
            "\nLaw Enforcement Case Number: " + casenumber +\
            "\nDevice Description: " + description +\
            "\nWired MAC Address: " + wired_mac + \
            "\nWireless MAC Address: " + wireless_mac +\
            "\nLast date the device was connected to the UT network : " + date +\
            "\nLocation/Building where device was stolen: " + location +\
            "\nEID of Primary User of Device: " + eid +\
            "\nIs there Category-I data stored on this device? " + is_cat_1 + \
            "\nIs the data on this device encrypted? " + encrypted

            send_mail('[Application] submission', message, 'forms.security@utexas.edu',
                ['security@utexas.edu',mail], fail_silently=False)

            return render_to_response('submit.html')
 
    return render(request, 'forms/iso_theft_form.html', {
        'form': form,
    })

def special_trust_exists(request):
    USER_EID = request.META['HTTP_UTLOGIN_EID']
    date = last_valid_post(USER_EID).split(' ')[:-1]
    last_date = ' '.join(date)
    last_date = {'last_date':last_date}
    if not last_date:
        return HttpResponseRedirect("/forms/specialtrust/")
    return render(request, 'forms/specialtrust_exists.html',{
        'last_date': last_date
    })

def special_trust_form(request):
    USER_EID = request.META['HTTP_UTLOGIN_EID']
    USER_NAME = request.META['HTTP_UTLOGIN_NAME']

    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)

    attrs = [
        'cn',
        'givenName',
        'sn',
        'utexasEduPersonPrimaryTitle',
        'utexasEduPersonOrgUnitName',
        'edupersonorgunitdn',
        'manager',
        'utexasEduPersonOfficeLocation',
        'telephoneNumber',
        'mail'
    ]
 
    p = conn.get_by_eid(USER_EID, attrs=attrs)

    USER_TITLE = p['utexasedupersonprimarytitle'][0]
    USER_MAIL = p['mail'][0]
    WORKPLACE = p['utexasedupersonorgunitname'][0]
    MANAGER = p['manager'][0]

    MANAGER_LST = MANAGER.replace('=',',').split(',')
    MANAGER_EID = MANAGER_LST[1]
    MANAGER_NAME = ''
    MANAGER_EMAIL = ''
    if 'restrict' in MANAGER_LST:
        MANAGER_NAME = 'your manager'
    else:
        mngr_attrs= [
            'cn',
            'mail'
        ]
        q = conn.get_by_eid(MANAGER_EID, attrs=mngr_attrs)
        MANAGER_NAME = q['cn'][0]
        MANAGER_EMAIL = q['mail'][0]

    USER_DEPARTMENT  = p['utexasEduPersonOrgUnitName'][0]
    DEPARTMENT = p['edupersonorgunitdn'][0].split(',')[0][6:]
    USER_ROOM = p['utexasEduPersonOfficeLocation'][0]
    
    if 'telephoneNumber' in p:
        USER_WORKPHONE = p['telephoneNumber']
    else:
        USER_WORKPHONE = 'N/A'

    info = {
        'eid':USER_EID,
        'name':USER_NAME,
        'title':USER_TITLE,
        'manager_name':MANAGER_NAME,
        'manager_eid': MANAGER_EID,
        'room':USER_ROOM,
        'phone':USER_WORKPHONE,
        'dept':USER_DEPARTMENT
    }

    if request.method == 'GET':
        last_date = last_valid_post(USER_EID)
        skip_check = request.GET.get('skip_check','')

        if not skip_check and last_date:
            return HttpResponseRedirect("/forms/specialtrust/exists/")
            
        form = SpecialTrustForm()
    else:
        form = SpecialTrustForm(request.POST)

        if form.is_valid():
            answer = str(form.cleaned_data['acceptance']).lower()

            answer = 1 if answer == "i agree" else 0

            add_entry(USER_EID, USER_NAME, DEPARTMENT, MANAGER_EID, MANAGER_NAME, USER_DEPARTMENT, answer)

            send_accept_mail(answer, USE_EID, USER_NAME, USER_MAIL, USER_TITLE, USER_DEPARTMENT,
                USER_ROOM, USER_WORKPHONE, MANAGER_EID, MANAGER_NAME, MANAGER_EMAIL)

            form_url = '/forms/specialtrust/accept/'
            return HttpResponseRedirect((str(form_url)))
 
    return render(request, 'forms/specialtrust_form.html', {
        'form': form,
        'info': info 
    })

def special_trust_managers(request):

    USER_EID = request.META['HTTP_UTLOGIN_EID']

    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)

    filt = '(&(utexasEduPersonSpecialTrustSw=Y)(eduPersonOrgDN=ou=UTAUS,ou=institutions,dc=entdir,dc=utexas,dc=edu)(manager=uid='+USER_EID+',ou=people,dc=entdir,dc=utexas,dc=edu))'

    attrs = ['utexasEduPersonEid','mail','displayName','utexasedupersonprimarytitle']

    search = conn.search(filt, attrs=attrs)

    subordinates = []

    for item in search:
        tmp = []
        tmp.append(item['utexasEduPersonEid'][0])
        tmp.append(item['mail'][0])
        tmp.append(item['displayName'][0])
        tmp.append(item['utexasEduPersonPrimaryTitle'][0])
        tmp.append(last_post_or_never(tmp[0]))
        
        if tmp[4] == 'Never' or strtotime(tmp[4]) < strtotime('-1 year -2 weeks'):
            tmp.append('<span class="overdue">Overdue</span>')
        elif strtotime(tmp[4]) <= strtotime('-1 year'):
            tmp.append('Due')
        else:
            tmp.append('Current')

        subordinates.append(tmp)
    
    subordinates.sort()

    person = {'eid':USER_EID}

    return render(request, 'forms/specialtrust_manager.html', {
        'person': person,
        'subordinates': subordinates
    })

def special_trust_hrcontacts(request):

    USER_EID = request.META['HTTP_UTLOGIN_EID']

    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
    
    filt = '(&(utexasEduRoleSource=OHSC)(member=uid='+USER_EID+',ou=people,dc=entdir,dc=utexas,dc=edu)(|(utexasEduRoleCode=0HC001)(utexasEduRoleCode=0DC200)(utexasEduRoleCode=0UN004))(utexasEduRoleAttribute=All))'

    attrs = ['utexasEduRoleScope']
    search = conn.search(filt, attrs=attrs)
    
    subordinates = []
    dept_search = ''
    filt = ''

    if len(search):

        for item in search:
            dept_search += "(eduPersonOrgUnitDn="+item['utexasEduRoleScope'][0]+")"

        if len(search) > 1:
            dept_search = "(|" + dept_search

        dept_search += ")"

        attrs = [
            'utexasEduPersonEid',
            'mail',
            'displayName',
            'title',
            'edupersonorgunitDN'
        ]

        filt = "(&(utexasEduPersonSpecialTrustSw=Y)(eduPersonOrgDN=ou=UTAUS,ou=institutions,dc=entdir,dc=utexas,dc=edu)" + dept_search+")"

        search = conn.search(filt, attrs=attrs)

        for item in search:
            if item['utexasEduPersonEid']:
                tmp = []
                tmp.append(item['displayName'][0])
                tmp.append(item['utexasEduPersonEid'][0])
                tmp.append(item['title'][0])
                
                if 'mail' in item:
                    tmp.append(item['mail'][0])
                else:
                    tmp.append('')
                
                tmp.append(last_post_or_never(tmp[1]))
                
                if tmp[4] == 'Never' or strtotime(tmp[4]) < strtotime('-1 year -2 weeks'):
                    tmp.append('<span class="overdue">Overdue</span>')
                elif strtotime(tmp[4]) <= strtotime('-1 year'):
                    tmp.append('Due')
                else:
                    tmp.append('Current')
                
                dept_name = item['eduPersonOrgUnitDn'][0].split(',')[0][6:].upper()
                tmp.append(dept_name)
                subordinates.append(tmp)  
        subordinates.sort()

    person = {'eid':USER_EID}

    return render(request, 'forms/specialtrust_hrcontacts.html', {
        'person': person,
        'subordinates': subordinates,
    })

def special_trust_admin(request):

    USER_EID = request.META['HTTP_UTLOGIN_EID']
    person = {'eid':USER_EID}

    if request.method == 'POST':
        post_eid = request.POST.get('eid', '')
        timestamp = request.POST.get('timestamp','')

        if len(timestamp) and USER_EID == post_eid:
            remove_entry(USER_EID, timestamp)
        USER_EID = post_eid

    entries = all_entries(USER_EID)
    
    for entry in entries:
        entry[2] = entry[2].strftime('%Y-%m-%d %H:%M:%S')
        entry[3] = "yes" if entry[3] == 1 else 'no'

    return render(request, 'forms/specialtrust_admin.html', {
        'person': person,
        'entries': entries
    },
    context_instance = RequestContext(request))

# class to add html to pdf using pyfpdyf
class MyFPDF(FPDF,HTMLMixin):
    pass

def special_trust_dump_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dump_current.csv"'

    writer = csv.writer(response, quotechar='"',quoting=csv.QUOTE_NONNUMERIC,delimiter=',')
    writer.writerow(["Dept_Code", "Name", "EID", "Agree", "Timestamp", "Department", "Manager", "Manager_EID"])

    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    timestamp = strtotime('-1 year')
    yearago = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    query = "SELECT department, name, eid, agree, timestamp, dept_name, manager_name, manager FROM specialtrust WHERE timestamp >= '{0}'".format(yearago)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    except:
        print("Error: unable to fetch data")

    db.close()

    return response

def pdf_view(request):
    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)

    USER_EID = request.META['HTTP_UTLOGIN_EID']
    USER_NAME = request.META['HTTP_UTLOGIN_NAME']
    
    attrs = [
        'cn',
        'givenName',
        'sn',
        'utexasEduPersonOrgUnitName',
        'utexasEduPersonPrimaryTitle',
        'utexasEduPersonOrgUnitName',
        'manager',
        'utexasEduPersonOfficeLocation',
        'telephoneNumber'
    ]

    p = conn.get_by_eid(USER_EID, attrs=attrs)

    USER_TITLE = p['utexasedupersonprimarytitle'][0]
    WORKPLACE = p['utexasedupersonorgunitname'][0]
    MANAGER = p['manager'][0]

    MANAGER_LST = MANAGER.replace('=',',').split(',')
    MANAGER_EID = MANAGER_LST[1]
    MANAGER_NAME = ''
    if 'restrict' in MANAGER_LST:
        MANAGER_NAME = 'your manager'
    else:
        mngr_attrs= ['cn']
        q = conn.get_by_eid(MANAGER_EID, attrs=mngr_attrs)
        MANAGER_NAME = q['cn'][0]

    USER_DEPARTMENT  = p['utexasEduPersonOrgUnitName'][0]
    USER_ROOM = p['utexasEduPersonOfficeLocation'][0]
    
    if 'telephoneNumber' in p:
        USER_WORKPHONE = p['telephoneNumber']
    else:
        USER_WORKPHONE = 'N/A'

    AGREE = request.POST.get('agree', 'electronically declined')

    dt = datetime.now()
    df = DateFormat(dt)

    textdate = str(df.format(get_format('DATE_FORMAT')))

    timestamp = str(df.format('m/d/Y')) + " at " + str(time.strftime("%H:%M:%S"))

    stamp = last_valid_post(USER_EID)
    stamp_textdate = ' '.join(stamp.split(' ')[:-1])
    stamp_time = ''.join(stamp.split(' ')[-1])
    tmp = stamp_textdate.replace(',','')
    stamp_date = str(datetime.strptime(tmp, '%B %d %Y').strftime('%m/%d/%Y'))
    # stamp_date = tmp
    msg = "I acknowledge my role as a Custodian of The University of Texas at Austin Information Resources."+ \
        " I realize that I have been assigned duties that will bring me in contact with information or information"+\
        " resources that are of value to the university and that require confidentiality and protection."+\
        " I further acknowledge that I am required to uphold university policies and standards to safeguard "+\
        "the information and associated resources that are entrusted to me or with which I have contact."+\
        " I agree to report violations of policies, standards, procedures, or guidelines that come to my attention "+\
        "to my supervisor and/or the Information Security Office.\n\nI understand and agree that violations of "+\
        "university policies, standards, and procedures pertaining to custodians of the university's Information Resources "+\
        "and confidential information shall be subject to disciplinary action up to and including termination.\n\n" +\
        USER_NAME +' '+ AGREE + \
        " concurrence with this responsibility on "+\
        stamp_textdate +\
        " for the job title and department listed above.\n\nThis form has been submitted to "+\
        MANAGER_NAME +\
        " and the Information Security Office.\n\nForm submitted: "+\
        stamp_date + ' at ' + stamp_time + \
        " \n\nReferences:\n\n"

    reference_links = [
        ["http://www.utexas.edu/cio/policies/pdfs/AUP.pdf", "UT Austin Acceptable Use Policy", "(section V, rule 11)"],
        ["http://www.utexas.edu/cio/policies/pdfs/Information%20Resources%20Use%20and%20Security%20Policy.pdf",
            "UT Austin Inform.ation Resources Use and Security Policy","(section V, item 4)"],
        ["http://www.utsystem.edu/policy/policies/uts165.html","UT System Information Resources Use and Security Policy","(section 4)"],
        ["http://info.sos.state.tx.us/pls/pub/readtac$ext.TacPage?sl=R&app=9&p_dir=&p_rloc=&p_tloc=&p_ploc=&pg=1&ti=1&ch=202&rl=75",
            "Texas Administrative Code 202", "(Rule 202.75, 7.C)"],
        ["http://www.statutes.legis.state.tx.us/Docs/PE/htm/PE.33.htm", "Texas Computer Crimes Act",'' ]
    ]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="download.pdf"'

    pdf = MyFPDF()
    pdf.add_page()

    pdf.set_left_margin(20)
    pdf.set_right_margin(20)

    pdf.set_font('Times','',12)

    pdf.set_line_width(0.1)
    pdf.line(20,12,196,12)
    pdf.set_xy(14,5)
    pdf.cell(0,10,'POSITION OF SPECIAL TRUST FORM',border=0,ln=1,align='C')
    pdf.cell(0,0,'The University of Texas at Austin',border=0,ln=1,align='C')

    pdf.set_xy(20,20)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Employee EID:")
    pdf.set_xy(60,20)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_EID)

    pdf.set_xy(20,25)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Employee Name:") 
    pdf.set_xy(60,25)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_NAME)

    pdf.set_xy(20,30)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Title:")
    pdf.set_xy(60,30)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_TITLE)

    pdf.set_xy(20,35)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Department:")
    pdf.set_xy(60,35)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_DEPARTMENT)

    pdf.set_xy(20,40)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Room Number:")
    pdf.set_xy(60,40)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_ROOM)

    pdf.set_xy(20,45)
    pdf.set_font('Times','B',12)
    pdf.write(3,"Office Phone:")
    pdf.set_xy(60,45)
    pdf.set_font('Times','',12)
    pdf.write(3,USER_WORKPHONE)

    pdf.set_xy(20,55)
    pdf.write(5,msg)

    for link in reference_links:
        tmp = '<a href="'+link[0]+'">'+link[1]+'</a>'
        pdf.write_html(tmp)
        pdf.write(5, ' '+link[2]+'\n')
        pdf.set_font('Times','',9)
        tmp = '['+ link[0]+']\n'
        pdf.write(5,tmp)
        pdf.set_font('Times','',12)

    response.write(pdf.output('','S'))
    return response

def send_accept_mail(agree, eid, name, email, title, department, room, workphone, manager_eid, manager_name, manager_email):
    mailing_list = []
    mailing_list.append('security@utexas.edu')

    message = ''
    if not agree:
        message += "NOTE: EMPLOYEE DID NOT AGREE.\n\n"
        mailing_list.append(manager_email)

    message += "Employee EID: {0}\n" + \
    "Employee Name: {1}\n" + \
    "Title: {2}\n" + \
    "Department: {3}\n" + \
    "Room Number: {4}\n" + \
    "Office Phone: {5}\n" + \
    "Manager EID: {6}\n" + \
    "Manager Name: {7}\n" + \
    "\nReferences:\n" + \
    "* UT Austin Acceptable Use Policy (section V, rule 11)\n" + \
    "* UT Austin Information Resources Use and Security Policy (section V, item 4)\n" + \
    "* UT System Information Resources Use and Security Policy (section 4)\n" + \
    "* Texas Administrative Code 202 (Rule 202.75, 7.C)\n" + \
    "* Texas Computer Crimes Act\n\n" + \
    "I acknowledge my role as a Custodian of The University of Texas at Austin Information Resources. I realize that I have been assigned duties that will bring me in contact with information or information resources that are of value to the university and that require confidentiality and protection. I further acknowledge that I am required to uphold university policies and standards to safeguard the information and associated resources that are entrusted to me or with which I have contact. I agree to report violations of policies, standards, procedures, or guidelines that come to my attention to my supervisor and/or the Information Security Office.\n I understand and agree that violations of university policies, standards, and procedures pertaining to custodians of the university's Information Resources and confidential information shall be subject to disciplinary action up to and including termination.\n\n".format(eid, name, title, department, room, workphone, manager_eid, manager_name)

    if agree:
        message += "I acknowledge my awareness of and concurrence with this responsibility.\n\n"
    else:
        message += "I do not wish to be in a position with such responsibility.\n\n"

    message += "Submitted by "+ name +" on " + str(datetime.now().strftime('%m/%d/%Y')) +" at " + str(datetime.now().strftime('%H:%M:%S'))

    title = "Position of Special Trust form for {0}, {1}".format(name, eid)

    send_mail(title, message, 'security@utexas.edu', mailing_list, fail_silently=False)

'''
def notify_users():
    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
    notify_users = []

    filt = '(&(utexasEduPersonSpecialTrustSw=Y)(eduPersonOrgDN=ou=UTAUS,ou=institutions,dc=entdir,dc=utexas,dc=edu))'

    attrs = ['utexasEduPersonEid','mail','displayName']

    search = conn.search(filt, attrs=attrs)
    
    # GET SPECIAL TRUST USERS
    for item in search:
        if item['utexasEduPersonEid']:
            tmp = []
            tmp.append(item['displayName'][0])
            tmp.append(item['utexasEduPersonEid'][0])
            
            if 'mail' in item:
                tmp.append(item['mail'][0])
            else:
                tmp.append('')
            
            notify_users.append(tmp)  
    notify_users.sort()

    unable_to_notify = []

    active = active_eids()

    # Remove active eids from notify_users
    notify_users = [user for user in notify_users if user[1] not in active]
    timestamp = strtotime('-1 year -2 weeks')
    cc_manager_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    for user in notify_users:
        name = user[0]
        eid = user[1]
        email = user[2]
        if email:
            attrs = ['cn','manager','edupersonorgunitdn']

            p = conn.get_by_eid(eid, attrs=attrs)

            manager = ''
            manager_email = ''
            dept_name = ''

            if 'edupersonorgunitdn' in p:
                dept_name = p['edupersonorgunitdn']   

            if len(dept_name) < 2:
                if 'manager' in p:
                    manager = p['manager'][0].split(',')[0][4:]
                    attrs = ['cn','mail']
                    conn1 = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
                    if manager:
                        q = conn1.get_by_eid(manager, attrs=attrs)
                        if 'mail' in q:
                            manager_email = q['mail'][0]
 
                if last_post(eid) <= cc_manager_date and manager:            
                    cron_send_user_mail(eid,name,email,manager_email)
        else:
            unable_to_notify.append(eid)

    cron_send_iso_mail( len(notify_users), unable_to_notify)
'''
def notify_users(request):
    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
    notify_users = []

    filt = '(&(utexasEduPersonSpecialTrustSw=Y)(eduPersonOrgDN=ou=UTAUS,ou=institutions,dc=entdir,dc=utexas,dc=edu))'

    attrs = ['utexasEduPersonEid','mail','displayName']

    search = conn.search(filt, attrs=attrs)
    
    # GET SPECIAL TRUST USERS
    for item in search:
        if item['utexasEduPersonEid']:
            tmp = []
            tmp.append(item['displayName'][0])
            tmp.append(item['utexasEduPersonEid'][0])
            
            if 'mail' in item:
                tmp.append(item['mail'][0])
            else:
                tmp.append('')
            
            notify_users.append(tmp)  
    notify_users.sort()

    unable_to_notify = []

    active = active_eids()

    # Remove active eids from notify_users
    notify_users = [user for user in notify_users if user[1] not in active]
    timestamp = strtotime('-1 year -2 weeks')
    cc_manager_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    users_to_notify = []
    l = len(notify_users)

    for user in notify_users:
        name = user[0]
        eid = user[1]
        email = user[2]
        if email:
            attrs = ['cn','manager','edupersonorgunitdn']

            p = conn.get_by_eid(eid, attrs=attrs)

            manager = ''
            manager_email = ''
            dept_name = ''
            tmp = []

            if 'manager' in p:
                manager = p['manager'][0].split(',')[0][4:]
                attrs = ['cn','mail']
                conn1 = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
                if manager:
                    q = conn1.get_by_eid(manager, attrs=attrs)
                if 'mail' in q:
                    manager_email = q['mail'][0]

            if 'edupersonorgunitdn' in p:
                dept_name = p['edupersonorgunitdn']

            if len(dept_name) < 2:
                # if last_post(eid) <= cc_manager_date and manager:
            
                tmp.append(eid)
                tmp.append(name)
                tmp.append(email)
                tmp.append(manager_email)                
                tmp.append(last_post(eid))
                tmp.append(cc_manager_date)
                users_to_notify.append(tmp)
                    # cron_send_user_mail(eid,name,email,manager_email)
        else:
            unable_to_notify.append(eid)

        # cron_send_iso_mail( len(notify_users), unable_to_notify)

    #delete this after
    unable_to_notify.sort()

    return render(request, 'forms/notify_users.html', {
        'l':l,
        'users_count': len(users_to_notify),
        'users_to_notify': users_to_notify,
        'unable_count': len(unable_to_notify),
        'unable_to_notify': unable_to_notify
    })

def quarterly_summaries(request):
    conn = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
    
    managers = {}
    users_to_managers = {}
    post_users = []

    filt = '(&(utexasEduPersonSpecialTrustSw=Y)(eduPersonOrgDN=ou=UTAUS,ou=institutions,dc=entdir,dc=utexas,dc=edu))'

    attrs = ['utexasEduPersonEid','displayName']

    search = conn.search(filt, attrs=attrs)
    
    # GET SPECIAL TRUST USERS
    for item in search:
        if item['utexasEduPersonEid']:
            tmp = []
            tmp.append(item['displayName'][0])
            tmp.append(item['utexasEduPersonEid'][0])
            post_users.append(tmp)  
    post_users.sort()

    special_trust_users = []

    for user in post_users:
        name = user[0]
        eid = user[1]

        dept_name = ''
        manager_eid = ''
        manager_name = ''
        manager_email = ''
    
        attrs = ['displayName','manager','edupersonorgunitdn']

        p = conn.get_by_eid(eid, attrs=attrs)

        if 'edupersonorgunitdn' in p:
            dept_name = p['edupersonorgunitdn']
            if len(dept_name) < 2:
                if 'manager' in p:
                    manager_eid = p['manager'][0].split(',')[0][4:]

                if manager_eid:


                    #used for testing
                    snth = []
                    snth.append(eid)
                    snth.append(name)
                    snth.append(manager_eid)
                    special_trust_users.append(snth)


                    attrs = ['displayName','mail']
                    conn1 = TEDConnection(eid=SERVICE_EID, password=SERVICE_PASS)
                    if manager_eid not in managers:
                        q = conn1.get_by_eid(manager_eid, attrs=attrs)
                        manager_name = q['displayName'][0]
                        if 'mail' in q:
                            manager_email = q['mail'][0]
                        manager_info = {
                            'name' : manager_name,
                            'email' : manager_email
                        }
                        managers[manager_eid] = {
                            'info' : manager_info,
                            'done' : {},
                            'notdone' : {}
                        }    
                    managers[manager_eid]['notdone'][eid] = name
                    users_to_managers[eid] = manager_eid


    active = active_entries()

    #used for testing
    active_people = []


    other_people = []


    for entry in active:
        name = entry[0]
        eid = entry[1]

        snth = []
        snth.append(eid)
        snth.append(name)
        active_people.append(snth)

        if eid in users_to_managers: # and eid in managers[manager_eid]['notdone']
            manager_eid = users_to_managers[eid]
            if eid in managers[manager_eid]['notdone']:
                managers[manager_eid]['done'][eid] = managers[manager_eid]['notdone'].pop(eid)
        else:
            other_people.append(eid+" "+name)

    managers_no_email = {}
    aoeu = []

    for manager_eid, key in managers.iteritems():
        if key['info']['email']:
            name = key['info']['name']
            email = key['info']['email']
            done = key['done']
            notdone = key['notdone']
            tmp = []
            tmp.append(name)
            tmp.append(email)
            tmp.append(done)
            tmp.append(notdone)
            aoeu.append(tmp)
            # cron_send_manager_quarterly_summary_mail(name, email, done, notdone)
        else:
            managers_no_email[manager_eid] = managers[manager_eid]['info']['name']

    # if managers_no_email:
    #     for key, value in managers_no_email.iteritems():

        # cron_send_audit_quarterly_warning_mail(managers_no_email)

    return render(request, 'forms/quarterly_summaries.html', {
        'special_trust_users':special_trust_users,
        'active_people': active_people,
        'aoeu':aoeu,
        'managers_no_email':managers_no_email,
        'other_people':other_people
    })


def cron_send_manager_quarterly_summary_mail(name, email, done, notdone):
    subject = "Quarterly Summary - Positions of Special Trust"
    header = 'From: "UT Information Security Office" <security@utexas.edu>'
    message = "$manager_name --\n\nThis is a quarterly report regarding the employees in positions of special trust whom you manage.\n\n"

    if done:
        message += "The following employees in positions of special trust have completed their PoST within the past year:\n";
        for eid, name in done:
            message += "{0} ({1})\n".format(name, eid)
    
    if notdone:
        message += "\nThe following employees in positions of special trust have NOT completed their PoST within the past year:\n";
        for eid, name in done:
            message += "{0} ({1})\n".format(name, eid)
        
    message += "\nIf you have any questions or concerns, please contact the Information Security Office at security@utexas.edu.\n\nYou can see the Position of Special Trust status for every employee that you manage by visiting:\nhttps://security.utexas.edu/specialtrust/managers/ at any time"
    send_mail(subject, message, header, [email], fail_silently=False)


def cron_send_audit_quarterly_warning_mail(managers_no_email):
    email = "donna.gandy@austin.utexas.edu"
    header = 'From: "UT Information Security Office" <security@utexas.edu>'
    subject = "Manager Quarterly Summary - Position of Special Trust (Missing Managers)"
    message = "The following is a quarterly report of managers without assigned email addresses who have employees in positions of special trust.\n\n"

    for eid, name in managers_no_email:
        message += "{0} ({1})\n".format(name, eid)

    message += "\nThis may be useful for identifying user who are no longer employees of the University but are still in HRMS as managers.\nIf you have any questions or concerns, please contact the Information Security Office at security@utexas.edu."
    send_mail(subject, message, header, [email], fail_silently=False)


def cron_send_user_mail(eid, name, email, manager_email):
    subject = "Reminder - Outstanding Position of Special Trust Form [{0} - {1}]".format(eid,name)

    header = 'From: "UT Information Security Office" <security@utexas.edu>'
    message = "Employee EID: {$0}\n".format(eid) + \
    "Employee Name: {0}\n\n".format(name) + \
    "This is a reminder that your Position of Special Trust form has not yet been completed.\n\n" + \
    "Your position has been identified as one that requires special trust.  As such, university policy requires that you complete the following form each year as a way of both acknowledging the responsibilities associated with your position and university policies.\n\n" + \
    "If you do not believe that your duties qualify as a Position of Special Trust then you should consult your supervisor for clarification or to have your status changed.\n\n" + \
    "If you have any questions or concerns, please contact the ITS Help Desk at help@its.utexas.edu or 512-475-9400.\n\n" + \
    "The Position of Special Trust form is located at:\n" + \
    "https://security.utexas.edu/specialtrust/\n\n" + \
    "Note: We've recently been informed of users having trouble logging into the PoST app with " + \
    "Internet Explorer. If you experience this issue, try another browser (Chrome, Firefox).\n\n" + \
    "Thank you for your assistance.\n\n" + \
    "Information Security Office\n" + \
    "University of Texas at Austin\n" + \
    "security@utexas.edu"
    if manager_email:
        email = EmailMessage(subject, message, email, header, headers={'Cc':manager_email})
        email.send()
    else:
        send_mail(subject, message, header,[email], fail_silently=False)

def cron_send_iso_mail(count, unable_to_notify):
    date = datetime.now().strftime('%m/%d/%Y')
    subject = "PoST reminders sent on {0}".format(date)
    message = "{0} messages were sent as a part of daily PoST mailings.".format(count)
    if unable_to_notify:
        unable_count = len(unable_to_notify)
        message += "\n\nAdditionally, {0} reminders were unable to be sent to the following eids due to missing email information:".format(unable_count)
        for item in unable_to_notify:
            message += "\n"+item

    send_mail(subject, message, '',['abuse@utexas.edu'], fail_silently=False)