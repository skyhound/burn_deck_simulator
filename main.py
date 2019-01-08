import random
import json

f = open("card_pool.json", "r")
card_pool = json.load(f)
f.close()
del f


class GameOver(Exception):
    pass


class Card:
    def __init__(self, **kwargs):
        for arg_name, arg_value in kwargs.items():
            self.__dict__[arg_name] = arg_value


class CardInstance(Card):
    def __init__(self, card_name):
        global card_pool
        super().__init__(**card_pool[card_name])
        self.name = card_name


class Deck(dict):
    pass


class Library(list):
    def __init__(self, deck):
        super().__init__()
        for card_name, card_quantity in deck.items():
            for i in range(card_quantity):
                self.append(CardInstance(card_name))

    def shuffle(self):
        random.shuffle(self)


class Hand(list):
    pass


class Permanent(Card):
    def __init__(self, card_name):
        global card_pool
        super().__init__(**card_pool[card_name])
        self.name = card_name

class Engine:
    def __init__(self, deck, player):
        self.deck = deck
        self.player = player
        self.battlefield = {}
        self.permanent_id = 0
        self.turn_counter = 0
        self.library = Library(self.deck)
        self.library.shuffle()
        self.hand = Hand()

    def start_game(self):
        self.turn_counter = 0
        self.battlefield = {}
        self.draw_hand()
        try:
            while True:
                self.turn_counter += 1
                self.make_turn()
        except GameOver as e:
            print(f"game over in {self.turn_counter} turns")

    def draw_hand(self):
        for i in range(7):
            self.draw_card()

    def draw_card(self):
        if len(self.library) == 0:
            raise GameOver
        card = self.library.pop()
        self.hand.append(card)

    def play_land_card(self, card_index):
        card = self.hand.pop(card_index)
        self.battlefield[self.permanent_id] = Permanent(card.name)

    def make_turn(self):
        # self.untap()
        # self.upkeep()
        self.draw_step()
        self.first_main()
        # self.combat()
        # self.second_main()
        # self.end_step()
        # self.cleanup()

    def draw_step(self):
        self.draw_card()

    def first_main(self):
        self.player.first_main(self)


class Player:
    def first_main(self, engine):
        land_index = self.check_land_in_hand(engine.hand)
        if land_index:
            engine.play_land_card(land_index)

    def check_land_in_hand(self, hand):
        for card in hand:
            if card.type == "Land":
                return hand.index(card)
        return False

deck = Deck(
    {
        "Mountain": 20,
        "Lightning Bolt": 40
    }
)
engine = Engine(deck, Player())
engine.start_game()
aa = 9

