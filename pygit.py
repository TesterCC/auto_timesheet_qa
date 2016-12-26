# coding=utf-8

###create by wenning at 2016-7-22
###First update at 2016-7-22

import config
import time
import cookielib
import urllib
import urllib2
import config
import os.path
from gittle import Gittle

def get_all_git_log():
    repo = Gittle(config.repo)
    return repo.log()

def get_git_log(date,log_list):
    y = date.tm_year
    m = date.tm_mon
    d = date.tm_mday
    s_begain = '{}-{}-{} {}'.format(y, m, d, '00:00:00')
    s_end    = '{}-{}-{} {}'.format(y, m, d, '23:59:59')
    print "Datetime between {} and {}".format(s_begain,s_end)
    i_begain = time.mktime(time.strptime(s_begain,'%Y-%m-%d %X'))
    i_end    = time.mktime(time.strptime(s_end   ,'%Y-%m-%d %X'))
    
    res = []
    for line in log_list:
#        print "compare log date time:{} with {}".format(line['time'],i_begain)
        if int(line['time']) < int(i_begain):
            continue;
        if int(line['time']) > int(i_end):
            continue;
        if (config.author in line['author']['name'] or config.author in line['author']['raw']) and int(line['time']) > int(i_begain):
                                                                                                    
            temp = line['message']
            if temp.find("Merge branch") != -1:
                continue
            temp = temp.strip()
            res.append(temp)
    if len(res) == 0:
        print "None git log were found"
        return None
    else:
        ret = '\n'.join(res)
        print """*******************description***********************
{}""".format(ret)
        print """*****************************************************"""
        return ret

def updateTimeSheet(date, description,_wpnonce,cookie,cookiefile):
    strDate = time.strftime(' %b %Y',date)
    strDate = "{}{}".format(date.tm_mday, strDate)
    postdata = urllib.urlencode({
        '_wpnonce':_wpnonce,
        '_wp_http_referer':'/wp-admin/admin.php?page=wp_timesheets_user_manage&action=add',
        'job_name':config.project,  # GRUC
        'jobtype_name':config.jobtype,
        'jobsubtype_name':config.jobsubtype,
        'work-type':config.worktype,
        # 'date':'6+Jul+2016',
        'date':strDate,
        'time1':config.starttime,
        'time2':config.endtime,
        'description':description,
        'action':'save'
        })
    url_post = config.url_form+"?page=wp_timesheets_user_manage"
    cookie.load(cookiefile, ignore_discard=True, ignore_expires=True)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.addheaders = ([('User-agent', 'Mozilla/5.0 (X11; Linux i686)')])
    submit_response = opener.open(config.url_form, postdata)
    output = open('output.html','w')
    output.write(submit_response.read())
    output.close()
    print "Upload success!!!"
    return