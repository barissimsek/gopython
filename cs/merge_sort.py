
def merge(left, right):
	UL = []
	i = 0
	j = 0
	k = 0

	while k < len(left) + len(right):
		if i >= len(left):
			UL.append(right[j])
			j += 1
			k += 1
			break
		if j >= len(right):
			UL.append(left[i])
			i += 1
			k += 1
			break

		if left[i] < right[j]:
			UL.append(left[i])
			i += 1
		else:
			UL.append(right[j])
			j += 1
		k += 1

	return UL

def merge_sort(ul):
	if len(ul) == 1:
		return ul

	c = int(round(len(ul) / 2))
	left = ul[:c] 			# split, left part
	right = ul[c:]			# split, right part

	print(str(left) + " : " + str(right))

	return merge(merge_sort(left), merge_sort(right))


if __name__== "__main__":
	ul = [0,99,15,33,55,21,78,18,90,43,32,58,12,17,47,93,91,72,14]
	print("Unsorted list: ", str(ul))

	sl = merge_sort(ul)
	print("Sorted list: ", str(sl))


