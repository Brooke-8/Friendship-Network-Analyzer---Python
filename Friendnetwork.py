#November 2023
#Brooke MacQuarrie, bmacq014@uottawa.ca

import random
import math

def getNumbersOfFriends(network):
    '''(2Dlist)->1D list
    Given a 2D-list for friendship network, returns a list of how many friends each ID has in network'''
    IDs = []
    for i in range(len(network)):
        IDs.append(len(network[i][1]))
    return IDs
def networkBinarySearch(user,network):
    '''(int,2Dlist)->int
    Given a 2D-list for a friendship network and user ID, performs a binary search on the network to find the index of the user ID in the network
    Precondition: user ID is in the network. 2D list sorted by the IDs'''
    userIndex = -1
    lower = 0
    upper = len(network)
    middle = (lower+upper)//2
    while network[middle][0] != user:
        if network[middle][0] < user:
            lower = middle
        elif network[middle][0] > user:
            upper = middle
        middle = (lower+upper)//2
    return middle

def create_network(file_name):
    '''(str)->list of tuples where each tuple has 2 elements the first is int and the second is list of int

    Precondition: file_name has data on social netowrk. In particular:
    The first line in the file contains the number of users in the social network
    Each line that follows has two numbers. The first is a user ID (int) in the social network,
    the second is the ID of his/her friend.
    The friendship is only listed once with the user ID always being smaller than friend ID.
    For example, if 7 and 50 are friends there is a line in the file with 7 50 entry, but there is line 50 7.
    There is no user without a friend
    Users sorted by ID, friends of each user are sorted by ID
    Returns the 2D list representing the frendship nework as described above
    where the network is sorted by the ID and each list of int (in a tuple) is sorted (i.e. each list of friens is sorted).
    '''
    friends = open(file_name).read().splitlines()
    network=[]
    numUsers = int(friends.pop(0))
    userIDs = []
    for i in range(len(friends)):
        friends[i] = friends[i].split()
        friends[i][0] = int(friends[i][0])
        if friends[i][0] not in userIDs:
            userIDs.append(friends[i][0])
        friends[i][1] = int(friends[i][1])
        if friends[i][1] not in userIDs:
            userIDs.append(friends[i][1])
    userIDs.sort()
    for i in range(numUsers):
        network.append((userIDs[i],[]))
    currentUser = friends[0][0]
    bs = 1
    for i in range(1,len(friends)):
        if (friends[i][0] == friends[i-1][0]):
            network[userIDs.index(currentUser)][1].append(friends[i-1][1])
            if currentUser not in (network[userIDs.index(friends[i-1][1])][1]):
                network[userIDs.index(friends[i-1][1])][1].append(currentUser)
        else:
            network[userIDs.index(currentUser)][1].append(friends[i-1][1])
            if currentUser not in (network[userIDs.index(friends[i-1][1])][1]):
                network[userIDs.index(friends[i-1][1])][1].append(currentUser)
            currentUser = friends[i][0]
        bs += 1
    network[userIDs.index(currentUser)][1].append(friends[bs-1][1])
    network[userIDs.index(friends[bs-1][1])][1].append(currentUser)
    return network

def getCommonFriends(user1, user2, network):
    '''(int, int, 2D list) ->list
    Precondition: user1 and user2 IDs in the network. 2D list sorted by the IDs,
    and friends of user 1 and user 2 sorted
    Given a 2D-list for friendship network, returns the sorted list of common friends of user1 and user2
    '''
    common=[]

    user1Index = networkBinarySearch(user1,network) #O(log(n))
    user2Index = networkBinarySearch(user2,network) #O(log(n))
    user1Length = len(network[user1Index][1]) #O(1)
    user2Length = len(network[user2Index][1]) #O(1)
    
    if user1Length >= user2Length: #O(1)
        for i in range(user1Length): #O(n1)
            if (network[user1Index][1][i]) in (network[user2Index][1]): #O(n1*n2)
                common.append(network[user1Index][1][i]) #O(n1*n2)
    elif user1Length <= user2Length: #O(1)
        for i in range(user2Length): #O(n2)
            if (network[user2Index][1][i]) in (network[user1Index][1]): #O(n1*n2)
                common.append(network[user2Index][1][i]) #O(n1*n2)
    return common #O(1)

# O(log(n)) + O(log(n)) + O(1) + O(1) + O(1) + O(n1) + O(n1*n2) + O(n1*n2) + O(1)
# = O(2log(n) + n1*n2) 
    

def recommend(user, network):
    '''(int, 2Dlist)->int or None
    Given a 2D-list for friendship network, returns None if there is no other person
    who has at least one neighbour in common with the given user and who the user does
    not know already.

    Otherwise it returns the ID of the recommended friend. A recommended friend is a person
    you are not already friends with and with whom you have the most friends in common in the whole network.
    If there is more than one person with whom you have the maximum number of friends in common
    return the one with the smallest ID. '''

    unknown =[[],[]]
    userIndexes = []
    for i in range(len(network)):
        if user == network[i][0]:
            userIndex = i
        userIndexes.append(network[i][0])

    userFriendAmount = len(network[userIndex][1])
    for i in range(userFriendAmount):
        friend = network[userIndex][1][i]
        friendIndex = userIndexes.index(friend)
        friendFriendAmount = len(network[friendIndex][1])
        for j in range(friendFriendAmount):
            friendFriendID = network[friendIndex][1][j]
            if (friendFriendID not in network[userIndex][1]) and (friendFriendID not in unknown[0]) and friendFriendID != user:
                unknown[0].append(friendFriendID)
                unknown[1].append(1)
            elif (friendFriendID not in network[userIndex][1]) and (friendFriendID in unknown[0]):
                unknown[1][unknown[0].index(friendFriendID)] += 1

    if len(unknown[0]) == 0:
        return None
    recommendedIndex = unknown[1].index(max(unknown[1]))
    return(unknown[0][recommendedIndex])
    #problems: also records themself as friend, missing one for 7 in net1



def k_or_more_friends(network, k):
    '''(2Dlist,int)->int
    Given a 2D-list for friendship network and non-negative integer k,
    returns the number of users who have at least k friends in the network
    Precondition: k is non-negative'''
    count = 0
    for i in range(len(network)):
        if len(network[i][1]) >= k:
            count +=1
    return count


def maximum_num_friends(network):
    '''(2Dlist)->int
    Given a 2D-list for friendship network,
    returns the maximum number of friends any user in the network has.
    '''
    return(max(getNumbersOfFriends(network)))



def people_with_most_friends(network):
    '''(2Dlist)->1D list
    Given a 2D-list for friendship network, returns a list of people (IDs) who have the most friends in network.'''
    max_friends=[]

    most = max(getNumbersOfFriends(network))
    for i in range(len(network)):
        if len(network[i][1]) == most:
            max_friends.append(network[i][0])

    return max_friends


def average_num_friends(network):
    '''(2Dlist)->number
    Returns an average number of friends overs all users in the network'''

    return(sum(getNumbersOfFriends(network))/len(getNumbersOfFriends(network)))


def knows_everyone(network):
    '''(2Dlist)->bool
    Given a 2D-list for friendship network,
    returns True if there is a user in the network who knows everyone
    and False otherwise'''

    for i in range(len(network)):
        if len(network)-1 == len(network[i][1]):
            return True
    return False


####### CHATTING WITH USER CODE:

def is_valid_file_name():
    '''None->str or None'''
    file_name = None
    try:
        file_name=input("Enter the name of the file: ").strip()
        f=open(file_name)
        f.close()
    except FileNotFoundError:
        print("There is no file with that name. Try again.")
        file_name=None
    return file_name

def get_file_name():
    '''()->str
    Keeps on asking for a file name that exists in the current folder,
    until it succeeds in getting a valid file name.
    Once it succeeds, it returns a string containing that file name'''
    file_name=None
    while file_name==None:
        file_name=is_valid_file_name()
    return file_name


def get_uid(network):
    '''(2Dlist)->int
    Keeps on asking for a user ID that exists in the network
    until it succeeds. Then it returns it'''

    userIDs = []
    userID = -1
    for i in range(len(network)):
        userIDs.append(network[i][0])
    while userID not in userIDs:
        try:
            userID = int(input("Enter an integer for a user ID: ").strip())
            if userID not in userIDs:
                print("That user ID does not exist. Try again.")
        except:
            print("That was not an integer. Please try again.")
    return(userID)


##############################
# main
##############################

file_name=get_file_name()

net=create_network(file_name)

print("\nFirst general statistics about the social network:\n")

print("This social network has", len(net), "people/users.")
print("In this social network the maximum number of friends that any one person has is "+str(maximum_num_friends(net))+".")
print("The average number of friends is "+str(average_num_friends(net))+".")
mf=people_with_most_friends(net)
print("There are", len(mf), "people with "+str(maximum_num_friends(net))+" friends and here are their IDs:", end=" ")
for item in mf:
    print(item, end=" ")

print("\n\nI now pick a number at random.", end=" ")
k=random.randint(0,len(net)//4)
print("\nThat number is: "+str(k)+". Let's see how many people has that many friends.")
print("There is", k_or_more_friends(net,k), "people with", k, "or more friends")

if knows_everyone(net):
    print("\nThere at least one person that knows everyone.")
else:
    print("\nThere is nobody that knows everyone.")

print("\nWe are now ready to recommend a friend for a user you specify.")
print("(Enter ID num between 0 and",len(net),")")
uid=get_uid(net)
rec=recommend(uid, net)
if rec==None:
    print("We have nobody to recommend for user with ID", uid, "since he/she is dominating in their connected component")
else:
    print("For user with ID", uid,"we recommend the user with ID",rec)
    print("That is because users", uid, "and",rec, "have", len(getCommonFriends(uid,rec,net)), "common friends and")
    print("user", uid, "does not have more common friends with anyone else.")


print("\nFinally, you showed interest in knowing common friends of some pairs of users.")
print("About 1st user ...")
uid1=get_uid(net)
print("About 2st user ...")
uid2=get_uid(net)
print("Here is the list of common friends of", uid1, "and", uid2)
common=getCommonFriends(uid1,uid2,net)
for item in common:
    print(item, end=" ")

