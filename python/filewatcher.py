# ------------------------------------------------------------------------
# first you need to get pymysql packacke for python 3
# it is important to use python version 3! python 2.* was not tested!
# command "pip3 install pymysql"

# ------------------------------------------------------------------------
# imports
import pymysql
from pathlib import Path
import time
import sys


# ------------------------------------------------------------------------
# global variables
host="localhost"
user="user_logger"
passwd="kW^!TccDnRU@&6*%^@iW$aBDdJrTXe8#%HnA8mQx@3FdjBf&Jep4z6RBKanN35TU"
selectedDatabase="db_logs"
locationToWatch=Path("testfolder/folderWithLogs/")
logFileName="log.txt"


# ------------------------------------------------------------------------
# functions
def connectToDatabase():
  # try to connect
  try:
    return pymysql.connect(host, user, passwd, selectedDatabase)
  except Exception as e:
    print('error while connection to db:', e)

def closeDatabaseConnectionAndExitScript():
  mydb.close
  sys.exit(0)


def getTodaysLogFileName():
  return time.strftime("%Y%m%d") + ".txt"

def doesFileExists(locationPath, filename):
  return Path.exists(locationPath / filename)

def onErrorWriteDB(errorMessage="something went wrong"):
  try:
    data = (errorMessage)
    sql = "INSERT INTO T_OnError (message) VALUES(%s)"
    with mydb.cursor() as cursor:
      e = cursor.execute(sql, data)
      mydb.commit()
  except Exception as e:
    print('error while db operation:', e)
    mydb.rollback() # if anything went wrong, rollback database


# ------------------------------------------------------------------------
# execution script
mydb = connectToDatabase()
logFileName = getTodaysLogFileName()
if doesFileExists(locationToWatch, logFileName) == False:
  onErrorWriteDB("file not found")
  closeDatabaseConnectionAndExitScript()







closeDatabaseConnectionAndExitScript()