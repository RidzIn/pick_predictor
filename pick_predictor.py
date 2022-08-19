import pandas as pd
# Function takes row data and takes only picks and results
from data_frames import *
from helping_functions import *

row_data = pd.read_csv('DOTA_DATA_MATCHES.csv')

print(row_data.head(20))


# Coping function of hero_picks_win_rate_df
def reformat_data_for_overall_winrate():
    return hero_picks_win_rate_df(row_data)


# Function to format the output
def add_spaces(my_len, for_what):
    if for_what == 'HERO':
        return ' ' * (20 - my_len)
    if for_what == 'TOTAL':
        return ' ' * (7 - my_len)
    if for_what == 'VS':
        return ' ' * (30 - my_len)


def formatted_winrate_string(main_df, pick, pick_number):
    result_winrates_string = '===PICK ' + str(pick_number) + '\n'
    for hero in pick:
        temp_ser = main_df.loc[main_df['HERO'] == hero]
        result_list = temp_ser.values
        result_winrates_string += result_list[0][0] + add_spaces(len(result_list[0][0]), 'HERO') + \
                                  str(result_list[0][1]) + add_spaces(len(str(result_list[0][1])), 'TOTAL') + \
                                  result_list[0][2] + '\n'
    return result_winrates_string


def get_formatted_match_pick_list():
    temp_data = row_data.copy()
    temp_data['PICK'] = every_pick_list(temp_data)
    temp_df = temp_data['PICK'].to_frame()
    temp_df = temp_df.groupby(temp_df.index // 2).agg(' | '.join).reset_index()
    my_list = temp_df['PICK'].to_list()
    for i in range(len(my_list)):
        my_list[i] = my_list[i].split(' | ')

    return my_list


def get_list_with_matched_heroes(hero):
    match_pick = get_formatted_match_pick_list()

    list_with_matched_hero = []
    for i in range(len(match_pick)):
        if hero in match_pick[i][0] or hero in match_pick[i][1]:
            list_with_matched_hero.append(match_pick[i])
    return list_with_matched_hero


def get_map_pick(ally_pick, list_enemy):
    pick1_score = 0
    pick2_score = 0
    result_outer_str = ''
    for hero in ally_pick:
        result_inner_str = '===' + hero + ' DUELS STAT===\n'
        for hero_to_duel in list_enemy:
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
    return [round(pick1_score), round(pick2_score)]


def get_prediction(pick_1, pick_2):
    result_string = '\t\t========= OVERALL WINRATES =======\n'
    hero_winrates_df = reformat_data_for_overall_winrate()

    result_string += formatted_winrate_string(hero_winrates_df, pick_1, 1)
    result_string += formatted_winrate_string(hero_winrates_df, pick_2, 2)

    print(result_string)
    print('\t\t========= DUEL WINRATES =======\n')
    pick_1_score, pick_2_score = get_map_pick(pick_1, pick_2)
    print('\t\t========= PICK SCORES =======\n')
    print(str(pick_1) + ' ' + str(pick_1_score))
    print(str(pick_2) + ' ' + str(pick_2_score))


# get_prediction(['Viper', 'Clockwerk', 'Winter Wyvern', 'Ember Spirit', 'Terrorblade'],
#              ['Marci', "Nature's Prophet", 'Enchantress', 'Night Stalker', 'Storm Spirit'])

# get_prediction(['Tiny', 'Abaddon', 'Keeper of the Light', 'Tidehunter', 'Morphling'],
#               ['Marci', 'Batrider', 'Enchantress', 'Timbersaw', 'Beastmaster'])

# get_prediction(['Dazzle', 'Puck', 'Clockwerk', 'Batrider', 'Pudge'],
#               ['Tiny', "Night Stalker", "Winter Wyvern", 'Bane', 'Lycan'])

# get_prediction(['Bristleback', 'Winter Wyvern', 'Skywrath Mage', 'Kunkka', 'Venomancer'],
#             ['Chen', 'Puck', 'Nyx Assassin', 'Batrider', 'Templar Assassin'])

# get_prediction(['Zeus', 'Dazzle', "Faceless Void", 'Snapfire', 'Underlord'],
#               ['Tiny', 'Brewmaster', 'Enchantress', 'Wraith King', 'Death Prophet'])

# get_prediction(['Dawnbreaker', 'Zeus', 'Elder Titan', 'Shadow Shaman', 'Weaver'],
#               ['Winter Wyvern', 'Marci', 'Io', 'Bristleback', 'Dragon Knight'])

# get_prediction(['Death Prophet', 'Tiny', 'Dazzle', 'Kunkka', 'Terrorblade'],
#              ['Io', 'Bristleback', 'Void Spirit', 'Weaver', 'Dawnbreaker'])

# get_prediction(['Dawnbreaker', 'Dragon Knight','Skywrath Mage', 'Brewmaster', 'Weaver'],
#              ['Puck', 'Nyx Assassin','Crystal Maiden', 'Batrider', 'Pudge'])

# get_prediction(['Zeus', 'Dawnbreaker', 'Viper', 'Clockwerk','Wraith King'],
#               ['Dazzle', 'Alchemist', 'Tusk', 'Keeper of the Light', 'Enigma'])

# get_prediction(['Winter Wyvern', 'Alchemist', 'Night Stalker', 'Windranger', 'Ogre Magi'],
#              ['Puck', 'Dazzle', 'Phoenix', 'Bristleback', 'Mars'])

# get_prediction(['Puck', 'Tiny', 'Ancient Apparition', 'Juggernaut', 'Beastmaster'],
#             ['Dazzle', 'Alchemist', 'Dragon Knight', 'Skywrath Mage', 'Wraith King'])

#get_prediction(['Marci', 'Night Stalker','Faceless Void','Skywrath Mage', 'Lina'],
#             ['Chen', 'Queen of Pain', 'Jakiro', 'Wraith King', 'Slardar'])

#get_prediction(['Tiny', 'Skywrath Mage', 'Winter Wyvern', 'Juggernaut', 'Doom'],
#             ['Puck', 'Lycan', 'Snapfire', 'Jakiro', 'Terrorblade'])

# get_prediction(['Marci', 'Timbersaw', 'Dragon Knight', 'Snapfire', 'Gyrocopter'],
#               ['Chen', 'Puck', 'Bloodseeker', 'Batrider', 'Earthshaker'])

# get_prediction(['Razor', 'Puck', 'Clockwerk', 'Viper', 'Ursa'],
#               ['Timbersaw', 'Enchantress', 'Skywrath Mage', 'Ember Spirit', 'Juggernaut'])

# get_prediction(['Chen', 'Mars', 'Winter Wyvern', 'Templar Assassin', 'Storm Spirit'],
#               ['Tiny', 'Timbersaw', 'Dazzle', 'Keeper of the Light', 'Luna'])

# get_prediction(['Tusk', 'Death Prophet', 'Winter Wyvern', 'Kunkka', 'Alchemist'],
#               ['Earth Spirit', 'Puck', 'Snapfire', 'Viper', 'Medusa'])

# get_prediction(['Marci', 'Puck', 'Dazzle', 'Lifestealer', 'Keeper of the Light'],
#               ['Tiny','Viper', 'Night Stalker', 'Death Prophet', 'Phantom Assassin'])


#get_prediction(['Wraith King', 'Puck', 'Brewmaster', 'Nyx Assassin', 'Dazzle'],
#              ['Dragon Knight', 'Skywrath Mage', 'Dawnbreaker', 'Rubick', 'Ursa'])


#get_prediction(['Chen', 'Lina', 'Night Stalker', 'Rubick', 'Wraith King'],
#               ['Tiny', 'Winter Wyvern', 'Puck', 'Alchemist', 'Venomancer'])

#get_prediction(['Chen', 'Puck', 'Phoenix', 'Mars', 'Templar Assassin'],
#               ['Tiny', 'Winter Wyvern', 'Ursa', 'Snapfire', 'Doom'])


# get_prediction(['Dawnbreaker', 'Winter Wyvern','Night Stalker', 'Templar Assassin', 'Storm Spirit'],
#               ['Tiny', 'Puck','Phoenix', 'Mars', 'Terrorblade'])

# get_prediction(['Death Prophet', 'Tiny', 'Kunkka', 'Juggernaut', 'Dazzle'],
#                ['Puck', 'Phoenix', 'Marci', 'Shadow Demon', 'Faceless Void'])

# get_prediction(['Marci', 'Visage', 'Dazzle', 'Storm Spirit', 'Doom'],
#               ['Puck', 'Chen', 'Dawnbreaker', 'Templar Assassin', 'Razor'])

# get_prediction(['Marci', 'Storm Spirit', 'Visage', 'Jakiro', 'Alchemist'],
#               ['Viper', 'Dazzle', 'Doom', 'Ember Spirit', 'Ursa'])

# get_prediction(['Tiny', 'Razor', 'Ogre Magi', 'Kunkka', 'Visage'],
#               ['Dawnbreaker', 'Techies', 'Lina', 'Viper', 'Pangolier'])

# get_prediction(['Dawnbreaker', 'Weaver', 'Tusk', 'Jakiro', 'Death Prophet'],
#               ['Viper', 'Nyx Assassin', 'Dazzle', 'Bloodseeker', 'Windranger'])

# get_prediction(['Marci', 'Razor', 'Zeus', 'Dazzle', 'Juggernaut'],
#               ['Dawnbreaker', 'Crystal Maiden', 'Tiny', 'Void Spirit', 'Skywrath Mage'])

# get_prediction(['Monkey King', 'Dawnbreaker', 'Tiny', 'Rubick', 'Batrider'],
#               ['Clinkz', 'Enigma', 'Timbersaw', 'Winter Wyvern', 'Storm Spirit'])

# get_prediction(['Puck', 'Beastmaster', 'Snapfire', 'Dazzle', 'Chaos Knight'],
#               ['Alchemist', 'Skywrath Mage', 'Ogre Magi', 'Razor', 'Tidehunter'])

# get_prediction(['Dawnbreaker', 'Viper', 'Warlock', 'Naga Siren', 'Clockwerk'],
#               ['Tiny', 'Lycan', 'Nyx Assassin', 'Windranger', 'Sniper'])

# get_prediction(['Tiny', 'Winter Wyvern', 'Dawnbreaker', 'Razor', 'Treant Protector'],
#               ['Enchantress', 'Night Stalker', 'Alchemist', 'Dazzle', 'Puck'])

# get_prediction(['Marci', 'Zeus', 'Faceless Void', 'Snapfire', 'Tidehunter'],
#               ['Dawnbreaker', 'Tiny', 'Winter Wyvern','Beastmaster', 'Alchemist'])

# get_prediction(['Marci', 'Viper', 'Nyx Assassin', 'Tidehunter', 'Void Spirit'],
#               ['Tiny', 'Dawnbreaker', 'Crystal Maiden', 'Razor', 'Puck'])

# get_prediction(['Tiny', "Nature's Prophet", 'Monkey King', 'Bounty Hunter', 'Keeper of the Light'],
#                ['Chaos Knight', 'Io', 'Marci', 'Void Spirit', 'Bristleback'])

# get_prediction(['Chen', 'Bristleback', 'Tusk', 'Visage', 'Void Spirit'],
#               ['Winter Wyvern', 'Tiny', 'Bane', 'Templar Assassin', 'Pangolier'])

# get_prediction(['Naga Siren','Razor', 'Marci', 'Necrophos', 'Lina'],
#               ['Tiny', 'Viper', 'Alchemist', 'Dazzle', 'Storm Spirit'])

# get_prediction(['Winter Wyvern', 'Puck', 'Snapfire', 'Templar Assassin', 'Slardar'],
#               ['Tiny', 'Enchantress', 'Rubick', 'Earthshaker', 'Spectre'])

# get_prediction(['Marci', 'Puck', 'Phoenix', 'Lifestealer', 'Necrophos'],
#               ['Chen', 'Kunkka', 'Rubick', 'Dawnbreaker', 'Beastmaster'])

get_prediction(['Earthshaker', 'Keeper of the Light', 'Bane', 'Monkey King', 'Timbersaw'],
               ['Marci', 'Death Prophet', 'Dazzle', 'Kunkka', 'Lone Druid'])


#def test_predictor():
#    picks_list = get_formatted_match_pick_list()
#    for map in picks_list:
#        str_to_list_pick1 = map[0].split('-')[:-1]
#        str_to_list_pick2 = map[1].split('-')[:-1]
#        print(str(get_map_pick(str_to_list_pick1, str_to_list_pick2)) + ' : '
#              + str([map[0][-4:], map[1][-4:]]))
