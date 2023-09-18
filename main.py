import chess
import chess.engine
import tkinter as tk
from PIL import Image, ImageTk


class DraggablePiece:
    def __init__(self, canvas, filename, x, y, square, color):
        self.canvas = canvas
        self.piece_image = Image.open(filename)
        self.photo_image = ImageTk.PhotoImage(self.piece_image)
        self.canvas_image = self.canvas.create_image(x, y, anchor="nw", image=self.photo_image)
        self.square = square
        self.color = color
        self.original_x = x
        self.original_y = y
        self.canvas.tag_bind(self.canvas_image, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.canvas_image, "<ButtonRelease-1>", self.on_release)
        self.canvas.tag_bind(self.canvas_image, "<B1-Motion>", self.on_drag)
        self.x = 0
        self.y = 0
        self.drag_data = None

    def on_press(self, event):
        if self.color == chess.WHITE:
            self.x = event.x
            self.y = event.y
            self.drag_data = {"x": event.x, "y": event.y}

    def on_release(self, event):
        if self.color == chess.WHITE:
            move = self.get_drop_square(event.x, event.y)
            if move is not None:
                if move in self.canvas.app.board.legal_moves:
                    self.canvas.app.board.push(move)
                    self.canvas.app.draw_chessboard()
                    self.canvas.app.play_ai_move()
                else:
                    self.snap_back()

    def on_drag(self, event):
        if self.color == chess.WHITE:
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            x, y = self.original_x + delta_x, self.original_y + delta_y
            self.canvas.coords(self.canvas_image, x, y)

    def get_drop_square(self, x, y):
        col = int(x / self.canvas.app.square_size)
        row = 7 - int(y / self.canvas.app.square_size)
        target_square = chess.square(col, row)
        return chess.Move(self.square, target_square) if self.square != target_square else None

    def snap_back(self):
        self.canvas.coords(self.canvas_image, self.original_x, self.original_y)


class ChessApp:
    def __init__(self, root):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("PATH_TO_STOCKFISH_EXECUTABLE")

        self.root = root
        self.root.title("Chess AI")

        self.square_size = 50
        self.canvas_width = 8 * self.square_size
        self.canvas_height = 8 * self.square_size

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.draw_chessboard()
        self.canvas.app = self
        self.player_turn = True

    def draw_chessboard(self):
        chessboard_image = Image.open("chessboard.png")
        chessboard_image = chessboard_image.resize((self.canvas_width, self.canvas_height),
                                                   Image.ANTIALIAS if "ANTIALIAS" in dir(Image) else 3)
        chessboard_photo = ImageTk.PhotoImage(chessboard_image)
        self.canvas.create_image(0, 0, anchor="nw", image=chessboard_photo)
        self.canvas.photo = chessboard_photo

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                color = "White" if piece.color == chess.WHITE else "Black"
                piece_name = piece.symbol().upper()
                filename = f"pieces/{color}{piece_name}.png"
                x, y = self.square_to_coordinates(square, piece.color)
                DraggablePiece(self.canvas, filename, x, y, square, piece.color)

    def square_to_coordinates(self, square, color):
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        x = col * self.square_size
        y = row * self.square_size

        if color == chess.WHITE:
            y -= 18
        elif color == chess.BLACK:
            y -= 5

        return x, y

    def play_ai_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
        attempted_move = result.move.uci()

        if self.board.is_legal(result.move):
            from_square = result.move.from_square
            to_square = result.move.to_square

            from_piece = self.board.piece_at(from_square)
            to_piece = self.board.piece_at(to_square)

            if self.board.is_checkmate():
                print("Game Over - Checkmate!")
            elif self.board.is_stalemate():
                print("Game Over - Stalemate!")
            elif self.board.is_insufficient_material():
                print("Game Over - Insufficient Material!")
            elif self.board.is_seventyfive_moves() or self.board.is_fivefold_repetition():
                print("Game Over - Draw (75-move rule or fivefold repetition)!")

            if from_piece:
                from_piece_name = from_piece.symbol().upper()
                if to_piece:
                    print(
                        f"Black moved {from_piece_name} from {chess.square_name(from_square)} to {chess.square_name(to_square)} and captured {to_piece.symbol().upper()}")
                else:
                    print(
                        f"Black moved {from_piece_name} from {chess.square_name(from_square)} to {chess.square_name(to_square)}")
            else:
                if to_piece:
                    print(
                        f"Black moved from {chess.square_name(from_square)} to {chess.square_name(to_square)} and captured {to_piece.symbol().upper()}")
                else:
                    print(f"Black moved from {chess.square_name(from_square)} to {chess.square_name(to_square)}")

            self.board.push(result.move)
            self.draw_chessboard()
        else:
            print(f"AI attempted an illegal move: {attempted_move}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
