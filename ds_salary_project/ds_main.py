import scraper as gs
import pandas as pd

path="/Users/sadiatabassum/Documents/DataSciencePortfolio/ds_salary_project/chromedriver"

df=gs.get_jobs('data analyst',200, False, path,15)

df.to_csv('/Users/sadiatabassum/Documents/DataSciencePortfolio/ds_salary_project/glassdoor_data.csv')