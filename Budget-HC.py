import sys
import copy
import random

class Node:
    def __init__(self, name: str, value: int, cost: int):
        self.name = name
        self.cost = int(cost)
        self.value = int(value)
class HC:
    def __init__(self, target: int, budget: int, input):
        self.target = target
        self.budget = budget
        self.nodes = self.constructNodes(input)
        self.adj_list = self.constructAdjList(self.budget, self.nodes)
        self.cur_state = None
        self.cur_error_value = None

    # generate a starting state(randomly sampling from nodes list) and calculate its error value for the HC Instance
    def generateStartingState(self, flag: bool) -> None:
        res = []
        for i in self.nodes:
            if random.choice([0,1]) == 1:
                res.append(i)
        if flag:
            print("Randomly chosen starting state: ")
            print(self.getResultString(res))
        # init values for cur_state, cur_error_value
        self.cur_state = res
        self.cur_error_value = self.calculateError(self.cur_state)

    # calculate error of current state(list of nodes)
    def calculateError(self, state: list[Node]) -> int:
        """Calculate Error based on current state, an Error value of 0 means we found the solution:
        1. Don't reward if cost is less than budget or value exceeds target value
        2. Punish if cost is more than budget or value doesn't meet target value
           
        Args:
            state (list[Node]): current list of nodes chosen

        Returns:
            int: Error value
        """
        total_cost = 0
        total_value = 0
        for i in state:
            total_cost += i.cost
            total_value += i.value
        return max(0, total_cost - self.budget) + max(0, self.target - total_value)
    
    # get all neighbors
    def getNeighbors(self, state: list[Node]) -> list[list[Node]]:
        """A Neighbor can be:
        1. Remove one existing Node from the state
        2. Add a Node which is currently not in the state

        Args:
            state (list[Node]): current state

        Returns:
            list[list[Node]]: list of neighboring states
        """
        res = []
        # remove one element
        for i in state:
            cpy = state[:]
            cpy.remove(i)
            res.append(cpy)
        # append one element
        for i in self.nodes:
            if i not in state:
                cpy = state[:]
                cpy.append(i)
                res.append(cpy)
        return res
    
    # get the best(lowest error value) neighbor from all available neighbors
    def getBestNeighbor(self, neighbors: list[list[Node]]) -> list[Node]:
        """Validate neighbor list and return the neighbor that has the lowest error value that is lower than current error value

        Args:
            neighbors (list[list[Node]]): list of neighboring states

        Returns:
            list[Node]: best neighbor to move on to
        """
        local_min = self.cur_error_value
        next_state = self.cur_state
        for state in neighbors:
            err_val = self.calculateError(state=state)
            if err_val < local_min:
                local_min = err_val
                next_state = state
        return next_state

    # do hillclimb with a starting state
    def hillClimb(self, flag: bool):
        while True:
            if self.cur_error_value == 0:
                result_string = self.getResultString(self.cur_state)
                print("Found solution: ")
                print(result_string)
                sys.exit(0)
            neighbors = self.getNeighbors(self.cur_state)
            # log out all neighbors
            if flag: self.printNeighbors(neighbors=neighbors)
            next_state = self.getBestNeighbor(neighbors=neighbors)
            # when the search fails
            if next_state == self.cur_state:
                return 
            else:
                if flag:
                    print("\n")
                    print("Move to", end=" ")
                    print(self.getResultString(next_state))
                self.cur_state = next_state
                self.cur_error_value = self.calculateError(self.cur_state)
    
    def randomRestart(self, restart_num: int, flag: bool):
        for i in range(restart_num):
            if i != 0 and flag: print("\n")
            # generate starting states
            self.generateStartingState(flag)
            self.hillClimb(flag)
        # Search failed if no state was returned before exhaust all restarts
        print("Search failed.")
        
    # print all neighbors
    def printNeighbors(self, neighbors: list[list[Node]]) -> None:
        if len(neighbors) > 0:
            print("Neighbors: ")
            for n in neighbors:
                print(self.getResultString(n)) 
       
    # format the result to result string
    def getResultString(self, res: list[Node]) -> str:
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
        res_string += "Value = {}. Cost = {}. Error = {}.".format(total_value, total_cost, self.calculateError(res))
        return res_string

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
    # seed for debuging purpose
    random.seed(1)
    # read the input.txt
    input = open('input.txt', 'r')
    # parse cmd input arg
    if len(sys.argv) != 5:
        print("Invalid arg count!!", file=sys.stderr)
        sys.exit(0)
        
    target = int(sys.argv[1])
    budget = int(sys.argv[2])
    flag = sys.argv[3]
    restart_num = int(sys.argv[4])
    # parse flag
    if flag == "V":
        flag = True
    elif flag == "C":
        flag = False
    else:
        print("Invalid flag input!!", file=sys.stderr)
        sys.exit(0)
    
    HC_instance = HC(target, budget, input)
    HC_instance.randomRestart(restart_num=restart_num, flag=flag)
    
    
    
    

