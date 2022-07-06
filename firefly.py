import matplotlib.pyplot as plt
import imageio
import numpy as np
import math

# Box boundries
xlim = [0, 1]
ylim = [0, 1]
zlim = [0, 1]

# When an ff emits light, how long is it lit (in seconds)? 
light_time = 1

# Frame rate of movie made at the end of this script
fps = 30

# How much to raise prob of lighting with every frame that we don't light up
# To change the prob of lighting up between files, I draw a number from 0 to 1 and multiply it by p_light_increment
p_light_increment = 0.00003
#p_light_increment = 0.01

# Number of frames to be lit 
light_frames = math.ceil(light_time * fps)

# How far away can a firefly see?
sight_distance = 0.4

# how likely are you to light up if you see a lit up firefly? 
p_light_on_sight = 0.05

# how many frames between lightings for one firefly?
refrac_pd = 100

class firefly:
	"""
	A single firefly. Parameters:
	x, y, z  - numeric. x, y, and z coordinates respectively. Between 0 and 1.
	light - boolean. is the fly lit up in this moment?
	p_light - numeric; between 0 and 1. Probability of the fly lighting up in the next frame
	last_fire - integer; the last integer at which the fly lit up. 
	p_light_multiplier – numeric; multiplier by which p_light_increment is multiplied to give different flies different light rates
	"""
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.light = 0.005
		self.p_light = 0
		self.last_fire = 0
		self.D = 0.01
		self.light_left = light_frames
		self.p_light_multiplier = np.random.uniform()

def make_firefly(ff_dict, iteration):
	ff = firefly(np.random.uniform(), np.random.uniform(), np.random.uniform())
	ff_dict[iteration] = ff
	return ff_dict

def check_boundary(position, lower_bound, upper_bound):
	"""
	Check if a firefly is within the bounds of the box. If not, reflect it into the box space.
	Takes three arguments: 
	the current position of the firefly in a specific dimension (x,y,z)
	The lower boundary in that dimension
	The upper boundary in that dimension
	Returns a number, which is the position, either kept as is if in bounds or reflected into the box if out
	"""
	if position < lower_bound:
		position = lower_bound - (position - lower_bound)
	elif position > upper_bound:
		position = upper_bound - (position - upper_bound)
	return position 

def light(bugs, current_frame):
	"""
	Function takes in as input a dictionary of bugs. Randomly determines which ones light up.
	Adjusts lighting probabilities for unlit bugs.
	"""
	for ff in bugs:
		if bugs[ff].light == 0:
			# Randomly determine if we light up
			do_we_light = np.random.uniform()
			if do_we_light < bugs[ff].p_light:
				# If we light then:
				# Update light status to true
				# Set current frame as the last time this ff lit up
				# Reset the probability of lighting to 0
				bugs[ff].light = 1
				bugs[ff].last_fire = current_frame 
				bugs[ff].p_light = 0
			else: 
				bugs[ff].p_light += np.random.uniform() * p_light_increment * bugs[ff].p_light_multiplier
		else: 
			bugs[ff].light_left -= 1
			if bugs[ff].light_left == 0: 
				bugs[ff].light = 0
				bugs[ff].light_left = light_frames

	return bugs

def walk(bugs):
	for ff in bugs:
		x_disp = np.random.randn(1)*bugs[ff].D
		y_disp = np.random.randn(1)*bugs[ff].D
		z_disp = np.random.randn(1)*bugs[ff].D

		x_pos = bugs[ff].x + x_disp
		y_pos = bugs[ff].y + y_disp
		z_pos = bugs[ff].z + z_disp

		# Check positions
		bugs[ff].x = float(check_boundary(x_pos, xlim[0], xlim[1]))
		bugs[ff].y = float(check_boundary(y_pos, ylim[0], ylim[1]))
		bugs[ff].z = float(check_boundary(z_pos, zlim[0], zlim[1]))

	return bugs

def radius(p1, p2):
	"""
	Takes two points and returns the distance between them. 
	Each point is a firefly-class object.
	This is pretty trivial, but also doing this as a function makes the code for find_radii much more legible. 
	"""
	return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def light_on_sight(bugs, current_frame):
	"""
	Takes a dictionary of positions and returns a list of all the pairwise distances between elements
	List is formatted as [[x1,y1,z1], [x2,y2,z2], etc.]
	"""
	# Find radii between all positions
	lit_bugs = []
	unlit_bugs = []
	nearby_unlit = []
	for ff in bugs:
		if bugs[ff].light == 1:
			lit_bugs.append(ff)
		else:
			unlit_bugs.append(ff)

	for lit_ff in lit_bugs:
		for unlit_ff in unlit_bugs:
			if (radius(bugs[lit_ff], bugs[unlit_ff]) < sight_distance) and ((current_frame - bugs[unlit_ff].last_fire > 100) or (current_frame < 100)):
				nearby_unlit.append(unlit_ff)
				unlit_bugs.remove(unlit_ff)

	for ff_in_sight in nearby_unlit:
		do_we_light = np.random.uniform()
		if do_we_light < p_light_on_sight:
			# If we light then:
			# Update light status to true
			# Set current frame as the last time this ff lit up
			# Reset the probability of lighting to 0
			bugs[ff_in_sight].light = 1
			bugs[ff_in_sight].last_fire = current_frame 
			bugs[ff_in_sight].p_light = 0
			nearby_unlit.remove(ff_in_sight)

	return bugs


	



	#return pd.DataFrame(l, columns = ['p1_idx', 'p2_idx', 'distance'])

# Function plots a single firefly and savces the 
def plot_fireflies(step_number, bugs):
	# initialize 3D plot 
	# Background color 
	plt.style.use('dark_background')
	fig = plt.figure(figsize=(12,8), dpi= 100)
	ax = plt.axes(projection='3d')

	# Remove grey pannel color
	ax.w_xaxis.pane.fill = False
	ax.w_yaxis.pane.fill = False
	ax.w_zaxis.pane.fill = False

	# For this time point, extract all of the coordinates to be plotted 
	plt_x = []
	plt_y = []
	plt_z = []
	#color = []

	for ff in bugs:
		# Only plot lit flies
		if bugs[ff].light == 1:
			plt_x.append(bugs[ff].x)
			plt_y.append(bugs[ff].y)
			plt_z.append(bugs[ff].z)
		#color.append(v.color)

	ax.scatter3D(plt_x, plt_y, plt_z, c = "#8ed847", s = [2 + y * 10 for y in plt_x])
	ax.scatter3D(plt_x, plt_y, plt_z, c = "#8ed847", s = [2 + y * 100 for y in plt_x], alpha=0.3)
	ax.scatter3D(plt_x, plt_y, plt_z, c = "#8ed847", s = [2 + y * 20 for y in plt_x], alpha=0.18)
	ax.scatter3D(plt_x, plt_y, plt_z, c = "#8ed847", s = [2 + y * 400 for y in plt_x], alpha=0.05)
	# Change view angle
	ax.view_init(0, 0)
	# Change camera distance 
	ax.dist = 4.7


	plt.xlim([0, 1])
	plt.ylim([0, 1])
	ax.set_zlim([0, 1])

	# Hid tick labels and lines
	ax.xaxis.set_ticklabels([])
	ax.yaxis.set_ticklabels([])
	ax.zaxis.set_ticklabels([])
	for line in ax.xaxis.get_ticklines():
		line.set_visible(False)
	for line in ax.yaxis.get_ticklines():
		line.set_visible(False)
	for line in ax.zaxis.get_ticklines():
		line.set_visible(False)
	# Hide grid
	ax.grid(False)
	plt.axis('off')


	
	# create filename and save figure
	fname="out/fig_"+str(step_number)
	plt.savefig(fname)
	plt.close()

	return fname

ff_dict = {}
N_bugs = 13
for i in range(N_bugs):
	ff_dict = make_firefly(ff_dict, i)

fnames = []
for i in range(1000):
	ff_dict = walk(ff_dict)
	ff_dict = light(ff_dict, i)
	bugs = light_on_sight(ff_dict, i)
	fnames.append(plot_fireflies(i, ff_dict))
	
# convert images to movie
frames = []  

for img in fnames:
	frames.append(imageio.imread(img + '.png'))
imageio.mimwrite('mv.mp4', frames, '.mp4', fps=fps)


