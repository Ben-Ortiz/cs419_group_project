import select

import socket

 

# Class representing a log file

class LogFile:

  

    def __init__(self, logFileName, logFile, descriptor):

        self.myLogFileName  = logFileName

        self.myLogFile      = logFile

        self.myDescriptor   = descriptor

 

# List of log files

logFiles    = []

 

file        = open("LogFile1.txt", "w")

logFile1    = LogFile("LogFile1.txt", file, file.fileno())

logFiles.append(logFile1)

 

file        = open("LogFile2.txt", "w")

logFile2    = LogFile("LogFile2.txt", file, file.fileno())

logFiles.append(logFile2)

 

file        = open("LogFile3.txt", "w")

logFile3    = LogFile("LogFile3.txt", file, file.fileno())

logFiles.append(logFile3)

 

# List of descriptors for read, write and exception conditions

rdescriptors    = []

wdescriptors    = []

xdescriptors    = []

 

# Add the write descriptors to the write descriptor list

for log in logFiles:

    wdescriptors.append(log.myDescriptor)

 

# Wait for write condition

rlist, wlist, xlist = select.select(rdescriptors, wdescriptors, xdescriptors)

 

print("Number of descriptors ready for write %d"%(len(wlist)))

 

# Write to all the logs that are ready

for writeDescriptor in wlist:

    for log in logFiles:

        if log.myDescriptor is writeDescriptor:

            log.myLogFile.write("Starting to log events")