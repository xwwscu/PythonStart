#!/usr/bin/python3
import os, time
import json

class DataProcess:
    '''process mqtt data
    sent file format: {"topic": "T1D_TrackingReport", "payload": json.dumps({"msgId": 1, "timestamp": int(time.time())}), ...}
    recv file format: msgId:timestamp
    merge file format: msgId:sentTimeStamp:recvTimeStamp'''
    __sentFile = ''
    __recvFile = ''

    def __init__(self, sendFile, recvFile) -> None:
       self.__sentFile = sendFile
       self.__recvFile = recvFile

    def processData(self, totalMsgCount):
        'process sent and receive data'
        if (self.__sentFile and self.__recvFile):
            outDir = os.getcwd() + '/data/'
            if (not os.path.exists(outDir)):
                os.mkdir(outDir)
            outFileName = outDir + 'mqtt_result_' + str(int(time.time())) + '.txt'
            try:
                outFile = open(outFileName, 'w+')
                sentFile = open(self.__sentFile, 'r') 
                sendMsgCount = 0
                aSentMsg = sentFile.readline() 
                while(aSentMsg):
                    sendMsgCount += 1
                    sendMsg = json.loads(aSentMsg)
                    sentPayload = json.loads(sendMsg['payload'])
                    with open(self.__recvFile, 'r') as recvFile:
                        aRecvMsg = recvFile.readline()
                        while(aRecvMsg):
                            # recvMsg = json.loads(aRecvMsg)
                            # recvPayload = json.loads(recvMsg['payload'])
                            segStrs = aRecvMsg.split(':')
                            msgId = int(segStrs[0])
                            if sentPayload['msgId'] == msgId:
                                outFile.write(':'.join([segStrs[0], str(sentPayload['timestamp']), segStrs[1]]))
                                # outFile.write(aRecvMsg + ':' + str(sentPayload['timestamp']) + '\n')
                                outFile.flush()
                                break
                            else:
                                aRecvMsg = recvFile.readline()
                    aSentMsg = sentFile.readline()
            # except IOError, argument:
                # print('open output file error')
                # print("open file error\n", argument)
            finally:
                sentFile.close()
                outFile.close()
                print('merge file end and start process output...')
                self.__processData(outFileName, totalMsgCount, sendMsgCount)
        else:
            print('Empty sentFile: ' + self.__sentFile + ' or Empty recvFile: ' + self.__recvFile)

    def __processData(self, outFileName, totalCount, sentCount):
        'inner process merge file and output result'
        # outDir = os.getcwd() + '/data/'
        # outFileName = outDir + 'mqtt_result_' + mergeFile.split('_')[2]
        # print('mqtt result file: ', outFileName)
        recvMsgCount = 0
        totalDelayMilTime = 0
        with open(outFileName, 'r') as outFile:
            aLine = outFile.readline()
            while(aLine):
                recvMsgCount += 1
                segStrs = aLine.split(':')
                sentTime = int(segStrs[1])
                recvTime = int(segStrs[2])
                totalDelayMilTime += (recvTime - sentTime)
                aLine = outFile.readline()
        with open(outFileName, 'a+') as outFile:
            outFile.write('\n\n')
            outFile.write('测试消息数量\t发送成功数量\t接收成功数量\t到达率\t平均时延\n')
            outFile.write('\t\t'.join([str(totalCount), str(sentCount), str(recvMsgCount), str(recvMsgCount / sentCount), str(totalDelayMilTime / recvMsgCount)]) + '\n')
        print('process data end!!!')
    


dirStr = os.getcwd() + '/'
sentFile = dirStr + 'data/sent_1629861630.txt'
recvFile = dirStr + 'data/recv_1629861634839.txt'
fileExist = os.path.exists(sentFile) and os.path.exists(recvFile)
if not fileExist:
    print('sent file: ' + sentFile + ' or recv file: ' + recvFile + ' not Exist!')
    raise Exception('sent or recv file not Exist')
totalMsgCount = 50
dataProcess = DataProcess(sentFile, recvFile)
dataProcess.processData(totalMsgCount)

