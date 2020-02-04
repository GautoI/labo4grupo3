# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:16:50 2020

@author: Publico
"""
import numpy as np
from matplotlib import pyplot as plt

frecuenciaC1 = np.array([50000,50010,50020,50030,50040,50050,50060,50070,50080,50090,50092,50094,50096,50097,50098,50100,50110,50120,50130,50140,50150])
voltajeC1 = np.array([50,52.4,58.6,60.4,68.2,79.2,91.2,118,170,376,500,734,1210,1600,1260,760,200,110,74.4,54,42])
plt.figure(1)
plt.plot(frecuenciaC1, voltajeC1, '.-')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Voltaje Pico a Pico [mV]')
#%%
len(frecuenciaC1)
len(voltajeC1)
#%%

frecuenciaC2=np.array([150100,150110,150120,150130,150140,150150,150160,150162,150164,150166,150168,150170,150180,150190,150200.150210])
voltajeC2=np.array([60.2,63.6,71.6,83.2,106,170,720,912,520,320,228,168.2,70.6,39.6,28.6])

plt.plot(frecuenciaC2, voltajeC2)
#%%
frecuencia = np.append(frecuenciaC1,frecuenciaC2)
voltaje = np.append(voltajeC1,voltajeC2)
plt.plot(frecuencia,voltaje)