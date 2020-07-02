# Respuestas Tarea 4 del curso IE0405
Estudiante: Mauricio Céspedes Tenorio - B71986

1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.  
R\ En la modulación **BPSK** (siglas del inglés *Binary Phase Shift Keying*, en español *Modulación por desplazamiento de fase*) se envía una forma de onda sinusoidal para el bit 1 y una sinusoidal negada (-seno) para el bit 0.

#### Lectura de bits del archivo CSV y modulación BPSK
```ruby
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
fm = p/T #200 puntos por periodo

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
```
