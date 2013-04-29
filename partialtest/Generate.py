import os
import sys
import swlib

# We ignore the max task length here

def Generate(sw):
    taskname = sw.GetName()
    nlists = int(sw.GetVar("lists"))
    tsize = sw.GetRange()
    ns = 0
    while ns < nlists:
        

def Worker(sw):
  Generate(sw)

if __name__ == '__main__':
    sw = swlib.SnapWorld()
    sw.Args(sys.argv)
    fname = "log-swwork-%s.txt" %(sw.GetName())
    flog  = open(fname, "a")
    sw.SetLog(flog)
    sw.GetConfig()
    Worker(sw)
