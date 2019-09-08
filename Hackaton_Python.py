#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 23:10:24 2019

@author: rafaelbarragan
"""

import pandas as pd, numpy as np

# REASIGNEN LAS RUTAS A LAS CORRESPONDIENTES

## Cargo Datasets de entrenamiento y valuacion
dfEval = pd.read_csv(r'/Users/rafaelbarragan/Downloads/DATASET_EVALUACION.txt', encoding = 'latin')
dfTrain = pd.read_csv(r'/Users/rafaelbarragan/Downloads/DATASET_ENTRENAMIENTO.txt', encoding = 'latin', 
                      converters = {'CD_OPE':str})

## Cargo catalogo de clientes y producto
dfDefCat = pd.read_excel(r'/Users/rafaelbarragan/Downloads/Cat_Categorias.xlsx', encoding = 'latin')
dfDefProd = pd.read_excel(r'/Users/rafaelbarragan/Downloads/Cat_clientes_productos.xlsx', encoding = 'latin')

## Contiene toda la transaccionalidad
dfClieProd = pd.read_excel(r'/Users/rafaelbarragan/Downloads/Clientes_productos.xlsx', encoding = 'latin',
                           converters = {'ZIP_CODE':str})

dfZC = pd.read_excel(r'/Users/rafaelbarragan/Downloads/ZC_ST_H_BBVA_2019.xlsx', encoding = 'latin',
                     converters={'ZipCodReg':str,'Estado':str})

## Asigno los nombres a las columnas (se puede realizar desde el archivo pero no lo hice)
dfZC.columns = ['idEstado','Estado']
#dfZC = pd.read_excel(r'/Users/rafaelbarragan/Downloads/ZC_ST_H_BBVA_2019.xlsx', encoding = 'latin', converters={'ZipCodReg':str,'Estado':str})

## Extraigo los primeros dos digitos del codigo postal para determinar el estado al que pertenece
dfClieProd['idEstado'] = dfClieProd['ZIP_CODE'].str[:2]

## Uno los resultados, para crear un solo dataframe hasta el momento de
dfZCClie = pd.merge(dfClieProd, dfZC, on = 'idEstado')

## Concateno para crear la llave que se unira con el catalog de las categorias.
dfTrain['COD_TRNFIMS'] = dfTrain['CD_TRX']+dfTrain['CD_OPE']

## Uno los dataframe del tipo de operacion
dfClientes = pd.merge(dfDefCat, dfTrain, on = 'COD_TRNFIMS')

## Diccionario de mapeo de valores
mapSIGNO = {'+':1, '-':0}

## Reasigno los valores de entrada y salida de las operaciones
dfClientes.loc[:,'idSIGNO'] = dfClientes.loc[:,'SIGNO'].map(mapSIGNO)

## Identifico que tipo de cuenta es

## Debido a que asignamos valores de 1 y 0 utilizamos el promedio para identificar si pertenece a
## ambos tipos de transaccionalidad.
dfTipCta = dfClientes.groupby(['CUENTA'], as_index = False).agg({'idSIGNO':'mean'})
## Para reclasificar si es de ambos tipos todo aquello que no sea 1 o 0 se clasifica como transaccionable
## 1 Pagos : 0 Cobros
dfTipCta.loc[(dfTipCta['idSIGNO']>0) & (dfTipCta['idSIGNO']<1), 'idSIGNO'] = 2


#######################################################
####################### PRUEBAS #######################
#######################################################  


## Pivoteo la informacion
UnPivotClien = dfClieProd.melt(id_vars = ['CLIENTE','GRUPO','ALTA_CLIENTE','FH_NACIMIENTO','SEGMENTO','CD_GIRO','ZIP_CODE','NB_ACTIVIDAD'], var_name = 'TipoProd', value_name= 'PromMont')

UnPivotClien = dfClieProd.loc[:,['CLIENTE','GRUPO','ALTA_CLIENTE','FH_NACIMIENTO','SEGMENTO','CD_GIRO','ZIP_CODE','NB_ACTIVIDAD','AP25',	'AP26',	'AP27',	'AP28',	'AP29',	'AP30',	'AP31',	'AP32',	'AP33',	'AP34',	'AP35',	'AP36',	'CV25',	'CV26',	'CV27',	'CV28',	'CV29',	'CV30',	'CV31',	'CV32',	'CV33',	'CV34',	'CV35',	'CV36',	'CX25',	'CX26',	'CX27',	'CX28',	'CX29',	'CX30',	'CX31',	'CX32',	'CX33',	'CX34',	'CX35',	'CX36',	'PP25',	'PP26',	'PP27',	'PP28',	'PP29',	'PP30',	'PP31',	'PP32',	'PP33',	'PP34',	'PP35',	'PP36',	'CT25',	'CT26',	'CT27',	'CT28',	'CT29',	'CT30',	'CT31',	'CT32',	'CT33',	'CT34',	'CT35',	'CT36',	'PE25',	'PE26',	'PE27',	'PE28',	'PE29',	'PE30',	'PE31',	'PE32',	'PE33',	'PE34',	'PE35',	'PE36',	'VE25',	'VE26',	'VE27',	'VE28',	'VE29',	'VE30',	'VE31',	'VE32',	'VE33',	'VE34',	'VE35',	'VE36',	'SI25',	'SI26',	'SI27',	'SI28',	'SI29',	'SI30',	'SI31',	'SI32',	'SI33',	'SI34',	'SI35',	'SI36',	'PN25',	'PN26',	'PN27',	'PN28',	'PN29',	'PN30',	'PN31',	'PN32',	'PN33',	'PN34',	'PN35',	'PN36',	'VN25',	'VN26',	'VN27',	'VN28',	'VN29',	'VN30',	'VN31',	'VN32',	'VN33',	'VN34',	'VN35',	'VN36']].melt(id_vars = ['CLIENTE','GRUPO','ALTA_CLIENTE','FH_NACIMIENTO','SEGMENTO','CD_GIRO','ZIP_CODE','NB_ACTIVIDAD'], var_name = 'TipoProd', value_name= 'PromMont')

#xx = dfClientes.iloc[:10,:1].head()

xx = dfTrain.head(5000)
xx['CodSIGNO'] = xx.loc[:, 'SIGNO'].map(mapSIGNO)
#xx['TipoCuenta'] = xx['CUENTA'] + xx['MONEDA']
#len(xx.TipoCuenta.unique())
#len(xx.CUENTA.unique())
tmpDF = xx.groupby(['CUENTA'], as_index = False).agg({'CodSIGNO':'mean'})
tmpDF.loc[(tmpDF['CodSIGNO']>0) & (tmpDF['CodSIGNO']<1), 'CodSIGNO'] = 2


for idx, i in tmpDF.iterrows():
    print(idx, i)


Cta = xx['CUENTA'].values
Sgn = xx['CodSIGNO'].values

dicN = dict(zip(Cta, Sgn))

#a = np.unique(xx[['CUENTA','MONEDA']].values)

TipoCuenta = xx.groupby(['CUENTA','SIGNO']).count() 
#TipoCuenta2 = xx['CUENTA','SIGNO'].groupby(['CUENTA','SIGNO']).count()

IdxTipCta = []
tempVal = ''

idxV = TipoCuenta.index.values

idxV = list(idxV)
aux = ''
diccionario = {}

for i in range(0,len(idxV)):
    if aux == idxV[i][0]:
        print(idxV[i][0], aux)
        diccionario[aux] = 2
    else:
        if idxV[i][1] == '+':
            diccionario[aux] = 1
        else:
            diccionario[aux] = 0
    aux = idxV[i][0]
    
for idx in range(0,len(idxV)-1100):
#    print(idx)
    a = idx
    if idxV[idx] == idxV[idx-1]:
        print(idxV[idx][0], idxV[idx][1])

    print(idx, '   ' , i)
    

for idx, i in TipoCuenta['TipoCuenta'].iteritems():
    print(TipoCuenta[idx])
    IdxTipCta.append(TipoCuenta[idx][0])
    
#    tempVal = idx
#    if tempVal == idx:
#        IdxTipCta.append(idx,3)
#    elif 

dd = TipoCuenta.index.values

for i in len(TipoCuenta):
    if TipoCuenta.iloc[i,:] == TipoCuenta.iloc[i+1,:]:
        IdxTipCta.append[TipoCuenta.iloc[i,:]]

aaaa = TipoCuenta.groupby('FH_OPERACION').count()

#TipoCuenta = xx.groupby(['CUENTA','COD_TRNFIMS','MONEDA','SIGNO']).count() 

UnPivotClien.groupby('CLIENTE')['PromMont'].sum()

#### Seccion de pruebas
#dfTrain.head()
#
#dfEval.head(10)
#
### Numero de fechas unicas
#dfEval.FH_OPERACION.unique()
### Tipo de entrada o salida
#dfEval.SIGNO.unique()
#
##dfClientes.groupby(['Estado']).
### Promedio de region y giro
#promGP = dfClieProd[['ZIP_CODE','AP25','AP26']].groupby(['ZIP_CODE']).mean()
#
#a = dfTrain.head(50)