import copy

# 定数定義
BLACK = 1  # 黒石
WHITE = 2  # 白石

# ボード上の位置に対するスコア
POSITION_SCORES = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2, 1, 1, -2, 10],
    [10, -2, 1, 1, -2, 10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

class TranspositionTable:
    """
    トランスポジションテーブル（盤面キャッシュ）を管理するクラス。
    """
    def __init__(self):
        self.table = {}

    def get(self, board, depth):
        key = self.hash_board(board)
        if key in self.table and self.table[key]["depth"] >= depth:
            return self.table[key]["value"]
        return None

    def set(self, board, depth, value):
        key = self.hash_board(board)
        self.table[key] = {"depth": depth, "value": value}

    @staticmethod
    def hash_board(board):
        return str(board)  # シンプルな盤面の文字列ハッシュ

def evaluate_board(board, stone):
    """
    現在の盤面の評価値を計算する（位置スコア + モビリティ + エッジ管理）。
    """
    score = 0
    # 位置スコアを計算
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += POSITION_SCORES[y][x]
            elif board[y][x] == (3 - stone):
                score -= POSITION_SCORES[y][x]

    # モビリティを計算
    player_moves = len(find_valid_moves(board, stone))
    opponent_moves = len(find_valid_moves(board, 3 - stone))
    mobility_score = player_moves - opponent_moves
    score += mobility_score * 5  # モビリティの重み

    # エッジ管理（動的スコア調整）
    edges = [
        (0, 1, 0, 4),  # 上辺
        (1, 0, 4, 0),  # 左辺
        (5, 1, 5, 4),  # 下辺
        (1, 5, 4, 5),  # 右辺
    ]
    for y1, x1, y2, x2 in edges:
        edge_stone = board[y1][x1]
        if edge_stone == stone:  # 辺が支配されている場合スコアアップ
            score += 15
        elif edge_stone == (3 - stone):  # 相手に支配されている場合スコアダウン
            score -= 15

    return score

def alphabeta(board, stone, depth, alpha, beta, maximizing_player, tt):
    """
    アルファベータ法を用いた最善の手の探索（トランスポジションテーブル対応）。
    """
    # トランスポジションテーブルのキャッシュを確認
    cached_value = tt.get(board, depth)
    if cached_value is not None:
        return cached_value, None

    if depth == 0:
        value = evaluate_board(board, stone)
        tt.set(board, depth, value)
        return value, None

    valid_moves = find_valid_moves(board, stone if maximizing_player else 3 - stone)
    if not valid_moves:
        value = evaluate_board(board, stone)
        tt.set(board, depth, value)
        return value, None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval, _ = alphabeta(new_board, stone, depth - 1, alpha, beta, False, tt)
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        tt.set(board, depth, max_eval)
        return max_eval, best_move

    else:
        min_eval = float('inf')
        opponent = 3 - stone
        for x, y in valid_moves:
            new_board = apply_move(board, opponent, x, y)
            eval, _ = alphabeta(new_board, stone, depth - 1, alpha, beta, True, tt)
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        tt.set(board, depth, min_eval)
        return min_eval, best_move

class nekosanAI:
    """
    トランスポジションテーブルとエッジ管理を備えた強化AI。
    """
    def __init__(self, depth=3, endgame_depth=8):
        self.depth = depth
        self.endgame_depth = endgame_depth
        self.tt = TranspositionTable()  # トランスポジションテーブルの初期化

    def face(self):
        return "🐱"

    def place(self, board, stone):
        """
        アルファベータ法を用いて最善の手を計算する。
        終盤では完全探索を行う。
        """
        valid_moves = find_valid_moves(board, stone)  # 置ける合法手を取得
        if not valid_moves:  # 合法手がない場合はパス
            return (-1, -1)

        remaining_moves = len(valid_moves) + len(find_valid_moves(board, 3 - stone))
        if remaining_moves <= 12:  # 終盤と判断
            _, best_move = alphabeta(board, stone, self.endgame_depth, float('-inf'), float('inf'), True, self.tt)
        else:
            _, best_move = alphabeta(board, stone, self.depth, float('-inf'), float('inf'), True, self.tt)

        # 返された手が合法手に含まれるか確認し、含まれない場合は最初の合法手を選択
        if best_move not in valid_moves:
            best_move = valid_moves[0]

        return best_move
