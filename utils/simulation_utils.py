import pandas as pd
import numpy as np
from functools import wraps
from time import time

from geopy import distance
from scipy.spatial.distance import euclidean
from sklearn.metrics import pairwise_distances
import sys
sys.path.append("..")
from agents.agents import Survivor, Removed, Zombie
import quadkey



def timing(f):
    """Decorator to measure time execution of a function
    From https://codereview.stackexchange.com/questions/169870/decorator-to-measure-execution-time-of-a-function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('Elapsed time: {}'.format(end-start))
        return result

    return wrapper


def move_one_random_step(
    start_lat, start_lon, km, iterations = 3, bbox=None, get_distance=False, verbose=False):


    # Select a random theta
    random_theta = np.random.choice(
        np.linspace(0, 2*np.pi, 1000))

    # Find new random coordinates
    a_n = start_lat + (0.013*km) * np.cos(random_theta)
    b_n = start_lon + (0.013*km) * np.sin(random_theta)


    if bbox:
        iteration = 1
        valid_move = False
        while valid_move is False and iteration <= iterations:

            if (a_n > bbox['min_lat'] and
                a_n < bbox['max_lat'] and
                b_n > bbox['min_lon'] and
                b_n < bbox['max_lon']):
                valid_move = True

            else:
                iteration += 1
                a_n = start_lat + (0.013*(km/iteration) * np.cos(random_theta))
                b_n = start_lon + (0.013*(km/iteration) * np.sin(random_theta))
                if verbose:
                    print("Finding valid position, iter {}".format(iteration))

        # If still not within bounding box then go back to start
        if (a_n > bbox['min_lat'] and
            a_n < bbox['max_lat'] and
            b_n > bbox['min_lon'] and
            b_n < bbox['max_lon']):
            pass
        else:
            a_n = start_lat
            b_n = start_lon
            if verbose:
                print('Moved out bounding box, going back to default')
                print('----------------')

    if get_distance:
        dist = distance.distance((start_lat, start_lon), (a_n, b_n)).meters
    else:
        dist = np.nan

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

def inherit_survivor_attributes(player, zombie_speed_ratio):

    new_state = Zombie()

    new_state.latitude = player.latitude
    new_state.longitude = player.longitude
    new_state.old_path = player.path
    new_state.age = player.age
    new_state.speed = player.speed * zombie_speed_ratio

    return new_state

@timing
def find_pairwise_distances(population, quadkey_level):

    zombies = find_all_zombie_positions(population)
    survivors = find_all_survivors_positions(population)

    zb_qk = list(set([quadkey.from_geo(x[1], quadkey_level) for x in zombies]))
    print("{} Zombies".format(len(zombies)))
    candidate_survivors = list(
        filter(lambda x: quadkey.from_geo(x[1], quadkey_level) in zb_qk, survivors))
    print("{} Candidate Survivors".format(len(candidate_survivors)))

    z_pos = [x[1] for x in zombies]
    s_pos = [x[1] for x in survivors]
    matches = pairwise_distances(X=z_pos, Y=s_pos)

    return zombies, survivors, matches

def find_matches(matches, threshold_distance):

    surv_meeting_zombies = np.where(matches <= threshold_distance)
    meetings = list(zip(surv_meeting_zombies[0], surv_meeting_zombies[1]))

    return meetings

def run_duels(meetings, survival_prob, zombie_prob, removal_prob):

    prob = [survival_prob, zombie_prob, removal_prob]

    # Based on the meeting there will be duels
    duels = np.random.choice([0,1,-1], size = len(meetings), p=prob)
    outcomes = list(filter(lambda x: x[0] != 0, list(zip(duels, meetings))))

    # Find which zombies and survivors are dead
    dead_survivors = list(filter(lambda x: x[0] == 1, outcomes))
#     print(dead_survivors)

    dead_zombies = list(filter(lambda x: x[0] == -1, outcomes))

    return dead_survivors, dead_zombies
