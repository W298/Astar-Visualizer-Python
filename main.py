import tkinter as tk


class Node:
    def __init__(self, i, j, renderer):
        self.renderer = renderer
        self.index = (i, j)
        self.parent = None
        self.is_start = False
        self.is_goal = False
        self.blocked = False
        self.f = 0
        self.g = 0
        self.h = 0


class NodeRender:
    def __init__(self, i, j, canvas, box_size):
        self.index = (i, j)
        self.master_canvas = canvas
        self.box_size = box_size
        self.node = Node(i, j, self)
        self.center_position = (box_size[0] / 2 + self.index[0] * box_size[0],
                                box_size[1] / 2 + self.index[1] * box_size[1])
        self.rect_obj = self.create_rect(i, j, box_size)
        self.text_F = self.create_text(0)
        self.text_G = self.create_text(1)
        self.text_H = self.create_text(2)

    def create_rect(self, i, j, box_size, color = 0):
        c = "#ffffff"
        if color == 1:
            c = "#08f26e"
        elif color == 2:
            c = "#B53737"
        elif color == 3:
            c = "black"
        elif color == 4:
            c = "blue"

        return self.master_canvas.create_rectangle(i * box_size[0], j * box_size[1],
                                                   i * box_size[0] + box_size[0],
                                                   j * box_size[1] + box_size[1],
                                                   outline='black', width=3, fill=c)

    def update_color(self, color):
        self.master_canvas.delete(self.rect_obj)
        self.rect_obj = self.create_rect(self.index[0], self.index[1], self.box_size, color)

    def create_text(self, type):
        font_size = '0'
        value = 0
        offset = (0, 0)

        if type == 0:
            font_size = '35'
            value = self.node.f
            offset = (0, 10)
        elif type == 1:
            font_size = '22'
            value = self.node.g
            offset = (-25, -25)
        else:
            font_size = '22'
            value = self.node.h
            offset = (25, -25)

        return self.master_canvas.create_text(self.center_position[0] + offset[0],
                                              self.center_position[1] + offset[1],
                                              text=value, anchor=tk.CENTER,
                                              font=('Arial', font_size))

    def update_text(self):
        self.master_canvas.delete(self.text_F)
        self.master_canvas.delete(self.text_G)
        self.master_canvas.delete(self.text_H)
        self.text_F = self.create_text(0)
        self.text_G = self.create_text(1)
        self.text_H = self.create_text(2)


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.box_size = (100, 100)
        self.n = (7, 4)

        self.width = self.box_size[0] * self.n[0]
        self.height = self.box_size[1] * self.n[1]

        self.canvas = tk.Canvas(self, bg='#ffffff', width=self.width, height=self.height)

        self.canvas.bind('<Button-1>', self.left_button)
        self.canvas.bind('<Button-3>', self.right_button)

        self.OPEN = []
        self.CLOSED = []
        self.PATH = []

        self.start_node = None
        self.goal_node = None

        self.matrix = [[]]
        self.setup_matrix()

        self.canvas.focus_set()
        self.canvas.pack()
        self.pack()

        # self.auto_search()
        # self.update()

    def auto_search(self):
        while len(self.OPEN) != 0:
            min_node = None
            min_f = 10000
            for node in self.OPEN:
                self.set_fgh(node)
                if node.f == min_f:
                    if node.h < min_node.h:
                        min_node = node
                        min_f = node.f
                elif node.f < min_f:
                    min_node = node
                    min_f = node.f

            if min_node.is_goal:
                self.OPEN.remove(min_node)
                self.CLOSED_Add(min_node)
                self.find()
                break

            self.search(min_node.index[0], min_node.index[1])

    def OPEN_Add(self, node):
        self.OPEN.append(node)
        node.renderer.update_color(1)

    def CLOSED_Add(self, node):
        self.CLOSED.append(node)
        node.renderer.update_color(2)

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
        g = parent.g + self.get_dist(node.index, parent.index)
        h = self.get_dist(node.index, self.goal_node.index)
        f = g + h
        return f, g, h

    def neighbor_node(self, node):
        i = node.index[0] - 1
        j = node.index[1] - 1

        n_list = []
        for _i in range(3):
            for _j in range(3):
                if 0 <= i + _i <= self.n[0] - 1:
                    if 0 <= j + _j <= self.n[1] - 1:
                        n_list.append(self.matrix[i+_i][j+_j].node)

        n_list.remove(self.matrix[i + 1][j + 1].node)
        return n_list

    def set_fgh(self, node):
        f, g, h = self.calc_fgh(node, node.parent)
        node.f = f
        node.g = g
        node.h = h

    def search(self, i, j):
        node = self.matrix[i][j].node
        self.OPEN.remove(node)
        self.CLOSED_Add(node)

        for n_node in self.neighbor_node(node):
            if n_node in self.CLOSED or n_node.blocked:
                continue

            if n_node not in self.OPEN or n_node.f > self.calc_fgh(n_node, node)[0]:
                n_node.parent = node
                f, g, h = self.calc_fgh(n_node, n_node.parent)
                n_node.f = f
                n_node.g = g
                n_node.h = h
                if n_node not in self.OPEN:
                    self.OPEN_Add(n_node)

    def find(self):
        node = self.goal_node
        path = []
        while node is not None:
            path.append(node)
            if node.is_start:
                break
            node = node.parent

        self.PATH = list(reversed(path))
        for node in self.PATH:
            node.renderer.update_color(4)

    def add_block_node(self, i, j):
        self.matrix[i][j].node.blocked = True
        self.matrix[i][j].update_color(3)

    def set_start_node(self, i, j):
        self.start_node = self.matrix[i][j].node
        self.start_node.parent = self.start_node
        self.matrix[i][j].node.is_start = True
        self.set_fgh(self.matrix[i][j].node)

    def set_goal_node(self, i, j):
        self.goal_node = self.matrix[i][j].node
        self.matrix[i][j].node.is_goal = True

    def init_node(self):
        self.set_goal_node(6, 1)
        self.set_start_node(1, 3)

        self.add_block_node(3, 1)
        self.add_block_node(4, 1)
        self.add_block_node(4, 2)

        self.OPEN_Add(self.start_node)

    def left_button(self, event):
        i = event.x // self.box_size[0]
        j = event.y // self.box_size[1]

        if self.matrix[i][j].node.is_goal:
            self.OPEN.remove(self.goal_node)
            self.CLOSED_Add(self.goal_node)
            self.find()
            self.update()
            return

        self.search(i, j)
        self.update()

    def right_button(self, event):
        self.update()

    def setup_matrix(self):
        for i in range(0, self.n[0]):
            temp_list = []
            for j in range(0, self.n[1]):
                temp_list.append(self.create_node_render(i, j))
            if i == 0:
                self.matrix[0] = temp_list.copy()
            else:
                self.matrix.append(temp_list.copy())

        self.init_node()
        self.update_node_render()

    def create_node_render(self, i, j):
        nr = NodeRender(i, j, self.canvas, self.box_size)
        return nr

    def update_node_render(self):
        for i in range(self.n[0]):
            for j in range(self.n[1]):
                self.matrix[i][j].update_text()

    def update(self):
        self.update_node_render()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('A_Star')
    game = Game(root)
    game.mainloop()
