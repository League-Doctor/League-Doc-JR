"""

dataCollector

This program is meant to automatically collect data during the champion selection stage of a League of Legends game
in order to plug the data into the Machine Learning function (that is not yet created) and then create a prediction
to be displayed in a separate app. This program is meant to run on a separate thread from the GUI.

@author Joseph Miller, Devin
@version September 12, 2021

"""

from lcu_driver import Connector
import csv
import json
from datetime import datetime
import os

connector = Connector()


@connector.ws.register('/lol-pre-end-of-game/v1/currentSequenceEvent', event_types=('UPDATE',))
async def end_game(connection, event):
    await get_end_game(connection)


async def get_end_game(connection):
    end = await connection.request('get', '/lol-pre-end-of-game/v1/currentSequenceEvent')
    end = json.loads(await end.read())
    if end['priority'] == 3:
        end_info = await connection.request('get', '/lol-end-of-game/v1/eog-stats-block')
        end_info = json.loads(await end_info.read())
        await save_end_game(end_info)


async def save_end_game(game):
    if not os.path.exists(os.getcwd() + "\\Dataset"):
        os.mkdir(os.getcwd() + "\\Dataset")
    date = str(datetime.now())
    final_date = ""
    for character in date:
        if character == ":" or character == ".":
            final_date += "x"
        elif character == "":
            pass
        else:
            final_date += character
    with open(os.getcwd() + "\\Dataset\\" + final_date + ".csv", 'a') as dataset:
        csv_writer = csv.writer(dataset)
        for key, value in game.items():
            csv_writer.writerow([key, value])
        dataset.close()


connector.start()
