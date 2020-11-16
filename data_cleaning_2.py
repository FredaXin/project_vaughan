import numpy as np
import pandas as pd

import os


permits = pd.read_csv('~/Desktop/Processed_Data.csv')
permits.head()


census_2006_2001 = pd.read_csv('~/projects/project_vaughan/census_data/census_2006_2001.csv')
census_2011_2006 = pd.read_csv('~/projects/project_vaughan/census_data/census_2011_2006.csv', encoding='latin-1')
census_2016_2011 = pd.read_csv('~/projects/project_vaughan/census_data/census_2016_2011.csv', encoding='latin-1')


pop_2011_2006 = census_2011_2006[['Geographic name', 'Population, 2011', 'Population, 2006']]
pop_2016_2011 = census_2016_2011[['Geographic name', 'Population, 2016', 'Population, 2011']]

print(census_2006_2001.tail())