#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
census=pd.read_csv("C:/Users/damodar reddy/Documents/COE1/datasets-main/census.csv")


# In[86]:


census


# # 1.No of Senior Citizen to get added in next X years

# In[19]:


X = 5
senior_voters = census[(census['Age'] < 60) & ((census['Age'] + X) >= 60)]
print(f"Number of Senior Citizens to be added in next {X} years:", len(senior_voters))


# # 2.No of Voters to get added in next X years

# In[18]:


X = 5
new_voters = census[(census['Age'] < 18) & ((census['Age'] + X) >= 18)]
print(f"Number of voters to be added in next {X} years:", len(new_voters))


# # 3.No of Employable Female Citizens who are Widows or Divorced

# In[41]:


employable_females = census[
    (census['Gender'] == 'Female') &
    (census['Marital Status'].isin(['Widowed','Divorced'])) &
    (census['Weeks Worked'] != '0')
]
print("Number of Employable Female Citizens (Widow/Divorced):", len(employable_females))


# # 4.No of Orphans for each category based on Parents Present

# In[47]:


orphans = census['Parents Status'].value_counts()
print(orphans)


# # 5.Pension Amount to be added after x years

# In[69]:


X=5
pension_add = census.loc[(census['Age'] < 60) & (census['Age'] + X >= 60)].shape[0]
pension_add


# # 6.Gender wise Per Capita Income

# In[52]:


gender_pci = census.groupby('Gender')['Income'].sum() / census['Gender'].value_counts()
gender_pci


# # 7.Per Capita Income

# In[54]:


per_capita_income= census['Income'].mean()
print(per_capita_income)


# # 8.Total Tax To Be collected

# In[100]:


tax_collected = census['Income']* 0.1
print(tax_collected.sum())


# # 9.Total Income of different types of Tax Payers

# In[57]:


total_income= census.groupby('Taxfilter status')['Income'].sum()
total_tax


# # 10.Gender wise Total Income Generated

# In[77]:


income= census.groupby('Gender')['Income'].sum()
print(income)


# # 11.Calculate Sex Ratio (Male : Female)

# In[91]:


gender_count = census['Gender'].value_counts()
sex_ratio = gender_count['Male'] / gender_count['Female']
print("Sex Ratio (Male : Female) = {:.2f} : 1".format(sex_ratio))


# # 12.Education Qualification Count based on Employment

# In[78]:


edu_employment = census.groupby(['Education', 'Weeks Worked']).size()
print(edu_employment)


# # 13.Education category-wise gender-wise count

# In[79]:


education_gender= census.groupby(['Education', 'Gender']).size()
print(education_gender)


# # 14.No of widow female candidates

# In[76]:


widow_female = census[
    (census['Gender'] == 'Female') &
    (census['Marital Status'] == 'Widowed')
]['Gender'].value_counts()
print(widow_female)


# # 15.No of children parents category-wise gender-wise

# In[74]:


parent = census.groupby(['Parents Status', 'Gender']).size()
print(parent)


# # 16.Age above 60 citizens and non-citizens

# In[73]:


age= census[census['Age'] > 60].groupby('Citizen Ship').size()
print(age)


# # 17.No of employable widows and divorced

# In[64]:


employable= census[
    (census['Marital Status'].isin(['Widowed','Divorced'])) &
    (census['Weeks Worked'] != '0')
]
print("Number of Employable Citizens (Widow/Divorced):", len(employable))


# # 18.No of non-citizens working %

# In[72]:


non_citizens = census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
percent_working = (non_citizens['Weeks Worked'] > 0).mean() * 100
print(percent_working)


# # 19.Money generated for non-citizens

# In[70]:


non_citizens= census[census['Citizen Ship'] == 'Foreignborn-NotacitizenofUS']
money_generated= non_citizens['Income'].sum()
print(money_generated)


# # 20.Citizens age above 23 having no employment and highest education

# In[94]:


filtered = census[
    (census['Age'] > 23) &
    (census['Weeks Worked'] == 0) &
    (census['Education'] == 'Doctoratedegree(PhDEdD)')
]
filtered[['Age', 'Weeks Worked', 'Education']]

