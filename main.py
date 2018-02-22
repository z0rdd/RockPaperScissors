import sqlite3
from tabulate import tabulate

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("scores.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, p_score INTEGER,"
                         "c_score INTEGER, result TEXT)")
        self.conn.commit()

    def insert(self, name, p_score, c_score, result):
        self.cur.execute("INSERT INTO scores VALUES (NULL, ?, ?, ?, ?)", (name, p_score, c_score, result))
        self.conn.commit()

    def view_all(self):
        view = self.cur.execute("SELECT * FROM scores")
        return view


db = Database()


class Game:
    def __init__(self):
        self.p_name = self.start()
        print("Hi, {}. Let's play a game".format(self.p_name))
        self.figures = ['rock', 'paper', 'scissors']
        self.play()

    def start(self):
        start_inp = input("Rock, Paper, Scissors. Play(y/n)?")
        if start_inp == "y":
            p_name = input("Enter player name: ")
            return p_name
        else:
            self.sub_menu()

    def sub_menu(self):
        choice = input("Scores? Exit?").lower()
        if choice == 'scores':
            print(tabulate([list(line) for line in db.view_all()], headers=['Game Id', 'Name', 'PlayersScore', 'CpuScores',
                                                                            'Result']))
        elif choice == 'exit':
            exit()
        else:
            self.sub_menu()

    def play(self):
        from random import choice as rnd

        outcomes = {'rockrock': [0, 0], 'rockpaper': [0, 1], 'rockscissors': [1, 0],
                    'paperrock': [1, 0], 'paperpaper': [0, 0], 'paperscissors': [0, 1],
                    'scissorsrock': [0, 1], 'scissorspaper': [1, 0], 'scissorsscissors': [0, 0]}
        p_score = 0
        c_score = 0
        while True:
            c_choice = rnd(self.figures)
            p_choice = self.player_choice()

            p_score += outcomes[p_choice + c_choice][0]
            c_score += outcomes[p_choice + c_choice][1]

            print('The Computer chose {}'.format(c_choice))
            print('Current score: {}: {}, Computer: {}'.format(self.p_name, p_score, c_score))
            if p_score == 3 or c_score == 3:
                break

        if p_score > c_score:
            print('You win')
            db.insert(self.p_name, p_score, c_score, "win")
            self.start()
        else:
            print('You lose')
            db.insert(self.p_name, p_score, c_score, "lose")
            self.start()

    def player_choice(self):
        while True:
            p_choice = input('Rock?, Paper?, Scissors? ').lower()
            if p_choice in self.figures:
                break
        return p_choice


game = Game()

