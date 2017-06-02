import pandas as pd

''' To train the 1R model with the data set and predict further with the model
    1. All the attribute are given with the heading Cat_ and outcome_ as the output'''

'''How to predict the 1R Model For each attribute, For each value of the attribute, make a rule as follows
count how often each class appears, find the most frequent class
make the rule assign that class to the attribute value, calculate the error state of the rules
choose the rules with smallest error state'''

data_read = pd.read_csv('model.csv', header=None)

# Get the test data size and no of categories including the outcome column
row_size = data_read.shape[0]

# change data_read from Panda data frame to numpy array and also transpose it so you get all categories
# as seperate list in the numpy array
data_np_array = data_read.T.values

# Find the header list
header_list = []
for i in range(0, len(data_np_array)):
    header_list.append(data_np_array[i][0])

# find the outcome index
count = 0
cat_count = 0
for x in header_list:
    if 'cat' in x.lower():
        cat_count += 1
    elif 'outcome' in x.lower():
        outcome_index = count
    else:
        print "Did you really make the header with 'Cat_' or 'Outlook_'"
    count += 1

outcome_set = list(set(data_np_array[outcome_index][1:row_size + 1]))

def cal_outcomes(index_in, outix_in, dat_ar_in, row_size_in):
    # Get the set to be compared for various outcome
    scan_list_out = []
    cat_set = list(set(dat_ar_in[index_in][1:row_size_in + 1]))
    out_set = list(set(dat_ar_in[outix_in][1:row_size_in + 1]))

    # Initiate the scan_list with category items * outcome items
    for i in range(0, len(cat_set)):
        for j in range(0, len(out_set)):
            scan_list_out.append(0)

    # count total number of outcome options from the list
    total_items = 0
    for x in range(1, row_size):
        count = scan_list_out[(cat_set.index(dat_ar_in[index_in][x]))*len(out_set) + out_set.index(dat_ar_in[outix_in][x])]
        scan_list_out[(cat_set.index(dat_ar_in[index_in][x]))*len(out_set) + out_set.index(dat_ar_in[outix_in][x])] = count + 1
        total_items += 1
    return scan_list_out

def process_verbose_error(index_in, outix_in, dat_ar_in, row_size_in, scan_list_in):
    cat_set = list(set(dat_ar_in[index_in][1:row_size_in + 1]))
    out_set = list(set(dat_ar_in[outix_in][1:row_size_in + 1]))
    count = 0
    error_option = []
    for x in cat_set:
        print '\nIn option "%s"' % (x),
        error = []
        for y in out_set:
            print "%s %s " % (scan_list_in[count], y),
            error.append(scan_list_in[count])
            if min(error) == scan_list_in[count]:
                error_opt = y
            else:
                pass
            count += 1
        error_option.append(error_opt)
    print '\n\nThe respective error state  in %s is %s' % ([x for x in cat_set], error_option)

    count = 0
    total_error = 0
    for i in range(0, len(cat_set)):
        total_error = min(scan_list_in[count * 2], scan_list_in[count * 2 + 1]) + total_error
        count = count + 1
    print "Total Error for %s is %s" % (header_list[index_in], total_error)
    return total_error

def cal_processed_output(final_list_in):
    index = header_list.index(final_list_in[0])
    sub_set = list(set(data_np_array[index][1:row_size + 1]))
    count = 0
    dict_subset = {}
    for i in range(0, len(sub_set)):
        if (final_list_in[2][count * 2]) > (final_list_in[2][count * 2 + 1]):
            index = 0
        else:
            index = 1
        dict_subset[sub_set[i]] = outcome_set[index]
        count += 1
    rule_list_out = [final_list_in[0], dict_subset]
    return rule_list_out

def live_prediction(optimal_rule_in):
    live_data_read = pd.read_csv('predict.csv', header=None)
    rule_dict = dict(optimal_rule_in[1])
    predicted_list = []
    for i in range(0,live_data_read.shape[1]):
        if str(live_data_read[i][0]).lower() == str(rule_list[0]).lower():
            for j in range(1,live_data_read.shape[0]):
                predicted_list.append(rule_dict[live_data_read[i][j]])
        else:
            pass
    for i in range(0,live_data_read.shape[1]):
        if  'outcome' in str(live_data_read[i][0]).lower():
            for j in range(1, live_data_read.shape[0]):
                live_data_read[i][j] = predicted_list[j-1]
    live_data_read.to_csv('new_predicted.csv',header=None)

count = 0
Error_Percent = []
scan_list_array = []
for head_index in range(0, len(header_list)):
    if (count != outcome_index):
        print '\n'
        print 'In Category',
        print  header_list[head_index]
        print "============================",
        scan_list = cal_outcomes(head_index, outcome_index, data_np_array, row_size)
        error = process_verbose_error(head_index, outcome_index, data_np_array, row_size, scan_list)
        Error_Percent.append(error)
        count = count + 1
        scan_list_array.append(scan_list)

final_list = zip(header_list, Error_Percent, scan_list_array)
print '\nAll options with with error list as follows'
print final_list
print '\nWith least error, chosen RULE from TRAINING data is as follows'
print rule_list
rule_list = cal_processed_output(list(final_list[Error_Percent.index(min(Error_Percent))]))
live_prediction(rule_list)













'''CSV file is read with a header as a row and End row. Hence no. of rows will be r+2 in 0th index
csv file gives column in shape in 1st index'''

'''
category_set = list(set(data_np_array[0][1:row_size+1]))
out_set = list(set(data_np_array[outcome_index][1:row_size+1]))
out_set = tuple(out_set)

print "There are %s possible in the outcome and they are %s, happy with the learning so far?" %(len(out_set),out_set)

scan_list = []
Initiate the scan_list with category items * outcome items
for i in range(0, len(category_set)):
    for j in range(0, len(out_set)):
        scan_list.append(0)

Output should be as follows, OUTLOOK 

('OUTLOOK, 
[
dic
{
'SUNNY':'play'
'OVERCAST':'no play'
'RAIN':'play
}

Training/prediction mode & Live mode

my_code.build_model('training_data.csv'
    print self explanatory
returns optimal rule_encoded as above while printing out how it worked out this as the optimal rule

my_code.live('live_data.csv',optimal_rule)

returns live_data.csv with the last column fillen up according to optimal_tule

----------------------------------
Example of running your code:

selena_optimal_rule = selena_code.build_model('weather_data_training.csv')

selena_predicted_outcome = selena_code.live('weather_data_live.csv', selena_optimal_rule)

'''
