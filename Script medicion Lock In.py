# -*- coding: utf-8 -*-
"""
LOCKIN Tektronix SR830
Manual (web): http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual (local): \\Srvlabos\manuales\Standford\SR830m.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import
import time

import numpy as np
import pyvisa as visa
import matplotlib.pyplot as plt


rm = visa.ResourceManager()


# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB0::8::INSTR'

lockin = rm.open_resource(resource_name)

# Pide indentificacion
print(lockin.query('*IDN?'))

# Lee las salidas una a la vez
# X=1, Y=2, R=3, T=4
x = lockin.query_ascii_values('OUTP ?1')
y = lockin.query_ascii_values('OUTP ?2')
r = lockin.query_ascii_values('OUTP ?3')
t = lockin.query_ascii_values('OUTP ?4')

print(x, y, r, t)

# O bien todas juntas
xyrt = lockin.query_ascii_values('SNAP ? 1,2,3,4')

print(xyrt)

# Cambia el voltaje en la salida auxiliar
# El primer numero es la salida y el segundo es el voltaje
#lockin.write('AUXV 0, 4.32')


#%%
#generador de funciones

resource_name2= 'USB0::0x0699::0x0346::C036493::INSTR'
fungen = rm.open_resource(resource_name2)
print(fungen.query('*IDN?'))

#%%
pausa = 1
freqs = np.linspace(50275,50295,400)

def medir(frecuencias):
    Amplitud=[]
    fase=[]
    frecs=[]
    for freq in frecuencias:
        fungen.write('FREQ %f' % freq)
        time.sleep(0.1)
        r = lockin.query_ascii_values('OUTP ?3')[0]
        t = lockin.query_ascii_values('OUTP ?4')[0]
        Amplitud.append(r)
        fase.append(t)
        frecs.append(freq)
        time.sleep(0.1)
    return frecs,Amplitud,fase
   


MedicionE1_list=medir(freqs)
MedicionE1 = np.asarray(MedicionE1_list)
#MedicionE2=medir(freqs)
# MedicionE3=medir(freqs)
# MedicionE4=medir(freqs)
# MedicionE5=medir(freqs)
# MedicionE6=medir(freqs)
# MedicionE7=medir(freqs)
# MedicionE8=medir(freqs)
# MedicionE9=medir(freqs)
# MedicionE10=medir(freqs)
#Max=max(Medicion1[0])

#Data = np.append([MedicionE1, MedicionE2, MedicionE3,])
np.savetxt('CampanaAntiResonanciaLiVentrada3', MedicionE1)

#%% 
# plt.figure()
# plt.errorbar(freqs,MedicionE1[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE2[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE3[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE4[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE5[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE6[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE7[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE8[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE9[0],fmt='o',yerr=std)
# plt.errorbar(freqs,MedicionE10[0],fmt="o",yerr=std)
# plt.grid(True)
# plt.show()
 
 
 #%% calculo errores voltaje
M = np.array([MedicionE1[0],MedicionE2[0],MedicionE3[0],MedicionE4[0],MedicionE5[0],MedicionE6[0],MedicionE7[0],MedicionE8[0],MedicionE9[0],MedicionE10[0]])
Mean = np.mean(M,0)
std = np.std(M,0)

plt.figure()
plt.errorbar(freqs, Mean, yerr=std)
plt.grid(True)
plt.show()

#%%

frecuencia = MedicionE1[0]
V2 = MedicionE1[1]
V1 = 1/np.sqrt(2)
transf = V2/V1
ws = frecuencia[np.argmax(transf)]
plt.figure
plt.plot(frecuencia,transf)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Transferencia')
#%%

DatoEntrada = np.loadtxt('CampanaResonanciaLiVentrada3')
DatoSalida = np.loadtxt('CampanaResonanciaLiVsalida3')

frecuencia = DatoEntrada[0]
V1 = DatoEntrada[2]

V2 = DatoSalida[2]

transf = V2/V1
ws = frecuencia[np.argmax(transf)]

plt.figure()
plt.plot(frecuencia,transf)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Transferencia')
#%%
DatoEntrada = np.loadtxt('CampanaAntiResonanciaLiVentrada3')
DatoSalida = np.loadtxt('CampanaAntiResonanciaLiVsalida3')

frecuencia = DatoEntrada[0]
V1 = DatoEntrada[2]

V2 = DatoSalida[2]

transf = V2/V1
wp = frecuencia[np.argmin(transf)]

plt.figure()
plt.plot(frecuencia,transf)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Transferencia')

#%%
#Parametros
R2 = 10000
R2err = R2*0.05 


Q = ws/(wmas - wmenos)
#Qerr = np.sqrt((wserr/(wmas-wmenos))**2+(ws*wmaserr/(wmas-wmenos)**2)**2+(ws*wmenoserr/(wmas-wmenos)**2)**2)

T = max(transf)
#Terr = transferr[np.argmax(transf)]

R = (R2/T) - R2
#Rerr = (R2*Terr)/(T**2)

L = (Q*R2)/(ws*T)
#Lerr = np.sqrt(((R2*Qerr)/(ws*T))**2+((Q*R2*wserr)/(T*ws**2))**2+((Q*R2*Terr)/(ws*T**2))**2)

C = 1/(L*ws**2)
#Cerr = np.sqrt((Lerr/(L*ws)**2)**2+(wserr/(L*ws**3))**2)

C2 = 1/((wp**2)*L - (1/C))
#C2err =  np.sqrt(((Lerr*wp**2)/((wp**2)*L - (1/C))**2)**2+((Cerr)/(((wp**2)*L - (1/C))**2*C**2)**2)