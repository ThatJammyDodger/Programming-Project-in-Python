import random
import os.path
import csv

Player1Cards = []
Player2Cards = []
Deck = []
Player1LoggedIn = False
Player2LoggedIn = False
scores = []
names = []

if not(os.path.isfile('winners.csv')):
  with open("winners.csv","w") as a:
    a.write("Simon Cowell,30\n")
    a.write("Me,26\n")
    a.write("Dr Who,16\n")
    a.write("Mrs Brown,20\n")
    a.write("My friend,16\n")

if not(os.path.isfile('logins.csv')):
  with open("logins.csv","w") as a:
    a.write("player1,pass1\n")
    a.write("player2,pass2\n")
    a.write("player3,pass3\n")

def SortLists():
  has_swapped = True
  num_of_iterations = 0
  while(has_swapped):
    has_swapped = False
    for i in range(len(scores) - 1 - num_of_iterations):
      if int(scores[i]) > int(scores[i+1]):
        scores[i], scores[i+1] = scores[i+1], scores[i]
        names[i], names[i+1] = names[i+1], names[i]
        has_swapped = True
    num_of_iterations += 1
  names.reverse()
  scores.reverse()

def reset():
  setDeck()
  shuffleDeck()
  Player1Cards.clear()
  Player2Cards.clear()

def setDeck():
  Deck.clear()
  for i in range(0,10):
    Deck.append(f"{i+1} Red")
    Deck.append(f"{i+1} Black")
    Deck.append(f"{i+1} Yellow")

def shuffleDeck():
  random.shuffle(Deck)

def calculateWinner(player1card, player2card):
  
      if (findCardNumber(player1card)>findCardNumber(player2card)):
        return 1
      elif (findCardNumber(player1card)<findCardNumber(player2card)):
        return 2
      elif ((findCardColour(player1card)=="Red") and(findCardColour(player2card)=="Black")):
        return 1
      elif ((findCardColour(player1card)=="Yellow")and(findCardColour(player2card)=="Red")):
        return 1
      elif ((findCardColour(player1card)=="Black")and(findCardColour(player2card)=="Yellow")):
        return 1
      elif ((findCardColour(player2card)=="Red")and(findCardColour(player1card)=="Black")):
        return 2
      elif ((findCardColour(player2card)=="Yellow")and(findCardColour(player1card)=="Red")):
        return 2
      elif ((findCardColour(player2card)=="Black")and(findCardColour(player1card)=="Yellow")):
        return 2
      else:
        return 1
      
def drawCard():
  return Deck.pop(0)

def findCardNumber(card):
  spaceindex=card.index(" ")
  returnn = int(card[0:spaceindex])
  return returnn

def findCardColour(card):
  spaceindex=card.index(" ")
  return card[spaceindex+1:]

def getFinalWinner():
  if len(Player1Cards)>len(Player2Cards):
    return 1
  else:
    return 2

def giveCards(player, card1, card2):
  if player==1:
    Player1Cards.append(card1)
    Player1Cards.append(card2)
  elif player==2:
    Player2Cards.append(card1)
    Player2Cards.append(card2)

def auth(enteredUsername, enteredPassword):
  with open("logins.csv","r") as a:
    aa=[]
    aaa=csv.reader(a)
    for row in aaa:
      aa+=[row]
  aaaa = enteredUsername
  for i in range(len(aa)-1):
    if aaaa == str(aa[i][0]):
      aaaaa = enteredPassword
      if aaaaa == str(aa[i][1]):
        return True
  return False

setDeck()
shuffleDeck()

players = ["",""]

AUTH = False

while not(AUTH):
  username1 = input("Enter username for player 1: ")
  password1= input("Enter password for player 1: ")
  username2 = input("\nEnter username for player 2: ")
  password2 = input("Enter password for player 2: ")

  auth1 = auth(username1, password1)
  auth2 = auth(username2, password2)

  print()

  if not(auth1):
    print("Login failure for player 1. Try again.")
  if not(auth2):
    print("Login failure for player 2. Try again.")
  if (username1==username2):
    auth1 = False
    print("Login failure: users must use different credentials to login.")
  print()
  if (auth1 and auth2):
    AUTH = True

while (players[0]==players[1]):
  print("Note: display names cannot be the same\n")
  players[0] = input("Enter display name for player 1: ")
  players[1] = input("Enter display name for player 2: ")

print("\nLoggeed in successfully\n")

def showStats():
  print("\n\t===================================")
  print("{} has {} cards, having won {} rounds out of 15.".format(players[0],len(Player1Cards), int(len(Player1Cards) / 2)))
  print("{} has {} cards, having won {} rounds out of 15.".format(players[1], len(Player2Cards), int(len(Player2Cards) / 2)))
  print("There are {} rounds left.".format(int(len(Deck) / 2)))
  print("\t===================================\n")

def play():
  reset()
  while len(Deck)>0:
    showStats()

    print("{}, type 'draw' to take a card.".format(players[0]))
    input()
    player1card = drawCard()
    print("Your card is {}.\n\nLet's give {} a go now too.".format(player1card,players[1]))
    print("\n{}, type 'draw' to take a card.".format(players[1]))
    player2card = drawCard()
    input()
    print("Your card is {}.\n\nLet me just calculate the winner".format(player2card))

    winner = calculateWinner(player1card, player2card)
    print("The winner of that round is {}.".format(players[winner - 1]))

    giveCards(winner, player1card, player2card)
    print("\n\n")
  
  finalWinner = getFinalWinner()

  WinnerNoOfCards = 0

  if finalWinner==1:
    WinnerNoOfCards = len(Player1Cards)
  elif finalWinner==2:
    WinnerNoOfCards = len(Player2Cards)

  print("\nGAME OVER!\n\n__________________________________________________\n")
  print("The final winner, as you probably already know, is ... *drumroll* ... {} with {} cards.".format(players[finalWinner - 1],WinnerNoOfCards))
  print("Their cards were:")

  if finalWinner==1:
    for x in Player1Cards:
      print("\t{}".format(x))
  elif finalWinner==2:
    for x in Player2Cards:
      print("\t{}".format(x))

  with open("winners.csv","a") as x:
    x.write(f"{players[finalWinner - 1]},{WinnerNoOfCards}\n")

  with open("winners.csv","r") as file:
    arr=[]
    read = csv.reader(file)
    for row in read:
      arr+=[row]
    for i in range(0,len(arr)):
      names.append(arr[i][0])
      scores.append(arr[i][1])

  SortLists()

  print("\nALL-TIME WINNERS:")
  for i in range(5):
    print(f"({i + 1}) {names[i]} with a score of {scores[i]}.")

play()
input()