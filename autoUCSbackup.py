"""
Script used to create local backup files in the default directory on F5 LTM devices
Dec 2019 - Wedlow

"""
import sys
import os
import datetime
import requests

filePath = os.path.join('/path/to/directory/scripts/logs/', 'autoUCSbackup_log.txt')

def getTime(): #Gets the current time and formats it
        time = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
        return time

def getTimeUCSname(): #Gets the current time and formats it without symbols - Used for UCS name
        time = datetime.datetime.now().strftime("DATE_%m-%d-%y_TIME_%H%M")
        return time

def setLog(str): #Logs to a file and appends newlines
        with open(filePath, 'a+') as logFile:
                logFile.write(getTime() + " : " + str + '\n')
proxies = {
    'http': 'http://ip:port',
    'https': 'https://ip:port',
}
deviceList = [
        '10.x.x.x',
        '10.x.x.x',     
]


def sendTeamsMessage(messageString): #Take a string and pass it to Teams Channel
    try:
        teamsURL = 'https://api.ciscospark.com/v1/messages'
        topkekTeams = 'xxxxxxxxxxxx'
        room = 'xxxxxxxxxxxxxxxx'
        messageText = getTime() + messageString
        headers = {'Authorization': 'Bearer ' + topkekTeams,
                   'Content-type': 'application/json;charset=utf-8'}
        post_data = {'roomId': room,
                     'text': messageText}
        response = requests.post(teamsURL, json=post_data, headers=headers, proxies=proxies)

    except: #Try again with no proxy
        teamsURL = 'https://api.ciscospark.com/v1/messages'
        topkekTeams = 'xxxxxxxxxx'
        room = 'xxxxxxxxxxxxxxx'
        messageText = getTime() + messageString + ' ERROR - no proxy used'

        headers = {'Authorization': 'Bearer ' + topkekTeams,
                   'Content-type': 'application/json;charset=utf-8'}
        post_data = {'roomId': room,
                     'text': messageText}
        response = requests.post(teamsURL, json=post_data, headers=headers)
        logMessage = getTime() + ' : Unable to send Webex Teams Message to xxxxxx'    
        
#Run the API call for UCS backup
def createUCS():
    apiURI_1 = '/mgmt/tm/sys/ucs'
    spongebob = 'xxxxxxxxx' # username
    uselessStringOfNothing = 'xxxxxxx'   # password

    for IP in deviceList:
        UCSname =  getTimeUCSname()
        post_data = {'command': 'save', 'name': UCSname}
        apiCommand1 = 'https://' + IP + apiURI_1
        try:
            response = requests.post(apiCommand1, json=post_data, auth=( spongebob, uselessStringOfNothing ), verify=False)
            if not response.ok:
                print(response.content)
                sendTeamsMessage('UCS backup failed - no HTTP 200/300 recieved for ' + IP)
                setLog('UCS backup failed - no HTTP 200/300 recieved for ' + IP)

        except:
            sendTeamsMessage('UCS backup failed. Unable to send POST request for ' + IP)
            setLog('UCS backup failed. Unable to send POST request for ' + IP)

setLog("Auto UCS Script running")
createUCS()
