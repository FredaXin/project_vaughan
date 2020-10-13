import os
import csv

# Reference: https://docs.python.org/3/library/csv.htimport os
def csv_to_dict(filename):
    '''Convert reader object into a list of dictionaries'''
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
    res = []
    for csd in input_dict: 
        if csd['\ufeffcsd'] in value_list: 
            res = csd 
            new_list.append(res)
    return new_list


def dict_list_to_csv(dict_list, filename):
    '''Covert list of dictionaries back into csv'''
    toCSV = dict_list
    keys = toCSV[0].keys()
    with open(f'{filename}.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)
    return output_file


# Loop through all the files in the directory 

# Generate a list of csv file paths
def generate_file_path_list(current_direct=os.getcwd()):
    '''Generate a list of csv file paths'''
    file_list = []
    for subdir, dirs, files in os.walk(current_direct):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".csv"):
                file_list.append(filepath)
    return file_list

print(generate_file_path_list())

# Call the funcitons
# print(os.getcwd())
# list_of_csd = ['Newfoundland and Labrador', 'Ontario']
# dict_csd_2014 = csv_to_dict('processed_data/csd_2014.csv')
# list_2014 = find_matching_in_dict_list(dict_csd_2014, list_of_csd)
# dict_list_to_csv(list_2014, '2014')

# print(list_2014)


