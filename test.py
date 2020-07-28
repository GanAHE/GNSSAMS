import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

me = 5.974 * 10 ** (24)  #  mass of the earth                                     
mm = 7.348 * 10 ** (22)  #  mass of the moon                                      
G = 6.67259 * 10 ** (-20)  #  gravitational parameter                             
re = 6378.0  #  radius of the earth in km                                         
rm = 1737.0  #  radius of the moon in km                                          
r12 = 384400.0  #  distance between the CoM of the earth and moon                 
M = me + mm

pi1 = me / M
pi2 = mm / M
mue = 398600.0  #  gravitational parameter of earth km^3/sec^2                    
mum = G * mm  #  grav param of the moon                                           
mu = mue + mum
omega = np.sqrt(mu / r12 ** 3)
nu = -129.21 * np.pi / 180  #  true anomaly angle in radian                       

x = 327156.0 - 4671
#  x location where the moon's SOI effects the spacecraft with the offset of the  
#  Earth not being at (0,0) in the Earth-Moon system                              
y = 33050.0   #  y location                                                       

vbo = 10.85  #  velocity at burnout                                               

gamma = 0 * np.pi / 180  #  angle in radians of the flight path                   

vx = vbo * (np.sin(gamma) * np.cos(nu) - np.cos(gamma) * np.sin(nu))
#  velocity of the bo in the x direction                                          
vy = vbo * (np.sin(gamma) * np.sin(nu) + np.cos(gamma) * np.cos(nu))
#  velocity of the bo in the y direction                                          

xrel = (re + 300.0) * np.cos(nu) - pi2 * r12
#  spacecraft x location relative to the earth         
yrel = (re + 300.0) * np.sin(nu)

#  r0 = [xrel, yrel, 0]                                                           
#  v0 = [vx, vy, 0]                                                               
u0 = [xrel, yrel, 0, vx, vy, 0]


def deriv(u, dt):
    n1 = -((mue * (u[0] + pi2 * r12) / np.sqrt((u[0] + pi2 * r12) ** 2
                                               + u[1] ** 2) ** 3)
        - (mum * (u[0] - pi1 * r12) / np.sqrt((u[0] - pi1 * r12) ** 2
                                              + u[1] ** 2) ** 3))
    n2 = -((mue * u[1] / np.sqrt((u[0] + pi2 * r12) ** 2 + u[1] ** 2) ** 3)
        - (mum * u[1] / np.sqrt((u[0] - pi1 * r12) ** 2 + u[1] ** 2) ** 3))
    return [u[3],  #  dotu[0] = u[3]                                              
            u[4],  #  dotu[1] = u[4]                                              
            u[5],  #  dotu[2] = u[5]                                              
            2 * omega * u[5] + omega ** 2 * u[0] + n1,  #  dotu[3] = that         
            omega ** 2 * u[1] - 2 * omega * u[4] + n2,  #  dotu[4] = that         
            0]  #  dotu[5] = 0                                                    


dt = np.arange(0.0, 320000.0, 1)  #  200000 secs to run the simulation            
u = odeint(deriv, u0, dt)
x, y, z, x2, y2, z2 = u.T

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)
PHI= np.linspace(0,2 * np.pi,100)
RM = G*M
THETA = np.linspace(0,np.pi,100)
XM = RM * np.outer(np.cos(PHI),np.sin(THETA))
YM = RM * np.outer(np.sin(PHI),np.sin(THETA))
ZM = RM * np.outer(np.ones(np.size(PHI)),np.cos(THETA))
ax.plot_surface(XM,YM,ZM)
plt.show()