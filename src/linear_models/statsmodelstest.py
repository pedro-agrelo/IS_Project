# Importar bibliotecas necesarias
import pandas as pd
import statsmodels.formula.api as sm

df = pd.read_csv('housing.csv')
print(df.head())

regresion = sm.ols('total_bedrooms ~ population - households', data=df) #Crear modelo linear
sol=regresion.fit() #Ajuste

print(sol.summary())
print('R**2 = ', sol.rsquared)
print(sol.params)
