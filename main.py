from matplotlib import pyplot as plt
import numpy as np


""" 
neme = BF PAV
https://www.as.up.krakow.pl/minicalc/PAVBF.HTM
p = 0.302318119
m0 = 2445886.5615
"""


def o_c_calc(m_obs, typ):
    # Funkcja obliczająca liczbę okresów E, moment minimum oraz o-c
    p = 0.302318119
    m0 = 2448056.9016
    e1 = (m_obs - m0) / p 
    if typ == 'pri': # Od typu zależy w jaki sposób zaokrąglić e
        e2 = int(e1) + 1
    else:
        e2 = round(e1*2) / 2
    mc = m0 + p * e2
    o_c = m_obs - mc
    return o_c, e2 # Funkcja zwraca o-c oraz e

with open('/content/drive/MyDrive/BF_Pav_minima.csv', 'r') as f:
    header1 = f.readline() # Wyodrębnienie nagłówków
    header2 = f.readline()
    data = np.array([i.strip().split(',') for i in f.read().splitlines()])
    o_c_list = []
    epoch = []
    for i in data:
        """ Pętla odczytuje kolejno m_obs oraz typ
            ('pri' lub 'sec') z arraya, po czym podstawia dane
            do funkcji o_c_calc, a otrzymane wyniki 
            dopisuje do wcześniej stworzonych list """
        m_obs = float(i[0])
        typ = i[2]
        o_c, e = o_c_calc(m_obs, typ)
        o_c_list.append(o_c)
        epoch.append(e)

for i in range(len(o_c_list)-1):
    # Pętla, która usuwa wartości odstające od normy
    if abs(o_c_list[i]) > 0.1:
        del o_c_list[i]
        del epoch[i]

p = np.polyfit(epoch, o_c_list, 3)
""" np.polyfit to funkcja, która pozwala na interpolację wielomianową
    w tym przypadku 3go stopnia, celem jest wygładzenie funkcji """
x_new = np.linspace(min(epoch), max(epoch))
# Nowe punkty, w których chcemy interpolować
y_interp = np.polyval(p, x_new)
# Interpolacja wielomianowa

plt.title("BF Pav") # Nagłówek
plt.axhline(y=0, color='#D3D3D3', linestyle='--')
plt.plot(epoch, o_c_list, color='#3480eb60')
plt.plot(x_new, y_interp, color='black')
plt.plot(epoch, o_c_list, '.', color='orange')
plt.xlabel('E')
plt.ylabel('O-C')
plt.xlim([-10000, 40000])
plt.show()
