"""
From https://www.reddit.com/r/dailyprogrammer/comments/398mtv/20150610_challenge_218_intermediate_generating/
"""

import sys
import time


def display(p):
    "Prints out polyomino p"
    n = len(p)
    for x in range(n):
        for y in range(n):
            if (x, y) in p:
                sys.stdout.write("#")
            else:
                sys.stdout.write(" ")
        sys.stdout.write("\n")


def transform(p, t):
    "Transforms polyomino p using transformation t and then normalizes it"
    result = []
    n = len(p)
    for x in range(n):
        for y in range(n):
            if (x, y) in p:
                result.append(t(x, y))
    return normalize(result)


def normalize(p):
    "Translates p so that all its x,y coords are non-negative and sorted"
    min_x = min(x for (x, y) in p)
    min_y = min(y for (x, y) in p)
    return sorted([(x-min_x, y-min_y) for (x, y) in p])


def is_connected((x, y), p):
    "Checks if (x,y) is connnected to polyomino p but not part of p"
    s = set([(x+1, y), (x-1, y), (x, y-1), (x, y+1)])
    return (x, y) not in p and len(s.intersection(set(p))) > 0


def coordinate_extensions(p):
    "Returns a set of all possible coordinate extensions of polyomino p"
    coords = range(-1, len(p)+1)
    return set([(x, y) for x in coords
                for y in coords
                if is_connected((x, y), p)])


def extend(p):
    "Returns a list of polyominoes extending p by one"
    results = []
    for (x, y) in coordinate_extensions(p):
        q = list(p)
        q.append((x, y))
        q = canonical(normalize(q))
        if q not in results:  # is_unique(q, results):
            results.append(q)
    return sorted(results)


def canonical(p):
    "Returns the canonical form of polyomino p"
    transformations = [lambda x, y: (x, y),
                       lambda x, y: (x, -y),
                       lambda x, y: (-x, y),
                       lambda x, y: (-x, -y),
                       lambda x, y: (y, x),
                       lambda x, y: (y, -x),
                       lambda x, y: (-y, x),
                       lambda x, y: (-y, -x),
                       ]
    return min(transform(p, t) for t in transformations)


def polyominoes(n):
    "Returns a list of all polyominoes of size n"
    if n == 1:
        return [[(0, 0)]]

    results = []
    for p in polyominoes(n-1):
        for q in extend(p):
            if q not in results:
                results.append(q)

    return sorted(results)


def tests():
    p = [(0, 0), (0, 1), (0, 2), (1, 2)]
    assert is_connected((1, 3), p) is True
    assert is_connected((1, 4), p) is False
    assert is_connected((0, 1), p) is False
    assert is_connected((-1, 0), p) is True
    assert is_connected((-1, -1), p) is False

    q = [(0, 0), (1, 0), (2, 0), (2, 1)]
    r = [(0, 0), (1, 0), (2, 0), (1, 1)]
    assert is_similar(p, q) is True
    assert is_similar(q, p) is True
    assert is_similar(p, r) is False
    assert is_similar(r, p) is False
    assert is_similar(q, r) is False
    assert is_similar(r, q) is False

    one = [(0, 0)]
    two_1 = [(0, 0), (0, 1)]
    two_2 = [(0, 0), (1, 0)]
    tee = [(0, 0), (0, 1), (0, 2)]
    tee_1 = sorted([(0, 0), (1, 0), (0, 1)])
    tee_2 = sorted([(0, 1), (1, 0), (1, 1)])
    tee_3 = sorted([(0, 0), (1, 1), (0, 1)])

    assert canonical(two_1) == two_1
    assert canonical(two_2) == two_1
    assert canonical(tee_1) == tee_1
    assert canonical(tee_2) == tee_1
    assert canonical(tee_3) == tee_1

    assert extend(one) == [two_1]
    assert extend(two_1) == [tee, tee_1]

    assert polyominoes(1) == [one]
    assert polyominoes(2) == [two_1]
    assert polyominoes(3) == [tee, tee_1]

    print 'Yay! All test cases passed.'
    print ''


def display_polyominoes(n):
    "Generate and display all n-polyominoes"
    start = time.time()
    p_list = polyominoes(n)
    end = time.time()
    print 'Here are all %d possibilities of %d-polyominoes:' % (len(p_list), n)
    print ''
    for p in p_list:
        display(p)
    print 'Hew... I took %.3f seconds to generate this list' % (end - start)
    return None


tests()
display_polyominoes(6)
