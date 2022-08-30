import pandas as pd


# It's helping function for 'hero_picks_win_rate_df'
# Creates Series
# (hero_1-result)
# (hero_2-result)
# (hero_3-result)
# (hero_5-result)
# (hero_5-result)
def generate_heroes_with_results_list(main_df):
    all_heroes = pd.concat([main_df['HERO_1'], main_df['HERO_2'], main_df['HERO_3'], main_df['HERO_4'],
                            main_df['HERO_5']]).reset_index(drop=True)
    all_results = pd.concat([main_df['RESULT'], main_df['RESULT'], main_df['RESULT'], main_df['RESULT'],
                             main_df['RESULT']]).reset_index(drop=True)
    return [all_heroes, all_results]


# Helping function for 'popular_pairs_df' 'unique_heroes_df'
# Generate list of unique heroes from 'generate_heroes_with_results_list'
def unique_heroes_list(main_df):
    return generate_heroes_with_results_list(main_df)[0].unique()


# Helping function for 'popular_pairs_df'
# Generate Series (hero1-hero2-hero3-hero4-hero5-result)
def every_pick_list(main_df):
    pick_formatted_list = main_df[['HERO_1', 'HERO_2', 'HERO_3', 'HERO_4', 'HERO_5', 'RESULT']].apply("-".join, axis=1)
    return pick_formatted_list.tolist()


# Helping function for 'unpicked_heroes_df'
# Takes .txt file with all heroes and return list of them
def all_heroes_list():
    with open('input_data/list_of_heroes.txt') as match_file:
        heroes_data = match_file.readlines()

    result_list = []
    for i in heroes_data:
        if i != '\n':
            result_list.append(i[:-1].lstrip())

    return result_list


# Helping function for 'popular_pairs_df'
# Takes dict of all possible pairs and return filtered by key('WIN', 'LOSE')
def get_picked_pairs_by_condition(my_dict, every_picks, key):
    if key == 'LOSE':
        for pick in every_picks:
            if pick[-4:] == 'LOSE':
                for key, value in my_dict.items():
                    if key[0] in pick[:-1] and key[1] in pick[:-1]:
                        my_dict[key] = my_dict.get(key, 0) + 1
        return my_dict

    if key == 'WIN':
        for pick in every_picks:
            if pick[-3:] == 'WIN':
                for key, value in my_dict.items():
                    if key[0] in pick[:-1] and key[1] in pick[:-1]:
                        my_dict[key] = my_dict.get(key, 0) + 1
        return my_dict


def unpicked_heroes_list(main_df):
    # Get list of unpicked heroes
    every_heroes = all_heroes_list()
    unique_heroes = unique_heroes_list(main_df)
    unpicked_heroes = []
    for i in every_heroes:
        if i not in unique_heroes:
            unpicked_heroes.append(i)
    return unpicked_heroes
