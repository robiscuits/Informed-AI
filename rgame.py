import random
import time
import game

class RandomPlayer:

    move_vectors = [
        (-1,-1), (0,-1), (1,-1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
    ]

    def __init__(self, piece):
        self.my_piece = piece
        self.played_turns = 0

    def do_drop(self, state):
        drops = [
            [(i, j)]
            for i, row in enumerate(state)
            for j, cell in enumerate(row)
            if cell == ' '
        ]

        return drops[random.randint(0, len(drops) - 1)]

    def do_move(self, state):
        moves = [
            [(i + mi, j + mj), (i, j)]
            for i, row in enumerate(state)
            for j, cell in enumerate(row)
            for mi, mj in self.move_vectors
            if (cell == self.my_piece and
                0 <= i + mi < 5 and
                0 <= j + mj < 5 and
                state[i + mi][j + mj] == ' ')
        ]

        return moves[random.randint(0, len(moves) - 1)]

    def make_move(self, state):
        move = self.do_move(state) if self.played_turns >= 4 else self.do_drop(state)
        self.played_turns += 1
        return move

def play(num_games):

    ai_wins = 0

    for _ in range(num_games):

        ai = game.Teeko2Player(fresh = True)
        rn = RandomPlayer(ai.opp)
        print(ai.my_piece)

        turn = 0

        # drop phase
        while ai.game_value(ai.board) == 0:

            # get the player or AI's move
            if ai.my_piece == ai.pieces[turn]:

                #ai.print_board()

                start = time.time()
                move = ai.make_move(ai.board)
                end = time.time()
                if end - start > 5:
                    raise Exception('AI took longer than 5 seconds!')

                ai.place_piece(move, ai.my_piece)
                #print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
            else:
                #ai.print_board()
                #print(ai.opp+"'s turn")
                move = rn.make_move(ai.board)
                ai.place_piece(move, ai.opp)
                #print(ai.opp+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))

            # update the game variables
            turn += 1
            turn %= 2

        #ai.print_board()
        if ai.game_value(ai.board) == 1:
            ai_wins += 1
            print("AI wins! Game over.")
        else:
            print("Random win! Game over.")


    return ai_wins

if __name__ == "__main__":
    num_games = 100
    aiw = play(num_games)

    print(f"AI won:{aiw} of {num_games} games")
