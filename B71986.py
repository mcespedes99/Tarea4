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

# Frecuencia de operación
f = 1000

# Duración del período de cada onda
T = 1/f
