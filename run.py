# coding=utf-8

###create by wenning at 2016-7-22
###First update at 2016-7-22

import cookielib
import urllib
import urllib2
import re
import time
import datetime

import config
import os.path
from pygit import get_git_log
from pygit import updateTimeSheet
from pygit import get_all_git_log



cookiefile = config.cookiefile
cookie = None
handler = None
opener = None

date = None
description = None
strdate = None

str_begin_date = raw_input("Please input the begain date you want set and comfirm the format is 'yyyy-mm-dd' or 'dd/mm/yyyy' (default is today):\n")
if (str_begin_date == None or str_begin_date == ''):
    date = time.localtime()
    strdate = '{}-{}-{}'.format(date.tm_year,date.tm_mon,date.tm_mday)
    print "Upload the time shit log for {}, please wait.".format(strdate)
else:
    if str_begin_date.find("/") != -1:
        ISOTIMEFORMAT='%d/%m/%Y'
    else:
        ISOTIMEFORMAT='%Y-%m-%d'
    begin_date = time.strptime(str_begin_date,ISOTIMEFORMAT)
    str_end_date = raw_input("Please input the end date you want set and comfirm the format is 'yyyy-mm-dd' or 'dd/mm/yyyy' (default is today):\n")
    if (str_end_date == None or str_end_date == ''):
        date = time.localtime()
        strdate = '{}-{}-{}'.format(date.tm_year,date.tm_mon,date.tm_mday)
        print "Upload the time shit log for {}, please wait.".format(strdate)
    else:
        if str_end_date.find("/") != -1:
            ISOTIMEFORMAT='%d/%m/%Y'
        else:
            ISOTIMEFORMAT='%Y-%m-%d'
        end_date = time.strptime(str_end_date,ISOTIMEFORMAT)

if strdate == None:
    description = raw_input("Please input the timesheet 'Description' (default is git log from {} to {}):\n".format(str_begin_date,str_end_date))
else:
    description = raw_input("Please input the timesheet 'Description' (default is git log at {}):\n".format(strdate))
##test for load git logs
#begin = datetime.datetime.strptime(str_begin_date, "%Y-%m-%d")
#end = datetime.datetime.strptime(str_end_date, "%Y-%m-%d")
#
#log_list = get_all_git_log()
#
#while begin <= end:
#    date = time.strptime(begin.strftime("%Y-%m-%d"),'%Y-%m-%d')
#    description = get_git_log(date,log_list)
#    begin += datetime.timedelta(days=1)
#exit()

print "Get login status...."
if os.path.isfile(cookiefile):
    need_login = False
else:
    need_login = True

print "Login...."
if need_login:
    cookie = cookielib.MozillaCookieJar(cookiefile)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    # first request to login
    logindata = urllib.urlencode({
        'log':config.account['username'],
        'pwd':config.account['password'],
        'rememberme':'forever',
        'wp-submit':'登录',
        'redirect_to':'http://intranet.gnum.com/wp-admin/',
        'testcookie':'1'
    })
    response = opener.open(config.url_login, logindata)
    cookie.save(ignore_discard=True, ignore_expires=True)
else:
    # load cookie file
    cookie = cookielib.MozillaCookieJar(cookiefile)
    cookie.load(cookiefile, ignore_discard=True, ignore_expires=True)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)


response2 = opener.open(config.url_form)
cookie.save(ignore_discard=True, ignore_expires=True)
#print(response2.read())
m = re.search(r'name="_wpnonce" value="(.*?)" />', response2.read())
# get _wpnonce
_wpnonce = m.group(1)
# set datetime format


if date != None:
    print "Upload the time sheet...."
    strDate = time.strftime(' %b %Y',date)
    strDate = "{}{}".format(date.tm_mday, strDate)

    if description == None or description == "":

        description = config.description
        # get desc from git repo

        # print "Get git log for default sheet Description"

        print "Get input descripton..."
        
        # description = get_git_log(date,get_all_git_log())

    if description == None or description == '':
        print 'None git commit message was found'
        exit()
    updateTimeSheet(date, description,_wpnonce,cookie,cookiefile)
else:
    print "Load description from local git...."
    if str_begin_date.find("/") != -1:
        ISOTIMEFORMAT='%d/%m/%Y'
    else:
        ISOTIMEFORMAT='%Y-%m-%d'
    begin = datetime.datetime.strptime(str_begin_date, ISOTIMEFORMAT)

    if str_end_date.find("/") != -1:
        ISOTIMEFORMAT='%d/%m/%Y'
    else:
        ISOTIMEFORMAT='%Y-%m-%d'
    end = datetime.datetime.strptime(str_end_date, ISOTIMEFORMAT)
    
    log_list = get_all_git_log()
    need_des = False
    if description == None:
        need_des = True
    while begin <= end:
        date = time.strptime(begin.strftime("%Y-%m-%d"),'%Y-%m-%d')
        if need_des == True:
            description = get_git_log(date,log_list)
        if description != None:
            updateTimeSheet(date, description,_wpnonce,cookie,cookiefile)
        begin += datetime.timedelta(days=1)

print "All done!!!"
exit()


