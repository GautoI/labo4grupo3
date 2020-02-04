# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 20:52:46 2020

@author: Usuario
"""

import numpy as np
from matplotlib import pyplot as plt

R2 = 10000
R2err = R2*0.05 
#Asumo R2 sin error

Datos = np.loadtxt('CampanaResonancia')

frec = Datos[:, 0]
frecerr = frec*0.03
transf = Datos[:, 3]
transferr = np.sqrt(((Datos[:,1]**2+Datos[:,2]**2)/Datos[:,2]**2)*(0.003/Datos[:,2]))


plt.figure(2)
plt.plot(frec,transf)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Transferencia')
#plt.errorbar(frec, transf, yerr=transferr)
#plt.legend(['Grafico de transferencia'])

ws = frec[np.argmax(transf)]
wserr = frecerr[np.argmax(transf)]
wp = 50296
#wperr = 
#wp determinado a vista, faltaria recopilar campana antiresonancia
#%%
#Determinar wmas y wmenos
#wmas = potencia[np.where(max(potencia)/2)]
#wmenos = potencia[np.where(max(potencia)/2)]

#Si esto falla determinar wmas y wmenos a partir del grafico de potencia
plt.errorbar(frec, potencia,potenciaerr)
plt.legend(['Grafico de potencia'])
wmas =
wmaserr = 
wmenos = 
wmenoserr =
#%%
#Calculo de parametros
Q = ws/(wmas - wmenos)
Qerr = np.sqrt((wserr/(wmas-wmenos))**2+(ws*wmaserr/(wmas-wmenos)**2)**2+(ws*wmenoserr/(wmas-wmenos)**2)**2)

T = max(transf)
Terr = transferr[np.argmax(transf)]

R = (R2/T) - R2
Rerr = (R2*Terr)/(T**2)

L = (Q*R2)/(ws*T)
Lerr = np.sqrt(((R2*Qerr)/(ws*T))**2+((Q*R2*wserr)/(T*ws**2))**2+((Q*R2*Terr)/(ws*T**2))**2)

C = 1/(L*ws**2)
Cerr = np.sqrt((Lerr/(L*ws)**2)**2+(wserr/(L*ws**3))**2)

C2 = 1/((wp**2)*L - (1/C))
C2err =  np.sqrt(((Lerr*wp**2)/((wp**2)*L - (1/C))**2)**2+((Cerr)/(((wp**2)*L - (1/C))**2*C**2)**2)



parametros = [["R","L","C","C2"],[R,L,C,C2],[Rerr,Lerr,Cerr,C2err]]

print(parametros)

