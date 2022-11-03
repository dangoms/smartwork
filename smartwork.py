#! /usr/bin/python
# -*-coding:utf-8-*-

import sys
import requests
import urllib2
import json
import time
import datetime
import os
from jira import JIRA
from chinese_calendar import is_holiday, is_workday

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

def setEncodingToUtf8():
    '''
    python default encoding is ASCII.
    for url date error 'ascii' codec can't decode byte 0xe4 in position 4: ordinal not in range(128)
    '''
    defaultencoding = 'utf-8'
    if sys.getdefaultencoding() != defaultencoding:
        reload(sys)
        sys.setdefaultencoding(defaultencoding)
    return

def httpPost(url,data):
    '''push a string to qiye socket'''
    jdata = json.dumps(data)
    req = urllib2.Request(url, jdata)
    response = urllib2.urlopen(req)
    return response.read()

class DateTime(object):
    def __init__(self):
        '''
        the class is designd for process workday and holiday, including some useful date and time process for dailywork.
        '''
        pass

    def getTodaydate(self):
        return str(datetime.date.today())

    def getYesterday(self): 
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        
        #today = datetime.date(2022, 5, 1)
        yesterday=today-oneday
        return yesterday

    def isWorkday(self):
        '''
        return bool of today if it is a workday.
        '''
        today=datetime.date.today()
        
        #today = datetime.date(2022, 5, 1)
        if self.isAWorkDay(today):
            return True
        else:
            return False

    def isWorkdayOrLastdayIsWorkday(self):
        '''
        return bool of today if it is a workday or last day is a workday.
        '''
        today=datetime.date.today()
        
        #today = datetime.date(2022, 5, 1)
        if self.isAWorkDay(today) or self.isAWorkDay(self.getYesterday()):
            return True
        else:
            return False

    def isAWorkDay(self, StandardDay):
        '''
        return bool True if the given day is a weekday. the return value base on third pary lib.
        '''
        try:
            if is_workday(StandardDay):
                return True
            else:
                return False
        except NotImplementedError:
            return True

    def getLastWorkdayOfMonth(self):
        '''
        get lask workday of the current month.
        return a standard day.
        '''
        today=datetime.date.today()
        monthHave31Days = [1,3,5,7,8,10,12]
       
        if today.month in monthHave31Days:
            lastDay = 31
        else:
            lastDay = 30
        
        if today.year%4 == 0:
            lastDayFeb = 29
        else:
            lastDayFeb = 28

        if today.month == 2:
            lastDate = datetime.date(today.year, today.month, lastDayFeb)
        else:
            lastDate = datetime.date(today.year, today.month, lastDay)

        oneday=datetime.timedelta(days=1)
        while True:
            if self.isAWorkDay(lastDate):
                break
            lastDate=lastDate-oneday
        
        return lastDate 

    def isLastWorkdayOfAMonth(self):
        '''
        retrun True if it is a isLastWorkdayOfAMonth
        '''
        today=datetime.date.today()

        lastWorkDate = self.getLastWorkdayOfMonth()
        
        if today == lastWorkDate:
            return True
        else:
            return False

    def isHolidaysComing(self):
        '''
        return True if isHolidaysComing
        '''
        #today = datetime.date(2022, 6, 1)
        oneday=datetime.timedelta(days=1)
        
        today=datetime.date.today()
        
        if not self.isAWorkDay(today + oneday):
            if not self.isAWorkDay(today + oneday + oneday):
                if not self.isAWorkDay(today + oneday + oneday + oneday):
                    return True
        return False

    def getLastWorkdate(self):
        '''
        retrun last work date.
        '''
        today=datetime.date.today()
        oneday=datetime.timedelta(days=1)
        
        #today = datetime.date(2022, 5, 4)
        LastWorkdate=today-oneday
        while True:
            if self.isAWorkDay(LastWorkdate):
                break
            LastWorkdate=LastWorkdate-oneday
        return LastWorkdate

    def getLastWorkWeekday(self):
        '''
        retrun a string of the last weekday.
        '''
        weekday = self.getLastWorkdate().weekday()
        sWeekday = ''
        if weekday == 6:
            sWeekday = '星期日'
        elif weekday == 5:
            sWeekday = '星期六'
        elif weekday == 4:
            sWeekday = '星期五'
        elif weekday == 3:
            sWeekday = '星期四'
        elif weekday == 2:
            sWeekday = '星期三'
        elif weekday == 1:
            sWeekday = '星期二'
        elif weekday == 0:
            sWeekday = '星期一'
        else:
            sWeekday = ''
        return sWeekday

    def getTodayWeekday(self):
        '''
        return a string of today's weekday
        '''
        weekday = datetime.datetime.now().weekday()
        sWeekday = ''
        if weekday == 6:
            sWeekday = '星期日'
        elif weekday == 5:
            sWeekday = '星期六'
        elif weekday == 4:
            sWeekday = '星期五'
        elif weekday == 3:
            sWeekday = '星期四'
        elif weekday == 2:
            sWeekday = '星期三'
        elif weekday == 1:
            sWeekday = '星期二'
        elif weekday == 0:
            sWeekday = '星期一'
        else:
            sWeekday = ''
        return sWeekday

class LocalFile(object):
    def __init__(self):
        '''
        the class is designd for process local file, including some useful process for dailywork.
        '''
        pass
        
    def getModifiedTime(self, fileName):
        '''
        return a fileName's modify time in struct_time format
        '''
        if os.path.exists(fileName):
            local_time = time.localtime(os.path.getmtime(fileName))
        return local_time

    def isModifiedOnToday(self, fileName):
        '''
        return bool Ture if file modified on today.
        '''
        today = datetime.date.today()
        modifyDay = self.getModifiedTime(fileName)

        if today.year == modifyDay.tm_year:
            if today.month == modifyDay.tm_mon:
                if today.day == modifyDay.tm_mday:
                    return True
        return False

class MessageJson(object):
    '''
        Common message template of Qiye.
    '''
    def __init__(self, msg_body): 
        self.dataTextJson = {
            "msgtype": "text",
            "text": {
                "content":msg_body,
                "mentioned_list":["@all"]
            }
        }

        self.dataMarkdownJson = {
            "msgtype": "markdown",
            "markdown": {
                #the longest length of markdown content is 4096byge，must encoding with uft8.
                "content": msg_body,
                "mentioned_list":["@all"]
            }
        }

        #support jpg,png format, the max size cann't exceed 2M before encoding with base64
        self.dataImageJson = {
            "msgtype": "image",
            "image": {
                        #the data of image encoding with base64
                        "base64": "DATA",
                        #the md5 value of raw data before encoding with base64
                        "md5": "MD5"
            }
        }

        #support 1~8 item of news.
        self.dataNewsJson = {
            "msgtype": "news",
            "news": {
               "articles" : [
                   {
                       #max 128byte
                       "title" : "test",
                       "description" : "test",
                       "url" : "www.tapd.cn",
                       #the link of the picture, support jpg,png format, the more looks is 1068*455 for big picture, 150*150 for small picture.
                       "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                   }
                ]
            }
        }

        self.dataFileJson = {
            "msgtype": "file",
            "file": {
                 #get the id by the reture of the uploading interface.
                 "media_id": "3a8asd892asd8asd"
            }
        }

#some useful ommon String
lastWorkDayInfo = ''
if DateTime().isLastWorkdayOfAMonth():
    lastWorkDayInfo = '<font color=\"info\">**今天是月末最后一个工作日，请大家提交今天的日报。**</font>'

everyJiraReport = '\n### 今天是<font color=\"warning\">' + DateTime().getTodaydate() + ' ' + DateTime().getTodayWeekday() + '</font>，' + lastWorkDayInfo + '[点击这里提交西研日报](http://jira.chino-e.com:8080/projects/Z1DR/summary)\n'

todayDateAndWeekday = '今天是' + DateTime().getTodaydate() + ' ' + DateTime().getTodayWeekday() + '，'