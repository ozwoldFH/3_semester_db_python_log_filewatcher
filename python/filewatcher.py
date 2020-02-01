# ------------------------------------------------------------------------
# first you need to get pymysql packacke for python 3
# it is important to use python version 3! python 2.* was not tested!
# command "pip3 install pymysql"

# ------------------------------------------------------------------------
# imports
import pymysql
from pathlib import Path
import time


# ------------------------------------------------------------------------
# global variables
host="localhost"
user="user_logger"
passwd="kW^!TccDnRU@&6*%^@iW$aBDdJrTXe8#%HnA8mQx@3FdjBf&Jep4z6RBKanN35TU"
locationToWatch=Path("testfolder/folderWithLogs/")
logName="log.txt"

# ------------------------------------------------------------------------
# functions
def connectToDatabase():
  # try to connect
  try:
    return pymysql.connect(host, user, passwd)
  except Exception as e:
    print('error while connection to db:', e)

def getTodaysLogFileName():
  return time.strftime("%Y%m%d") + ".txt"

def doesFileExists():
  print(Path.exists(locationToWatch / logName))
  return Path.exists(locationToWatch / logName)

# ------------------------------------------------------------------------
# execution script
mydb = connectToDatabase()
logName = getTodaysLogFileName()
if doesFileExists():
  print("BINGO")
else:
  print("sad")






mydb.close