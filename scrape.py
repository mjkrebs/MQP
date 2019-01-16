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
import urllib.request

import createPlayerFile
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
        # This needs to be in there for draft sheets
        index = 0

        for col in table.find_all('th'):
            if index > 9 and index < 31:
                c_names.append(col.get_text())
            index = index + 1
        c_names.insert(2,"PID")

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
            # del th_tags[0]
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())


        # print(len(column_names))
        # print(n_columns)
        # Safeguard on Column Titles
        # if len(column_names) > 0 and len(column_names) != n_columns:
        #     raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        # for c in column_names:
        #     # TODO This is necessary to uncomment out when you are doing the player stats data pull
        #     if c!='\xa0' and len(c)>0:
        #         c_names.append(c)
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
                else:
                    r.append('0.0')
            if(len(r)>0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

    def parse_url_ncaa(self, url, type, _id):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        if _id == "college_names":
            # urllib.request.urlretrieve(url, "test.txt")
            f = open("test.txt", "r")
            x = re.findall("friv\/colleges\.fcgi\?college=(.+)\">(.+)<", f.read())
            r = []
            for element in x:
                id = element[0]
                name = element[1]
                r.append((id,name))
            result = pd.DataFrame(r,columns=["ID","Team"])
            result.to_excel("NCAA/name_url.xlsx")
        if _id == "all":
            roster_pattern = "class=\"(left |left sr_nba)\" data-stat=\"player\" csk=\"((?:\w+ |\w+|\w+.){1,4},(?:\w+ |\w+|\w+.){1,4})\".+pos\" >(\w).+height\" csk=\"(\d+.\d+).+weight\" csk=\"(\d+)"
            urllib.request.urlretrieve(url, "test.txt")
            f = open("test.txt")
            read = f.read()
            x = re.findall(roster_pattern, read)
            year = re.findall("itemprop=\"name\">(\d+-\d+)", read)[0]
            nba = []
            player = []
            pos= []
            height = []
            weight = []
            for element in x:
                if element[0] == "left ":
                    nba.append(0)
                else:
                    nba.append(1)
                # Right here we need to turn this into fname lname from lname,fname
                name = element[1].split(",")
                name = name[1] + " " + name[0]
                player.append(name)
                pos.append(element[2])
                height.append(element[3])
                weight.append(element[4])

            team = re.findall("https://www.sports-reference.com/cbb/schools/(\w+-\w+-\w+-\w+|\w+-\w+-\w+|\w+-\w+|\w+)", url)[0]
            result = pd.DataFrame()
            result["Team"] = pd.Series([team]*len(player))
            result["Year"] = year
            result["Player"] = player
            result["NBA"] = nba
            result["Pos"] = pos
            result["Height"] = height
            result["Weight"] = weight
            result.to_excel("basic.xlsx")


            table = soup.find_all('table', id="per_game")
            # print(soup)
            if len(table) > 0:
                if type == "all":
                    table1 =  [(1, self.parse_html_table_ncaa_by_id(t)) \
                            for t in table]
            else:
                comments = soup.findAll(text=lambda text: isinstance(text, Comment))
                rx = re.compile(r'<table.+?id="' + _id + '".+?>[\s\S]+?</table>')
                for comment in comments:
                    try:
                        found = rx.search(comment.string).group(0)
                        soup2 = BeautifulSoup(found, 'lxml')
                        table = soup2.find_all('table', id=_id)
                        if len(table) > 0:
                            if type == "all":
                                table1 =  [(1, self.parse_html_table_ncaa_by_id(t)) \
                                        for t in table]
                    except:
                        pass
            table0 = soup.find_all('table', id="advanced")
            if len(table0) > 0:
                if type == "all":
                    table2 = [(1, self.parse_html_table_ncaa_by_id(t)) \
                            for t in table0]
            else:
                comments = soup.findAll(text=lambda text: isinstance(text, Comment))
                rx = re.compile(r'<table.+?id="' + "advanced" + '".+?>[\s\S]+?</table>')
                for comment in comments:
                    try:
                        found = rx.search(comment.string).group(0)
                        soup2 = BeautifulSoup(found, 'lxml')
                        table0 = soup2.find_all('table', id="advanced")
                        if len(table) > 0:
                            if type == "all":
                                table2 = [(1, self.parse_html_table_ncaa_by_id(t)) \
                                          for t in table0]
                    except:
                        pass
            return (table1, table2)

        if _id == "":
            table = soup.find_all('table')
            if type == "conference":
                return [(1, self.parse_html_table_ncaa_conference_summary(t)) \
                        for t in table]
            elif type == "schoolstat":
                return [(1, self.parse_html_table_ncaa_school_stats(t)) \
                        for t in table]
            elif type == "all_teams":
                return [(1, self.parse_html_table_ncaa_all_team(t)) \
                        for t in table]
            elif type == "all_rosters":
                return [(1, self.parse_html_table_ncaa_all_roster(t)) \
                        for t in table]
            elif type == "college_names":
                return [(1, self.parse_html_table_ncaa_names(t)) \
                        for t in table]
        else:
            table = soup.find_all('table', id =_id)
            # print(soup)
            if len(table)>0:
                if type=="conference":
                    return [(1, self.parse_html_table_ncaa_conference_summary(t)) \
                            for t in table]
                elif type == "schoolstat":
                    return [(1, self.parse_html_table_ncaa_school_stats(t)) \
                            for t in table]
                elif type == "all_teams":
                    return [(1, self.parse_html_table_ncaa_all_team(t)) \
                            for t in table]
                elif type == "all_rosters":
                    return [(1, self.parse_html_table_ncaa_all_roster(t)) \
                            for t in table]
                elif type == "college_names":
                    return [(1, self.parse_html_table_ncaa_names(t)) \
                            for t in table]
                elif type=="by_id":
                    return [(1, self.parse_html_table_ncaa_by_id(t)) \
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
                            if type == "conference":
                                return [(1, self.parse_html_table_ncaa_conference_summary(t)) \
                                        for t in table]
                            elif type == "schoolstat":
                                return [(1, self.parse_html_table_ncaa_school_stats(t)) \
                                        for t in table]
                            elif type == "all_rosters":
                                return [(1, self.parse_html_table_ncaa_all_roster(t)) \
                                        for t in table]
                            elif type == "college_names":
                                return [(1, self.parse_html_table_ncaa_names(t)) \
                                        for t in table]
                            elif type == "by_id":
                                return [(1, self.parse_html_table_ncaa_by_id(t)) \
                                        for t in table]
                    except:
                        pass

    def parse_html_table_ncaa_school_stats(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
        column_names = ["ID", "School", "G", "W", "L", "W-L%", "SRS", "SOS", "CW", "CL", "HW", "HL", "AW", "AL", "TPoints",
                        "OPoints", "DEL", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "TRB", "AST", "STL", "BLK", "TOV", "PF"]
        # Safeguard on Column Titles
        # if len(column_names) > 0 and len(column_names) != n_columns:
        #     raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                # print(str(column))
                pid = re.findall("href=\"/cbb/schools/(\w+-\w+-\w+|\w+-\w+|\w+)", str(column))
                if len(pid) > 0:
                    r.append(pid[0])
                if column.get_text() != '':
                    r.append(column.get_text())
                else:
                    r.append('0.0')
            if(len(r)>0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

    def parse_html_table_ncaa_conference_summary(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())
        try:
            column_names.remove("Rk")
        except Exception as e:
            print(e)
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                if column.get_text() != '':
                    r.append(column.get_text())
                else:
                    r.append('0.0')
            if (len(r) > 0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

    def parse_html_table_ncaa_all_team(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

        column_names = ["Player", "Year", "Rd", "Overall", "From", "To", "G", "MP", "FG", "FGA", "3P", "3PA", "FT", "FTA",
                        "ORB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS", "FG%", "3P%", "FT%", "MP/G", "PTS/G", "TRB/G", "AST/G"]

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                if column.get_text() != '':
                    r.append(column.get_text())
                else:
                    r.append('0.0')
            if (len(r) > 0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

    def parse_html_table_ncaa_all_roster(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

        column_names = ["Player", "G", "GS", "MP", "FG", "FGA", "FG%", "2P", "2PA", "2P%", "3P", "3PA", "3P%", "FT",
                        "FTA","FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
        # if len(column_names) > 0 and len(column_names) != n_columns:
        #     raise Exception("Column titles do not match the number of columns")
        # columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                if column.get_text() != '':
                    r.append(column.get_text())
                else:
                    r.append('0.0')
            if (len(r) > 0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

    def parse_html_table_ncaa_by_id(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
            th_tags = row.find_all('th')
            # TODO Make the below line not necessary for doing the PG, Adv, and Total
            del th_tags[0]
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")
        # columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                if column.get_text() != '':
                    r.append(column.get_text())
                else:
                    r.append('0.0')
            if (len(r) > 0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data
    def parse_html_table_ncaa_names(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
        column_names = ["ID", "Team"]
        # Safeguard on Column Titles
        # if len(column_names) > 0 and len(column_names) != n_columns:
        #     raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        row_marker = 0
        data = []
        data.append(column_names)
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            r = []
            for column in columns:
                name = column.get_text()
                # print(str(column))
                pid = re.findall("friv\/colleges\.fcgi\?college=(\w+-\w+-\w+|\w+-\w+|\w+)\"> (\w+ \w+ \w+|\w+ \w+|\w+)", str(column))
                if len(pid) > 0:
                    r.append(pid)
            if (len(r) > 0):
                data.append(r)
            if len(columns) > 0:
                row_marker += 1
        return data

def crawl(url, name, type, id):
    hp = HTMLTableParser()
    t = []
    if type == "nba":
        table = hp.parse_url(url, id)
        t = table[0][1]
        export.export(t, name, False)
    else:
        table = hp.parse_url_ncaa(url, type, id)
        if id == "all":
            pg = table[0][0][1]
            adv = table[1][0][1]
            export.export(pg, "per_game", False)
            export.export(adv, "advanced", False)

            return 1
        if table==None or len(table)>0:
            try:
                t = table[0][1]
                export.export(t, name, False)
                return 1
            except:
                # print("Empty table")
                return -1
        else:
            return -1


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


def pull_year_school_stats(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "NCAA/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.sports-reference.com/cbb/seasons/' + s_year + '-school-stats.html',
              foldername + "School_Stats" + s_year, "schoolstat", "")
        year = year + 1
        x = pd.read_excel(foldername + "School_Stats" + s_year + ".xlsx")
        x = x.drop(["DEL"], axis = 1)
        x.to_excel(foldername + "School_Stats" + s_year + ".xlsx")


def pull_year_conference_summary(start_year, end_year):
    year = start_year
    while year <= end_year:
        s_year = str(year)
        foldername = "NCAA/" + s_year + "/"
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        crawl('https://www.sports-reference.com/cbb/seasons/' + s_year + '.html',
              foldername + "Conference_Summary" + s_year, "conference", "")
        year = year + 1
        x = pd.read_excel(foldername + "Conference_Summary" + s_year + ".xlsx")
        x.to_excel(foldername + "Conference_Summary" + s_year + ".xlsx")


def pull_college_names():
    crawl('https://www.basketball-reference.com/friv/colleges.fcgi?',
          "NCAA/test", "college_names", "college_names")


def pull_all_teams_nba_players():
    all_teams = pd.read_excel("NCAA/master_teams_urls.xlsx")
    all_teams = all_teams[all_teams.URLS != "None"]
    ids = all_teams["URLS"]
    print(len(ids))
    urls = []
    for id in ids:
        foldername = "NCAA/Teams/" + id
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        c = crawl("https://www.basketball-reference.com/friv/colleges.fcgi?college=" + id, foldername + "/NBA_Players_" + id, "all_teams", "")


def pull_rosters_from_top_100(start, end):
    for year in range(start, end+1):
        s_year = str(year)
        curr_year_id = pd.read_excel("NCAA/" + s_year + "/School_Stats" + s_year + ".xlsx").sort_values(by=["SRS"], ascending=False).head(100).get("ID")
        for id in curr_year_id:
            foldername = "NCAA/" +s_year + "/Rosters/" + id +"_roster"
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            crawl("https://www.sports-reference.com/cbb/schools/" + id + "/" + s_year + ".html", foldername + "/roster",
                  "all_rosters", "per_game")
        # Now we just need to combine all of them
        master_year = pd.DataFrame
        for id in curr_year_id:
            curr = pd.read_excel("NCAA/" +s_year + "/Rosters/" + id +"_roster" + "/roster.xlsx")
            curr.insert(0, "Team", id)
            if master_year.empty:
                master_year = curr
            else:
                master_year = master_year.merge(curr, how="outer")
        master_year = master_year.sort_values("Team")
        master_year.insert(2, "NBA", 0)
        # master_year.reset_index()
        # master_year.__delitem__("index")
        master_year.to_excel("NCAA/" + s_year + "/" + s_year + "_master_roster.xlsx")


def pull_combine_stats():
        anthro = open("combine_anthro.txt", "r")
        x = re.findall(">(.+)<.+\n {10}<td class=\"text\">(\w+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<", anthro.read())
        r = []
        for element in x:
            p = element[0]
            pos = element[1]
            bf = element[2]
            hl = element[3]
            hw = element[4]
            hwos = element[5]
            hws = element[6]
            sr = element[7]
            weight = element[8]
            wspan = element[9]
            r.append((p, pos, bf, hl, hw, hwos, hws, sr, weight, wspan))
        ant = pd.DataFrame(r, columns=["Player", "Pos", "BodyFat%", "HandLength", "HandWidth", "HeightNoShoes",
                                              "HeightShoes", "StandingReach", "Weight", "Wingspan"])
        ant.to_excel("NCAA/Combine/combine_anthro.xlsx")
        agility = open("combine_agility.txt", "r")
        y = re.findall(">(.+)<.+\n {10}<td class=\"text\">(\w+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<.+\n {10}<td>(.+)<", agility.read())
        s = []
        for element in y:
            p = element[0]
            pos = element[1]
            lat = element[2]
            sr = element[3]
            tqs = element[4]
            svl = element[5]
            mvl = element[6]
            mbp = element[7]
            s.append((p,pos,lat,sr,tqs,svl,mvl,mbp))
        agi = pd.DataFrame(s, columns=["Player", "Pos", "LaneAgilityTime", "ShuttleRun", "ThreeQuarterSprint", "StandingVerticalLeap",
                                          "MaxVerticalLeap", "MaxBenchPress"])
        agi.to_excel("NCAA/Combine/combine_agility.xlsx")


def pull_master_ncaa_data(start, end):
    # First go through the years
    # Then iterate through the master url sheet to get the teams urls
    # Copy the text into a text file and the have a big regex which pulls the data we need
    df = pd.read_excel("NCAA/master_teams_urls.xlsx")["ID"]

    for year in range(start, end+1):
        master = pd.DataFrame
        s_year = str(year)
        for id in df:
            try:
                crawl("https://www.sports-reference.com/cbb/schools/" + id + "/" + s_year + ".html", "basic",
                      "all", "all")
                # crawl("https://www.sports-reference.com/cbb/schools/" + id + "/" + s_year + ".html", "per_game",
                #       "by_id", "per_game")
                # crawl("https://www.sports-reference.com/cbb/schools/" + id + "/" + s_year + ".html", "advanced",
                #       "by_id", "advanced")
                basic = pd.read_excel("basic.xlsx")
                pg = pd.read_excel("per_game.xlsx")
                adv = pd.read_excel("advanced.xlsx")
                basic = basic.merge(pg, on="Player")
                basic = basic.merge(adv, on = "Player")
                if master.empty:
                    master = basic
                else:
                    master = master.append(basic)
            except:
                print(id + "is not present in the year " + s_year)

        master.to_excel("all_NCAA_players_zz" + s_year + ".xlsx")
    return

def append_ncaa(start, end):
    first = pd.read_excel("all_NCAA_players_zz" + str(start) + ".xlsx")
    for year in range(start + 1,end+1):
        s_year = str(year)
        curr = pd.read_excel("all_NCAA_players_zz" + s_year + ".xlsx")
        first = first.append(curr)
    first.to_excel("all_NCAA_test.xlsx")


start = time.time()
start_year = 2003
end_year = 2018
# pull_player_data(start_year, end_year)
# In order to run the below we need to not del[0] but when running the above line we need to in line 64
# pull_season_solo_awards(start_year, end_year, 'all_awards')
# export.multiple_masters(start_year, end_year)
# headers = ["PS/G", "TRB", "AST", "STL", "BLK"]
# percentile.multiple_percentiles(start_year, end_year, headers)
# pull_draft(start_year, end_year)
# salary_cleanup(start_year, end_year)
# add_PID_master(start_year, end_year)
# make_master_draft()
# add_draft_to_master()
#
# pull_year_school_stats(start_year, end_year)
# pull_year_conference_summary(start_year, end_year)
# pull_all_teams_nba_players()

#Florida 2000
#Hawaii 2002
# pull_rosters_from_top_100(start_year, end_year)


# All we need to do now is figure out how to fill the NBA field with every college master sheet

# for some reason agility 16-17 isnt loading, try again and place it in between tables where added break lines are
# pull_combine_stats()

# pull_master_ncaa_data(start_year, end_year)
# fix_column_names(2000,2000)
append_ncaa(2015,2018)
end = time.time()
print(end-start)

