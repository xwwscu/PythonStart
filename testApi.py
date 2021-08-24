#!/usr/bin/python3.8
import requests
import time
import hashlib

class TuanYouApi:
    "apis about tuanyou"
    __baseUrl = "https://test-mcs.czb365.com/"
    apiToken = ""
    tokenStamp = 0
    appKey = "lionTuanYou"
    appSecret="secret"
    platformType = 1
    platformCode = ""

    def __init__(self, platformType, platformCode):
        TuanYouApi.platformType = platformType
        TuanYouApi.platformCode = platformCode

    def __getToken(self):
        if len(TuanYouApi.apiToken) == 0 or not self.__isTokenValid():
            #init getToken
            url = self.__baseUrl + "services/v3/begin/platformLoginSimpleAppV4"
            body = {
                'platformType':TuanYouApi.platformType,
                'platformCode':TuanYouApi.platformCode
            }
            print("request token url:", url)
            reponse = requests.post(url, data=body)
            print(reponse.text)
        else:
            return TuanYouApi.apiToken
    
    def __isTokenValid(self):
        if len(TuanYouApi.apiToken) == 0:
            return False
        elif time.time() - TuanYouApi.tokenStamp <= 20 * 24 * 60 * 60 * 1000:
            return True
        else:
            return False

    def getGasInfoList(self):
        "query init gas info list"
        token = self.__getToken()
        print('getGasInfoList token:', token)

    def __signParams(self, paramDicts):
        "sign api params"
        if paramDicts:
            paramDicts['app_key'] = TuanYouApi.appKey
            paramDicts['timestamp'] = int(time.time())
        else:
            paramDicts = {'app_key':'', 'timestamp':int(time.time())}
        keyList = sorted(paramDicts.keys(), reverse=False)
        joinStr = TuanYouApi.appSecret
        for x in keyList:
            joinStr = joinStr + x + str(paramDicts[x])
        joinStr = joinStr + TuanYouApi.appSecret
        encodedStr = hashlib.md5(joinStr.encode('utf-8')).hexdigest()
        print('signParam string:', joinStr, 'encoded:', encodedStr)
        return encodedStr

    def testRequests(self):
        "test request module"
        params = {
            'a':'123',
            'k':'789'
        }
        signStr = self.__signParams(params)
        print('test signParams:', signStr)
        resp = requests.get("https://www.baidu.com")
        print(resp.text)

api = TuanYouApi(1, "lion-tech")
api.testRequests()
# api.getGasInfoList()

