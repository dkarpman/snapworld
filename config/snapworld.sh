#!/bin/bash

export SNAPWBIN=${HOME}/Research/work
export SNAPWEXEC=${HOME}/Research/snapwexec
export SNAPWOUTPUT=${HOME}/Research/snapwexec
export PYTHON=python

SNAPWID=$1
SNAPWPORT=$2
SNAPWMASTER=$3
SNAPWMASTERPORT=$4

echo $SNAPREMOTE $SNAPWID $SNAPWPORT $SNAPWMASTER $SNAPWMASTERPORT
echo ${PYTHON} ${SNAPWBIN}/host.py -d -i ${SNAPWID} -p ${SNAPWPORT} -m ${SNAPWMASTER}:${SNAPWMASTERPORT}
${PYTHON} ${SNAPWBIN}/host.py -d -i ${SNAPWID} -p ${SNAPWPORT} -m ${SNAPWMASTER}:${SNAPWMASTERPORT} >> ${SNAPWEXEC}/log-snapw-host-${SNAPWPORT}.txt 2>&1

#SNAPWBIN=/home/rok/git/rok/snapworld
#SNAPWEXEC=/home/rok/snapwexec
#python2.6 /lfs/1/tmp/rok/snapworld/host.py -d -i %s -p %s -m %s:%s

