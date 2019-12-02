def clean_new_nodes(new_nodes):
    for node in new_nodes:
        if node[1][0] < node[2][0]:
            node = [node[0], node[1], node[2]]
            node[1][0], node[2][0] = node[2][0], node[1][0]
            node = (node[0], node[1], node[2])


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
                points_dict[edge.points[i]] = (edge.points[i], len(points_dict))
                nodes.append(edge.points[i])

            if i == 0:
                new_edges[(start, points_dict[edge.points[i]][1])] = (start, points_dict[edge.points[i]][1])
            if i == len(edge.points) - 1:
                new_edges[(points_dict[edge.points[i]][1], end)] = (points_dict[edge.points[i]][1], end)
            if i != 0:
                new_edges[(points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])] = \
                    (points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])

    for edge in g2_dict:
        #         start = edge.segment[0]
        #         end = edge.segment[1]
        if nodes[edge.segment[0]][0] < nodes[edge.segment[1]][0]:
            start = edge.segment[0]
            end = edge.segment[1]
        else:
            start = edge.segment[1]
            end = edge.segment[0]

        if new_edges.get((start, end)) is not None:
            new_edges.pop((start, end))

        edge.points.sort(key=lambda x: x[0])

        for i in range(len(edge.points)):
            if points_dict.get(edge.points[i]) is None:
                points_dict[edge.points[i]] = (edge.points[i], len(points_dict))
                nodes.append(edge.points[i])

            if i == 0:
                new_edges[(start, points_dict[edge.points[i]][1])] = (start, points_dict[edge.points[i]][1])
            if i == len(edge.points) - 1:
                new_edges[(points_dict[edge.points[i]][1], end)] = (points_dict[edge.points[i]][1], end)
            if i != 0:
                new_edges[(points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])] = \
                    (points_dict[edge.points[i - 1]][1], points_dict[edge.points[i]][1])

    return new_edges, nodes