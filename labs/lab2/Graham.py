%matplotlib notebook

import math
import random

# punkty = [(7, 2), (11, 4), (13, 5), (11, 6), (12, 9), (9, 7), (8, 10),
#          (6, 9), (5, 5), (1, 7), (2, 3), (9, 2), (7, 4), (11, 2), (7, 6)]

def genPoints(l, r, n):
    points = []
    for x in range(n):
        points.append((random.randint(l,r), random.randint(l,r)))
    return points
    
punkty = genPoints(0, 1000, 100)

# Wybór p0 ###
punkty.sort(key=lambda x: (x[1], x[0]))
p0 = punkty[0]
# ###

# funkcja liczaca kąt nachylenia do osi 0X ###
def nachylenie_do_osi_x(ax, ay, bx, by):
    if ax == bx and ay == by: return None
    if ax == bx: return 'X'
    if ay == by: return 'Y'
    return ((ay - by) / (ax - bx))
# ###

# funkcja liczaca wyznacznik ###
def wyznacznik(ax, ay, bx, by, cx, cy):
    return (((ax - cx) * (by - cy)) - ((ay - cy) * (bx - cx)))
# >0 => lewa strona
# <0 => prawa strona
# =0 => na linii
# ###

# Tworzenie posortowanej po kącie względem p0 tablicy punktów ###
na_linii_z_y = []
na_linii_z_x = []
dodatnie_nachylenie = []
ujemne_nachylenie = []

for punkt in punkty:
    nachylenie = (nachylenie_do_osi_x(p0[0], p0[1], punkt[0], punkt[1]), punkt)
    if nachylenie[0] is None: continue
    elif nachylenie[0] == 'X': na_linii_z_x.append(nachylenie)
    elif nachylenie[0] == 'Y': na_linii_z_y.append(nachylenie)
    elif nachylenie[0] > 0: dodatnie_nachylenie.append(nachylenie)
    else: ujemne_nachylenie.append(nachylenie)

na_linii_z_y.sort(key=lambda x: x[1][0], reverse=True)
na_linii_z_x.sort(key=lambda x: x[1][0], reverse=True)
dodatnie_nachylenie.sort(key=lambda x: (x[0], x[1][0]))
ujemne_nachylenie.sort(key=lambda x: (x[0], x[1][0]))

nachylenia = []

if na_linii_z_y != []: nachylenia.append(na_linii_z_y[0][1])
tmp = []
for punkt in dodatnie_nachylenie: 
    if tmp == [] or punkt[0] == tmp[len(tmp) - 1][0]:
        tmp.append(punkt)
    else:
        nachylenia.append(tmp[len(tmp) - 1][1])
        tmp.append(punkt)
if tmp != []: nachylenia.append(tmp[len(tmp) - 1][1])
        
if na_linii_z_x != []: nachylenia.append(na_linii_z_x[0][1])
tmp = []
for punkt in ujemne_nachylenie: 
    if tmp == [] or punkt[0] == tmp[len(tmp) - 1][0]:
        tmp.append(punkt)
    else:
        nachylenia.append(tmp[len(tmp) - 1][1])
        tmp.append(punkt)
if tmp != []:nachylenia.append(tmp[len(tmp) - 1][1])
nachylenia.insert(0, p0)
# ###

# Wyliczanie właściwych punktów otoczki ###
i = 3
stos = []
stos.append(nachylenia[0])
stos.append(nachylenia[1])
stos.append(nachylenia[2])

while i < len(nachylenia):
    j = len(stos) - 2
    
    ax = stos[j][0]
    ay = stos[j][1]
    bx = stos[j + 1][0]
    by = stos[j + 1][1]
    cx = nachylenia[i][0]
    cy = nachylenia[i][1]
    
    wyz = wyznacznik(ax, ay, bx, by, cx, cy)
    if wyz > 0:
        stos.append(nachylenia[i])
        i += 1
    elif wyz < 0:
        stos.pop()
# ###

print("\nOtoczka: ", stos)
Plot([PointsCollection(punkty, color = 'blue')]).draw()

for i in range(len(stos)):
    if i > 0:
        Plot([PointsCollection([])], [LinesCollection([[stos[i-1],stos[i]]])]).draw()
Plot([PointsCollection([])], [LinesCollection([[stos[0],stos[len(stos) - 1]]])]).draw()