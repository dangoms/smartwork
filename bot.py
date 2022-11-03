#! /usr/bin/python
# -*-coding:utf-8-*-

import sys
import smartwork

content = ' <font color=\"info\">**小娜 温馨提示：请各领域使用WBS下发工作任务。**</font>\n'

def main():
    msgBody = \
             smartwork.todayDateAndWeekday + \
             content

    msgMarkdown = smartwork.MessageJson(msgBody).dataMarkdownJson
    
    #test url
    testUrl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2b64b834-f3f1-43e7-825f-c20e11bbb532'

    #post message
    if smartwork.DateTime().isWorkday():
        resp = smartwork.httpPost3(testUrl,msgMarkdown)
        print (resp)

if __name__ == "__main__":
    main()
    exit(0)
