import math
import random

# zadanie 3 ###
def genA(l, r, n):
    points = []
    for x in range(n):
        points.append((random.uniform(l, r), random.uniform(l, r)))
    return points


def genB(A, R, n):
    points = []
    for x in range(n):
        p = random.uniform(0,2 * math.pi)
        points.append(((math.sin(p) * R) + A[0],
                       (math.cos(p) * R + A[1])))
    return points


def genC(A, B, C, D, n):
    points = []
    for x in range(n):
        side = random.randint(1,4)
        if side == 1:  # A-B
            points.append((A[0], random.uniform(A[1], B[1])))
        elif side == 2:  # B-C
            points.append((random.uniform(B[0], C[0]), B[1]))
        elif side == 3:  # C-D
            points.append((C[0], random.uniform(C[1], D[1])))
        else:  # D-A
            points.append((random.uniform(A[0], D[0]), A[1]))
    return points


def genD(A, B, C, D, no, np):
    points = []
    for x in range(no):
        points.append((random.uniform(0, B[0]), 0))
        points.append((0, random.uniform(0, D[1])))
    for x in range(np):
        place = random.uniform(0, B[0])
        points.append((place, place))
        place = random.uniform(0, B[0])
        points.append((place, B[0] - place))
    return points
# ###


# funkcja liczaca kąt nachylenia do osi 0X ###
def slope_to_OX(a, b):
    if a[0] == b[0] and a[1] == b[1]:
        return None
    if a[0] == b[0]:
        return 'X'
    if a[1] == b[1]:
        return 'Y'
    return (a[1] - b[1]) / (a[0] - b[0])
    # ###


# funkcja liczaca wyznacznik ###
def determinant(a, b, c):
    return ((a[0] - c[0]) * (b[1] - c[1])) - ((a[1] - c[1]) * (b[0] - c[0]))
# >0 => lewa strona
# <0 => prawa strona
# =0 => na linii
# ###


# algorytm Grahama ###
def Graham(points):
    points.sort(key=lambda x: (x[1], x[0]))
    p0 = points[0]

    share_x_with_p0 = []
    share_y_with_p0 = []
    positive_slope = []
    negative_slope = []

    for point in points:
        slope = (slope_to_OX(p0, point), point)

        if slope[0] is None:
            continue
        elif slope[0] == 'X':
            share_x_with_p0.append(slope)
        elif slope[0] == 'Y':
            share_y_with_p0.append(slope)
        elif slope[0] > 0:
            positive_slope.append(slope)
        else:
            negative_slope.append(slope)

    share_x_with_p0.sort(key=lambda x: x[1][1], reverse=True)
    share_y_with_p0.sort(key=lambda x: x[1][0], reverse=True)
    positive_slope.sort(key=lambda x: (x[0], x[1][0]))
    negative_slope.sort(key=lambda x: (x[0], x[1][0]))

    slopes = []

    if share_y_with_p0 != []:
        slopes.append(share_y_with_p0[0][1])
    tmp = []
    for point in positive_slope:
        if tmp == [] or point[0] == tmp[len(tmp) - 1][0]:
            tmp.append(point)
        else:
            slopes.append(tmp[len(tmp) - 1][1])
            tmp.append(point)
    if tmp != []: slopes.append(tmp[len(tmp) - 1][1])

    if share_x_with_p0 != []: slopes.append(share_x_with_p0[0][1])
    tmp = []
    for point in negative_slope:
        if tmp == [] or point[0] == tmp[len(tmp) - 1][0]:
            tmp.append(point)
        else:
            slopes.append(tmp[len(tmp) - 1][1])
            tmp.append(point)
    if tmp != []: slopes.append(tmp[len(tmp) - 1][1])
    slopes.insert(0, p0)

    i = 3
    stack = []
    stack.append(slopes[0])
    stack.append(slopes[1])
    stack.append(slopes[2])

    while i < len(slopes):
        j = len(stack) - 2

        det = determinant(stack[j], stack[j + 1], slopes[i])
        if det > 0:
            stack.append(slopes[i])
            i += 1
        elif det < 0:
            stack.pop()
        else:
            stack.pop()
            stack.append(slopes[i])
            i += 1

    return stack