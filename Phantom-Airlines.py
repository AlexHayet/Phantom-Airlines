import heapq
import math
from typing import List, Tuple, Dict, Set
from collections import deque

# Constant values
EMPTY = None
MIN_DIST = 3  # Minimum distance between between party members


def distance(p1, p2):
    # Computes the distance between two seats
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def distanceViolation(seats, partyMembers):
    # Checks for the proper distance between party members
    for i in range(len(partyMembers)):
        for j in range(i + 1, len(partyMembers)):
            s1 = partyMembers[i]
            s2 = partyMembers[j]
            if distance(s1, s2) < MIN_DIST:
                return True # Party members are too close to each other
    return False # Party members are spaced properly

def seatDistance(seat, assignedSeats):
    # Computes a score for distance that tells how far a seat is from other party members,
    # a higher score means a larger distance
    return sum(distance(seat, other) for other in assignedSeats)


def greedyPlacement(plane, parties):
    # Greedy algorithm that is designed to maximize party member seat distances
    rows, cols = len(plane), len(plane[0]) # Dimensions of the plane seating
    partyPositions = {} # Dictionary that is used to keep track of seating positions

    for partyID, party in enumerate(parties): # Iterate through the parties
        placed = [] # Tracks the seat positions of the members of the party that is currenty being iterated through

        for _ in party: # Place the party members
            desiredSeat = None
            bestScore = -1
            
            for r in range(rows): # Go through each seat in the plane
                for c in range(cols):
                    if plane[r][c] is EMPTY: # Checks if the seat is empty
                        score = seatDistance((r, c), placed) # Computes the score (distance) that is used against currently seated party members
                        if score > bestScore:
                            bestScore = score
                            desiredSeat = (r, c) 
                            
            if desiredSeat: # Assigns the desired seat maximizes distance from party members
                plane[desiredSeat[0]][desiredSeat[1]] = f"P{partyID}"
                placed.append(desiredSeat)
                
        partyPositions[partyID] = placed # Updates placed with the positions of the party that has been placed
    return plane, partyPositions # Returns the updates plane with the updated party seats


def astarShift(plane, partyID, positions, rows, cols):
    # If there are distance violations then this method that uses a modified A*/BFS hybrid will reposition
    # party members to locations that fulfill the minimum distance requirements
    def validity(r, c):
        # Checks for validity of a seat which in this case means if the seat is in bounds and empty
        return 0 <= r < rows and 0 <= c < cols and plane[r][c] == EMPTY

    # A* for repositioning
    size = len(positions) # Holds the amount of members that need to be reassigned seats
    frontier = deque() # Holds placements that need to be reassigned
    visited = set() # Will be used so already visited combinations are not revisited
    
    # Starting with empty seats
    initial = []
    for r in range(rows):
        for c in range(cols):
            if plane[r][c] == EMPTY:
                initial.append([(r, c)])

    for start in initial: # Seeds the frontier
        frontier.append(start)

    while frontier: # Use BFS to search through the combination of seat assignments
        current = frontier.popleft()
        if len(current) == size: # Checks if there is a violation in seating
            if not distanceViolation(plane, current):
                return current  # Found valid new seats
            continue

        for r in range(rows): # Expand search through adding another valid seat
            for c in range(cols):
                if (r, c) in current or not validity(r, c):
                    continue # Skips past seats that are already occupied or not valid
                candidate = current + [(r, c)] # Adds new seat
                if tuple(candidate) not in visited: # If the seat has not been visited
                    frontier.append(candidate) # Add the new seat configuration in order to search
                    visited.add(tuple(candidate)) # Mark it as visited

    return None  # No placement found for the party that satisfies the conditions

def seatAssignment(plane: List[List[str]], parties: List[List[str]]):
    # Assigns the seats for all parties and members using the greedy placement, and then using A* in order to fix any violations
    rows, cols = len(plane), len(plane[0])
    plane, partyPositions = greedyPlacement(plane, parties) # Calls the greedyPlacement method for assignment

    # Check for violations in seating, then fix with A* if it is needed
    for partyID, positions in partyPositions.items():
        if distanceViolation(plane, positions):
            print(f"Fixing Party {partyID}")
            for r, c in positions: # Clear violating seats
                plane[r][c] = EMPTY

            newSeat = astarShift(plane, partyID, positions, rows, cols) # Call A* to find a new seat placement that is valid
            
            if newSeat: # If the new seat is valid, 
                for r, c in newSeat:
                    plane[r][c] = f"P{partyID}"
            else:
                print(f"Warning: could not fix party {partyID}'s placement.")

    return plane # Returns the final seating arrangement

# TEST CASE 1
plane = [[EMPTY for _ in range(6)] for _ in range(6)]

# Parties (each with 3 members)
parties = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"], ["J", "K", "L"]]

result = seatAssignment(plane, parties)


for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))

# TEST CASE 2
plane = [[None for _ in range(6)] for _ in range(6)]
parties = [
    ["A", "B", "C", "D"],    # Party 0 (4 members)
    ["E", "F", "G"],         # Party 1 (3 members)
    ["H", "I"],              # Party 2 (2 members)
    ["J", "K", "L", "M"]     # Party 3 (4 members)
]

result = seatAssignment(plane, parties)

for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))

# TEST CASE 3
plane = [[None for _ in range(4)] for _ in range(4)]
parties = [["A", "B"], ["C", "D"], ["E", "F"], ["G", "H"], ["I", "J"], ["K", "L"]]

result = seatAssignment(plane, parties)

for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))

# TIMING THE TEST CASES
# Timed Test Case 1
import time

plane = [[EMPTY for _ in range(6)] for _ in range(6)]
parties = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"], ["J", "K", "L"]]

# Runtime measurement
startTime = time.time()

result = seatAssignment(plane, parties)

endTime = time.time()
runtime = endTime - startTime

for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))


print(f"\nRuntime: {runtime:.4f} seconds")

# Timed Test Case 2
import time

plane = [[EMPTY for _ in range(6)] for _ in range(6)]
parties = [
    ["A", "B", "C", "D"],    # Party 0 (4 members)
    ["E", "F", "G"],         # Party 1 (3 members)
    ["H", "I"],              # Party 2 (2 members)
    ["J", "K", "L", "M"]     # Party 3 (4 members)
]

# Runtime measurement
startTime = time.time()

result = seatAssignment(plane, parties)

endTime = time.time()
runtime = endTime - startTime

for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))


print(f"\nRuntime: {runtime:.4f} seconds")

# Timed Test Case 3
import time

plane = [[EMPTY for _ in range(6)] for _ in range(6)]
parties = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"], ["J", "K", "L"]]

# Runtime measurement
startTime = time.time()

result = seatAssignment(plane, parties)

endTime = time.time()
runtime = endTime - startTime

for row in result:
    print(" | ".join(f"{seat or ' . ':>3}" for seat in row))


print(f"\nRuntime: {runtime:.4f} seconds")
