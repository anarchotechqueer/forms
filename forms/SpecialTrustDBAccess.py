import MySQLdb

from datetime import datetime
import time
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from timelib import strtotime

# ---------------- Global Vars ---------------- 
MYSQL_HOST = "mysqldb02.its.utexas.edu" 
MYSQL_USER = "iso65_post" 
MYSQL_PASS = "paus9Wu.ZIn" 
MYSQL_DB = "iso65_post"
# ---------------- Global Vars ---------------- 

def active_eids():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    timestamp = strtotime('-1 year')
    yearago = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    query = "SELECT eid FROM specialtrust WHERE timestamp >= '{0}' ORDER BY eid ASC".format(yearago)
    entries = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            entries.append(row[0])
    except:
        db.close()
        return ''
    
    db.close()
    return entries

def active_entries():
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    timestamp = strtotime('-1 year')
    yearago = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    query = "SELECT distinct name, eid FROM specialtrust WHERE timestamp >= '{0}'".format(yearago)
    entries = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:

            tmp = []
            tmp.append(row[0])
            tmp.append(row[1])
            entries.append(tmp)
    except:
        db.close()
        return ''
    
    db.close()
    return entries


def last_post(eid):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    cutoffdate = strtotime('-1 year -2 weeks -1 day')
    definitely_cc_boss_date = str(datetime.fromtimestamp(cutoffdate).strftime('%Y-%m-%d'))
    query = "SELECT COALESCE( MAX(timestamp), '{0}' ) FROM specialtrust WHERE eid = '{1}'".format(definitely_cc_boss_date, eid)
    last_post = ''
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        last_post = results[0][0]
    except:
        return ''

    db.close()
    return last_post

def last_post_or_never(eid):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    query = "SELECT COALESCE( IF ( MAX(timestamp), DATE_FORMAT(MAX(timestamp),'%m/%d/%Y'),NULL), 'Never' ) FROM specialtrust WHERE eid = '{0}'".format(eid)
    last_post = ''
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        last_post = results[0][0]
    except:
        return ''

    db.close()
    return last_post

def last_valid_post(eid):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    timestamp = strtotime('-1 year')
    yearago = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    query = "SELECT st.* FROM ( SELECT eid, MAX( timestamp ) AS newest FROM specialtrust WHERE eid = '{0}' ) AS st_max INNER JOIN specialtrust AS st ON ( st.eid = st_max.eid AND st.timestamp = st_max.newest ) WHERE st.eid='{0}' AND st.timestamp >= '{1}'".format(eid, yearago)
    last_post = ''
    try:
        cursor.execute(query)
        last_post = cursor.fetchall()
    except:
        db.close()
        return ''

    db.close()

    date = last_post[0][0].strftime("%B %d, %Y %H:%M:%S")
    return date

def all_entries(eid):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    query = "SELECT department, manager, timestamp, agree FROM specialtrust WHERE eid='{0}'".format(eid)
    entries = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            tmp = []
            tmp.append(row[0])
            tmp.append(row[1])
            tmp.append(row[2])
            tmp.append(row[3])
            entries.append(tmp)
    except:
        db.close()
        return ''
    
    db.close()
    return entries

def remove_entry(eid, timestamp):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    query = "DELETE FROM specialtrust WHERE eid='{0}' AND timestamp = '{1}'".format(eid, timestamp)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()
    return

def add_entry(eid, name, department, manager, manager_name, dept_name, agree):
    db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO specialtrust ( timestamp, eid, name, department, manager, manager_name, dept_name, agree ) VALUES ( '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}' )".format(timestamp, eid, name, department, manager, manager_name, dept_name, agree)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()