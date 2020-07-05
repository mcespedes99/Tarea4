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

print("Respuestas de la Tarea #4 del curso IE0405 - Modelos Probabilísticos de Señales y Sistemas.")
print("Estudiante: Mauricio Céspedes Tenorio. Carné: B71986.")
'''
1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.
'''
#Extracción de datos del bits10k.cvs en un array que serían los bits:
bits = np.genfromtxt('bits10k.csv', delimiter='\n')

#Número de bit:
N = len(bits)

# Frecuencia de portadora de 5 kHz:
f = 5000

# Periodo de símbolo igual a periodo completo de onda portadora:
T = 1/f

# Número de puntos de muestreo por cada período:
p = 80

# Creación de espacio lineal para después crear onda sinusoidal:
tp = np.linspace(0, T, p)

#Ondas necesarias para modulación BPSK:
# 1. Creación de la forma de onda sinusoidal:
seno = np.sin(2*np.pi * f * tp)
#Visualización de esta onda:
plt.plot(tp, seno, label='Onda portadora sinusoidal')
plt.ylabel('Amplitud')
plt.xlabel('Tiempo [s]')
plt.legend()
plt.show()

#Definición de frecuencia de muestreo:
fm = p/T #80 puntos por periodo, 400 kHz

# Creación de la línea temporal para toda la señal a modular:
t = np.linspace(0, N*T, N*p)

#Creación de array de señal a modular. Iniclalmente llena de ceros:
senal = np.zeros(N*p)

# Creación de la señal modulada BPSK:
for i, b in enumerate(bits):
  senal[i*p:(i+1)*p] = (2*b-1) * seno #El término (2*b-1) hace que los 1 en bits sigan siendo 1 y los 0 pasen a -1. De esta forma, en los ceros se coloca un seno negativo y en los 1 un seno positivo.

#Visualización de los primeros 8 bits modulados
pb = 8
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
Pprom = integrate.trapz(Pinst, t) / (T*N) #Pprom=Ps
print("La potencia promedio de la señal modulada es: "+"{:.4f}".format(Pprom))

'''
3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.
'''
# Matriz con valores a probar para el SNR:
valores_SNR = [-2, -1, 0, 1, 2, 3]

#Se crea una matriz en la cual se guardarán los distintos valores de BER para todos los SNR:
valores_BER = []

#EL PUNTO 3 CONTINÚA DESPUÉS DEL 4 CON EL FOR.

'''
4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.
'''
#Gráfica antes del canal ruidoso:
fw, PSD = signal.welch(senal, fm, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Densidad espectral de potencia [V**2/Hz]')
plt.show()

#La gráfica de densidad después del canal ruidoso está dentro del for para cada SNR.

'''
Continuación del punto 3:
'''
#Se realiza un for para valorar los distintos valores de SNR solicitados:
for SNR in valores_SNR:
    # Potencia de señal de ruido para el SNR deseado y potencia de la señal modulada ya calculada:
    Pn = Pprom / np.power(10,SNR / 10)

    # Cálculo de la desviación estándar del ruido requerido (Pn = sigma^2):
    sigma = np.sqrt(Pn)

    # Crear ruido a partir de la desviación estándar:
    ruido = np.random.normal(0, sigma, senal.shape)

    # Simulación del canal ruidoso de tipo AWGN:
    Rx = senal + ruido

    # Visualización de los primeros ocho bits de la señal ruidosa:
    pb = 8
    plt.figure()
    plt.plot(Rx[0:pb*p],label='Señal ruidosa. SNR={}'.format(SNR))
    plt.xlabel('Puntos de muestreo (50 por bit o periodo)')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.show()

    '''
    Segunda parte del punto 4. Densidad espectral de potencia después del canal ruidoso:
    '''
    #Gráfica después del canal ruidoso:
    fw, PSD = signal.welch(Rx, fm, nperseg=1024)
    plt.figure()
    plt.semilogy(fw, PSD, label='SNR={}'.format(SNR))
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Densidad espectral de potencia [V**2/Hz]')
    plt.legend()
    plt.show()

    '''
    5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.
    '''
    # Pseudo-energía de la onda original (esta es suma, no integral)
    Es = np.sum(seno**2)

    # Inicialización del vector de bits recibidos
    bitsRx = np.zeros(bits.shape)

    # Decodificación de la señal por detección de energía:
    for k, b in enumerate(bits):
        Ep = np.sum(Rx[k*p:(k+1)*p] * seno)
        #Si la señal de Rx es el negativo de seno, la multiplicación será: seno*-seno, lo cual da el inverso de la Pseudo-energía; es decir, un resultado negativo. Por eso se compara con cero.
        if Ep > 0:
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0

    #Errores contados:
    err = np.sum(np.abs(bits - bitsRx))

    #Tasa de error de Bits:
    BER = err/N
    valores_BER = np.append(valores_BER, BER)
    print('Con un SNR de {}, hay un total de {} errores en {} bits para una tasa de error de {}.'.format(SNR, err, N, BER))

'''
6. Graficar BER versus SNR.
'''
plt.figure()
plt.plot(valores_SNR, valores_BER, 'go')
plt.xlabel('BER')
plt.ylabel('SNR')
plt.show()
