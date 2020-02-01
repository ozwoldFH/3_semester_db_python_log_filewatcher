# ------------------------------------------------------------------------
# first you need to get pymysql packacke for python 3
# it is important to use python version 3! python 2.* was not tested!
# please run if not installed: command "pip3 install pymysql"

# ------------------------------------------------------------------------
# imports
import pymysql
from pathlib import Path
from datetime import datetime
from datetime import timedelta  
import sys
import csv
import os

# ------------------------------------------------------------------------
# global variables
host="localhost"
user="user_logger"
passwd="kW^!TccDnRU@&6*%^@iW$aBDdJrTXe8#%HnA8mQx@3FdjBf&Jep4z6RBKanN35TU"
selectedDatabase="db_logs"
locationToWatch=Path("testfolder/folderWithLogs/")
logFileName="log.log"
nDaysToRemoveFiles = 2
logDelimiter=";"
logEndWith=".log"


# ------------------------------------------------------------------------
# class
class LogLine:
  def __init__(self, log_datetime, pc_name, name, a, b):
    self.log_datetime = log_datetime
    self.pc_name = pc_name
    self.name = name
    self.a = a
    self.b = b


# ------------------------------------------------------------------------
# functions
def connectToDatabase():
  # try to connect
  try:
    return pymysql.connect(host, user, passwd, selectedDatabase)
  except Exception as e:
    print("error while connection to db:", e)

def closeDatabaseConnectionAndExitScript():
  mydb.close
  sys.exit(0)

def getYesterdaysLogFileName():
  return (datetime.now() - timedelta(days=1)).strftime("%Y%m%d") + logEndWith

def getTodaysLogFileName():
  return datetime.now().strftime("%Y%m%d") + logEndWith

def doesFileExists(locationPath, filename):
  return Path.exists(locationPath / filename)

def onErrorWriteDB(errorMessage="something went wrong"):
  try:
    data = (errorMessage)
    sql = "INSERT INTO T_OnError (message) VALUES(%s);"
    with mydb.cursor() as cursor:
      cursor.execute(sql, data)
      mydb.commit()
  except Exception as e:
    print("error while db operation:", e)
    mydb.rollback()

def getLatestDatetimeFromDB():
  try:
    sql = "CALL P_getLatestDatetimeFromSuccessOrError();"
    with mydb.cursor() as cursor:
      cursor.execute(sql)
      return cursor.fetchone()
  except Exception as e:
    print("error while db operation:", e)

def onSuccessWriteDB(logLineObject: LogLine):
  try:
    data = (logLineObject.log_datetime, logLineObject.pc_name, logLineObject.name, logLineObject.a, logLineObject.b)
    sql = "INSERT INTO T_OnSuccess (log_datetime, pc_name, name, a, b) VALUES(%s, %s, %s, %s, %s);"
    with mydb.cursor() as cursor:
      cursor.execute(sql, data)
      mydb.commit()
  except Exception as e:
    print("error while db operation:", e)
    mydb.rollback()

def readFileAndWriteDBforEachLine(lastDatetime):
  try:
    with open(locationToWatch / logFileName) as f:
      for line in csv.reader(f, delimiter=logDelimiter):
        log_datetime = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S.%f')
        if(log_datetime <= lastDatetime):
          print("log: " + str(log_datetime) + "last: " + str(lastDatetime))
          continue
        
        # hotfix
        emptyArray = [''] * 10
        for i in range(len(line)):
          emptyArray[i] = line[i]

        logLineObject = LogLine(log_datetime, emptyArray[1], emptyArray[2], emptyArray[3], emptyArray[4])
        onSuccessWriteDB(logLineObject)
        #print(logLineObject.log_datetime, logLineObject.pc_name, logLineObject.name, logLineObject.a, logLineObject.b)
  except Exception as e:
    onErrorWriteDB("error while reading: " + str(e))

def removeLogFilesOlderNDays(n):
  # remove files which are older than n days
  old_time = datetime.now() - timedelta(days=n)
  for f in os.scandir(locationToWatch):
    if f.name.endswith(logEndWith):
      creation_time = datetime.fromtimestamp(os.path.getctime(f))
      if (creation_time < old_time):
          os.unlink(f)


# ------------------------------------------------------------------------
# execution script
# 1. connect first
mydb = connectToDatabase()
# 2. read files from yesterday so we dont miss any information
logFileName = getYesterdaysLogFileName()
if doesFileExists(locationToWatch, logFileName) == True:
  lastDatetime = getLatestDatetimeFromDB()[0]
  readFileAndWriteDBforEachLine(lastDatetime)
# 3. continue with files from today
logFileName = getTodaysLogFileName()
if doesFileExists(locationToWatch, logFileName) == False:
  onErrorWriteDB("file not found")
  closeDatabaseConnectionAndExitScript()
lastDatetime = getLatestDatetimeFromDB()[0]
readFileAndWriteDBforEachLine(lastDatetime)
# 4. remove old log files 
removeLogFilesOlderNDays(nDaysToRemoveFiles)
# 5. close connection
closeDatabaseConnectionAndExitScript()