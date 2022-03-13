import numpy as np
import math
cimport numpy as cnp
cimport cython

def normalize(x):
    cdef double sq
    sq = x[0]*x[0]+x[1]*x[1]+x[2]*x[2]
    return x/math.sqrt(sq)
    
def intersect_sphere(O, D, S, R):
    cdef double a, b, c, disc, distSqrt, q, t, t0, t1, tol
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 \
            else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf

def trace_ray(position,radius,color,diffuse,specular_c,specular_k,L,color_light,ambient,O, D):
    cdef double coe1, coe2
    t = intersect_sphere(O, D, position, radius)
    if t == np.inf:
        return
    M = O + np.multiply(D,t)
    N = normalize(M - position)
    toL = normalize(L - M)
    toO = normalize(O - M)
    coe1 = diffuse*max(np.dot(N, toL), 0)
    coe2 = specular_c * max(np.dot(N,normalize(toL + toO)), 0)** specular_k
    return (ambient+coe1*color+coe2*color_light)
    
def run_op(position,radius,color,diffuse,specular_c,specular_k,L,color_light,ambient,O,Q,w,h):
    cdef unsigned int i, j
    cdef double x, y
    cdef cnp.ndarray[cnp.float64_t,ndim=3] img = np.zeros((h, w, 3),dtype=np.double)
    
    for i, x in enumerate(np.linspace(-1, 1, w)):
        for j, y in enumerate(np.linspace(-1, 1, h)):
            Q[0], Q[1] = x, y
            D = normalize(Q - O)
            col = trace_ray(position,radius,color,diffuse,specular_c,specular_k,L,color_light,ambient,O, D)
            if col is None:
                continue
            img[h - j - 1, i, :] = np.clip(col, 0, 1)
    return img