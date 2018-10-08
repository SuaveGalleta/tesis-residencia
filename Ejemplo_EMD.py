import numpy as np
from PyEMD import EMD
import matplotlib.pyplot as tls
from numpy import *
from matplotlib.pyplot import *
from scipy.signal import *
from scipy.interpolate import splrep, splev

x = np.linspace(0,10, 10000) 
noise = random.uniform(-0.05,0.05,10000)
signal = sin (2*pi*1*x) + noise

emd = EMD()

IMFs = emd(signal, x)
print(IMFs)
n = IMFs.shape[0]+1

tls.figure("Señal")
tls.plot(signal)

tls.figure("DME")
tls.plot(IMFs[9])


for i, imf in enumerate(IMFs):
    tls.figure("funciones intrinsecas")
    tls.subplot(n,1,i+2)
    tls.plot(x,imf, 'g')
    tls.title("IMF "+str(i+1))
    tls.xlabel("Time [s]")
tls.show()

# Define signal
#t = np.linspace(0, 1, 200)
#s = np.cos(11*2*np.pi*t*t) + 6*t*t

# Execute EMD on signal
#IMF = EMD().emd(s,t)
#N = IMF.shape[0]+1

# Plot results
#tls.subplot(N,1,1)
#tls.plot(t, s, 'r')
#tls.title("Input signal: $S(t)=cos(22\pi t^2) + 6t^2$")
#tls.xlabel("Time [s]")

#for n, imf in enumerate(IMF):
#    tls.subplot(N,1,n+2)
#    tls.plot(t, imf, 'g')
#    tls.title("IMF "+str(n+1))
#    tls.xlabel("Time [s]")

#tls.tight_layout()
#tls.savefig('simple_example')
#tls.show()