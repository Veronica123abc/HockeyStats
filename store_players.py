import mysql.connector
import mysql
import pandas as pd
import numpy as  np
import os
from sportlogiq import extract_game_info_from_schedule_html
import sportlogiq
import scraping
def open_database():
    stats_db = mysql.connector.connect(
        host="localhost",
        user="apa",
        auth_plugin='mysql_native_password',
        password="apa",
        database="hockeystats",
    )
    return stats_db


def store_players(filename):
    stats_db = open_database()
    nan = np.nan
    df = pd.read_csv(filename)
    skaters = df.query("playerReferenceId not in [@nan, 'None']").playerReferenceId.unique()
    goalies = df.query("teamGoalieOnIceRef not in [@nan, 'None']").teamGoalieOnIceRef.unique()

    for skater in skaters:
        skater_data = df[df.playerReferenceId == skater]
        cursor = stats_db.cursor()
        sl_id=int(skater)
        cursor.execute("SELECT * FROM player WHERE sl_id = %s", (sl_id,))
        cursor.fetchall()
        # print(cursor.rowcount)
        if cursor.rowcount < 1:
            print('Adding player ', skater_data.playerFirstName.iloc[0], ' ', skater_data.playerLastName.iloc[0])
            sql = "INSERT INTO player (sl_id, firstName, lastName ) VALUES (%s, %s, %s)"
            val = (int(skater_data.playerReferenceId.iloc[0]), skater_data.playerFirstName.iloc[0], skater_data.playerLastName.iloc[0])
            cursor.execute(sql, val)
            stats_db.commit()


        #cursor.execute("SELECT SL_key from player"):


def store_team():
    stats_db = open_database()
    cursor = stats_db.cursor()
    team = ['Leksand','','LIF',324]
    sql = "INSERT INTO team (name, suffix, sl_code, sl_id) VALUES (%s, %s, %s, %s)"
    val = (team[0], team[1], team[2], 310)
    cursor.execute(sql, val)
    stats_db.commit()

def assign_team():
    stats_db = open_database()
    cursor = stats_db.cursor()
    sql = "SELECT id from team"
    cursor.execute(sql)
    teams = cursor.fetchall()
    cursor.execute("SELECT id from league where name='SHL'")
    league = cursor.fetchall()[0][0]
    season="2022-23"
    for team in teams:
        t = team[0]
        sql = "INSERT INTO participation (league_id, team_id, season) values (%s, %s, %s)"
        values = (league, t, season)
        cursor.execute(sql, values)
        stats_db.commit()

def get_plain_name(team_name):
    stats_db = open_database()
    cursor = stats_db.cursor()
    cursor.execute("select name from team")
    all_teams = cursor.fetchall()
    for team in [t[0] for t in all_teams]:
        if len(team_name.split(team)) > 1:
            return team
    return None

def get_team_id(team_name):
    stats_db = open_database()
    cursor = stats_db.cursor()
    name = get_plain_name(team_name)
    sql = "select id from team where name=%s"
    values = (name,)
    cursor.execute(sql, values)
    id = cursor.fetchall()
    if len(id) > 0:
        return id[0][0]
    else:
        return -1

def store_game(game):
    stats_db = open_database()
    cursor = stats_db.cursor()

    home_team_id = get_team_id(game[0])
    away_team_id = get_team_id(game[1])
    sql = "INSERT INTO game (home_team_id, away_team_id, date, sl_game_id) values (%s, %s, %s, %s)"
    values = (home_team_id, away_team_id, game[2], int(game[3]))
    try:
        cursor.execute(sql, values)
    except:
        print("SQL error when inserting")
    stats_db.commit()
    print('apa')

if __name__ == '__main__':
    # scraping.download_schedule(1, '/home/veronica/hockeystats/NHL/2022-23', regular_season=True)

    for i in range(1,32):
        scraping.download_schedule('https://hockey.sportlogiq.com/teams/21/schedule', i,
                                   '/home/veronica/hockeystats/NHL/2022-23',
                                   regular_season=True)

        scraping.download_schedule('https://hockey.sportlogiq.com/teams/21/schedule', i,
                                   '/home/veronica/hockeystats/NHL/2022-23',
                                   regular_season=False)





    # root_dir = '/home/veronica/hockeystats/SHL/2022-23/regular-season/schedules/'
    # files = [os.path.join(root_dir, file) for file in os.listdir(root_dir)]
    #
    #
    # for file in files[3:4]:
    #     games = extract_game_info_from_schedule_html(file)
    #     #store_game(games[0])
    #     for game in games:
    #         store_game(game)
    # store_game(games[1])
    # #feature_engineering.extract_player_data(filename='test.csv')
    # #feature_engineering.generate_summary(filename='playsequence.csv', team='Sweden Sweden')
    # #feature_engineering.generate_summary(filename='nhl.csv', team='Dallas Stars')
    # #feature_engineering.test(filename='playsequence.csv', team="Sweden Sweden")
    # #scrape()
    # assign_team()
    # files = os.listdir('/home/veronica/hockeystats/SHL/2022-23/regular-season')
    # files = [os.path.join('/home/veronica/hockeystats/SHL/2022-23/regular-season', file) for file in files]
    # for file in files:
    #     print(file)
    #     store_players(file)