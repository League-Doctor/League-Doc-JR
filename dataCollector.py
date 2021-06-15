from lcu_driver import Connector
import csv
import json
from datetime import datetime
import os
connector = Connector()
@connector.ws.register('/lol-pre-end-of-game/v1/currentSequenceEvent', event_types=('UPDATE',))
async def endGame(connection,event):
    await getEndGame(connection)
async def getEndGame(connection):
    end = await connection.request('get', '/lol-pre-end-of-game/v1/currentSequenceEvent')
    end = json.loads(await end.read())
    if end['priority'] == 3:
        endInfo = await connection.request('get', '/lol-end-of-game/v1/eog-stats-block')
        endInfo = json.loads(await endInfo.read())
        await saveEndGame(endInfo)
async def saveEndGame(game):
    if os.path.exists(os.getcwd()+"\\Dataset") != True:
            os.mkdir(os.getcwd()+"\\Dataset")
    date = str(datetime.now())
    finalDate = ""
    for character in date:
        if character == ":" or character ==".":
            finalDate+="x"
        elif character == "":
            pass
        else:
            finalDate+=character
    with open(os.getcwd()+"\\Dataset\\"+finalDate+".csv", 'a') as dataset:
        csvwriter  = csv.writer(dataset)
        for key, value in game.items():
            csvwriter.writerow([key, value])
        dataset.close()
connector.start()

    

        
