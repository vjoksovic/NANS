import pandas as pd
from functions import *

dodavanja_data=pd.read_csv("data\dodavanja.csv")
sutevi_data=pd.read_csv("data\sutevi.csv")
statistika_data=pd.read_csv("data\statistika.csv")
predikcije_data=pd.read_csv("data\predikcije.csv")

statistika_sutevi=pd.merge(statistika_data,sutevi_data, on=["naziv_kluba", "naziv_protivnika"])
dodavanja_predikcije=pd.merge(dodavanja_data,predikcije_data, on=["naziv_kluba", "naziv_protivnika"])
data=pd.merge(statistika_sutevi,dodavanja_predikcije, on=["naziv_kluba", "naziv_protivnika"])

x = data['sutevi_u_okvir_gola']
y = data['postignuti_golovi']

model=get_fitted_model(x,y)
#print(model.summary())


alpha=0.05
sutevi = int(input("Unesite broj suteva u okvir gola: "))
const_sutevi = sm.add_constant([0, sutevi])
pred_intervals = model.get_prediction(const_sutevi).summary_frame(alpha)

mean_y_pred = pred_intervals['mean'][1] 
low_y_pred = pred_intervals['obs_ci_lower'][1] 
high_y_pred = pred_intervals['obs_ci_upper'][1] 

print(f"Minimalni broj golova: {int(low_y_pred)}")
print(f"Predviđeni broj golova: {int(mean_y_pred)}")
print(f"Maksimlni broj golova: {int(high_y_pred)}")









