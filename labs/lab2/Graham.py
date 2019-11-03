%matplotlib notebook

import math
import random

# plot = Plot([PointsCollection([(7, 2), (11, 4), (13, 5), (11, 6), (12, 9), (9, 7), 
#                               (8, 10), (6, 9), (5, 5), (1, 7), (2, 3)])])

punkty = [((7, 2), 'A'), ((11, 4), 'B'), ((13, 5), 'C'), ((11, 6), 'D'), ((12, 9), 'E'), ((9, 7), 'F'), ((8, 10), 'G'),
         ((6, 9), 'H'), ((5, 5), 'I'), ((1, 7), 'J'), ((2, 3), 'K'), ((9, 2), 'Aprim'), ((7, 4), 'Abis'), 
        ((11, 2), 'Aprimprim'), ((7, 6), 'Abisbis')]
# Plot([PointsCollection(testShape)]).draw()

# Wybór p0 ###
punkty.sort(key=lambda x: (x[0][1], x[0][0]))
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
    nachylenie = (nachylenie_do_osi_x(p0[0][0], p0[0][1], punkt[0][0], punkt[0][1]), punkt)
    if nachylenie[0] is None: continue
    elif nachylenie[0] == 'X': na_linii_z_x.append(nachylenie)
    elif nachylenie[0] == 'Y': na_linii_z_y.append(nachylenie)
    elif nachylenie[0] > 0: dodatnie_nachylenie.append(nachylenie)
    else: ujemne_nachylenie.append(nachylenie)

na_linii_z_y.sort(key=lambda x: x[1][0], reverse=True)
na_linii_z_x.sort(key=lambda x: x[1][0], reverse=True)
dodatnie_nachylenie.sort(key=lambda x: (x[0], x[1][0][0]))
ujemne_nachylenie.sort(key=lambda x: (x[0], x[1][0][0]))

nachylenia = []

if na_linii_z_y != []: nachylenia.append(na_linii_z_y[0][1])
tmp = []
for punkt in dodatnie_nachylenie: 
    if tmp == [] or punkt[0] == tmp[len(tmp) - 1][0]:
        tmp.append(punkt)
    else:
        nachylenia.append(tmp[len(tmp) - 1][1])
        tmp.append(punkt)
nachylenia.append(tmp[len(tmp) - 1][1])
        
if na_linii_z_x != []: nachylenia.append(na_linii_z_x[0][1])
tmp = []
for punkt in ujemne_nachylenie: 
    if tmp == [] or punkt[0] == tmp[len(tmp) - 1][0]:
        tmp.append(punkt)
    else:
        nachylenia.append(tmp[len(tmp) - 1][1])
        tmp.append(punkt)
nachylenia.append(tmp[len(tmp) - 1][1])
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
    
    ax = stos[j][0][0]
    ay = stos[j][0][1]
    bx = stos[j + 1][0][0]
    by = stos[j + 1][0][1]
    cx = nachylenia[i][0][0]
    cy = nachylenia[i][0][0]
    
    wyz = wyznacznik(ax, ay, bx, by, cx, cy)
    if wyz > 0:
        stos.append(nachylenia[i])
        i += 1
    elif wyz < 0:
        stos.pop()
# ###

print("\nOtoczka: ", stos)