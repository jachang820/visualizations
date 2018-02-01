import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider, Button

np.seterr(divide='ignore', invalid='ignore')
colors = ['steelblue', 'cornflowerblue', 'cadetblue', 'coral',
	'tomato', 'mediumturquoise', 'orange', 'lightgreen',
	'palevioletred', 'plum', 'mediumorchid', 'grey', 'gold']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
euclidean = {}
limits = [2., 0.5] # boundary, interval

def euclid(x, y, z):
	if not (x, y, z) in euclidean:
		euclidean[(x, y, z)] = np.linalg.norm([x, y, z], 2)
	return euclidean[(x, y, z)]

def plot_norm(space, limits):
	# space variables
	p = space
	bound, interval = limits
	grid = np.arange(-bound, bound, interval)
	grid = np.append(grid, grid[-1] + interval)
	points = []

	# common calculations
	zero_index = len(grid) // 2
	ax_length = len(grid)
	ax_square = ax_length * ax_length
	
	# build scale factors for just one quadrant
	scale = {(0, 0, 0): 0}
	for x in grid[zero_index : ]:
		for y in grid[zero_index : ]:
			for z in grid[zero_index : ]:
				scale[(x, y, z)] = np.divide(
					np.linalg.norm([x, y, z], p), euclid(x, y, z))
	
	# build points
	for x in grid:
		for y in grid:
			for z in grid:
				s = scale[(np.abs(x), np.abs(y), np.abs(z))]
				points.append([x*s, y*s, z*s])

	color = np.random.choice(colors)

	# hide grid lines
	ax.grid(False)

	# hide axes
	ax.set_xticks([])
	ax.set_yticks([])
	ax.w_xaxis.line.set_lw(0.)
	ax.w_yaxis.line.set_lw(0.)

	# hide figure background
	ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
	ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
	ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

	points = np.array(points)
	ax.scatter(points[:,0], points[:,1], points[:,2], alpha=0.4, s=5, c=color)

	for i in range(ax_length):
		outer = i * ax_square
		for j in range(ax_length):
			inner = outer + j * ax_length

			# line along x axis
			subset = points[i * ax_length + j : : ax_square]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c=color, linewidth=1, alpha=0.25)

			# line along y axis
			subset = points[outer + j : outer + ax_square + j: ax_length]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c=color, linewidth=1, alpha=0.25)

			# line along z axis
			subset = points[inner : inner + ax_length]
			ax.plot(subset[:,0], subset[:,1], subset[:,2], 
				c=color, linewidth=1, alpha=0.25)

		ax.set_title('Lebesgue Space Transformations', y=1.08)
		fig.canvas.draw()


plot_norm(2, limits)

current_space = 2
def update(val):
	global current_space
	current_space = pspace.val
	ax.clear()
	plot_norm(current_space, limits)

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

