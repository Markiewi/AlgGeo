nodes = [(2, 10), (1, 4), (7, 1), (14, 5), (15, 8), (8, 12), (3, 8), (4, 5), (10, 5), (11, 7),
         (9, 9), (5, 10), (4, 7), (7, 3), (8, 4), (7, 8), (12, 8), (13, 6), (16, 6), (14, 3),
         (16, 1), (19, 7), (17, 11)]
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5), (6, 7), (7, 8), (8, 9), (9, 10),
         (6, 10), (11, 12), (12, 13), (13, 14), (14, 15), (11, 15), (15, 16), (14, 17),
         (16, 17), (16, 18), (14, 19), (18, 19), (13, 20), (20, 21), (21, 22), (11, 22)]
new_nodes = [((4.411764705882353, 8.235294117647058), (12, 11), (6, 10)),
             ((5.5, 5.0), (12, 13), (7, 8)),
             ((6.428571428571429, 8.571428571428571), (11, 15), (6, 10)),
             ((7.75, 5.0), (15, 14), (7, 8)), ((9.52, 2.44), (13, 20), (2, 3)),
             ((10.0, 8.0), (10, 9), (15, 16)),
             ((10.672727272727272, 10.472727272727273), (5, 4), (11, 22)),
             ((11.290322580645162, 3.4516129032258065), (2, 3), (14, 19)),
             ((14.571428571428571, 6.714285714285714), (3, 4), (16, 18))]


class SegmentInterPoints:
    def __init__(self, segment, coords=None):
        self.segment = segment
        self.points = []
        if coords is not None:
            self.points.append(coords)

    def __eq__(self, other):
        return self.segment[0] == other.segment[0] and self.segment[1] == other.segment[1]

    def __hash__(self):
        return hash((self.segment[0], self.segment[1]))

    def __repr__(self):
        return 'Segment: %s, Points: %s' % (self.segment, self.points)


def new_edges_and_points(edges, nodes, new_nodes):
    for i in range(len(new_nodes)):
        if new_nodes[i][1][0] < new_nodes[i][2][0]:
            new_nodes[i] = list(new_nodes[i])
            new_nodes[i][1], new_nodes[i][2] = new_nodes[i][2], new_nodes[i][1]
            new_nodes[i] = tuple(new_nodes[i])

    g1_dict = {}
    g2_dict = {}

    for new_node in new_nodes:
        inter = SegmentInterPoints(new_node[1], new_node[0])

        if g1_dict.get(inter) is None:
            g1_dict[inter] = inter
        else:
            g1_dict.get(inter).points.append(inter.points[0])

        inter = SegmentInterPoints(new_node[2], new_node[0])

        if g2_dict.get(inter) is None:
            g2_dict[inter] = inter
        else:
            g2_dict.get(inter).points.append(inter.points[0])

    points_dict = {}
    for i in range(len(nodes)):
        points_dict[nodes[i]] = nodes[i], i

    new_edges = {}
    for edge in edges:
        new_edges[edge] = edge

    for edge in g1_dict:
        if nodes[edge.segment[0]][0] < nodes[edge.segment[1]][0]:
            start = edge.segment[0]
            end = edge.segment[1]
        else:
            start = edge.segment[1]
            end = edge.segment[0]

        if new_edges.get((start, end)) is not None:
            new_edges.pop((start, end))
        elif new_edges.get((end, start)) is not None:
            new_edges.pop((end, start))

        edge.points.sort(key=lambda x: x[0])

        for i in range(len(edge.points)):
            if points_dict.get(edge.points[i]) is None:
                points_dict[edge.points[i]] = edge.points[i], len(points_dict)
                nodes.append(edge.points[i])

            if i == 0:
                new_edges[(start, points_dict[edge.points[i]][1])] = (start, points_dict[edge.points[i]][1])
            if i == len(edge.points) - 1:
                new_edges[(points_dict[edge.points[i]][1], end)] = (points_dict[edge.points[i]][1], end)
            if i != 0:
                new_edges[(points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])] = \
                    (points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])

    for edge in g2_dict:
        if nodes[edge.segment[0]][0] < nodes[edge.segment[1]][0]:
            start = edge.segment[0]
            end = edge.segment[1]
        else:
            start = edge.segment[1]
            end = edge.segment[0]

        if new_edges.get((start, end)) is not None:
            new_edges.pop((start, end))
        elif new_edges.get((end, start)) is not None:
            new_edges.pop((end, start))

        edge.points.sort(key=lambda x: x[0])

        for i in range(len(edge.points)):
            if points_dict.get(edge.points[i]) is None:
                points_dict[edge.points[i]] = edge.points[i], len(points_dict)
                nodes.append(edge.points[i])

            if i == 0:
                new_edges[(start, points_dict[edge.points[i]][1])] = (start, points_dict[edge.points[i]][1])
            if i == len(edge.points) - 1:
                new_edges[(points_dict[edge.points[i]][1], end)] = (points_dict[edge.points[i]][1], end)
            if i != 0:
                new_edges[(points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])] = \
                    (points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])

    return new_edges, nodes


new_edges, nodes = new_edges_and_points(edges, nodes, new_nodes)

nnn = []
for e in new_edges:
    nnn.append([nodes[e[0]], nodes[e[1]]])
print(nnn)
