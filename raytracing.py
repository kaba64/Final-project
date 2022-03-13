from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt
import function

#@profile
def normalize(x):
        # This function normalizes a vector.
        #norm = 1./math.sqrt(x[0]*x[0]+x[1]*x[1]+x[2]*x[2])
        #x = x*norm
        x /= np.linalg.norm(x)
        return x
#@profile
def intersect_sphere(O, D, S, R):
        # Return the distance from O to the intersection
        # of the ray (O, D) with the sphere (S, R), or
        # +inf if there is no intersection.
        # O and S are 3D points, D (direction) is a
        # normalized vector, R is a scalar.
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
#@profile
def trace_ray(O, D):
        # Find first point of intersection with the scene.
        t = intersect_sphere(O, D, position, radius)
        # No intersection?
        if t == np.inf:
            return
        # Find the point of intersection on the object.
        M = O + D*t
        N = normalize(M - position)
        toL = normalize(L - M)
        toO = normalize(O - M)
        col = ambient
        # Lambert shading (diffuse).
        col += diffuse * max(np.dot(N, toL), 0) * color
        # Blinn-Phong shading (specular).
        col += specular_c * color_light * \
                max(np.dot(N,normalize(toL + toO)), 0) \
                ** specular_k
        return col
#@profile
def run():
        img = np.zeros((h, w, 3))
        # Loop through all pixels.
        for i, x in enumerate(np.linspace(-1, 1, w)):
            for j, y in enumerate(np.linspace(-1, 1, h)):
                # Position of the pixel.
                Q[0], Q[1] = x, y
                # Direction of the ray going through
                # the optical center.
                D = normalize(Q - O)
                # Launch the ray and get the color
                # of the pixel.
                col = trace_ray(O, D)
                if col is None:
                    continue
                img[h - j - 1, i, :] = np.clip(col, 0, 1)
        return img

# Sphere properties.
position = np.array([0., 0., 1.])
radius = 1.
color = np.array([0., 0., 1.])
diffuse = 1.
specular_c = 1.
specular_k = 50
    
# Light position and color.
L = np.array([5., 5., -10.])
color_light = np.ones(3)
ambient = .05
# Camera.
O = np.array([0., 0., -1.])  # Position.
Q = np.array([0., 0., 0.])  # Pointing to.
w, h = 50, 50  # Initial size of the screen in pixels.
refinement = int(input("Enter the number of refinement: "))
Cython_optimize = input("Use Cython optimizion; Enter y or n: ")
times = np.zeros(shape=(refinement,2))
if __name__ == "__main__":
        for k in range(refinement):
                times[k][1] = timer()
                if(Cython_optimize=="y"):
                        img = function.run_op(position,radius,color,diffuse,specular_c,specular_k,L,color_light,ambient,O,Q,w,h)        
                elif(Cython_optimize=="n"):
                        img = run()
                times[k][1] = timer()-times[k][1]
                times[k][0] = h
                h*=2
                w*=2
        per_type = "Ray"
        if(Cython_optimize=="y"):
                per_type+="_op"
        f = open(per_type+".txt", "w")
        for i in times:
                f.write(f"{i[0]}\t{i[1]}\n")
        f.close()        
        #fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        #ax.imshow(img)
        #ax.set_axis_off()
        #plt.show()
