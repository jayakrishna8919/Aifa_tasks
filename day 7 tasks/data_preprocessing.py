import pandas as pd
data_frame=pd.read_csv('customers-1000.csv')
print(df)

print(list(data_frame.columns))            # Program to print all the column name of the dataframe
print(data_frame.describe())
print(data_frame.isnull( ))               
print(data_frame.isnull().sum())

print(data_frame.drop(4).head())           #Removing 4th indexed value from the dataframe

data_frame['college'] = 1                  #Creates a new column with all the values equal to 1
data_frame.head()
print(list(data_frame.columns))
print(data_frame.sort_values(by='First Name', ascending=False).head())
