import numpy as np
import matplotlib.pyplot as plt

def manhattan(puzzle, goal):
    a = abs(puzzle // 3 - goal // 3)
    b = abs(puzzle % 3 - goal % 3)
    mhcost = a + b
    return sum(mhcost[1:])

def coordinates(puzzle):
    pos = np.array(range(9))
    for p, q in enumerate(puzzle):
        pos[q] = p
    return pos

def generate_neighbors(puzzle):
    neighbors = []
    blank = puzzle.index(0)
    row, col = blank // 3, blank % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            new_puzzle = puzzle[:]
            new_puzzle[blank], new_puzzle[new_blank] = new_puzzle[new_blank], new_puzzle[blank]
            neighbors.append(new_puzzle)
    
    return neighbors

def hill_climbing(puzzle, goal):
    current_state = puzzle
    current_hn = manhattan(coordinates(current_state), coordinates(goal))
    steps = [current_state]
    heuristic_values = [current_hn]
    
    while True:
        neighbors = generate_neighbors(current_state)
        next_state = None
        next_hn = current_hn
        
        for neighbor in neighbors:
            neighbor_hn = manhattan(coordinates(neighbor), coordinates(goal))
            if neighbor_hn < next_hn:
                next_state = neighbor
                next_hn = neighbor_hn
        
        if next_state is None or next_hn >= current_hn:
            break
        
        current_state = next_state
        current_hn = next_hn
        steps.append(current_state)
        heuristic_values.append(current_hn)
    
    return steps, heuristic_values, current_hn

puzzle = []
print("Please enter the initial state of the puzzle (use 0 for the blank tile).")

for i in range(0, 9):
    x = int(input(f"Enter the value for tile {i + 1}: "))
    puzzle.append(x)

goal = []
print("\nPlease enter the goal state of the puzzle (use 0 for the blank tile).")

for i in range(0, 9):
    x = int(input(f"Enter the value for tile {i + 1}: "))
    goal.append(x)

steps, heuristic_values, final_hn = hill_climbing(puzzle, goal)

if final_hn == 0:
    print("\nGoal reached! Here are the steps:")
    for i, step in enumerate(steps):
        print(f"Step {i + 1}:")
        print(np.array(step).reshape(3, 3))
else:
    print("\nNo solution found. The algorithm encountered a local maxima or plateau.")

plt.plot(heuristic_values, marker='o', linestyle='-', color='b')
plt.title('Heuristic Values Over Time')
plt.xlabel('Step Number')
plt.ylabel('Heuristic Value (Manhattan Distance)')
plt.grid(True)
plt.show()
