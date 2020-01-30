


from __future__ import division, unicode_literals, print_function, absolute_import
import time
import pyvisa as visa
import numpy as np
from matplotlib import pyplot as plt 
#print(__doc__)
# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.

resource_name1 = 'USB0::0x0699::0x0363::C108013::INSTR'

rm1 = visa.ResourceManager()

osci = rm1.open_resource(resource_name1)

# Pide indentificacion
print(osci.query('*IDN?'))

#%%
#######################################################################

"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000_p.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\AFG3012B (M Usuario).pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\AFG3012B (Prog Manual).pdf
"""





# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado.

resource_name2 = 'USB0::0x0699::0x0346::C034165::INSTR'

rm2 = visa.ResourceManager()
# Abre la sesion VISA de comunicacion
fungen = rm2.open_resource(resource_name2)

print(fungen.query('*IDN?'))


#%%
#######################################################################



# tiempo = float(input("Introduzca el tiempo a medir: "))
#frec = float(input("Introduzca la frecuencia de muestreo en Hz: "))
pausa = 2
frec1 = float(50080)
frec2 = float(50120)
paso = 1

datos=[]

# Rampa lineal de frequencias
frecuencias = np.linspace(frec1, frec2, int((frec2-frec1)/paso)+1)
for freq in frecuencias:
    
    time.sleep(pausa)	
    fungen.write('FREQ %f' % freq)
    osci.write('MEASUrement:IMMed:SOURCE1')
    osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh1 = osci.query('MEASU:IMM:VAL?')
    amplitudCh1 = float(amplitudCh1)
    osci.write('MEASUrement:IMMed:SOURCE2')
    osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh2 = osci.query('MEASU:IMM:VAL?')
    amplitudCh2 = float(amplitudCh2)
    Trans = amplitudCh1/amplitudCh2
    fCh1Ch2T = np.array([freq, amplitudCh1, amplitudCh2, Trans])
    datos.append(fCh1Ch2T)
	

print(datos)

A = np.array(datos)

nombre = input("Indique el nombre del archivo a guardar: ")

np.savetxt(str(nombre), A)

import matplotlib.pyplot as plt


plt.plot(A[:,0], A[:,4])
plt.show()

# A = np.loadtxt("nombredelarchivo.txt")   <--- Esta linea es para cargar el archivo con los datos por si se lo quiere manipular desde Python despues de medir.


fungen.close()
osci.close()


 