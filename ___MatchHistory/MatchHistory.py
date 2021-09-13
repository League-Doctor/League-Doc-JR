"""

MatchHistory

When a username of a league player is inputted into the initial text area box, data for that player's last 20 games is
received and then viewable within the running_app_frame. Currently this only works with players in the NA region.

@author Joseph Miller
@version September 12, 2021

"""

import time
import threading
import os
from riotwatcher import LolWatcher, ApiError
from tkinter import *
import pandas as pd
import colorScheme as Cs

color_scheme = Cs.basic_color_scheme

# a list of all the statistics wanted to be stored within the csv file for each player
# (will most likely decrease this list)
wanted_stats = ['assists', 'baronKills', 'champLevel', 'championId', 'championName', 'damageDealtToBuildings',
                'damageDealtToObjectives', 'damageDealtToTurrets', 'damageSelfMitigated', 'deaths', 'firstBloodKill',
                'firstTowerKill', 'goldEarned', 'goldSpent', 'individualPosition', 'inhibitorKills',
                'inhibitorTakedowns', 'inhibitorsLost', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6',
                'itemsPurchased', 'kills', 'lane', 'largestKillingSpree', 'longestTimeSpentLiving', 'magicDamageDealt',
                'magicDamageDealtToChampions', 'magicDamageTaken', 'neutralMinionsKilled', 'nexusKills', 'nexusLost',
                'nexusTakedowns', 'objectivesStolen', 'objectivesStolenAssists', 'physicalDamageDealt',
                'physicalDamageDealtToChampions', 'physicalDamageTaken', 'profileIcon', 'puuid', 'role',
                'spell1Casts', 'spell2Casts', 'spell3Casts', 'spell4Casts', 'summoner1Casts', 'summoner1Id',
                'summoner2Casts', 'summoner2Id', 'summonerLevel', 'teamPosition', 'timeCCingOthers',
                'totalDamageDealtToChampions', 'totalDamageShieldedOnTeammates', 'totalDamageTaken', 'totalHeal',
                'totalHealsOnTeammates', 'totalMinionsKilled', 'totalTimeCCDealt', 'totalTimeSpentDead',
                'trueDamageDealt', 'trueDamageDealtToChampions', 'trueDamageTaken', 'turretKills', 'turretTakedowns',
                'turretsLost', 'unrealKills', 'visionScore', 'win']
# creates the data columns array to be inserted in the pandas dataframe to create the csv file
data_columns = wanted_stats[:]
# csv will always list the summonerName first, despite it appearing later in the retrieved data
data_columns.insert(0, 'summonerName')


def run(gui):
    api_key = gui.api_key
    watcher = LolWatcher(api_key)

    SummonerNameEntry(gui, watcher)


class SummonerNameEntry:

    def __init__(self, gui, watcher):
        self.gui = gui
        self.watcher = watcher  # from the riotWatcher api. Allows for data collection.
        self.running_app_frame = gui.running_app_frame
        self.get_sum_name()
        self.summoner_name = ''

    # places the summoner name input field and submit button
    def get_sum_name(self):
        self.gui.clear_running_app_frame()
        sum_name_frame = Frame(self.running_app_frame)
        sum_name_text = Label(sum_name_frame, text='Enter Summoner Name', fg=color_scheme['dark_text'], font=90)
        sum_name_text.grid(row=0, column=0, pady=5, padx=5)
        enter_sum_name = Entry(sum_name_frame, justify=CENTER, fg=color_scheme['dark_text'],
                               bg=color_scheme['light_text'], font=90)
        enter_sum_name.grid(row=1, column=0, pady=5, padx=5)
        submit_sum_name = Button(sum_name_frame, text='Submit', fg=color_scheme['light_text'],
                                 bg=color_scheme['dark_text'],
                                 command=lambda: self.validate_entered_sum(enter_sum_name, sum_name_text),
                                 font=90)
        submit_sum_name.grid(row=2, column=0, pady=5, padx=5)
        sum_name_frame.place(anchor='c', relx=.5, rely=.4)

    # ensure that the summoner name entered is indeed a currently used, username
    def validate_entered_sum(self, entry_widget, text_widget):
        sum_name = entry_widget.get()
        print(f'Summoner Name: {sum_name}')

        if sum_name != '':
            try:
                self.watcher.summoner.by_name('na1', sum_name)
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
            self.open_match_history()

    # switches the gui to a listing of the match history of the entered summoner name
    def open_match_history(self):
        self.get_data_csv()
        self.gui.clear_running_app_frame()

        match_hist_frame = Frame(self.running_app_frame, width=self.gui.raf_width - 100,
                                 height=self.gui.raf_height - 100,
                                 bg='blue')  # color_scheme['dark'])
        match_hist_frame.pack_propagate(0)

        match_hist_label = Label(match_hist_frame, text=f'{self.summoner_name}\'s Match History',
                                 fg=color_scheme['dark_text'], bg=color_scheme['dark'], font=90)
        match_hist_label.pack(side=TOP, pady=5)
        back_button = Button(match_hist_frame, text='Enter New Summoner', fg=color_scheme['light_text'],
                             bg=color_scheme['dark_text'],
                             command=lambda: self.get_sum_name(),
                             font=90)
        back_button.pack(side=BOTTOM, pady=5)

        self.gui.config_raf_height(self.gui.raf_height * 2)

        match_hist_frame.place(anchor=CENTER, relx=.5, rely=.5)

    # retrieves the list of match ids of the entered summoner name
    def retrieve_match_list(self):
        self.make_player_dir()
        summoner = self.watcher.summoner.by_name('na1', self.summoner_name)
        summoner_puuid = summoner['puuid']
        return self.watcher.match_v5.matchlist_by_puuid('AMERICAS', summoner_puuid)

    # retrieves the match_data from an entered parameter match_id
    def retrieve_match_data(self, match_id, match_data, index):
        match_data.insert(index, self.watcher.match_v5.by_id('AMERICAS', match_id))

    # prints the received match data into a csv file "<match_id>.csv" within a folder "<summoner_name>" from a pandas df
    def get_data_csv(self):
        match_list = self.retrieve_match_list()

        # allows for faster download of match data by creating multiple threads.
        last_twenty_matches = []
        match_download_threads = []

        time.sleep(1)  # prevents overflow of api requests per second.
        for i in range(20):
            thread = threading.Thread(target=self.retrieve_match_data,
                                      args=(match_list[i], last_twenty_matches, i))
            match_download_threads.append(thread)
            thread.start()
        time.sleep(1)  # prevents overflow of api requests per second.

        for i in range(len(match_download_threads)):
            match_download_threads[i].join()

        for match in last_twenty_matches:
            players = []
            for player in match['info']['participants']:
                player_stats = [player['summonerName']]

                for stat in range(len(wanted_stats)):
                    # sometimes, players will not have a stat listed within the data downloaded. This try/catch
                    # statement prevents the program from terminating, while also filling in a "NONE" value for the
                    # unknown statistic.
                    try:
                        player_stats.append(player[wanted_stats[stat]])
                    except KeyError:
                        player_stats.append('NONE')

                players.append(player_stats)

            # creates the csv file
            match_list_df = pd.DataFrame(players, columns=data_columns)
            player_dir = '.\\playerMatchHistory\\' + self.summoner_name + '\\'
            csv_file_name = match['metadata']['matchId'] + '.csv'
            csv_path = player_dir + csv_file_name
            match_list_df.to_csv(csv_path)

    # makes a directory for the entered summoner_name
    def make_player_dir(self):
        player_dir = '.\\playerMatchHistory\\' + self.summoner_name
        if not os.path.isdir(player_dir):
            os.mkdir(player_dir)
