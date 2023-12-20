import redis
from SQLite_module import getScript_sql

def setRedis(n):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True )
    for i in range(1, n+1):
        r.setnx(str(i), getScript_sql(i))

def delRedis(n):
    r = redis.Redis(host='localhost', port=6379,decode_responses=True)
    for i in range(1,n+1):
        r.delete(str(i))

def getRedis(n):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.get(str(n))

