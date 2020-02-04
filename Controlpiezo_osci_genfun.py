
"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000.pdf
Manual P (web): https://github.com/hgrecco/labosdf-bin/raw/master/manuals/TektronixAFG3000_p.pdf
Manual U (local): \\Srvlabos\manuales\Tektronix\AFG3012B (M Usuario).pdf
Manual P (local): \\Srvlabos\manuales\Tektronix\AFG3012B (Prog Manual).pdf
"""


from __future__ import division, unicode_literals, print_function, absolute_import
import time
import pyvisa as visa
import numpy as np
from matplotlib import pyplot as plt 


#Comunicación con el osciloscopio
resource_name1 = 'USB0::0x0699::0x0363::C102223::INSTR'

rm1 = visa.ResourceManager()

osci = rm1.open_resource(resource_name1)

# Pide indentificacion
print(osci.query('*IDN?'))

#%%
#Comunicación con el generador de funciones

resource_name2 = 'USB0::0x0699::0x0346::C034167::INSTR'

rm2 = visa.ResourceManager()
# Abre la sesion VISA de comunicacion
fungen = rm2.open_resource(resource_name2)

print(fungen.query('*IDN?'))


#%%
#Barrido de frecuencias

# tiempo = float(input("Introduzca el tiempo a medir: "))
#frec = float(input("Introduzca la frecuencia de muestreo en Hz: "))
pausa = 3
frec1 = float(50080)
frec2 = float(50120)
paso = 1

datos=[]

# Rampa lineal de frequencias
frecuencias = np.linspace(frec1, frec2, int((frec2-frec1)/paso)+1)
for freq in frecuencias:
   
    fungen.write('FREQ %f' % freq)
    time.sleep(pausa)	
    osci.write('MEASUrement:IMMed:SOUrce CH1')
    osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh1_str = osci.query('MEASU:IMM:VAL?')
    time.sleep(1)
    amplitudCh1 = float(amplitudCh1_str)
    print('canal 1:', amplitudCh1)
    
    osci.write('MEASUrement:IMMed:SOU CH2')
    #osci.write('MEASUrement:IMMed:TYPe CRMs')
    amplitudCh2_str = osci.query('MEASU:IMM:VAL?')
    amplitudCh2 = float(amplitudCh2_str)
    print('canal 2:', amplitudCh2)
    
    Trans = amplitudCh1/amplitudCh2
    fCh1Ch2T = np.array([freq, amplitudCh1, amplitudCh2, Trans])
    datos.append(fCh1Ch2T)
	

print(datos)

A = np.array(datos)

nombre = 'CampanaResonancia2'

np.savetxt(str(nombre), A)

plt.figure()
plt.plot(A[:,0], A[:,3])
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Transferencia')
#plt.show()

# A = np.loadtxt("nombredelarchivo.txt")   <--- Esta linea es para cargar el archivo con los datos por si se lo quiere manipular desde Python despues de medir.

fungen.close()
osci.close()


 