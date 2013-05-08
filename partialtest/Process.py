import os
import sys
import random
import swlib

def GenerateList(sw):
    taskname = sw.GetName()
    msglist  = sw.GetMsgList()
    sw.flog.write("msglist " + str(msglist) + "\n")
    sw.flog.flush()
    for item in msglist:
        dmsg = sw.GetMsg(item)

        sw.flog.write("dmsg " + str(dmsg) + "\n")
        sw.flog.flush()

        ns = dmsg["body"]["s"]
        ne = dmsg["body"]["r"] + ns

        i = ns
        randlist = []
        while i < ne:
            randlist.append(random.randint(1, 1000))
            i = i + 1
        # -1 is what is used for End Of Stream
        randlist.append(-1) 
    dmsgout                      = {}
    dmsgout["src"]               = taskname
    dmsgout["cmd"]               = "join"
    dmsgout["body"]              = {}
    dmsgout["body"]["values"]    = randlist
    dmsgout["body"]["ident"]     = int(taskname.split("-", 1)[1]) %2
    dmsgout["body"]["type"]      = "new"
#    dmsgout["body"]["starting"]  = 0
    # Hard-coded funnel
    dst     = int(int(taskname.split("-", 1)[1]) / 2)
#    port    = int(taskname.split("-", 1)[1]) % 2  
    sw.Send(dst, dmsgout)

def Worker(sw):
    GenerateList(sw)

if __name__ == '__main__':
    sw = swlib.SnapWorld()
    sw.Args(sys.argv)
    fname = "log-swwork-%s.txt" % (sw.GetName())
    flog  = open(fname, "a")
    sw.SetLog(flog)
    sw.GetConfig()
    Worker(sw)
