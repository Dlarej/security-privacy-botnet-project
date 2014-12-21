#!/usr/bin/pyhton

import sys

profileInfo = {}
profileReasons = {}
reasons = []
reasonsCounter = {}

if len(sys.argv) == 2:
    file_in = open(str(sys.argv[1]), 'r')
    file_out = open('_analyze_'+str(sys.argv[1]).replace('.csv',''), 'w')
    for line in file_in:
        splitter = line.split('Reasons:')
        userInfo = splitter[0]
        reason = splitter[1]
        currentID = ''
        userInfo = userInfo.replace(' ','')
        userInfo = userInfo.split(',')
        currentID = userInfo[0]
        if currentID not in profileInfo:
            profileInfo[currentID] = userInfo[1]
            profileReasons[currentID] = []
        x=0 
        reason = reason.replace(' ','')
        reason = reason.replace('\n','')
        reason = reason.split(',')
        for r in reason:
            if r == '':
                reason.remove(r)
        toStore = list(set(reason) | set(profileReasons[currentID]))
        profileReasons[currentID] = toStore
    # Starting mining data
    for userID in profileInfo:
        file_out.write(userID+': '+profileInfo[userID]+'\n')
        file_out.write('-----Reasons----\n')
        for r in profileReasons[userID]:
            file_out.write(r+'\n')
            if r not in reasonsCounter:
                reasonsCounter[r] = 0
            reasonsCounter[r] = reasonsCounter[r] + 1
        file_out.write('----------------\n\n')

    file_out.write('\n\n-----Summary-----\n')
    for reason in reasonsCounter:
        file_out.write(reason+' '+str(reasonsCounter[reason])+'\n')
    file_out.write('-----------------\n')
else:
    print("Usage: <fakes_file.csv>")
