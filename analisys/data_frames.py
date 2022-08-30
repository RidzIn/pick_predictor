from analisys.helping_functions import *
from analisys.series import *


#   TEAM	          MATCHES	WINS    LOSES	WINRATE
# 0	BOOM Esports	  14	    5	    9	    36.0%
# 1	BetBoom Team	  21	    11	    10	    52.0%
# 2	Evil Geniuses	  12	    2	    10	    17.0%
# 3	Fnatic	          16	    7	    9	    44.0%
# 4	Gaimin Gladiators 18	    10	    8	    56.0%
def team_win_rate_df(main_df):
    # Creating 4 Series
    matches_won = matches_won_ser(main_df, 'TEAM')
    matches_lost = matches_lose_ser(main_df, 'TEAM')
    matches_count = matches_count_ser(main_df, 'TEAM')
    win_rate = matches_win_rate_ser(matches_won, matches_count)

    # Concatenating created Series to Data Frame and do a little refactor
    result_df = pd.concat([matches_count, matches_won, matches_lost, win_rate], axis=1).reset_index()
    result_df.columns = ['TEAM', 'MATCHES', 'WINS', 'LOSES', 'WINRATE']
    result_df = result_df.sort_values(by=['MATCHES', 'WINRATE'], ascending=False).reset_index(drop=True)
    return result_df


# 	TEAM	            AVG	MAX	MIN	AVG(MATCH)
# 0	BOOM Esports	    22	43	4	50
# 1	BetBoom Team	    27	42	10	49
# 2	Evil Geniuses	    19	33	8	48
# 3	Fnatic	            21	44	9	43
# 4	Gaimin Gladiators	23	43	5	46
def kills_team_info_df(main_df):
    # Creating 3 Series
    average_kills = kills_ser_by_key(main_df, key='AVG')
    max_kills = kills_ser_by_key(main_df, key='MAX')
    min_kills = kills_ser_by_key(main_df, key='MIN')

    # Create temp Data Frame(contains info about every match)
    #     MATCH_ID     TEAM            AVG    MAX   MIN
    # 0   1            BOOM Esports    20.0   36    4
    # 1   1            BetBoom Team    22.0   29    15
    # 2   2            BetBoom Team    26.0   42    10
    # 3   2            Tundra Esports  21.5   25    18
    result_df = pd.concat([average_kills, max_kills, min_kills], axis=1).reset_index()
    result_df.columns = ['MATCH_ID', 'TEAM', 'AVG', 'MAX', 'MIN']

    # Creating 4 Series for out result Data Frame
    teams_avg_kills_ser = result_df.groupby('TEAM')['AVG'].mean()
    teams_avg_kills_ser = teams_avg_kills_ser.map(int)
    teams_max_kills_ser = result_df.groupby('TEAM')['MAX'].max()
    teams_min_kills_ser = result_df.groupby('TEAM')['MIN'].min()

    # Concatenating created Series to Data Frame and do a little refactor
    team_individual_kills_info = pd.concat([teams_avg_kills_ser, teams_max_kills_ser, teams_min_kills_ser,
                                            match_average_kills_ser(main_df)],
                                           axis=1).reset_index()
    team_individual_kills_info.columns = ['TEAM', 'AVG', 'MAX', 'MIN', 'AVG(MATCH)']
    team_individual_kills_info = team_individual_kills_info.sort_values(by=['AVG'], ascending=False) \
        .reset_index(drop=True)
    return team_individual_kills_info


#  TEAM	        FASTEST	AVG	    AVG(LOSE)	AVG(WIN)	LONGEST
# 0	BOOM Esports	28:47	38:37	38:6	    39:34	    52:12
# 1	BetBoom Team	26:16	39:42	38:42	    40:36	    58:47
# 2	Evil Geniuses	31:23	38:42	38:39	    38:59	    48:23
# 3	Fnatic	        22:18	40:51	42:37	    38:35	    64:6
# 4	OG	            21:35	35:14	37:40	    33:18	    48:48
def time_team_info_df(main_df):
    # Concatenating series to Data Frame and do a little refactor
    result_df = pd.concat([fastest_game_ser(main_df), average_time_no_matter_result_ser(main_df),
                           average_time_if_lose_ser(main_df), average_time_if_win_ser(main_df),
                           longest_game_ser(main_df)],
                          axis=1).reset_index()
    result_df.columns = ['TEAM', 'FASTEST', 'AVG', 'AVG(LOSE)', 'AVG(WIN)', 'LONGEST']
    result_df = result_df.sort_values(by=['AVG'], ascending=False).reset_index(drop=True)
    return result_df


#   HERO	      PICKS	 WINRATE
# 0	Mars	      58	 43.0%
# 1	Chaos Knight  48	 56.0%
# 2	Grimstroke	  45	 40.0%
# 3	Pugna	      43	 58.0%
# 4	Storm Spirit  35	 54.0%
def hero_picks_win_rate_df(main_df):
    # Create Data Frame
    #                 0 RESULT
    # 0       Pangolier   LOSE
    # 1     Bloodseeker    WIN
    # 2         Leshrac    WIN
    my_list = generate_heroes_with_results_list(main_df)
    hero_info = pd.concat([my_list[0], my_list[1]], axis=1).reset_index(drop=True)

    # Create 3 Series
    matches_won = matches_won_ser(hero_info, 0)
    matches = matches_count_ser(hero_info, 0)
    winning_rate = matches_win_rate_ser(matches_won, matches)
    winning_rate = winning_rate.fillna(value=0)

    # Concatenating created series to Data Frame and do a little refactor
    result_df = pd.concat([matches, winning_rate], axis=1).reset_index()
    result_df.columns = ['HERO', 'TOTAL', 'WINRATE']
    result_df = result_df[result_df['TOTAL'] > 1]
    result_df = result_df.sort_values(by=['TOTAL', 'WINRATE'], ascending=False).reset_index(drop=True)
    return result_df


#   PAIR                    TOTAL WIN LOSE  WINRATE
# 0 Grimstroke-Tiny         12    2   10    17.0%
# 1 Void Spirit-Grimstroke  11    6   5     55.0%
# 2 Chaos Knight-Grimstroke 11    4   7     36.0%
# 3 Mars-Io                 11    4   7     36.0%
# 4 Grimstroke-Mars         10    3   7     30.0%
def popular_pairs_df(main_df):
    # Initialize list of every possible combination
    list_of_all_combinations = []
    unique_heroes = unique_heroes_list(main_df)
    every_picks = every_pick_list(main_df)
    for i in range(len(unique_heroes)):
        for j in range(i + 1, len(unique_heroes)):
            list_of_all_combinations.append((unique_heroes[i], unique_heroes[j]))

    # Create and return 2 dicts of every possible combination with 0 as default values
    def set_defaults():
        win_dict_in, lose_dict_in = {}, {}
        for pick in list_of_all_combinations:
            win_dict_in.setdefault(pick, 0)
            lose_dict_in.setdefault(pick, 0)
        return [win_dict_in, lose_dict_in]

    win_dict, lose_dict = set_defaults()
    # Fill created dicts with values
    win_picks = get_picked_pairs_by_condition(win_dict, every_picks, 'WIN')
    lose_picks = get_picked_pairs_by_condition(lose_dict, every_picks, 'LOSE')

    # Sort these dicts to get only picked pairs at least 1 time
    win_picks = {k: v for k, v in sorted(win_picks.items(), key=lambda item: item[1], reverse=True) if v > 0}
    lose_picks = {k: v for k, v in sorted(lose_picks.items(), key=lambda item: item[1], reverse=True) if v > 0}

    # A lot of messy staff to get normal output Data Frame
    win_df = pd.Series(win_picks).reset_index()
    win_df.columns = ['HERO_1', 'HERO_2', 'WIN']
    win_df["PAIR"] = win_df['HERO_1'].astype(str) + "-" + win_df["HERO_2"]
    del win_df['HERO_1']
    del win_df['HERO_2']
    lose_df = pd.Series(lose_picks).reset_index()
    lose_df.columns = ['HERO_1', 'HERO_2', 'LOSE']
    lose_df["PAIR"] = lose_df['HERO_1'].astype(str) + "-" + lose_df["HERO_2"]
    del lose_df['HERO_1']
    del lose_df['HERO_2']
    result_df = pd.merge(win_df, lose_df, on="PAIR", how='outer')
    result_df = result_df.fillna(value=0)
    result_df['TOTAL'] = result_df['WIN'] + result_df['LOSE']
    result_df = result_df[['PAIR', 'TOTAL', 'WIN', 'LOSE']]
    result_df['WINRATE'] = matches_win_rate_ser(result_df['WIN'], result_df['TOTAL'])
    result_df['TOTAL'] = result_df['TOTAL'].map(int)
    result_df['WIN'] = result_df['WIN'].map(int)
    result_df['LOSE'] = result_df['LOSE'].map(int)
    result_df = result_df[result_df['TOTAL'] > 4]
    return result_df


# Takes result data frame from 'popular_pairs_df' or 'hero_picks_win_rate_df' and sort values by keys
# ['TOTAL', 'WINRATE'] - to get most frequent values
# ['WINRATE', 'LOWEST'] - to get lowest winrate pairs or heroes
# ['WINRATE', 'BIGGEST'] - to get biggest winrate pairs or heroes
def sort_data_frame_by_keys(result_df, keys):
    if keys[-1] == 'LOWEST':
        return result_df.sort_values(by=keys[:-1], ascending=True).reset_index(drop=True).head(10)
    if keys[-1] == 'BIGGEST':
        return result_df.sort_values(by=keys[:-1], ascending=False).reset_index(drop=True).head(10)
    if keys[-1] == 'WINRATE':
        return result_df.sort_values(by=keys, ascending=False).reset_index(drop=True)


#   HERO
# 0	Axe
# 1	Dawnbreaker
# 2	Marci
# 3	Pudge
def unpicked_heroes_df(main_df):
    # Get list of unpicked heroes
    unpicked_heroes = unpicked_heroes_list(main_df)
    # Do some refactoring to get Data Frame output
    indexes = [i for i in range(len(unpicked_heroes))]
    result_dict = dict(zip(indexes, unpicked_heroes))
    result_df = pd.Series(data=result_dict).to_frame()
    result_df.columns = ['HERO']
    return result_df


def get_overall_info(main_df, winner):
    return {'MAPS': len(main_df) // 2,
            'AVG Duration': duration_in_sec_to_duration_in_minutes(main_df['DURATION IN SEC'].mean()),
            'AVG Kills': int(main_df['SCORE'].mean() * 2),
            'Fastest Game': duration_in_sec_to_duration_in_minutes(main_df['DURATION IN SEC'].min()),
            'Longest Game': duration_in_sec_to_duration_in_minutes(main_df['DURATION IN SEC'].max()),
            'WINNER': winner,
            'Unpicked Heroes': unpicked_heroes_list(main_df)}
