import httplib
import urllib
import json
import hashlib
import hmac
import time
 
api_key = "YOUR_API_KEY" # TODO replace with your api key from profile page
api_secret = "YOUR_API_SECRET" # TODO replace with your api secret from profile page

nonce = int(round(time.time()*1000))
 
params = {"nonce": nonce}
params = urllib.urlencode(params)
 
H = hmac.new(api_secret, digestmod=hashlib.sha512)
H.update(params)
sign = H.hexdigest()
 
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Key":api_key,
           "Sign":sign}
conn = httplib.HTTPSConnection("api.incorex.com")
conn.request("POST", "/v1/user_info", params, headers)
response = conn.getresponse()
 
print response.status, response.reason
print json.load(response)
 
conn.close()