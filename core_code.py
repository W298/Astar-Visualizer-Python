import operator
import sys


class Node:
    def __init__(self, index):
        self.index = index
        self.parent = None
        self.isBlocked = False
        self.fgh = (0, 0, 0)


class PathFinder:
    def __init__(self, size, start_index, goal_index, blocked_list):
        self.NODES = [[]]
        self.OPEN = []
        self.CLOSED = []
        self.PATH = []
        self.start_node = None
        self.goal_node = None

        self.setup_nodes(size[0], size[1])
        self.set_start_goal(start_index, goal_index)
        self.set_blocked(blocked_list)

    def setup_nodes(self, w, h):
        for i in range(w):
            temp_list = []
            for j in range(h):
                node = Node((i, j))
                temp_list.append(node)
            if i == 0:
                self.NODES[0] = temp_list.copy()
            else:
                self.NODES.append(temp_list.copy())

    def set_start_goal(self, start_index, goal_index):
        self.start_node = self.NODES[start_index[0]][start_index[1]]
        self.goal_node = self.NODES[goal_index[0]][goal_index[1]]

        self.start_node.parent = self.start_node
        self.start_node.fgh = self.calc_fgh(self.start_node, self.start_node)
        self.OPEN.append(self.start_node)

    def set_blocked(self, index_list):
        for index in index_list:
            self.NODES[index[0]][index[1]].isBlocked = True

    def get_dist(self, i1, i2):
        dx = abs(i1[0] - i2[0])
        dy = abs(i1[1] - i2[1])

        if dx == 0:
            return dy * 10
        elif dy == 0:
            return dx * 10

        if dx == dy:
            return dx * 14
        elif dx > dy:
            return (dx - dy) * 10 + dy * 14
        else:
            return (dy - dx) * 10 + dx * 14

    def calc_fgh(self, node, parent):
        g = parent.fgh[1] + self.get_dist(node.index, parent.index)
        h = self.get_dist(node.index, self.goal_node.index)
        f = g + h
        return f, g, h

    def get_current_node(self):
        min_f = sys.maxsize
        min_node = None
        for n in self.OPEN:
            self.calc_fgh(n, n.parent)
            if n.fgh[0] == min_f:
                if n.fgh[2] < n.fgh[2]:
                    min_node = n
                    min_f = n.fgh[0]
            elif n.fgh[0] < min_f:
                min_node = n
                min_f = n.fgh[0]

        return min_node

    def get_neighbor_node(self, node):
        i = node.index[0] - 1
        j = node.index[1] - 1

        n_list = []
        for _i in range(3):
            for _j in range(3):
                if 0 <= i + _i <= len(self.NODES[0]) - 1:
                    if 0 <= j + _j <= len(self.NODES) - 1:
                        n_list.append(self.NODES[i + _i][j + _j])

        n_list.remove(self.NODES[i + 1][j + 1])
        return n_list

    def search(self):
        while len(self.OPEN) != 0:
            current_node = self.get_current_node()
            self.OPEN.remove(current_node)
            self.CLOSED.append(current_node)

            if current_node is self.goal_node:
                self.trace()
                return

            for n_node in self.get_neighbor_node(current_node):
                if n_node in self.CLOSED or n_node.isBlocked:
                    continue

                if n_node.fgh[0] > self.calc_fgh(n_node, current_node)[0] or n_node not in self.OPEN:
                    n_node.parent = current_node
                    n_node.fgh = self.calc_fgh(n_node, n_node.parent)
                    if n_node not in self.OPEN:
                        self.OPEN.append(n_node)

    def trace(self):
        current_node = self.goal_node
        path = []
        while current_node is not None:
            path.append(current_node)
            if current_node is self.start_node:
                break
            current_node = current_node.parent

        self.PATH = list(reversed(path))
        for n in self.PATH:
            print(n.index)


if __name__ == '__main__':
    blocked_index_list = [(3, 1), (4, 1), (4, 2), (4, 3), (3, 3), (3, 4), (3, 0), (6, 2)]
    pathfinder = PathFinder((8, 7), (1, 2), (6, 1), blocked_index_list)

    pathfinder.search()
