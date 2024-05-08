import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

df = pd.read_excel(r"C:\Users\cem.aydemir\Documents\PYTHON\Ocak_Nakliye.xlsx")


df['Sayi'] = df['NET']
df = df[['Zaman' , 'Sayi']]
#%%
df['Zaman'] = pd.to_datetime(df['Zaman'], 
                                    format='%H:%M:%S')

df['Zaman'] = (df.Zaman - df.Zaman.dt.normalize()).dt.floor('5T')

df = df.groupby([pd.Grouper(key= 'Zaman', 
                               freq= 'h')])['Sayi'].count().reset_index()
# groupby işleminin sonundaki reset_index() çıktıyı tekrar
# dataframe'e dönmesini sağlıyor. Yoksa dataframe işlemi yapılmıyor.
# Yani dataframe index'inin olması gerekiyor. 

df = df[df['Sayi'] > 0]
print(df.sum())

#%%
df['Zaman'] = pd.Series([pd.Timedelta(hours=i) for i in range(0,24,1)])
df['Zaman'] = df['Zaman'].astype(str).str.split('0 days ').str[-1]
df = df.dropna(axis=0)

pd.options.display.min_rows = 30
print(df)
x =df['Zaman']
y= df['Sayi']
plt.figure(figsize=(15,8))
plt.xticks(rotation= 90)
plt.bar(x,y)
plt.grid(True)
plt.show()


