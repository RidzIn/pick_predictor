import pandas as pd
from pick_predictor import get_formatted_match_pick_list, get_duel_stats


# Takes file name which you get as result
# [816, 784] : ['-WIN', 'LOSE']
# [734, 766] : ['LOSE', '-WIN']
# [733, 967] : ['LOSE', '-WIN']
def predictor_test(file_to_save, data_to_test):
    my_file = open(file_to_save, 'w')
    picks_list = get_formatted_match_pick_list(data_to_test)
    for map_pick in picks_list:
        str_to_list_pick1 = map_pick[0].split('-')[:-1]
        str_to_list_pick2 = map_pick[1].split('-')[:-1]
        my_file.write(str(str(get_duel_stats(str_to_list_pick1, str_to_list_pick2)) + ' : '
                          + str([map_pick[0][-4:], map_pick[1][-4:]])) + '\n')

    return my_file


# Takes generated file from 'predictor_test' and gap between pick_scores
# CORRECT: 23
# INCORRECT: 30
# EVEN: 13
def prediction_stat(file_to_test, pick_score_gap):
    with open(file_to_test, 'r') as f:
        data = f.read()
    new_list = data.split('\n')
    another_list = []
    for i in new_list:
        another_list.append(i.split(' : '))
    # print(another_list)
    correct_prediction = 0
    incorrect_prediction = 0
    even_prediction = 0
    for i in another_list:
        try:
            i[0] = i[0][1:-1].split(', ')
            i[1] = i[1][1:-1].split(', ')
            # print(str(i[0][0]) + ' : ' + str(i[0][1]))
            # print(str(i[1][0]) + ' : ' + str(i[1][1]))
            if abs(int(i[0][0]) - int(i[0][1])) > pick_score_gap:
                if int(i[0][0]) > int(i[0][1]) and i[1][0] == "'-WIN'":
                    correct_prediction += 1
                elif int(i[0][0]) < int(i[0][1]) and i[1][1] == "'-WIN'":
                    correct_prediction += 1
                else:
                    incorrect_prediction += 1
            else:
                even_prediction += 1
        except IndexError:
            pass
    print('CORRECT: ' + str(correct_prediction))
    print('INCORRECT: ' + str(incorrect_prediction))
    print('EVEN: ' + str(even_prediction))


# D2CL Tier 2.5
# Doubled - 24 21 2
# Not Doubled 24 22 1

# predictor_test('some_test.txt')
# ESL Malesia
# Not doubled - 29 33 4
# Doubled - 33 31 2

'''
Guide how to get prediction statistic.
1) Create Data frame from CVS file you want to test
2) Use 'predictor_test' to generate log file
3) generated file use as parameter for 'prediction_stat'
4) Check your results
'''
test_data = pd.read_csv('data/test_data.csv')
test_data_before_patch = pd.read_csv('data/test_data_before_patch.csv')

predictor_test('some_test.txt', test_data)
prediction_stat('some_test.txt', 10)
