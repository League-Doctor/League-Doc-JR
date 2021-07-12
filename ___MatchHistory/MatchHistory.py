from riotwatcher import LolWatcher, ApiError
from tkinter import *
import pandas as pd
import applicationManagement as Am
import colorScheme as Cs
import csv

color_scheme = Cs.basic_color_scheme


def run(gui):
    api_key = gui.api_key
    watcher = LolWatcher(api_key)

    app_frame = gui.running_app_frame
    app_frame_width = int(gui.width - (gui.width / 5))
    app_frame_height = int(gui.height)

    summoner_name = SummonerNameEntry(app_frame, watcher).summoner_name
    print('done')
    print(summoner_name)

    """match_list = watcher.match.matchlist_by_puuid('AMERICAS', '')
    print(match_list)"""


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
                                 command=lambda: self.validate_entered_sum(enter_sum_name, sum_name_text, watcher), font=90)
        submit_sum_name.grid(row=2, column=0, pady=5, padx=5)
        sum_name_frame.place(anchor='c', relx=.5, rely=.4)

    def validate_entered_sum(self, entry_widget, text_widget, watcher):
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
