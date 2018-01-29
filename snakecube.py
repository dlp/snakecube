#!/usr/bin/env python2

S = [
    (0,0), (1,0), (2,0), (2,1), (3,1), (3,2), (3,3), (4,3), (4,4),
    (4,5), (5,5), (5,6), (6,6), (7,6), (7,7), (7,8), (8,8), (8,9),
    (9,9), (9,10), (9,11), (10,11), (11,11), (11,12), (11,13), (12,13), (13,13),
    ]


def dist(xv, yv):
    """Return Manhattan distance between two points."""
    return sum(abs(x-y) for (x,y) in zip(xv,yv))

def check_input(lst):
    assert len(lst) == len(set(lst))
    assert all(dist(x1,x) == 1 for (x1, x) in zip(S[0:-1], S[1:]))
    print "Input OK"

def lift(lst):
    """Lift from 2D to 3D, with z=0."""
    return [(x,y,0) for (x,y) in lst]

def extent(lst):
    """Get extent."""
    vecs = zip(*lst)
    return [max(v) - min(v) for v in vecs]

def check_extent(lst):
    """Returns true if points are within a 3x3x3 cube."""
    return all(e <= 3 for e in extent(lst))

def norm_vec(lst, pos):
    assert len(lst)>1 and pos>0
    return [a-a1 for (a,a1) in zip(lst[pos], lst[pos-1])]

def solve(lst, pos):
    assert len(lst)>0 and pos<len(lst)
    if not check_extent(lst[:pos+1])
        return # dead end

if __name__ == "__main__":
    check_input(S)
    s = lift(S[:9]) # FIXME small part
    for p in range(1,len(s)):
        print norm_vec(s, p)
