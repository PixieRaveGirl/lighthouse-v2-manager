#!/usr/bin/env python3

import asyncio
import sys
import re
import os
import signal
#import lighthouse-v2-manager

import subprocess


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

processName = 'vrcompositor.exe'#'notepad.exe'
isRunning = 0 if process_exists(processName) else 1 #This will be backwards so that it runs off or on correctly
pid = str(os.getpid())
pidfile = "mydaemonsteamvr.pid"

pidLightHouseManager = 0



print(" ".join(sys.argv[2:]))
lh_macs = " ".join(sys.argv[2:])

if os.path.isfile(pidfile):
	f = open(pidfile, 'r')
	pid = f.read()
	print("SteamVR Manager is already running "+ pid)
	try:
		print("Closing Other SteamVR Manager"+ pid)
		os.kill(int(pid), signal.SIGTERM)
	except:
		print("Failed to close "+ pid + " probaby doesn't exist.. continuing...")
		pass
	#sys.exit()
open(pidfile, 'w').write(pid)
try:
    while 1:
        if(process_exists(processName) and isRunning == 0):
            isRunning = 1
            print("SteamVR is Running")
            # Do some actual work here
            #subprocess.Popen("python lighthouse-v2-manager.py on C7:61:9F:18:BF:B2 D0:60:D2:2D:C1:C8 D7:96:07:E9:10:19 DF:9D:A3:04:1E:02 D1:DA:66:D4:24:57",creationflags=subprocess.CREATE_NEW_CONSOLE)
            #flags = 0
            #flags |= 0x00000200  # CREATE_NEW_PROCESS_GROUP
            #flags |= 0x00000010  # CREATE_NEW_CONSOLE
            #flags |= 0x00000008  # DETACHED_PROCESS
            #subprocess.Popen([sys.executable, "lighthouse-v2-manager.py on C7:61:9F:18:BF:B2 D0:60:D2:2D:C1:C8 D7:96:07:E9:10:19 DF:9D:A3:04:1E:02 D1:DA:66:D4:24:57"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **{'creationflags': flags})
            try:
                print("Closing Other LightHouse Manager "+ pid)
                os.kill(int(pidLightHouseManager), signal.SIGTERM)
            except:
                print("Failed to close "+ pid + " probaby doesn't exist.. continuing...")
                pass
            
            if (sys.argv[1] == 'true'):
                pidLightHouseManager = subprocess.Popen("python lighthouse-v2-manager.py on "+lh_macs,creationflags=subprocess.CREATE_NEW_CONSOLE).pid
            else:
                pidLightHouseManager = subprocess.run("python lighthouse-v2-manager.py on "+lh_macs, creationflags=subprocess.CREATE_NEW_CONSOLE).pid
        elif(not process_exists(processName) and isRunning == 1):
            isRunning = 0
            print("SteamVR is Not Running")
            #subprocess.Popen("python lighthouse-v2-manager.py off C7:61:9F:18:BF:B2 D0:60:D2:2D:C1:C8 D7:96:07:E9:10:19 DF:9D:A3:04:1E:02 D1:DA:66:D4:24:57",creationflags=subprocess.CREATE_NEW_CONSOLE)
            #flags = 0
            #flags |= 0x00000200  # CREATE_NEW_PROCESS_GROUP
            #flags |= 0x00000010  # CREATE_NEW_CONSOLE
            #flags |= 0x00000008  # DETACHED_PROCESS
            #subprocess.Popen([sys.executable, "lighthouse-v2-manager.py on C7:61:9F:18:BF:B2 D0:60:D2:2D:C1:C8 D7:96:07:E9:10:19 DF:9D:A3:04:1E:02 D1:DA:66:D4:24:57"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **{'creationflags': flags})
            
            try:
                #print("Closing Other LightHouse Manager "+ pid)
                os.kill(int(pidLightHouseManager), signal.SIGTERM)
            except:
                #print("Failed to Close "+ pid + " Probaby Doesn't Exist.. Continuing...")
                pass

            if (sys.argv[1] == 'true'):
                pidLightHouseManager = subprocess.Popen("python lighthouse-v2-manager.py off "+lh_macs,creationflags=subprocess.CREATE_NEW_CONSOLE).pid
            else:
                pidLightHouseManager = subprocess.run("python lighthouse-v2-manager.py off "+lh_macs, creationflags=subprocess.CREATE_NEW_CONSOLE).pid
finally:
	os.unlink(pidfile)