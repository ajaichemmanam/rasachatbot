import os.path
from os import path
import time
import json


def log(chats):
    logDirectory = 'chatHistoryLogs'  # file directory to save log files
    # time format for naming the file based on the date
    timestr = time.strftime("%d-%b-%Y")

    # Check if the log files directory exists or not, else create the directory
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)

    logFileName = os.path.abspath(logDirectory+"/"+timestr+'.json')  # log file path
    print("Logs in",logFileName)
    print("Logs in", os.path.isfile(logFileName))
    chatsData = []  # variable to hold the chats data before we log the data to file
    if not os.path.isfile(logFileName):
        chatsData.append(chats)
        with open(logFileName, mode='w') as f:
            f.write(json.dumps(chatsData, indent=2))
    else:
        with open(logFileName) as logsData:
            chatLogs = json.load(logsData)

        chatLogs.append(chats)
        with open(logFileName, mode='w') as f:
            f.write(json.dumps(chatLogs, indent=2))
