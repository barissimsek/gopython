import sys

# Dijkstra\'s Shortest Path Algorithm: https://www.youtube.com/watch?v=pVfj6mxhdMw
# Below sample graph is from this video.

def get_root_distance(vertex, root, prev):
	if prev[vertex] == vertex:
		return 0

	root_distance = 0
	root_distance = graph[prev[vertex]].get(vertex) + get_root_distance(prev[vertex], root, prev)

	return root_distance

def get_nearest_vertex(distance, unvisited):
	unvisited_distance = { k: distance[k] for k in unvisited }

	minval = min(unvisited_distance.values())

	for k, v in unvisited_distance.iteritems():
		if v == minval:
			return k

def visit_vertex(graph, distance, unvisited, prev, root_distance, vertex):
	neighbors = graph[vertex]

	for n in neighbors:
		if n in unvisited:
			if neighbors[n] + root_distance < distance[n]:
				prev[n] = vertex
				distance[n] = neighbors[n] + root_distance

	return distance, prev

def dijkstra(graph, start, finish):
	max = sys.maxsize
	prev = {start: start}
	visited = []
	unvisited = graph.keys()

	distance = dict(zip(unvisited, len(unvisited)*[sys.maxsize]))	# default distances from the start vertex
	distance[start] = 0
	
	while unvisited:
		vertex = get_nearest_vertex(distance, unvisited)
		print("\n+++ Visiting %s +++" % vertex)
		root_distance = get_root_distance(vertex, start, prev)
		distance, prev = visit_vertex(graph, distance, unvisited, prev, root_distance, vertex)
		print("Distance matrix: ", distance)

		unvisited.remove(vertex)
		visited.append(vertex)

	return distance

if __name__ == "__main__":
	graph = {
		'a': {'b': 6, 'd': 1},
		'b': {'a': 6, 'c': 5, 'd':2, 'e':2},
		'c': {'b': 5, 'e': 5},
		'd': {'a': 1, 'b': 2, 'e': 1},
		'e': {'b': 2, 'c': 5, 'd': 1}
	}

	distance = dijkstra(graph,'a','e')

	print("\n\nResult: %s" % distance)


