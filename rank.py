#!/usr/bin/env python
#encoding=utf-8
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import Request
import os

class Rank(db.Model):
  rank = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  ip   = db.StringProperty()


print 'Content-Type: text/plain'
print os.environ["REMOTE_ADDR"]
import urllib2
subject=urllib2.urlopen("http://www.cnblogs.com/AllBloggers.aspx").read()
import re
result = re.findall(r'<small>(\d+)[\s\S]*?</small><a href="http://www.cnblogs.com[\s\S]*?">([\s\S]*?)</a>', subject)
for elem in result:
    if elem[1].strip()=="lexus":
        print elem[0]

        rank=Rank(rank=int(elem[0].strip()),ip=os.environ["REMOTE_ADDR"])
        rank.put()

print "*"*30
q = Rank.all().count()
print q

for r in Rank.all().order("-date"):
    print r.rank,r.date,r.ip
        