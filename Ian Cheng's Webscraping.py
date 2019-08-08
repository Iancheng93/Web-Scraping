#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 02:13:13 2019

@author: Ian Cheng
"""

import requests 
import re

data = []
link = 'http://www.ilga.gov/legislation/'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

r = requests.get(link,headers=headers)

x = r'grplist.asp\?num1=([0-9]*)&num2=([0-9]*)&DocTypeID=[SH]B&GA=101&SessionId=108'
m_findall = re.findall(r'(grplist.asp\?num1=[0-9]*&num2=[0-9]*&DocTypeID=[SH]B&GA=101&SessionId=108)',r.text)


for i1 in m_findall:
    link1 = 'http://www.ilga.gov/legislation/'+i1
    r = requests.get(link1,headers=headers)
    x = r'<a href="/legislation/(BillStatus.asp\?.*?)">'
    m_findall_set = re.findall(x,r.text)
    for i in m_findall_set:
        link2 = 'http://www.ilga.gov/legislation/'+i
        r = requests.get(link2,headers=headers)
        chamber = re.findall('<span class="heading">Bill Status of ([SH]B)',r.text)
        bill_number = re.findall('<span class="heading">Bill Status of [SH]B([0-9]*)',r.text)
        b_act = bool(re.findall('width="75%" align="left">(Public Act)',r.text))
        n_amendment = re.findall('Floor Amendment No. ([0-9]*)</b>',r.text)
        n_amendment = len(n_amendment)
    
    ##### calculate the number of D and R
        n_D = 0
        n_R = 0
    
        m_findall_senate = re.findall(r'href="/(senate/Senator.asp\?MemberID=[0-9]*)',r.text)
#        print(m_findall_senate)
        for i5 in m_findall_senate:
            link3 = 'http://www.ilga.gov/'+ i5
            r = requests.get(link3,headers=headers)
            if re.findall('\(D\)</span>',r.text):
                n_D = n_D +1
            if re.findall('\(R\)</span>',r.text):
                n_R = n_R +1
            
        m_findall_house = re.findall(r'href="/(house/Rep.asp\?MemberID=[0-9]*)',r.text)
#        print(m_findall_house)
        for i5 in m_findall_house:
            link3 = 'http://www.ilga.gov/'+ i5
            r = requests.get(link3,headers=headers)
            if re.findall('\(D\)</span>',r.text):
                n_D = n_D +1
            if re.findall('\(R\)</span>',r.text):
                n_R = n_R +1
            
    ###### amendent        
        line = [chamber,bill_number,b_act,n_amendment,n_D,n_R] 
        print(line)
        data.append(line)

