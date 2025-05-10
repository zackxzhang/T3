import tkinter as tk
from tkinter import messagebox
from t3 import Stone, State, Agent, Learner
from t3.state import Index, Coord, s0, transition, boardify, judge


def ij2k(ij: Coord) -> Index:
    i, j = ij
    return i * 3 + j


def k2ij(k: Index) -> Coord:
    return divmod(k, 3)


class Human:

    def __init__(self, stone: Stone):
        self.stone = stone


class TicTacToe:

    def __init__(self, human_1st: bool):
        if human_1st:
            human = Human(Stone.X)
            agent = Learner.load('a2.json').eval()
            self.players = (human, agent)
        else:
            human = Human(Stone.O)
            agent = Learner.load('a1.json').eval()
            self.players = (agent, human)
        self.round = 0
        self.winner = Stone._
        self.trajectory = [s0]

    @property
    def player(self):
        return self.players[self.round % 2]

    @property
    def state(self):
        return self.trajectory[-1]

    @property
    def board(self):
        return boardify(self.state)

    def evo(self, action: State):
        self.trajectory.append(action)
        self.winner = judge(action)
        self.round += 1
        return self.winner


class TicTacToeUI:

    def __init__(self, root: tk.Tk, human_1st: bool):
        root.title('Tic Tac Toe')
        self.root = root
        self.human_1st = human_1st
        self.canvas()
        self.reset()

    def canvas(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.root,
                    text=' ',
                    font=('Helvetica', 24),
                    width=8,
                    height=4,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def reset(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')
        self.game = TicTacToe(self.human_1st)
        match self.game.player:
            case Agent():
                self.autopilot()
            case Human():
                pass
            case _:
                raise ValueError('Unknown player')

    def signal(self, winner: Stone):
        if winner == Stone.X | Stone.O:
            messagebox.showinfo("Game Over", "It's a draw!")
        elif winner == Stone.X or winner == Stone.O:
            messagebox.showinfo("Game Over", f"{winner} wins!")
        else:
            raise ValueError('Game NOT over yet')

    def on_click(self, row: int, col: int):
        if not self.game.board[row][col]:
            k = ij2k((row, col))
            stone = self.game.player.stone
            state = self.game.state
            action = transition(state, stone, k)
            winner = self.game.evo(action)
            self.buttons[row][col].config(text=str(stone))
            self.root.update_idletasks()
            if winner:
                self.signal(winner)
                self.reset()
            else:
                self.autopilot()  # explictly go to agent

    def autopilot(self):
        agent  = self.game.player
        action = agent.act(self.game.state)
        winner = self.game.evo(action)
        board  = self.game.board
        for i in range(3):
            for j in range(3):
                if board[i][j]:
                    self.buttons[i][j].config(text=str(board[i][j]))
        self.root.update_idletasks()
        if winner:
            self.signal(winner)
            self.reset()
        else:
            pass  # implicitly go to human


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Tic Tac Toe')
    parser.add_argument(
        '-m',
        '--move',
        action='store',
        type=int,
        default=1,
        help='choose 1 (1st move) or 2 (2nd move)',
    )
    args = parser.parse_args()

    root = tk.Tk()
    TicTacToeUI(root, True if args.move == 1 else False)
    root.mainloop()
