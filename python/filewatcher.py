#####################################################################
# first you need to get pymysql packacke for python 3
# it is important to use python version 3! python 2.* was not tested!
# command "pip3 install pymysql"

import pymysql

#####################################################################
# global variables
host="localhost"
user="user_logger"
passwd="kW^!TccDnRU@&6*%^@iW$aBDdJrTXe8#%HnA8mQx@3FdjBf&Jep4z6RBKanN35TU"



try:
  mydb = pymysql.connect(host, user, passwd)
  print('hi')
  mydb.close
except Exception as e:
  #print('error while connection to db:', e)
  print('bye')

mydb.close