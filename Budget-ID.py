import sys

class Node:
    def __init__(self, name: str, value: int, cost: int):
        self.name = name
        self.cost = int(cost)
        self.value = int(value)

class ID:
    def __init__(self, target: int, budget: int, input):
        self.target = target
        self.budget = budget
        self.nodes = self.constructNodes(input)
        self.adj_list = self.constructAdjList(self.budget, self.nodes)

    # ids
    def ids(self, flag):

        return

    # dfs
    def dfsHelp(self, cur_node: Node, cur_depth: int, max_depth: int, visited: set[Node]):
        # break out of the recursion if exceeds depth
        if len(visited) == max_depth:
            # print("broke!")
            return
        print("curdepth: {} maxdepth: {}".format(cur_depth, max_depth), end="")
        print("Visited: ", end="")
        visited.add(cur_node)
        for v in visited:
            print(v.name, end=" ")
        print("\n")
        cur_depth += 1
        # print("Node {} has {} avail neighbors".format(cur_node.name, len(self.adj_list[cur_node])))
        for n in self.adj_list[cur_node]:
            if n not in visited:
                # print("{} is not in visited".format(n.name))
                # print("curdepth: {} maxdepth: {}".format(cur_depth, max_depth), end="")
                self.dfsHelp(n, cur_depth, max_depth, visited)
            # else:
                # print("{} is already in visited".format(n.name))

    def dfs(self, depth: int):
        # init a new set for visited nodes
        visited_dict = {}
        for n in self.nodes:
            visited_dict[n] = set()

        print("Depth = {}".format(depth))

        for n in self.nodes:
            visited = set()
            self.dfsHelp(n, 1, depth, visited)
        


    # construct nodes from input
    def constructNodes(self, input) -> list[Node]:
        nodes = []
        lines = input.readlines()
        # instatiate nodes
        for line in lines:
            split_line = line.split()
            if len(split_line) != 3:
                return "Input file formatted incorrectly!!!"
            nodes.append(Node(split_line[0], split_line[1], split_line[2]))
        #for n in nodes:
            #print("Node {}, Cost {}, Value {}".format(n.name, n.cost, n.value))
        return nodes

    # construct Adjacency list
    def constructAdjList(self, budget: int, nodes: list[Node]) -> dict[Node, list[Node]]:
        adj_list = {}
        node_num = len(nodes)
        for i in range(node_num):
            l = []
            leftover = budget - nodes[i].cost
            for n in nodes:
                if n.cost <= leftover and n is not nodes[i]:
                    l.append(n)
            adj_list[nodes[i]] = l
            print("Node {} has ".format(nodes[i].name), end="")
            for n in l:
                print("{}".format(n.name), end=" ")
            print("\n")
        return adj_list







if __name__ == "__main__":
    # read the input.txt
    input = open('input.txt', 'r')
    # parse cmd input arg
    target = int(sys.argv[1])
    budget = int(sys.argv[2])
    flag = sys.argv[3]
    ID_instance = ID(target, budget, input)
    ID_instance.dfs(2)

