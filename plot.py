import numpy as np
import matplotlib.pyplot as plt

datadir    = ''
plt.figure(figsize=(8.5, 6))

dataname     = "Ray.txt"
dataname_op  = "Ray_op.txt"
time         = np.loadtxt(dataname)
time_op      = np.loadtxt(dataname_op)
plt.plot(time[:,0],time[:,1],'-.',color='blue')
plt.plot(time_op[:,0],time_op[:,1],'-.',color='green')
plt.legend(("Ray Tracing Engine","Ray Tracing Engine with Cython optimization"),
	   loc='best', prop={'size': 15})
plt.xlabel(r"$n$",fontsize=18)
plt.ylabel(r"$Run time$",fontsize=18)
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.savefig("compare_op_Ray.png")
#plt.show()
