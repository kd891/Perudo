'''Perudo optimal bet calculation'''
import random as rd
import collections as c
import math
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt


class Player_Scores:

    def __init__(self, name, num_dice):
        self.num_dice = num_dice

    def player_dice(self):
        num_dice = self.num_dice
        player_vals = []
        for i in range (num_dice):
            dice = rd.randint(1,6)
            player_vals.append(dice)

        return player_vals

        #print(player_vals)
def count_ones(freqs):
    for freq in freqs:
        if freq[0] == 1:
            return freq[1]




def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur.

    thanks to @MarkDickinson for providing this function

    """

    dividers = sorted(rd.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def constrained_sum_sample_nonneg(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]


def run_sim(total_dice):

    split_dice = constrained_sum_sample_nonneg(6, total_dice)

    Person1 = Player_Scores('Lexi', split_dice[0])
    Person2 = Player_Scores('AJ', split_dice[1])
    Person3 = Player_Scores('Daisy', split_dice[2])
    Person4 = Player_Scores('Margot', split_dice[3])
    Person5 = Player_Scores('Kush', split_dice[4])
    Person6 = Player_Scores('Flo', split_dice[5])

    Players = [Person1, Person2, Person3, Person4, Person5, Person6]

    all_dice =[]


    for player in Players:

        vals = player.player_dice()
        all_dice = all_dice + vals

    counter = c.Counter(all_dice)
    freqs = counter.most_common()

    total = 0
    first = freqs[0]

    if first[0] != 1:

        try:
            total = first[1]
            ones = count_ones(freqs)
            total = total + ones
        except TypeError:
            total = np.NaN
    else:
        total = count_ones(freqs)

    return total, total_dice

def simulateRolls(iterations, total_dice):

    totals = []
    for i in tqdm(range(iterations)):
        total, tot_dice = run_sim(total_dice)
        totals.append(total)

    totals_arr = np.array(totals)
    average = np.nanmean(totals_arr)

    return total_dice, average


averages = []
no_dice = []
prop_dice = []

for i in range(30):

    try:

        total_dice, average = simulateRolls(1000000, i)
        no_dice.append(total_dice)
        averages.append(average)

    except Exception:

        no_dice.append(0)
        averages.append(0)

fig, ax = plt.subplots()
plt.plot(no_dice, averages)
plt.show()
