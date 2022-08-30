# Function takes row data and takes only picks and results
from analisys.data_frames import *
from analisys.helping_functions import *
import functools

row_data = pd.read_csv('data/DOTA_DATA_MATCHES.csv')

row_data_doubled = pd.read_csv('data/DOTA_DATA_MATCHES_DOUBLED.csv')

print(row_data.head(20))


# Coping function of hero_picks_win_rate_df
def reformat_data_for_overall_winrate():
    return hero_picks_win_rate_df(row_data)


print(reformat_data_for_overall_winrate())


# Function to format the output
def add_spaces(my_len, for_what):
    if for_what == 'HERO':
        return ' ' * (20 - my_len)
    if for_what == 'TOTAL':
        return ' ' * (7 - my_len)
    if for_what == 'VS':
        return ' ' * (40 - my_len)


# Takes raw data, and pick to return overall winrate of heroes in given pick
# ===PICK 1
# Viper               81     53.0%
# Clockwerk           101    50.0%
# Winter Wyvern       141    50.0%
# Ember Spirit        132    48.0%
# Terrorblade         67     48.0%
def formatted_winrate_string(main_df, pick, pick_number):
    result_winrates_string = '===PICK ' + str(pick_number) + '\n'
    for hero in pick:
        temp_ser = main_df.loc[main_df['HERO'] == hero]
        result_list = temp_ser.values
        result_winrates_string += result_list[0][0] + add_spaces(len(result_list[0][0]), 'HERO') + \
                                  str(result_list[0][1]) + add_spaces(len(str(result_list[0][1])), 'TOTAL') + \
                                  result_list[0][2] + '\n'
    return result_winrates_string


# Takes raw data and merge hero pick of one team with second into one row
# Then returns 2d list with this structure
# [[TEAM_1_PICK-RESULT, TEAM_2_PICK-RESULT], [TEAM_1_PICK, TEAM_2_PICK-RESULT]]
def get_formatted_match_pick_list(data_file):
    temp_data = data_file.copy()
    temp_data['PICK'] = every_pick_list(temp_data)
    temp_df = temp_data['PICK'].to_frame()
    temp_df = temp_df.groupby(temp_df.index // 2).agg(' | '.join).reset_index()
    #    Temp DF has this structure
    # 1  Lycan-Ogre Magi-Bloodseeker-Zeus-Tiny-WIN | Tiny, Io, ...
    # 2  Spectre-Enigma-Dazzle-Razor-Tiny-WIN | Queen of Pain, ...
    my_list = temp_df['PICK'].to_list()
    for i in range(len(my_list)):
        my_list[i] = my_list[i].split(' | ')

    return my_list


# Takes hero and return list of every pick where this hero appeared
def get_list_with_matched_heroes(hero):
    match_pick = get_formatted_match_pick_list(row_data_doubled)
    list_with_matched_hero = []
    for i in range(len(match_pick)):
        if hero in match_pick[i][0] or hero in match_pick[i][1]:
            list_with_matched_hero.append(match_pick[i])
    return list_with_matched_hero


# In progress
def get_heroes_synergy(pick_1):
    pick_1_synergy = []
    for hero in pick_1:
        matched_list = get_list_with_matched_heroes(hero)
        pick_list = [] # List where hero append
        for pick in matched_list:
            if hero in pick[0]:
                pick_list.append(pick[0])
            elif hero in pick[1]:
                pick_list.append(pick[1])

        for hero_to_match in pick_1:
            count_of_pairs_picked = 0
            count_of_pairs_picked_win = 0
            for i in pick_list:
                # print(i)
                if hero_to_match in i:
                    count_of_pairs_picked += 1
                    if i[-3:] == 'WIN':
                        count_of_pairs_picked_win += 1
            if count_of_pairs_picked > 3:
                try:
                    pick_1_synergy.append(round(count_of_pairs_picked_win / count_of_pairs_picked, 2))
                except ZeroDivisionError:
                    pick_1_synergy.append(0)

    return round(functools.reduce(lambda a, b: a + b, pick_1_synergy) / len(pick_1_synergy), 2)


def get_synergy_odds(pick1, pick2):
    return [get_heroes_synergy(pick1), get_heroes_synergy(pick2)]


# Takes 2 picks and returns duel statistic in the end 2 pick_scores
# ===Terrorblade DUELS STAT===
# Terrorblade vs Marci                    6      66.67%
# Terrorblade vs Nature's Prophet         2      50.0%
# Terrorblade vs Enchantress              8      62.5%
# Terrorblade vs Night Stalker            5      60.0%
# Terrorblade vs Storm Spirit             2      0.0%
# [750, 385]
def get_duel_stats(pick_1, pick_2):
    pick1_score = 0
    pick2_score = 0
    result_outer_str = ''
    for hero in pick_1:
        result_inner_str = '===' + hero + ' DUELS STAT===\n'
        for hero_to_duel in pick_2:
            matched_list = get_list_with_matched_heroes(hero)
            enemy_list = []
            for i in matched_list:
                if hero in i[0]:
                    enemy_list.append(i[1])
                else:
                    enemy_list.append(i[0])
            is_win_count = 0
            total_count = 0
            for i in enemy_list:
                if hero_to_duel in i:
                    total_count += 1
                    if i[-4:] == 'LOSE':
                        is_win_count += 1
            try:
                winrate = str(round(is_win_count / total_count * 100, 2)) + '%'
            except ZeroDivisionError:
                winrate = '0%'
            vs = hero + ' vs ' + hero_to_duel
            result_inner_str += vs + add_spaces(len(vs), 'VS') + str(total_count) + add_spaces(len(str(total_count)),
                                                                                               'TOTAL') + winrate + '\n'
            if total_count > 2:
                pick1_score += float(winrate[:-1])
                pick2_score += 100 - float(winrate[:-1])
        result_outer_str += result_inner_str

    print(result_outer_str)
    pick_1_synergy, pick_2_synergy = get_synergy_odds(pick_1, pick_2)
    return [round(pick1_score * pick_1_synergy), round(pick2_score * pick_2_synergy)]


def get_prediction(pick_1, pick_2):
    result_string = '\t\t========= OVERALL WINRATES =======\n'
    hero_winrates_df = reformat_data_for_overall_winrate()

    result_string += formatted_winrate_string(hero_winrates_df, pick_1, 1)
    result_string += formatted_winrate_string(hero_winrates_df, pick_2, 2)

    print(result_string)
    print('\t\t========= DUEL WINRATES =======\n')
    pick_1_score, pick_2_score = get_duel_stats(pick_1, pick_2)
    pick_1_synergy, pick_2_synergy = get_synergy_odds(pick_1, pick_2)
    print(str(pick_1_synergy) + " : " + str(pick_2_synergy) + '\n')
    print('\t\t========= PICK SCORES =======\n')
    print(str(pick_1) + ' ' + str(pick_1_score ))
    print(str(pick_2) + ' ' + str(pick_2_score ))


# print(get_synergy_odds(['Razor', 'Elder Titan', 'Snapfire', 'Templar Assassin', 'Pangolier'],
#                    ['Chen', 'Lone Druid', 'Nyx assassin', 'Enigma', 'Storm Spirit']) )
#
# get_prediction(['Razor', 'Elder Titan', 'Snapfire', 'Templar Assassin', 'Pangolier'],
#                 ['Chen', 'Lone Druid', 'Nyx Assassin', 'Enigma', 'Storm Spirit'])


