import time

from agents.heuristics import evaluate_othello


class AlphaBetaAgent:
    def __init__(self, depth=4):
        self.depth = depth
        self.reset_stats()

    def reset_stats(self):
        self.nodes_searched = 0
        self.total_nodes = 0
        self.move_count = 0
        self.elapsed_time = 0.0
        self.last_value = 0
        self.last_nodes = 0

    def evaluate(self, game, player):
        return evaluate_othello(game, player)

    def alphabeta(self, game, depth, alpha, beta, maximizing, root_player):
        self.nodes_searched += 1

        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None

        current_player = root_player if maximizing else -root_player
        moves = game.get_valid_moves(current_player)

        if not moves:
            value, _ = self.alphabeta(
                game, depth - 1, alpha, beta, not maximizing, root_player
            )
            return value, None

        moves = self.ordered_moves(game, moves, current_player, root_player, maximizing)

        best_move = None
        if maximizing:
            best_value = float("-inf")
            for move in moves:
                child = game.copy()
                child.make_move(current_player, *move)
                value, _ = self.alphabeta(child, depth - 1, alpha, beta, False, root_player)
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value, best_move

        best_value = float("inf")
        for move in moves:
            child = game.copy()
            child.make_move(current_player, *move)
            value, _ = self.alphabeta(child, depth - 1, alpha, beta, True, root_player)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

    def ordered_moves(self, game, moves, current_player, root_player, maximizing):
        scored_moves = []
        for move in moves:
            child = game.copy()
            child.make_move(current_player, *move)
            scored_moves.append((self.evaluate(child, root_player), move))

        scored_moves.sort(reverse=maximizing, key=lambda item: item[0])
        return [move for _, move in scored_moves]

    def choose_move(self, game, player):
        self.nodes_searched = 0
        started_at = time.perf_counter()
        value, move = self.alphabeta(
            game, self.depth, float('-inf'), float('inf'), True, player
        )
        self.last_value = value
        self.last_nodes = self.nodes_searched
        self.total_nodes += self.last_nodes
        self.move_count += 1
        self.elapsed_time += time.perf_counter() - started_at
        return move
