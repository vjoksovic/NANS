import pandas as pd
from sklearn.model_selection import train_test_split
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

statistika_sutevi=pd.merge(statistika_test,sutevi_test, on=["naziv_kluba", "naziv_protivnika"])
dodavanja_predikcije=pd.merge(dodavanja_test,predikcije_test, on=["naziv_kluba", "naziv_protivnika"])
test=pd.merge(statistika_sutevi,dodavanja_predikcije, on=["naziv_kluba", "naziv_protivnika"])


data=data.drop(columns=['naziv_kluba', 'naziv_protivnika',"domaci_teren","procenat_pobeda",
                        "procenat_poraza","posed_lopte","procenat_remija","progresivna_dodavanja",
                        "procenat_preciznosti_dodavanja", "kvota_remi", "kljucna_dodavanja", "primljeni_golovi"])


data=remove_outliers(data,1.6)

x = data.drop(columns=['postignuti_golovi'])
y = data['postignuti_golovi']


#perfect_collinearity_assumption(data)  

model=get_fitted_model(x,y)
#print(model.summary())


x_train, x_val, y_train, y_val = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=42)

train_model = get_fitted_model(x_train,y_train)
x1_train=sm.add_constant(x_train)


print(f"assumtions_satisfied: {are_assumptions_satisfied(train_model, x_train, y_train)} \n")

val_rmse = get_rmse(train_model, x_val, y_val)
print(f'validation rmse result: {val_rmse}')
val_radj = get_rsquared_adj(train_model, x_val, y_val)
print(f'validation rsquared_adj result: {val_radj} \n')

y_val_pred = train_model.predict(sm.add_constant(x_val))


test=test.drop(columns=['naziv_kluba', 'naziv_protivnika',"domaci_teren","procenat_pobeda",
                        "procenat_poraza","posed_lopte","procenat_remija","progresivna_dodavanja", 
                        "procenat_preciznosti_dodavanja", "kvota_remi", "kljucna_dodavanja", "primljeni_golovi"])


x_test = test.drop(columns=['postignuti_golovi'])
y_test = test['postignuti_golovi']

test_rmse = get_rmse(train_model, x_test, y_test)
print(f'test rmse result: {test_rmse}')
test_radj = get_rsquared_adj(train_model, x_test, y_test)
print(f'test rsquared_adj result: {test_radj}')






