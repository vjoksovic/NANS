import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from functions import *

dodavanja_data=pd.read_csv("data\dodavanja.csv")
sutevi_data=pd.read_csv("data\sutevi.csv")
statistika_data=pd.read_csv("data\statistika.csv")
predikcije_data=pd.read_csv("data\predikcije.csv")

statistika_sutevi=pd.merge(statistika_data,sutevi_data, on=["naziv_kluba", "naziv_protivnika"])
dodavanja_predikcije=pd.merge(dodavanja_data,predikcije_data, on=["naziv_kluba", "naziv_protivnika"])
data=pd.merge(statistika_sutevi,dodavanja_predikcije, on=["naziv_kluba", "naziv_protivnika"])

dodavanja_test=pd.read_csv("test\dodavanja.csv")
sutevi_test=pd.read_csv("test\sutevi.csv")
statistika_test=pd.read_csv("test\statistika.csv")
predikcije_test=pd.read_csv("test\predikcije.csv")

statistika_sutevi1=pd.merge(statistika_test,sutevi_test, on=["naziv_kluba", "naziv_protivnika"])
dodavanja_predikcije1=pd.merge(dodavanja_test,predikcije_test, on=["naziv_kluba", "naziv_protivnika"])
test=pd.merge(statistika_sutevi1,dodavanja_predikcije1, on=["naziv_kluba", "naziv_protivnika"])


data=data.drop(columns=['naziv_kluba', 'naziv_protivnika', "broj_penala",
                        "domaci_teren","primljeni_golovi","procenat_pobeda",
                        "progresivna_dodavanja","procenat_remija","kljucna_dodavanja",
                        "sutevi_na_gol","kvota_remi","kvota_pobeda","posed_lopte",
                        "broj_dodavanja"])
                 

#data=remove_outliers(data,1.6)

x = data.drop(columns=['postignuti_golovi'])
y = data['postignuti_golovi']


x_train, x_val, y_train, y_val = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=42)

train_model = RandomForestRegressor(n_estimators=500, random_state=42) 
train_model.fit(x_train, y_train)

feature_importances = train_model.feature_importances_
feature_names = x_train.columns 

feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
#print(feature_importance_df)

val_rmse = get_rmse_rf(train_model, x_val, y_val)
print(f'validation rmse result: {val_rmse}')
val_radj = get_rsquared_adj_rf(train_model, x_val, y_val)
print(f'validation rsquared_adj result: {val_radj} \n')


test=test.drop(columns=['naziv_kluba', 'naziv_protivnika', "broj_penala",
                        "domaci_teren","primljeni_golovi","procenat_pobeda",
                        "progresivna_dodavanja","procenat_remija","kljucna_dodavanja",
                        "sutevi_na_gol","kvota_remi","kvota_pobeda","posed_lopte",
                        "broj_dodavanja"])

x_test = test.drop(columns=['postignuti_golovi'])
y_test = test['postignuti_golovi']

test_rmse = get_rmse_rf(train_model, x_test, y_test)
print(f'test rmse result: {test_rmse}')
test_radj = get_rsquared_adj_rf(train_model, x_test, y_test)
print(f'test rsquared_adj result: {test_radj} \n')