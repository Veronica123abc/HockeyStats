import mysql.connector
import mysql
import pandas as pd
import numpy as  np
import os
from difflib import SequenceMatcher
from sportlogiq import extract_game_info_from_schedule_html
import sportlogiq
import scraping
import feature_engineering
import db_tools
import uuid
import logging
def open_database():
    stats_db = mysql.connector.connect(
        host="localhost",
        user="apa",
        auth_plugin='mysql_native_password',
        password="apa",
        database="hockeystats",
    )
    return stats_db


def longest_substring(s1, s2):
    match = SequenceMatcher(None, s1, s2)
    return match.find_longest_match(0, len(s1),0, len(s2)).size


def store_players(filename):
    stats_db = open_database()
    nan = np.nan

    df = pd.read_csv(filename)
    skaters = df.query("playerReferenceId not in [@nan, 'None']").playerReferenceId.unique()
    goalies = df.query("teamGoalieOnIceRef not in [@nan, 'None']").teamGoalieOnIceRef.unique()

    sl_game_id = int(os.path.basename(filename).split('_')[0])
    affiliations=[]
    for skater in skaters:
        skater_data = df.query("playerReferenceId == @skater")
        team_name = skater_data.team.unique()[0]
        first_name = skater_data.playerFirstName.unique()[0]
        last_name = skater_data.playerLastName.unique()[0]
        sl_id = int(skater_data.playerReferenceId.unique()[0])
        team_id = get_team_id_from_substring(team_name)

        cursor = stats_db.cursor()
        sl_id=int(skater)
        cursor.execute("SELECT * FROM player WHERE sl_id = %s", (sl_id,))
        cursor.fetchall()
        # print(cursor.rowcount)
        if cursor.rowcount < 1:
            print('Adding player: ', first_name, ' ', last_name, ' ', team_name, ' ', str(sl_game_id))
            sql = "INSERT INTO player (sl_id, firstName, lastName ) VALUES (%s, %s, %s)"
            val = (int(sl_id), first_name, last_name)
            cursor.execute(sql, val)
            stats_db.commit()
        cursor.execute(f'select id from player where sl_id={sl_id}')
        player_id = cursor.fetchall()[0][0]
        cursor.execute(f'select id from game where sl_game_id = {sl_game_id}')
        game_id = cursor.fetchall()[0][0]
        affiliations.append({'game_id': game_id, 'player_id':player_id, 'team_id': team_id})
    print('Adding affiliations: ', affiliations)
    for affiliation in affiliations:
        sql = f"INSERT INTO affiliation (player_id, game_id, team_id) VALUES ({affiliation['player_id']}, {affiliation['game_id']}, {affiliation['team_id']})"
        try:
            cursor.execute(sql)
            stats_db.commit()
        except:
            print('Could not add affiliation. Already stored ...?')




        #cursor.execute("SELECT SL_key from player"):

def add_jersey_number_to_affiliation(gamefile):
    stats_db = open_database()
    cursor = stats_db.cursor()
    nan = np.nan
    sl_game_id = int(os.path.basename(gamefile).split('_')[0])
    game_id = get_game_id(sl_game_id=sl_game_id)
    df = pd.read_csv(gamefile)
    skaters = df.query("playerReferenceId not in [@nan, 'None']").playerReferenceId.unique()
    goalies = df.query("teamGoalieOnIceRef not in [@nan, 'None']").teamGoalieOnIceRef.unique()
    records=[]
    for skater in skaters:
        player_facts = df.loc[df['playerReferenceId'] == int(skater)].iloc[0][['playerJersey', 'playerPosition']]
        records.append((get_player_id(int(skater)), game_id,
                       int(player_facts['playerJersey']), player_facts['playerPosition']))

    for record in records:
        print(record)
        sql=f"update affiliation set jersey_number = {record[2]}, position=\'{record[3]}\' " + \
            f"where player_id={record[0]} and game_id={record[1]};"
        try:
            cursor.execute(sql)
            stats_db.commit()
        except:
            print('Could not update record ', record)

def store_teams(teams):
    stats_db = open_database()
    cursor = stats_db.cursor()
    for team in teams:
        sql = "INSERT INTO team (sl_id, name) VALUES (%s, %s)"
        val = (team[0], team[1])
        cursor.execute(sql, val)
        stats_db.commit()

def _assign_teams(team_ids, league_id, season):
    if not isinstance(team_ids, list):
        teams_ids = [team_ids]
    stats_db = open_database()
    cursor = stats_db.cursor()

    for team in teams_ids:
        sql = "INSERT INTO participation (league_id, team_id, season) values (%s, %s, %s)"
        values = (league_id, team, season)
        try:
            cursor.execute(sql, values)
            stats_db.commit()
        except:
            print("Assignment could not be added. Already stored?")


def get_team_of_player(player_sl_id, first_name, last_name, game_file):
    df = pd.read_csv(game_file)
    p_o_i = feature_engineering.player_on_ice(df, str(player_sl_id))
    p_o_i = df.query("")
    df = df.query("player ")
    skaters = df.query("playerReferenceId not in [@nan, 'None']").playerReferenceId.unique()
    goalies = df.query("teamGoalieOnIceRef not in [@nan, 'None']").teamGoalieOnIceRef.unique()

def get_team_id_from_substring(team_name):
    stats_db = open_database()
    cursor = stats_db.cursor()
    cursor.execute("select id, name from team")
    all_teams = cursor.fetchall()
    lls = 0
    team_id = -1
    for t in all_teams:
        team=t[1]
        ss = longest_substring(team, team_name)
        if ss > lls:
             team_id = t[0]
             lls = ss
    return team_id

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

def get_league_id(league_name):
    stats_db = open_database()
    cursor = stats_db.cursor()
    sql = "select id from league where name=%s"
    values = (league_name,)
    cursor.execute(sql, values)
    id = cursor.fetchall()
    if len(id) > 0:
        return id[0][0]
    else:
        return -1

def assign_team(team_name, league_name, season):
    team_id = get_team_id(team_name)
    league_id = get_league_id(league_name)
    _assign_teams(team_id, league_id, season)

def store_game(game, league_id):
    stats_db = open_database()
    cursor = stats_db.cursor()

    home_team_id = get_team_id_from_substring(game[0]) #get_team_id(game[0])
    away_team_id = get_team_id_from_substring(game[1])  #get_team_id(game[1])
    sql = "INSERT INTO game (home_team_id, away_team_id, date, sl_game_id, league_id) values (%s, %s, %s, %s, %s)"
    values = (home_team_id, away_team_id, game[2], int(game[3]), int(league_id))
    try:
        cursor.execute(sql, values)
        stats_db.commit()
    except:
        print("Could not store the game. Already stored?")


def store_games(root_dir, league_id):
    files = [os.path.join(root_dir, file) for file in os.listdir(root_dir)]
    for file in files:
        print('Extracting games from ', file)
        games = extract_game_info_from_schedule_html(file)
        print(file,' ', len(games))
        for game in games:
            print('Storing: ', game)
            store_game(game, league_id)

def extract_teams_from_league(filename):
    f = open(filename)
    html = f.read()
    team_segments = html.split('data-cy-teamid-value')
    teams=[]
    for team_segment in team_segments[1:]:
        team_id = int(team_segment.split('\"')[1])
        team_name =  team_segment.split('title=\"')[1].split('\"')[0]
        teams.append(tuple((team_id, team_name)))
    return teams



def download_all_schedules():
    teams = extract_teams_from_league('/home/veronica/hockeystats/NHL/2022-23/Teams_NHL')
    for team in teams:
        team_id = team[0]
        url = f'https://hockey.sportlogiq.com/teams/{team_id}/schedule'
        scraping.download_schedule(url,
                                      '/home/veronica/hockeystats/NHL/tmp',
                                      regular_season=True)

def get_player_id(sl_id):
    stats_db = open_database()
    cursor = stats_db.cursor()
    if isinstance(sl_id, str):
        sl_id = feature_engineering.convert_to_int(sl_id)
    query = f"select id from player where sl_id = {sl_id};"

    cursor.execute(query)
    id = cursor.fetchall()[0][0]
    return id

def get_game_id(sl_game_id = None, sl_game_reference_id = None):
    stats_db = open_database()
    cursor = stats_db.cursor()
    if sl_game_id:
        game_id_query = sl_game_id
        q_column = 'sl_game_id'
        query = f"select id from game where sl_game_id = {sl_game_id};"
    elif sl_game_reference_id:
        game_id_query = sl_game_reference_id
        q_column = 'sl_game_reference_id'
        query = f"select id from game where sl_game_reference_id = {sl_game_reference_id};"
    else:
        return -1
    cursor.execute(query)
    game_id = cursor.fetchall()[0][0]
    return game_id

def get_column_names(table):
    stats_db = open_database()
    cursor = stats_db.cursor()
    cursor.execute("SELECT COLUMN_NAME   FROM INFORMATION_SCHEMA.COLUMNS   WHERE TABLE_SCHEMA = 'hockeystats' AND TABLE_NAME = 'event';")
    column_names=cursor.fetchall()
    map = {}
    for c in column_names:
        map[c[0]]=c[0]
    print(map)
    return ', '.join([c[0] for c in column_names])


def team_name_2_id(val, map):
    #try:
    new_val = map.get(val)
    #except:
    #    new_val = None
    return new_val

def player_slid_2_id(val, map):
    sl_ids = val.split(' ')
    new_item = []
    pass
def clean_dataframe(df):

    stats_db = open_database()
    cursor = stats_db.cursor()

    # Substitute team-name with team_id
    teams = df['teamInPossession'].dropna().unique().tolist()
    teams = [t for t in teams if not t=='None']
    team_map={}
    for team in teams:
        team_map[team] = get_team_id_from_substring(team)
    # team_map['None'] = 'None'
    # team_map['none'] = 'none'
    team_in_possession = df.teamInPossession
    tip = team_in_possession.dropna().apply(lambda t: team_map.get(t))
    df['teamInPossession'] = tip

    apig = feature_engineering.all_players_in_game(df)
    player_map={}
    for player in apig:
        try:
            cursor.execute(f'select id from player where sl_id={player}')
            player_id=cursor.fetchall()[0][0]
            player_map[player] = player_id
        except:
            print(f'Player with sportlogic reference id {player_id} is not stored in the database')

    apoi = feature_engineering.all_players_on_ice(df)
    apoi_int = feature_engineering.all_players_on_ice_as_int(apoi, player_map)
    df['apoi'] = pd.Series(apoi_int)
    df = feature_engineering.add_player_and_goalies(df, player_map)
    return df
def store_events(gamefile):

    #log_root = '/home/veronica/hockeystats/logs'
    #event_log = os.path.join(log_root, 'events')
    #log_file = os.path.basename(gamefile).split('_')[0] + '_' + str(uuid.uuid4()) + '.log'
    #logging.basicConfig(filename=os.path.join(event_log, log_file), level=logging.DEBUG, format='')
    #logger = logging.getLogger('event_logger')
    #logger.setLevel(logging.DEBUG)


    #print("Begin storing events. Logging to " + os.path.join(event_log, log_file))
    logging.debug('Storing events from ' + gamefile + '\n')

    stats_db = open_database()
    cursor = stats_db.cursor()

    map = {'game_id':'gameReferenceId', 'expected_goals_all_shots': 'expectedGoalsAllShots', 'expected_goals_on_net': 'expectedGoalsOnNet',
     'flags': 'flags', 'game_time': 'gameTime', 'sl_id': 'id', 'is_defensive_event': 'isDefensiveEvent',
     'is_last_play_of_possession': 'isLastPlayOfPossession', 'is_possession_breaking': 'isPossessionBreaking',
     'is_possession_event': 'isPossessionEvent', 'manpower_situation': 'manpowerSituation', 'name': 'name',
     'outcome': 'outcome', 'period': 'period', 'period_time': 'periodTime', 'play_in_possession': 'currentPlayInPossession',
     'play_zone': 'playZone', 'possession_id': 'currentPossession', 'previous_name': 'previousName',
     'previous_outcome': 'previousOutcome', 'previous_type': 'previousType', 'player_id':'playerReferenceId',
     'team_goalie_id':'teamGoalieOnIceRef', 'opposing_team_goalie_id': 'opposingTeamGoalieOnIceRef',
     'score_differential': 'scoreDifferential', 'shorthand': 'shorthand',
     'team_in_possession': 'teamInPossession', 'team_skaters_on_ice': 'teamSkatersOnIce', 'timecode': 'timecode',
     'video_frame': 'frame', 'x_adjacent_coordinate': 'xAdjCoord', 'x_coordinate': 'xCoord',
     'y_adjacent_coordinate': 'yAdjCoord', 'y_coordinate': 'yCoord', 'zone': 'zone', 'type': 'type'}

    inv_map = {map[k] : k for k in map.keys()}
    value_names = []
    sl_game_id = int(os.path.basename(gamefile).split('_')[0])
    df = pd.read_csv(gamefile)
    game_id = get_game_id(sl_game_id=str(sl_game_id))
    game_id = df.gameReferenceId.apply(lambda x: game_id)
    df.gameReferenceId = game_id
    df = clean_dataframe(df)
    df = df.rename(columns=inv_map)
    df = df[list(map.keys())]
    entries = df.to_dict(orient='records')
    for e in entries:
        new_record=[(k, e[k]) for k in e.keys() if pd.notna(e[k])]


    # for i, row in df.iterrows():
    #     new_record = [('game_id', game_id)]
    #
    #
    #     for key in list(map.keys()):
    #         if isinstance(row[map[key]], str) and not row[map[key]] in ['None', 'none']:
    #             if key == 'team_in_possession':
    #                 new_record.append((key, team_map[row[map[key]]]))
    #             else:
    #                 new_record.append((key, row[map[key]]))
    #         elif isinstance(row[map[key]], str):
    #             pass
    #         elif not np.isnan(row[map[key]]):
    #             new_record.append((key, row[map[key]]))
    #
    #     new_record.append(('player_on_ice', row['apoi']))
    #     if isinstance(row['player'], str):
    #         try:
    #             new_record.append(('player_id', int(row['player'])))
    #         except:
    #             pass
    #     if isinstance(row['team_goalie_on_ice'], str):
    #         try:
    #             new_record.append(('team_goalie_id', int(row['team_goalie_on_ice'])))
    #         except:
    #             pass
    #     if isinstance(row['opposing_team_goalie_on_ice'], str):
    #         try:
    #             new_record.append(('opposing_team_goalie_id', int(row['opposing_team_goalie_on_ice'])))
    #         except:
    #             pass

        columns = ', '.join([c[0] for c in new_record])
        sql = "INSERT INTO event (" + columns + ") VALUES (" + ', '.join(len(new_record)*['%s']) + ');'
        val = tuple([c[1] for c in new_record])
        # print(sql)
        # print(val)
        # try:
        #     event_id = row['id']
        # except:
        #     pass
        event_id=0
        logging.debug(f"======== Trying to register event {event_id} in game {game_id}========================\n")
        #cursor.execute(sql, val)
        try:
            # print(f"Trying to add event: game_id: {game_id} sl_game_id: {sl_game_id} sl_event_id: {event_id}")
            logging.debug(new_record)
            logging.debug('\n')
            cursor.execute(sql, val)
            # print('Record added successfully')
            logging.debug('mysql registered event successfully \n')
        except:
            print(str(event_id), 'Could not register event. Already registered ...?')
            logging.debug('mysql failed to register event')


    logging.debug('Trying to commit to database')
    try:
        stats_db.commit()
        logging.debug('mysql committed successfully')
    except:
        print('Could not commit')
        logging.debug(f"mysql failed to commit changes for game {game_id}")

    # for i, row in df.iterrows():
    #     apoi = [int(s) for s in row.apoi.split() if s.isdigit()]
    #     event_id
    #     for i in apoi:
    #         sql = f"insert into player_on_ice (event_id, player_id) values({event_id}, {get_player_id(i)});"
    #         cursor.execute(sql)



def store_players_on_ice(event_row):
    all_players_on_ice = feature_engineering.player_on_ice(event_row)
    print('apa')




if __name__ == '__main__':

    import re
    import shutil

    log_root = '/home/veronica/hockeystats/logs'
    event_log = os.path.join(log_root, 'events')
    log_file = 'insert_events_' + str(uuid.uuid4()) + '.log'
    logging.basicConfig(filename=os.path.join(event_log, log_file), level=logging.DEBUG, format='')
    logger = logging.getLogger('event_logger')
    logger.setLevel(logging.DEBUG)

    file = '/home/veronica/hockeystats/NHL/2022-23/gamefiles/92424_playsequence-20230413-NHL-VGKvsSEA-20222023-21312.csv'
    stat_db = open_database()

    # add_jersey_number_to_affiliation(file)
    # store_events(file)
    # BOILERPLATE FOR STORING PLAYERS AND AFFILIATIONS FOR EACH GAMEFILE
    # sql='select sl_game_id from game join affiliation on game.id=affiliation.game_id group by sl_game_id order by sl_game_id;'
    # cursor = stat_db.cursor()
    # cursor.execute(sql)
    # games = cursor.fetchall()
    root_dir = '/home/veronica/hockeystats/NHL/2022-23/gamefiles'
    files_in_dir = os.listdir(root_dir)
    files_in_dir = [file for file in files_in_dir if os.path.splitext(file)[-1] == '.csv']
    gamefiles = [os.path.join(root_dir, gf) for gf in files_in_dir]
    start = False
    ctr = 0;
    for gamefile in gamefiles:
        ctr += 1

        print(gamefile + f" [{ctr} of {len(gamefiles)}]")
        sl_game_id = int(os.path.basename(gamefile).split('_')[0])
        if sl_game_id==92157:
            #start=True
        #if start:
            store_events(gamefile)
        # store_type(gamefile)
        # add_jersey_number_to_affiliation(gamefile)


    #BOILERPLATE FOR FINDING ERRORS IN GAMEFILE-NAMES AND TO FIND MISSING GAMEFILES
    # shl_gamefiles = '/home/veronica/hockeystats/SHL/2022-23/gamefiles'
    # nhl_gamefiles = '/home/veronica/hockeystats/NHL/2022-23/gamefiles'
    # missing_game_ids = db_tools.find_missing_gamefiles(nhl_gamefiles, league_id=2)
    # errors_messages, error_game_ids, error_game_files = db_tools.verify_game_files(nhl_gamefiles, league_id=2)



    # BOILERPLATE FOR DOWNLOADING SCHEDULES
    #scraping.download_schedule_v2('https://hockey.sportlogiq.com/teams/21/schedule',
    #                           '/home/veronica/hockeystats/NHL/tmp',
    #                           regular_season=True)
    #download_all_schedules()
    #scraping.download_schedule_v2('https://hockey.sportlogiq.com/teams/2/schedule',
    #                              '/home/veronica/hockeystats/NHL/tmp',
    #                              regular_season=True)

    # BOILERPLATE FOR EXTRACTING GAMES FROM SCHEDULE TEXTFILE
    # games = extract_game_info_from_schedule_html('/home/veronica/hockeystats/NHL/2022-23/COLUMBUS_regular_season.txt')


    # BOILERPLATE FOR STORING ALL TEAMS FROM A TEXTFILE
    # assign_team('Calgary Flames','NHL', '2022-23')
    #driver = scraping.download_gamefiles([103315, 103332,103331])
    # teams = extract_teams_from_league('/home/veronica/hockeystats/NHL/2022-23/Teams_NHL')
    # print(teams)
    #store_teams(teams)

    # BOILERPLATE FOR STORING GAMES FROM SCHEDULES IN A DIRECTORY
    # games = scraping.get_all_game_numbers('/home/veronica/hockeystats/SHL/2022-23/playoff')
    # store_games('/home/veronica/hockeystats/NHL/tmp', 2)
    # team_names = [team[1] for team in teams]


    # BOILERPLATE FOR ADDING A TEAM TO A LEAGUE
    # for team in team_names:
    #     assign_team(team, 'NHL', '2022-23')


    # BOILERPLATE FOR FETCHING ALL TEAMS FROM A LEAGUE
    # stat_db = open_database()
    # cursor = stat_db.cursor()
    # sql = "select sl_game_id from game where league_id=2"
    # cursor.execute(sql)
    # games = cursor.fetchall()
    # stat_db.close()

    # BOILERPLATE FOR DOWNLOADING GAMEFILES
    # games = [g[0] for g in games if g[0] == 84806]
    # games.sort()
    # scraping.download_gamefile(missing_game_ids, src_dir = nhl_gamefiles)






    # #feature_engineering.extract_player_data(filename='test.csv')
    # #feature_engineering.generate_summary(filename='playsequence.csv', team='Sweden Sweden')
    # #feature_engineering.generate_summary(filename='nhl.csv', team='Dallas Stars')
    # #feature_engineering.test(filename='playsequence.csv', team="Sweden Sweden")
    # assign_team()