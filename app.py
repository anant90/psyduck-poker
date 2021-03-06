#
# pokersim.py - Runs a Monte Carlo simulation of a hand
#               with user-specified 3 community cards
#
#
import argparse
import random

from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    flop = request.args.get('flop')
    iterations = request.args.get('iterations')
    return main(flop, int(iterations))


def readable_hand(cards):
    #
    # Returns a readable version of a set of cards
    #
    card_rank = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8",
                 7: "9", 8: "T", 9: "J", 10: "Q", 11: "K", 12: "A", -1: "X"}
    card_suit = {0: "c", 1: "d", 2: "h", 3: "s", -1: "x"}
    return_string = ""
    for i in cards:
        return_string += card_rank[i[0]] + card_suit[i[1]]
    return return_string


def hand_copy(cards, discarded_card1_index = None, discarded_card2_index = None, discarded_card3_index = None):
    #
    # Returns copy of hand (replaces deepcopy with 20x speed improvement)
    #
    results = []
    index = 0
    for i in cards:
        if discarded_card1_index != index:
            if discarded_card2_index != index:
                if discarded_card3_index != index:
                    results.append(i)
        index+=1
    return results


def legal_hand(cards):
    #
    # Returns True if hand is legal
    # Returns False if hand is illegal
    #   Case 1: two or more of same card
    #   Case 2: random card
    #
    for i in cards:
        if cards.count(i) > 1 or cards == [-1, -1]:
            return False
    return True


def valid_card(card):
    #
    # Returns True if card is a valid card in text format (rank in (A-2),
    #  suit in (c, d, h, s) or wildcard (Xx)
    # Returns False if card is invalid
    #
    if card[0] in ("X", "x", "A", "a", "K", "k", "Q", "q", "J", "j",
                   "T", "t", "9", "8", "7", "6", "5", "4", "3", "2") \
            and card[1] in ("x", "X", "c", "C", "d", "D", "h", "H", "s", "S"):
        return True
    else:
        return False


def hand_to_numeric(cards):
    #
    # Converts alphanumeric hand to numeric values for easier comparisons
    # Also sorts cards based on rank
    #
    card_rank = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6,
                 "9": 7, "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12, "X": -1,
                         "t": 8, "j": 9, "q": 10, "k": 11, "a": 12, "x": -1}
    card_suit = {"c": 0, "C": 0, "d": 1, "D": 1, "h": 2, "H": 2,
                 "s": 3, "S": 3, "x": -1, "X": -1}
    result = []
    for i in range(len(cards) // 2 + len(cards) % 2):
        result.append([card_rank[cards[i * 2]], card_suit[cards[i * 2 + 1]]])
    result.sort()
    result.reverse()
    return result


def check_flush(hand):
    #
    # Returns True if hand is a Flush, otherwise returns False
    #
    hand_suit = [hand[0][1], hand[1][1], hand[2][1], hand[3][1], hand[4][1]]
    for i in range(4):
        if hand_suit.count(i) == 5:
            return True
    return False


def check_straight(hand):
    # Return True if hand is a Straight, otherwise returns False
    if hand[0][0] == (hand[1][0] + 1) == (hand[2][0] + 2) == (hand[3][0] + 3)\
            == (hand[4][0] + 4):
        return True
    elif (hand[0][0] == 12) and (hand[1][0] == 3) and (hand[2][0] == 2)\
            and (hand[3][0] == 1) and (hand[4][0] == 0):
        return True
    return False


def check_straightflush(hand):
    # Return True if hand is a Straight Flush, otherwise returns False
    if check_flush(hand) and check_straight(hand):
        return True
    return False


def check_fourofakind(hand):
    # Return True if hand is Four-of-a-Kind, otherwise returns False
    # Also returns rank of four of a kind card and rank of fifth card
    # (garbage value if no four of a kind)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for quad_card in range(13):
        if hand_rank.count(quad_card) == 4:
            for kicker in range(13):
                if hand_rank.count(kicker) == 1:
                    return True, quad_card, kicker
    return False, 13, 13


def check_fullhouse(hand):
    # Return True if hand is a Full House, otherwise returns False
    # Also returns rank of three of a kind card and two of a kind card
    # (garbage values if no full house)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for trip_card in range(13):
        if hand_rank.count(trip_card) == 3:
            for pair_card in range(13):
                if hand_rank.count(pair_card) == 2:
                    return True, trip_card, pair_card
    return False, 13, 13


def check_threeofakind(hand):
    # Return True if hand is Three-of-a-Kind, otherwise returns False
    # Also returns rank of three of a kind card and remaining two cards
    # (garbage values if no three of a kind)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for trip_card in range(13):
        if hand_rank.count(trip_card) == 3:
            for n in range(13):
                if hand_rank.count(n) == 1:
                    for m in range(n+1, 13):
                        if hand_rank.count(m) == 1:
                            return True, trip_card, [m, n]
    return False, 13, [13, 13]


def check_twopair(hand):
    # Return True if hand is Two Pair, otherwise returns False
    # Also returns ranks of paired cards and remaining card
    # (garbage values if no two pair)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for low_pair_card in range(13):
        if hand_rank.count(low_pair_card) == 2:
            for high_pair_card in range(low_pair_card + 1, 13):
                if hand_rank.count(high_pair_card) == 2:
                    for kicker in range(13):
                        if hand_rank.count(kicker) == 1:
                            return True, [high_pair_card, low_pair_card], \
                                kicker
    return False, [13, 13], 13


def check_onepair(hand):
    # Return True if hand is One Pair, otherwise returns False
    # Also returns ranks of paired cards and remaining three cards
    # (garbage values if no pair)
    hand_rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for pair_card in range(13):
        if hand_rank.count(pair_card) == 2:
            for kicker1 in range(13):
                if hand_rank.count(kicker1) == 1:
                    for kicker2 in range(kicker1 + 1, 13):
                        if hand_rank.count(kicker2) == 1:
                            for kicker3 in range(kicker2 + 1, 13):
                                if hand_rank.count(kicker3) == 1:
                                    return True, pair_card, \
                                        [kicker3, kicker2, kicker1]
    return False, 13, [13, 13, 13]


def highest_card(hand, hand2):
    # Return 0 if hand is higher
    # Return 1 if hand2 is higher
    # Return 2 if equal
    hand_rank = \
        [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    hand2_rank = \
        [hand2[0][0], hand2[1][0], hand2[2][0], hand2[3][0], hand2[4][0]]
    #
    # Compare
    #
    if hand_rank > hand2_rank:
        return 0
    elif hand_rank < hand2_rank:
        return 1
    return 2


def highest_card_straight(hand, hand2):
    # Return 0 if hand is higher
    # Return 1 if hand2 is higher
    # Return 2 if equal
    #
    # Compare second card first (to account for Ace low straights)
    # if equal, we could have Ace low straight, so compare first card.
    # If first card is Ace, that is the lower straight
    #
    if hand[1][0] > hand2[1][0]:
        return 0
    elif hand[1][0] < hand2[1][0]:
        return 1
    elif hand[0][0] > hand2[0][0]:
        return 1
    elif hand[0][0] < hand2[0][0]:
        return 0
    return 2


def compare_hands(hand, hand2):
    #
    # Compare two hands
    # Return 0 if hand is better
    # Return 1 if hand2 is better
    # Return 2 if equal
    #
    result1 = []
    result2 = []
    #
    # Check for straight flush
    #
    if check_straightflush(hand):
        if check_straightflush(hand2):
            return(highest_card_straight(hand, hand2))
        else:
            return 0
    elif check_straightflush(hand2):
            return 1
    #
    # Check for four of a kind
    #
    result1 = check_fourofakind(hand)
    result2 = check_fourofakind(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for full house
    #
    result1 = check_fullhouse(hand)
    result2 = check_fullhouse(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for flush
    #
    if check_flush(hand):
        if check_flush(hand2):
            return(highest_card(hand, hand2))
        else:
            return 0
    elif check_flush(hand2):
        return 1
    #
    # Check for straight
    #
    if check_straight(hand):
        if check_straight(hand2):
            temp = highest_card_straight(hand, hand2)
            return temp
        else:
            return 0
    elif check_straight(hand2):
        return 1
    #
    # Check for three of a kind
    #
    result1 = check_threeofakind(hand)
    result2 = check_threeofakind(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for two pair
    #
    result1 = check_twopair(hand)
    result2 = check_twopair(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    #
    # Check for one pair
    #
    result1 = check_onepair(hand)
    result2 = check_onepair(hand2)
    if result1[0] == 1:
        if result2[0] == 1:
            if result1[1] > result2[1]:
                return 0
            elif result1[1] < result2[1]:
                return 1
            elif result1[2] > result2[2]:
                return 0
            elif result1[2] < result2[2]:
                return 1
            else:
                return 2
        else:
            return 0
    elif result2[0] == 1:
        return 1
    return (highest_card(hand, hand2))


def best_five(hand, community):
    #
    # Takes hand and community cards in numeric form
    # Returns best five cards
    #
    currentbest = hand_copy(hand, 0)
    currentbest.sort()
    currentbest.reverse()

    #
    # Compare current best to five cards including only one community cards out of 3, and 4 in hand cards
    #

    for m in range(3):
        for n in range(6):
            for o in range(n+1,6):
                #m is picked of 3 community, n and o are not picked out of hand
                comparehand = hand_copy(hand, n, o)
                comparehand.append(community[m])
                comparehand.sort()
                comparehand.reverse()

                if compare_hands(currentbest, comparehand) == 1:
                    currentbest = hand_copy(comparehand)

    #
    # Compare current best to five cards including only two community cards out of 3, and 3 in hand cards out of 6
    #

    for m in range(3):
        for n in range(n, 6):
            for o in range(n+1,6):
                for p in range(o+1,6):
                    #m is eliminated of 3 community, n, o and p are not picked out of hand
                    comparehand = hand_copy(hand, n, o, p)
                    comparehand2 = hand_copy(community, m)
                    comparehand.concat(comparehand2)
                    comparehand.sort()
                    comparehand.reverse()

                    if compare_hands(currentbest, comparehand) == 1:
                        currentbest = hand_copy(comparehand)


    #
    # Compare current best to five cards including all three community cards out of 3, and 2 in hand cards out of 6
    #

    for m in range(6):
        for n in range(n+1, 6):
            comparehand = hand_copy(community)
            comparehand.append(hand[m])
            comparehand.append(hand[n])
            comparehand.sort()
            comparehand.reverse()

            if compare_hands(currentbest, comparehand) == 1:
                currentbest = hand_copy(comparehand)

    return currentbest


def main(community_arg="AhAdAs", iterations_arg=1):
    iterations = iterations_arg
    temp_community_string = community_arg
    community = ""
    while temp_community_string:
        current_community_card = temp_community_string[:2]
        if not valid_card(current_community_card):
            quit("Community Card Invalid")
        community += current_community_card
        temp_community_string = temp_community_string[2:]

    communitynum = hand_to_numeric(community)

    # Initialize counters
    totals = [0, 0, 0, 0, 0]
    # Monte Carlo Simulation
    for _ in range(iterations):

        hand_original = hand_to_numeric("XxXxXxXxXxXx")
        hand_temp = hand_original[:]

        while not legal_hand(hand_temp + communitynum):
            hand_temp = hand_original[:]
            for i in range(len(hand_temp)):
                if hand_temp[i][0] == -1:
                    hand_temp[i] = [random.randint(0, 12),
                                         random.randint(0, 3)]


        best_hand = best_five(hand_temp, communitynum)

        if (check_threeofakind(best_hand)[0]):
            totals[0]+=1
        if (check_straight(best_hand)):
            totals[1]+=1
        if (check_flush(best_hand)):
            totals[2]+=1
        if (check_fullhouse(best_hand)[0]):
            totals[3]+=1
        if (check_fourofakind(best_hand)[0]):
            totals[4]+=1

    # Print results
    return_string = ""
    return_string += "Total Hands: %i\n" % (iterations)
    return_string += "3s: %i Straight: %i Flush: %i Full House: %i Quads: %i\n" % (totals[0], totals[1], totals[2], totals[3], totals[4])
    return_string += "3s: %.2f%% Straight: %.2f%% Flush: %.2f%% Full House: %.2f%% Quads: %.2f%% \n" % \
        (100 * round((totals[0] / (iterations + 0.0)), 4),
         100 * round((totals[1] / (iterations + 0.0)), 4),
         100 * round((totals[2] / (iterations + 0.0)), 4),
         100 * round((totals[3] / (iterations + 0.0)), 4),
         100 * round((totals[4] / (iterations + 0.0)), 4))
    return return_string
