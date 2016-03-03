
from cardrules import CardRules
from deck import Deck


# only coded this to play with builder pattern
class SimulationBuilder(object):

    def __init__(self):
        self.startingCards = None #string
        self.numberDraws = None #int
        self.target = None #string
        self.simulations = None #int
        self.MAXCARDS = 5 # number of cards dealt to a player at start

    def setStartingCards(self, s):
        self.startingCards = s
        return self

    def setNumberOfDraws(self, d):
        self.numberDraws = d
        return self

    def setTarget(self, t):
        self.target = t
        return self

    def setSimulations(self, r):
        self.simulations = r
        return self

    def build(self):
        return Simulation(self.startingCards, self.numberDraws, self.target, self.simulations, self.MAXCARDS)


class Simulation(object):
    '''
    Responsible for running the simulations and

    Use SimulationBuilder to build this class safely
    '''

    def __init__(self,s,d,t,r,m=5):

        self.starting_cards=s
        self.number_of_draws=d
        self.target_rank=t
        self.number_simulations=r
        self.MAX_CARDS_IN_HAND=m

    def launch(self):

        success_count = 0

        for u in range(self.number_simulations):

            deck = Deck()

            card_rules=CardRules()
            card_rules.set_target(deck.convert_rank_to_int(self.target_rank))

            starting_hand = self.get_starting_hand(deck, self.starting_cards)

            # required to run CardRules
            integer_hand=self.convert_cards_to_integers(deck, starting_hand)

            for v in range(self.number_of_draws):
                # note these are int cards, not string cards
                retained_cards = card_rules.apply_rules(integer_hand)

                #draw additional cards from deck to make a full hand
                new_hand = [deck.get_card() for c in range(self.MAX_CARDS_IN_HAND - len(retained_cards))]
                integer_hand=retained_cards+self.convert_cards_to_integers(deck, new_hand)

            # at the end of the last draw we check the final hand to see if we hit the target
            card_rules.set_final_check()
            issuccess=card_rules.apply_rules(integer_hand)

            if issuccess:
                success_count+=1

        return (success_count+0.0)/self.number_simulations

    def get_starting_hand(self, deck, starting_cards):

        starting_hand = []

        if(len(starting_cards)>0):

            tpcards=starting_cards.split('+')

            # do basic sanity checks
            # TODO should also add checks for suit only and rank only
            for c in tpcards:
                if(len(c)>2 or len(c)==0 or len(c)==1):
                    raise Exception('Incorrect card format. Please ensure cards are separated by + signs'
                                    'and are 2 characters')

            # we assume well formatted 2 chars cards for now
            for c in tpcards:
                starting_hand.append(c)
                deck.remove_card_from_deck(c)

        # get the rest of the starting hand
        for i in range(5-starting_hand.__len__()):
            starting_hand.append(deck.get_card())

        return starting_hand

    def convert_cards_to_integers(self, deck, starting_hand):
        return [deck.cards_to_int_dict[j] for j in starting_hand]





    