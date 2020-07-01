# -*- coding: utf-8 -*-
"""
Tarea #4. IE0405 - Modelos Probabilísticos de Señales y Sistemas.
Empezada el Miércoles 1 de Julio 15:30 2020

@author: Mauricio Céspedes Tenorio.
Carné: B71986
"""
#Librerías
import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt

print("Respuestas de la Tarea #3 del curso IE0405 - Modelos Probabilísticos de Señales y Sistemas.")
print("Estudiante: Mauricio Céspedes Tenorio. Carné: B71986.")
'''
1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.
'''
#Extracción de datos del bits10k.cvs en un array que serían los bits:
bits = np.genfromtxt('bits10k.csv', delimiter='\n')

#Número de bit:
N = len(bits)

# Frecuencia de portadora:
f = 5000

# Periodo de símbolo igual a periodo completo de onda portadora:
T = 1/f

# Número de puntos de muestreo por cada período:
p = 55

# Creación de espacio lineal para después crear onda sinusoidal:
tp = np.linspace(0, T, p)

#Ondas necesarias para modulación BPSK:
# 1. Creación de la forma de onda sinusoidal:
seno = np.sin(2*np.pi * f * tp)

#Definición de frecuencia de muestre:
fm = p/T #55 puntos por periodo

# Creación de la línea temporal para toda la señal a modular:
t = np.linspace(0, N*T, N*p)

#Creación de array de señal a modular. Iniclalmente llena de ceros:
senal = np.zeros(N*p)

# Creación de la señal modulada BPSK:
for i, b in enumerate(bits):
  senal[i*p:(i+1)*p] = (2*b-1) * seno #El término (2*b-1) hace que los 1 en bits sigan siendo 1 y los 0 pasen a -1. De esta forma, en los ceros se coloca un seno negativo y en los 1 un seno positivo.

#Visualización de los primeros 6 bits modulados
pb = 6
plt.figure()
plt.plot(senal[0:pb*p], label='Señal modulada en BPSK')
plt.xlabel('Puntos de muestreo (50 por bit o periodo)')
plt.ylabel('Amplitud')
plt.legend()
plt.show()

'''
2. Calcular la potencia promedio de la señal modulada generada.
'''
# Potencia intantánea de la señal modulada:
Pinst = senal**2

# Potencia promedio: promedio temporal (equivalente a la integración) de la potencia instantánea
Pprom = integrate.trapz(Pinst, t) / (T*N)
print("La potencia promedio de la señal modulada es: "+"{:.4f}".format(Pprom))
