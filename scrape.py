# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:12:15 2019

@author: Mike
"""
import re
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import Comment
import export
import os
import csv
import percentile


class HTMLTableParser:
    def parse_url(self, url, _id):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        if _id == "" or "creamy":
            table = soup.find_all('table')
            return [(1, self.parse_html_table(t)) \
                    for t in table]
        else:
            table = soup.find_all('table', id=_id)
            print(soup)
            if len(table)>0:
                return [(1, self.parse_html_table(t)) \
                        for t in table]
            else:
                comments = soup.findAll(text=lambda text: isinstance(text, Comment))
                rx = re.compile(r'<table.+?id="'+ _id +'".+?>[\s\S]+?</table>')
                for comment in comments:
                    try:
                        found = rx.search(comment.string).group(0)
                        soup2 = BeautifulSoup(found, 'lxml')
                        table = soup2.find_all('table', id=_id)
                        if len(table)>0:
                            return [(1, self.parse_html_table(t)) \
                                for t in table]
                    except:
                        pass
    def parse_html_table(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can

        c_names = []
        '''
        # This needs to be in there for draft sheets
        index = 0
        for col in table.find_all('th'):
            if index > 9 and index < 31:
                c_names.append(col.get_text())
            index = index + 1
        '''

        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th')
            # TODO Make the below line not necessary for doing the PG, Adv, and Total
            del th_tags[0]
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())


        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        c_names.append("PID")
        for c in column_names:
            # TODO This is necessary to uncomment out when you are doing the player stats data pull
            if c!='\xa0' and len(c)>0:
                c_names.append(c)
        data.append(c_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                pid = re.findall("data-append-csv=\"(\w+)", str(column))
                if len(pid) > 0:
                    r.append(pid[0])
                if column.get_text() != '':
                    r.append(column.get_text())
                # else:
                #     r.append('0.0')
            if(len(r)>0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data


def crawl(url, name, id):
    hp = HTMLTableParser()
    t = []
    table = hp.parse_url(url, id)
    t = table[0][1]
    export.export(t, name, False)


def pull_player_data(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "Resources/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.basketball-reference.com/leagues/NBA_' + s_year + '_per_game.html', foldername + "PG_" + s_year, "")
        crawl("https://www.basketball-reference.com/leagues/NBA_" + s_year + "_advanced.html", foldername + "Advanced_" + s_year, "")
        crawl("https://www.basketball-reference.com/leagues/NBA_" + s_year + "_advanced.html", foldername + "Totals_" + s_year, "")
        year = year + 1


def pull_season_solo_awards(start_year, end_year, id):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "Resources/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.basketball-reference.com/leagues/NBA_' + s_year + '.html', foldername + "Single_Player_Awards_"+s_year, id)
        year = year + 1


def pull_draft(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "Resources/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.basketball-reference.com/draft/NBA_' + s_year + '.html',
              foldername + "Draft_" + s_year, id)
        year = year + 1


def salary_cleanup(start_year, end_year):
    f = open("Resources/nba_salaries_1990_to_2018.csv","r")
    all_file = f.read()
    for i in range(start_year, end_year+1):
        s_year = str(i)
        players = re.findall('(.+),(\d+),(' + s_year + '),(\d+),(\w+),(\w+ \w+)', all_file)
        correct_players = []
        for player in players:
            firstname = ""
            lastname = ""
            player_names = re.findall('(\w+)', player[0])
            for names in range(len(player_names)):
                if names == len(player_names)-1:
                    lastname = player_names[names]
                else:
                    firstname = firstname + player_names[names]
            fixed_player = []
            for col in range(len(player)):
                if col == 0:
                    fixed_player.append(lastname + " " + firstname)
                else:
                    fixed_player.append(player[col])
            correct_players.append(fixed_player)
        sorted_players = export.sort_by_column(correct_players, 0,"str")
        tempout = open("Resources/" + s_year + "/Salary_" + s_year + ".csv", "w+")
        for player in sorted_players:
            for col in range(len(player)):
                tempout.write(player[col])
                if col == len(player)-1:
                    tempout.write("\n")
                else:
                    tempout.write(",")
    f.close()


def add_PID_master(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "Resources/" + s_year + "/"
        master = pd.read_excel("Resources/" + s_year + "/Master_" + s_year + ".xlsx")
        players = []
        player_ids = []
        player_names = get_PIDS()

        for index, row in master.iterrows():
            names = re.findall('(\w+|\w.\w.) (\w+)', str(row["Player"]))
            players.append(names)
        for i in range(len(players)):
            if len(players[i][0])>0 and "." not in players[i][0][1]:
                name = players[i][0][2] + players[i][0][0]
                player_names.append(name)
                player_ids.append(name + "0" + str(player_names.count(name)))
            elif len(players)>0:
                name = players[i][0][2] + players[i][0][0][0] + players[i][0][1][0]
                player_names.append(name)
                player_ids.append(name + "0" + str(player_names.count(name)))
        write_to_PIDS(player_names)
        try:
            master.insert(0, "PID", player_ids, False)
            writer = pd.ExcelWriter("Resources/" + s_year + "/Master_" + s_year + ".xlsx")
            master.to_excel(writer, 'Master')
            writer.save()
        except Exception as e:
            print(e)
        year = year + 1


start = time.time()
start_year = 2018
end_year = 2019
# pull_player_data(start_year, end_year)
# In order to run the below we need to not del[0] but when running the above line we need to in line 64
# pull_season_solo_awards(start_year, end_year, 'all_awards')
# export.multiple_masters(start_year, end_year)
name = "Advanced"
headers = ["Name", "Overall", "PER", "VORP", "TS%", "WS/48", "USG%"]
cols = [29,48,30,44,40]
percentile.multiple_percentiles(name , start_year, end_year, headers, cols)
# pull_draft(1990, 2018)
# salary_cleanup(start_year, end_year)
# add_PID_master(start_year, end_year)
end = time.time()
print(end-start)

