#imports required librares
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from matplotlib.cbook import get_sample_data
from matplotlib.widgets import Slider

#point at picture with formula
im = plt.imread(get_sample_data('formula1.PNG'))

#create a window and subplot for graph
fig1 = plt.figure(1)
ax = fig1.add_subplot(1,2,1, projection='3d')

#set limits for graph
ax.set_xlim(-1.01, 1.01)
ax.set_ylim(-1.01, 1.01)
ax.set_zlim(-1.01, 1.01)

#set place for sliders
plt.subplots_adjust(left=0.35, bottom=0.4)

#set initial parameters
Nx = 10
Ny = 10
c = 3e8
f = 3e9
lam = c/f
k = 2*np.pi/lam
meanx = 0.5
meany = 0.5
dx = lam * meanx
dy = lam * meany
fi_a = 45*np.pi/180
teta_a = 45*np.pi/180

#set the settings of sliders
teta_change = plt.axes([0.25, 0.3, 0.65, 0.03])
s_teta_change = Slider(teta_change, 'fi', 0, 360, valinit=teta_a*180/np.pi, valstep=1)

fi_change = plt.axes([0.25, 0.25, 0.65, 0.03])
s_fi_change = Slider(fi_change, 'teta', 0, 180, valinit=fi_a*180/np.pi, valstep=1)

Nx_change = plt.axes([0.25, 0.2, 0.65, 0.03])
s_Nx_change = Slider(Nx_change, 'Nx', 1, 20, valinit=Nx, valstep=1)

Ny_change = plt.axes([0.25, 0.15, 0.65, 0.03])
s_Ny_change = Slider(Ny_change, 'Ny', 1, 20, valinit=Ny, valstep=1)

dx_change = plt.axes([0.25, 0.1, 0.65, 0.03])
s_dx_change = Slider(dx_change, 'dx/lam', 0.1, 4, valinit=meanx, valstep=0.05)

dy_change = plt.axes([0.25, 0.05, 0.65, 0.03])
s_dy_change = Slider(dy_change, 'dy/lam', 0.1, 4, valinit=meany, valstep=0.05)

#set arrays of azimuth and elevate angles
theta, phi = np.linspace(0, 2*np.pi, 40), np.linspace(0, 1*np.pi, 40)
THETA, PHI = np.meshgrid(theta, phi)

#the function of generating of RP
def form_rp(fi_a, teta_a, Nx, Ny, meanx, meany):

    #calculate distance between the elements
    dx = lam * meanx
    dy = lam * meany

    #calculating components of the main formula
    a = np.sin(Nx*dx*k*0.5*(np.sin(PHI)-np.sin(fi_a)))
    b = Nx*np.sin(dx*k*0.5*(np.sin(PHI)-np.sin(fi_a)))

    c = np.sin(Ny*dy*k*0.5*(np.sin(THETA)-np.sin(teta_a)))
    d = Ny*np.sin(dy*k*0.5*(np.sin(THETA)-np.sin(teta_a)))

    #creating RP
    R = abs(np.sin(PHI))*(a/b)*(c/d)
    return R

#the function of bringing to cartesean coordinates
def form_coords(R, Nx, Ny, meanx, meany):

    #forming new coordinates system
    X = R * np.sin(PHI) * np.cos(THETA)
    Y = R * np.sin(PHI) * np.sin(THETA)
    Z = R * np.cos(PHI)

    #clear subplot before redraw
    ax.cla()

    #plot draw
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), linewidth=0, antialiased=False, alpha=0.5)

    #set limits for graph
    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.4, 0.4)
    ax.set_zlim(-0.4, 0.4)

    #draw coordinate lines
    ax.plot([-1, 1], [0, 0], [0, 0], c='r')
    ax.plot([0, 0], [-1, 1], [0, 0], c='g')
    ax.plot([0, 0], [0, 0], [-1, 1], c='b')

    #draw coordinate titles
    ax.text(1, 0, 0, "X", color='red')
    ax.text(0, 1, 0, "Y", color='green')
    ax.text(0, 0, 1, "Z", color='blue')

    #drow the elements of the antenna array
    for i in range (0, Nx, 1):
        for j in range(0, Ny, 1):
            ax.scatter(meanx*(i - Nx/2)/Nx, meany*(j- Ny/2)/Ny, 0, s=1, c='black')

#reaction to the slider action
def update(val):
    fi_a = s_fi_change.val * np.pi/180
    teta_a = s_teta_change.val * np.pi/180
    Nx = int(s_Nx_change.val)
    Ny = int(s_Ny_change.val)
    meanx = s_dx_change.val
    meany = s_dy_change.val
    R = form_rp(fi_a, teta_a, Nx, Ny, meanx, meany)
    form_coords(R, Nx, Ny, meanx, meany)
    
#check the slider action
s_fi_change.on_changed(update)
s_teta_change.on_changed(update)
s_Nx_change.on_changed(update)
s_Ny_change.on_changed(update)
s_dx_change.on_changed(update)
s_dy_change.on_changed(update)

#initial drawing of the RP
R = form_rp(fi_a, teta_a, Nx, Ny, meanx, meany)
form_coords(R, Nx, Ny, meanx, meany)

#obtain the picture of the formula in the window
newax = fig1.add_axes([0.5, 0.5, 0.5, 0.5], anchor='NE', zorder=-1)
newax.imshow(im)
newax.axis('off')

#call window
plt.show()