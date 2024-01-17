import pandas as pd
import numpy as np
from datetime import datetime


def fullname(string):
    if string == 'RCB':
        string = 'Royal Challengers Bangalore'
    elif string == 'Mumbai':
        string = 'Mumbai Indians'
    elif string == 'Royals':
        string = 'Rajasthan Royals'
    elif string == 'Super Kings':
        string = 'Chennai Super Kings'
    elif string == 'KKR':
        string = 'Kolkata Knight Riders'
    elif string == 'Chargers':
        string = 'Deccan Chargers'
    elif string == 'Capitals' or string == 'Daredevils':
        string = 'Dehli Capitals'
    elif string == 'Punjab Kings' or string == 'Kings XI':
        string = 'Punjab Kings'
    elif string == 'Sunrisers':
        string = 'Sunrisers Hyderabad'
    elif string == 'Titans':
        string = 'Gujarat Titans'
    elif string == 'Guj Lions':
        string = 'Gujarat Lions'
    elif string == 'Warriors':
        string = 'Pune Warriors'
    elif string == 'Supergiants' or string == 'Supergiant':
        string = 'Rising Pune Supergiants'
    elif string == 'Super Giants':
        string = 'Lucknow Super Giants'
    return string

def match_scorecard(results, battingcard, bowlingcard,players, match_name, season):
    tempresultsdf = results[(results['season'] == int(season)) & (results['match_name'] == match_name)].merge(
        players[['player_id', 'player_name', 'image_url']], left_on='mom_player', right_on='player_id', how='left')
    tempbatting = battingcard[battingcard['match_id'] == tempresultsdf['match_id'][0]].merge(
        players[['player_id', 'player_name', 'image_url']], left_on='batsman_id', right_on='player_id', how='left')
    tempbowling = bowlingcard[bowlingcard['match_id'] == tempresultsdf['match_id'][0]].merge(
        players[['player_id', 'player_name', 'image_url']], left_on='bowler_id', right_on='player_id', how='left')

        if tempresultsdf['team1_name'][0] == 'Gujarat Titans':
        tempresultsdf['team1_url'] = "https://www.timesofsports.com/wp-content/uploads/2022/02/Gujarat-Titans-Logo.png"
    elif tempresultsdf['team2_name'][0] == 'Gujarat Titans':
        tempresultsdf['team2_url'] = "https://www.timesofsports.com/wp-content/uploads/2022/02/Gujarat-Titans-Logo.png"

    if tempresultsdf['team1_name'][0] == 'Chennai Super Kings':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/I/ipl-chennai-super-kings-logo-E534CFAF4A-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Chennai Super Kings':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/I/ipl-chennai-super-kings-logo-E534CFAF4A-seeklogo.com.png"

    if tempresultsdf['team1_name'][0] == 'Mumbai Indians':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/I/ipl-mumbai-indians-logo-5FD6E24965-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Mumbai Indians':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/I/ipl-mumbai-indians-logo-5FD6E24965-seeklogo.com.png"

    if tempresultsdf['team1_name'][0] == 'Punjab Kings':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/I/ipl-kings-xi-punjab-logo-6747D5C02B-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Punjab Kings':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/I/ipl-kings-xi-punjab-logo-6747D5C02B-seeklogo.com.png"

    if tempresultsdf['team1_name'][0] == 'Rajasthan Royals':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/I/ipl-rajasthan-royals-logo-F69DDCEF15-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Rajasthan Royals':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/I/ipl-rajasthan-royals-logo-F69DDCEF15-seeklogo.com.png"

    if tempresultsdf['team1_name'][0] == 'Royal Challengers Bangalore':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/R/rcb-logo-526F657E15-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Royal Challengers Bangalore':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/R/rcb-logo-526F657E15-seeklogo.com.png"

    if tempresultsdf['team1_name'][0] == 'Kolkata Knight Riders':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/K/kolkata-knight-riders-logo-532F9512B0-seeklogo.com.png?v=638133656700000000"
    elif tempresultsdf['team2_name'][0] == 'Kolkata Knight Riders':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/K/kolkata-knight-riders-logo-532F9512B0-seeklogo.com.png?v=638133656700000000"

    if tempresultsdf['team1_name'][0] == 'Deccan Chargers':
        tempresultsdf['team1_url'] = "https://seeklogo.com/images/I/ipl-deccan-chargers-logo-8BA14B44F2-seeklogo.com.png"
    elif tempresultsdf['team2_name'][0] == 'Deccan Chargers':
        tempresultsdf['team2_url'] = "https://seeklogo.com/images/I/ipl-deccan-chargers-logo-8BA14B44F2-seeklogo.com.png"
    
    return tempresultsdf, tempbatting, tempbowling

def match_scorecard_line(results, deliveries, match_name, season):
    tempresultsdf = results[(results['season'] == int(season)) & (results['match_name'] == match_name)]
    match_id = tempresultsdf.iloc[0]['match_id']
    tempdeliveriesdf = deliveries[deliveries['match_id'] == match_id]
    return tempdeliveriesdf, tempresultsdf


def basic_stats(results, team):
    results['match_winner'] = results['match_winner'].apply(lambda x: fullname(x))
    temp_series = results[results['title'] == 'Final'].groupby('match_winner').count()['season']
    if team not in temp_series:
        titles = 0
    else:
        titles = temp_series[team]
    games = results[(results['team1_name'] == team) | (results['team2_name'] == team)].shape[0]
    wins = results[
        ((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] == team)].shape[
        0]
    losses = results[
        ((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] != team)].shape[
        0]
    if team == "Gujarat Titans":
        teamurl = "https://www.timesofsports.com/wp-content/uploads/2022/02/Gujarat-Titans-Logo.png"
    elif team == 'Chennai Super Kings':
        teamurl = 'https://seeklogo.com/images/I/ipl-chennai-super-kings-logo-E534CFAF4A-seeklogo.com.png'
    elif team == 'Mumbai Indians':
        teamurl = 'https://seeklogo.com/images/I/ipl-mumbai-indians-logo-5FD6E24965-seeklogo.com.png'
    elif team == 'Punjab Kings':
        teamurl = 'https://seeklogo.com/images/I/ipl-kings-xi-punjab-logo-6747D5C02B-seeklogo.com.png'
    elif team == 'Rajasthan Royals':
        teamurl = 'https://seeklogo.com/images/I/ipl-rajasthan-royals-logo-F69DDCEF15-seeklogo.com.png'
    elif team == 'Royal Challengers Bangalore':
        teamurl = 'https://seeklogo.com/images/R/rcb-logo-526F657E15-seeklogo.com.png'
    elif team == 'Deccan Chargers':
        teamurl = 'https://seeklogo.com/images/I/ipl-deccan-chargers-logo-8BA14B44F2-seeklogo.com.png'
    elif team == 'Kolkata Knight Riders':
        teamurl = 'https://seeklogo.com/images/K/kolkata-knight-riders-logo-532F9512B0-seeklogo.com.png?v=638133656700000000'
    else:
        teamurl = results[results['team1_name'] == team].iloc[0, :]['team1_url']
    
    return titles, games, wins, losses, teamurl


def team_performance(results, players, battingcard, bowlingcard, team):
    x = results[((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] == team)]
    y = results[((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] != team)]
    tempx = x.groupby(['match_venue_stadium', 'match_venue_city', 'match_venue_country']).count()['season'].reset_index()
    tempy = y.groupby(['match_venue_stadium', 'match_venue_city', 'match_venue_country']).count()['season'].reset_index()
    stadiumperformance = tempx.merge(tempy, on=['match_venue_stadium', 'match_venue_city', 'match_venue_country'], how='outer').fillna(0).sort_values('season_x',
                                                                                                         ascending=False).rename(
        columns={'match_venue_stadium': 'Stadium', 'season_x': 'Wins', 'season_y': 'Losses'})

    stadiumperformance['Wins'] =stadiumperformance['Wins'].astype(int)
    stadiumperformance['Losses'] = stadiumperformance['Losses'].astype(int)
    stadiumperformance['Games Played'] = stadiumperformance['Wins'] + stadiumperformance['Losses']
    stadiumperformance['Location'] = stadiumperformance['match_venue_city'] + ', ' + stadiumperformance[
        'match_venue_country']
    stadiumperformance = stadiumperformance[['Stadium', 'Location', 'Wins', 'Losses', 'Games Played']]

    tempteamlist = results.groupby('team1_name').count()['season'].reset_index()
    x = results[((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] == team)]
    temp1 = x.groupby('team1_name').count()['match_id'].reset_index()
    temp2 = x.groupby('team2_name').count()['match_id'].reset_index()

    tempwdf = tempteamlist.merge(temp1, how='left', on='team1_name').fillna(0).merge(temp2, how='left',
                                                                                     left_on='team1_name',
                                                                                     right_on='team2_name').fillna(0)
    tempwdf['Total Wins'] = tempwdf['match_id_x'] + tempwdf['match_id_y']
    tempwdf['Total Wins'] = tempwdf['Total Wins'].astype(int)
    tempwdf.drop(columns=['season', 'team2_name', 'match_id_x', 'match_id_y'], inplace=True)
    tempwdf.rename(columns={'team1_name': 'Teams'}, inplace=True)
    tempwdf = tempwdf[tempwdf['Teams'] != team]

    y = results[((results['team1_name'] == team) | (results['team2_name'] == team)) & (results['match_winner'] != team)]
    temp1 = y.groupby('team1_name').count()['match_id'].reset_index()
    temp2 = y.groupby('team2_name').count()['match_id'].reset_index()

    templdf = tempteamlist.merge(temp1, how='left', on='team1_name').fillna(0).merge(temp2, how='left',
                                                                                     left_on='team1_name',
                                                                                     right_on='team2_name').fillna(0)
    templdf['Total Losses'] = templdf['match_id_x'] + templdf['match_id_y']
    templdf['Total Losses'] = templdf['Total Losses'].astype(int)
    templdf.drop(columns=['season', 'team2_name', 'match_id_x', 'match_id_y'], inplace=True)
    templdf.rename(columns={'team1_name': 'Teams'}, inplace=True)
    templdf = templdf[templdf['Teams'] != team]

    wins_losses_opponents = pd.merge(tempwdf, templdf, on='Teams')
    wins_losses_opponents['Games Played'] = wins_losses_opponents['Total Wins'] + wins_losses_opponents['Total Losses']
    opponentperformance = wins_losses_opponents.sort_values('Total Wins', ascending=False).reset_index(drop=True)

    tempruns = battingcard.copy()
    tempruns['team'] = tempruns['team'].apply(lambda x: fullname(x))
    tempruns = tempruns.groupby(['team', 'batsman_id']).agg(
        {'runs': 'sum', 'fours': 'sum', 'sixes': 'sum', 'balls': 'sum', 'isout': 'sum', 'match_id': 'count'}).reset_index()
    tempruns = tempruns.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns=['batsman_id', 'player_id'])
    tempruns = tempruns[['team', 'player_name', 'runs', 'balls', 'fours', 'sixes', 'isout', 'match_id']]
    tempruns['runs'] = tempruns['runs'].astype(int)
    tempruns['balls'] = tempruns['balls'].astype(int)
    tempruns['sixes'] = tempruns['sixes'].astype(int)
    tempruns['fours'] = tempruns['fours'].astype(int)
    tempruns['strike rate'] = round((tempruns['runs'] / tempruns['balls']) * 100, 2).fillna(0)

    def coalesce(number):
        if number == 0:
            number = 1
        else:
            number = number
        return number

    tempruns['average'] = round((tempruns['runs'] / tempruns['isout'].apply(lambda x: coalesce(x))).fillna(0), 2)
    tempruns = tempruns[tempruns['team'] == team].sort_values('runs', ascending=False).head(10).reset_index(drop=True)
    tempruns = tempruns[['player_name', 'runs', 'fours', 'sixes', 'average', 'strike rate', 'match_id']].rename(columns={'match_id': 'innings'})
    tempruns = tempruns[['player_name', 'innings', 'runs', 'fours', 'sixes', 'average', 'strike rate']]
    tempruns['innings'] = tempruns['innings'].astype(int)
    topbatter = tempruns.iloc[0:3]
    topbatter = topbatter.merge(players[['player_name', 'image_url']], on='player_name')

    tempwickets = bowlingcard.copy()
    tempwickets['team'] = tempwickets['team'].apply(lambda x: fullname(x))
    tempwickets = tempwickets.groupby(['team', 'bowler_id']).agg(
        {'wickets': 'sum', 'balls': 'sum', 'conceded': 'sum', 'overs': 'sum', 'match_id': 'count'}).rename(
        columns={'match_id': 'innings'}).reset_index()
    tempwickets = tempwickets.merge(players[['player_id', 'player_name']], left_on='bowler_id', right_on='player_id')
    tempwickets['wickets'] = tempwickets['wickets'].astype(int)
    tempwickets['innings'] = tempwickets['innings'].astype(int)
    tempwickets['economy'] = round(tempwickets['conceded'] / tempwickets['overs'], 2)
    tempwickets['average'] = round(tempwickets['conceded'] / tempwickets['wickets'], 2)
    tempwickets['strike_rate'] = round((tempwickets['balls'] / tempwickets['wickets']), 2)
    tempwickets = tempwickets[tempwickets['team'] == team].sort_values('wickets', ascending=False).head(10)
    tempwickets = tempwickets[['player_name', 'innings', 'wickets', 'economy', 'average', 'strike_rate']]
    topbowler = tempwickets.iloc[0:3]
    topbowler = topbowler.merge(players[['player_name', 'image_url']], on='player_name')

    return opponentperformance, stadiumperformance, tempruns, tempwickets, topbatter, topbowler


def teambattingbowling(battingcard, bowlingcard,results, team):
    # batting
    tempbat = battingcard.copy()
    tempbat['team'] = tempbat['team'].apply(lambda x: fullname(x))
    tempbat = tempbat[tempbat['team'] == team]
    tempbat = tempbat.merge(results[['match_id', 'season']], on='match_id')
    tempbat = tempbat.groupby(['season', 'match_id']).agg({'runs': 'sum', 'fours': 'sum', 'sixes': 'sum'}).reset_index()
    tempbat = tempbat.groupby('season').agg(
        {'runs': 'sum', 'fours': 'sum', 'sixes': 'sum', 'match_id': 'count'}).reset_index()
    tempbat['Avg Runs'] = round(tempbat['runs'] / tempbat['match_id'], 2)
    tempbat['Avg Fours'] = round(tempbat['fours'] / tempbat['match_id'], 2)
    tempbat['Avg Sixes'] = round(tempbat['sixes'] / tempbat['match_id'], 2)
    tempbat = tempbat[['season', 'Avg Runs', 'Avg Fours', 'Avg Sixes']]
    tempbat['Avg Runs'] = tempbat['Avg Runs'].astype(int)
    tempbat['Avg Fours'] = tempbat['Avg Fours'].astype(int)
    tempbat['Avg Sixes'] = tempbat['Avg Sixes'].astype(int)

    templeaguebat = battingcard.copy()
    templeaguebat['team'] = templeaguebat['team'].apply(lambda x: fullname(x))
    templeaguebat = templeaguebat.merge(results[['match_id', 'season']], on='match_id')
    templeaguebat = templeaguebat.groupby(['season', 'match_id']).agg(
        {'runs': 'sum', 'fours': 'sum', 'sixes': 'sum'}).reset_index()
    templeaguebat = templeaguebat.groupby('season').agg(
        {'runs': 'sum', 'fours': 'sum', 'sixes': 'sum', 'match_id': 'count'}).reset_index()
    templeaguebat['League Avg Runs'] = round(templeaguebat['runs'] / (templeaguebat['match_id'] * 2), 0).astype(int)
    templeaguebat['League Avg Fours'] = round(templeaguebat['fours'] / (templeaguebat['match_id'] * 2), 0).astype(int)
    templeaguebat['League Avg Sixes'] = round(templeaguebat['sixes'] / (templeaguebat['match_id'] * 2), 0).astype(int)
    templeaguebat = templeaguebat[['season', 'League Avg Runs', 'League Avg Fours', 'League Avg Sixes']]
    mergebatting = templeaguebat.merge(tempbat, on='season')

    # bowling
    tempbowl = bowlingcard.copy()
    tempbowl['team'] = tempbowl['team'].apply(lambda x: fullname(x))
    tempbowl = tempbowl[tempbowl['team'] == team]
    tempbowl = tempbowl.merge(results[['match_id', 'season']], on='match_id')
    tempbowl = tempbowl.groupby(['season', 'match_id']).agg(
        {'wickets': 'sum', 'conceded': 'sum', 'sixes': 'sum', 'fours': 'sum'}).reset_index()
    tempbowl = tempbowl.groupby('season').agg(
        {'wickets': 'sum', 'conceded': 'sum', 'sixes': 'sum', 'fours': 'sum', 'match_id': 'count'}).reset_index()
    tempbowl['Avg Wickets Taken'] = round(tempbowl['wickets'] / tempbowl['match_id'], 0).astype(int)
    tempbowl['Avg Runs Conceded'] = round(tempbowl['conceded'] / tempbowl['match_id'], 0).astype(int)
    tempbowl['Avg Sixes Conceded'] = round(tempbowl['sixes'] / tempbowl['match_id'], 0).astype(int)
    tempbowl['Avg Fours Conceded'] = round(tempbowl['fours'] / tempbowl['match_id'], 0).astype(int)
    tempbowl = tempbowl[
        ['season', 'Avg Wickets Taken', 'Avg Runs Conceded', 'Avg Sixes Conceded', 'Avg Fours Conceded']]

    tempbowlleague = bowlingcard.copy()
    tempbowlleague['team'] = tempbowlleague['team'].apply(lambda x: fullname(x))
    tempbowlleague = tempbowlleague.merge(results[['match_id', 'season']], on='match_id')
    tempbowlleague = tempbowlleague.groupby(['season', 'match_id']).agg(
        {'wickets': 'sum', 'conceded': 'sum', 'sixes': 'sum', 'fours': 'sum'}).reset_index()
    tempbowlleague = tempbowlleague.groupby('season').agg(
        {'wickets': 'sum', 'conceded': 'sum', 'sixes': 'sum', 'fours': 'sum', 'match_id': 'count'}).reset_index()
    tempbowlleague['League Avg Wickets Taken'] = round(tempbowlleague['wickets'] / (tempbowlleague['match_id'] * 2),
                                                       0).astype(int)
    tempbowlleague['League Avg Runs Conceded'] = round(tempbowlleague['conceded'] / (tempbowlleague['match_id'] * 2),
                                                       0).astype(int)
    tempbowlleague['League Avg Sixes Conceded'] = round(tempbowlleague['sixes'] / (tempbowlleague['match_id'] * 2),
                                                        0).astype(int)
    tempbowlleague['League Avg Fours Conceded'] = round(tempbowlleague['fours'] / (tempbowlleague['match_id'] * 2),
                                                        0).astype(int)
    tempbowlleague = tempbowlleague[
        ['season', 'League Avg Wickets Taken', 'League Avg Runs Conceded', 'League Avg Sixes Conceded',
         'League Avg Fours Conceded']]
    mergebowling = tempbowlleague.merge(tempbowl, on='season')

    return mergebatting, mergebowling

def player_overview(players, results, name, option):
    if option == 'Player Overview':
        tempplayer = players.copy()
        tempplayer = tempplayer[tempplayer['player_name'] == name].reset_index(drop=True)
        tempplayer['dob'] = pd.to_datetime(tempplayer['dob'])
        # tempplayer['age'] = (datetime.now() - tempplayer['dob']).astype('<m8[Y]')
        tempplayer['age'] = ((datetime.now() - tempplayer['dob']).dt.days / 365.25)
        tempplayer['age'] = tempplayer['age'].astype(int)
        playerid = tempplayer['player_id'][0]
        tempdf = results[results['team1_playing11'].apply(lambda x: str(playerid) in x)][['season', 'team1_name', 'team1_playing11']]
        tempdf2 = results[results['team2_playing11'].apply(lambda x: str(playerid) in x)][['season', 'team2_name', 'team2_playing11']].rename(columns={'team2_name': 'team1_name', 'team2_playing11': 'team1_playing11'})
        stint = pd.concat([tempdf,tempdf2]).sort_values('season').groupby('team1_name').agg(from_season = ('season', 'min'), to_season = ('season', 'max')).sort_values('from_season', ascending=True).reset_index().rename(columns={'team1_name':'teams'})
        playername = tempplayer['player_name'][0]
        age = tempplayer['age'][0]
        battingstyle = tempplayer['batting_style'][0]
        bowlingstyle = tempplayer['bowling_style'][0]
        image = tempplayer['image_url'][0]

        return playername, age, battingstyle, bowlingstyle, stint, image

def coalesce(number):
    if number == 0:
        number = 1
    else:
        number = number
    return number


def player_batting(results, battingcard, players, deliveries,bowlingcard, name):
    player_id = players[players['player_name'] == name].reset_index()['player_id'][0]
    tempbat = battingcard.copy()
    tempbat['team'] = tempbat['team'].apply(lambda x: fullname(x))
    tempbat = tempbat.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id')
    tempbat = tempbat.merge(results[['match_id', 'season']], on='match_id')
    tempbat = tempbat[tempbat['player_name'] == name]
    batpermatch = tempbat.groupby(['season', 'match_id', 'team']).agg(
        {'runs': 'sum', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum', 'isout': 'sum'}).reset_index()
    batperszn = batpermatch.groupby(['season', 'team']).agg(
        {'runs': 'sum', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum', 'isout': 'sum',
         'match_id': 'count'}).reset_index()
    batperszn['runs'] = batperszn['runs'].astype(int)
    batperszn['fours'] = batperszn['fours'].astype(int)
    batperszn['sixes'] = batperszn['sixes'].astype(int)
    batperszn['average'] = round(batperszn['runs'] / (batperszn['isout'].apply(lambda x: coalesce(x))), 2)
    batperszn['strike rate'] = round((batperszn['runs'] / batperszn['balls']) * 100, 2)
    batperszn = batperszn.rename(columns={'match_id': 'innings'}).drop(columns=['balls', 'isout'])
    batperszn = batperszn[['season', 'team', 'innings', 'runs', 'fours', 'sixes', 'average', 'strike rate']]
    careerbat = tempbat.groupby('player_name').agg(
        {'runs': 'sum', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum', 'isout': 'sum',
         'match_id': 'count'}).reset_index()
    careerbat['runs'] = careerbat['runs'].astype(int)
    careerbat['fours'] = careerbat['fours'].astype(int)
    careerbat['sixes'] = careerbat['sixes'].astype(int)
    careerbat['average'] = round(careerbat['runs'] / (careerbat['isout'].apply(lambda x: coalesce(x))), 2)
    careerbat['strike rate'] = round((careerbat['runs'] / careerbat['balls']) * 100, 2)
    careerbat = careerbat.rename(columns={'match_id': 'innings'}).drop(columns=['balls', 'isout'])
    careerbat['player_name'] = 'Career'
    careerbat['team'] = 'Total'
    careerbat = careerbat.rename(columns={'player_name': 'season'})
    careerbat = careerbat[['season', 'team', 'innings', 'runs', 'fours', 'sixes', 'average', 'strike rate']]
    finalbatdf = pd.concat([batperszn, careerbat]).reset_index(drop=True)

    tempruns = deliveries.copy()
    tempruns = tempruns.merge(bowlingcard[['match_id', 'bowler_id', 'team']], on=['match_id', 'bowler_id']).rename(
        columns={'team': 'opposition'})
    tempruns['opposition'] = tempruns['opposition'].apply(lambda x: fullname(x))
    tempruns = tempruns.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id')
    tempruns = tempruns[tempruns['player_name'] == name]
    tempruns['dismissals'] = (tempruns['player_id'] == tempruns['out_player_id']).astype(int)
    tempruns = tempruns.groupby(['opposition', 'match_id']).agg(
        {'batsman_runs': 'sum', 'over': 'count', 'dismissals': 'sum'}).reset_index()
    tempruns = tempruns.groupby('opposition').agg(
        {'batsman_runs': 'sum', 'over': 'sum', 'dismissals': 'sum', 'match_id': 'count'}).reset_index()
    tempruns = tempruns.sort_values('batsman_runs', ascending=False)
    tempruns['strike rate'] = round((tempruns['batsman_runs'] / tempruns['over']) * 100, 2)
    tempruns['average'] = round((tempruns['batsman_runs'] / tempruns['dismissals'].apply(lambda x: coalesce(x))), 2)
    tempruns = tempruns.rename(columns={'batsman_runs': 'runs', 'match_id': 'innings'})
    tempruns = tempruns[['opposition', 'innings', 'dismissals', 'runs', 'strike rate', 'average']].reset_index(
        drop=True)
    tempruns['runs'] = tempruns['runs'].astype(int)

    tempvenue = deliveries.copy()
    tempvenue = deliveries.merge(results[['match_id', 'match_venue_stadium', 'match_venue_city']], on='match_id')
    tempvenue = tempvenue.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id')
    tempvenue = tempvenue[tempvenue['player_name'] == name]
    tempvenue['dismissals'] = (tempvenue['player_id'] == tempvenue['out_player_id']).astype(int)
    tempvenue = tempvenue.groupby(['match_venue_stadium', 'match_venue_city', 'match_id']).agg(
        {'batsman_runs': 'sum', 'dismissals': 'sum', 'over': 'count'}).reset_index()
    tempvenue = tempvenue.rename(columns={'match_id': 'innings', 'over': 'balls'})
    tempvenue = tempvenue.groupby(['match_venue_stadium', 'match_venue_city']).agg(
        {'batsman_runs': 'sum', 'dismissals': 'sum', 'innings': 'count', 'balls': 'sum'}).reset_index()
    tempvenue = tempvenue.sort_values('batsman_runs', ascending=False)
    tempvenue['strike rate'] = round((tempvenue['batsman_runs'] / tempvenue['balls']) * 100, 2)
    tempvenue['average'] = round((tempvenue['batsman_runs'] / tempvenue['dismissals'].apply(lambda x: coalesce(x))), 2)
    tempvenue = tempvenue.rename(
        columns={'batsman_runs': 'runs', 'match_venue_stadium': 'stadium', 'match_venue_city': 'city'})
    tempvenue['runs'] = tempvenue['runs'].astype(int)
    tempvenue['stadium'] = tempvenue['stadium'] + ', ' + tempvenue['city']
    tempvenue = tempvenue[['stadium', 'innings', 'dismissals', 'runs', 'strike rate', 'average']].reset_index(drop=True)

    temphs = battingcard[battingcard['batsman_id'] == player_id]
    temphs = temphs[temphs['runs'] == temphs['runs'].max()].reset_index()
    temphs['runs'] = temphs['runs'].astype(int)
    temphs['balls'] = temphs['balls'].astype(int)
    runs = temphs['runs'][0]
    balls = temphs['balls'][0]

    if temphs['isout'][0] == True:
        highscore = f"{runs}({balls})"
    else:
        highscore = f"{runs}*({balls})"

    bataverage = finalbatdf.iloc[-1]['average']
    batstrikerate = finalbatdf.iloc[-1]['strike rate']

    tempscore = battingcard[(battingcard['batsman_id'] == player_id) & (battingcard['runs'] > 30)]
    scores30 = tempscore.shape[0]

    tempscore1 = battingcard[(battingcard['batsman_id'] == player_id) & (battingcard['runs'] >= 50)]
    scores50 = tempscore1.shape[0]

    tempscore2 = battingcard[(battingcard['batsman_id'] == player_id) & (battingcard['runs'] >= 100)]
    scores100 = tempscore2.shape[0]

    tempcap = battingcard.merge(results[['match_id', 'season']], on='match_id')
    tempcamp = tempcap.groupby(['season', 'batsman_id'])['runs'].sum().reset_index().sort_values(['season', 'runs'],
                                                                                                 ascending=[True,
                                                                                                            False])
    tempcamp = tempcamp.drop_duplicates(subset='season', keep='first')
    tempcamp = tempcamp.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns='player_id')
    number = 0
    for i in tempcamp['player_name']:
        if i == name:
            number = number + 1
        else:
            number = number

    careerhighscore = batperszn[batperszn['runs'] == batperszn['runs'].max()].reset_index(drop=True)
    careerhighscore = careerhighscore['runs'][0]

    innings = finalbatdf[finalbatdf['innings'] == finalbatdf['innings'].max()].reset_index(drop=True)['innings'][0]

    image = players[players['player_name'] == name].reset_index(drop=True)['image_url'][0]

    return finalbatdf, tempruns, tempvenue, highscore, bataverage, batstrikerate, scores30, scores50, scores100, number, careerhighscore, innings, image

def outcome(string):
    if string >=4:
        string = 'Boundary (4 or 6)'
    elif string <4 and string >0:
        string = 'Strike Rotation (1,2 or 3 runs)'
    elif string == 0:
        string = 'Dot Ball(0 runs)'
    return string

def bowling_outcome(string):
    if string == 4:
        string = '4 runs'
    elif string == 5:
        string = '5 runs'
    elif string == 0:
        string = 'Dot Ball (0 runs)'
    elif string == 6:
        string = '6 runs'
    elif string == 3:
        string = '3 runs'
    elif string == 2:
        string = '2 runs'
    elif string == 1:
        string = '1 run'
    return string


def over_situation(string):
    if string < 6:
        string = 'Powerplay'
    elif string > 6 and string <15:
        string = 'Middle Overs'
    else:
        string = 'Death Overs'
    return string


def bowling_category(string):
    if string == 'right-arm fast' or string == 'left-arm fast':
        string = 'Fast Bowler'

    elif string in ['left-arm fast-medium', 'left-arm medium', 'left-arm medium-fast', 'right-arm medium-fast',
                    'right-arm medium', 'right-arm fast-medium']:
        string = 'Medium Pacer'
    elif string in ['legbreak googly', 'slow left-arm orthodox', 'legbreak', 'left-arm wrist-spin',
                    'right-arm offbreak']:
        string = 'Spinner'

    return string



def player_batting_viz(deliveries, players, battingcard, name):
    # Subplot 1: Performance against Different Bowling Styles(Multiple Column Bar Chart)

    tempbowltype = deliveries.copy()
    tempbowltype = tempbowltype.merge(players[['player_id', 'player_name', 'bowling_style']], left_on='bowler_id',
                                      right_on='player_id').rename(columns={'player_name': 'bowler_name'}).drop(
        columns='player_id')
    tempbowltype = tempbowltype.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                      right_on='player_id').rename(columns={'player_name': 'batsman_name'}).drop(
        columns='player_id')
    tempbowltype = tempbowltype[tempbowltype['batsman_name'] == name]
    tempbowltype['bowling_style'] = tempbowltype['bowling_style'].apply(lambda x: bowling_category(x))
    tempbowltype['dismissals'] = (tempbowltype['out_player_id'] == tempbowltype['batsman_id']).astype(int)
    tempbowltype = tempbowltype.groupby(['bowling_style', 'match_id']).agg(
        {'batsman_runs': 'sum', 'over': 'count', 'dismissals': 'sum'}).reset_index()
    tempbowltype = tempbowltype.groupby('bowling_style').agg(
        {'batsman_runs': 'sum', 'over': 'sum', 'dismissals': 'sum', 'match_id': 'count'}).reset_index()
    tempbowltype['batsman_runs'] = tempbowltype['batsman_runs'].astype(int)
    tempbowltype['strike rate'] = round((tempbowltype['batsman_runs'] / tempbowltype['over']) * 100, 2)
    tempbowltype['average runs'] = round((tempbowltype['batsman_runs'] / tempbowltype['dismissals']), 2)
    tempbowltype = tempbowltype[['bowling_style', 'average runs', 'strike rate', 'dismissals']]

    # Subplot 2: Strike Rate throughout the innings (Line plot)

    tempstrike = deliveries.copy()
    tempstrike = tempstrike.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                  right_on='player_id').drop(columns='player_id')
    tempstrike = tempstrike[tempstrike['player_name'] == name]
    tempstrike['ball'] = tempstrike.groupby(['match_id', 'player_name']).cumcount() + 1
    bins = [-1, 10, 20, 30, float('inf')]
    labels = ['0-10', '11-20', '21-30', '30+']
    tempstrike['balls_range'] = pd.cut(tempstrike['ball'], bins=bins, labels=labels, right=False)
    tempstrike['dismissals'] = (tempstrike['batsman_id'] == tempstrike['out_player_id']).astype(int)
    tempstrike = tempstrike.groupby('balls_range').agg(
        {'batsman_runs': 'sum', 'ball': 'count', 'dismissals': 'sum'}).reset_index()
    tempstrike['strike rate'] = round((tempstrike['batsman_runs'] / tempstrike['ball']) * 100, 2)
    tempstrike = tempstrike[['balls_range', 'strike rate']]

    # Subplot 3: Innings Breakdown (Pie Chart)

    tempinnings = deliveries.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                   right_on='player_id').drop(columns='player_id')
    tempinnings = tempinnings[tempinnings['player_name'] == name]
    tempinnings['ball_outcome'] = tempinnings['batsman_runs'].apply(lambda x: outcome(x))
    matches = tempinnings['match_id'].nunique()
    tempinnings = tempinnings.groupby('ball_outcome').agg({'batsman_runs': 'count'}).reset_index()
    tempinnings['runs'] = round(tempinnings['batsman_runs'] / matches, 2)

    # subplot 4: Heatmap for player performance in powerplay, middle overs and death overs

    tempheatmap = deliveries.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                   right_on='player_id').drop(columns='player_id')
    tempheatmap = tempheatmap[tempheatmap['player_name'] == name]
    tempheatmap['ball_outcome'] = tempheatmap['batsman_runs'].apply(lambda x: outcome(x))
    tempheatmap['over_situation'] = tempheatmap['over'].apply(lambda x: over_situation(x))
    temppivot = tempheatmap.pivot_table(index='over_situation', columns='ball_outcome', values='batsman_runs',
                                        aggfunc='count')

    # Subplot 5: 2d kde plot (x='batsman_runs', y='strike rate')

    tempkde = deliveries.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns='player_id')
    tempkde = tempkde[tempkde['player_name'] == name]
    tempkde = tempkde.groupby('match_id').agg({'batsman_runs': 'sum', 'over': 'count'}).reset_index()
    tempkde['strike rate'] = round((tempkde['batsman_runs'] / tempkde['over']) * 100, 2)
    tempkde['batsman_runs'] = tempkde['batsman_runs'].astype(int)
    tempkde = tempkde[tempkde['batsman_runs'] >= 10]

    # Subplot 6: Types of Dismissals (Pie chart)

    tempdismissals = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                       right_on='player_id').drop(columns='player_id')
    tempdismissals = tempdismissals[(tempdismissals['player_name'] == name) & (tempdismissals['wickettype'] != 'DNB')]
    tempdismissals = tempdismissals.groupby('wickettype').count()['match_id'].reset_index()

    return tempbowltype, tempstrike, tempinnings, temppivot, tempkde, tempdismissals


def favbowler(deliveries, players, name, sort):
    favbowler = deliveries.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                 right_on='player_id').rename(columns={'player_name': 'batsman_name'}).drop(
        columns='player_id')
    favbowler = favbowler.merge(players[['player_id', 'player_name', 'bowling_style']], left_on='bowler_id',
                                right_on='player_id').rename(columns={'player_name': 'bowler_name'}).drop(
        columns='player_id')
    favbowler = favbowler[favbowler['batsman_name'] == name]
    favbowler['dismissals'] = (favbowler['out_player_id'] == favbowler['batsman_id']).astype(int)
    favbowler = favbowler.groupby(['bowler_name', 'bowling_style']).agg(
        {'batsman_runs': 'sum', 'over': 'count', 'dismissals': 'sum'}).reset_index()
    favbowler['strike rate'] = round((favbowler['batsman_runs'] / favbowler['over']) * 100, 2)
    favbowler['average'] = round(
        favbowler['batsman_runs'] / favbowler['dismissals'].apply(lambda x: 1 if x == 0 else x), 2)
    favbowler = favbowler[favbowler['over'] >= 24]
    favbowler = favbowler[['bowler_name', 'bowling_style', 'batsman_runs', 'strike rate', 'average', 'dismissals']]
    favbowlerfull = favbowler.sort_values(sort, ascending=False).head(15).reset_index(drop=True)
    favbowlerfull['batsman_runs'] = favbowlerfull['batsman_runs'].astype(int)
    favbowlertop3 = favbowlerfull.iloc[0:3].reset_index()
    favbowlertop3 = favbowlertop3.merge(players[['player_name', 'image_url']], left_on='bowler_name',
                                        right_on='player_name').drop(columns='player_name')

    return favbowlerfull, favbowlertop3


def worstbowler(deliveries, players, name, sort):
    worstbowler = deliveries.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                   right_on='player_id').rename(columns={'player_name': 'batsman_name'}).drop(
        columns='player_id')
    worstbowler = worstbowler.merge(players[['player_id', 'player_name', 'bowling_style']], left_on='bowler_id',
                                    right_on='player_id').rename(columns={'player_name': 'bowler_name'}).drop(
        columns='player_id')
    worstbowler = worstbowler[worstbowler['batsman_name'] == name]
    worstbowler['dismissals'] = (worstbowler['out_player_id'] == worstbowler['batsman_id']).astype(int)
    worstbowler = worstbowler.groupby(['bowler_name', 'bowling_style']).agg(
        {'batsman_runs': 'sum', 'over': 'count', 'dismissals': 'sum'}).reset_index()
    worstbowler['strike rate'] = round((worstbowler['batsman_runs'] / worstbowler['over']) * 100, 2)
    worstbowler['average'] = round(
        worstbowler['batsman_runs'] / worstbowler['dismissals'].apply(lambda x: 1 if x == 0 else x), 2)
    worstbowler = worstbowler[worstbowler['over'] >= 24]
    worstbowler = worstbowler[['bowler_name', 'bowling_style', 'batsman_runs', 'strike rate', 'average', 'dismissals']]

    if sort == 'dismissals':
        worstbowlerfull = worstbowler.sort_values('dismissals', ascending=False).head(15).reset_index(drop=True)
        worstbowlerfull['batsman_runs'] = worstbowlerfull['batsman_runs'].astype(int)
        worsbowlertop3 = worstbowlerfull.iloc[0:3].reset_index()
        worsbowlertop3 = worsbowlertop3.merge(players[['player_name', 'image_url']], left_on='bowler_name',
                                              right_on='player_name').drop(columns='player_name')

    else:
        worstbowlerfull = worstbowler.sort_values(sort, ascending=True).head(15).reset_index(drop=True)
        worstbowlerfull['batsman_runs'] = worstbowlerfull['batsman_runs'].astype(int)
        worsbowlertop3 = worstbowlerfull.iloc[0:3].reset_index()
        worsbowlertop3 = worsbowlertop3.merge(players[['player_name', 'image_url']], left_on='bowler_name',
                                              right_on='player_name').drop(columns='player_name')

    return worstbowlerfull, worsbowlertop3


def player_bowling_stats(bowlingcard, players, results, name):
    # Performance Over the Years
    bowlersdf = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                  right_on='player_id').drop(columns='player_id')
    bowlersdf['team'] = bowlersdf['team'].apply(lambda x: fullname(x))
    bowlersdf['opposition'] = bowlersdf['opposition'].apply(lambda x: fullname(x))
    bowlersdf = bowlersdf.merge(results[['match_id', 'season']], on='match_id')

    # Bowling Performance Over the Years
    bowlperszn = bowlersdf[bowlersdf['player_name'] == name]
    bowlperszn = bowlperszn.groupby(['season', 'team']).agg(
        {'conceded': 'sum', 'balls': 'sum', 'wickets': 'sum', 'overs': 'sum', 'match_id': 'count',
         'maidens': 'sum'}).reset_index()
    bowlperszn = bowlperszn.rename(columns={'match_id': 'innings'})
    bowlperszn['wickets'] = bowlperszn['wickets'].astype(int)
    bowlperszn['maidens'] = bowlperszn['maidens'].astype(int)
    bowlperszn['economy'] = round((bowlperszn['conceded'] / bowlperszn['overs']), 2)
    bowlperszn['average'] = round((bowlperszn['conceded'] / bowlperszn['wickets']), 2)
    bowlperszn['strike rate'] = round((bowlperszn['balls'] / bowlperszn['wickets']), 2)
    bowlperszn = bowlperszn[['season', 'team', 'innings', 'wickets', 'maidens', 'economy', 'average', 'strike rate']]

    careerbowl = bowlersdf.groupby('player_name').agg(
        {'conceded': 'sum', 'balls': 'sum', 'wickets': 'sum', 'overs': 'sum', 'match_id': 'count',
         'maidens': 'sum'}).reset_index()
    careerbowl = careerbowl[careerbowl['player_name'] == name]
    careerbowl = careerbowl.rename(columns={'match_id': 'innings'})
    careerbowl['wickets'] = careerbowl['wickets'].astype(int)
    careerbowl['maidens'] = careerbowl['maidens'].astype(int)
    careerbowl['economy'] = round((careerbowl['conceded'] / careerbowl['overs']), 2)
    careerbowl['average'] = round((careerbowl['conceded'] / careerbowl['wickets']), 2)
    careerbowl['strike rate'] = round((careerbowl['balls'] / careerbowl['wickets']), 2)
    careerbowl['player_name'] = 'career'
    careerbowl['team'] = 'total'
    careerbowl = careerbowl[
        ['player_name', 'team', 'innings', 'wickets', 'maidens', 'economy', 'average', 'strike rate']].rename(
        columns={'player_name': 'season'})

    seasonbowl = pd.concat([bowlperszn, careerbowl]).reset_index(drop=True)

    # Performance against Opponents
    performopp = bowlersdf[bowlersdf['player_name'] == name]
    performopp = performopp.groupby('opposition').agg(
        {'conceded': 'sum', 'balls': 'sum', 'wickets': 'sum', 'overs': 'sum', 'match_id': 'count',
         'maidens': 'sum'}).reset_index()
    performopp = performopp.rename(columns={'match_id': 'innings'})
    performopp['wickets'] = performopp['wickets'].astype(int)
    performopp['maidens'] = performopp['maidens'].astype(int)
    performopp['economy'] = round((performopp['conceded'] / performopp['overs']), 2)
    performopp['average'] = round((performopp['conceded'] / performopp['wickets']), 2)
    performopp['strike rate'] = round((performopp['balls'] / performopp['wickets']), 2)
    performopp = performopp[
        ['opposition', 'innings', 'wickets', 'maidens', 'economy', 'average', 'strike rate']].sort_values('wickets',
                                                                                                          ascending=False).reset_index(
        drop=True)

    # Performance in Different Stadiums
    performvenue = bowlersdf[bowlersdf['player_name'] == name]
    performvenue = performvenue.merge(results[['match_id', 'match_venue_stadium', 'match_venue_city']], on='match_id')
    performvenue = performvenue.groupby(['match_venue_stadium', 'match_venue_city']).agg(
        {'conceded': 'sum', 'balls': 'sum', 'wickets': 'sum', 'overs': 'sum', 'match_id': 'count',
         'maidens': 'sum'}).reset_index()
    performvenue = performvenue.rename(columns={'match_id': 'innings'})
    performvenue['wickets'] = performvenue['wickets'].astype(int)
    performvenue['maidens'] = performvenue['maidens'].astype(int)
    performvenue['economy'] = round((performvenue['conceded'] / performvenue['overs']), 2)
    performvenue['average'] = round((performvenue['conceded'] / performvenue['wickets']), 2)
    performvenue['strike rate'] = round((performvenue['balls'] / performvenue['wickets']), 2)
    performvenue['stadium'] = performvenue['match_venue_stadium'] + ', ' + performvenue['match_venue_city']
    performvenue = performvenue[
        ['stadium', 'innings', 'wickets', 'maidens', 'economy', 'average', 'strike rate']].sort_values('wickets',
                                                                                                       ascending=False).reset_index(
        drop=True)

    # Individual Column Statistics: Innings, Wickets, Economy, Average, Strike Rate, Purple Caps, 3fers, 5fers, Best Bowling Figures

    tempstats = seasonbowl[seasonbowl['team'] == 'total'].reset_index(drop=True)
    innings = tempstats['innings'][0]
    wickets = tempstats['wickets'][0]
    economy = tempstats['economy'][0]
    average = tempstats['average'][0]
    strike_rate = tempstats['strike rate'][0]

    wickets3 = bowlersdf[(bowlersdf['player_name'] == name) & (bowlersdf['wickets'] == 3)]
    wickets3 = wickets3.shape[0]
    wickets5 = bowlersdf[(bowlersdf['player_name'] == name) & (bowlersdf['wickets'] == 5)]
    wickets5 = wickets5.shape[0]

    bowlhighscore = bowlersdf[bowlersdf['player_name'] == name]
    bowlhighscore = \
    bowlhighscore.sort_values(['wickets', 'conceded'], ascending=[False, True]).reset_index(drop=True).iloc[0]
    if bowlhighscore.shape[0] == 0:
        bowlhighscore = 'NA'
    else:
        wickets2 = (bowlhighscore['wickets']).astype(int)
        runs2 = (bowlhighscore['conceded']).astype(int)
        bowlhighscore = f"{wickets2}/{runs2}"

    purplecaps = bowlersdf.groupby(['season', 'player_name']).agg(
        {'conceded': 'sum', 'balls': 'sum', 'wickets': 'sum', 'overs': 'sum', 'match_id': 'count',
         'maidens': 'sum'}).reset_index().sort_values(['season', 'wickets', 'conceded'], ascending=[True, False, True])
    purplecaps = purplecaps.drop_duplicates(subset='season')
    purplecap = 0
    for i in purplecaps['player_name']:
        if i == name:
            purplecap = purplecap + 1
        else:
            purplecap = purplecap

    return seasonbowl, performopp, performvenue, innings, wickets, economy, average, strike_rate, wickets3, wickets5, bowlhighscore, purplecap

def player_bowling_viz1(deliveries, players, name, battingcard):
    # Subplot 1: Performance Against Different Batsmen (Multiple Bar Chart: y axis = wickets, economy. x axis = batting style)
    completedf = deliveries.merge(players[['player_id', 'player_name', 'batting_style']], left_on='batsman_id',
                                  right_on='player_id').drop(columns='player_id').rename(
        columns={'player_name': 'batsman_name'})
    completedf = completedf.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                  right_on='player_id').drop(columns='player_id').rename(
        columns={'player_name': 'bowler_name'})
    completedf = completedf[completedf['bowler_name'] == name]

    bowlerdf = completedf.copy()
    bowlerdf['wickets'] = (completedf['batsman_id'] == completedf['out_player_id']).astype(int)
    bowlerdf = bowlerdf.groupby('batting_style').agg(
        {'wickets': 'sum', 'batsman_runs': 'sum', 'over': 'count'}).reset_index()
    bowlerdf['economy'] = round(bowlerdf['batsman_runs'] / (bowlerdf['over'] / 6), 2)

    # Subplot 2: Economy in Different Overs of the Match (Line plot, y axis= economy, x axis = over number)
    economydf = completedf.groupby('over_number').agg({'batsman_runs': 'sum', 'over': 'count'}).reset_index()
    economydf['economy'] = round(economydf['batsman_runs'] / (economydf['over'] / 6), 2)
    economydf = economydf[['over_number', 'economy']]

    # Subplot 3: Performance in Different Situations of the Match (Heatmap)
    heatmapdf = completedf.copy()
    heatmapdf['match_situation'] = heatmapdf['over'].apply(lambda x: over_situation(x))
    heatmapdf['ball_outcome'] = heatmapdf['batsman_runs'].apply(lambda x: bowling_outcome(x))
    heatmapdf = heatmapdf.pivot_table(index='match_situation', columns='ball_outcome', values='batsman_runs',
                                      aggfunc='count')

    # Subplot 4: Relationship Between Wickets and overs bowled (scatterplot, size of each circle = wickets)
    wicketdf = completedf.copy()
    wicketdf['wickets'] = (wicketdf['batsman_id'] == wicketdf['out_player_id']).astype(int)
    wicketdf = wicketdf.groupby('over_number')['wickets'].sum().reset_index()

    # Subplot 5: Distribution of Types of Wickets Taken
    piewickets = battingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                   right_on='player_id').drop(columns='player_id').rename(
        columns={'player_name': 'bowler_name'})
    piewickets = piewickets[piewickets['bowler_name'] == 'Jasprit Bumrah']
    piewickets = piewickets.groupby('wickettype').count()['isout'].reset_index()

    # Subplot 6: Distribution of Delivery Outcomes
    pieoutcome = deliveries.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                  right_on='player_id').drop(columns='player_id').rename(
        columns={'player_name': 'bowler_name'})
    pieoutcome = pieoutcome[pieoutcome['bowler_name'] == 'Jasprit Bumrah']
    pieoutcome['ball_outcome'] = pieoutcome['batsman_runs'].apply(lambda x: bowling_outcome(x))
    pieoutcome = pieoutcome.groupby('ball_outcome').count()['batsman_runs'].reset_index()

    return bowlerdf, economydf, heatmapdf, wicketdf, piewickets, pieoutcome

def favbatsman(deliveries, players,name, sort_by):
    favbatsman = deliveries.merge(players[['player_id', 'player_name', 'batting_style']], left_on='batsman_id', right_on='player_id').rename(columns={'player_name': 'batsman_name'}).drop(columns='player_id')
    favbatsman = favbatsman.merge(players[['player_id', 'player_name', 'bowling_style']], left_on='bowler_id', right_on='player_id').rename(columns={'player_name': 'bowler_name'}).drop(columns='player_id')
    favbatsman = favbatsman[favbatsman['bowler_name'] == name]
    favbatsman['wickets'] = (favbatsman['out_player_id'] == favbatsman['batsman_id']).astype(int)
    favbatsman = favbatsman.groupby(['batsman_name', 'batting_style']).agg({'wickets':'sum','batsman_runs':'sum', 'over':'count'}).reset_index()
    favbatsman['economy'] = round(favbatsman['batsman_runs']/(favbatsman['over']/6),2)
    favbatsman['average'] = round(favbatsman['batsman_runs']/favbatsman['wickets'],2)
    favbatsman['strike rate'] = round(favbatsman['over']/favbatsman['wickets'],2)
    favbatsman = favbatsman.rename(columns={'batsman_name': 'batsman name', 'batting_style': 'batting style', 'batsman_runs': 'batsman runs'})
    favbatsman = favbatsman[favbatsman['over'] >= 24]
    favbatsman = favbatsman[['batsman name', "batting style", 'wickets', 'batsman runs', 'economy', 'average', 'strike rate']]
    favbatsman['batsman runs'] = favbatsman['batsman runs'].astype(int)
    if sort_by == 'wickets':
        favbatsman = favbatsman.sort_values(['wickets', 'batsman runs'], ascending=[False, True]).head(10).reset_index(drop=True)
    elif sort_by == 'batsman runs':
        favbatsman = favbatsman.sort_values(['batsman runs', 'wickets'], ascending=[True, False]).head(10).reset_index(drop=True)
    elif sort_by == 'economy':
        favbatsman = favbatsman.sort_values(['economy', 'batsman runs'], ascending=[True, True]).head(10).reset_index(drop=True)
    elif sort_by == 'average':
        favbatsman = favbatsman.sort_values(['average', 'wickets', 'batsman runs'], ascending=[True, False, True]).head(10).reset_index(drop=True)
    elif sort_by == 'strike rate':
        favbatsman = favbatsman.sort_values(['strike rate', 'wickets', 'batsman runs'], ascending=[True, False, True]).head(10).reset_index(drop=True)

    favbat3 = favbatsman.iloc[0:3]
    favbat3 = favbat3.merge(players[['player_name', 'image_url']], left_on='batsman name', right_on='player_name').drop(columns='player_name')

    return favbatsman, favbat3


# Worst Batsman
def worstbatsman(deliveries, players, name, sort_by):
    worstbatsman = deliveries.merge(players[['player_id', 'player_name', 'batting_style']], left_on='batsman_id',
                                    right_on='player_id').rename(columns={'player_name': 'batsman_name'}).drop(
        columns='player_id')
    worstbatsman = worstbatsman.merge(players[['player_id', 'player_name', 'bowling_style']], left_on='bowler_id',
                                      right_on='player_id').rename(columns={'player_name': 'bowler_name'}).drop(
        columns='player_id')
    worstbatsman = worstbatsman[worstbatsman['bowler_name'] == name]
    worstbatsman['wickets'] = (worstbatsman['out_player_id'] == worstbatsman['batsman_id']).astype(int)
    worstbatsman = worstbatsman.groupby(['batsman_name', 'batting_style']).agg(
        {'wickets': 'sum', 'batsman_runs': 'sum', 'over': 'count'}).reset_index()
    worstbatsman['economy'] = round(worstbatsman['batsman_runs'] / (worstbatsman['over'] / 6), 2)
    worstbatsman['average'] = round(worstbatsman['batsman_runs'] / worstbatsman['wickets'], 2)
    worstbatsman['strike rate'] = round(worstbatsman['over'] / worstbatsman['wickets'], 2)
    worstbatsman = worstbatsman.rename(
        columns={'batsman_name': 'batsman name', 'batting_style': 'batting style', 'batsman_runs': 'batsman runs'})
    worstbatsman = worstbatsman[worstbatsman['over'] >= 24]
    worstbatsman = worstbatsman[
        ['batsman name', "batting style", 'wickets', 'batsman runs', 'economy', 'average', 'strike rate']]
    worstbatsman['batsman runs'] = worstbatsman['batsman runs'].astype(int)
    if sort_by == 'wickets':
        worstbatsman = worstbatsman.sort_values(['wickets', 'batsman runs'], ascending=[True, False]).head(
            10).reset_index(drop=True)
    elif sort_by == 'batsman runs':
        worstbatsman = worstbatsman.sort_values(['batsman runs', 'wickets'], ascending=[False, True]).head(
            10).reset_index(drop=True)
    elif sort_by == 'economy':
        worstbatsman = worstbatsman.sort_values(['economy', 'batsman runs'], ascending=[False, False]).head(
            10).reset_index(drop=True)
    elif sort_by == 'average':
        worstbatsman = worstbatsman.sort_values(['average', 'wickets', 'batsman runs'],
                                                ascending=[False, True, False]).head(10).reset_index(drop=True)
    elif sort_by == 'strike rate':
        worstbatsman = worstbatsman.sort_values(['strike rate', 'wickets', 'batsman runs'],
                                                ascending=[False, True, False]).head(10).reset_index(drop=True)

    worstbat3 = worstbatsman.iloc[0:3]
    worstbat3 = worstbat3.merge(players[['player_name', 'image_url']], left_on='batsman name',
                              right_on='player_name').drop(columns='player_name')

    return worstbatsman, worstbat3

def ipl_records_batting1(battingcard,players):
    mostruns = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                 right_on='player_id').drop(columns='player_id')
    mostruns = mostruns.groupby('player_name').agg({'match_id': 'count', 'runs': 'sum'}).reset_index().rename(
        columns={'match_id': 'innings'})
    mostruns['runs'] = mostruns['runs'].astype(int)
    mostruns = mostruns.sort_values('runs', ascending=False).head(15).reset_index(drop=True)
    mostruns

    top3runs = mostruns.iloc[0:3]
    top3runs = top3runs.merge(players[['player_name', 'image_url']], on='player_name')

    highscore = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                  right_on='player_id').drop(columns='player_id')
    highscore['team'] = highscore['team'].apply(lambda x: fullname(x))
    highscore = highscore[['player_name', 'team', 'runs', 'balls', 'fours', 'sixes', 'strikerate']].sort_values('runs',
                                                                                                                ascending=False).head(
        15).reset_index(drop=True)
    highscore['runs'] = highscore['runs'].astype(int)
    highscore['balls'] = highscore['balls'].astype(int)
    highscore['fours'] = highscore['fours'].astype(int)
    highscore['sixes'] = highscore['sixes'].astype(int)

    top3highscore = highscore.iloc[0:3]
    top3highscore = top3highscore.merge(players[['player_name', 'image_url']], on='player_name')

    bestavg = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns='player_id')
    bestavg = bestavg.groupby('player_name').agg({'runs': 'sum', 'isout': 'sum', 'balls': 'sum'}).reset_index()
    bestavg = bestavg[bestavg['runs'] >= 1000]
    bestavg['average'] = (bestavg['runs'] / bestavg['isout'])
    bestavg = bestavg.sort_values('average', ascending=False).head(15).reset_index(drop=True)
    bestavg['average'] = round(bestavg['average'].astype(float), 2)
    bestavg['runs'] = bestavg['runs'].astype(int)
    bestavg = bestavg.rename(columns={'isout': 'dismissals'})
    bestavg = bestavg[['player_name', 'average', 'runs', 'dismissals']]

    top3avg = bestavg.iloc[0:3]
    top3avg = top3avg.merge(players[['player_name', 'image_url']], on='player_name')

    beststriker = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                    right_on='player_id').drop(columns='player_id')
    beststriker = beststriker.groupby('player_name').agg(
        {'runs': 'sum', 'match_id': 'count', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum'}).reset_index()
    beststriker = beststriker[beststriker['runs'] >= 1000]
    beststriker['strike rate'] = round((beststriker['runs'] / beststriker['balls']) * 100, 2)
    beststriker = beststriker.sort_values('strike rate', ascending=False).head(15).reset_index(drop=True)
    beststriker['runs'] = beststriker['runs'].astype(int)
    beststriker['balls'] = beststriker['balls'].astype(int)
    beststriker['fours'] = beststriker['fours'].astype(int)
    beststriker['sixes'] = beststriker['sixes'].astype(int)
    beststriker = beststriker.rename(columns={'match_id': 'innings'})
    beststriker = beststriker[['player_name', 'innings', 'runs', 'balls', 'fours', 'sixes', 'strike rate']]

    top3striker = beststriker.iloc[0:3]
    top3striker = top3striker.merge(players[['player_name', 'image_url']], on='player_name')

    return mostruns,top3runs,highscore,top3highscore,bestavg,top3avg, beststriker, top3striker

def ipl_records_batting2(battingcard,players):
    most100 = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns='player_id')
    most100 = most100[most100['runs'] >= 100]
    most100 = most100.groupby('player_name').agg({'match_id': 'count', 'runs': 'max'}).reset_index().sort_values(
        'match_id', ascending=False).head(10).rename(
        columns={'match_id': 'hundreds', 'runs': 'highest score'}).reset_index(drop=True)
    most100['highest score'] = most100['highest score'].astype(int)

    top3centuries = most100.iloc[0:3]
    top3centuries = top3centuries.merge(players[['player_name', 'image_url']], on='player_name')

    most50 = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id', right_on='player_id').drop(
        columns='player_id')
    most50 = most50[(most50['runs'] >= 50) & (most50['runs'] < 100)]
    most50 = most50.groupby('player_name').agg({'match_id': 'count', 'runs': 'max'}).reset_index().sort_values(
        'match_id', ascending=False).head(10).rename(
        columns={'match_id': 'fifties', 'runs': 'highest score (non 100)'}).reset_index(drop=True)
    most50['highest score (non 100)'] = most50['highest score (non 100)'].astype(int)

    top350 = most50.iloc[0:3]
    top350 = top350.merge(players[['player_name', 'image_url']], on='player_name')

    mostfours = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                  right_on='player_id').drop(columns='player_id')
    mostfours = mostfours.groupby('player_name').agg(
        {'runs': 'sum', 'match_id': 'count', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum'}).reset_index().sort_values(
        'fours', ascending=False).head(10).reset_index(drop=True).rename(columns={'match_id': 'innings'})
    mostfours['runs'] = mostfours['runs'].astype(int)
    mostfours['fours'] = mostfours['fours'].astype(int)
    mostfours['sixes'] = mostfours['sixes'].astype(int)
    mostfours = mostfours[['player_name', 'innings', 'runs', 'fours', 'sixes']]

    top3fours = mostfours.iloc[0:3]
    top3fours = top3fours.merge(players[['player_name', 'image_url']], on='player_name')

    mostsixes = battingcard.merge(players[['player_id', 'player_name']], left_on='batsman_id',
                                  right_on='player_id').drop(columns='player_id')
    mostsixes = mostsixes.groupby('player_name').agg(
        {'runs': 'sum', 'match_id': 'count', 'balls': 'sum', 'fours': 'sum', 'sixes': 'sum'}).reset_index().sort_values(
        'sixes', ascending=False).head(10).reset_index(drop=True).rename(columns={'match_id': 'innings'})
    mostsixes['runs'] = mostsixes['runs'].astype(int)
    mostsixes['fours'] = mostsixes['fours'].astype(int)
    mostsixes['sixes'] = mostsixes['sixes'].astype(int)
    mostsixes = mostsixes[['player_name', 'innings', 'runs', 'fours', 'sixes']]

    top3sixes = mostsixes.iloc[0:3]
    top3sixes = top3sixes.merge(players[['player_name', 'image_url']], on='player_name')

    return most100, top3centuries, most50, top350, mostfours, top3fours, mostsixes, top3sixes

def ipl_bowling_record(bowlingcard, players):
    # Bowling Records
    mostwickets = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                    right_on='player_id').drop(columns='player_id')
    mostwickets = mostwickets.groupby('player_name').agg({'wickets': 'sum'}).reset_index().sort_values('wickets',
                                                                                                       ascending=False).head(
        10)
    mostwickets['wickets'] = mostwickets['wickets'].astype(int)
    mostwickets = mostwickets.reset_index(drop=True)

    top3wickets = mostwickets.iloc[0:3]
    top3wickets = top3wickets.merge(players[['player_name', 'image_url']], on='player_name')

    bestbowlfig = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                    right_on='player_id').drop(columns='player_id')
    bestbowlfig = bestbowlfig.sort_values(['player_name', 'wickets', 'conceded'], ascending=[True, False, True])
    bestbowlfig = bestbowlfig[['player_name', 'overs', 'conceded', 'wickets']].drop_duplicates(subset='player_name')
    bestbowlfig = bestbowlfig.sort_values(['wickets', 'conceded'], ascending=[False, True]).head(10)
    bestbowlfig['wickets'] = bestbowlfig['wickets'].astype(int)
    bestbowlfig['conceded'] = bestbowlfig['conceded'].astype(int)
    bestbowlfig = bestbowlfig.reset_index(drop=True)

    top3bowlfig = bestbowlfig.iloc[0:3]
    top3bowlfig = top3bowlfig.merge(players[['player_name', 'image_url']], on='player_name')

    most3wickets = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                     right_on='player_id').drop(columns='player_id')
    most3wickets = most3wickets[most3wickets['wickets'] >= 3]
    most3wickets = most3wickets.groupby('player_name')['wickets'].count().reset_index().sort_values('wickets',
                                                                                                    ascending=False).head(
        10).reset_index(drop=True).rename(columns={'wickets': '3 wicket hauls'})

    top3fers = most3wickets.iloc[0:3]
    top3fers = top3fers.merge(players[['player_name', 'image_url']], on='player_name')

    bestbowlavg = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                    right_on='player_id').drop(columns='player_id')
    bestbowlavg = bestbowlavg.groupby('player_name').agg({'wickets': 'sum', 'conceded': 'sum'}).reset_index()
    bestbowlavg = bestbowlavg[bestbowlavg['wickets'] >= 50]
    bestbowlavg['average'] = round(bestbowlavg['conceded'] / bestbowlavg['wickets'], 2)
    bestbowlavg['wickets'] = bestbowlavg['wickets'].astype(int)
    bestbowlavg['conceded'] = bestbowlavg['conceded'].astype(int)
    bestbowlavg['average'] = bestbowlavg['average'].astype(float)
    bestbowlavg = bestbowlavg.sort_values('average', ascending=True).head(10).reset_index(drop=True)

    top3bowlavg = bestbowlavg.iloc[0:3]
    top3bowlavg = top3bowlavg.merge(players[['player_name', 'image_url']], on='player_name')

    bestbowleco = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                    right_on='player_id').drop(columns='player_id')
    bestbowleco = bestbowleco.groupby('player_name')[['conceded', 'overs']].sum().reset_index()
    bestbowleco = bestbowleco[bestbowleco['overs'] >= 100]
    bestbowleco['economy'] = round(bestbowleco['conceded'] / bestbowleco['overs'], 2)
    bestbowleco['conceded'] = bestbowleco['conceded'].astype(int)
    bestbowleco = bestbowleco.sort_values('economy', ascending=True).head(10).reset_index(drop=True)

    top3economy = bestbowleco.iloc[0:3]
    top3economy = top3economy.merge(players[['player_name', 'image_url']], on='player_name')

    bestbowlstriker = bowlingcard.merge(players[['player_id', 'player_name']], left_on='bowler_id',
                                        right_on='player_id').drop(columns='player_id')
    bestbowlstriker = bestbowlstriker.groupby('player_name').agg({'wickets': 'sum', 'balls': 'sum'}).reset_index()
    bestbowlstriker = bestbowlstriker[bestbowlstriker['wickets'] >= 50]
    bestbowlstriker['strike rate'] = round(bestbowlstriker['balls'] / bestbowlstriker['wickets'], 2)
    bestbowlstriker['wickets'] = bestbowlstriker['wickets'].astype(int)
    bestbowlstriker['balls'] = bestbowlstriker['balls'].astype(int)
    bestbowlstriker = bestbowlstriker.sort_values('strike rate', ascending=True).head(10).reset_index(drop=True)

    top3striker = bestbowlstriker.iloc[0:3]
    top3striker = top3striker.merge(players[['player_name', 'image_url']], on='player_name')

    return mostwickets, top3wickets, most3wickets, top3fers, bestbowlfig, top3bowlfig, bestbowleco, top3economy, bestbowlavg, top3bowlavg, bestbowlstriker, top3striker
