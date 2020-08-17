#!/usr/bin/env python
# coding: utf-8

# # Import Libraries

# In[1]:


import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
from bs4 import BeautifulSoup # package to transform the data of webpage into pandas dataframe
import requests # library to handle requests


# # Retreive Wikipedia data and place into the Dataframe

# In[2]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
content = BeautifulSoup(requests.get(url).content, 'lxml')


# In[4]:


# obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe
table = content.find('table')
td = table.find_all('td')
postcode = []
borough = []
neighbourhood = []

for i in range(0, len(td), 3):
    postcode.append(td[i].text.strip())
    borough.append(td[i+1].text.strip())
    neighbourhood.append(td[i+2].text.strip())
    
# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood        
wiki_df = pd.DataFrame(data=[postcode, borough, neighbourhood]).transpose()
wiki_df.columns = ['Postal Code', 'Borough', 'Neighborhood']

# Ignore cells with a borough that is Not assigned.
wiki_df['Borough'].replace('Not assigned', np.nan, inplace=True)
wiki_df.dropna(subset=['Borough'], inplace=True)

# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. 
wiki_df['Neighborhood'].replace('Not assigned', "Queen's Park", inplace=True)

# More than one neighborhood can exist in one postal code area. 
# These two rows will be combined into one row with the neighborhoods separated with a comma.
wiki_df = wiki_df.groupby(['Postal Code', 'Borough'])['Neighborhood'].apply(', '.join).reset_index()
wiki_df.columns = ['Postal Code', 'Borough', 'Neighborhood']
wiki_df.head(12)


# In[5]:


wiki_df.shape


# In[18]:


url="http://cocl.us/Geospatial_data"
geospatial_df = pd.read_csv(url)
geospatial_df.columns = ['Postal Code', 'Latitude', 'Longitude']
toronto_metro_df = pd.merge(wiki_df, geospatial_df, on=['Postal Code'], how='inner')
toronto_metro_df .head()


# In[7]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(toronto_metro_df ['Borough'].unique()),
        toronto_metro_df .shape[0]
    )
)

