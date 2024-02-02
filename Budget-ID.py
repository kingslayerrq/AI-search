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

    def checkNode(self, n: Node, res: set[Node]) -> bool:
        cur_cost = 0
        for r in res:
            cur_cost += r.cost
        return True if cur_cost + n.cost <= self.budget else False

    # dfs
    def dfsHelp(
        self,
        cur_node: Node,
        cur_depth: int,
        max_depth: int,
        visited: set[Node],
        res: set[Node],
        flag: bool,
    ):
        # break out of the recursion if exceeds depth
        if cur_depth > max_depth:
            return
        cur_depth += 1
        res.add(cur_node)

        # log out the result by depth
        result_string = self.getResultString(res)
        if flag:
            print(result_string)
        if self.checkResult(res):
            if flag: print("\n")
            print("Found solution ", result_string)
            sys.exit(0)

        for n in self.adj_list[cur_node]:
            # make sure the node is valid to add (not exceeding the budget), not visited, hasn't appeared in the result set
            if n not in visited and self.checkNode(n, res) and n not in res:
                res.add(n)
                self.dfsHelp(n, cur_depth, max_depth, visited, res, flag)
                res.remove(n)  # backtrack

    # do dfs based on depth of a tree
    def dfs(self, depth: int, flag: bool):
        visited = set()
        for n in self.nodes:
            res = set()
            # initialize on first iteration since I didnt set a null node to start from
            visited.add(n)
            self.dfsHelp(n, 1, max_depth=depth, visited=visited, res=res, flag=flag)

    # call iterative deepening search with flag for display
    def ids(self, depth: int, flag: bool):
        for i in range(1, depth + 1):
            if flag:
                print("Depth = {}".format(i))
            self.dfs(i, flag)
            if flag:
                print("\n")
        # no solution
        print("No Solution")
        sys.exit(0)

    # format the result to result string
    def getResultString(self, res: set[Node]) -> str:
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
        return res_string

    # check result
    def checkResult(self, res: set[Node]) -> bool:
        total_value = 0
        total_cost = 0
        for r in res:
            total_value += r.value
            total_cost += r.cost
        return (
            True if total_cost <= self.budget and total_value >= self.target else False
        )

    # construct nodes from input file content
    def constructNodes(self, input_content) -> list[Node]:
        nodes = []
        lines = input_content.readlines()
        # instatiate nodes
        for line in lines:
            split_line = line.split()
            # log an err if the input file is malformatted and exit the app
            if len(split_line) != 3:
                print("Input file formatted incorrectly!!!", file=sys.stderr)
                sys.exit(0)
            nodes.append(Node(split_line[0], split_line[1], split_line[2]))
        # for n in nodes:
        # print("Node {}, Cost {}, Value {}".format(n.name, n.cost, n.value))
        return nodes

    # construct Adjacency list
    def constructAdjList(
        self, budget: int, nodes: list[Node]
    ) -> dict[Node, list[Node]]:
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
    input = open("input.txt", "r")
    # parse cmd input arg
    if len(sys.argv) != 4:
        print("Invalid arg count!!", file=sys.stderr)
        sys.exit(0)
    target = int(sys.argv[1])
    budget = int(sys.argv[2])
    flag = sys.argv[3]
    # parse flag
    if flag == "V":
        flag = True
    elif flag == "C":
        flag = False
    else:
        print("Invalid flag input!!", file=sys.stderr)
        sys.exit(0)
    # construct instance of ID
    ID_instance = ID(target, budget, input)
    # do ids based on max num of branching factor
    ID_instance.ids(len(ID_instance.nodes), flag)
