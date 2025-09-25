import hashlib
from hashlib import sha1
import hmac
import base64
from datetime import datetime
from datetime import timezone
import requests
import json

KeyId = "1300386381676526360"
secretKey = b'9585365aa561413eaf2f4e13286864bd'

VERB="POST"
now = datetime.now(timezone.utc)
Date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

#Body = '{"userId":"1300386381676526360"}'
Body1 = '{"id":"1298491919448716710"}'
#Body = '{"stationId":"1298491919448716710"}'
#Body2='{"id":"1308675217947124126","sn":"160F3221C160035"}'
Body2 = '{"id":"1298491919448716710","sn":"1031042254170109"}'
#Body='{"userName":"xxxxx","userType":0}'

Content_Type = "application/json"

#CanonicalizedResource = "/v1/api/userStationList"
CanonicalizedResource1 = "/v1/api/stationDetail"
#CanonicalizedResource = "/v1/api/inveterList"
CanonicalizedResource2 = "/v1/api/inverterDetail"
#CanonicalizedResource = "/v1/api/addUser"

url = 'https://www.soliscloud.com:13333'

def stationDetail():

   Content_MD5 = base64.b64encode(hashlib.md5(Body1.encode('utf-8')).digest()).decode('utf-8')

   req = url + CanonicalizedResource1

   encryptStr = (VERB + "\n"
       + Content_MD5 + "\n"
       + Content_Type + "\n"
       + Date + "\n"
       + CanonicalizedResource1)

   h = hmac.new(secretKey, msg=encryptStr.encode('utf-8'), digestmod=hashlib.sha1)
   Sign = base64.b64encode(h.digest())
   Authorization = "API " + KeyId + ":" + Sign.decode('utf-8')

   requestStr = (VERB + " " + CanonicalizedResource1 + "\n"
       + "Content-MD5: " + Content_MD5 + "\n"
       + "Content-Type: " + Content_Type + "\n"
       + "Date: " + Date + "\n"
       + "Authorization: "+ Authorization + "\n"
       + "Body      ^z" + Body1)

   header = { "Content-MD5":Content_MD5,
       "Content-Type":Content_Type,
       "Date":Date,
       "Authorization":Authorization
            }

   x = requests.post(req, data=Body1, headers=header)
   try:   
      jsonResponse = x.json()
      totalPower = jsonResponse['data']['dayEnergy']
      currentUse = jsonResponse['data']['oneSelf']
   except:
      totalPower = 0
      currentUse = 0
   return totalPower , currentUse

def inverterDetail():

   Content_MD5 = base64.b64encode(hashlib.md5(Body2.encode('utf-8')).digest()).decode('utf-8')

   req = url + CanonicalizedResource2

   encryptStr = (VERB + "\n"
       + Content_MD5 + "\n"
       + Content_Type + "\n"
       + Date + "\n"
       + CanonicalizedResource2)

   h = hmac.new(secretKey, msg=encryptStr.encode('utf-8'), digestmod=hashlib.sha1)
   Sign = base64.b64encode(h.digest())
   Authorization = "API " + KeyId + ":" + Sign.decode('utf-8')

   requestStr = (VERB + " " + CanonicalizedResource2 + "\n"
       + "Content-MD5: " + Content_MD5 + "\n"
       + "Content-Type: " + Content_Type + "\n"
       + "Date: " + Date + "\n"
       + "Authorization: "+ Authorization + "\n"
       + "Body      ^z" + Body2)

   header = { "Content-MD5":Content_MD5,
       "Content-Type":Content_Type,
       "Date":Date,
       "Authorization":Authorization
            }

   x = requests.post(req, data=Body2, headers=header)
   try:
      jsonResponse = x.json()
      currentPower = jsonResponse['data']['pac']
      gridPower = jsonResponse['data']['psum']
      gridSell = jsonResponse['data']['gridSellTodayEnergy']
      gridBuy = jsonResponse['data']['gridPurchasedTodayEnergy']
      batteryCharge = jsonResponse['data']['batteryCapacitySoc']
   except:
      currentPower = 0
      gridPower = 0
      gridSell = 0
      gridBuy = 0
      batteryCharge = 0

   return currentPower,gridPower,gridSell,gridBuy,batteryCharge
