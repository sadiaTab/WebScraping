import pandas as pd

import numpy as np
import re

df=pd.read_csv('glassdoor_data.csv')
df=df[df['Salary Estimate']!='-1']

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'Employer est.' in x.lower() else 0)
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0].replace('K','').replace('$',''))
# salary=minusk.apply(lambda x: x.replace('Per Hour','').replace('Employer est.',''))

# Extract minimum and maximum salary from "Salary Estimate" column
def extract_min_salary(salary):
    try:
        split_values = salary.split('-')
        if len(split_values) >= 2:
            return float(split_values[0].strip().lstrip('$').rstrip('K').rstrip(' per hour'))
    except:
        pass
    return None

def extract_max_salary(salary):
    try:
        split_values = salary.split('-')
        if len(split_values) >= 2:
            return float(split_values[1].split('(')[0].strip().lstrip('$').rstrip('K').rstrip(' per hour'))
    except:
        pass
    return None

df['Min Salary'] = salary.apply(extract_min_salary)
df['Max Salary'] = salary.apply(extract_max_salary)
df['Rating'] = df['Rating'].apply(lambda x: x.split(' ')[0])
# df['Company Name'] = df['Company Name'].apply(lambda x: x.split(' ')[0])

def remove_numerical_part(value):
    value = re.sub(r'\d+', '', value)  # Remove numerical part
    value = re.sub(r'[^\w\s]', '', value)  # Remove special characters
    return value.strip()  # Remove leading and trailing whitespaces


df['Company Name'] = df['Company Name'].apply(remove_numerical_part)

def extract_jobstate(location):
    splitval = location.split(',')
    if len(splitval)>=2:
        return (splitval[1])

df['job_state'] = df['Location'].apply(extract_jobstate)

# df.job_state.value_counts()

df['age']=df['Founded'].apply(lambda x: x if x<1 else (2023-int(x)))

df['python']=df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

df['excel']=df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df['sql']=df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

df.sql.value_counts()

def extract_company(ownership):
    splitval=ownership.split('-')
    if len(splitval)>1:
        return splitval[1]
df['Type of ownership']=df['Type of ownership'].apply(extract_company)

# df.columns
df_out = df.drop(['Unnamed: 0','Headquarters','Competitors'], axis =1)

df_out.to_csv('data_cleaned.csv',index=False)

