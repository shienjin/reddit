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
    result = set()
    n = len(p)
    for x in range(n):
        for y in range(n):
            if (x, y) in p:
                result.add(t(x, y))
    return normalize(result)


def normalize(p):
    "Translates p so that all its x,y coords are non-negative"
    min_x = min(x for (x, y) in p)
    min_y = min(y for (x, y) in p)
    return set([(x-min_x, y-min_y) for (x, y) in p])


def is_connected((x, y), p):
    "Checks if (x,y) is connnected to polyomino p but not part of p"
    s = set([(x+1, y), (x-1, y), (x, y-1), (x, y+1)])
    return (x, y) not in p and len(s.intersection(p)) > 0


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
        q = p.copy()
        q.add((x, y))
        q = normalize(q)
        if is_unique(q, results):
            results.append(q)
    return results


def is_similar(p, q):
    "Checks if p and q are similar polyominoes"
    transformations = [lambda x, y: (x, y),
                       lambda x, y: (x, -y),
                       lambda x, y: (-x, y),
                       lambda x, y: (-x, -y),
                       lambda x, y: (y, x),
                       lambda x, y: (y, -x),
                       lambda x, y: (-y, x),
                       lambda x, y: (-y, -x),
                       ]
    return q in [transform(p, t) for t in transformations]


def is_unique(p, polyominoes):
    "Checks if p is a unique polyomino in the list of given polyominoes"
    for q in polyominoes:
        if is_similar(p, q):
            return False
    return True


def polyominoes(n):
    "Returns a list of all polyominoes of size n"
    if n == 1:
        return [set([(0, 0)])]

    results = []
    for p in polyominoes(n-1):
        for q in extend(p):
            if is_unique(q, results):
                results.append(q)

    return results


def tests():
    p = set([(0, 0), (0, 1), (0, 2), (1, 2)])
    assert is_connected((1, 3), p) is True
    assert is_connected((1, 4), p) is False
    assert is_connected((0, 1), p) is False
    assert is_connected((-1, 0), p) is True
    assert is_connected((-1, -1), p) is False

    q = set([(0, 0), (1, 0), (2, 0), (2, 1)])
    r = set([(0, 0), (1, 0), (2, 0), (1, 1)])
    assert is_similar(p, q) is True
    assert is_similar(q, p) is True
    assert is_similar(p, r) is False
    assert is_similar(r, p) is False
    assert is_similar(q, r) is False
    assert is_similar(r, q) is False

    one = set([(0, 0)])
    two = set([(0, 0), (0, 1)])
    tee = [set([(0, 1), (1, 0), (1, 1)]),
           set([(0, 0), (0, 1), (0, 2)])]
    assert extend(one) == [two]
    assert extend(two) == tee

    assert polyominoes(1) == [one]
    assert polyominoes(2) == [two]
    assert polyominoes(3) == tee

    print 'Yay! All test cases passed.'
    print ''

tests()

n = 6
start = time.time()
p_list = polyominoes(n)
end = time.time()
print 'Here are all %d possibilities of %d-polyominoes:' % (len(p_list), n)
print ''
for p in p_list:
    display(p)
print 'Hew... I took %.3f seconds to generate this list' % (end - start)
