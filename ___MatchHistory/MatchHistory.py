import time

from riotwatcher import LolWatcher, ApiError
from tkinter import *
import pandas as pd
import applicationManagement as Am
import colorScheme as Cs
import csv

color_scheme = Cs.basic_color_scheme
wanted_stats = ['championId', 'championName', 'profileIcon', 'puuid', 'summonerLevel', 'assists', 'deaths', 'kills',
                'individualPosition', 'lane', 'role', 'teamPosition', 'baronKills', 'firstBloodKill', 'firstTowerKill',
                'inhibitorKills', 'inhibitorTakedowns', 'inhibitorsLost', 'nexusKills' 'nexusLost', 'nexusTakedowns',
                'objectivesStolen', 'objectivesStolenAssists', 'turretKills', 'turretTakedowns', 'turretsLost',
                'damageDealtToBuildings', 'damageDealtToObjectives', 'damageDealtToTurrets', 'magicDamageDealt',
                'magicDamageDealtToChampions', 'physicalDamageDealt', 'physicalDamageDealtToChampions',
                'timeCCingOthers', 'totalDamageDealtToChampions', 'trueDamageDealt', 'trueDamageDealtToChampions',
                'damageSelfMitigated', 'magicDamageTaken', 'physicalDamageTaken', 'totalDamageTaken', 'trueDamageTaken',
                'neutralMinionsKilled', 'totalMinionsKilled', 'totalDamageShieldedOnTeammates', 'totalHeal',
                'totalHealsOnTeammates', 'goldEarned', 'goldSpent', 'item0', 'item1', 'item2', 'item3', 'item4',
                'item5', 'item6', 'itemsPurchased', 'champLevel', 'longestTimeSpentLiving', 'largestKillingSpree',
                'totalTimeCCDealt', 'totalTimeSpentDead', 'unrealKills', 'visionScore', 'win', 'spell1Casts',
                'spell2Casts', 'spell3Casts', 'spell4Casts', 'summoner1Casts', 'summoner1Id', 'summoner2Casts',
                'summoner2Id']


def run(gui):
    api_key = gui.api_key
    watcher = LolWatcher(api_key)

    app_frame = gui.running_app_frame
    app_frame_width = int(gui.width - (gui.width / 5))
    app_frame_height = int(gui.height)

    SummonerNameEntry(app_frame, watcher)




class SummonerNameEntry:

    def __init__(self, frame, watcher):
        self.get_sum_name(frame, watcher)
        self.summoner_name = ''

    def get_sum_name(self, frame, watcher):
        sum_name_frame = Frame(frame)
        sum_name_text = Label(sum_name_frame, text='Enter Summoner Name', fg=color_scheme['dark_text'], font=90)
        sum_name_text.grid(row=0, column=0, pady=5, padx=5)
        enter_sum_name = Entry(sum_name_frame, justify=CENTER, fg=color_scheme['dark_text'],
                               bg=color_scheme['light_text'], font=90)
        enter_sum_name.grid(row=1, column=0, pady=5, padx=5)
        submit_sum_name = Button(sum_name_frame, text='Submit', fg=color_scheme['light_text'],
                                 bg=color_scheme['dark_text'],
                                 command=lambda: self.validate_entered_sum(enter_sum_name, sum_name_text, frame, watcher),
                                 font=90)
        submit_sum_name.grid(row=2, column=0, pady=5, padx=5)
        sum_name_frame.place(anchor='c', relx=.5, rely=.4)

    def validate_entered_sum(self, entry_widget, text_widget, frame, watcher):
        sum_name = entry_widget.get()
        print(f'Summoner Name: {sum_name}')

        if sum_name != '':
            try:
                response = watcher.summoner.by_name('na1', sum_name)
                self.summoner_name = sum_name
            except ApiError as err:
                # server issue i think
                if err.response.status_code == 429:
                    print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
                    print('this retry-after is handled by default by the RiotWatcher library')
                    print('future requests wait until the retry-after time passes')
                # when the summoner name does not exist
                elif err.response.status_code == 404:
                    text_widget.configure(text='This Name Does Not Exist')
                else:
                    raise Exception('raised')
            self.retrieve_match_list(frame, watcher)

    def retrieve_match_list(self, frame, watcher):
        print(self.summoner_name)
        summoner = watcher.summoner.by_name('na1', self.summoner_name)
        summoner_puuid = summoner['puuid']
        match_list = watcher.match_v5.matchlist_by_puuid('AMERICAS', summoner_puuid)
        # print(len(match_list))
        # print(match_list)

        last_twenty_matches = []
        for match in match_list:
            last_twenty_matches.append(watcher.match_v5.by_id('AMERICAS', match))
        #     time.sleep(1)

        # print(last_twenty_matches[0]['info']['participants'][0])
        players = []
        for player in last_twenty_matches[0]['info']['participants']:
            summoner_name_temp = ''
            player_stats = []
            for stat in player:
                wanted = False
                if stat == 'summonerName':
                    summoner_name_temp = player[stat]
                else:
                    for stat_name in wanted_stats:
                        if stat == stat_name:
                            print(f'{stat_name} and {stat}')
                            wanted = True
                            break
                        else:
                            wanted = False
                    if wanted is True:
                        print(f'{stat}: {player[stat]}')
                        player_stats.append(player[stat])
            player_stats.insert(0, summoner_name_temp)
            players.append(player_stats)

        for array in players:
            print(array)
        match_list_df = pd.DataFrame(players, columns=player_info)
        # match_list_df.to_csv(last_twenty_matches[0] + '.csv')
