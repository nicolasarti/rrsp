

#1 removed comp2 and comp3
#2 removed score3 and score4
#4 game play mod 4 strip:
#4 if player wins 5 games the opponent will remove something and both winning count will be reset to 0
#4 if opponent wins 5 games winning count will be reset to 0
#5 ksge integration
#6 python3 translation 
#7 fixes for not responding when repeating click on replace during scenes
#10 fixed "not responding" in some phases of the game
#11 now los clip is played also when going from act to ris
#12 multi-opponent feature


import operator
import random
import pygame
import platform #5
import time
#import os #5


print (platform.system()) #5
#7 time.sleep(0.5)

#####################################################Global constants here######START
modelname = "KSP" # model/game name #5 must be equal to C1 on ksge #12
wcou = 3 # number of winning row... must be equal to C5bis on ksge

if platform.system() == "Windows": #5
	wdir = "act"
	wfile = "act\\action"+modelname  #5
else:
	wdir = "act"
	wfile = "act/action"+modelname #5
######################################################Global constants here######END	

#os.makedirs(wdir, exist_ok=True) #5

class Card:

	def __init__(self, rank, suit):

		self.rank = 0
		self.suit = ''
		self.image_path = ('img/'+str(rank) + str(suit) + '.png')
		self.selected = False

		#convert the rank to an integer so it's easier to compute the winner of a hand
		if rank == 'A':
			self.rank = 14
		elif rank == 'K':
			self.rank = 13
		elif rank == 'Q':
			self.rank = 12
		elif rank == 'J':
			self.rank = 11
		elif rank == 'T':
			self.rank = 10
		else:
			self.rank = int(rank)

		self.suit = suit

	def __str__(self):
		out = ""

		#convert rank back to a word so it's easier to read
		if self.rank == 14:
			out += "Ace"
		elif self.rank == 13:
			out += "King"
		elif self.rank == 12:
			out += "Queen"
		elif self.rank == 11:
			out += "Jack"
		else:
			out += str(self.rank)

		out += ' of '

		#convert the suit to a word so it's easier to read
		if self.suit == 'H':
			out += 'Hearts'
		elif self.suit == 'S':
			out += 'Spades'
		elif self.suit == 'C':
			out += 'Clubs'
		else:
			out += 'Diamonds'

		return out

#only exists for the __str__ function
class Hand:

	def __init__(self, hand):
		self.hand = hand

	def __str__(self):
		out = ""
		for card in self.hand:
			out += str(card) + ", "
		return out

	def __getitem__(self, index):
		return self.hand[index]

	def __len__(self):
		return len(self.hand)

class Deck:

	def __init__(self):
		self.deck = []

		for suit in ['H','S','C','D']:
			for rank in range(2,15):
				self.deck.append(Card(rank, suit))

	def __str__(self):
		out = ""
		for card in self.deck:
			out += str(card) + "\n"
		return out

	def __getitem__(self, index):
		return self.deck[index]

	#return a list a cards taken from the deck
	def deal(self, amount):
		cards = []

		#cap out the cards dealt
		if amount > len(self.deck):
			print ("There are not enough cards!  I can only deal " + str(len(self.deck)) + " cards.")
			amount = len(self.deck)

		#create and then return a list of cards taken randomly from the deck
		for i in range(amount):
			card = random.choice(self.deck)
			self.deck.remove(card)
			cards.append(card)
		return cards


class Poker:

	def __init__(self):
		self.deck = Deck()
		#2self.scores = [0,0,0,0]
		self.scores = [0,0]

		self.playerHand = Hand(self.deck.deal(5))
		self.comp1Hand = Hand(self.deck.deal(5))
		#1self.comp2Hand = Hand(self.deck.deal(5))
		#1self.comp3Hand = Hand(self.deck.deal(5))

	def __init__(self, scores):
		self.deck = Deck()
		self.scores = scores

		self.playerHand = Hand(self.deck.deal(5))
		self.comp1Hand = Hand(self.deck.deal(5))
		#1self.comp2Hand = Hand(self.deck.deal(5))
		#1self.comp3Hand = Hand(self.deck.deal(5))

	#make each computer take a turn
	def computerReplace(self):
		self.AI_replace(self.comp1Hand)
		#1self.AI_replace(self.comp2Hand)
		#1self.AI_replace(self.comp3Hand)

	def get_most_suit(self, hand):
		suits = {'H':0, 'C':0, 'S':0, 'D':0}
		for card in hand:
			suits[card.suit] += 1
		return max(suits.items(), key=operator.itemgetter(1))[0]

	def get_most_rank(self, hand):
		ranks = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}
		for card in hand:
			ranks[card.rank] += 1
		return max(ranks.items(), key=operator.itemgetter(1))[0]

	def replace_suit(self, hand):
		suit = self.get_most_suit(hand)
		for card in hand:
			if card.suit != suit:
				card.selected = True
		self.replace(hand)

	def replace_rank(self, hand):
		rank = self.get_most_rank(hand)
		for card in hand:
			if card.rank != rank:
				card.selected = True
		self.replace(hand)

	def AI_replace(self, hand):

		score = self.get_score(hand)

		#decide which cards not to toss away so as to keep the same score

		if str(score)[0] == '1': #High card, try for flush
			self.replace_suit(hand)
		elif str(score)[0] == '2': #One pair, switch out cards not paired
			self.replace_rank(hand)
		elif str(score)[0] == '3': #Two pair, switch out card not paired
			self.replace_rank(hand)
		elif str(score)[0] == '4': #Three of a kind, switch out cards not paired
			self.replace_rank(hand)
		elif str(score)[0] == '8': #Four of a kind, switch out the not paired not
			self.replace_rank(hand)

		#all other cases are a pass

	#repalces the selected cards in the hand with the top cards on the deck
	def replace(self, hand):
		count = 0
		for i in range(3):
			for card in hand:
				if card.selected:
					hand.hand.remove(card)
					count += 1

		hand.hand.extend(self.deck.deal(count))

	#plays a round of poker with 4 hands
	#winner is displayed and scores for each hand as well
	#the number of the winner is returned by the function
	def play_round(self):

		score1 = self.get_score(self.playerHand)
		score2 = self.get_score(self.comp1Hand)
		#1score3 = self.get_score(self.comp2Hand)
		#1score4 = self.get_score(self.comp3Hand)

		#2winner = max(score1, max(score2, max(score3, score4)))
		winner = max(score1, score2)


		if winner == score1:
			self.scores[0] += 1
			if self.scores[0] == (wcou - 1):
				##11 write los to ksge and wait
				f = open(wfile, "w")
				f.write("los")
				f.close()
				print ("Oh no, risky situation for me..")
				xwai = "los"
				while xwai == "los":
					print ("oh no! I lost again")
					time.sleep(1)
					f = open(wfile, "r")
					xwai = f.read()
					f.close() #11 end 
				##5 write risk to ksge
				f = open(wfile, "w")
				f.write("ris")
				f.close() 
				print ("oh my god, risky situation for me..")
				#7 time.sleep(2)
				##5
			else:
				##5 write los to ksge and wait
				f = open(wfile, "w")
				f.write("los")
				f.close()
				print (".. I lost ..")
				#7 xwai = "los"
				#7 while xwai == "los":
				#7	print ("los-waiting")
					#7 time.sleep(1)
				#7	f = open(wfile, "r")
				#7	xwai = f.read()
				#7	f.close() 
				##5

		elif winner == score2:
			self.scores[1] += 1
			##5 write win to ksge and wait
			f = open(wfile, "w")
			f.write("win")
			f.close() 
			print ("I won!")
			#7 xwai = "win"
			#7 while xwai == "win":
			#7	print ("win-waiting")
				#7 time.sleep(1)
			#7	f = open(wfile, "r")
			#7	xwai = f.read()
			#7	f.close() 
			##5
			# if risk status play again risk
			if self.scores[0] == (wcou - 1):
				##5 write risk to ksge
				f = open(wfile, "w")
				f.write("ris")
				f.close() 
				print ("oh my god, risky situation for me..")
				##5
		
		if self.scores[0] >= wcou: #winning count
			self.scores[0] = 0
			self.scores[1] = 0
			#10 wait for los play
			xwai = "los"
			while xwai == "los":
				print ("Looks like I lost")
				time.sleep(1)
				f = open(wfile, "r")
				xwai = f.read()
				f.close() 
			##5 write off to ksge and wait
			f = open(wfile, "w")
			f.write("off")
			f.close() 
			xwai = "off"
			while xwai == "off":
				print ("You won this series, I don't believe it, do I really have to undress?..")
				time.sleep(1)
				f = open(wfile, "r")
				xwai = f.read()
				f.close() 
			##5
		
		if self.scores[1] >= wcou: #winning count
			self.scores[0] = 0
			self.scores[1] = 0
			##5 write win to ksge and wait
			f = open(wfile, "w")
			f.write("win")
			f.close() 
			print ("I won this series! what you will take off?")
			#7 xwai = "win"
			#7 while xwai == "win":
			#7	print ("win-waiting")
				#7 time.sleep(1)
			#7	f = open(wfile, "r")
			#7	xwai = f.read()
			#7	f.close() 
			##5

		#2elif winner == score3:
		#2	self.scores[2] += 1

		#2elif winner == score4:
		#2	self.scores[3] += 1

		#2return [score1, score2, score3, score4]
		return [score1, score2]


	#returns an integer that represents a score given to the hand.  The first digits represents the type of hand and the rest represent the cards in the hands
	def get_score(self, hand):
		#make a dictionary containing the count of each each
		cardCount = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}

		for card in hand.hand:
			cardCount[card.rank] += 1

		#count number of unique cards
		uniqueCount = 0
		for rankCount in cardCount.values():
			if rankCount > 0:
				uniqueCount += 1

		straight = self.is_straight(hand)
		flush = self.is_flush(hand)

		points = 0

		if straight and flush:
			points = max(points, 9) #straight flush
		elif flush and not straight:
			points = max(points, 6) #flush
		elif not flush and straight:
			points = max(points, 5) #straight

		elif uniqueCount == 2:
			if max(cardCount.values()) == 4:
				points = 8 #four of a kind (2 uniques and 4 are the same)
			elif max(cardCount.values()) == 3:
				points = 7 #full house (2 unique and 3 are the same)

		elif uniqueCount == 3:
			if max(cardCount.values()) == 3:
				points = 4 #three of a kind (3 unique and 3 are the same)
			elif max(cardCount.values()) == 2:
				points = 3 #two pair (3 uniques and 2 are the same)

		elif uniqueCount == 4:
			if max(cardCount.values()) == 2:
				points = 2 #one pair (4 uniques and 2 are the same)

		elif uniqueCount == 5:
			points = 1 #high card 

		#print out the values of the cards in order from greatest to least with 2 digits for each card in order to generate a point value
		sorted_cardCount = sorted(cardCount.items(), key=operator.itemgetter(1,0), reverse=True)
		for keyval in sorted_cardCount:
			if keyval[1] != 0:
				points = int(str(points) + (keyval[1] * str(keyval[0]).zfill(2)))

		return points

	#given an integer score, returns the poker term equivalent
	def convert_score(self, score):
		if str(score)[0] == '1':
			return "High Card"
		elif str(score)[0] == '2':
			return "One Pair"
		elif str(score)[0] == '3':
			return "Two Pair"
		elif str(score)[0] == '4':
			return "Three of a Kind"
		elif str(score)[0] == '5':
			return "Straight"
		elif str(score)[0] == '6':
			return "Flush"
		elif str(score)[0] == '7':
			return "Full House"
		elif str(score)[0] == '8':
			return "Four of a Kind"
		elif str(score)[0] == '9':
			return "Straight Flush"

	#a hand is a straight if, when sorted, the current card's rank + 1 is the same as the next card
	def is_straight(self,hand):
		values = []
		for card in hand.hand:
			values.append(card.rank)

		values.sort()

		for i in range(0,4):
			if values[i] + 1 != values[i + 1]:
				return False
		return True

	#a hand is a flush if all the cards are of the same suit
	def is_flush(self,hand):
		suit = hand.hand[0].suit
		for card in hand.hand:
			if card.suit != suit:
				return False
		return True
