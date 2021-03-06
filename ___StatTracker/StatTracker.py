"""

StatTracker

This program is meant to collect the user's statistics while playing (and from past matches) and then display them in an
easy, readable format for the user

@author Joseph Miler
@version September 12, 2021

"""

from riotwatcher import LolWatcher, ApiError
from tkinter import *
import pandas as pd
import applicationManagement as Am
import colorScheme as Cs
import csv


def run(gui):
    api_key = gui.api_key
    watcher = LolWatcher(api_key)

    me = watcher.summoner.by_name('na1', 'jjjooommmill')
    my_ranked_stats = watcher.league.by_summoner('na1', me['id'])
    print(my_ranked_stats)
