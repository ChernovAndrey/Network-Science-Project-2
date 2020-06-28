#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pycountry
import plotly.express as px
import pandas as pd


# In[2]:


# ----------- Step 1 ------------
URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df1 = pd.read_csv(URL_DATASET)
# print(df1.head) # Uncomment to see what the dataframe is like
# ----------- Step 2 ------------
list_countries = df1['Country'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

# print(d_country_code) # Uncomment to check dictionary  

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v

# print(df1.head)  # Uncomment to confirm that ISO codes added


# In[3]:


# ----------- Step 3 ------------
fig = px.choropleth(data_frame = df1,
                    locations= "iso_alpha",
                    color= "Confirmed",  # value in column 'Confirmed' determines color
                    hover_name= "Country",
                    color_continuous_scale= 'aggrnyl',  #  color scale red, yellow green
                    animation_frame= "Date",
                    width=800, height=400,
                   )
fig.show()


# In[4]:


df = pd.read_csv('confirmed.csv')


# In[5]:


iso_alpha = []
for i in df.Country:
    l = list(set(df1[df1['Country'] == i]['iso_alpha']))
    str1 = ''.join(l)
    iso_alpha.append(str1)


# In[6]:


df['iso_alpha'] = iso_alpha


# In[7]:


new_df = df.iloc[:, 11:]
new_df['Country'] = df['Country']
new_df.head(3)


# In[8]:


map_list = []
for date in new_df.columns[:-2]:
    for i in range(len(new_df)):
        l = [date, new_df.iloc[i, :][date], new_df.iloc[i, :]['Country'], new_df.iloc[i, :]['iso_alpha']]
        map_list.append(l)


# In[9]:


map_df = pd.DataFrame(map_list, columns=['date', 'confirmed', 'country', 'iso_alpha'])


# In[10]:


map_df['iso_alpha'][map_df.country == 'United States'] = 'USA'


# In[41]:


map_df['iso_alpha'][map_df.country == 'South Korea'] = 'KOR'


# In[45]:


map_df['iso_alpha'][map_df.country == 'Taiwan'] = 'TWN'


# In[49]:


map_df['iso_alpha'][map_df.country == 'Democratic Republic of the Congo'] = 'COD'


# In[50]:


map_df['iso_alpha'][map_df.country == 'Republic of the Congo'] = 'COG'


# In[51]:


new_map_df = map_df.iloc[13160:, :]


# In[52]:


fig = px.choropleth(data_frame = new_map_df,
                    locations= "iso_alpha",
                    color= "confirmed",  # value in column 'Confirmed' determines color
                    hover_name= "country",
                    color_continuous_scale= 'OrRd',  #  color scale red, yellow green
                    animation_frame= "date",
                   )
fig.show()


# In[ ]:




