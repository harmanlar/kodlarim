# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:15:16 2024

@author: cem.aydemir
"""

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel(r"C:\Users\cem.aydemir\Documents\YAPI VE YAPI İŞLER\CrystalReportViewer1.xls")
df = df[['KODU' , 'PLAKA NO' , 'EKİPMAN ADI' , 'FİRMA' , 'TARİH' , 'YAKIT (Lt)' , 'SAAT' , 'KM' ]]
for i in range (1,9):
    df.drop([(1113 + i)], axis=0, inplace=True)
    
df = df.dropna(subset=['TARİH'])
df.reset_index(drop=True)
df = df.dropna(subset=['YAKIT (Lt)'])
df['TARİH'] = pd.to_datetime(df['TARİH'], format='%Y:%m:%d %H:%M:%S')


df_mak = df[df['EKİPMAN ADI'].str.contains('EKS|EXC|PC|KOMATSU|HITACHI')]
unique_kod = df_mak['KODU'].unique()
unique_kod
kod_list = []
proje_list = []
gunluk_saat_list =[]
for kod in unique_kod:
    df_bul = df_mak.query('KODU == @kod')
    proje = df_bul['FİRMA'].iloc[0]
    ilk_saat = df_bul['SAAT'].min()
    son_saat = df_bul['SAAT'].max()
    saat = son_saat - ilk_saat
    ilk_tarih = df_bul['TARİH'].min()
    son_tarih = df_bul['TARİH'].max()
    fark = son_tarih - ilk_tarih
    fark_saati = fark.total_seconds()/3600
    sayi = fark_saati/24
    gunluk_saat = round(saat / sayi, 2)
    kod_list.append(kod)
    proje_list.append(proje)
    gunluk_saat_list.append(gunluk_saat)
    proje
df_hesap = pd.DataFrame({
    'kod_list': kod_list,
    'proje_list': proje_list,
    'gunluk_saat_list': gunluk_saat_list
})
df_hesap = df_hesap[df_hesap['gunluk_saat_list'] < 24]
df_hesap.loc[(df_hesap['proje_list'] == 'SİNOP')]

df_esk = df_hesap.loc[(df_hesap['proje_list'] == 'ESKİŞEHİR')]
df_bil = df_hesap.loc[(df_hesap['proje_list'] == 'BİLECİK')]
plt.figure(figsize=(15, 6))
plt.bar(df_esk['kod_list'], df_esk['gunluk_saat_list'], color='skyblue')
plt.bar(df_bil['kod_list'], df_bil['gunluk_saat_list'], color='green')
plt.xlabel('Kod')
plt.ylabel('Günlük Saat')
plt.title('Kod ve Günlük Saat')
plt.xticks(rotation=90)
plt.legend(['Eskişehir','Bilecik'], loc='upper left')
plt.show()