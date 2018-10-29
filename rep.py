# -*- coding: utf-8 -*-

def onQQMessage(bot, contact, member, content):
    import requests
    from lxml import etree
    import sys
    import io
    import re
    import datetime
    date = datetime.datetime.now().isocalendar()
    # date = (2018,43,5)

    data = {'txtUserName':'2018001970','txtPassWord':'121014','Button1':'登录','__VIEWSTATE':'/wEPDwUJMTQyNDg3OTM5ZGQ=','__EVENTVALIDATION':'/wEWBAK4vfWFDAKl1bKzCQK1qbSWCwKM54rGBg=='}
    y = '20181'
    c = '1805114'
    url = 'http://jwgl.cust.edu.cn/teachweb/kbcx/Report/wfmRptLessonByClass.aspx?year=' + y + '&classInfoName=' + c
    w = date[1] - 33
    du = ''
    if w % 2 == 1:
        du = '单周'
    else:
        du = '双周'
    req = requests.get(url)
    html = req.content.decode("utf-8")
    ehtml = etree.HTML(html)
    vz = 2
    ke = 0
    xq = 0
    sche = {}
    myclass = 114

    for xq in range(5):
        xq += 1
        kes = {}
        for ke in range(5):
            jps = ehtml.xpath('//table[@cellspacing="0"]/tr[%d]/td[%d]/table/tr/td/text()'%(ke+2,xq+1))
            for jp in jps:
                min = 0
                max = 0
                t = 0
                jp = str(jp)
                jp1 = re.search('\d.*\d.*',jp)
                jp2 = jp1.group().split('. ')
                jp3 = re.search('\d*-\d*',jp2[4])
                jp5 = re.search('[^x00-xff]{2}$',jp2[4])
                if jp5 == None or jp5.group() == du:
                    if jp3 != None:
                        jp31 = re.search('\d+',jp3.group())
                        jp32 = jp3.group().replace(jp31.group()+'-','')
                        wmin = int(jp31.group())
                        wmax = int(jp32)
                        jp4 = re.search('\d{3}-\d{3}',jp2[0])
                        jp40 = re.search('\d*$',jp2[0])
                        if jp4 != None:
                            jp41 = re.search('\d+',jp4.group())
                            jp42 = jp4.group().replace(jp41.group()+'-','')
                            cmin = int(jp41.group())
                            cmax = int(jp42)
                            if not(cmin <= myclass <= cmax):
                                continue
                        elif jp40.group() == '':
                            continue
                        subject = {}    
                        if wmin <= w <= wmax:
                            ke += 1
                            subject['subject'] = jp2[1]
                            subject['teacher'] = jp2[2]
                            subject['class'] = jp2[3]
                            kes[ke] = subject
                            break
                            # sche[xq] = 
                    else:
                        jp3 = re.search('\d*',jp2[4])
                        t = int(jp3.group())
                        if w == t:
                            subject['subject'] = jp2[1]
                            subject['teacher'] = jp2[2]
                            subject['class'] = jp2[3]
                            kes[ke] = subject
                            break
                else:
                    continue
        sche[xq] = kes
    SCH = ''
    if date[2] <6 :
        for key in sche[date[2]]:
            sc = sche[date[2]][key]
            SCH = SCH + '第' + str(key) + '节：' + sc['subject'] + '-' + sc['class'] + '\n'
    else :
        SCH = '同学今天没有课，休息一下吧！'
    # print(SCH)
    if content == '课程表':
        bot.SendTo(contact, SCH)
    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()