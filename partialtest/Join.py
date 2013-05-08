import os
import sys
import swlib

def Check1(num1, num2):
    if num1 * num2 > 900 * 900:
        return True
    else:
        return False

def Check2(num1, num2):
    if num1 * num2 > 900 * 900 * 900 * 900:
        return True
    else:
        return False

def Join(sw):
    taskname = sw.GetName()
    msglist  = sw.GetMsgList()
    todo = 1000
    listprogress = {}
    thelist = {}
    outputlist = []

    for item in msglist:
        
        dmsg = sw.GetMsg(item)
        
        if dmsg["body"]["type"] == "old":
            if not thelist.has_key(int(dmsg["body"]["ident"])):
                thelist[int(dmsg["body"]["ident"])] = []
            thelist[int(dmsg["body"]["ident"])] += dmsg["body"]["values"]

            try:
                dmsg["body"]["starting"]
            except NameError:
                listprogress[int(dmsg["body"]["ident"])] = 0
            except KeyError:
                listprogress[int(dmsg["body"]["ident"])] = 0
            else:
                listprogress[int(dmsg["body"]["ident"])] = int(dmsg["body"]["starting"])

    for item in msglist:
        dmsg = sw.GetMsg(item)
        if dmsg["body"]["type"] == "new":
            if not thelist.has_key(int(dmsg["body"]["ident"])):
                thelist[int(dmsg["body"]["ident"])] = []
            thelist[int(dmsg["body"]["ident"])] += dmsg["body"]["values"]

            if not listprogress.has_key(int(dmsg["body"]["ident"])):
                listprogress[int(dmsg["body"]["ident"])] = 0
#    sw.flog.write('stuff : ' + item + "\n")
#    sw.flog.flush()
            

    sw.flog.write("TheList      = " + str(thelist) + "\n")
    sw.flog.write("ListProgress = " + str(listprogress) + "\n")
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
            if (int(taskname.split("-", 1)[1]) <  2 and Check1(thelist[which][listprogress[which]], thelist[1 - which][j])) or \
               (int(taskname.split("-", 1)[1]) == 2 and Check2(thelist[which][listprogress[which]], thelist[1 - which][j])):
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
            dmsgout["body"]["ident"]     = a
            dmsgout["body"]["type"]      = "old"
            dst                          = taskname.split("-", 1)[1]
            sw.Send(dst, dmsgout, "1")

    sw.flog.write("Output list = " + str(outputlist) + "\n")
    sw.flog.flush()
    dmsgout = {}
    dmsgout["src"]            = taskname
    dmsgout["cmd"]            = "join"
    dmsgout["body"]           = {}
    dmsgout["body"]["values"] = outputlist
    dmsgout["body"]["ident"]  = taskname.split("-", 1)[1]
    dmsgout["body"]["type"]   = "new"
    if int(taskname.split("-", 1)[1]) < 2:
        dst = 2
        sw.Send(dst, dmsgout, "1")
    else:
        dst = 0
        sw.Send(dst, dmsgout, "2")

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
