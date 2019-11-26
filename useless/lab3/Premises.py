# for checking if the premises of the sweeping algorithm are met
# 1. No vertical line segments (no line segments with the same direction as the broom)
# 2. Two line segments must meet at one point maximum (no parallel line segments that overlap)
# 3. Each intersection must of exactly two line segments (no three or more line segments can go through one point)


def vertical_check(line_segments):  # O(n), n - number of line segments
    for line_segment in line_segments:
        if line_segment.calculate_slope() is None:
            return False
    return True


def overlap_check(line_segments):  # O(n*log(n)), n - number of line segments
    line_segments.sort(key=lambda x: x.p.x)
    for i in range(1, len(line_segments)):
        if line_segments[i - 1].q.x > line_segments[i].p.x:
            return True
    return False


def parallel_check(line_segments):  # O(n*log(n)), n - number of line segments
    slopes = []
    same_slopes = []

    for line_segment in line_segments:
        slopes.append((line_segment.calculate_slope(), line_segment.calculate_y_intersect(), line_segment))
    slopes.sort(key=lambda x: x[0])

    for i in range(1, len(slopes)):
        if slopes[i - 1][0] == slopes[i][0] and slopes[i - 1][1] == slopes[i][1]:
            same_slopes.append(slopes[i - 1][2])
        else:
            same_slopes.append(slopes[i - 1][2])

            if len(same_slopes) == 1:
                same_slopes = []
            else:
                if overlap_check(same_slopes):
                    return False

    return True


def premises_check(line_segments):
    return vertical_check(line_segments) and parallel_check(line_segments)
