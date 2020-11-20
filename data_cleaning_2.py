import numpy as np
import pandas as pd
import os

def change_path(input_path):
    return os.chdir(input_path)

change_path('/Users/fredaxin/projects/project_vaughan')


#TODO Change path
permits = pd.read_csv('~/Desktop/Processed_Data.csv')

census_2006_2001 = pd.read_csv('./census_data/census_2006_2001.csv')
census_2011_2006 = pd.read_csv('./census_data/census_2011_2006.csv', encoding='latin-1')
census_2016_2011 = pd.read_csv('./census_data/census_2016_2011.csv', encoding='latin-1')


# Check if the 'Geographic code' is unique
print(f'Geographic code is unique: {pd.Series(census_2011_2006["Geographic code"]).is_unique}')

# Select relevant columns
pop_2001 = census_2006_2001[['CSD', '2001']]
pop_2006 = census_2011_2006[['Geographic code', 'Geographic name', 'Population, 2006']]
pop_2016_2011 = census_2016_2011[['Geographic code', 'Geographic name', 'Province or territory', 'Population, 2016', 'Population, 2011']]

# Merge census data from all years
pop_2006_2011_2016 = pd.merge(pop_2006, pop_2016_2011, on='Geographic code')
pop_2001_to_2016 = pd.merge(pop_2001, pop_2006_2011_2016, left_on='CSD', right_on='Geographic name_x', how='inner')

# Drop redundant columns and rows
pop_2001_to_2016.drop('Geographic name_x', axis=1, inplace=True)
pop_2001_to_2016.drop(0, axis=0, inplace=True)

# Rearrange the order of the columns
pop_2001_to_2016 = pop_2001_to_2016[['CSD', 'Geographic name_y', 'Province or territory', 'Geographic code', 
                                     '2001', 'Population, 2006', 'Population, 2011', 'Population, 2016']]
                                     
# Rename columns                                   
pop_2001_to_2016 = pop_2001_to_2016.rename(columns={'Geographic name_y': 'CSD_CD', 
                                                    'Province or territory': 'province_or_territory',
                                                    'Geographic code': 'geographic_code',
                                                    'Population, 2006': '2006',
                                                    'Population, 2011': '2011', 
                                                    'Population, 2016': '2016'})


# Change datatypes
pop_2001_to_2016['2001'] = pop_2001_to_2016['2001'].apply(lambda x: int(x.replace(',', '')))

convert_dict = {'geographic_code': int, 
                '2006': int,
                '2011': int,
                '2016': int} 
pop_2001_to_2016 = pop_2001_to_2016.astype(convert_dict) 


def recorded_year(year):
    '''
    Take a year as int, return a assigned year as int.
    Since the population census data only available for the year of 2001, 2006,
    2011, and 2016, we decided to assign the population of a city of a given
    year to the nearest available census data. 
    '''
    if 2000 <= year <= 2005:
        return 2001
    elif 2006 <= year <= 2010:
        return 2006
    elif 2011 <= year <= 2015:
        return 2011
    elif 2016 <= year <= 2019:
        return 2016
    else:
        raise RuntimeError(f'Invalid year {year}')


def pop_by_city_prov_year(pops: pd.DataFrame) -> '(str, str, int) -> int':
    '''
    Take a pandas dataframe, return a function.
    The output funciton takes 3 inputs (city as str,
    province as str, year as int) and return the population as int.
    '''
    def lookup(city: str, prov: str,  year: int) -> int:
        year = str(recorded_year(year))
        try:
            singleton_df = pops.loc[(pops['CSD_CD'] == city) & (pops['province_or_territory'] == prov)]
            series = singleton_df.iloc[0]
            population = series[year]
            return population
        except:
            print(f'ERROR: no population found for {(city, prov, year)}')
    return lookup


def set_city_year_pop(pop_f:'(str, str, int) -> int') -> 'pd.Series -> pd.Series':
    '''
    Take a function, return a function.
    The output function takes a pandas series and return a pandas series.
    '''
    def func(s: pd.Series):
        population = pop_f(s['City'], s['Province'], s['Year'])
        new_pop = pd.Series({'Population2': population})
        return s.append(new_pop)
    return func

pop_lookup_func = pop_by_city_prov_year(pop_2001_to_2016)
pop_set_func = set_city_year_pop(pop_lookup_func)

print(permits.apply(pop_set_func, axis=1))
# print(pop_by_city_prov_year(pop_2001_to_2016)('Toronto', 'Ontario', 2001))


    