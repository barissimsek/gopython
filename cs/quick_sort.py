
def quick_sort(ul):
	left = []
	right = []

	if (len(ul) == 1) or (len(ul) == 0): # no need to sort
		return ul

	pivot = ul[0]
	print("Pivot: " + str(pivot))

	for v in ul[1:]:
		if v < pivot:
			left.append(v)
		elif v > pivot:
			right.append(v)

	return quick_sort(left) + [pivot] + quick_sort(right)


if __name__== "__main__":
	ul = [0,99,15,33,55,21,78,18,90,43,32,58,12,17,47,93,91,72]
	print("Unsorted list: ", str(ul))

	sl = quick_sort(ul)
	print("Sorted list: ", str(sl))


