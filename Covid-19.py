#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from datetime import datetime


# In[3]:


raw_confirmed = pd.read_csv('Desktop/Cor_Confirmed.csv')


# In[4]:


raw_Deaths = pd.read_csv('Desktop/Cor_Deaths.csv')


# In[5]:


raw_recovered = pd.read_csv('Desktop/Cor_Recovered.csv')


# In[9]:


raw_recovered.head()


# In[10]:


print("The Shape of Cornirmed is: ", raw_confirmed.shape)
print("The Shape of Cornirmed is: ", raw_Deaths.shape)
print("The Shape of Cornirmed is: ", raw_recovered.shape)


# In[14]:


# Un-Pivoting the data

raw_confirmed2 = pd.melt(raw_confirmed, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name=['Date'])
raw_deaths2 = pd.melt(raw_Deaths, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name=['Date'])
raw_Recovered2 = pd.melt(raw_recovered, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name=['Date'])

print("The Shape of Cornirmed is: ", raw_confirmed2.shape)
print("The Shape of Cornirmed is: ", raw_deaths2.shape)
print("The Shape of Cornirmed is: ", raw_Recovered2.shape)


# In[15]:


# Converting the new column to dates

raw_confirmed2['Date'] = pd.to_datetime(raw_confirmed2['Date'])
raw_deaths2['Date'] = pd.to_datetime(raw_deaths2['Date'])
raw_Recovered2['Date'] = pd.to_datetime(raw_Recovered2['Date'])


# In[16]:


# Renaming the Values
raw_confirmed2.columns = raw_confirmed2.columns.str.replace('value', 'Confirmed')
raw_deaths2.columns = raw_deaths2.columns.str.replace('value', 'Deaths')
raw_Recovered2.columns = raw_Recovered2.columns.str.replace('value', 'Recovered')


# In[17]:


# Investigating the NULL values
raw_confirmed2.isnull().sum()


# In[18]:


# Dealing with NULL values

raw_confirmed2['Province/State'].fillna(raw_confirmed2['Country/Region'], inplace=True)
raw_deaths2['Province/State'].fillna(raw_confirmed2['Country/Region'], inplace=True)
raw_Recovered2['Province/State'].fillna(raw_confirmed2['Country/Region'], inplace=True)

raw_confirmed2.isnull().sum()


# In[19]:


# printing shapes before the join
print("The Shape of Cornirmed is: ", raw_confirmed2.shape)
print("The Shape of Cornirmed is: ", raw_deaths2.shape)
print("The Shape of Cornirmed is: ", raw_Recovered2.shape)


# In[20]:


# Full Joins

# Confirmed with Deaths
full_join = raw_confirmed2.merge(raw_deaths2[['Province/State','Country/Region','Date','Deaths']], 
                                      how = 'outer', 
                                      left_on = ['Province/State','Country/Region','Date'], 
                                      right_on = ['Province/State', 'Country/Region','Date'])

print("Shape of first join: ", full_join.shape)

# full join with Recovered
full_join = full_join.merge(raw_Recovered2[['Province/State','Country/Region','Date','Recovered']], 
                                      how = 'outer', 
                                      left_on = ['Province/State','Country/Region','Date'], 
                                      right_on = ['Province/State', 'Country/Region','Date'])

print("Shape of second join: ", full_join.shape)

full_join.head()


# In[21]:


# checking for null values (especially long and lat)
full_join.isnull().sum()


# In[22]:


# Adding Month and Year as a new Column
full_join['Month-Year'] = full_join['Date'].dt.strftime('%b-%Y')


# In[23]:


full_join.head()


# In[24]:


#############################################################################################
######################## Braking the numbers by Day #########################################
#############################################################################################

# filtering data to Anhui to give you an example

#creating a new df    
test = full_join[full_join['Province/State'] == 'Anhui']

#creating a new df    
full_join2 = test.copy()

#creating a new date columns - 1
full_join2['Date - 1'] = full_join2['Date'] + pd.Timedelta(days=1)
full_join2.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1',
                          'Date': 'Date Minus 1'}, inplace=True)

#Joing on the 2 DFs
full_join3 = test.merge(full_join2[['Province/State', 'Country/Region','Confirmed - 1', 'Deaths - 1', 
                            'Recovered - 1', 'Date - 1', 'Date Minus 1']], how = 'outer',
                             left_on = ['Province/State','Country/Region','Date'], 
                             right_on = ['Province/State', 'Country/Region','Date - 1'])

# Additional Calculations
full_join3['Confirmed Daily'] = full_join3['Confirmed'] - full_join3['Confirmed - 1']


test.head()
full_join2.head()
full_join3.head()


# In[25]:


test.head()


# In[26]:


#############################################################################################
######################## Braking the numbers by Day #########################################
#############################################################################################

## Applying it on all dataset

#creating a new df    
full_join2 = full_join.copy()

#creating a new date columns - 1
full_join2['Date - 1'] = full_join2['Date'] + pd.Timedelta(days=1)
full_join2.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1',
                          'Date': 'Date Minus 1'}, inplace=True)

#Joing on the 2 DFs
full_join3 = full_join.merge(full_join2[['Province/State', 'Country/Region','Confirmed - 1', 'Deaths - 1', 
                            'Recovered - 1', 'Date - 1', 'Date Minus 1']], how = 'left',
                             left_on = ['Province/State','Country/Region','Date'], 
                             right_on = ['Province/State', 'Country/Region','Date - 1'])

#minus_onedf.rename(columns={'Confirmed': 'Confirmed - 1', 'Deaths': 'Deaths - 1', 'Recovered': 'Recovered - 1'}, inplace=True)

full_join3.head()

# Additional Calculations
full_join3['Confirmed Daily'] = full_join3['Confirmed'] - full_join3['Confirmed - 1']
full_join3['Deaths Daily'] = full_join3['Deaths'] - full_join3['Deaths - 1']
full_join3['Recovered Daily'] = full_join3['Recovered'] - full_join3['Recovered - 1']

print(full_join3.shape)


# In[27]:


full_join3.head()


# In[28]:


# Additing manually the numbers for first day

full_join3['Confirmed Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Confirmed']
full_join3['Deaths Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Deaths']
full_join3['Recovered Daily'].loc[full_join3['Date'] == '2020-01-22'] = full_join3['Recovered']

# deleting columns
del full_join3['Confirmed - 1']
del full_join3['Deaths - 1']
del full_join3['Recovered - 1']
del full_join3['Date - 1']
del full_join3['Date Minus 1']


# In[29]:


full_join3.head()


# In[31]:


# Exporting the data

# Setting my path
path = "C:\\Users\\User\\Desktop\\CoronaVirus"
full_join3.to_csv('CoronaVirus PowerBI Raw', sep='\t')


# In[32]:


full_join3.head()


# In[33]:


# puting unique values in list
dates = full_join3['Date'].unique()

#creating a df with unique
dates = pd.DataFrame(dates, columns=['Date'])

# Ordering df
dates = dates.sort_values(by=['Date'])

# Creating an ordered list now
dates = full_join3['Date'].unique()

print(full_join3.shape)

try:
    del concat_data
except:
    print()
    
try:
    del final_concat_data
except:
    print()
    

for i in dates:
    new_data = full_join3[full_join3['Date'] == i]
    new_data['Cumulative Date'] = i
    print(i)
    
    try:     
        concat_data = pd.concat([concat_data, new_data], ignore_index = True)
        concat_data['Cumulative Date 2'] = i
        print(concat_data['Date'].unique())
        
        try:
            final_concat_data = pd.concat([final_concat_data, concat_data], ignore_index = True)
        except:
            final_concat_data = concat_data

    except:
        concat_data = new_data
        
print(final_concat_data.shape)


# In[34]:


# Exporting the data

final_concat_data.to_csv('CoronaVirus PowerBI Raw - Cumulative Test', sep='\t')


# In[ ]:




