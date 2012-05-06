#!/usr/bin/env python
#encoding=utf-8
import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import Request
from google.appengine.api import mail
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
    
#ranks=Rank.gql("order by date desc LIMIT 2")
r=Rank.all().order("-date").fetch(2)
print len(r)
if len(r)==2:
  if r[0].rank<>r[1].rank:
    print "send email"
    mail.send_mail(sender="frederick.mao@gmail.com",
                  to="maolingzhi@gmail.com",
                  subject="[GAE]博客园排名升至"+str(r[0].rank)+"位",
                  body="""
    Dear mao:
    
    your blog rank from %s to %s,good job!
    """%(r[0].rank,r[1].rank))
  else:
    print "the same 22"
else:
  print "the same"
        