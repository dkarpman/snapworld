import os
import sys
import swlib

def Check(num1, num2):
    if num1 * num2 > 900 * 900:
        return True
    else:
        return False

def Join(sw):
    taskname = sw.GetName()
    msglist  = sw.GetMsgList()
    todo = 1000
    listprogress = []
    thelist = {}
    outputlist = []

    for item in msglist:
        sw.flog.write('stuff : ' + item + "\n")
        sw.flog.flush()
        dmsg = sw.GetMsg(item)
        thelist[int(dmsg["body"]["ident"])].append(dmsg["body"]["values"])
        try:
          dmsg["body"]["starting"]
        except NameError:
          listprogress.append(0)
        except KeyError:
          listprogress.append(0)
        else:
          listprogress.append(dmsg["body"]["starting"])
   
    sw.flog.write("Thelist = " + str(thelist) + "\n")
    sw.flog.flush()
    i = 0

    while i < todo and \
          listprogress[0] < len(thelist[0]) and \
          listprogress[1] < len(thelist[1]) and \
          not (thelist[0][listprogress[0]] == -1 and \
               thelist[1][listprogress[1]] == -1):
        which = 0 
        if listprogress[which] > listprogress[1 - which] or \
           thelist[which][listprogress[which]] == 0:
           which = 1
          
        for j in range(0, listprogress[1 - which]):
            i += 1
            if Check(thelist[which][listprogress[which]], thelist[1 - which][j]):
                outputlist.append(thelist[which][listprogress[which]] * thelist[1 - which][j])
        
        listprogress[which] += 1
    
    
    if thelist[0][listprogress[0]] == -1 and thelist[1][listprogress[1]] == -1:
        # I do some sort of stuff here
        sw.flog.write("i'm done")
        sw.flog.flush()
        outputlist.append(-1)
    else:
        for a in range(0, 2):
            dmsgout                      = { }
            dmsgout["src"]               = taskname
            dmsgout["cmd"]               = "join"
            dmsgout["body"]              = { }
            dmsgout["body"]["values"]    = thelist[a]
            dmsgout["body"]["starting"]  = listprogress[a]
            dst                          = taskname.split("-", 1)[1]
            sw.Send(dst, dmsgout, "1")

    sw.flog.write("Output list = " + str(outputlist) + "\n")
    sw.flog.flush()

    dmsgout = {}
    dmsgout["src"] = taskname
    dmsgout["cmd"] = "join"
    dmsgout["body"] = {}
    dmsgout["body"]["values"] = outputlist
    dst = 2
    sw.Send(dst, dmsgout, "1")

def Worker(sw):
    Join(sw)
    
if __name__ == '__main__':
    sw = swlib.SnapWorld()
    sw.Args(sys.argv)

    fname = "log-swwork-%s.txt" %(sw.GetName())
    flog  = open(fname, "a")

    sw.SetLog(flog)
    sw.GetConfig()

    Worker(sw)
