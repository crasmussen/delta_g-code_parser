layer_vertices = []
layer_codes = []
layers = []

machine_x, machine_y, machine_z, machine_e, machine_f, machine_layer = 0, 0, 0, 0, 0, 0
machine_home_x, machine_home_y, machine_home_z = 0,0,0

import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import re
from array import *



def strip_axis(line):
	string = re.sub(r'(X|Y|Z|E|F)', '', line, re.I)
	return string.rstrip()

def machine_update(x, y, z, e, f):
	global machine_x, machine_y, machine_z, machine_e, machine_f, machine_layer
	global layer_vertices
	global layer_codes
	global layers
	machine_x = x
	machine_y = y
	machine_e = e
	machine_f = f
	
	if z > 0:
		# next build layer
		layers.append((layer_vertices, layer_codes))
		layer_vertices = []
		layer_codes = []
		machine_z = z
		machine_layer += 1
	print machine_z
	
def plot_add_vertex():
	global layer_vertices
	global layer_codes

	if machine_x <> None and machine_y <> None:
		layer_vertices.append((machine_x, machine_y))
		
		if machine_e > 0:
			layer_codes.append(Path.LINETO)
		else:
			layer_codes.append(Path.MOVETO)	


f = open ('Nautilus_Gear.gcode', 'r')


#Machine state settings
extrude = False

re_g_1 = re.compile('G0*1 ', re.I)
re_g_92 = re.compile('G0*92 ', re.I)
re_g_28 = re.compile('G0*28 ', re.I)
re_x = re.compile('X\d+.\d* *', re.I)
re_y = re.compile('Y\d+.\d* *', re.I)
re_z = re.compile('Z\d+.\d* *', re.I)
re_e = re.compile('E\d+.\d* *', re.I)
re_f = re.compile('F\d+.\d* *', re.I)

for line in f:
	print line.rstrip('\r\n')
	
	#check if G1
	m = re_g_1.match(line)
	if m:
		x, y, z, e = None, None, None, None
		
		#X
		m = re_x.search(line)
		if m:
			x = strip_axis(m.group(0))
		
		#Y
		m = re_y.search(line)
		if m:
			y = strip_axis(m.group(0))
			
		#Z
		m = re_z.search(line)
		if m:
			z = strip_axis(m.group(0))
		
		#E
		m = re_e.search(line)
		if m:
			e = strip_axis(m.group(0))
		
		#F
		m = re_f.search(line)
		if m:
			f = strip_axis(m.group(0))
		
		print "G1 " + "X: " + str(x) + ", Y: " + str(y) + ", Z: " + str(z) + ", E: " + str(e) + ", F: " + str(f) + "\n\n"
		machine_update(x, y, z, e, f)
		plot_add_vertex()
		
		
	m = re_g_28.match(line)
	if m:
		#E
		m = re_e.search(line)
		if m:
			e = strip_axis(m.group(0))

	m = re_g_92.match(line)
	if m:
		#E
		m = re_e.search(line)
		if m:
			e = strip_axis(m.group(0))
			
print len(layer_vertices)

vertices = np.array(layer_vertices, float)
path = Path(vertices, layer_codes)

pathpatch = PathPatch(path, facecolor='None', edgecolor='green')

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.add_patch(pathpatch)
ax.set_title('A compound path')

ax.dataLim.update_from_data_xy(layer_vertices)
ax.autoscale_view()


plt.show()