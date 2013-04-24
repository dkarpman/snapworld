import httplib
import urllib2

def config(server):
    # get configuration
    url = "http://%s/config" % (server)
    f = urllib2.urlopen(url)
    sconf = f.read()
    f.close()

    return sconf

def step(server):
    # send step start
    url = "http://%s/step" % (server)

    #print "step", server

    f = urllib2.urlopen(url)
    body = f.read()
    f.close()

def getexec(server,prog,timestamp):
    '''
    get executable from the head task
    - return values
        "", no change
        <body>, new content
        None, no file found
    '''

    # send a request for executable
    if not timestamp:
        url = "http://%s/exec?p=%s" % (server, prog)
    else:
        url = "http://%s/exec?p=%s&t=%s" % (server, prog, str(timestamp))

    print "exec", server, prog, timestamp

    httpcode = 200
    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        httpcode = e.code

    if httpcode == 304:
        return ""

    if httpcode != 200:
        return None

    body = f.read()
    f.close()

    return body

def quit(server):
    # send termination quit
    url = "http://%s/quit" % (server)

    #print "step", server

    f = urllib2.urlopen(url)
    body = f.read()
    f.close()

def dummy(server):
    # send a dummy request
    url = "http://%s/dummy" % (server)

    #print "step", server

    f = urllib2.urlopen(url)
    body = f.read()
    f.close()

def prepare(server):
    # send step prepare
    url = "http://%s/prepare" % (server)
    f    = urllib2.urlopen(url)
    body = f.read()
    f.close()

def done(server, id):
    # send done
    url  = "http://%s/done/%s" % (server,id)
    f    = urllib2.urlopen(url)
    body = f.read()
    f.close()

def ready(server, id, numtasks=0):
    # send ready
    url = "http://%s/ready/%s/%s" % (server,id,str(numtasks))
    f    = urllib2.urlopen(url)
    body = f.read()
    f.close()

def message(server, src, dst, body):
    # send a task message from src to dst
    url = "http://%s/msg/%s/%s" % (server,dst,src)
    length = len(body)

    print "message url", url

    request = urllib2.Request(url, data=body)
    request.add_header('Content-Length', '%d' % length)
    f    = urllib2.urlopen(request)
    body = f.read()
    f.close()

def messagevec(server, src, dst, Vec):
    h = httplib.HTTPConnection(server)
    h.connect()
    url = "/msg/%s/%s" % (dst,src)
    h.putrequest("POST",url)
    h.putheader("Content-Length", str(Vec.GetMemSize()))
    h.endheaders()

    fileno = h.sock.fileno()
    n      = Vec.Send(fileno)
    res    = h.getresponse()
    data   = res.read()
    h.close()

