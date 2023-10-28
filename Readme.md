1. Download the html-section for the teams in the league
2. Run: teams = extract_teams_from_league('teams-in-league.html')
	This returns a list of dictionaries: [{'sl_id':1234, 'sl_name':'team name'},.,{...}]
	The teamname is the name sportlogic uses when mouse-hoover over the team in the team-selector. This name can be quite random.
	IMPORTANT: sl_id for a team seems to change when the team moves up or down between divisions.
3. Run db_tools.store_teams(teams) to store all teams in the database.
	NOTE: the only unique key in the table is "name". Thus, make sure that sportlogiq has not changed the team-name since that will cause a duplication.

4. Run db_tools.assign_teams(teams, season='2022-23', league='Hockeyallsvenskan') to register the teams for a specific league for a specific season.
	To locate the correct team id from the database, the column "sl_name" is used (since that is the name returned from step 2).
5. Run scraping.download_all_schedules('teams-in-league.html', './tmp', regular_season=True/False).
	This will download the html-segments for each teams:s schedule in the folder 'tmp'.
6. Run db_tools.store_games('path/to/schedules', league_id). This will store all games extracted from the schedules.
	NOTE: Do this for the regular-season schedule as well as for the playoff schedule (when available)
7. Run games = scraping.get_all_game_numbers('./tmp'). games is a list containing sportlogqs game_id numbers for all games played in the league.
8. Run scraping.download_gamefiles(games, 'path/to/source_dir'). This will download all gamefiles to "source_dir".
9. 