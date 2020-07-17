from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Create instance of a player with the world's starting room
player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

# Store rooms
rooms = {}

# Opposite / inverse directions for backtracking
inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

# List to track backwards movements through our map
reverse_path = [None]

# Initialize dictionaries and store current room and its exits
rooms[player.current_room.id] = player.current_room.get_exits()

# While the length of our rooms dictionary is less than the length of total rooms in the map
while len(rooms) < len(room_graph):
    # If player's current room is not in our rooms dictionary,
    # add it and add its respective exits
    if player.current_room.id not in rooms:
        rooms[player.current_room.id] = player.current_room.get_exits()

        # Grab the inverse of the last direction traveled so that
        # it can be removed from the exit options of the current room
        reverse_direction = reverse_path[-1]
        rooms[player.current_room.id].remove(reverse_direction)

    # When a room has no available exits, we've reached a dead end and must backtrack
    while len(rooms[player.current_room.id]) < 1:
        # Pop the last reverse direction traveled to remove it
        # from our reverse path list and add it to the traversal path,
        # then move the player in this reverse direction
        reverse_direction = reverse_path.pop()
        traversal_path.append(reverse_direction)
        player.travel(reverse_direction)

    # Pop the first available exit direction to remove it from possible exits and
    # add it to the traversal path, then add it to the end of the reverse path list
    exit_direction = rooms[player.current_room.id].pop(0)
    traversal_path.append(exit_direction)
    reverse_path.append(inverse_directions[exit_direction])

    # Move in the direction of the first available exit
    player.travel(exit_direction)

    # If there's only one room left unvisited, store the last room and its exits
    # in the rooms dictionary to avoid an error due to using pop() on an empty list
    if len(room_graph) - len(rooms) == 1:
        rooms[player.current_room.id] = player.current_room.get_exits()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
