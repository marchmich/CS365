'''
Egan White and Katrina Ziebarth
CS365 Lab A Part 1
eganwhite-katrinaziebarth-labA-part1.py
'''
import copy
import argparse
import os.path
import queue

class Mouse:
    
    def __init__(self):
        self.mouse_pos=None
        self.cheese_locations=[]
        #stores initial values for state attributes while parsing file
        self.maze_arr=[]
        self.height = 0
        self.width = 0
        self.initial_state=None
        self.heuristic_type = 'md' #default is Manhattan Distance
        
    def heuristic(self, state):
        if self.heuristic_type == 'md': #if heuristic is Manhattan Distance
            return self.manhattan_distance(state.location)
        elif self.heuristic_type == 'mds': #if heuristic is max distance sum
            return self.max_distance_sum(state)
        else:
            raise ValueError ('Heuristic type does not exist.')
    
    class State:
        def __init__(self, location, cheese_list, action):
            self.location = location
            self.cheese_list = cheese_list
            self.action = action
            
        def __hash__(self):
            return hash((self.location, str(self.cheese_list)))
            #hashes information denoting a unique state
        
        def __eq__(self, other):
            if self.location == other.location and self.cheese_list == self.cheese_list:
                    return True
            return False
            
        def print_state(self):
            print("Location: " + str(self.location))
            print("Cheese list: " + str(self.cheese_list))
            print("Action: " + str(self.action))
    
    def manhattan_distance(self, location, cheese_index=0):
        x_diff = abs(location[0] - self.cheese_locations[cheese_index][0])
        y_diff = abs(location[1] - self.cheese_locations[cheese_index][1])
        return x_diff + y_diff
    
    def combined_manhattan_distance(self, state):
        h_cheese_list = copy.deepcopy(state.cheese_list)
        total_estimate = 0
        position = state.location
        for i in range(len(h_cheese_list)):
            position = h_cheese_list[i]
            min_distance = self.height + self.width
            for j in range(len(h_cheese_list)):
                distance = self.manhattan_distance(position, i)
                if distance < min_distance and i!=j:
                    min_distance = distance
            total_estimate += min_distance
        return total_estimate
    
    def max_distance_sum(self, state):
       	position = state.location
       	max_north = 0
       	max_south = 0
       	max_east = 0
       	max_west = 0
       	for cheese in state.cheese_list:
      	    if position[1] - cheese[1] > max_north:
      		    max_north = position[1] - cheese[1]
      	    if cheese[1] - position[1] > max_south:
      		    max_south = cheese[1] - position[1]
      	    if position[0] - cheese[0] > max_west:
      		    max_west = position[0] - cheese[0]
      	    if cheese[0] - position[0] > max_east:
      		    max_east = cheese[0] - position[0]
       	if max_north < max_south:
       		max_north = max_north*2
       	else:
       		max_south = max_south*2
       	if max_east < max_west:
       		max_east = max_east*2
       	else:
       		max_west = max_west*2
        return max_north + max_south + max_east + max_west
        
        

    def transition (self, current_state, action):
        if action == "n":
            new_location=(current_state.location[0], current_state.location[1]-1)
        elif action == "e":
            new_location=(current_state.location[0]+1, current_state.location[1])
        elif action == "w":
            new_location=(current_state.location[0]-1, current_state.location[1])
        elif action == "s":
            new_location=(current_state.location[0], current_state.location[1]+1)
        else:
            raise ValueError("Action is not possible.")
        new_cheese_list=copy.deepcopy(current_state.cheese_list)
        for i in range(len(new_cheese_list)):
            if new_location==new_cheese_list[i]:
                del new_cheese_list[i] #remove cheese from new list
                break
        return self.State(new_location, new_cheese_list, action)


    def print_maze(self):
        for j in range(self.height):
            for i in range(self.width):
                print(self.maze_arr[i][j], end="")
            print('\n', end="")

    def init_maze(self, file): #initilizes maze into 2d array, gets (x, y) position of mouse and all cheeses.
        read_file=open(file, "r")
        lines=read_file.readlines()
        self.width=len(lines[0])-1 #-1 for new line
        self.height=len(lines)
        row_index=0
        #print("Width of maze: "+str(width)+" Height of maze: "+str(height))
        
        columns = []
        for j in range(self.width):
            columns.append([])
        #create list of columns
        for row in lines:
            for i in range(self.width):
                columns[i].append(row[i])
                if row[i]==".":
                    cheese_location=(i, row_index)
                    self.cheese_locations.append(cheese_location)
                elif(row[i]=="P"):
                    #print("MOUSE FOUND!!!")
                    self.mouse_pos=(i, row_index)
            row_index += 1

        #print("Mouse: "+str(self.mouse_pos))
        #print(cheese_location)
        self.initial_state= Mouse.State(self.mouse_pos, self.cheese_locations, None)
        self.maze_arr=columns


    def test_movement(self, state):
        current_state=state
        current_state.print_state()
        while(1==1):
            #print("Mouse position: \n")
            
            user_input=input("Which direction would you like to move? (n/s/e/w): ")
            current_state = self.transition(current_state, user_input)
            current_state.print_state()
            if self.goal_test(current_state)==True:
                print("All cheeses collected! Exiting...")
                return
            
            
        #print_state1
    def goal_test(self, state):
        if state.cheese_list:
        #if cheese remaining in list
            return False
        else:
        #otherwise, return true
            return True
        
        
class Node:
    def __init__(self, state, steps, action, parent):
        self.state = state
        self.steps = steps
        self.action = action
        self.parent = parent


def expand(mouse, node, v_map):
    position = node.state.location
    last_action = node.action
    if mouse.maze_arr[position[0]] [position[1]] == '.':
        last_action = None
    #last action will be ignored if cheese was at current location
    possible_actions = []
    node_list = []
    actions = ('n', 'e', 'w', 's')
    counteractions = ('s', 'w', 'e', 'n')
    new_positions = ((position[0], position[1]-1), (position[0]+1, position[1]),
        (position[0]-1, position[1]), (position[0], position[1]+1))
    for i in range(4):
        if mouse.maze_arr[new_positions[i][0]] [
                new_positions[i][1]] != '%' and last_action != counteractions[i]:
            possible_actions.append(actions[i])
    for action in possible_actions:
        child_node = Node(mouse.transition(node.state, action), node.steps+1, action, node)    
        if v_map.visited(child_node) == False:
            #child_node.state.print_state()
            #v_map.visited(child_node)
            node_list.append(child_node)
    return node_list



def solution_path(mouse, node):
    position = node.state.location
    cheese_count=len(mouse.cheese_locations)
    extra_cheeses = copy.deepcopy(mouse.cheese_locations)
    #print(position)
    map_copy = copy.deepcopy(mouse.maze_arr)
    multi = 0
    if len(mouse.cheese_locations)>1:
        multi = True
    while(node.parent!=None):
        if node.action == 'n':
            new_position = (position[0], position[1]+1)
        elif node.action == 'e':
            new_position = (position[0]-1, position[1])
        elif node.action == 'w':
            new_position = (position[0]+1, position[1])
        elif node.action == 's':
            new_position = (position[0], position[1]-1)
        if map_copy[new_position[0]] [new_position[1]] == ' ':
            map_copy[new_position[0]] [new_position[1]]='#'
        #for multiple cheese maze
        if multi == True and cheese_count > -1:
            for i in range(len(extra_cheeses)):
                if extra_cheeses[i]==position:
                    if cheese_count<11:
                        map_copy[position[0]] [position[1]] = str(cheese_count-1)
                        #print(str(cheese_count-1))
                    elif cheese_count<37:
                        map_copy[position[0]] [position[1]] = chr(cheese_count+86)
                        #print(chr(cheese_count+86))
                    elif cheese_count<63:
                        map_copy[position[0]] [position[1]] = chr(cheese_count+28)
                        #print(chr(cheese_count+54))
                    cheese_count -= 1
                    del extra_cheeses[i]
                    break
        else:
            if mouse.cheese_locations[0]==position:
                map_copy[position[0]] [position[1]] = '.'
        node = node.parent
        position = new_position
    for j in range(mouse.height):
        for i in range(mouse.width):
            print(map_copy[i][j], end="")
        print('\n', end="")


class Visited_Map:
    
    def __init__(self, mouse):
        self.columns = []
        for i in range(mouse.width):
            self.columns.append([])
            for j in range(mouse.height):
                self.columns[i].append(False)
                #appends false initially
                
                
    def visited(self, node):
        location = node.state.location
        if self.columns[location[0]] [location[1]] == True:
            return True
        else:
            return False
        
    def add(self, node):
        location = node.state.location
        self.columns[location[0]] [location[1]] = True

        
class Visited_Dict:
    
    def __init__(self, mouse):
        self.dict = {}
                             
    def visited(self, node):
        if hash(node.state) in self.dict:
            return True
        else:
            return False
        
    def add(self, node):
        self.dict[hash(node.state)] = node.state
            
                    
    


def single_dfs(file_path):
    stack=[]
    expand_count = 0
    mouse=Mouse()
    mouse.init_maze(file_path)
    v_map = Visited_Map(mouse)
    stack.append(Node(mouse.initial_state, 0, None, None))
    while(len(stack)>0):
        current=stack.pop()
        #current.state.print_state()
        if(mouse.goal_test(current.state)==False):
            expand_count+=1
            v_map.add(current)
            children = expand(mouse, current, v_map)
            for child in children:
                #child.state.print_state()
                stack.append(child)
        else:
            solution_path(mouse, current)
            print("Cost of solution: " + str(current.steps))
            break
    print("Nodes expanded: " + str(expand_count))
    
    
def single_bfs(file_path):
    search_queue = queue.Queue()
    expand_count = 0
    mouse=Mouse()
    mouse.init_maze(file_path)
    #mouse.initial_state.print_state()
    """
    if len(mouse.cheese_locations)<2:
        v_map = Visited_Map(mouse)
    else:
        v_map = Visited_Dict(mouse)
    """
    v_map = Visited_Map(mouse)
    search_queue.put(Node(mouse.initial_state, 0, None, None))
    while(search_queue.empty()==False):
        current=search_queue.get()
        while v_map.visited(current)==True:
            current=search_queue.get()
        """
        if expand_count > 100:
            print('Hi')
            current.state.print_state()
            print(expand_count)
            print(v_map.columns[current.state.location[0]][current.state.location[1]])
        if expand_count == 115:
            break
        

        #current.state.print_state()
        """
        if(mouse.goal_test(current.state)==False and v_map.visited(current)==False):
            expand_count+=1
            v_map.add(current)
            #print(v_map.visited(current))
            children = expand(mouse, current, v_map)
            #print('children')
            for child in children:
                #child.state.print_state()
                #print(v_map.visited(child))
                search_queue.put(child)
        else:
            solution_path(mouse, current)
            print("Cost of solution: " + str(current.steps))
            break
    print("Nodes expanded: " + str(expand_count))
    

class Greedy_Node:
    
    def __init__(self, mouse, node):
        self.h = mouse.heuristic(node.state)
        self.node = node
        
    def __lt__(self, other):
        if self.h < other.h:
            return True
        else:
            return False
    
    
def single_gbfs(file_path):
    search_priority_queue = queue.PriorityQueue()
    expand_count = 0
    mouse=Mouse()
    mouse.init_maze(file_path)
    mouse.heuristic_type = 'md'
    v_map = Visited_Map(mouse)
    first_greedy_node = Greedy_Node(mouse, Node(mouse.initial_state, 0, None, None))
    search_priority_queue.put(first_greedy_node)
    while(search_priority_queue.empty()==False):
        current=search_priority_queue.get().node
        #current.state.print_state()
        if(mouse.goal_test(current.state)==False):
            expand_count+=1
            v_map.add(current)
            children = expand(mouse, current, v_map)
            for child in children:
                #child.state.print_state()
                search_priority_queue.put(Greedy_Node(mouse, child))
        else:
            solution_path(mouse, current)
            print("Cost of solution: " + str(current.steps))
            break
    print("Nodes expanded: " + str(expand_count))
    


class Astar_Node:
    
    def __init__(self, mouse, node):
        self.f = mouse.heuristic(node.state) + node.steps
        self.node = node
        
    def __lt__(self, other):
        if self.f < other.f:
            return True
        else:
            return False
    


def single_astar(file_path):
    search_priority_queue = queue.PriorityQueue()
    expand_count = 0
    mouse=Mouse()
    mouse.init_maze(file_path)
    mouse.heuristic_type = 'md'
    #mouse.initial_state.print_state()
    v_map = Visited_Map(mouse)
    first_astar_node = Astar_Node(mouse, Node(mouse.initial_state, 0, None, None))
    search_priority_queue.put(first_astar_node)
    while(search_priority_queue.empty()==False):
        current=search_priority_queue.get().node
        #current.state.print_state()
        if(mouse.goal_test(current.state)==False):
            expand_count+=1
            v_map.add(current)
            children = expand(mouse, current, v_map)
            for child in children:
                #child.state.print_state()
                search_priority_queue.put(Astar_Node(mouse, child))
        else:
            solution_path(mouse, current)
            print("Cost of solution: " + str(current.steps))
            break
    print("Nodes expanded: " + str(expand_count))
    
    
    
def multi_astar(file_path):
    search_priority_queue = queue.PriorityQueue()
    expand_count = 0
    mouse=Mouse()
    mouse.init_maze(file_path)
    mouse.heuristic_type = 'mds'
    #mouse.initial_state.print_state()
    v_map = Visited_Dict(mouse)
    first_astar_node = Astar_Node(mouse, Node(mouse.initial_state, 0, None, None))
    search_priority_queue.put(first_astar_node)
    while(search_priority_queue.empty()==False):
        current=search_priority_queue.get().node
        #current.state.print_state()
        if(mouse.goal_test(current.state)==False):
            if mouse.heuristic(current.state)<0:
                print('h')
                print(mouse.heuristic(current.state))
                print('f-value')
                print(mouse.heuristic(current.state) + current.state.steps)
            expand_count+=1
            v_map.add(current)
            children = expand(mouse, current, v_map)
            for child in children:
                #child.state.print_state()
                search_priority_queue.put(Astar_Node(mouse, child))
        else:
            solution_path(mouse, current)
            print("Cost of solution: " + str(current.steps))
            break
    print("Nodes expanded: " + str(expand_count))



    
#print_maze("/Users/egray/Desktop/SCHOOL2022/AI/1prize-medium.txt")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help='input file path', type=str)
    parser.add_argument("-a", help='algorithm name', type=str)
    arguments=parser.parse_args()
    if not os.path.exists(arguments.i):
        raise ValueError("File path is not valid.")
    if arguments.a == 'single_dfs':
        single_dfs(arguments.i)
    elif arguments.a == 'single_bfs':
        single_bfs(arguments.i)
    elif arguments.a == 'single_gbfs':
        single_gbfs(arguments.i)
    elif arguments.a == 'single_astar':
        single_astar(arguments.i)
    elif arguments.a == 'multi_astar':
        multi_astar(arguments.i)