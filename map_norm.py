import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def plot_norm(space):

	p = space
	grid = np.arange(-1.0, 1.1, 0.2)
	pt_ax = len(grid)
	points = []
	for x in grid:
		for y in grid:
			for z in grid:
				if x==0 and y==0 and z==0:
					points.append([0, 0, 0])
				else:
					scale = np.linalg.norm([x, y, z], p) / np.linalg.norm([x, y, z], 2)
					points.append([x*scale, y*scale, z*scale])

	points = np.array(points)
	ax.scatter(points[:,0], points[:,1], points[:,2], alpha=0.5, s=5)

	for i in range(pt_ax):
		setno_i = i*pt_ax*pt_ax
		for j in range(pt_ax):
			setno_j = j*pt_ax
			setno = setno_i + setno_j
			subset = points[setno : setno+pt_ax]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c='steelblue', linewidth=1, alpha=0.25)
			subset = points[setno_i + j : setno_i + pt_ax*pt_ax + j: pt_ax]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c='steelblue', linewidth=1, alpha=0.25)
			subset = points[i*pt_ax + j : : pt_ax*pt_ax]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c='steelblue', linewidth=1, alpha=0.25)

		ax.set_title('Lebesgue Space Transformations', y=1.08)
		fig.canvas.draw()


plot_norm(2)

def update(val):
	ax.clear()
	plot_norm(val)

def round_p(event):
	rounded_val = np.round(pspace.val)
	pspace.set_val(np.round(rounded_val))
	update(rounded_val)

axcolor = 'lightsteelblue'
axspace = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
pspace = Slider(axspace, 'p', 0., 30.2, valinit=2)
pspace.on_changed(update)

roundax = plt.axes([0.1, 0.05, 0.1, 0.03])
button = Button(roundax, 'Round', color=axcolor, hovercolor='0.975')
button.on_clicked(round_p)

plt.show()

