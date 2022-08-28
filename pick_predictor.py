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


def get_heroes_synergy(pick_1, pick_2):
    for hero in pick_1:
        matched_list = get_list_with_matched_heroes(hero)
        pick_list = []
        for pick in matched_list:
            if hero in pick[0]:
                pick_list.append(pick[0])
            elif hero in pick[1]:
                pick_list.append(pick[1])

        count_of_pairs_picked = 0
        count_of_pairs_picked_win = 0
        for i in pick_list:
            if 'Marci' in i:
                count_of_pairs_picked += 1
                if i[-3:] == 'WIN':
                    count_of_pairs_picked_win += 1
        print(count_of_pairs_picked)
        print(count_of_pairs_picked_win)


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

# ############################################################################################################
# # Alliance Entity Map 1 (799:901)
# get_prediction(['Viper', 'Tiny', 'Warlock', 'Pudge', 'Windranger'],
#                ['Sven', 'Chen', 'Enigma','Visage', 'Razor'])
# # Secret Thunder Map 1 (1143:1057)
# get_prediction(['Razor', 'Marci', 'Ogre Magi', 'Batrider', 'Void Spirit'],
#                ['Winter Wyvern', 'Weaver','Snapfire', 'Timbersaw', 'Mars'])
# # Talon Aster Map 1 (860:940)
# get_prediction(['Io', 'Storm Spirit', 'Earth Spirit', 'Brewmaster', 'Sniper'],
#                ['Tiny', 'Puck', 'Grimstroke', 'Viper', 'Bristleback'])
# ############################################################################################################
# # Alliance Entity Map 2 (558:842)
# get_prediction(['Chen', 'Enigma', 'Sven', 'Invoker', 'Pudge'],
#                ['Viper', 'Tiny', 'Warlock', 'Faceless Void', 'Death Prophet'])
# # Thunder Secret Map 2 (770:830)
# get_prediction(['Weaver', 'Monkey King', 'Abaddon', 'Alchemist'],
#               ['Marci', 'Viper', 'Chen', 'Void Spirit', 'Templar Assassin'])
# # Talon Aster Map 2 (764:1436)
# get_prediction(['Snapfire', 'Dawnbreaker', 'Void Spirit', 'Faceless Void', 'Alchemist'],
#                ['Tiny', 'Razor', 'Dazzle', 'Enigma', 'Bloodseeker'])
# ############################################################################################################
# # Entity Talon Map 1 (1184:1016)
# get_prediction(['Bristleback', 'Puck', 'Bane', 'Visage', 'Zeus'],
#                ['Razor', 'Void Spirit', 'Death Prophet', 'Tusk', 'Dazzle'])
# # Aster Thunder Map 1 (994:906)
# get_prediction(['Razor', 'Winter Wyvern', 'Clockwerk', 'Templar Assassin', 'Invoker'],
#                ['Tiny', 'Queen of Pain', 'Dazzle', 'Bloodseeker', 'Timbersaw'])
# # Secret Alliance Map 1 (944:856)
# get_prediction(['Dazzle', 'Faceless Void', 'Puck', 'Snapfire', 'Timbersaw'],
#               ['Razor', 'Marci', 'Omniknight', 'Kunkka', 'Beastmaster'])
# ############################################################################################################
# # Secret Alliance Map 2 ()
# get_prediction(['Marci', 'Razor', 'Dark Willow','Timbersaw', 'Monkey King'],
#                ['Earth Spirit', 'Keeper of the Light', 'Bristleback', 'Mars', 'Io'])
# # Talon Entity Map 2 (625:575)
# get_prediction(['Io', 'Bristleback', 'Keeper of the Light', 'Tusk', 'Timbersaw'],
#                ['Chen', 'Viper', 'Sven', 'Invoker', 'Pudge'])
# # Thunder Aster Map 2 (959:1041)
# get_prediction(['Tiny', 'Batrider', 'Ogre Magi', 'Weaver', 'Monkey King'],
#                ['Razor', 'Grimstroke', 'Earth Spirit', 'Faceless Void', 'Void Spirit'])
# ############################################################################################################
# # Liquid OG Map 1 (775:825)
# get_prediction(['Tiny', 'Puck', 'Ancient Apparition', 'Lycan', 'Dawnbreaker'],
#                ['Razor', 'Chen', 'Earthshaker', 'Templar Assassin', 'Ember Spirit'])
# # TSM Nigma Map1 (784:816)
# get_prediction(['Razor', 'Tiny', 'Jakiro', 'Doom', 'Phantom Assassin'],
#                ['Enchantress', 'Puck', 'Tusk', 'Lone Druid', 'Death Prophet'])
# # Fnatic Boom Map 1 (1138:962)
# get_prediction(['Chen', 'Faceless Void', 'Marci', 'Batrider', 'Pudge'],
#                ['Mars', 'Snapfire', 'Winter Wyvern', 'Juggernaut', 'Zeus'])
# ############################################################################################################
# # Liquid OG Map 2 (939:761)
# get_prediction(['Chen', 'Lone Druid', 'Nyx Assassin', 'Enigma', 'Storm Spirit'],
#                ['Razor', 'Elder Titan', 'Snapfire', 'Templar Assassin', 'Pangolier'])
# # TSM Nigma Map 2 (766:734)
# get_prediction(['Mirana', 'Puck', 'Witch Doctor', 'Brewmaster', 'Templar Assassin'],
#                ['Enchantress', 'Lone Druid', 'Monkey King', 'Nyx Assassin', 'Enigma'])
# # Fnatic Boom Map 2 (835:1065)
# get_prediction(['Tiny', 'Batrider', 'Templar Assassin', 'Enchantress', 'Keeper of the Light'],
#                ['Kunkka', 'Winter Wyvern', 'Mirana', 'Phantom Lancer', 'Venomancer'])
# ############################################################################################################
# # Liquid Nigma Map 1 (910:1090)
# get_prediction(['Death Prophet', 'Tiny', 'Keeper of the Light', 'Night Stalker', 'Skywrath Mage'],
#                ['Puck', 'Tusk', 'Bristleback', 'Snapfire', 'Visage'])
# # TSM Boom Map 1 (1077:1223)
# get_prediction(['Enchantress', 'Puck', 'Rubick', 'Faceless Void', 'Lycan'],
#                ['Tiny', 'Death Prophet', 'Zeus', 'Clockwerk', 'Wraith King'])
# # OG Fnatic Map 1 (851:849)
# get_prediction(['Razor', 'Elder Titan', 'Winter Wyvern', 'Kunkka', 'Alchemist'],
#                ['Chen', 'Faceless Void', 'Queen of Pain', 'Earth Spirit', 'Weaver'])
# ############################################################################################################
# # Liquid Nigma Map 2 (793:1007)
# get_prediction(['Dazzle', 'Tiny', 'Batrider', 'Timbersaw', 'Ursa'],
#                ['Winter Wyvern', 'Keeper of the Light', 'Chen', 'Faceless Void', 'Axe'])
# # TSM Boom Map 2 (1061:1039)
# get_prediction(['Enchantress', 'Enigma', 'Queen of Pain', 'Tusk', 'Monkey King'],
#                ['Tiny', 'Dazzle', 'Pangolier', "Nature's Prophet", 'Weaver'])
# # OG Fnatic Map 2 (802:598)
# get_prediction(['Chen', 'Puck', 'Treant Protector', 'Arc Warden', 'Sand King'],
#                ['Razor', 'Templar Assassin', 'Monkey King', 'Enchantress', 'Broodmother'])
# ############################################################################################################

# # Thunder Entity Map 1(588:812)
# get_prediction(['Winter Wyvern', 'Mars', 'Rubick', 'Centaur Warrunner', 'Phantom Assassin'],
#                 ['Tiny', 'Invoker', 'Abaddon','Faceless Void', 'Phoenix'])
# # Secret Aster Map 1 (918:982)
# get_prediction(['Ogre Magi', 'Monkey King', 'Dawnbreaker', 'Queen of Pain', 'Tusk'],
#                ['Mars', 'Templar Assassin', 'Batrider', 'Mars', 'Enchantress'])
# # Talon Alliance Map 1 (444:456)
# get_prediction(['Ursa', 'Templar Assassin', 'Beastmaster', 'Hoodwink', 'Ogre Magi'],
#                ['Phoenix', 'Enchantress', 'Centaur Warrunner', 'Huskar', 'Pudge'])

# # Secret Aster Map 2 (570:630)
# get_prediction(['Ogre Magi', 'Queen of Pain', 'Bloodseeker', 'Dark Willow', 'Timbersaw'],
#                ['Grimstroke', 'Monkey King', 'Dragon Knight', 'Enigma', 'Tiny'])
# # Thunder Entity Map 2 (640:760)
# get_prediction(['Mars', 'Kunkka', 'Dazzle', 'Enigma', 'Rubick'],
#                ['Disruptor', 'Tiny', 'Queen of Pain', 'Visage', 'Lifestealer'])


# # Entity Secret Map 1 (590:410)
# get_prediction(['Sven', 'Visage', 'Bane', 'Pudge', 'Ember Spirit'],
#                ['Ogre Magi', 'Templar Assassin', 'Techies', 'Tidehunter', 'Mars'])
# # Thunder Talon Map 1 (800:600)
# get_prediction(['Tiny', 'Templar Assassin', 'Snapfire', 'Ogre Magi', 'Tidehunter'],
#                ['Enchantress', 'Centaur Warrunner', 'Phoenix', 'Pudge', 'Monkey King'])

# # Entity Secret Map 2 (369:331)
# get_prediction(['Techies', 'Sven', 'Tidehunter', 'Bristleback', 'Sniper'],
#                ['Chen', 'Visage', 'Hoodwink', 'Lone Druid', 'Ember Spirit'])
# # Thunder Talon Map 2 (904:996)
# get_prediction(['Batrider', 'Winter Wyvern', 'Centaur Warrunner', 'Nyx Assassin', 'Wraith King'],
#                ['Doom', 'Clockwerk', 'Puck', 'Visage', 'Bane'])

# # Boom Nigma Map 1 ()
# get_prediction(['Doom', 'Rubick'],
#                ['Enchantress', 'Dawnbreaker', 'Earth Spirit'])
# # OG TSM Map 1 ()
# get_prediction(['Snapfire', 'Faceless Void', 'Legion Commander', 'Dazzle', 'Death Prophet'],
#                ['Chen', 'Mars', 'Techies', 'Troll Warlord', 'Shadow Fiend'])
# # Fnatic Liquid Map 1 ()
# get_prediction(['Tiny', 'Puck', 'Bloodseeker', 'Shadow Demon'],
#                ['Keeper of the Light', 'Bristleback', 'Nyx Assassin', 'Batrider'])

# # Nigma Boom Map 2 (563:637)
# get_prediction(['Io', 'Terrorblade', 'Lion', 'Queen of Pain', 'Pudge'],
#                ['Death Prophet', 'Tusk', 'Snapfire', 'Faceless Void', 'Zeus'])

# get_prediction(['Puck', 'Tusk', 'Enchantress', 'Pudge', 'Batrider'],
#               ['Keeper of the Light', 'Night Stalker', 'Earthshaker', 'Razor'])

# # Fnatic TSM Map 1 ()
# get_prediction(['Keeper of the Light', 'Beastmaster', 'Rubick', 'Brewmaster', 'Luna'],
#                    ['Queen of Pain', 'Nyx Assassin', 'Warlock', 'Phantom Assassin', 'Dark Seer'])
#
# get_prediction(['Chaos Knight', 'Dazzle', 'Rubick', 'Pangolier', 'Juggernaut'],
#                ['Death Prophet', 'Brewmaster', 'Puck', 'Dark Willow', 'Alchemist'])

# get_prediction(['Snapfire', 'Mars', 'Mirana', 'Ogre Magi', 'Medusa'],
#                ['Tiny', 'Enchantress', 'Monkey King', 'Storm Spirit', 'Visage'])
#
# get_prediction(['Keeper of the Light', 'Bristleback', 'Nyx Assassin', 'Razor', 'Pangolier'],
#                ['Batrider', 'Mars', 'Dark Willow', 'Dawnbreaker', 'Phantom Assassin'])

# get_prediction(['Queen of Pain', 'Shadow Shaman', 'Undying', 'Beastmaster', 'Ursa'],
#                ['Ogre Magi', 'Invoker', 'Monkey King', 'Techies', 'Axe'])
#
# get_prediction(['Chen', 'Tusk', 'Rubick', 'Pudge', 'Faceless Void'],
#                ['Tiny', 'Puck', 'Templar Assassin', 'Elder Titan', 'Keeper of the Light'])

# get_prediction(['Enigma', 'Batrider', 'Ancient Apparition', 'Nyx Assassin', 'Alchemist'],
#               ['Dawnbreaker', 'Winter Wyvern', 'Puck', 'Phantom Assassin', 'Beastmaster'])

# def test_predictor():
#    picks_list = get_formatted_match_pick_list()
#    for map in picks_list:
#        str_to_list_pick1 = map[0].split('-')[:-1]
#        str_to_list_pick2 = map[1].split('-')[:-1]
#        print(str(get_map_pick(str_to_list_pick1, str_to_list_pick2)) + ' : '
#              + str([map[0][-4:], map[1][-4:]]))
