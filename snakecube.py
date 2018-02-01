#!/usr/bin/env python2
#
# Solve a snake cube puzzle!
#
# Author:  Daniel Wiltsche-Prokesch <daniel.prokesch@gmail.com>
# Date:    2018-02-01
# License: MIT
#

import sys

# the input snake, in the x,y plane
S = [
    (0,0), (1,0), (2,0), (2,1), (3,1), (3,2), (3,3), (4,3), (4,4),
    (4,5), (5,5), (5,6), (6,6), (7,6), (7,7), (7,8), (8,8), (8,9),
    (9,9), (9,10), (9,11), (10,11), (11,11), (11,12), (11,13), (12,13), (13,13),
    ]

# coordinate system: left handed
# y
# |
# +----x
# z away from you

class Matrix4D(list):
    """Transformation matrix for 3D with homogenous coordinates."""
    def __init__(self, initial):
        assert isinstance(initial, list) and len(initial) == 4*4
        list.__init__(self, initial)

    def __mul__(self, other):
        r = []
        if isinstance(other, Matrix4D):
            for y in range(4):
                for x in range(4):
                    v = 0
                    for i in range(4):
                        v += (self[i * 4 + x] * other[y * 4 + i])
                    r.append(v)
        else:
            raise NotImplementedError
        return Matrix4D(r)

    def transform(self, x, y, z):
        r = []
        for i in range(4):
            row = self[(i*4):(i*4+4)]
            r.append(sum(r*a for r,a in  zip(row, (x,y,z,1))))
        return tuple(r[:-1])

# 0, pi/2, pi, 3pi/2
sin = [ 0, 1, 0, -1 ]
cos = [ 1, 0, -1, 0 ]

def Rx(a):
    assert abs(a) in range(4)
    return Matrix4D([
        1,      0,       0, 0,
        0, cos[a], -sin[a], 0,
        0, sin[a],  cos[a], 0,
        0,      0,       0, 1,
    ])

def Ry(a):
    assert abs(a) in range(4)
    return Matrix4D([
        cos[a], 0, -sin[a], 0,
             0, 1,       0, 0,
        sin[a], 0,  cos[a], 0,
             0, 0,       0, 1,
    ])

def Rz(a):
    assert abs(a) in range(4)
    return Matrix4D([
        cos[a], -sin[a], 0, 0,
        sin[a],  cos[a], 0, 0,
             0,       0, 1, 0,
             0 ,      0, 0, 1,
    ])

def T(tx,ty,tz):
    return Matrix4D([
        1, 0, 0, tx,
        0, 1, 0, ty,
        0, 0, 1, tz,
        0, 0, 0,  1,
    ])

def rotmat(nv, a):
    """Get rotation matrix for given normal vector and a*(pi/2)."""
    assert abs(sum(nv)) == 1
    rm = [Rx, Ry, Rz]
    # we select the non-null component and don't care about the sign.
    return [R(a*sel) for R, sel in  zip(rm, nv) if sel][0]

def mat_at_pt(lst, idx, a):
    """Get the transform matrix to apply rotation at cube lst[idx]."""
    assert 0 < idx < len(lst)
    assert a in range(4)
    nv = norm_vec(lst, idx)
    x, y, z = lst[idx]
    return T(-x,-y,-z) * rotmat(nv, a) * T(x,y,z)

def dist(xv, yv):
    """Return Manhattan distance between two points."""
    return sum(abs(x-y) for (x,y) in zip(xv,yv))

def check_input(lst):
    """Input constraints: a snake; no two cubes at the same location. """
    assert len(lst) == len(set(lst))
    assert all(dist(x1,x) == 1 for (x1, x) in zip(S[0:-1], S[1:]))
    print "Input OK"

def print_input(lst):
    """Print 2D input snake."""
    xmax, ymax = [max(v) for v in zip(*lst)]
    for yrow in range(ymax,-1,-1):
        pts = [x for x,y in lst if y == yrow]
        print ''.join(['[]' if i in pts else '  ' for i in range(xmax+1)])

def lift(lst):
    """Lift from 2D to 3D, with z=0."""
    return [(x, y, 0) for (x,y) in lst]

def extent(lst):
    """Get extent (dimensions object given by lst)."""
    vecs = zip(*lst)
    return [max(v) - min(v) for v in vecs]

def check_extent(lst):
    """Returns true if points are within a 3x3x3 cube."""
    return all(e < 3 for e in extent(lst))

def norm_vec(lst, idx):
    """Get the normal vector pointing to cube at idx (from previous cube)."""
    assert len(lst)>1 and 0 < idx < len(lst)
    return [a-a1 for (a,a1) in zip(lst[idx], lst[idx-1])]

def solve(lst, idx):
    """Recursive solving procedure.

    Try solutions systematically, starting at cube lst[idx].
    """
    assert len(lst)>1 and 0 < idx < len(lst)
    #print " "*idx, "solve({}, {})".format(lst, idx)
    # normal vector has not changed, proceed to next
    if idx < len(lst) -1 and norm_vec(lst, idx) == norm_vec(lst, idx-1):
        solve(lst, idx+1)
        return
    # good up to now?
    # llst is the part of the snake up to now
    # rlst is the remainder
    llst, rlst = lst[:idx+1], lst[idx+1:]
    if not check_extent(llst) or len(llst) != len(set(llst)):
        #print "dead end", llst, rlst
        return # dead end
    # check solution
    if idx == len(lst) - 1:
        print "solution!", lst
        # or return, if you don't want to quit on the first found solution
        sys.exit(0)
    # 4 possible twists
    for a in range(4):
        mat = mat_at_pt(lst, idx, a)
        new_list = []
        for pt in rlst:
            new_list.append(mat.transform(*pt))
        # move on with the newly built list
        solve(llst + new_list, idx+1)

if __name__ == "__main__":
    print "input:", S
    print_input(S)
    check_input(S)
    s = lift(S)
    solve(s, 2)

