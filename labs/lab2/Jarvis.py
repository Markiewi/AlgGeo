def determinant(p, q, r):
    return ((p[0] - r[0]) * (q[1] - r[1])) - ((p[1] - r[1]) * (q[0] - r[0]))


# Liczenie poczatkowego indeksu
def bottom_index(points):
    bottom = 0
    for i in range(1, len(points)):
        if points[i][1] < points[bottom][1]:
            bottom = i
        elif points[i][1] == points[bottom][1]:
            if points[i][0] < points[bottom][0]:
                bottom = i
    return bottom
# ###

def distance(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

# algorytm Jarvisa ###
def Jarvis(points):
    n = len(points)
    if n < 3:
        return

    p0 = bottom_index(points)
    hull = []

    p = p0
    while True:
        hull.append(points[p])
        q = (p + 1) % n

        for i in range(n):
            if determinant(points[p], points[i], points[q]) > 0:
                q = i
            elif determinant(points[p], points[i], points[q]) == 0:
                if distance(points[p], points[i]) > distance(points[p], points[q]):
                    q = i

        p = q
        if p == p0:
            break

    return hull
# ###


pointss = [(2, 4), (8, 2), (4, 7), (2, 10), (5, 11), (9, 6), (8, 9), (7, 14), (12, 5), (13, 11), (14, 3)]
print(Jarvis(pointss))
