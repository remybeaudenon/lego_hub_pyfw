#-----------------------------------------------------------------------------
# Title:        MindCuber-RI
#
# Author:       David Gilday
#
# Copyright:    (C) 2021-2023 David Gilday
#
# Website:      http://mindcuber.com
#
# Version:      v1p1
#
# Modified:    $Date: 2023-05-29 21:20:31 +0100 (Mon, 29 May 2023) $
#
# Revision:    $Revision: 7965 $
#
# Usage:
#
#   This software may be used for any non-commercial purpose providing
#   that the original author is acknowledged.
#
# Disclaimer:
#
#   This software is provided 'as is' without warranty of any kind, either
#   express or implied, including, but not limited to, the implied warranties
#   of fitness for a purpose, or the warranty of non-infringement.
#-----------------------------------------------------------------------------

import gc, os, time, hub

hub.display.show(hub.Image.DIAMOND)

def fatal_error(msg):
    print("ERROR: "+msg)
    raise SystemExit

def trace(msg):
    if False:
        gc.collect()
        print("TRACE: "+msg+" mem="+str(gc.mem_free()))

#-----------------------------------------------------------------------------

MAXINT = 0x7FFFFFFF

MV_MAX = 80
MV_TGT = 33

import random

trace("class cube")
class cube():

    colors = None

    def __init__(self):
        self.mv_n    = 0
        self.quick    = False
        self.end_time = 0
        self.pce    = [0] * NFACE
        for f in range(NFACE):
            self.pce[f] = [f] * (2*NSIDE)
        self.mv_f    = [0] * MV_MAX
        self.mv_r    = [0] * MV_MAX
        self.col    = ['w', 'g', 'y', 'b', 'r', 'o']
        self.colors= None
        # pre-allocate for speed
        self.tmp_f    = [0] * cube_mtab.MV_MENT
        self.tmp_r    = [0] * cube_mtab.MV_MENT
        self.tmp_mi= cube_idx()

    def reset_state(self):
        for f in range(NFACE):
            for o in range(2*NSIDE):
                self.pce[f][o] = f

    def alloc_colors(self):
        if self.colors == None:
            self.colors = cube_colors(self)
            self.valc = [0] * NFACE
            self.vale = [0] * NFACE
            for f in range(NFACE):
                self.valc[f] = [False] * NFACE
                self.vale[f] = [False] * NFACE

    def copy(self, m):
        for f in range(NFACE):
            for i in range(2*NSIDE):
                self.pce[f][i] = m.pce[f][i]

    def copy_moves(self, m):
        self.mv_n = m.mv_n
        for i in range(self.mv_n):
            self.mv_f[i] = m.mv_f[i]
            self.mv_r[i] = m.mv_r[i]

    def corner(self, f0, f1):
        return self.pce[f0][cm.corner(f0, f1)]

    def edge(self, f0, f1):
        return self.pce[f0][cm.edge(f0, f1)]

    def rot(self, f, r):
        r= RMOD(r)
        p0 = self.pce[f]
        fd = cm.dir(f, NSIDE_M1)
        while r > 0:
            r-= 1
            p= p0[6]; p0[6] = p0[4]; p0[4] = p0[2]; p0[2] = p0[0]; p0[0] = p
            p= p0[7]; p0[7] = p0[5]; p0[5] = p0[3]; p0[3] = p0[1]; p0[1] = p
            pd= self.pce[fd]
            od2 = cm.corner(fd, f)
            od0 = (od2-2)&7
            c0= pd[od0]
            e0= pd[od0+1]
            c1= pd[od2]
            for d in range(NSIDE-2, -1, -1):
                fs= cm.dir(f, d)
                os2 = cm.corner(fs, f)
                os0 = (os2-2)&7
                ps= self.pce[fs]
                pd[od0]= ps[os0]
                pd[od0+1] = ps[os0+1]
                pd[od2]= ps[os2]
                pd= ps
                od0 = os0
                od2 = os2
            # }
            pd[od0]= c0
            pd[od0+1] = e0
            pd[od2]= c1

    def backtrack_a(self, f):
        i = self.mv_n
        btrack = False
        while (i > 0):
            i -= 1
            fi = self.mv_f[i]
            if cm.adjacent(f, fi):
                break
            if f <= fi:
                btrack = True
                break
        # }
        return btrack

    def add_mv(self, f, r):
        i = self.mv_n
        mrg = False
        while (i > 0):
            i -= 1
            fi = self.mv_f[i]
            if cm.adjacent(f, fi):
                break
            if f == fi:
                r += self.mv_r[i]
                r = RFIX(r)
                if r != 0:
                    self.mv_r[i] = r
                else:
                    self.mv_n -= 1
                    while (i < self.mv_n):
                        self.mv_f[i] = self.mv_f[i+1]
                        self.mv_r[i] = self.mv_r[i+1]
                        i += 1
                    # }
                # }
                mrg = True
                break
            # }
        # }
        if not mrg:
            self.mv_f[self.mv_n] = f
            self.mv_r[self.mv_n] = RFIX(r)
            self.mv_n += 1
        # }

    def move(self, f, r):
        self.rot(f, r)
        self.add_mv(f, r)

    def valid_pieces(self):
        for f0 in range(NFACE):
            for f1 in range(NFACE):
                adj = cm.adjacent(f0, f1)
                self.valc[f0][f1] = adj
                self.vale[f0][f1] = adj
        for f0 in range(0, 3, 2):
            for f1 in range(NFACE):
                if cm.adjacent(f0, f1):
                    f2 = cm.get_remap(f0, f1).fm[5]
                    c0 = self.corner(f0, f1)
                    c1 = self.corner(f1, f2)
                    invalid = True
                    if self.valc[c0][c1]:
                        c2 = self.corner(f2, f0)
                        if c2 == cm.get_remap(c0, c1).fm[5]:
                            self.valc[c0][c1] = False
                            self.valc[c1][c2] = False
                            self.valc[c2][c0] = False
                            invalid = False
                    if invalid:
                        return False
            # }
        # }
        for f0 in range(1, NFACE):
            for f1 in range(f0):
                if cm.adjacent(f0, f1):
                    e0 = self.edge(f0, f1)
                    e1 = self.edge(f1, f0)
                    if self.vale[e0][e1]:
                        self.vale[e0][e1] = False
                        self.vale[e1][e0] = False
                    else:
                        return False
            # }
        # }
        return True

    def valid_positions(self):
        self.valid = False
        self.solve(0)
        return self.valid

    def solved(self):
        slvd = True
        f = 0
        while (slvd and f < NFACE):
            for p in range(2*NSIDE):
                if self.pce[f][p] != f:
                    slvd = False
                    break
            # }
            f += 1
        # }
        return slvd

    def timeout(self):
        return time.ticks_ms() >= self.end_time

    def solve_remap(self, best, s0, check = False):
        slvd = True
        for s in range(s0, solve_map.NSTAGE):
            mi = self.tmp_mi
            mi.init(self)
            i = mi.index(s)
            if i != 0:
                f = self.tmp_f
                r = self.tmp_r
                n = mt[s].moves(i, f, r)
                if n > 0:
                    mv = self.mv_n + n
                    for j in range(n):
                        self.add_mv(f[j], r[j])
                    # }
                    if (self.mv_n > best or
                        (s == 0 and self.mv_n < mv)):
                        slvd = False
                        break
                    # }
                    if s < (solve_map.NSTAGE-1) or check:
                        for j in range(n):
                            self.rot(f[j], r[j])
                    # }
                else:
                    slvd = False
                    break
                # }
            # }
        # }
        self.valid = check and slvd and self.solved()
        return slvd

    def solve_one(self, cb, cs, depth):
        slvd = False
        if self.mv_n < depth:
            f = 0
            while (not slvd and f < NFACE):
                if not self.backtrack_a(f):
                    n = self.mv_n+1
                    for i in range(1, NSIDE):
                        self.move(f, 1)
                        if not slvd and self.solve_one(cb, cs, depth):
                            slvd = True
                    # }
                    self.move(f, 1)
                # }
                f += 1
            # }
        else:
            # print("solve_one: quick="+str(cb.quick))
            cs.copy(self)
            cs.copy_moves(self)
            cs.end_time = cb.end_time
            if cs.solve_remap(cb.mv_n, 0, cb.quick):
                cb.valid = cs.valid
                if cs.mv_n < cb.mv_n:
                    # print("solve_one: solved="+str(cs.mv_n))
                    cb.copy_moves(cs)
                # }
            # }
            # finish if a short solution has been found or if any solution
            # has been found and the timeout has expired or if only a quick
            # solve is required
            if cb.mv_n <= MV_TGT or (cb.mv_n <= MV_MAX and (cb.quick or cb.timeout())):
                trace("solved_one()")
                slvd = True
        return slvd

    def solve(self, msecs = 1000):
        start_time = time.ticks_ms()
        self.mv_n = MAXINT
        self.end_time = start_time + msecs
        self.quick = (msecs == 0)
        cw = cube()
        cw.copy(self)
        cs = cube()
        depth = 0
        while (not cw.solve_one(self, cs, depth)):
            depth += 1
        # print("Moves: "+str(self.mv_n)+" "+
        #    "Time: "+str(int(time.ticks_ms() - start_time))+"ms ")

    def solve_apply(self):
        for i in range(self.mv_n):
            self.rot(self.mv_f[i], self.mv_r[i])

    def scramble(self, msecs = 1000):
        self.reset_state()
        # Generate a random state by randomly exchanging pairs of edge and corner
        # pieces of a solved cube similar to WCA scramble regulations
        # Note: the random state may be impossible to solve but the solve algorithm
        # will solve as many as possible so is equivalent to generating a legal state
        for i in range(NEDGE-1):
            f0 = sm.ep0[i]
            f1 = sm.ep1[i]
            o0 = cm.edge(f0, f1)
            o1 = cm.edge(f1, f0)
            j= random.randint(i, NEDGE-1)
            f2 = sm.ep0[j]
            f3 = sm.ep1[j]
            if random.randint(0, 1) == 1:
                f2, f3 = (f3, f2)
            o2 = cm.edge(f2, f3)
            o3 = cm.edge(f3, f2)
            self.pce[f0][o0], self.pce[f1][o1], self.pce[f2][o2], self.pce[f3][o3] = (
                self.pce[f2][o2], self.pce[f3][o3], self.pce[f0][o0], self.pce[f1][o1]
                )
        for i in range(NCORNER-1):
            f0 = sm.cp0[i]
            f1 = sm.cp1[i]
            f2 = sm.cp2[i]
            o0 = cm.corner(f0, f1)
            o1 = cm.corner(f1, f2)
            o2 = cm.corner(f2, f0)
            j= random.randint(i, NCORNER-1)
            f3 = sm.cp0[j]
            f4 = sm.cp1[j]
            f5 = sm.cp2[j]
            for r in range(random.randint(0, 2)):
                f3, f4, f5 = (f4, f5, f3)
            o3 = cm.corner(f3, f4)
            o4 = cm.corner(f4, f5)
            o5 = cm.corner(f5, f3)
            self.pce[f0][o0], self.pce[f1][o1], self.pce[f2][o2], self.pce[f3][o3], self.pce[f4][o4], self.pce[f5][o5] = (
                self.pce[f3][o3], self.pce[f4][o4], self.pce[f5][o5], self.pce[f0][o0], self.pce[f1][o1], self.pce[f2][o2]
                )
        # Solve the cube and use the solution as the scramble sequence
        # Note: this is the inverse of the scramble sequence for randomly
        # generated state but the result is equivalently random
        self.solve(msecs)
        # Apply the scramble sequence to a solved cube to get a scrambled state
        self.reset_state()
        self.solve_apply()
        # print("Scramble moves:",self.mv_n)
        # self.display()

    def set_rgb(self, f, o, rgb):
        self.colors.set_rgb(f, o, rgb)

    def get_clr(self, f, o):
        return self.colors.get_clr(f, o)

    def determine_colors(self, t):
        return self.colors.determine_colors(t)

    def display_three(self, f, a, b, c):
        s = self.col[self.pce[f][a]] + " "
        if b == 8:
            s += self.col[f]
        else:
            s += self.col[self.pce[f][b]]
        return s + " " + self.col[self.pce[f][c]]

    def display_line(self, f, l):
        if (l == 0):
            s = self.display_three(f, 2, 3, 4)
        elif (l == 1):
            s = self.display_three(f, 1, 8, 5)
        else:
            s = self.display_three(f, 0, 7, 6)
        return s

    def display(self):
        for l in range(3):
            print("    " + self.display_line(4, l))
        for l in range(3):
            print(self.display_line(0, l) + " " +
                self.display_line(1, l) + " " +
                self.display_line(2, l) + " " +
                self.display_line(3, l))
        for l in range(3):
            print("    " + self.display_line(5, l))

#-----------------------------------------------------------------------------

NFACE = 6

def POS(f, o):
    return f*9+o

trace("class cube_colors")
class cube_colors():

    def __init__(self, cb):
        self.cb   = cb
        self.clrs = []
        for i in range(NFACE*9):
            self.clrs.append(color())

    def set_col(self, f, o, c):
        self.cb.pce[f][o] = c

    def clr_ratio(self, c0, c1):
        ratio = 0
        if c0 < c1:
            ratio = -(2000*(c1-c0)//(c1+c0))
        elif c0 > c1:
            ratio =(2000*(c0-c1)//(c1+c0))
        return ratio

    def cmp_h(self, c0, c1):
        return c1.h > c0.h

    def cmp_sl(self, c0, c1):
        return c1.sl > c0.sl

    def cmp_slr(self, c0, c1):
        return c1.sl < c0.sl

    def cmp_l(self, c0, c1):
        return c1.l > c0.l

    def cmp_lr(self, c0, c1):
        return c1.l < c0.l

    def cmp_r_g(self, c0, c1):
        return self.clr_ratio(c1.r, c1.g) < self.clr_ratio(c0.r, c0.g)

    def cmp_b_r(self, c0, c1):
        return self.clr_ratio(c1.b, c1.r) < self.clr_ratio(c0.b, c0.r)

    def cmp_b_g(self, c0, c1):
        return self.clr_ratio(c1.b, c1.g) < self.clr_ratio(c0.b, c0.g)

    def sort_clrs(self, co, b, n, cmp_fn):
        e = b+n
        for i in range(b+1, e):
            ib = b
            ie = i
            ci = co[i]
            while ib < ie:
                ip = (ib+ie)//2
                if cmp_fn(self.clrs[ci], self.clrs[co[ip]]):
                    ie = ip
                else:
                    ib = ip + 1
            # }
            ie = i
            while ie > ib:
                co[ie] = co[ie-1]
                ie -= 1
            # }
            co[ie] = ci
        # }

    def sort_colors(self, co, t, s):
        if t < 6:
            # Lightness
            self.sort_clrs(co, 0, 6*s, self.cmp_lr)
            # Saturation
            self.sort_clrs(co, 0, 3*s, self.cmp_sl)
        else:
            # Saturation
            self.sort_clrs(co, 0, 6*s, self.cmp_sl)
        # }
        # Hue
        self.sort_clrs(co, s, 5*s, self.cmp_h)
        # Red/Orange
        cmp_fn = (None,
                  self.cmp_r_g,
                  self.cmp_b_g,
                  self.cmp_b_r,
                  self.cmp_slr,
                  self.cmp_l)[t % 6]
        if cmp_fn != None:
            self.sort_clrs(co, s, 2*s, cmp_fn)
        i = 0
        while i < 1*s:
            self.clrs[co[i]].clr = 0
            i += 1
        while i < 2*s:
            self.clrs[co[i]].clr = 4
            i += 1
        while i < 3*s:
            self.clrs[co[i]].clr = 5
            i += 1
        while i < 4*s:
            self.clrs[co[i]].clr = 2
            i += 1
        while i < 5*s:
            self.clrs[co[i]].clr = 1
            i += 1
        while i < 6*s:
            self.clrs[co[i]].clr = 3
            i += 1

    def determine_colors(self, t):
        clr_ord = [0] * (NFACE*4)
        for i in range(NFACE):
            clr_ord[i] = POS(i, 8)
        self.sort_colors(clr_ord, t, 1)
        for i in range(NFACE):
            clr_ord[4*i+0] = POS(i, 0)
            clr_ord[4*i+1] = POS(i, 2)
            clr_ord[4*i+2] = POS(i, 4)
            clr_ord[4*i+3] = POS(i, 6)
        # }
        self.sort_colors(clr_ord, t, 4)
        for i in range(NFACE):
            clr_ord[4*i+0] = POS(i, 1)
            clr_ord[4*i+1] = POS(i, 3)
            clr_ord[4*i+2] = POS(i, 5)
            clr_ord[4*i+3] = POS(i, 7)
        # }
        self.sort_colors(clr_ord, t, 4)
        clr_map = [0] * NFACE
        for f in range(NFACE):
            clr_map[self.clrs[POS(f, 8)].clr] = f
        col = self.cb.col
        col[clr_map[0]] = 'w'
        col[clr_map[1]] = 'g'
        col[clr_map[2]] = 'y'
        col[clr_map[3]] = 'b'
        col[clr_map[4]] = 'r'
        col[clr_map[5]] = 'o'
        for f in range(NFACE):
            for o in range(8):
                self.set_col(f, o, clr_map[self.clrs[POS(f, o)].clr])
        # }
        return self.cb.valid_pieces()

    def set_rgb(self, f, o, rgb):
        self.clrs[POS(f, o)].set_rgb(rgb[0], rgb[1], rgb[2])

    def get_clr(self, f, o):
        clr = self.clrs[POS(f, o)]
        c = 8 # white
        if clr.sl > 50:
            c = 8*clr.h//CMAX
        return c

#    def str3(self, s):
#        return (""+str(s))[-3:]
#
#    def hsl(self, f, o):
#        c = self.clrs[POS(f,o)]
#        if o == 8:
#            p = f;
#        else:
#            p = c.pce[f][o];
#        return "["+str(p)+":"+self.str3(c.r)+" "+self.str3(c.g)+" "+self.str3(c.b)+":"+self.str3(c.h)+" "+self.str3(c.sl)+" "+self.str3(c.l)+"]"
#
#    def display_line(self, f, l):
#        if l == 0:
#            s = self.hsl(f,2)+" "+self.hsl(f,3)+" "+self.hsl(f,4)
#        elif l == 1:
#            s = self.hsl(f,1)+" "+self.hsl(f,8)+" "+self.hsl(f,5)
#        else:
#            s = self.hsl(f,0)+" "+self.hsl(f,7)+" "+self.hsl(f,6)
#        return s
#
#    def display(self):
#        for l in range(3):
#            print((" "*84)+self.display_line(4, l))
#        for l in range(3):
#            print(self.display_line(0, l)+" "+
#                self.display_line(1, l)+" "+
#                self.display_line(2, l)+" "+
#                self.display_line(3, l))
#        for l in range(3):
#            print((" "*84)+self.display_line(5, l))

#-----------------------------------------------------------------------------
# Purpose:    Color module for MindCuber-RI robot
#-----------------------------------------------------------------------------

CMAX = 1024

trace("class color")
class color():

    def __init__(self):
        self.set_rgb(0, 0, 0)

    def set_rgb(self, r, g, b):
        # Convert to hsl
        h  = 0
        s  = 0
        sl = 0
        l  = 0
        v  = r
        if g > v:
            v = g
        if b > v:
            v = b
        m = r
        if g < m:
            m = g
        if b < m:
            m = b
        vf = v+m
        l = vf//2
        if l > 0:
            vm = v-m
            if vm > 0:
                if vf <= CMAX:
                    vf = 2*CMAX-vf
                s = CMAX*vm//vf
                if r == v:
                    h = 0*CMAX+CMAX*(g-b)//vm
                elif g == v:
                    h = 2*CMAX+CMAX*(b-r)//vm
                else:
                    h = 4*CMAX+CMAX*(r-g)//vm
            h += CMAX # rotate so R/B either side of 0
            h = h//6
            if h < 0:
                h += CMAX
            elif h >= CMAX:
                h -= CMAX
            # Emphasize low saturation for bright colors (e.g. white)
            sl = CMAX*s//l
        # }
        self.r  = r
        self.g  = g
        self.b  = b
        self.h  = h
        self.sl = sl
        self.l  = l

#-----------------------------------------------------------------------------
# Purpose:    Cube mapping module for MindCuber-RI robot
#-----------------------------------------------------------------------------

NFACE    = 6
NSIDE    = 4
NSIDE_M1 = NSIDE-1

def RMOD(r):
    return r & NSIDE_M1

#-----------------------------------------------------------------------------

trace("class remap")
class remap():

    def __init__(self):
        self.fm = [-1] * NFACE
        self.rm = [-1] * NFACE

    def init_maps(self, f, r):
        self.fm[f] = r
        self.rm[r] = f

#-----------------------------------------------------------------------------

trace("class face_map")
class face_map():

    def __init__(self):
        self.face        = -1
        self.face_edge   = [-1] * NFACE
        self.face_corner = [-1] * NFACE

    def init(self, f, f0, f1, f2, f3):
        self.face = f
        self.fce  = [f0, f1, f2, f3]

    def init_rest(self):
        for d in range(NSIDE):
            f = self.fce[d].face
            self.face_edge[f]   = 2*d+1
            self.face_corner[f] = (self.face_edge[f]+1)&(2*NSIDE-1)

    def dir1(self, d):
        return self.fce[d].face

    def dir(self, f, d):
        fd = -1
        for i in range(NSIDE):
            if self.fce[i].face == f:
                m = self.fce[i]
                for j in range(NSIDE):
                    if m.fce[j].face == self.face:
                        fd = m.fce[RMOD(j+d)].face
                        break
                break
        return fd

#-----------------------------------------------------------------------------

trace("class cube_map")
class cube_map():

    def __init__(self):
        self.map = []
        self.rm  = []
        self.dst = []
        for i in range(NFACE):
            self.map.append(face_map())
            self.rm.append([])
            self.dst.append([-1] * NFACE)
            for j in range(NFACE):
                self.rm[i].append(remap())
        self.map[0].init(0, self.map[3], self.map[4], self.map[1], self.map[5])
        self.map[1].init(1, self.map[0], self.map[4], self.map[2], self.map[5])
        self.map[2].init(2, self.map[1], self.map[4], self.map[3], self.map[5])
        self.map[3].init(3, self.map[2], self.map[4], self.map[0], self.map[5])
        self.map[4].init(4, self.map[0], self.map[3], self.map[2], self.map[1])
        self.map[5].init(5, self.map[0], self.map[1], self.map[2], self.map[3])
        for i in range(NFACE):
            self.map[i].init_rest()
        for f0 in range(NFACE):
            for f1 in range(NFACE):
                self.dst[f0][f1] = 2
        ff0 = 0
        for fr0 in range(NFACE):
            self.dst[fr0][fr0] = 0
            for d0 in range(NSIDE):
                ff1 = 1
                fr1 = self.map[fr0].dir1(d0)
                self.dst[fr0][fr1] = 1
                for d1 in range(NSIDE):
                    ff2 = self.map[ff0].dir(ff1, d1)
                    fr2 = self.map[fr0].dir(fr1, d1)
                    for d2 in range(NSIDE):
                        ff3 = self.map[ff1].dir(ff2, d2)
                        fr3 = self.map[fr1].dir(fr2, d2)
                        self.rm[fr0][fr1].init_maps(ff3, fr3)

    def dir(self, f, d):
        return self.map[f].dir1(d)

    def adjacent(self, f0, f1):
        return self.dst[f0][f1] == 1

    def edge(self, f0, f1):
        return self.map[f0].face_edge[f1]

    def corner(self, f0, f1):
        return self.map[f0].face_corner[f1]

    def get_remap(self, f0, f1):
        return self.rm[f0][f1]

#-----------------------------------------------------------------------------
# Purpose:    Rubik's Cube solver for MindCuber-RI robot
#-----------------------------------------------------------------------------

NFACE    = 6
NSIDE    = 4
NSIDE_M1 = NSIDE-1
NCORNER  = NFACE*NSIDE//3
NEDGE    = NFACE*NSIDE//2

def RMOD(r):
    return r & NSIDE_M1

def RFIX(r):
    return ((r+1) & NSIDE_M1)-1

def POS(f, o):
    return f*9+o

#-----------------------------------------------------------------------------

large = False
small = False

# Use large tables if they have been downloaded
try:
    tab_fname = "/mcrimtab4_v1p1.bin"
    large = os.stat(tab_fname)[6] == 2561877
except:
    None
if not large:
    try:
        tab_fname = "/mcrimtab1_v1p1.bin"
        small = os.stat(tab_fname)[6] == 18985
    except:
        None
    if not small:
        fatal_error("no lookup tables installed")

if large:
    # Large tables
    trace("class cube_mtab4")
    class cube_mtab4:

        NSTAGE = 4    # Number of stages in solve
        NPIECE = 4    # Maximum number of corners/edges per stage

        def init(c):
            # 0
            s = c.stage(0)
            c.adde(s, 0, 1)
            c.adde(s, 0, 4)
            c.adde(s, 1, 4)
            c.addc(s, 0, 4, 1)
            c.send(s)

            # 1
            s = c.stage(s)
            c.adde(s, 0, 3)
            c.adde(s, 0, 5)
            c.adde(s, 5, 1)
            c.addc(s, 0, 1, 5)
            c.send(s)

            # 2
            s = c.stage(s)
            c.adde(s, 3, 5)
            c.adde(s, 4, 3)
            c.addc(s, 0, 3, 4)
            c.addc(s, 0, 5, 3)
            c.send(s)

            # 3
            s = c.stage(s)
            c.adde(s, 2, 1)
            c.adde(s, 2, 3)
            c.adde(s, 2, 4)
            c.addc(s, 2, 1, 4)
            c.addc(s, 2, 3, 5)
            c.addc(s, 2, 4, 3)
            c.send(s)

            # Unused stage since last corner and edge will already be solved
            s = c.stage(s)
            c.adde(s, 2, 5)
            c.addc(s, 2, 5, 1)

        mtb = (
            5, 6, 7, 9
            )

        MV_MENT = 17

    cube_mtab = cube_mtab4

    print("Using large lookup tables")

else:
    # Mini tables

    trace("class cube_mtab1")
    class cube_mtab1:

        NSTAGE = 8    # Number of stages in solve
        NPIECE = 3    # Maximum number of corners/edges per stage

        def init(c):
            # 0
            s = c.stage(0)
            c.adde(s, 2, 1)
            c.adde(s, 2, 4)
            c.send(s)

            # 1
            s = c.stage(s)
            c.adde(s, 1, 4)
            c.addc(s, 2, 1, 4)
            c.send(s)

            # 2
            s = c.stage(s)
            c.adde(s, 2, 3)
            c.adde(s, 2, 5)
            c.send(s)

            # 3
            s = c.stage(s)
            c.adde(s, 4, 3)
            c.addc(s, 2, 4, 3)
            c.send(s)

            # 4
            s = c.stage(s)
            c.adde(s, 3, 5)
            c.addc(s, 2, 3, 5)
            c.send(s)

            # 5
            s = c.stage(s)
            c.adde(s, 0, 3)
            c.adde(s, 0, 4)
            c.addc(s, 0, 3, 4)
            c.send(s)

            # 6
            s = c.stage(s)
            c.addc(s, 0, 1, 5)
            c.addc(s, 0, 4, 1)
            c.addc(s, 2, 5, 1)
            c.send(s)

            # 7
            s = c.stage(s)
            c.adde(s, 0, 1)
            c.adde(s, 5, 1)
            c.send(s)

            # Unused stage since last corner and edge will already be solved
            s = c.stage(s)
            c.adde(s, 0, 5)
            c.addc(s, 0, 5, 3)

        mtb = (
            3, 4, 4, 5, 5, 6, 7, 7
            )

        MV_MENT = 13

    cube_mtab = cube_mtab1

trace("class solve_map")
class solve_map():

    NSTAGE = cube_mtab.NSTAGE
    NPIECE = cube_mtab.NPIECE

    def __init__(self):
        # Offset into cp/ep tables for each stage
        self.cn    = [-1] * (solve_map.NSTAGE+2)
        self.en    = [-1] * (solve_map.NSTAGE+2)
        self.sz    = [-1] * solve_map.NSTAGE

        # Unrotated corner and edge positions - reverse solve order
        self.cp0= [-1] * NCORNER
        self.cp1= [-1] * NCORNER
        self.cp2= [-1] * NCORNER
        self.ep0= [-1] * NEDGE
        self.ep1= [-1] * NEDGE

        self.cn[0] = NCORNER
        self.en[0] = NEDGE

        cube_mtab.init(self)

    def addc(self, s, c0, c1, c2):
        i = self.cn[s]-1
        self.cn[s]  = i
        self.cp0[i] = c0
        self.cp1[i] = c1
        self.cp2[i] = c2

    def adde(self, s, e0, e1):
        i = self.en[s]-1
        self.en[s]  = i
        self.ep0[i] = e0
        self.ep1[i] = e1

    def stage(self, s):
        self.cn[s+1] = self.cn[s]
        self.en[s+1] = self.en[s]
        return s+1

    def send(self, s):
        msg = "STAGE: "+str((s-1))
        idx = 1
        nc  = self.cn[s-1]-self.cn[s]
        msg += " C"+str(nc)
        if nc > 0:
            i = self.cn[s]
            while (i < self.cn[s-1]):
                msg += " ["+str(self.cp0[i])+","+str(self.cp1[i])+","+str(self.cp2[i])+"]"
                idx *= 3*(i+1)
                i += 1
        ne = self.en[s-1]-self.en[s]
        msg += " E"+str(ne)
        if ne > 0:
            i = self.en[s]
            while (i < self.en[s-1]):
                msg += " ["+str(self.ep0[i])+","+str(self.ep1[i])+"]"
                idx *= 2*(i+1)
                i += 1
        if s == solve_map.NSTAGE:
            idx = idx//2
        self.sz[s-1] = idx
        # print(msg+" SZ="+str(self.sz[s-1]))

#-----------------------------------------------------------------------------

trace("class mtab")
class mtab():

    def __init__(self, s):
        self.stage  = s
        self.sz     = sm.sz[s]
        self.nbytes = cube_mtab.mtb[s]
        self.foff   = 0
        for i in range(s):
            self.foff += (sm.sz[i]-1)*cube_mtab.mtb[i]
        self.fmap = (0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5)
        self.rmap = (1, 2, -1) * NFACE

    def moves(self, i, f, r):
        mv = 0
        if i > 0:
            fs = open(tab_fname, 'rb')
            fs.seek(self.foff+(i-1)*self.nbytes)
            data = fs.read(self.nbytes)
            fs.close()
            d = 0
            b = data[d]
            d += 1
            if b != 0xFF:
                mvm = self.nbytes*2-1
                f0 = self.fmap[b]
                f[mv] = f0
                r[mv] = self.rmap[b]
                mv += 1
                while (mv < mvm):
                    b >>= 4
                    if (mv & 1) != 0:
                        b = data[d]
                        d += 1
                    b0 = b & 0xF
                    if b0 == 0xF:
                        break
                    f0 = self.fmap[b0]
                    r[mv] = self.rmap[b0]
                    if f0 >= f[mv-1]:
                        f0 += 1
                    f[mv] = f0
                    mv += 1

        return mv

#-----------------------------------------------------------------------------

trace("class cube_idx")
class cube_idx():

    def __init__(self, m = None):
        self.ci = []
        self.ei = []
        for i in range(NFACE):
            self.ci.append([0] * NFACE)
            self.ei.append([0] * NFACE)
        # pre-allocate for speed
        self.tmp_idx = [0] * solve_map.NPIECE

        self.init(m)

    def init(self, m):
        if m != None:
            for i in range(NCORNER):
                cp0 = sm.cp0[i]
                cp1 = sm.cp1[i]
                cp2 = sm.cp2[i]
                c0  = m.corner(cp0, cp1)
                c1  = m.corner(cp1, cp2)
                c2  = m.corner(cp2, cp0)
                i3  = 3*i
                self.ci[c0][c1] = i3+2
                self.ci[c1][c2] = i3+1
                self.ci[c2][c0] = i3
            # }
            for i in range(NEDGE):
                ep0 = sm.ep0[i]
                ep1 = sm.ep1[i]
                e0  = m.edge(ep0, ep1)
                e1  = m.edge(ep1, ep0)
                i2  = 2*i
                self.ei[e0][e1] = i2+1
                self.ei[e1][e0] = i2
            # }

    def index(self, s):
        idx = self.tmp_idx
        ind = 0
        cs  = sm.cn[s]
        ce  = sm.cn[s+1]
        cn  = cs - ce
        cm  = 3*cs
        for i in range(cn):
            cp0 = sm.cp0[cs-i-1]
            cp1 = sm.cp1[cs-i-1]
            ii  = self.ci[cp0][cp1]
            for j in range(i):
                if ii > idx[j]:
                    ii -= 3
            # }
            idx[i] = ii
            ind = (ind*cm)+ii
            cm  -= 3
        # }
        es = sm.en[s]
        ee = sm.en[s+1]
        en = es - ee
        em = 2*es
        for i in range(en):
            ep0 = sm.ep0[es-i-1]
            ep1 = sm.ep1[es-i-1]
            ii  = self.ei[ep0][ep1]
            for j in range(i):
                if ii > idx[j]:
                    ii -= 2
            # }
            idx[i] = ii
            ind = (ind*em)+ii
            em  -= 2
        # }
        if s == (solve_map.NSTAGE-1):
            # Minimise index when parity known
            if en > 0:
                ind = ((ind//4)*2)+(ind&1)
            else:
                ind = ((ind//6)*3)+(ind%3)
        # }
        sz  = sm.sz[s]
        ind = (sz-1-ind)
        return ind

#-----------------------------------------------------------------------------

scan_mid   = 135
scan_edg   = 105
scan_crn   = 90
scan_awy   = 40
scan_rst   = -140

scan_speed = 75
scan_pwr   = 80

turn_mul   = 60
turn_div   = 20
turn_3     = turn_mul* 3//turn_div
turn_45    = turn_mul*45//turn_div
turn_90    = turn_mul*90//turn_div

FACE       = hub.Image('60990:60990:00000:60990:60990')
FACE_LEFT  = hub.Image('60990:60990:00000:06099:06099')
FACE_RIGHT = hub.Image('06099:06099:00000:60990:60990')
FACE_BLNK0 = hub.Image('60060:60060:00000:60060:60060')
FACE_BLNK1 = hub.Image('60000:60000:00000:60000:60000')

def GetPorts():
    global c, cm, portscan
    global sensor_dist, sensor_color, motor_scan, motor_turn, motor_tilt
    c = cube()
    c.alloc_colors()
    hub.led(0, 0, 0)
    hub.display.clear()
    portscan = True
    while portscan:
        time.sleep_ms(100)
        portscan      = False
        sensor_dist   = check_port(hub.port.A, False, [62],     0, 0)
        sensor_color  = check_port(hub.port.C, False, [61],     0, 2)
        motor_scan    = check_port(hub.port.E, True,  [48, 75], 0, 4)
        motor_turn    = check_port(hub.port.D, True,  [48, 75], 4, 2)
        motor_tilt    = [
                            check_port(hub.port.B, True,  [48, 75], 4, 0),
                            check_port(hub.port.F, True,  [48, 75], 4, 4)
                        ]

def check_port(port, motor, t, x, y):
    if motor:
        dev = port.motor
    else:
        dev = port.device
    if dev != None and (port.info()['type'] in t):
        hub.display.pixel(x, y, 0)
    else:
        print("check_port: "+str(port)+" "+str(port.info()['type']))
        global portscan
        portscan = True
        hub.display.pixel(x, y, 9)
    return dev

def Position(mot):
    return mot.get()[1]

def run_wt(mot, pos, off):
    while abs(mot.get()[1]-pos) > off:
        time.sleep_ms(1)

def run_wt_up(mot, pos):
    while mot.get()[1] < pos:
        time.sleep_ms(1)

def run_wt_dn(mot, pos):
    while mot.get()[1] > pos:
        time.sleep_ms(1)

def run_wt_dir(mot, pos, off):
    if off < 0:
        while mot.get()[1] < pos:
            time.sleep_ms(1)
    else:
        while mot.get()[1] > pos:
            time.sleep_ms(1)

def run_nw(mot, pos, speed):
    mot.run_to_position(pos, speed=speed, max_power=speed, stall=False, acceleration=100, deceleration=100, stop=mot.STOP_HOLD)

def run_to(mot, pos, speed):
    mot.run_to_position(pos, speed=speed, max_power=speed, stall=False, acceleration=100, deceleration=100, stop=mot.STOP_HOLD)
    run_wt(mot, pos, 3)

def ScanReset():
    ColorOff()
    motor_scan.pwm(55)
    pos1 = Position(motor_scan)
    pos0 = pos1-100
    while pos1 > pos0:
        time.sleep_ms(100)
        pos0 = pos1
        pos1 = Position(motor_scan)
    global motor_scan_base
    motor_scan_base = Position(motor_scan)+scan_rst
    run_to(motor_scan, motor_scan_base, scan_pwr)
    motor_scan.brake()

def ScanPiece(spos, tpos, f, o, i, back = False):
    global slower
    spos += motor_scan_base
    run_nw(motor_scan, spos, 100)
    pos = Position(motor_scan)
    ScanDisp(i)
    if back:
        run_wt_dn(motor_turn, tpos+3)
    else:
        run_wt_up(motor_turn, tpos-3)
    ScanRGB(f, o)
    off = Position(motor_scan)-spos
    if pos < spos:
        if off < -5:
            slower += 1
    else:
        if off > 5:
            slower += 1

def TurnReset():
    global motor_turn_base
    motor_turn_base = Position(motor_turn)
    motor_turn.brake()

def TurnRotate(rot):
    TiltAway()
    global motor_turn_base
    motor_turn_base = motor_turn_base+turn_90*rot
    run_nw(motor_turn, motor_turn_base, 100)
    run_wt(motor_turn, motor_turn_base, turn_45)

def TurnTurn(rot, rotn):
    extra  = turn_3*4
    extran = turn_3
    if rot < 0:
        extra = -extra
    if rotn < 0:
        extra -= extran
    elif rotn > 0:
        extra += extran
    global motor_turn_base
    motor_turn_base = motor_turn_base+turn_90*rot
    pos = motor_turn_base+extra
    run_nw(motor_turn, pos, 100)
    time.sleep_ms(20)
    TiltHold()
    run_wt(motor_turn, pos, 3)
    run_nw(motor_turn, motor_turn_base, 100)

def TiltReset():
    mot0 = motor_tilt[0]
    mot1 = motor_tilt[1]
    mot0.pwm(-40)
    mot1.pwm(40)
    pos1 = [Position(mot0), Position(mot1)]
    pos0 = [pos1[0]+100, pos1[1]-100]
    while pos1[0] < pos0[0] or pos1[1] > pos0[1]:
        time.sleep_ms(200)
        pos0 = pos1
        pos1 = [Position(mot0), Position(mot1)]
    bwd0 = Position(mot0)
    bwd1 = Position(mot1)
    mot0 = motor_tilt[0]
    mot1 = motor_tilt[1]
    mot0.pwm(40)
    mot1.pwm(-40)
    pos1 = [Position(mot0), Position(mot1)]
    pos0 = [pos1[0]-100, pos1[1]+100]
    while pos1[0] > pos0[0] or pos1[1] < pos0[1]:
        time.sleep_ms(200)
        pos0 = pos1
        pos1 = [Position(mot0), Position(mot1)]
    fwd0 = Position(mot0)-3
    fwd1 = Position(mot1)+3
    global motor_tilt_fwd, motor_tilt_hld, motor_tilt_bwd
    motor_tilt_fwd = [fwd0, fwd1]
    motor_tilt_hld = [fwd0-32, fwd1+32]
    motor_tilt_bwd = [fwd0-67, fwd1+67]
    trace("tilt "+str(motor_tilt_fwd)+" "+str(motor_tilt_hld)+" "+str(motor_tilt_bwd))
    trace("bwd "+str([bwd0, bwd1]))
    if fwd0-bwd0 < 60 or bwd1-fwd1 < 60:
        fatal_error("tilt arms jammed?")
    TiltAway()

def TiltAway():
    run_nw(motor_tilt[0], motor_tilt_bwd[0], 100)
    run_nw(motor_tilt[1], motor_tilt_bwd[1], 100)
    run_wt_dn(motor_tilt[0], motor_tilt_hld[0]-6)
    run_wt_up(motor_tilt[1], motor_tilt_hld[1]+6)

def TiltHold():
    run_nw(motor_tilt[0], motor_tilt_hld[0], 100)
    run_nw(motor_tilt[1], motor_tilt_hld[1], 100)

def TiltTilt(mid0, scan = False):
    mid1 = 1-mid0
    pwr  = 100
    pwra = -40
    bwd  = -20
    fwd  = -10
    hld  = 10
    if mid0 == 1:
        pwr  = -pwr
        pwra = -pwra
        bwd  = -bwd
        fwd  = -fwd
        hld  = -hld
    run_nw(motor_tilt[mid1], motor_tilt_bwd[mid1], 100)
    if abs(Position(motor_tilt[mid0])-motor_tilt_hld[mid0])>10:
        run_to(motor_tilt[mid0], motor_tilt_hld[mid0], 100)
    run_wt_dir(motor_tilt[mid1], motor_tilt_bwd[mid1]+bwd, bwd)
    motor_tilt[mid0].pwm(pwr)
    run_wt_dir(motor_tilt[mid0], motor_tilt_fwd[mid0]+fwd, fwd)
    time.sleep_ms(100)
    motor_tilt[mid1].pwm(-pwr)
    time.sleep_ms(10)
    motor_tilt[mid0].pwm(pwra)
    if scan:
        run_nw(motor_scan, motor_scan_base+scan_mid, scan_pwr)
    run_wt_dir(motor_tilt[mid1], motor_tilt_hld[mid1]+hld, hld)
    run_nw(motor_tilt[mid0], motor_tilt_hld[mid0], 100)
    run_nw(motor_tilt[mid1], motor_tilt_hld[mid1], 100)

def ColorOff():
    sensor_color.mode(2)

def ColorOn():
    sensor_color.mode(5)

def CubeWait(img):
    global wait_count
    if wait_count <= 0:
        Show(img)
        Eyes(0,0,3,3)
        wait_count = 200
    elif wait_count == 180 or wait_count == 20:
        hub.display.clear()
        Eyes()
    elif wait_count == 160:
        Show(FACE)
    wait_count -= 1

def CubeSense():
    cm = sensor_dist.get(sensor_dist.FORMAT_SI)[0]
    # print(cm)
    return cm != None and cm < 6

def CubeRemove():
    global wait_count
    wait_count = 0
    count      = 0
    while count < 150:
        count += 1
        if CubeSense():
            count = 0
        CubeWait(hub.Image.ARROW_W)
        time.sleep_ms(10)
    Show(FACE)
    Eyes()

def CubeInsert():
    global motor_turn_base
    global wait_count
    global scramble_mode
    wait_count = 0
    hub.button.left.presses()
    hub.button.right.presses()
    count = 0
    while count < 150:
        count += 1
        if not CubeSense():
            count = 0
        CubeWait(hub.Image.ARROW_E)
        short      = True
        start_time = time.ticks_ms()
        if hub.button.left.presses() > 0:
            # print("left")
            while hub.button.left.is_pressed():
                if short and time.ticks_ms() - start_time > 1000:
                    short         = False
                    scramble_mode = True
                    Show3x3('968576895')
            if short:
                motor_turn_base -= turn_mul*2//turn_div
                run_nw(motor_turn, motor_turn_base, 40)
        if hub.button.right.presses() > 0:
            # print("right")
            while hub.button.right.is_pressed():
                if short and time.ticks_ms() - start_time > 1000:
                    short         = False
                    scramble_mode = False
                    Show3x3('999999999')
            if short:
                motor_turn_base += turn_mul*2//turn_div
                run_nw(motor_turn, motor_turn_base, 40)
        time.sleep_ms(10)
    Show(FACE)
    Eyes()

def Init():
    global scramble_mode
    scramble_mode = False
    GetPorts()
    Show(FACE)
    ScanReset()
    if CubeSense():
        CubeRemove()
    TiltReset()
    TurnReset()
    random.seed()

def Eyes(a=0, b=0, c=0, d=0):
    sensor_dist.mode(5, b''+chr(a*9)+chr(b*9)+chr(c*9)+chr(d*9))

def Show(img):
    hub.display.show(img)

def Show3x3(s):
    Show(
        hub.Image('00000:0'+s[0:3]+'0:0'+s[3:6]+'0:0'+s[6:9]+'0:00000')
    )

def ScanDisp(p):
    Show3x3(('900000000', '009000000', '000000009', '000000900',
             '090000000', '000009000', '000000090', '000900000',
             '000090000')[p])

def ScanRGB(f, o):
    rgb = sensor_color.get()
    c.set_rgb(f, o, rgb)
    rgb = ((2,0,0),
           (2,0,0),
           (2,1,0),
           (2,2,0),
           (0,2,0),
           (0,2,0),
           (0,0,2),
           (0,0,2),
           (2,2,2))[c.get_clr(f, o)]
    hub.led(rgb[0]*125, rgb[1]*20, rgb[2]*20)

def ScanFace(f, o, tilt = 1, back = False):
    global slower, scan_speed
    global motor_turn_base
    dir = scan_mid
    mid = True
    if f > 0:
        run_nw(motor_scan, motor_scan_base+scan_awy, scan_pwr)
        TiltTilt(tilt, True)
        dir -= scan_awy
        mid = False
    scanning = True
    while scanning:
        # print("FACE "+str(f))
        slower = 0
        if mid:
            run_nw(motor_scan, motor_scan_base+scan_mid, scan_pwr)
        TiltAway()
        ScanDisp(8)
        if dir > 0:
            run_wt_up(motor_scan, motor_scan_base+scan_mid-3)
        else:
            run_wt_dn(motor_scan, motor_scan_base+scan_mid+3)
        ScanRGB(f, 8)
        if back:
            motor_turn_base -= turn_90
            run_nw(motor_turn, motor_turn_base+turn_45, scan_speed)
        else:
            run_nw(motor_turn, motor_turn_base+turn_90*4, scan_speed)
        for i in range(4):
            ScanPiece(scan_crn, motor_turn_base+turn_45, f, o, i, back)
            if back:
                back = False
                run_nw(motor_turn, motor_turn_base+turn_90*4, scan_speed)
            motor_turn_base += turn_90
            ScanPiece(scan_edg, motor_turn_base, f, o+1, i+4)
            o += 2
            if o > 7:
                o = 0
        if slower > 4:
            dir = scan_mid-scan_edg
            mid = True
            scan_speed -= 1
            print("Scan speed "+str(slower)+" "+str(scan_speed))
        scanning = False
    hub.display.clear()

tiltd = 0

def SolveOrScrambleCube():
    global tiltd, scramble_mode
    scrambled = False
    while True:
        if scramble_mode:
            # print("Scrambling...")
            msg = "SCRAMBLED"
            c.scramble(2000)
            scrambled = True
            # c.display()
        CubeInsert()
        if scrambled or not scramble_mode:
            break
    ms   = time.ticks_ms()
    scan = 0
    found = scramble_mode
    while not found and scan < 3:
        ColorOn()
        ms = time.ticks_ms()
        scan += 1
        tiltd += 1
        ScanFace(0, 2)
        ScanFace(4, 4, 0)
        ScanFace(2, 4, 0, True)
        ScanFace(3, 2, 0, True)
        ScanFace(5, 6)
        ScanFace(1, 6)
        ColorOff()
        hub.led(0, 0, 0)
        Show3x3('968776897')
        run_nw(motor_scan, motor_scan_base, scan_pwr)
        TiltHold()
        Show(FACE_LEFT)
        sms = (time.ticks_ms()-ms)//100
        print("SCAN: "+str(sms//10)+"."+str(sms%10)+"s")
        t = -1
        for i in range(12):
            # print("TYPE "+str(i))
            valid = c.determine_colors(i)
            # c.display()
            if valid:
                t = i
                # print("Valid: "+str(t))
                valid = c.valid_positions()
                if valid:
                    found = True
                    break
        if not found and scan == 3 and t >= 0:
            found = c.determine_colors(t)
    # }
    if found:
        Show(FACE_RIGHT)
        if scramble_mode:
            # Cube orientation for scramble (up - white, front - green)
            d = 2
            f = 1
        else:
            # print("Solving...")
            msg = "SOLVED"
            c.solve(2000)
            # c.solve_apply()
            # c.display()
            # Cube orientation after scan
            d = 3
            f = 0
        Show(FACE)
        for mv in range(c.mv_n):
            md = c.mv_f[mv]
            mr = c.mv_r[mv]
            # print("Move ["+str(md)+" "+str(mr)+"]")
            # print("["+str(d)+" "+str(f)+"]")
            while d != md:
                rm = cm.get_remap(d, f)
                if md == rm.fm[1] or md == rm.fm[3]:
                    Show(FACE_BLNK0)
                    TiltAway()
                    Show(FACE_BLNK1)
                    if (md == rm.fm[1]) != (tiltd > 0):
                        TurnRotate(1)
                        f = rm.fm[4]
                    else:
                        TurnRotate(-1)
                        f = rm.fm[5]
                    Show(FACE_BLNK0)
                elif md == rm.fm[4] or (md == rm.fm[2] and tiltd > 0):
                    if mv % 4 == 0:
                        Show(FACE_LEFT)
                    TiltTilt(0)
                    tiltd -= 1
                    d = rm.fm[4]
                    # print("tiltd = "+str(tiltd))
                else: # md == rm.fm[5]
                    if mv % 4 == 2:
                        Show(FACE_RIGHT)
                    TiltTilt(1)
                    tiltd += 1
                    d = rm.fm[5]
                    # print("tiltd = "+str(tiltd))
                if d != md:
                    # Wait to ensure double tilt is reliable
                    time.sleep_ms(150)
            # }
            # print("["+str(d)+" "+str(f)+"]")
            mrn = 0
            mvn = mv+1
            while mvn < c.mv_n:
                if cm.adjacent(c.mv_f[mvn], md):
                    mrn = c.mv_r[mvn]
                    break
                mvn += 1
            # }
            Show(FACE)
            TurnTurn(mr, mrn)
        # }
        ms = (time.ticks_ms()-ms)//100
        print(msg+": "+str(c.mv_n)+" turns "+str(ms//10)+"."+str(ms%10)+"s")
        TiltAway()
        if c.mv_n > 0 and not scramble_mode:
            time.sleep_ms(500)
            TurnRotate(-6)
    # }
    else:
        print("Scan error:")
        c.display()
        run_nw(motor_scan, motor_scan_base, scan_pwr)
        TiltAway()
    while (motor_scan.busy(1) or
           motor_turn.busy(1) or
           motor_tilt[0].busy(1) or
           motor_tilt[1].busy(1)):
        time.sleep_ms(1)
    motor_scan.brake()
    motor_turn.brake()
    motor_tilt[0].brake()
    motor_tilt[1].brake()
    CubeRemove()

#-----------------------------------------------------------------------------

def main():
    trace("main()")
    Init()
    while True:
        SolveOrScrambleCube()

#-----------------------------------------------------------------------------

cm = cube_map()
sm = solve_map()
mt = []
for s in range(cube_mtab.NSTAGE):
    mt.append(mtab(s))
trace("initialised maps")

#-----------------------------------------------------------------------------

main()

# END