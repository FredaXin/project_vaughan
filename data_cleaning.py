#!/usr/bin/env python3

import os
import csv
from pathlib import Path

# Reference: https://docs.python.org/3/library/csv.htimport os
def csv_to_dict(filename):
    '''Convert csv file into reader object, then into a list of dictionaries'''
    result_list=[]
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result_list.append(dict(row))
    return result_list


def find_matching_in_dict_list(input_dict, value_list):
    '''Loop through a list of dictionaries to find matching values
    Return a list of dictionaries'''
    new_list = []
    for csd in input_dict: 
        if csd['\ufeffcsd'] in value_list: 
            new_list.append(csd)
    return new_list


def dict_list_to_csv(dict_list, filename):
    '''Covert list of dictionaries back into csv'''
    keys = dict_list[0].keys()
    with open(f'{filename}.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)
    return output_file


# Loop through all the files in the directory 

# Generate a list of csv file paths
# Reference: https://www.newbedev.com/python/howto/how-to-iterate-over-files-in-a-given-directory/
def generate_file_path_list(current_direct=os.getcwd()):
    '''Generate a list of csv file paths'''
    file_list = []
    for subdir, dirs, files in os.walk(current_direct):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".csv"):
                file_list.append(filepath)
    return file_list



# Main block: call all the functions 
if __name__ == '__main__': 
    # Any mulicipty names can be stored in this list. 
    # The strings need to be the same as it is on the CSV files.
    list_of_csd = ['Newfoundland and Labrador', 'Ontario']

    cwd_path = Path(__file__).parent

    # 1. Change 'processed_data' into the name of the directory where you store all
    #    the CSV files.
    # 2. Switch out the file name 'csd_2014.csv' if you want to inspect
    #    different CSV files.
    # 3. change the name 'dict_csd_2014' accordingly
    dict_csd_2014 = csv_to_dict(str(cwd_path / 'processed_data' / 'csd_2014.csv'))
      
    list_2014 = find_matching_in_dict_list(dict_csd_2014, list_of_csd)
    dict_list_to_csv(list_2014, '2014')

    print(list_2014)
    print(generate_file_path_list(str(cwd_path)))


