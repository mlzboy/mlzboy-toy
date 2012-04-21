#!/usr/bin/env python
#encoding=utf-8
import bottle
from bottle import route, default_app
from google.appengine.ext.webapp.util import run_wsgi_app
from bottle import route, run,redirect,request
t=""
html="""
<html>bottle.run(server='gae')
<title>life is tough,use python~</title>
<body>
<form name="form1" action="/" method="post">
<textarea name="t" cols="80" rows="25">%s</textarea>
<input type="submit" name="sub" value="save" />
</form>
</body>
</html>
"""
from google.appengine.ext import db
class Pastebin(db.Model):
  content   = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


#@route('/',method=["POST","GET"])
@route('/',method=["POST"])
def index():
    global t,html
    t=request.POST.get("t")
    #print t
    if Pastebin.all().count()==0:
        p=Pastebin(content=t)
    else:
        p=Pastebin.all().order("-date").fetch(1)[0]
        p.content=t
    p.put()
    return html%t

@route('/')
def index():
    global t,html
    #print t
    t=db.GqlQuery("SELECT * FROM Pastebin order by date desc limit 1")
    if t.count()==0:
        p=Pastebin(content="")
        p.put()
        redirect("/")
    #print t
    #print type(t)
    #print t[0].content
    return html%t[0].content

#run(host='localhost', port=8084)
#bottle.run(server='gae')
bottle.debug(True)
app = default_app()
run_wsgi_app(app)