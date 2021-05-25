import os
import pandas as pd
filename=input("Enter merged file name(without extension):")
filename=filename+=".xlsx"
cwd = os.path.abspath('') 
files = os.listdir(cwd)  
df = pd.DataFrame()
for file in files:
     if file.endswith('.xlsx'):
         df = df.append(pd.read_excel(file), ignore_index=True) 
df.head()
df.to_excel(filename)