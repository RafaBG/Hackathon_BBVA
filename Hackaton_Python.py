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