#!/usr/bin/python3.8
import requests
import base64
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed 

class MqttTest:
    "test mqtt some api like pubush/batchPub.."
    __baseUrl = ""
    __appKey = ""
    __appSecret=""
    #__fileHandle

    def __init__(self, appKey, appSecret) -> None:
        self.__appKey = appKey
        self.__appSecret = appSecret

    def __genBasicAuth(self):
        content = ":".join((self.__appKey, self.__appSecret)).encode("utf-8")
        return "Basic " + base64.b64encode(content).decode()

    def publishMsg(self, jsonBody):
        apiUrl = self.__baseUrl + 'api/v3/mqtt/publish'
        auth = self.__genBasicAuth()
        print("url: " + apiUrl + ', basic auth: ' + auth)
        headers = {'Content-Type': 'application/json', 'Authorization': auth}
        response = requests.post(url=apiUrl, data=jsonBody, headers=headers)
        print('respCode: ' + str(response.status_code) + " msg: " + jsonBody)
        if response.status_code == 200:
            return jsonBody
        else:
            return None
        # return jsonBody

    def __genPatchMsg(self, index):
        msgContent = {"topic": "T1D_TrackingReport", "payload": json.dumps({"msgId": index, "timestamp": int(time.time())}), "qos": 2, "client_id":"T18T1D123456789", "retain": False}
        return json.dumps(msgContent)

    def patchPublishMsg(self, total):
        with ThreadPoolExecutor(4) as excutors:
            allTasks = [excutors.submit(self.publishMsg, (self.__genPatchMsg(index))) for index in range(0, total)]
        dirStr = os.getcwd() + '/data/'
        dirExist = os.path.exists(dirStr)
        print('dir: ' + dirStr + ' exist: ' + str(dirExist))
        if not dirExist:
            os.mkdir(dirStr)
        fileName = dirStr + 'sent_' + str(time.time()) + '.txt'
        print('file:', fileName)
        with open(fileName, 'w+') as fo:
            for future in as_completed(allTasks):
                data = future.result()
                if not (data is None):
                    fo.write(data + '\n')
        print("process success!")

    def __saveSentMsgs(self):
        'save all send msg to data analysis later'
        pass

appKeyStr = "20f4eb16851a9"
appSecretStr = "MzAwNjIzODEzOTM4OTE5ODY3OTczNTE1NjY4NzY1NDA5MjI"
msgContent = {"topic": "T1D_TrackingReport", "payload": "good morning", "qos": 2, "client_id":"T18T1D123456789", "retain": False}
print("content:", json.dumps(msgContent))
apiTest = MqttTest(appKeyStr, appSecretStr)
# apiTest.publishMsg(json.dumps(msgContent))
apiTest.patchPublishMsg(10)