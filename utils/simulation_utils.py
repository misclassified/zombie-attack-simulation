import pandas as pd
import numpy as np
from geopy import distance
from scipy.spatial.distance import euclidean
from sklearn.metrics import pairwise_distances
import sys
sys.path.append("..")
from agents.agents import Survivor, Removed, Zombie



def move_one_random_step(start_lat, start_lon, km):

    # Select a random theta
    random_theta = np.random.choice(
        np.linspace(0, 2*np.pi, 1000))

    # Find new random coordinates
    a_n = start_lat + (0.013*km) * np.cos(random_theta)
    b_n = start_lon + (0.013*km) * np.sin(random_theta)

    dist = distance.distance((start_lat, start_lon), (a_n, b_n)).meters

    return dist, a_n, b_n

def find_all_zombie_positions(population):

    zombies = list(filter(
        lambda x: x['type'].__str__() == 'Zombie', population))

    positions = []

    for z in zombies:
        pos = (z['id'], (z['type'].latitude, z['type'].longitude))
        positions.append(pos)

    return positions


def find_all_survivors_positions(population):

    survivors = list(filter(
        lambda x: x['type'].__str__() == 'Survivor', population))

    positions = []

    for s in survivors:
        pos = (s['id'], (s['type'].latitude, s['type'].longitude))
        positions.append(pos)

    return positions

def inherit_zombie_attributes(player):

    new_state = Removed()

    new_state.latitude = player.latitude
    new_state.longitude = player.longitude
    new_state.age = player.age

    return new_state

def inherit_survivor_attributes(player):

    new_state = Zombie()

    new_state.latitude = player.latitude
    new_state.longitude = player.longitude
    new_state.old_path = player.path
    new_state.age = player.age

    return new_state

def find_pairwise_distances(population):

    zombies = find_all_zombie_positions(population)
    survivors = find_all_survivors_positions(population)

    z_pos = [x[1] for x in zombies]
    s_pos = [x[1] for x in survivors]
    matches = pairwise_distances(X=z_pos, Y=s_pos)

    return zombies, survivors, matches

def find_matches(matches, threshold_distance):

    surv_meeting_zombies = np.where(matches <= threshold_distance)
    meetings = list(zip(surv_meeting_zombies[0], surv_meeting_zombies[1]))

    return meetings

def run_duels(meetings):

    # Based on the meeting there will be duels
    duels = np.random.choice([0,1,-1], size = len(meetings), p=[0.4,0.3,0.3])
    outcomes = list(filter(lambda x: x[0] != 0, list(zip(duels, meetings))))

    # Find which zombies and survivors are dead
    dead_survivors = list(filter(lambda x: x[0] == 1, outcomes))
#     print(dead_survivors)

    dead_zombies = list(filter(lambda x: x[0] == -1, outcomes))

    return dead_survivors, dead_zombies
