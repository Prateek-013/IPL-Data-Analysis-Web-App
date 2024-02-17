import streamlit as st
import pandas as pd
import helper
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from lightgbm import LGBMRegressor


results = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/IPL-Data-Analysis-Web-App/main/results.csv')
deliveries = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/IPL-Data-Analysis-Web-App/main/ipl_ball_by_ball_data.csv')
battingcard = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/IPL-Data-Analysis-Web-App/main/ipl_batting_card.csv')
bowlingcard = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/IPL-Data-Analysis-Web-App/main/ipl_bowling_card.csv')
players = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/IPL-Data-Analysis-Web-App/main/ipl_players_info.csv')

st.set_page_config(layout="wide")

st.sidebar.title('IPL Analysis')
st.sidebar.image(r'https://th.bing.com/th?id=OIP.Ul-BofEafiIrwwMAKJ3C5QHaDm&w=350&h=170&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2')


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Home Page', 'Match Scorecard', 'Team Analysis', 'Player Analysis', 'IPL Records', '2024 Predictions')
)

if user_menu == 'Home Page':
    # st.title("IPL Statistics & Analysis (2008-2023)")
    st.markdown("<h1 style='text-align: center;'>IPL Statistics & Analysis (2008-2023)</h1>", unsafe_allow_html=True)
    image_url = "https://th.bing.com/th/id/R.eb4b4d161b90079c6fa57bca0ecfda91?rik=H%2fksdInnSgEHOQ&pid=ImgRaw&r=0"
    st.image(image_url, caption="IPL Image", use_column_width=True)


    col1, col2 = st.columns(2)

    with col1:
        st.header('Total Players')
        st.subheader('696')
    with col2:
        st.header('Nationalities')
        st.subheader('16')

    col1, col2 = st.columns(2)

    with col1:
        st.header('Ad Revenue in 2023')
        st.subheader('$442 Million')
    with col2:
        st.header('Valuation')
        st.subheader('$10.7 Billion')

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write(f"**Disclaimer:** "
             f"The statistics presented herein are derived exclusively from completed games. All abandoned games have been systematically excluded from the analysis. Consequently, there may be slight variations between the presented statistics and actual statistics. Users are encouraged to interpret the data with this consideration in mind.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.write(f"**Data Source Credit**")
    st.markdown('[Bhuvanesh Prasad, Kaggle Expert](https://www.kaggle.com/bhuvaneshprasad)')

if user_menu == 'Match Scorecard':
    available_season = results['season'].unique().tolist()
    selected_season = st.sidebar.selectbox('Select a Season', available_season)
    available_matches = results[results['season'] == selected_season]['match_name'].unique().tolist()
    selected_match = st.sidebar.selectbox('Select a Match', available_matches)
    match, batting, bowling = helper.match_scorecard(results, battingcard, bowlingcard,players, selected_match, selected_season)

    st.title('Match Scorecard of ' + selected_match + ', ' + str(selected_season))

    col1,col2,col3 = st.columns(3)


    col1.image(match['team1_url'][0])
    col2.markdown(' ')
    col3.image(match['team2_url'][0])

    st.markdown(f"**Match Date:** {match['match_date'][0]}")
    st.markdown(f"**Match Venue:** {match['match_venue_stadium'][0]}")
    st.markdown(f"**Match Location:** {match['match_venue_city'][0]},{match['match_venue_country'][0]}")

    st.markdown(f"**Toss Result:** {match['toss_winner'][0]} won the toss and chose to {match['toss_winner_choice'][0]}.")

    col1, col2 = st.columns(2)

    with col1:
        #First Innings Batting
        st.subheader(f"**1st Innings:** {match['team1_name'][0]} scored {match['team1_runs_scored'][0].astype(int)}/{match['team1_wickets_fell'][0].astype(int)}.")
        first_innings_batting_top5 = batting[(batting['innings'] == 1) & (batting['runs'].notnull())].sort_values(by='runs', ascending=False).head(5)
    
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='player_name', y='runs', data=first_innings_batting_top5, palette='viridis')
        plt.xticks(rotation=90, ha='center')
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
                        textcoords='offset points')
        plt.title('Top 5 Batsmen in 1st Innings')
        plt.xlabel('Batsmen')
        plt.ylabel('Runs')
        st.pyplot(fig)
    
        column_dtypes = {'runs': 'int', 'balls': 'int', 'fours': 'int', 'sixes': 'int', 'strikerate': 'float'}
        tempbattingdf = first_innings_batting_top5[['player_name', 'runs', 'balls', 'fours', 'sixes', 'strikerate']]
        tempbattingdf = tempbattingdf.astype(column_dtypes)
        st.table(tempbattingdf.reset_index(drop=True))


        #First Innings Bowling
    
        first_innings_bowling_top5 = bowling[(bowling['innings'] == 1) & (bowling['wickets'] != 0)].sort_values(by=['wickets', 'economy'],
                                                                                              ascending=[False, True]).head(5)
        fig, ax = plt.subplots(figsize=(12, 8))  # Increase figure size
        labels = [f"{player['player_name']} ({int(player['wickets'])}/{int(player['conceded'])})" for _, player in
                  first_innings_bowling_top5.iterrows()]
        wedges, texts, autotexts = ax.pie(first_innings_bowling_top5['wickets'], labels=labels, startangle=90, autopct='',
                                          pctdistance=0.85, colors=sns.color_palette('viridis'))
        plt.title('Top Bowlers in 1st Innings')
        st.pyplot(fig)
    
        column_bowling_dtypes = {'overs': 'float', 'wickets': 'int', 'conceded': 'int', 'economy': 'float'}
        tempbowlingdf = first_innings_bowling_top5[['player_name', 'overs', 'wickets', 'conceded', 'economy']]
        tempbowlingdf = tempbowlingdf.astype(column_bowling_dtypes)
        st.table(tempbowlingdf.reset_index(drop=True))


    with col2:
        #Second Innings Batting
        st.subheader(f"**2nd Innings:** {match['team2_name'][0]} scored {match['team2_runs_scored'][0].astype(int)}/{match['team2_wickets_fell'][0].astype(int)}.")
        second_innings_batting_top5 = batting[(batting['innings'] == 2) & (batting['runs'].notnull())].sort_values(by='runs', ascending=False).head(5)
    
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='player_name', y='runs', data=second_innings_batting_top5, palette='viridis')
        plt.xticks(rotation=90, ha='center')
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 10),
                        textcoords='offset points')
        plt.title('Top 5 Batsmen in 2nd Innings')
        plt.xlabel('Batsmen')
        plt.ylabel('Runs')
        st.pyplot(fig)
    
        column_dtypes = {'runs': 'int', 'balls': 'int', 'fours': 'int', 'sixes': 'int', 'strikerate': 'float'}
        tempbattingdf2 = second_innings_batting_top5[['player_name', 'runs', 'balls', 'fours', 'sixes', 'strikerate']]
        tempbattingdf2 = tempbattingdf2.astype(column_dtypes)
        st.table(tempbattingdf2.reset_index(drop=True))

        #Second Innings Bowling
        second_innings_bowling_top5 = bowling[(bowling['innings'] == 2) & (bowling['wickets'] != 0)].sort_values(by=['wickets', 'economy'],ascending=[False, True]).head(5)
        fig, ax = plt.subplots(figsize=(12, 8))  # Increase figure size
        labels = [f"{player['player_name']} ({int(player['wickets'])}/{int(player['conceded'])})" for _, player in
                  second_innings_bowling_top5.iterrows()]
        wedges, texts, autotexts = ax.pie(second_innings_bowling_top5['wickets'], labels=labels, startangle=90, autopct='',
                                          pctdistance=0.85, colors=sns.color_palette('viridis'))
        plt.title('Top Bowlers in 2nd Innings')
        st.pyplot(fig)
    
        column_bowling_dtypes = {'overs': 'float', 'wickets': 'int', 'conceded': 'int', 'economy': 'float'}
        tempbowlingdf2 = second_innings_bowling_top5[['player_name', 'overs', 'wickets', 'conceded', 'economy']]
        tempbowlingdf2 = tempbowlingdf2.astype(column_bowling_dtypes)
        st.table(tempbowlingdf2.reset_index(drop=True))

    tempballbyball, tempresult = helper.match_scorecard_line(results, deliveries, selected_match, selected_season)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=tempballbyball[tempballbyball['innings_no'] == 1.0]['over_number'],
                 y=tempballbyball[tempballbyball['innings_no'] == 1.0]['current_innings_runs'], label=f"1st Innings: {tempresult.iloc[0]['team1_name']}",
                 color='red')
    sns.lineplot(x=tempballbyball[tempballbyball['innings_no'] == 2.0]['over_number'],
                 y=tempballbyball[tempballbyball['innings_no'] == 2.0]['current_innings_runs'], label=f"2nd Innings: {tempresult.iloc[0]['team2_name']}",
                 color='blue')
    wickets_1st_innings = tempballbyball[(tempballbyball['innings_no'] == 1.0) & (tempballbyball['iswicket'] == True)]
    plt.scatter(x=wickets_1st_innings['over_number'], y=wickets_1st_innings['current_innings_runs'],
                marker='o', color='red', label='Wicket (1st Innings)')
    wickets_2nd_innings = tempballbyball[(tempballbyball['innings_no'] == 2.0) & (tempballbyball['iswicket'] == True)]
    plt.scatter(x=wickets_2nd_innings['over_number'], y=wickets_2nd_innings['current_innings_runs'],
                marker='o', color='blue', label='Wicket (2nd Innings)')
    plt.xticks(range(1, 21))
    plt.xlabel('Over Number')
    plt.ylabel('Current Innings Runs')
    plt.title('Team Runs & Wickets throughout the Innings')
    st.pyplot(fig)

    st.subheader(f"**Match Result:** {match['match_result_text'][0]}.")
    st.subheader(f"Man of the Match")
    st.image(match['image_url'][0], caption=match['player_name'][0], width=150)

    centered_text = f"<h2 style='text-align: center;'>Team Comparison</h2>"
    st.markdown(centered_text, unsafe_allow_html=True)

    table_data = [
        {'Particulars': 'Total Runs', f"{match['team1_name'][0]}": f"{int(match['team1_runs_scored'][0])}",f"{match['team2_name'][0]}": f"{int(match['team2_runs_scored'][0])}"},
        {'Particulars': 'Powerplay Runs', f"{match['team1_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 1.0) & (tempballbyball['over'] <=6)]['total_runs'].sum())}", f"{match['team2_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 2.0) & (tempballbyball['over'] <=6)]['total_runs'].sum())}"},
        {'Particulars': 'Middle Over Runs', f"{match['team1_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 1.0) & (tempballbyball['over'] >=6) & (tempballbyball['over'] <=15)]['total_runs'].sum())}", f"{match['team2_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 2.0) & (tempballbyball['over'] >=6) & (tempballbyball['over'] <=15)]['total_runs'].sum())}"},
        {'Particulars': 'Death Over Runs', f"{match['team1_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 1.0) & (tempballbyball['over'] >15) & (tempballbyball['over'] <=20)]['total_runs'].sum())}", f"{match['team2_name'][0]}": f"{int(tempballbyball[(tempballbyball['innings_no'] == 2.0) & (tempballbyball['over'] >15) & (tempballbyball['over'] <=20)]['total_runs'].sum())}"},
        {'Particulars': 'Sixes', f"{match['team1_name'][0]}" : f"{int(batting[batting['innings'] == 1]['sixes'].sum())}", f"{match['team2_name'][0]}" : f"{int(batting[batting['innings'] == 2]['sixes'].sum())}"},
        {'Particulars': 'Fours', f"{match['team1_name'][0]}": f"{int(batting[batting['innings'] == 1]['fours'].sum())}", f"{match['team2_name'][0]}": f"{int(batting[batting['innings'] == 2]['fours'].sum())}"},
        {'Particulars': 'Run Outs', f"{match['team1_name'][0]}" : f"{batting[(batting['innings'] == 1) & (batting['wickettype'] =='run out')]['wickettype'].count()}", f"{match['team2_name'][0]}" : f"{batting[(batting['innings'] == 2) & (batting['wickettype'] =='run out')]['wickettype'].count()}"}
    ]

    st.table(table_data)

if user_menu == 'Team Analysis':
    results['team1_name'] = results['team1_name'].apply(lambda x: helper.fullname(x))
    available_teams = results['team1_name'].unique().tolist()
    available_teams.sort()
    selected_team = st.sidebar.selectbox('Select a Team', available_teams)
    titles, games, wins, losses, teamurl = helper.basic_stats(results, selected_team)

    # st.image(f"{teamurl}", width=400)

    centered_image_html = f"<div style='display: flex; justify-content: center;'><img src='{teamurl}' width='400'></div>"

    st.markdown(centered_image_html, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.header('Games Played')
        st.subheader(f"{games}")
    with col2:
        st.header('Total Wins')
        st.subheader(f"{wins}")
    with col3:
        st.header('Total Losses')
        st.subheader(f"{losses}")
    with col4:
        st.header('Titles Won')
        st.subheader(f"{titles}")


    headtohead, stadium, runs, wickets, topbatter, topbowler = helper.team_performance(results, players, battingcard, bowlingcard, selected_team)

    centered_text = f"<h2 style='text-align: center;'>Head to Head Record Against Opponents</h2>"
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(centered_text, unsafe_allow_html=True)
    st.table(headtohead)
    st.markdown("<br>", unsafe_allow_html=True)
    centered_text = f"<h2 style='text-align: center;'>Win/Loss Record in Different Stadiums</h2>"
    st.markdown(centered_text, unsafe_allow_html=True)
    st.table(stadium)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    centered_text = f"<h2 style='text-align: center;'>Top Runs Scorers for {selected_team}</h2>"
    st.markdown(centered_text, unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader(f"{topbatter.iloc[0]['player_name']}")
        image_url = f"{topbatter.iloc[0]['image_url']}"
        caption = f"1. {topbatter.iloc[0]['runs']} runs"
        st.image(image_url, caption, width=175)
    with col2:
        st.subheader(f"{topbatter.iloc[1]['player_name']}")
        image_url = f"{topbatter.iloc[1]['image_url']}"
        caption = f"2. {topbatter.iloc[1]['runs']} runs"
        st.image(image_url, caption, width=175)
    with col3:
        st.subheader(f"{topbatter.iloc[2]['player_name']}")
        image_url = f"{topbatter.iloc[2]['image_url']}"
        caption = f"3. {topbatter.iloc[2]['runs']} runs"
        st.image(image_url, caption, width=175)
    st.table(runs)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    centered_text = f"<h2 style='text-align: center;'>Top Wicket Takers for {selected_team}</h2>"
    st.markdown(centered_text, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(f"{topbowler.iloc[0]['player_name']}")
        image_url = f"{topbowler.iloc[0]['image_url']}"
        caption = f"1. {topbowler.iloc[0]['wickets']} wickets"
        st.image(image_url, caption, width=175)
    with col2:
        st.subheader(f"{topbowler.iloc[1]['player_name']}")
        image_url = f"{topbowler.iloc[1]['image_url']}"
        caption = f"2. {topbowler.iloc[1]['wickets']} wickets"
        st.image(image_url, caption, width=175)
    with col3:
        st.subheader(f"{topbowler.iloc[2]['player_name']}")
        image_url = f"{topbowler.iloc[2]['image_url']}"
        caption = f"3. {topbowler.iloc[2]['wickets']} wickets"
        st.image(image_url, caption, width=175)
    st.table(wickets)

    teambat, teambowl = helper.teambattingbowling(battingcard,bowlingcard,results, selected_team)

    #batting
    fig = sp.make_subplots(rows=3, cols=1, subplot_titles=['Average Runs per match Over the Years',
                                                           'Average Sixes per match Over the Years',
                                                           'Average Fours per match Over the Years'],
                           shared_xaxes=True, vertical_spacing=0.1, row_heights=[1, 1, 1])

    # Add traces for each metric
    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['Avg Runs'], mode='lines+markers', name='Avg Runs',
                   line=dict(color='red')), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['League Avg Runs'], mode='lines', name='League Avg Runs',
                   line=dict(color='black', dash='dash')), row=1, col=1)

    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['Avg Sixes'], mode='lines+markers', name='Avg Sixes',
                   line=dict(color='blue')), row=2, col=1)
    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['League Avg Sixes'], mode='lines', name='League Avg Sixes',
                   line=dict(color='black', dash='dash')), row=2, col=1)

    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['Avg Fours'], mode='lines+markers', name='Avg Fours',
                   line=dict(color='green')), row=3, col=1)
    fig.add_trace(
        go.Scatter(x=teambat['season'], y=teambat['League Avg Fours'], mode='lines', name='League Avg Fours',
                   line=dict(color='black', dash='dash')), row=3, col=1)

    # Update layout
    fig.update_layout(title_text='',
                      showlegend=True,
                      height=800, width=1100)  # Adjust the overall height of the figure
    centered_text = f"<h2 style='text-align: center;'>{selected_team} Batting Performance Over the Years</h2>"
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(centered_text, unsafe_allow_html=True)
    st.plotly_chart(fig)

    #Bowling
    fig = sp.make_subplots(rows=3, cols=1,
                           subplot_titles=['Avg Wickets Taken Over the Years', 'Avg Runs Conceded Over the Years',
                                           'Avg Sixes Conceded Over the Years'],
                           shared_xaxes=True, vertical_spacing=0.1, row_heights=[1, 1, 1])

    # Add traces for each metric
    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['Avg Wickets Taken'], mode='lines+markers',
                             name='Avg Wickets Taken', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['League Avg Wickets Taken'], mode='lines',
                             name='League Avg Wickets Taken', line=dict(color='black', dash='dash')), row=1, col=1)

    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['Avg Runs Conceded'], mode='lines+markers',
                             name='Avg Runs Conceded', line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['League Avg Runs Conceded'], mode='lines',
                             name='League Avg Runs Conceded', line=dict(color='black', dash='dash')), row=2, col=1)

    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['Avg Sixes Conceded'], mode='lines+markers',
                             name='Avg Sixes Conceded', line=dict(color='green')), row=3, col=1)
    fig.add_trace(go.Scatter(x=teambowl['season'], y=teambowl['League Avg Sixes Conceded'], mode='lines',
                             name='League Avg Sixes Conceded', line=dict(color='black', dash='dash')), row=3, col=1)

    # Update layout
    fig.update_layout(title_text='',
                      showlegend=True,
                      height=800, width=1100)  # Adjust the overall height of the figure

    centered_text = f"<h2 style='text-align: center;'>{selected_team} Bowling Performance Over the Years</h2>"
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(centered_text, unsafe_allow_html=True)
    st.plotly_chart(fig)

if user_menu == 'Player Analysis':
    playerlist = players['player_name'].tolist()
    playerlist.sort()
    selected_player = st.sidebar.selectbox('Select a Player', playerlist)
    selected_about = st.sidebar.selectbox('Select an Option', ['Player Overview', 'Batting', 'Bowling'])

    if selected_about == 'Player Overview':
        playername, age, battingstyle, bowlingstyle, stint, image = helper.player_overview(players, results,
                                                                                           selected_player,
                                                                                           selected_about)
        centered_text = f"<h1 style='text-align: center;'>Player Overview: {playername}</h1>"
        st.markdown(centered_text, unsafe_allow_html=True)
        centered_image_html = f"<div style='display: flex; justify-content: center;'><img src='{image}' width='300'></div>"
        st.markdown(centered_image_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2,col3 = st.columns(3)
        with col1:
            st.subheader('Age')
            st.markdown(f"<p style='font-size:20px;'>{age} years</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col2:
            st.subheader('Batting Style')
            st.markdown(f"<p style='font-size:20px;'>{battingstyle.title()}</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        with col3:
            st.subheader('Bowling Style')
            st.markdown(f"<p style='font-size:16px;'>{bowlingstyle.title()}</p>", unsafe_allow_html=True)


        st.subheader('Teams Played For')
        st.table(stint)

    if selected_about == 'Batting':
        try:
            careerruns, oppruns, stadiumruns, highscore, bataverage, batstrikerate, scores30, scores50, scores100, orangecaps, careerhighscore, innings, image = helper.player_batting(results, battingcard, players, deliveries,bowlingcard, selected_player)
            centered_text = f"<h1 style='text-align: center;'>Batting Statistics of {selected_player}</h1>"
            st.markdown(centered_text, unsafe_allow_html=True)
            centered_image_html = f"<div style='display: flex; justify-content: center;'><img src='{image}' width='300'></div>"
            st.markdown(centered_image_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
    
            with col1:
                st.subheader('Innings Played')
                st.markdown(f"<p style='font-size:20px;'>{innings}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Batting Average')
                st.markdown(f"<p style='font-size:20px;'>{bataverage}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('30+ Scores')
                st.markdown(f"<p style='font-size:20px;'>{scores30}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            with col2:
                st.subheader('Best Innings')
                st.markdown(f"<p style='font-size:20px;'>{highscore}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Batting Strike Rate')
                st.markdown(f"<p style='font-size:20px;'>{batstrikerate}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Half Centuries')
                st.markdown(f"<p style='font-size:20px;'>{scores50}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
            with col3:
                st.subheader('Best Season')
                st.markdown(f"<p style='font-size:20px;'>{careerhighscore} runs</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Orange Caps')
                st.markdown(f"<p style='font-size:20px;'>{orangecaps}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Centuries')
                st.markdown(f"<p style='font-size:20px;'>{scores100}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Runs Throughout Their IPL Career</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(careerruns)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Runs Scored Against Opponents</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(oppruns)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Runs Scored in Different Stadiums</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(stadiumruns)
    
            st.markdown("<br>", unsafe_allow_html=True)
    
            tempbowltype, tempstrike, tempinnings, temppivot, tempkde, tempdismissals =helper.player_batting_viz(deliveries, players, battingcard, selected_player)
            centered_text = f"<h2 style='text-align: center;'>Batting Analysis of {selected_player}</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
            fig = make_subplots(rows=2, cols=2,
                                subplot_titles=['Performance against Bowling Styles', 'Strike Rate Throughout the Innings',
                                                'Performance in Different Situations of the Match',
                                                'Relation Between Strike Rate and Runs'])
    
            # Subplot 1: Performance vs Bowling Styles (Bar Chart)
            trace1 = go.Bar(x=tempbowltype['bowling_style'], y=tempbowltype['average runs'], name='Average Runs',
                            marker=dict(color='blue'))
            trace2 = go.Bar(x=tempbowltype['bowling_style'], y=tempbowltype['strike rate'], name='Strike Rate',
                            marker=dict(color='green'))
            tracen = go.Bar(x=tempbowltype['bowling_style'], y=tempbowltype['dismissals'], name='Dismissals',
                            marker=dict(color='red'))
            fig.add_trace(trace1, row=1, col=1)
            fig.add_trace(trace2, row=1, col=1)
            fig.add_trace(tracen, row=1, col=1)
            fig.update_xaxes(title_text='Bowling Style', row=1, col=1)
            fig.update_yaxes(title_text='Average Runs / Strike Rate', row=1, col=1)
    
            # Subplot 2: Strike Rate throughout the innings (Line plot)
            trace3 = go.Scatter(x=tempstrike['balls_range'], y=tempstrike['strike rate'], mode='lines+markers',
                                name='Strike Rate', line=dict(color='red'))
            fig.add_trace(trace3, row=1, col=2)
            fig.update_xaxes(title_text='Balls Played', row=1, col=2)
            fig.update_yaxes(title_text='Strike Rate', row=1, col=2)
    
            # Subplot 4: Heatmap for player performance in powerplay, middle overs and death overs
            trace5 = go.Heatmap(z=temppivot.values, x=temppivot.columns, y=temppivot.index, colorscale='Viridis',
                                texttemplate="%{z}", hoverinfo='text')
            fig.add_trace(trace5, row=2, col=1)
            fig.update_xaxes(title_text='Outcome of the ball bowled', row=2, col=1)
            fig.update_yaxes(title_text='Over Situation', row=2, col=1)
    
            # Subplot 5: 2d kde plot (x='batsman_runs', y='strike rate') bivariate kde plot
            trace6 = go.Scatter(x=tempkde['batsman_runs'], y=tempkde['strike rate'], mode='markers',
                                name='Bivariate KDE Plot', marker=dict(color='purple'))
            fig.add_trace(trace6, row=2, col=2)
            fig.update_xaxes(title_text='Batsman Runs', row=2, col=2)
            fig.update_yaxes(title_text='Strike Rate', row=2, col=2)
    
            # Update layout
            fig.update_layout(height=1000, width=1500, title_text='')
    
            # Show the figure
            st.plotly_chart(fig)

            fig = make_subplots(rows=1, cols=2, subplot_titles=["Distribution of the Player's Innings",
                                                                "Distribution of Types of Dismissals"],
                                specs=[[{"type": "pie"}, {"type": "pie"}]])
            trace4 = go.Pie(values=tempinnings['batsman_runs'], labels=tempinnings['ball_outcome'])
            fig.add_trace(trace4, row=1, col=1)
            trace7 = go.Pie(values=tempdismissals['match_id'], labels=tempdismissals['wickettype'])
            fig.add_trace(trace7, row=1, col=2)
            fig.update_layout(title="",height=500, width=1500)
            st.plotly_chart(fig)
    
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>{selected_player}'s Favourite Bowlers to Face</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
    
            sort_by = st.selectbox('Sort Bowlers By', ['strike rate', 'batsman_runs', 'average'])
            favbowlerfull, favbowlertop3 = helper.favbowler(deliveries, players, selected_player, sort_by)
    
            st.markdown("<br>", unsafe_allow_html=True)
    
            col1,col2,col3 = st.columns(3)

            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{favbowlertop3['bowler_name'][1]}")
                st.image(f"{favbowlertop3['image_url'][1]}", width=150)
    
            with col2:
                st.subheader(f"{favbowlertop3['bowler_name'][0]}")
                st.image(f"{favbowlertop3['image_url'][0]}", width=150)
    
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{favbowlertop3['bowler_name'][2]}")
                st.image(f"{favbowlertop3['image_url'][2]}", width=150)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.table(favbowlerfull)
            st.write("Atleast 4 overs bowled to the batsman*")
    
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>{selected_player}'s  Least Favourite Bowlers to Face</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            sort_by2 = st.selectbox('Sort Bowlers By', ['dismissals','strike rate', 'batsman_runs', 'average'])
            worstbowlerfull, worsbowlertop3 = helper.worstbowler(deliveries, players, selected_player, sort_by2)
    
            st.markdown("<br>", unsafe_allow_html=True)
    
            col1, col2, col3 = st.columns(3)
    
            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{worsbowlertop3['bowler_name'][1]}")
                st.image(f"{worsbowlertop3['image_url'][1]}", width=150)
    
            with col2:
                st.subheader(f"{worsbowlertop3['bowler_name'][0]}")
                st.image(f"{worsbowlertop3['image_url'][0]}", width=150)
    
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{worsbowlertop3['bowler_name'][2]}")
                st.image(f"{worsbowlertop3['image_url'][2]}", width=150)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.table(worstbowlerfull)
            st.write("Atleast 4 overs bowled to the batsman*")
        except:
            st.write("Not enough Data to show further Statistics and Visualizations")

    if selected_about == 'Bowling':
        try:
            seasonbowl, performopp, performvenue, innings, wickets, economy, average, strike_rate, wickets3, wickets5, bowlhighscore, purplecap = helper.player_bowling_stats(bowlingcard,players,results, selected_player)
            image = players[players['player_name'] == selected_player].reset_index(drop=True)['image_url'][0]
    
            centered_text = f"<h1 style='text-align: center;'>Bowling Statistics of {selected_player}</h1>"
            st.markdown(centered_text, unsafe_allow_html=True)
            centered_image_html = f"<div style='display: flex; justify-content: center;'><img src='{image}' width='300'></div>"
            st.markdown(centered_image_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
    
            with col1:
                st.subheader('Matches Played')
                st.markdown(f"<p style='font-size:20px;'>{innings}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Total Wickets')
                st.markdown(f"<p style='font-size:20px;'>{wickets}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Overall Average')
                st.markdown(f"<p style='font-size:20px;'>{average}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
            with col2:
                st.subheader('Best Figures')
                st.markdown(f"<p style='font-size:20px;'>{bowlhighscore}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('3 Wicket Hauls')
                st.markdown(f"<p style='font-size:20px;'>{wickets3}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Overall Strike Rate')
                st.markdown(f"<p style='font-size:20px;'>{strike_rate}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            with col3:
                st.subheader('Purple Caps')
                st.markdown(f"<p style='font-size:20px;'>{purplecap}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('5 Wicket Hauls')
                st.markdown(f"<p style='font-size:20px;'>{wickets5}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
                st.subheader('Economy')
                st.markdown(f"<p style='font-size:20px;'>{economy}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Performance Throughout The Career</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(seasonbowl)
    
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Performance Against Different Opponents</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(performopp)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Performance in Different Stadiums</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.table(performvenue)
    
            bowlerdf, economydf, heatmapdf, wicketdf,piewickets, pieoutcome = helper.player_bowling_viz1(deliveries,players, selected_player, battingcard)
    
            fig = make_subplots(rows=2, cols=2,
                                subplot_titles=['Performance against Bowling Styles', 'Economy in Different Overs of the Match',
                                                'Performance in Different Situations of the Match',
                                                'Relationship Between Wickets Taken and Over of the Match'])
    
            trace1 = go.Bar(x=bowlerdf['batting_style'], y=bowlerdf['wickets'], name='Wickets', marker=dict(color='blue'))
            trace2 = go.Bar(x=bowlerdf['batting_style'], y=bowlerdf['economy'], name='Economy', marker=dict(color='green'))
            fig.add_trace(trace1, row=1, col=1)
            fig.add_trace(trace2, row=1, col=1)
            fig.update_xaxes(title_text='Batting Style', row=1, col=1)
            fig.update_yaxes(title_text='Wickets / Economy', row=1, col=1)
    
            trace3 = go.Scatter(x=economydf['over_number'], y=economydf['economy'], mode='lines+markers', name='Economy',
                                line=dict(color='red'))
            fig.add_trace(trace3, row=1, col=2)
            fig.update_xaxes(title_text='Over Number', row=1, col=2)
            fig.update_yaxes(title_text='Economy', row=1, col=2)

            trace5 = go.Heatmap(z=heatmapdf.values, x=heatmapdf.columns, y=heatmapdf.index, colorscale='Viridis',
                                texttemplate="%{z}", hoverinfo='text')
            fig.add_trace(trace5, row=2, col=1)
            fig.update_xaxes(title_text='Ball Outcome', row=2, col=1)
            fig.update_yaxes(title_text='Over Situation', row=2, col=1)
    
            trace6 = go.Scatter(x=wicketdf['over_number'], y=wicketdf['wickets'], mode='markers',
                                marker=dict(size=wicketdf['wickets']*1.5, color='blue'), name='Wickets')
    
            fig.add_trace(trace6, row=2, col=2)
            fig.update_xaxes(title_text='Over Number', row=2, col=2)
            fig.update_yaxes(title_text='Wickets', row=2, col=2)
    
            fig.update_layout(height=1000, width=1500, title_text=' ')
    
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>Bowling Analysis of {selected_player}</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.plotly_chart(fig)

            fig = make_subplots(rows=1, cols=2, subplot_titles=["Distribution of Types of Wickets",
                                                                "Distribution of Delivery Outcomes"],
                                specs=[[{"type": "pie"}, {"type": "pie"}]])
    
            trace4 = go.Pie(values=piewickets['isout'], labels=piewickets['wickettype'])
            fig.add_trace(trace4, row=1, col=1)
            trace7 = go.Pie(values=pieoutcome['batsman_runs'], labels=pieoutcome['ball_outcome'])
            fig.add_trace(trace7, row=1, col=2)
            fig.update_layout(title="", height=500, width=1500)
            st.plotly_chart(fig)
    
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>{selected_player}'s Favourite Batsmen to Bowl to</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            selected_sort = st.selectbox('Sort Batsmen By', ['wickets', 'batsman runs', 'economy', 'average', 'strike rate'])
            favbatsman, favbat3 = helper.favbatsman(deliveries, players, selected_player, selected_sort)
            st.markdown("<br>", unsafe_allow_html=True)
    
            col1, col2, col3 = st.columns(3)
    
            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{favbat3['batsman name'][1]}")
                st.image(f"{favbat3['image_url'][1]}", width=150)
    
            with col2:
                st.subheader(f"{favbat3['batsman name'][0]}")
                st.image(f"{favbat3['image_url'][0]}", width=150)
    
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{favbat3['batsman name'][2]}")
                st.image(f"{favbat3['image_url'][2]}", width=150)
    
            st.table(favbatsman)
            st.write('Atleast 4 overs bowled*')
    
            st.markdown("<br>", unsafe_allow_html=True)
            centered_text = f"<h2 style='text-align: center;'>{selected_player}'s Least Favourite Batsmen to Bowl to</h2>"
            st.markdown(centered_text, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            sort_by3 = st.selectbox('Sort Batsmen By', ['wickets', 'economy', 'average', 'strike rate'])
            worstbatsman, worstbat3 = helper.worstbatsman(deliveries, players, selected_player, sort_by3)
            st.markdown("<br>", unsafe_allow_html=True)
    
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{worstbat3['batsman name'][1]}")
                st.image(f"{worstbat3['image_url'][1]}", width=150)
    
            with col2:
                st.subheader(f"{worstbat3['batsman name'][0]}")
                st.image(f"{worstbat3['image_url'][0]}", width=150)
    
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader(f"{worstbat3['batsman name'][2]}")
                st.image(f"{worstbat3['image_url'][2]}", width=150)
    
            st.table(worstbatsman)
            st.write('Atleast 4 overs bowled*')
        except KeyError:
            st.write("Not enough Data to show Bowling Statistics and Visualizations.")

if user_menu == 'IPL Records':
    selected_option = st.sidebar.selectbox('Select an Option', ['Batting', 'Bowling'])
    if selected_option == 'Batting':
        mostruns, top3runs, highscore, top3highscore, bestavg, top3avg, beststriker, top3striker = helper.ipl_records_batting1(battingcard,players)
        most100, top3centuries, most50, top350, mostfours, top3fours, mostsixes, top3sixes = helper.ipl_records_batting2(battingcard, players)

        st.markdown("<br>", unsafe_allow_html=True)
        centered_text = f"<h1 style='text-align: center;'>IPL Batting Records</h1>"
        st.markdown(centered_text, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Runs in IPL History')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3runs['player_name'][1]}")
            st.image(f"{top3runs['image_url'][1]}", caption=f"2. {top3runs['runs'][1]} runs",width=150)

        with col2:
            st.subheader(f"{top3runs['player_name'][0]}")
            st.image(f"{top3runs['image_url'][0]}", caption=f"1. {top3runs['runs'][0]} runs", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3runs['player_name'][2]}")
            st.image(f"{top3runs['image_url'][2]}",caption=f"3. {top3runs['runs'][2]} runs", width=150)

        st.table(mostruns)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Highest Score in an Innings')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3highscore['player_name'][1]}")
            st.image(f"{top3highscore['image_url'][1]}", caption=f"2. {top3highscore['runs'][1]} runs", width=150)

        with col2:
            st.subheader(f"{top3highscore['player_name'][0]}")
            st.image(f"{top3highscore['image_url'][0]}", caption=f"1. {top3highscore['runs'][0]} runs", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3highscore['player_name'][2]}")
            st.image(f"{top3highscore['image_url'][2]}", caption=f"3. {top3highscore['runs'][2]} runs", width=150)

        st.table(highscore)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Overall Average')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3avg['player_name'][1]}")
            st.image(f"{top3avg['image_url'][1]}", caption=f"2. {top3avg['average'][1]}", width=150)

        with col2:
            st.subheader(f"{top3avg['player_name'][0]}")
            st.image(f"{top3avg['image_url'][0]}", caption=f"1. {top3avg['average'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3avg['player_name'][2]}")
            st.image(f"{top3avg['image_url'][2]}", caption=f"3. {top3avg['average'][2]}", width=150)

        st.table(bestavg)
        st.write("Minimum 1000 runs scored*")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Overall Strike Rate')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3striker['player_name'][1]}")
            st.image(f"{top3striker['image_url'][1]}", caption=f"2. {top3striker['strike rate'][1]}", width=150)

        with col2:
            st.subheader(f"{top3striker['player_name'][0]}")
            st.image(f"{top3striker['image_url'][0]}", caption=f"1. {top3striker['strike rate'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3striker['player_name'][2]}")
            st.image(f"{top3striker['image_url'][2]}", caption=f"3. {top3striker['strike rate'][2]}", width=150)

        st.table(beststriker)
        st.write("Minimum 1000 runs scored*")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Hundreds')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3centuries['player_name'][1]}")
            st.image(f"{top3centuries['image_url'][1]}", caption=f"2. {top3centuries['hundreds'][1]} 100s", width=150)

        with col2:
            st.subheader(f"{top3centuries['player_name'][0]}")
            st.image(f"{top3centuries['image_url'][0]}", caption=f"1. {top3centuries['hundreds'][0]} 100s", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3centuries['player_name'][2]}")
            st.image(f"{top3centuries['image_url'][2]}", caption=f"3. {top3centuries['hundreds'][2]} 100s", width=150)

        st.table(most100)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Fifties')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top350['player_name'][1]}")
            st.image(f"{top350['image_url'][1]}", caption=f"2. {top350['fifties'][1]} 50s", width=150)

        with col2:
            st.subheader(f"{top350['player_name'][0]}")
            st.image(f"{top350['image_url'][0]}", caption=f"1. {top350['fifties'][0]} 50s", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top350['player_name'][2]}")
            st.image(f"{top350['image_url'][2]}", caption=f"3. {top350['fifties'][2]} 50s", width=150)

        st.table(most50)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Fours')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3fours['player_name'][1]}")
            st.image(f"{top3fours['image_url'][1]}", caption=f"2. {top3fours['fours'][1]} fours", width=150)

        with col2:
            st.subheader(f"{top3fours['player_name'][0]}")
            st.image(f"{top3fours['image_url'][0]}", caption=f"1. {top3fours['fours'][0]} fours", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3fours['player_name'][2]}")
            st.image(f"{top3fours['image_url'][2]}", caption=f"3. {top3fours['fours'][2]} fours", width=150)

        st.table(mostfours)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Sixes')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3sixes['player_name'][1]}")
            st.image(f"{top3sixes['image_url'][1]}", caption=f"2. {top3sixes['sixes'][1]} sixes", width=150)

        with col2:
            st.subheader(f"{top3sixes['player_name'][0]}")
            st.image(f"{top3sixes['image_url'][0]}", caption=f"1. {top3sixes['sixes'][0]} sixes", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3sixes['player_name'][2]}")
            st.image(f"{top3sixes['image_url'][2]}", caption=f"3. {top3sixes['sixes'][2]} sixes", width=150)

        st.table(mostsixes)

    if selected_option == 'Bowling':
        mostwickets, top3wickets, most3wickets, top3fers, bestbowlfig, top3bowlfig, bestbowleco, top3economy, bestbowlavg, top3bowlavg, bestbowlstriker, top3striker = helper.ipl_bowling_record(bowlingcard, players)

        st.markdown("<br>", unsafe_allow_html=True)
        centered_text = f"<h1 style='text-align: center;'>IPL Bowling Records</h1>"
        st.markdown(centered_text, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most Wickets in IPL History')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3wickets['player_name'][1]}")
            st.image(f"{top3wickets['image_url'][1]}", caption=f"2. {top3wickets['wickets'][1]} wickets", width=150)

        with col2:
            st.subheader(f"{top3wickets['player_name'][0]}")
            st.image(f"{top3wickets['image_url'][0]}", caption=f"1. {top3wickets['wickets'][0]} wickets", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3wickets['player_name'][2]}")
            st.image(f"{top3wickets['image_url'][2]}", caption=f"3. {top3wickets['wickets'][2]} wickets", width=150)

        st.table(mostwickets)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Most 3 Wicket Hauls in IPL History')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3fers['player_name'][1]}")
            st.image(f"{top3fers['image_url'][1]}", caption=f"2. {top3fers['3 wicket hauls'][1]} 3fers", width=150)

        with col2:
            st.subheader(f"{top3wickets['player_name'][0]}")
            st.image(f"{top3wickets['image_url'][0]}", caption=f"1. {top3fers['3 wicket hauls'][0]} 3fers", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3fers['player_name'][2]}")
            st.image(f"{top3fers['image_url'][2]}", caption=f"3. {top3fers['3 wicket hauls'][2]} 3fers", width=150)

        st.table(most3wickets)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Bowling Figures in an Innings')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3bowlfig['player_name'][1]}")
            st.image(f"{top3bowlfig['image_url'][1]}", caption=f"2. {top3bowlfig['wickets'][1]}/{top3bowlfig['conceded'][1]}", width=150)

        with col2:
            st.subheader(f"{top3bowlfig['player_name'][0]}")
            st.image(f"{top3bowlfig['image_url'][0]}", caption=f"1. {top3bowlfig['wickets'][0]}/{top3bowlfig['conceded'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3bowlfig['player_name'][2]}")
            st.image(f"{top3bowlfig['image_url'][2]}", caption=f"3. {top3bowlfig['wickets'][2]}/{top3bowlfig['conceded'][2]}", width=150)

        st.table(bestbowlfig)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Overall Bowling Average')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3bowlavg['player_name'][1]}")
            st.image(f"{top3bowlavg['image_url'][1]}",
                     caption=f"2. {top3bowlavg['average'][1]}", width=150)

        with col2:
            st.subheader(f"{top3bowlavg['player_name'][0]}")
            st.image(f"{top3bowlavg['image_url'][0]}",
                     caption=f"1. {top3bowlavg['average'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3bowlavg['player_name'][2]}")
            st.image(f"{top3bowlavg['image_url'][2]}",
                     caption=f"3. {top3bowlavg['average'][2]}", width=150)

        st.table(bestbowlavg)
        st.write('Minimum 50 wickets taken*')
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Overall Bowling Economy')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3economy['player_name'][1]}")
            st.image(f"{top3economy['image_url'][1]}",
                     caption=f"2. {top3economy['economy'][1]}", width=150)

        with col2:
            st.subheader(f"{top3economy['player_name'][0]}")
            st.image(f"{top3economy['image_url'][0]}",
                     caption=f"1. {top3economy['economy'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3economy['player_name'][2]}")
            st.image(f"{top3economy['image_url'][2]}",
                     caption=f"3. {top3economy['economy'][2]}", width=150)

        st.table(bestbowleco)
        st.write('Minimum 100 overs bowled*')
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader('Best Overall Bowling Strike Rate')
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3striker['player_name'][1]}")
            st.image(f"{top3striker['image_url'][1]}",
                     caption=f"2. {top3striker['strike rate'][1]}", width=150)

        with col2:
            st.subheader(f"{top3striker['player_name'][0]}")
            st.image(f"{top3striker['image_url'][0]}",
                     caption=f"1. {top3striker['strike rate'][0]}", width=150)

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader(f"{top3striker['player_name'][2]}")
            st.image(f"{top3striker['image_url'][2]}",
                     caption=f"3. {top3striker['strike rate'][2]}", width=150)

        st.table(bestbowlstriker)
        st.write('Minimum 100 overs bowled*')
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

if user_menu == '2024 Predictions':
    selected_option = st.sidebar.selectbox('Select Prediction Type', ['1st Innings: Projected Score', '2nd Innings: Win Probability'])
    teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Punjab Kings', 'Chennai Super Kings',
             'Rajasthan Royals','Delhi Capitals', 'Lucknow Super Giants', 'Gujarat Titans']

    cities = ['Bengaluru', 'Chandigarh', 'Kolkata', 'Mumbai', 'Jaipur', 'Chennai', 'Hyderabad', 'Navi Mumbai', 'Cape Town', 'Gqeberha',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley', 'Cuttack', 'Ahmedabad', 'Nagpur', 'Dharamsala', 'Visakhapatnam',
       'Ranchi', 'Delhi', 'Abu Dhabi', 'Dubai', 'Sharjah', 'Pune', 'Indore', 'Guwahati', 'Lucknow']

    

    if selected_option == '1st Innings: Projected Score':
        st.markdown("<h1 style='text-align: center;'>1st Innings Score Predictor</h1>",
                    unsafe_allow_html=True)
        st.write(
            "Welcome to our First Innings Score Estimator! This tool predicts the likely score a cricket team will achieve in their first innings. It considers essential factors like team composition, match location, and ongoing match dynamics such as runs scored and wickets taken. Designed for both cricket enthusiasts and strategic thinkers, our Estimator offers reliable insights to enhance your understanding of expected first innings performance. Enjoy the game with informed anticipation, courtesy of our user-friendly prediction model.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            batting_team = st.selectbox('Select Batting Team', sorted(teams))

        with col2:
            eligible_teams = sorted(set(teams) - {batting_team})
            bowling_team = st.selectbox('Select Bowling Team', sorted(eligible_teams))

        city = st.selectbox('Select Match Venue', sorted(cities))

        col3, col4, col5 = st.columns(3)

        with col3:
            current_score = st.number_input('Current Score', min_value=0, max_value=1000, step=1)

        with col4:
            overs_done = st.number_input('Overs Played (Works for over > 5)', min_value=0, max_value=20, value=5, step=1)

        with col5:
            wickets = st.number_input('Wickets', min_value=0, max_value=10, step=1)

        last_five = st.number_input('Runs Scored in Last Five Overs', min_value=0, max_value=180, step=1)

        deliveries_df = results[['match_id', 'team1_name', 'team2_name', 'match_venue_city']].merge(
            deliveries[deliveries['innings_no'] == 1], on='match_id').rename(
            columns={'team1_name': 'batting_team', 'team2_name': 'bowling_team'})
        deliveries_df['balls_left'] = 126 - (deliveries_df['over_number'] * 6 + deliveries_df['ball_number'])
        deliveries_df['crr'] = (deliveries_df['current_innings_runs'] * 6) / (120 - deliveries_df['balls_left'])
        deliveries_df['wickets_left'] = 10 - deliveries_df['current_innings_wickets']
        deliveries_df['last_five'] = deliveries_df.groupby('match_id')['total_runs'].rolling(window=30).sum().values
        deliveries_df['balls_left'] = deliveries_df['balls_left'].apply(lambda x: x if x >= 0 else 0)
        deliveries_df = deliveries_df.merge(
            deliveries_df.groupby('match_id')['current_innings_runs'].max().reset_index().rename(
                columns={'current_innings_runs': 'total_innings_runs'}), on='match_id')
        final_bat = deliveries_df[
            ['batting_team', 'bowling_team', 'match_venue_city', 'current_innings_runs', 'wickets_left', 'crr',
             'balls_left', 'last_five', 'total_innings_runs']]
        final_bat = final_bat.dropna()
        final_bat = final_bat.sample(final_bat.shape[0])
        X = final_bat.drop(columns='total_innings_runs')
        y = final_bat['total_innings_runs']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        trf = ColumnTransformer([
            ('trf', OneHotEncoder(drop='first'), ['batting_team', 'bowling_team', 'match_venue_city'])
        ]
            , remainder='passthrough')
        
        # pipe = Pipeline(steps=[
        #     ('step1', trf),
        #     ('step2', StandardScaler(with_mean=False)),
        #     ('step3', LinearRegression())
        # ])
        
        pipe = Pipeline(steps=[
            ('step1', trf),
            ('step2', StandardScaler(with_mean=False)),
            ('step3', LGBMRegressor(n_estimators=1000, learning_rate=0.2, max_depth=12, random_state=1))
        ])
        
        pipe.fit(X_train, y_train)
        
        if st.button('Predict Projected Score'):
            wickets_left = 10 - wickets
            crr = current_score/overs_done
            balls_left = 120 - (overs_done*6)

            input_df = pd.DataFrame(
                {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'match_venue_city': [city],
                 'current_innings_runs': [current_score], 'balls_left': [balls_left], 'wickets_left': [wickets_left], 'crr': [crr],
                 'last_five': [last_five]})

            result = pipe.predict(input_df)
            st.header("Predicted Score - " + str(int(result[0])))
        
        
    if selected_option == '2nd Innings: Win Probability':
        st.markdown("<h1 style='text-align: center;'>Win Probability Predictor in 2nd Innings</h1>",
                    unsafe_allow_html=True)
        st.write(
            "Explore our 2nd Innings Win Probability Predictor! This model forecasts the win probability for both the batting and bowling teams in a cricket match's second innings. Considered factors include team dynamics, match venue, target score, and real-time match situations like the current run rate, required run rate, and remaining wickets. Tailored for cricket enthusiasts and strategic analysts, our Predictor offers precise win probability insights, empowering you to anticipate the outcome with informed confidence.")
        
        total_score_df = deliveries.groupby(['match_id', 'innings_no'])['total_runs'].sum().reset_index()
        total_score_df = total_score_df[total_score_df['innings_no'] == 1]
        match_df = results.merge(total_score_df[['match_id', 'total_runs']], on='match_id')
        match_df['team1_name'] = match_df['team1_name'].str.replace('Delhi Daredevils', 'Delhi Capitals')
        match_df['team2_name'] = match_df['team2_name'].str.replace('Delhi Daredevils', 'Delhi Capitals')

        match_df['team1_name'] = match_df['team1_name'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
        match_df['team2_name'] = match_df['team2_name'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

        match_df = match_df[match_df['team1_name'].isin(teams)]
        match_df = match_df[match_df['team2_name'].isin(teams)]
        match_df = match_df[['match_id', 'match_venue_city', 'match_winner', 'total_runs']]
        match_df['match_winner'] = match_df['match_winner'].apply(lambda x: helper.fullname(x))
        delivery_df = match_df.merge(deliveries, on='match_id')
        delivery_df = delivery_df[delivery_df['innings_no'] == 2]
        delivery_df['runs_left'] = delivery_df['total_runs_x'] - delivery_df['current_innings_runs']
        delivery_df['balls_left'] = 126 - (delivery_df['over_number'] * 6 + delivery_df['ball_number'])
        delivery_df['wickets_left'] = 10 - delivery_df['current_innings_wickets']
        delivery_df['crr'] = (delivery_df['current_innings_runs'] * 6) / (120 - delivery_df['balls_left'])
        delivery_df['rrr'] = (delivery_df['runs_left'] * 6) / (delivery_df['balls_left'])
        delivery_df = delivery_df.merge(results[['match_id', 'team1_name', 'team2_name']], on='match_id').rename(
            columns={'team2_name': 'batting_team', 'team1_name': 'bowling_team'})

        def results(row):
            return 1 if row['batting_team'] == row['match_winner'] else 0
        
        delivery_df['result'] = delivery_df.apply(results, axis=1)
        final_df = delivery_df[
            ['batting_team', 'bowling_team', 'match_venue_city', 'runs_left', 'balls_left', 'wickets_left',
             'total_runs_x', 'crr', 'rrr', 'result']]
        final_df.dropna(inplace=True)
        final_df = final_df[final_df['balls_left'] != 0]
        final_df = final_df.sample(final_df.shape[0])
        X = final_df.iloc[:, :-1]
        y = final_df.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        trf = ColumnTransformer([
            ('trf', OneHotEncoder(drop='first'), ['batting_team', 'bowling_team', 'match_venue_city'])
        ]
            , remainder='passthrough')
        pipe = Pipeline(steps=[
            ('step1', trf),
            ('step2', LogisticRegression(solver='liblinear'))
        ])
        pipe.fit(X_train, y_train)

        col1, col2 = st.columns(2)
        
        with col1:
            batting_team = st.selectbox('Select the Batting Team', sorted(teams))
        with col2:
            eligible_teams = sorted(set(teams) - {batting_team})
            bowling_team = st.selectbox('Select the Bowling Team', sorted(eligible_teams))

        selected_city = st.selectbox("Select Match Venue City", sorted(cities))
        target = st.number_input('Target', min_value=0, max_value=1000, step=1)

        col3, col4, col5 = st.columns(3)

        with col3:
            score = st.number_input('Current Score', min_value=0, max_value=1000, step=1)
        with col4:
            overs = st.number_input('Overs Completed', min_value=0, max_value=20, step=1)
        with col5:
            wickets = st.number_input('Wickets', min_value=0, max_value=10, step=1)

        if st.button('Predict Probability'):
            runs_left = target - score
            balls_left = 120 - (overs * 6)
            wickets_left = 10 - wickets
            crr = score / overs
            rrr = (runs_left * 6) / balls_left

            input_df = pd.DataFrame(
                {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'match_venue_city': [selected_city],
                 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                 'total_runs_x': [target],
                 'crr': [crr], 'rrr': [rrr]})

            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]
            st.header(batting_team + "- " + str(round(win * 100)) + "%")
            st.header(bowling_team + "- " + str(round(loss * 100)) + "%")
            
    




