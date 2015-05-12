import sys
from collections import deque
from heapq import heappush, heappop

# Load the txt maze file into 2D list, as well as recording starting and ending point
def loadMaze(filename):
	f = open(filename, 'r')
	maze = []
	start = []
	food_list = []
	i = 0
	for line in f:
		maze.append([])
		j = 0
		for c in line:
			if c != '\n':
				maze[i].append(c)
				if c == 'P':
					start = (i, j)
				if c == '.':
					food_list.append((i,j))
			j+=1
		i+=1
	
	f.close()
	return maze, start, food_list

# print the maze to stdout
def printMaze(maze):
	for line in maze:
		for c in line:
			print c,
		print('\n')

# display the solution
def displaySolution(filename, node_expanded, path):
	maze, start, food_list = loadMaze(filename)
	if (filename == 'smallSearch.txt' or filename == 'trickySearch.txt'):
		i = 1
		for point in path:
			if point in food_list:
				if i < 10:
					maze[point[0]][point[1]] = str(i)
				else:
					maze[point[0]][point[1]] = chr(ord('a')+i-10)
				i+=1
		printMaze(maze)
#	print path
#	print('Path cost (number of steps): %g') %(len(path)-1)
	print('Number of nodes expanded: %g') %(node_expanded)

# maze solver
def solver(filename, option):
	maze, start, food_list = loadMaze(filename)
	#print start
	#print food_list
	#printMaze(maze)
	#return
	if (len(food_list) == 0):
		return true
	solution = False
	nodes = [] # track nodes expanded
	frontier = [start] # track the frontier
	path = [] # track the actual path to the goal
	visited = [] # track the visited nodes
	if option == 'A':
		print 'A star search:'
		path, node_expanded = Astar(maze, start, food_list)
		displaySolution(filename, node_expanded, path)

# A* search method
def Astar(maze, start, food_list):
	closedset = set() # The set of nodes already evaluated.
	openset = set() # The set of tentative nodes to be evaluated, initially containing the start node
	openset.add(start)
	came_from = {} # parents of the node

	g_score = {}
	g_score[start] = 0 	# Cost from start along best known path.
	# Estimated total cost from start to goal through y
	f_score = {}
	f_score[start] = g_score[start] + AstarHeuristics(start, food_list)
	node_expanded = 0
	path = []

	while (len(openset) > 0):
		# get the node with lowest f score
		current = getLowestNode(openset, food_list, g_score)
		# check if reaching the goal state
		if (current in food_list) and len(food_list) == 1:
			#return reconstruct_path(current, came_from, food_list), node_expanded
			path.append(current)
			return path, node_expanded
		# remove current from openset
		openset.remove(current)
		# if current is in food list, remove it from food list
		if current in food_list:
			food_list.remove(current)
			path.append(current)
		# increment the node expanded number
		node_expanded += 1
		# add current to the closedset
		closedset.add(current)
		# find all the neighbors of the current node
		neighbors = findNeighbors(current, maze, closedset)
		for neighbor in neighbors:
			tenta_g_score = g_score[current] + 1
			if neighbor not in openset:
				# update parent information
				came_from[neighbor] = current
				# update heuristic scores
				g_score[neighbor] = tenta_g_score
				f_score[neighbor] = g_score[neighbor] + AstarHeuristics(neighbor, food_list)
				openset.add(neighbor)

	return False

# get the path from current to the ancestors
def reconstruct_path(current, came_from, food_list):
	total_path = [current]
	while current in came_from:
		current = came_from[current]
		total_path.append(current)
	return total_path

# return the node with lowest heuristic value
def getLowestNode(openset, food_list, g_score):
	max_value = sys.maxint
	for t in openset:
		f_score = g_score[t] + AstarHeuristics(t, food_list)
		if f_score < max_value:
			candidate = t
			max_value = f_score
	return candidate
	
# calcualte manhattan distance
def manhattan(node, end):
	return abs(node[0] - end[0]) + abs(node[1] - end[1])

# calculate heuristics
def AstarHeuristics(node, foodList):
	distance = 0.

	if (len(foodList)==0):
		return distance

	# calculate the distance between each node,using manhattan distance
	distList = []
	allNodesList = foodList[:]

	# add the current node to the list
	allNodesList.insert(0,node)

	# generate the dictionary of distance between two food dots
	for food1 in allNodesList:
		node_distance = {}
		for food2 in allNodesList:
			node_distance[food2] = manhattan(food1, food2)
		distList.append(node_distance)

	# store the shortest distance from the node to the MST
	lowt = []

	# store shorest path node
	clot = []
	for node in allNodesList:
		lowt.append(distList[0][node])
		clot.append(node)

	count = 1
	while count<len(allNodesList):
		tmpLow = lowt[:]
		tmpLow.sort(cmp=None, key=None, reverse=False)
		tmpSubLow = tmpLow[count:]
      
		lowCostNodeIndex = lowt.index(tmpSubLow[0])
		lowt[lowCostNodeIndex] = 0
      
		theLowCostNode = allNodesList[lowCostNodeIndex]
      
		# update the values of lowt and clot
		for node in allNodesList:
			if distList[lowCostNodeIndex][node] < lowt[allNodesList.index(node)]:
				lowt[allNodesList.index(node)] = distList[lowCostNodeIndex][node]
				clot[allNodesList.index(node)] = theLowCostNode
      
		count += 1
  
	index = 0
	#calculate sum of each edge in MST
	for node in allNodesList:
		distance += distList[index][clot[index]]
		index += 1

	return distance

def findNeighbors(node, maze, closedset):
	neighbors = []
	# down neighbor
	down = (node[0]+1, node[1])
	if (down not in closedset) and (maze[down[0]][down[1]] != '%'):
		neighbors.append(down)
	# left neighbor
	left = (node[0], node[1]-1)
	if (left not in closedset) and (maze[left[0]][left[1]] != '%'):
		neighbors.append(left)
	# up neighbor
	up = (node[0]-1, node[1])
	if (up not in closedset) and (maze[up[0]][up[1]] != '%'):
		neighbors.append(up)
	# right neighbor
	right = (node[0], node[1]+1)
	if (right not in closedset) and (maze[right[0]][right[1]] != '%'):
		neighbors.append(right)

	return neighbors

# Main function
def main():
	if (len(sys.argv) != 3):
		print("usage: python multiple_dots.py option{dfs, bfs, greedy, A} mazefile")
		print('\n')
		sys.exit(1)
	option = sys.argv[1]
	mazefile = sys.argv[2]
	solver(mazefile, option)

if __name__ == '__main__':
	main()
