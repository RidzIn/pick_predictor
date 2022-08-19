from mapping_fuctions import *
import pandas as pd


# Takes Data Frame and return grouped by team Series in case of winning the game
# BOOM Esports    39:34
# BetBoom Team    40:36
def average_time_if_win_ser(main_df):
    aver_time = main_df[main_df['RESULT'] == 'WIN'].groupby('TEAM')['DURATION IN SEC'].mean()
    return aver_time.map(duration_in_sec_to_duration_in_minutes)


# Takes Data Frame and return grouped by team Series no matter winning or losing
# BOOM Esports    38:37
# BetBoom Team    39:42
def average_time_no_matter_result_ser(main_df):
    aver_time = main_df.groupby('TEAM')['DURATION IN SEC'].mean()
    return aver_time.map(duration_in_sec_to_duration_in_minutes)


# Takes Data Frame and return grouped by team Series in case of losing the game
# BOOM Esports     38:6
# BetBoom Team    38:42
def average_time_if_lose_ser(main_df):
    aver_time = main_df[main_df['RESULT'] == 'LOSE'].groupby('TEAM')['DURATION IN SEC'].mean()
    return aver_time.map(duration_in_sec_to_duration_in_minutes)


# Takes Data Frame and return grouped by team Series with their fastest game
# BOOM Esports    28:47
# BetBoom Team    26:16
def fastest_game_ser(main_df):
    fast_game = main_df.groupby('TEAM')['DURATION IN SEC'].min()
    return fast_game.map(duration_in_sec_to_duration_in_minutes)


# Takes Data Frame and return grouped by team Series with their longest game
# BOOM Esports    52:12
# BetBoom Team    58:47
def longest_game_ser(main_df):
    long_game = main_df.groupby('TEAM')['DURATION IN SEC'].max()
    return long_game.map(duration_in_sec_to_duration_in_minutes)


# Takes Data Frame and return grouped by key('TEAM','HERO') Series in case of winning
# By ------By HERO--------
# Abaddon                6
# Alchemist              2
# ---------By TEAM--------
# BOOM Esports           5
# BetBoom Team          11
def matches_won_ser(main_df, key):
    return main_df[main_df['RESULT'] == 'WIN'].groupby(key)['RESULT'].count()


# Takes Data Frame and return grouped by key('TEAM','HERO') Series in case of losing
# By ------By HERO--------
# Abaddon                2
# Alchemist              1
# ---------By TEAM--------
# BOOM Esports           3
# BetBoom Team           5
def matches_lose_ser(main_df, key):
    return main_df[main_df['RESULT'] == 'LOSE'].groupby(key)['RESULT'].count()


# Takes Data Frame and return grouped by key('TEAM','HERO') Series no matter win or lose
# By ------By HERO--------
# Abaddon                8
# Alchemist              3
# ---------By TEAM--------
# BOOM Esports           8
# BetBoom Team          16
def matches_count_ser(main_df, key):
    return main_df.groupby(key)['RESULT'].count()


# Takes 2 Series('matches_count_ser', 'matches_won_ser') and return
# By ------By HERO------------
# Abaddon                46.0%
# Alchemist             100.0%
# ---------By TEAM------------
# BOOM Esports           36.0%
# BetBoom Team           52.0%
def matches_win_rate_ser(matches_won, matches_count):
    win_rate = matches_won / matches_count
    return win_rate.map(winrate_format)


# Takes Data Frame and return grouped by team Series with average kills per match(both teams)
# BetBoom Team         49
# BOOM Esports         50
def match_average_kills_ser(main_df):
    list_of_teams = main_df['TEAM'].unique()
    team_match_id_dict = {}
    for i in list_of_teams:
        team_match_id_dict.setdefault(i, [])
    for k, v in team_match_id_dict.items():
        v = main_df.loc[main_df['TEAM'] == k]['MATCH_ID'].to_list()
        team_match_id_dict[k] = list(set(v))
    avg_ser = main_df.groupby(['MATCH_ID'])['SCORE'].sum().to_dict()

    maps_count_dict = main_df.groupby(['MATCH_ID'])['MAP'].count().to_dict()
    for k, v in team_match_id_dict.items():
        for i in range(len(v)):
            v[i] = avg_ser[v[i]] // (maps_count_dict[v[i]] // 2)
    for k, v in team_match_id_dict.items():
        kills_sum = 0
        for i in v:
            kills_sum += i
        team_match_id_dict[k] = int(kills_sum / len(v))

    result_ser = pd.Series(data=team_match_id_dict)
    return result_ser


# Takes Data Frame and return group by match_id and team Series and sort values by keys
# # ['AVG'] - to get average kills(individual not total kills for match)
# # ['MAX'] - to get biggest amount of kills(individual not total kills for match)
# # ['MIN'] - to get lowest amount of kills(individual not total kills for match)
def kills_ser_by_key(main_df, key):
    if key == 'AVG':
        return main_df.groupby(['MATCH_ID', 'TEAM'])['SCORE'].mean()
    if key == 'MAX':
        return main_df.groupby(['MATCH_ID', 'TEAM'])['SCORE'].max()
    if key == 'MIN':
        return main_df.groupby(['MATCH_ID', 'TEAM'])['SCORE'].min()
