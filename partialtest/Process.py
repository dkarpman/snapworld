import os
import sys
import swlib

def GenerateList(sw):
    taskname = sw.GetName()
    msglist  = sw.GetMsgList()
    sw.flog.write("msglist " + str(msglist) + "\n")
    sw.flog.flush()
    for item in msglist:
        dmsg = sw.GetMsg(item)

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
