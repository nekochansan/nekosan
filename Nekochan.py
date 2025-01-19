import random

# 定数定義
BLACK = 1  # 黒石
WHITE = 2  # 白石

# 6x6の初期状態のオセロボードを定義
board = [
    [0, 0, 0, 0, 0, 0],  # 0は空きマスを表す
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],  # 中央に黒石(1)と白石(2)が配置されている
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# 各マスの評価スコア
POSITION_SCORES = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2, 1, 1, -2, 10],
    [10, -2, 1, 1, -2, 10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを判定する。
    """
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def count_flipped(board, stone, x, y):
    """
    石を置いたときに裏返せる石の数をカウントする。
    """
    if not can_place_x_y(board, stone, x, y):
        return 0

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    total_flipped = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped = 0
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            flipped += 1

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            total_flipped += flipped

    return total_flipped

class NekochanAI:
    """
    石を置く位置を評価関数を使って決定する戦略的なAI。
    """
    def face(self):
        return "🧠"

    def place(self, board, stone):
        """
        最も良い評価スコアを持つ位置を選んで返す。
        """
        best_score = float('-inf')
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    flipped_count = count_flipped(board, stone, x, y)
                    position_score = POSITION_SCORES[y][x]
                    score = flipped_count + position_score

                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move
