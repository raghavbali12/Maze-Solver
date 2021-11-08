import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# %matplotlib inline
import copy
import math
import heapq

'''
This code contains TA starter code from CS540: Intro to AI at the University of Wisconsin.
Starter code is called out in comments below.
'''

#Intialize the dimensions of the maze. Will need to be changed based on maze size
width, height = 57, 58
X, Y = 14, 2

#Input the maze png image as readable data
ori_img = mpimg.imread('practice_maze.png')
img = ori_img[:,:,0]

#Figure out the horizontal pattern for each row of cells in the maze
h_list = []
for vertical in range(0,len(img)-1,16): #range takes a step of 16 because that is the length of a cell
	l = []
	for block in range(0,len(img[vertical][2:]),16):
		if sum(img[vertical][block:block+16]) == 0: #If the sum of a given 16 elements is 0, that means there is a line there
			l.append('L')
		else:
			l.append('B') #If the sum is anything but 0, there is a blank space there
	h_list.append(l)

#Figure out the vertical pattern for each row of cells in the maze
v_list = []
for horizontal in range(2,len(img)-4,16):
	l = []
	for block in range(2,(len(img[horizontal][2:])),16):
		if img[horizontal][block:block+16][-2] == 0 and img[horizontal][block:block+16][-1] == 0:
			l.append('B*') #This indicates a cell with a wall on the right side
		else:
			l.append('B') #This indicates a cell with no wall on the right side
	v_list.append(l)


#Output the maze in a txt format
with open("practice_maze.txt",'a') as file:
	for l1,l2 in zip(h_list,v_list):
		h_str = "+" #initialize each horizontal and vertical row with the appropriate character
		v_str = "|"
		for n in l1:
			if n == 'L': #If the list has an L, output a line
				h_str += "--+"
			elif n == 'B': #If the list has a B, output a blank space
				h_str += "  +"
		file.write(h_str + '\n')
		for m in l2:
			if m == 'B': #If the list has a B, output a space
				v_str += "   "
			elif m == 'B*': #If the list has a B*, output a space with a wall character
				v_str += "  |"
		file.write(v_str + '\n')
	h_str = "+"
	for n in h_list[-1]:
		if n == 'L':
			h_str += "--+"
		elif n == 'B':
			h_str += "  +"
	file.write(h_str)

#Create a cell class to map out possible movement spaces
#TA code start
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.succ = ''
        self.action = ''  # which action the parent takes to get this cell
cells = [[Cell(i,j) for j in range(width)] for i in range(height)]

#For each cell in the maze, calculate the successor matrix
for i in range(height):
    succ = []
    for j in range(width):
        s = ''
        c1, c2 = i * 16 + 8, j * 16 + 8
        if img[c1-8, c2] == 1: s += 'U'
        if img[c1+8, c2] == 1: s += 'D'
        if img[c1, c2-8] == 1: s += 'L'
        if img[c1, c2+8] == 1: s += 'R'
        cells[i][j].succ = s
        succ.append(s)
#TA code end

cells[0][28].succ = cells[0][28].succ.replace('U', '') #Modified for entrance
cells[57][28].succ = cells[57][28].succ.replace('D', '') #Modified for exit


# Use BFS to find the solution
visited = set()
s1 = {(0,28)} #Entrance of maze
s2 = set() #Set to add moved cells to
while (57,28) not in visited:
    for a in s1:
        visited.add(a)
        i, j = a[0], a[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in (s1 | s2 | visited):
            s2.add((i-1,j))
            cells[i-1][j].action = 'U'
        if 'D' in succ and (i+1,j) not in (s1 | s2 | visited):
            s2.add((i+1,j))
            cells[i+1][j].action = 'D'
        if 'L' in succ and (i,j-1) not in (s1 | s2 | visited):
            s2.add((i,j-1))
            cells[i][j-1].action = 'L'
        if 'R' in succ and (i,j+1) not in (s1 | s2 | visited):
            s2.add((i,j+1))
            cells[i][j+1].action = 'R'
    s1 = s2
    s2 = set()

cur = (57,28)
s = ''
seq = []
while cur != (0,28):
    seq.append(cur)
    i, j = cur[0], cur[1]
    t = cells[i][j].action
    s += t
    if t == 'U': cur = (i+1, j)
    if t == 'D': cur = (i-1, j)
    if t == 'L': cur = (i, j+1)
    if t == 'R': cur = (i, j-1)
action = s[::-1]
seq = seq[::-1]

solution = [(0,28)]
#Plot out solution cells
for a in action:
	if a == 'U':
		new_cell = (solution[-1][0] - 1 ,solution[-1][1])
		solution.append(new_cell)
	if a == 'D':
		new_cell = (solution[-1][0] + 1 ,solution[-1][1])
		solution.append(new_cell)
	if a == 'L':
		new_cell = (solution[-1][0],solution[-1][1] - 1)
		solution.append(new_cell)
	if a == 'R':
		new_cell = (solution[-1][0], solution[-1][1] + 1)
		solution.append(new_cell)

l = list(zip(h_list,v_list))

for i in range(1,len(solution)):
	delta_h = solution[i][0] - solution[i-1][0]
	h = solution[i][0]
	w = solution[i][1]
	if delta_h == 0:
		#l[h][1][w] = 'S'
		if v_list[h][w] == 'B*':
			v_list[h][w] = 'S*'
		else:
			v_list[h][w] = 'S'
	elif delta_h == 1:
		#l[h][1][w] = 'S'
		#l[h][0][w] = 'S'
		if v_list[h][w] == 'B*':
			v_list[h][w] = 'S*'
		else:
			v_list[h][w] = 'S'
		if h_list[h][w] == 'B':
			h_list[h][w] = 'S'
	elif delta_h == -1:
		#l[h][1][w] = 'S'
		#l[h][0][w] = 'S'
		if v_list[h][w] == 'B*':
			v_list[h][w] = 'S*'
		else:
			v_list[h][w] = 'S'
		if h_list[h+1][w] == 'B':
			h_list[h+1][w] = 'S'

h_list[0][28] = 'S'
v_list[0][28] = 'S' #initializing solution
h_list[-1][28] = 'S' #initializing exit

with open("pactice_maze_solution.txt",'a') as file:
	for l1,l2 in zip(h_list,v_list):
		h_str = "+"
		v_str = "|"
		for n in l1:
			if n == 'L':
				h_str += "--+"
			elif n == 'B':
				h_str += "  +"
			elif n == 'S':
				h_str += "##+"
		file.write(h_str + '\n')
		for m in l2:
			if m == 'B':
				v_str += "   "
			elif m == 'B*':
				v_str += "  |"
			elif m == 'S':
				v_str += "## "
			elif m == 'S*':
				v_str += "##|"
		file.write(v_str + '\n')
	h_str = "+"
	for n in h_list[-1]:
		if n == 'L':
			h_str += "--+"
		elif n == 'B':
			h_str += "  +"
		elif n == 'S':
			h_str += "##+"
	file.write(h_str)

file.close()
