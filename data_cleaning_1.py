import numpy as np
import pandas as pd
import os

def change_path(input_path):
    return os.chdir(input_path)

change_path('/Users/fredaxin/projects/project_vaughan')

top_25 = pd.read_csv('./processed_data_1/building_permits_2000_2019_top_25.csv')
york_region = pd.read_csv('./processed_data_1/building_permits_2000_2019_york_region.csv')
census = pd.read_csv('./processed_data_1/census_2001_to_2016.csv')

# print(
#     top_25.head(), 
#     top_25.info()
#     )

# print(
#     york_region.head(),
#     york_region.info()
# )

# Change data types
def obj_to_int(series):
    return series.apply(lambda x: x.replace(',', '')).astype(int)

columns_to_change_25 = [
    'value_nonresidential_commercial',
    'value_nonresidential_industrial', 'value_nonresidential_institutional',
    'value_residential_single_single', 'value_residential_single_mobile',
    'value_residential_single_cottage', 'value_residential_multiple_double',
    'value_residential_multiple_row', 'value_residential_multiple_apartment',
    'units_residential_single_single', 'units_residential_multiple_double',
    'units_residential_multiple_row', 'units_residential_multiple_apartment'
    ]  
top_25[columns_to_change_25] = top_25[columns_to_change_25].apply(obj_to_int, axis=1)

columns_to_change_york = [
    'value_nonresidential_commercial',
    'value_nonresidential_industrial', 'value_nonresidential_institutional',
    'value_residential_single_single', 'value_residential_single_mobile',
    'value_residential_single_cottage', 'value_residential_multiple_double',
    'value_residential_multiple_row', 'value_residential_multiple_apartment',
    ]
york_region[columns_to_change_york] = york_region[columns_to_change_york].apply(obj_to_int, axis=1)

# Check unique values 
# print(sorted(list(top_25['csd'].unique())), len(list(top_25['csd'].unique())))

# Notes: 
# For the naming of CSD, from 2000 to 2017 are consistant; 
# 2018 & 2019 are without Census subdivisions types. 
# More info about the Census subdivisions types:
# https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/geo012-eng.cfm

# Target CSD List
# The list is chosen from 
census.sort_values(by='2016',  ascending=False, inplace=True)
census['CSD&type'] = census['CSD_0'] + ', ' + census['geographic_type']
target_csd_list_1 = list(set(census['CSD&type'].head(26)))
target_csd_list_2 = list(set(census['CSD_0'].head(26)))



### Deal with 2000 to 2017 permit data ###

top_25_00to17 = top_25[top_25['year'] <= 2017]
csd_list_00to17 = sorted(list(top_25_00to17['csd'].unique())) 
csd_list_00to17_len = len(list(top_25_00to17['csd'].unique()))


# Since for the 2000 to 2017 data, all csd names contains the ensus subdivisions
# types, i.e. "Vaughan, CY", we can infer that the ones that do not contain the
# types are not the csd we need. 
# This is confirmed by inspecting the following list in the source data.
suspect_list = [i for i in csd_list_00to17 if ',' not in i]
top_25_00to17 = top_25_00to17[~top_25_00to17['csd'].isin(suspect_list)]


# Check if all elements in the target list are in csd list
csd_list_00to17 = sorted(list(top_25_00to17['csd'].unique()))
# print(set(target_csd_list_1).issubset(csd_list_00to17))

# Only keep the csds that are in the target list
top_25_00to17 = top_25_00to17[top_25_00to17['csd'].isin(target_csd_list_1)]

# Sort the df by csd and year
top_25_00to17 = top_25_00to17.sort_values(['csd', 'year'], ascending=[True, True])

# Check duplicated rows
mask_1 = top_25_00to17.duplicated(keep=False)
# print(f'duplicated rows: {top_25_00to17[mask_1]}')

# Check if each csd contains from 2000 to 2017 data
# Check if there is duplicates for each csd
# For each csd, it should have one row for each year. Each csd should include 18
# years. Any csd that has less or more than 18 is a problem.
temp_df_1 = top_25_00to17.groupby(['csd']).count().reset_index()
problem_set_1 = set(temp_df_1[temp_df_1['year']!=18]['csd'])
print(problem_set_1)

# Check if for each csd, each year is included. If the count of year does not eqaul
# 1, it is a porblem.
temp_df_2 = top_25_00to17.groupby(['csd', 'year']).size().to_frame(name='count').reset_index()
problem_set_2 = set(temp_df_2[temp_df_2['count']!=1]['csd'])
print(problem_set_2)
print(temp_df_2[temp_df_2['count']!=1])

# Check if the two problem groups are the same.
# print(problem_set_1 == problem_set_2)

# TODO: Investigate the csd in these group



### Deal with 2018 to 2019 permit data ###

top_25_18to19 = top_25[top_25['year'] > 2017]
csd_list_18to19 = sorted(list(top_25_18to19['csd'].unique())) 
csd_list_len_18to19 = len(list(top_25_18to19['csd'].unique()))
# print(csd_list_18to19, csd_list_len_18to19)

# Check if all elements in the target list are in csd list
# print(set(target_csd_list_2).issubset(csd_list_18to19))

# Inspect the csds in the building permit data that are not in the target list
# Upon inspection, these csds should not be included.
diff_list = np.setdiff1d(csd_list_18to19, target_csd_list_2)
# print(f'csds that are not in the targest list: {diff_list}')
top_25_18to19 = top_25_18to19[top_25_18to19['csd'].isin(target_csd_list_2)]

# Sort the df by csd and year
top_25_18to19 = top_25_18to19.sort_values(['csd', 'year'], ascending=[True, True])

# Check duplicated rows
# Upon inspection, those duplicated rows came from the 2018 permit data, and
# they are caused by formating issues
# 6 duplicated rows were deleted
mask_2 = top_25_18to19.duplicated(keep=False)
# print(f'duplicated rows: {top_25_18to19[mask_2]}')
top_25_18to19 = top_25_18to19.drop_duplicates(keep='first')


# csd_list_18to19 = sorted(list(top_25_18to19['csd'].unique())) 
# csd_list_len_18to19 = len(list(top_25_18to19['csd'].unique()))
# print(csd_list_18to19, csd_list_len_18to19)

# For each csd, it should have one row for each year. Each csd should include 2
# years. Any csd that has less or more than 18 is a problem.
temp_df_3 = top_25_18to19.groupby(['csd']).count().reset_index()
problem_list_3 = list(set(temp_df_3[temp_df_3['year']!=2]['csd']))
# print(temp_df_3.head())
# print(problem_list_3)
# print(temp_df_3[temp_df_3['year']!=2])


# Check if for each csd, each year is included. If the count of year does not eqaul
# 1, it is a porblem.
temp_df_4 = top_25_18to19.groupby(['csd', 'year']).size().to_frame(name='count').reset_index()
problem_list_4 = list(set(temp_df_4[temp_df_4['count'] > 1]['csd']))
# print(temp_df_4.head())
# print(problem_set_4)
print(temp_df_4[temp_df_4['count'] != 1])

# Check if the two problem groups are the same.
# print(problem_set_1 == problem_set_2)
