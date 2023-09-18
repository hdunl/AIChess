# AIChess
Very simple and thrown together chess application. Not intended to be completely finalized code although it does work.


# Description (cont.)
This is a simple chess application implemented in Python using the Tkinter library for the graphical user interface and the python-chess library for chessboard manipulation and move validation. This application allows you to play chess against a basic AI opponent that uses the Stockfish chess engine. Below is a detailed explanation of the code and how to use it.

## Prerequisites

Before running the application, you need to have the following prerequisites installed:

1. **Python**: You need to have Python 3.x installed on your system.

2. **Tkinter**: Tkinter is a built-in Python library for creating GUI applications. It should be available by default with your Python installation.

3. **python-chess**: Install the python-chess library using pip, which provides chessboard manipulation and move validation. You can install it using the following command: pip install chess
   
4. **Stockfish Chess Engine**: Download and install the Stockfish chess engine. You can get it from the official Stockfish website: [https://stockfishchess.org/download/](https://stockfishchess.org/download/)

## How to Use

1. **Clone the Repository**: git clone https://github.com/yourusername/chess-ai.git --->  cd chess-ai

2. **Run the Application**: python main.py

3. **Playing the Game**:

- The chessboard is displayed, and you play as the white pieces.
- Click and drag a piece to move it. Legal moves will be highlighted.
- Make your move by releasing the mouse button.
- The AI opponent (black pieces) will respond automatically using the Stockfish chess engine.

4. **Game Over**:

- The game can end in various ways: checkmate, stalemate, insufficient material, or a draw (75-move rule or fivefold repetition).
- When the game ends, a message will be printed in the console to indicate the result.

## Code Explanation

The code is organized into two classes: `DraggablePiece` and `ChessApp`.

### DraggablePiece Class

- The `DraggablePiece` class represents a chess piece that can be clicked, dragged, and dropped on the chessboard.
- It loads the piece image from a file (e.g., 'pieces/WhiteP.png' or 'pieces/BlackK.png') and displays it on the canvas.
- The piece can be dragged within legal move boundaries and snapped back to its original position if the move is not legal.
- The `on_press`, `on_release`, and `on_drag` methods handle the mouse interactions.

### ChessApp Class

- The `ChessApp` class represents the chess application itself.
- It initializes the chessboard, sets up the GUI using Tkinter, and handles user interactions.
- The `draw_chessboard` method draws the chessboard with pieces using a custom chessboard image.
- The `square_to_coordinates` method converts a chess square to pixel coordinates on the canvas.
- The `play_ai_move` method plays a move for the AI opponent using the Stockfish chess engine.

## Customization

- You can customize the appearance of the chess pieces by replacing the piece image files in the 'pieces' folder.
- You can modify the GUI and board layout by editing the `draw_chessboard` method and the chessboard image ('chessboard.png').
