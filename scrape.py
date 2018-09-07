# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:12:15 2019

@author: Mike
"""
import re
import requests
import time
from bs4 import BeautifulSoup
from bs4 import Comment
import export
import os
import percentile


class HTMLTableParser:
    def parse_url(self, url, _id):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        if _id == "":
            table = soup.find_all('table', id=_id)
            return [(1, self.parse_html_table(t)) \
                    for t in table]
        else:
            table = soup.find_all('table', id=_id)
            if len(table)>0:
                print(table)
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
            #del th_tags[0]
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        c_names = []
        for c in column_names:
            #TODO This is necessary to uncomment out when you are doing the player stats data pull
            # if c!='\xa0' and len(c)>0:
            c_names.append(c)
        data.append(c_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                r.append(column.get_text())
            if(len(r)>0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1

        return data


def crawl(url, name, id):
    hp = HTMLTableParser()
    table = hp.parse_url(url,id)
    t = table[0][1]
    export.export(t, name)


def pull_player_data(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "Resources/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.basketball-reference.com/leagues/NBA_' + s_year + '_per_game.html', foldername + "PG_" + s_year, "")
        crawl("https://www.basketball-reference.com/leagues/NBA_" + s_year + "_advanced.html", foldername + "Advanced_" + s_year,"")
        crawl("https://www.basketball-reference.com/leagues/NBA_" + s_year + "_advanced.html", foldername + "Totals_" + s_year,"")
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


start = time.time()

start_year = 2018
end_year = 2019
# pull_player_data(start_year, end_year)
# pull_season_solo_awards(start_year, end_year, 'all_awards')
export.multiple_masters(start_year, end_year)
headers = ["Name", "Overall", "Points", "Assists", "Rebounds", "Steals", "Blocks"]
cols = [28, 23, 22, 24, 25]
percentile.multiple_percentiles(start_year, end_year, headers, cols)

end = time.time()
print(end-start)

