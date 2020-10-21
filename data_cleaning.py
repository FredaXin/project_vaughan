#!/usr/bin/env python3

import os
import csv
from pathlib import Path

TOTAL_COLUMN = 17
CSD = '\ufeffcsd'


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


# Reference: https://docs.python.org/3/library/csv.htimport os
def csv_to_dict(filename):
    '''Convert csv file into reader object, then into a list of dictionaries'''
    result_list=[]
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result_list.append(dict(row))
    return result_list

# Two matching functions below: partial vs. exact
# Please choose one of them based on your need
def find_matching_in_dict_list(input_dict, value_list):
    '''Loop through a list of dictionaries to find matching values
    Return a list of dictionaries
    Partial String Match'''
    new_list = []
    for csd in input_dict: 
        for value in value_list:
            if csd[CSD] in value_list or value in csd[CSD]: 
                new_list.append(csd)
    return new_list

# def find_matching_in_dict_list(input_dict, value_list):
#     '''Loop through a list of dictionaries to find matching values
#     Return a list of dictionaries
#     Exact String Match'''
#     new_list = []
#     for csd in input_dict: 
#         if csd[CSD] in value_list: 
#             new_list.append(csd)
#     return new_list

def get_column_names(dict_list):
    '''Return all the columns names of a dictionary list as a list'''
    return list(dict_list[0].keys())


def get_year(column_names):
    '''Find the year of the dataframe'''
    year = 0
    for column_name in column_names:
        if column_name[0].isdigit():
            year = column_name[0:4]
            break 
    return int(year)


def add_year_to_dict_list(year, dict_list):
    '''Add the year to the dict list as new key:value pair'''
    for dict in dict_list:
        dict['year'] = year
    return dict_list


def change_column_names(dict_list):
    '''Strip the year from column names'''
    for indv_dict in dict_list:
        keys = list(indv_dict.keys())
        for key in keys:
            if key[0].isdigit():
                new_key = key[5:]
                indv_dict[new_key] = indv_dict.pop(key)
            else: 
                continue
    return dict_list


# Special Treatment for sheet year 2000 - 2013 
def split_years(dict_list):
    '''
    For csv files contains multiple years on one sheet.
    Take a list of dictionaries, output a list dictionaries with each year as
    separate dictionary.
    '''
    new_dict_list = []

    for indv_dict in dict_list:
        column_names = list(indv_dict.keys())
        year_list = list(set([name[0:4] for name in column_names if name[0].isdigit()]))
    
        for year in year_list:
            new_dict = {}
            new_dict[CSD] = indv_dict[CSD]

            for name in column_names:
                if name[0:4] == year:
                    new_dict[name] = indv_dict[name]
                    new_dict['year'] = year
                else:
                    continue
            new_dict_list.append(new_dict)

    return new_dict_list


def merge_two_dicts(dict1, dict2):
    '''Merge two dictionaries into one'''
    new_dict = {}

    for key, value in dict1.items():
        new_dict[key] = value

    for key, value in dict2.items():
        new_dict[key] = value

    return new_dict

def merge_value_unit(dict_list):
    '''merge the value and unit sheets into one dictionary'''
    new_dict_list = []

    while dict_list:
        indv_dict_1 = dict_list.pop()
        if len(indv_dict_1) >= TOTAL_COLUMN:
            new_dict_list.append(indv_dict_1)
        else:
            for index, indv_dict_2 in enumerate(dict_list):     
                if indv_dict_1[CSD] == indv_dict_2[CSD] and indv_dict_1['year'] == indv_dict_2['year']:
                    merged_dict = merge_two_dicts(indv_dict_1, indv_dict_2)
                    new_dict_list.append(merged_dict)
                    dict_list.pop(index)
                    break
            else:
                raise RuntimeError(f'problmetic dict: {indv_dict_1}')
    return new_dict_list
                    

def consolidate_all_years(value_list, cwd_path=Path(__file__).parent):
    '''Loop through all csv files and consolidate into one dictionary list'''
    file_path_list = generate_file_path_list(str(cwd_path))

    final_dict_list = []

    for path in file_path_list:
        dict_list = csv_to_dict(path)
        matched_dict_list = find_matching_in_dict_list(dict_list, value_list)
        column_names = get_column_names(matched_dict_list)

        # Based on the original data file type, process the data accordingly
        if len(column_names) < TOTAL_COLUMN: 
            year = get_year(column_names)
            dict_list_with_year = add_year_to_dict_list(year, matched_dict_list)
            dict_list_with_changed_column_names = change_column_names(dict_list_with_year)
            final_dict_list.extend(dict_list_with_changed_column_names)

        else: 
            splitted_dicts_with_year = split_years(matched_dict_list)
            dict_list_with_changed_column_names = change_column_names(splitted_dicts_with_year)
            final_dict_list.extend(dict_list_with_changed_column_names)
 
    return merge_value_unit(final_dict_list)


# Optional: export dictionary list back to csv
def dict_list_to_csv(dict_list, filename):
    '''Convert list of dictionaries back into csv'''
    keys = dict_list[0].keys()
    with open(f'{filename}.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)
    return output_file


# Main block: call all the functions 
if __name__ == '__main__': 
    # Any mulicipty names can be stored in this list. 
    # The strings need to be the same as it is on the CSV files.
    list_of_csd = ['Toronto']
    final_list = consolidate_all_years(list_of_csd)

    dict_list_to_csv(final_list, 'test')
 
