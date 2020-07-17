import random
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    # Fisher Yates Shuffle from randomness lesson
    def fisher_yates_shuffle(self, l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) - 1)
            l[random_index], l[i] = l[i], l[random_index]

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users based on number of users passed in
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        # Make a list with all possible friendships
        friendships = []

        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users + 1):
                friendship = (user, friend)
                friendships.append(friendship)

        # Shuffle the list with Fisher Yates Shuffle
        self.fisher_yates_shuffle(friendships)

        # Take as many friendships as we need based on our average number
        total_friendships = num_users * avg_friendships

        random_friendships = friendships[:total_friendships//2]

        # Add to self.friendships
        for friendship in random_friendships:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """

        # Instructor Solution

        # Plan: BFT, use dictionary as visited

        visited = {}  # Note that this is a dictionary, not a set

        q = Queue()
        q.enqueue([user_id])

        # while q isn't empty
        while q.size() > 0:
            # dequeue the current path
            current_path = q.dequeue()

            # grab last vertex from path (current user)
            current_user = current_path[-1]

            # if it hasn't been visited,
            if current_user not in visited:
                # add to our visited dictionary
                visited[current_user] = current_path

                friends = self.friendships[current_user]

                # then enqueue paths to each of our neighbors
                for friend in friends:
                    path_to_friend = current_path + [friend]

                    q.enqueue(path_to_friend)

        return visited

        # # Create a queue for BFS to determine shortest path
        # q = Queue()

        # # Enqueue the path to the passed in user
        # q.enqueue([user_id])

        # # While items are in the queue
        # while q.size() > 0:
        #     # Dequeue the current path
        #     path = q.dequeue()

        #     if not visited.get(path[-1], None):
        #         visited[path[-1]] = path

        #         for friend in self.friendships[path[-1]]:
        #             friend_path = list(path)
        #             friend_path.append(friend)
        #             q.enqueue(friend_path)

        # return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
