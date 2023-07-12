import itertools
import random


def generate_sets():
    while True:
        stock = []
        player = []
        computer = []
        for i, j in itertools.combinations_with_replacement([0, 1, 2, 3, 4, 5, 6], 2):
            stock.append((i, j))
        for p in range(7):
            player.append(stock.pop(random.randint(0, len(stock)-1)))
        for c in range(7):
            computer.append(stock.pop(random.randint(0, len(stock)-1)))
        if any([i not in stock for i in [(j, j) for j in range(7)]]):
            break
    maxp, maxc = -1, -1
    if len([i for i,j in player if i==j]):
        maxp=max([i for i,j in player if i==j])
    if len([i for i,j in computer if i==j]):
        maxc=max([i for i,j in computer if i==j])
    maxtotal=[maxp,maxc]
    starter = ['player', 'computer'][maxtotal.index(max(maxtotal))]
    domino = (max(maxtotal), max(maxtotal))
    return {'stock': stock, 'player': player, 'computer': computer}, starter, domino


def turn():
    stock, player, computer = sets.values()
    print(f'{"="*70}\nStock size: {len(stock)}\nComputer pieces: {len(computer)}\n')
    if len(snake)<=6:
        print(*snake,sep="")
    else:
        print(*snake[:3],'...',*snake[-3:],sep="")
    print('\nYour pieces:')
    for i, j in enumerate(player):
        print(i+1, list(j), sep=":")


def moveinput():
    continueprompts = {"player": "It's your turn to make a move. Enter your command.",
                       "computer": "Computer is about to make a move. Press Enter to continue..."}
    print(f'\nStatus: {continueprompts[status]}')
    if status == 'computer':
        input()
        return AI()
    else:
        while True:
            choice = input()
            domino_choice = choice.strip("-")
            if all([i not in '1234567890' for i in list(domino_choice)]):
                print('Invalid input. Please try again.')
                continue
            elif int(domino_choice) > len(sets['player']):
                print('Invalid input. Please try again.')
                continue
            choice = int(choice)
            if choice > 0 and snake[-1][1] not in sets['player'][abs(choice)-1]:
                print("Illegal move. Please try again.")
                continue
            elif choice < 0 and snake[0][0] not in sets['player'][abs(choice)-1]:
                print("Illegal move. Please try again.")
                continue
            else:
                return choice


def update():
    if choice == 0:
        if len(sets['stock']) > 0:
            sets[status].append(sets['stock'].pop(random.randint(0, len(sets['stock'])-1)))
        else:
            return
    else:
        entry = sets[status].pop(abs(choice)-1)
        if choice < 0:
            if entry[1] == snake[0][0]:
                snake.insert(0, list(entry))
            else:
                snake.insert(0, list(entry[::-1]))
        if choice > 0:
            if entry[0] == snake[-1][1]:
                snake.insert(len(snake), list(entry))
            else:
                snake.insert(len(snake), list(entry[::-1]))


def AI():
    pool = sets['computer'] + snake
    flattenpool = [i for j in pool for i in j]
    cnts = {i: flattenpool.count(i) for i in range(7)}
    score = {(i[0],i[1]): cnts[i[0]]+cnts[i[1]] for i in sets['computer'] if (any(j in [snake[-1][1],snake[0][0]] for j in i)) }
    if score == {}:
        choice = 0
    else:
        cardchoice = max(score, key=score.get)
        choice = sets['computer'].index(max(score, key=score.get))+1
        if snake[-1][1] in cardchoice:
            choice = -choice
    return choice


sets, starter, domino = generate_sets()
sets[starter].remove(domino)
snake = [list(domino)]
status = "player" if 'player' != starter else "computer"
unfinished = True
while unfinished:
    turn()
    choice = moveinput()
    update()
    if len(sets[status]) == 0:
        result = status+'wins'
        turn()
        break
    flattensnake = [i for j in snake for i in j]
    for i in range(7):
        if flattensnake.count(i) == 8:
            result = "draw"
            turn()
            unfinished = False
            break
    status = "player" if 'player' != status else "computer"

resultprompts = {"playerwins": "The game is over. You won!",
                 "computerwins": "The game is over. The computer won!",
                 "draw": "The game is over. It's a draw!"}
print("Status: ", resultprompts[result])
