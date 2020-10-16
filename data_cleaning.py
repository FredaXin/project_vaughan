#!/usr/bin/env python3

import os
import csv
from pathlib import Path

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

def get_column_names(dict_list):
    '''Return all the columns names of a dict list'''
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


# def clean_label(l: str) -> str:
#     return l[5:] if l[0].isdigit() else l

# def clean_dict_labels(d: dict) -> dict:
#     return {clean_label(k): v for k, v in d.items()}
     
# def change_column_names_(dict_list: 'list(dict)') -> 'list(dict)':
#     return [clean_dict_labels(d) for d in dict_list]

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


def consolidate_all_years(value_list, cwd_path=Path(__file__).parent):
    file_path_list = generate_file_path_list(str(cwd_path))
    final_dict_list = []
    for path in file_path_list:
        dict_list = csv_to_dict(path)
        matched_dict_list = find_matching_in_dict_list(dict_list, value_list)
        column_names = get_column_names(matched_dict_list)
        year = get_year(column_names)
        print(year)
        dict_list_with_year = add_year_to_dict_list(year, matched_dict_list)
        dict_list_with_changed_column_names = change_column_names(dict_list_with_year)
        final_dict_list.extend(dict_list_with_changed_column_names)
    return final_dict_list 



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
    list_of_csd = ['Vaughan, CY', 'Vaughan']

    # # Find the parent path of the current working directory
    # cwd_path = Path(__file__).parent

    # # Print out the paths of all CSV files in current and sub directories
    # print(generate_file_path_list(str(cwd_path)))

    # # 1. Change 'processed_data' into the name of the directory where you store all
    # #    the CSV files.
    # # 2. Switch out the file name 'csd_2014.csv' if you want to inspect
    # #    different CSV files.
    # # 3. change the name 'dict_csd_2014' accordingly
    # #dict_csd_2014 = csv_to_dict(str(cwd_path / 'processed_data' / 'csd_2014.csv'))


    # # Generate a list of dictionary based on chosen list of csd
    # #list_2014 = find_matching_in_dict_list(dict_csd_2014, list_of_csd)
    # #print(list_2014)

    # column_names = get_column_names(list_2014)
    # print(column_names)

    # year = get_year(column_names)
    # print(year)

    # new_dict_list = add_year_to_dict_list(year, list_2014)
    # print(new_dict_list)

    # new_new_dict_list = change_column_names(new_dict_list)
    # print(new_new_dict_list)

    final_list = consolidate_all_years(list_of_csd)
    print(final_list)

    dict_list_to_csv(final_list, 'test')
 



    # # Convert list of dicts into CSV
    # dict_list_to_csv(list_2014, '2014')
