import matplotlib.pyplot as plt
import numpy as np
t = np.arange(0,2*np.pi,0.1)
x = [(16*np.sin(t)**3)*i for i in range(99)]
y = [(13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t))*i for i in range(99)]
colors = [(i,0,1-i) for i in np.arange(0.4,1,0.005)]
for i in range(99):plt.plot(x[i],y[i],color=colors[i])
font={'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
plt.text(-1500, -1700, 'Valentine Days', fontdict=font)
plt.text(500, -1700, '2018', fontdict=font)
plt.show()
