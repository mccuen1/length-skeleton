import numpy as np

arr = np.array([[1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 0, 1], [1, 1, 0, 0], [1, 1, 0, 1]])

def bfs(start):
    queue = []
    visited = []
    queue.append(start)
    visited.append(start)
    i, j = start
    arr[i, j] = 5

    while queue:
        i, j = queue.pop(0)
        if arr[i, j] == 0:
            visited.append((i, j))
            continue
        arr[i, j] = 5
        print(f"visiting cell {i},{j}")
        neighbors = []
        if i-1 > -1:
            neighbors.append((i-1, j))
        if j-1 > -1:
            neighbors.append((i, j-1))
        if i+1 < arr.shape[0]:
            neighbors.append((i+1, j))
        if j+1 < arr.shape[1]:
            neighbors.append((i, j+1))

        for index in neighbors:
            if index not in visited and index not in queue:
                queue.append(index)
        visited.append((i, j))

class Test:

    def __init__(self):
        self.a = 0
        self.b = None

    def __repr__(self):
        return f"a: {self.a}, b: {self.b}"



if __name__ == "__main__":
    test_objs = [Test() for _ in range(10)]
    print(test_objs)
    obj1 = test_objs[0]
    print(obj1)
    obj1.a = 5
    print(obj1)
    print(test_objs[0])
    print(test_objs)
    
