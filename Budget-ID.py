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

    # dfs
    def dfsHelp(self, cur_node: Node, cur_depth: int, max_depth: int, visited: set[Node], res: set[Node]):
        # break out of the recursion if exceeds depth
        if cur_depth > max_depth:
            return
        # log out the result by depth
        self.printResult(res)
        cur_depth += 1
        for n in self.adj_list[cur_node]:
            if n not in visited:
                res.add(n)
                self.dfsHelp(n, cur_depth, max_depth, visited, res)
                res.remove(n)                                                           # backtrack

    # do dfs based on depth of a tree
    def dfs(self, depth: int):
        visited = set()
        for n in self.nodes:
            res = set()
            # initialize on first iteration since I didnt set a null node to start from
            visited.add(n)
            res.add(n)
            self.dfsHelp(n, 1, max_depth = depth, visited = visited, res = res)
        
    # call iterative deepening search with flag for display
    def ids(self, depth: int, flag):
        for i in range( 1, depth + 1):
            print("Depth = {}".format(i))
            self.dfs(i)
            print("\n")

    # log out dfs result
    def printResult(self, res: set[Node]):
        total_value = 0
        total_cost = 0
        res_string = ""
        res_string += "{"
        for r in res:
            total_value += r.value
            total_cost += r.cost
            res_string += r.name
            res_string += " "
        res_string = res_string.strip()
        res_string += "}. "
        res_string += "Value = {}. Cost = {}.".format(total_value, total_cost)
        print(res_string)

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
            # print("Node {} has ".format(nodes[i].name), end="")
            # for n in l:
                # print("{}".format(n.name), end=" ")
            # print("\n")
        return adj_list







if __name__ == "__main__":
    # read the input.txt
    input = open('input.txt', 'r')
    # parse cmd input arg
    target = int(sys.argv[1])
    budget = int(sys.argv[2])
    flag = sys.argv[3]
    ID_instance = ID(target, budget, input)
    ID_instance.ids(2, flag)

