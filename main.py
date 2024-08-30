from matplotlib import pyplot as plt
import numpy as np


""" 
neme = BF PAV
https://www.as.up.krakow.pl/minicalc/PAVBF.HTM
p = 0.302318119
m0 = 2445886.5615
"""


def o_c_calc(m_obs, typ):
    # Function that calculates the number of E periods, the moment of minimum and o-c
    p = 0.302318119
    m0 = 2448056.9016
    e1 = (m_obs - m0) / p 
    if typ == 'pri': # The type determines how to round e
        e2 = int(e1) + 1
    else:
        e2 = round(e1*2) / 2
    mc = m0 + p * e2
    o_c = m_obs - mc
    return o_c, e2 # The function returns o-c and e

with open('/content/drive/MyDrive/BF_Pav_minima.csv', 'r') as f:
    header1 = f.readline() # Extracting headers
    header2 = f.readline()
    data = np.array([i.strip().split(',') for i in f.read().splitlines()])
    o_c_list = []
    epoch = []
    for i in data:
        """ The loop reads m_obs and 
            the type ('pri' or 'sec') from array,
            then inserts the data into the o_c_calc function,
            and adds the obtained results to the previously created lists """
        m_obs = float(i[0])
        typ = i[2]
        o_c, e = o_c_calc(m_obs, typ)
        o_c_list.append(o_c)
        epoch.append(e)

for i in range(len(o_c_list)-1):
    # A loop that removes outliers from the norm
    if abs(o_c_list[i]) > 0.1:
        del o_c_list[i]
        del epoch[i]

p = np.polyfit(epoch, o_c_list, 3)
""" np.polyfit to funkcja, która pozwala na interpolację wielomianową
    w tym przypadku 3go stopnia, celem jest wygładzenie funkcji """
x_new = np.linspace(min(epoch), max(epoch))
# New points where we want to interpolate
y_interp = np.polyval(p, x_new)
# Polynomial interpolation

plt.title("BF Pav")
plt.axhline(y=0, color='#D3D3D3', linestyle='--')
plt.plot(epoch, o_c_list, color='#3480eb60')
plt.plot(x_new, y_interp, color='black')
plt.plot(epoch, o_c_list, '.', color='orange')
plt.xlabel('E')
plt.ylabel('O-C')
plt.xlim([-10000, 40000])
plt.show()
