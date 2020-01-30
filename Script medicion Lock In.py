# -*- coding: utf-8 -*-
"""
LOCKIN Tektronix SR830
Manual (web): http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual (local): \\Srvlabos\manuales\Standford\SR830m.pdf
"""

from __future__ import division, unicode_literals, print_function, absolute_import
import time

import numpy as np
import visa
import matplotlib.pyplot as plt
rm = visa.ResourceManager()

print(__doc__)

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.
resource_name = 'GPIB0::11::INSTR'

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
lockin.write('AUXV 0, 4.32')


#%%
#generador de funciones

resource_name2= 'USB0::0x0699::0x0346::C034166::INSTR'
fungen = rm.open_resource(resource_name2)
print(fungen.query('*IDN?'))

freqs = np.linspace(49500,50500,800)

for freq in freqs:
    fungen.write('FREQ %f' % freq)
    time.sleep(0.3)
#%%
def medir(frecuencias):
    Amplitud=[]
    fase=[]
    for freq in frecuencias:
        fungen.write('FREQ %f' % freq)
        r = lockin.query_ascii_values('OUTP ?3')
        t = lockin.query_ascii_values('OUTP ?4')
        Amplitud.append(r)
        fase.append(t)
        time.sleep(0.1)
    return Amplitud,fase
   
MedicionE1=medir(freqs)    
MedicionE2=medir(freqs)
MedicionE3=medir(freqs)
MedicionE4=medir(freqs)
MedicionE5=medir(freqs)
MedicionE6=medir(freqs)
MedicionE7=medir(freqs)
MedicionE8=medir(freqs)
MedicionE9=medir(freqs)
MedicionE10=medir(freqs)
 Max=max(Medicion1[0])
 
 plt.figure()
 plt.errorbar(freqs,MedicionE1[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE2[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE3[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE4[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE5[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE6[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE7[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE8[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE9[0],fmt='o',yerr=std)
 plt.errorbar(freqs,MedicionE10[0],fmt="o",yerr=std)
 plt.grid(True)
 plt.show()
 
 
 #%% calculo errores voltaje
 M = np.array([MedicionE1[0],MedicionE2[0],MedicionE3[0],MedicionE4[0],MedicionE5[0],MedicionE6[0],MedicionE7[0],MedicionE8[0],MedicionE9[0],MedicionE10[0]])
 Mean = np.mean(M,0)
 std = np.std(M,0)

plt.figure()
plt.errorbar(freqs,Mean,yerr=std,"o")
plt.grid(True)
plt.show()