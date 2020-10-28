import tkinter as tk


class Node:
    def __init__(self, i, j):
        self.index = (i, j)
        self.parent = None
        self.is_start = False
        self.is_goal = False
        self.f = 0
        self.g = 0
        self.h = 0


class NodeRender:
    def __init__(self, i, j, render_obj, canvas, box_size):
        self.index = (i, j)
        self.master_canvas = canvas
        self.render_obj = render_obj
        self.node = Node(i, j)
        self.center_position = (box_size[0] / 2 + self.index[0] * box_size[0],
                                box_size[1] / 2 + self.index[1] * box_size[1])
        self.text_F = self.create_text(0)
        self.text_G = self.create_text(1)
        self.text_H = self.create_text(2)

    def create_text(self, type):
        font_size = '0'
        value = 0
        offset = (0, 0)

        if type == 0:
            font_size = '30'
            value = self.node.f
            offset = (0, 5)
        elif type == 1:
            font_size = '15'
            value = self.node.g
            offset = (-15, -15)
        else:
            font_size = '15'
            value = self.node.h
            offset = (15, -15)

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
        self.box_size = (60, 60)
        self.n = (10, 5)

        self.width = self.box_size[0] * self.n[0]
        self.height = self.box_size[1] * self.n[1]

        self.canvas = tk.Canvas(self, bg='#ffffff', width=self.width, height=self.height)

        self.canvas.bind('<Button-1>', self.left_button)
        self.canvas.bind('<Button-3>', self.right_button)

        self.start_node = None
        self.goal_node = None

        self.matrix = [[]]
        self.setup_matrix()

        self.OPEN = []
        self.CLOSED = []
        self.PATH = []

        self.canvas.focus_set()
        self.canvas.pack()
        self.pack()

    def OPEN_Add(self, node):
        self.OPEN.append(node)

    def calc_fgh(self, node):
        g = node.parent.g + abs(node.index[0] - node.parent.index[0]) + abs(node.index[1] - node.parent.index[1])
        h = abs(self.goal_node.index[0] - node.index[0]) + abs(self.goal_node.index[1] - node.index[1])
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

    def search(self, i, j):
        node = self.matrix[i][j].node
        f, g, h = self.calc_fgh(node)
        node.f = f
        node.g = g
        node.h = h


        for n_node in self.neighbor_node(node):
            n_node.parent = node
            f, g, h = self.calc_fgh(n_node)
            n_node.f = f
            n_node.g = g
            n_node.h = h

    def init_node(self):
        self.start_node = self.matrix[0][0].node
        self.start_node.parent = self.start_node
        self.goal_node = self.matrix[self.n[0] - 1][self.n[1] - 1].node

        self.matrix[0][0].node.is_start = True
        self.matrix[self.n[0] - 1][self.n[1] - 1].node.is_goal = True

    def left_button(self, event):
        i = event.x // self.box_size[0]
        j = event.y // self.box_size[1]

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

    def create_node_render(self, i, j):
        obj = self.canvas.create_rectangle \
            (i * self.box_size[0], j * self.box_size[1],
             i * self.box_size[0] + self.box_size[0],
             j * self.box_size[1] + self.box_size[1],
             outline='black', width=3)
        nr = NodeRender(i, j, obj, self.canvas, self.box_size)
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
