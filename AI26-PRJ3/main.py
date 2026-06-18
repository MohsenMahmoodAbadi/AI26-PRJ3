"""
University: University of Isfahan
Faculty: Mathematics and Statistics
Department: Computer Science
Course: Artificial Intelligence
Professor: Dr. Faria Nasiri Mofakham
TAs: MehrAzin Marzough, Mohammad Karimi, Anahita Honarmandian
Project: Adversarial Search in Othello (Minimax and Alpha-Beta Pruning)
"""

from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent
from tournament import play_game
import random


def evaluate_agent(agent_factory, opponent_factory, games=20, size=6):
    wins = 0
    losses = 0
    draws = 0
    score_diff_total = 0
    total_nodes = 0
    total_moves = 0
    total_time = 0.0

    for game_index in range(games):
        random.seed(14050300 + game_index)
        candidate = agent_factory()
        opponent = opponent_factory()
        candidate_is_black = game_index % 2 == 0

        if candidate_is_black:
            black_agent, white_agent = candidate, opponent
        else:
            black_agent, white_agent = opponent, candidate

        black_score, white_score = play_game(black_agent, white_agent, size=size)
        candidate_score = black_score if candidate_is_black else white_score
        opponent_score = white_score if candidate_is_black else black_score
        diff = candidate_score - opponent_score
        score_diff_total += diff

        if diff > 0:
            wins += 1
        elif diff < 0:
            losses += 1
        else:
            draws += 1

        total_nodes += getattr(candidate, "total_nodes", 0)
        total_moves += getattr(candidate, "move_count", 0)
        total_time += getattr(candidate, "elapsed_time", 0.0)

    win_rate = 100 * wins / games
    avg_diff = score_diff_total / games
    avg_nodes = total_nodes / total_moves if total_moves else 0
    avg_time_ms = 1000 * total_time / total_moves if total_moves else 0

    return {
        "games": games,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "win_rate": win_rate,
        "avg_diff": avg_diff,
        "avg_nodes": avg_nodes,
        "avg_time_ms": avg_time_ms,
    }


def print_result(agent_name, depth, opponent_name, result):
    print(
        f"{agent_name:<10} depth={depth:<2} vs {opponent_name:<6} | "
        f"games={result['games']:>2} wins={result['wins']:>2} "
        f"draws={result['draws']:>2} losses={result['losses']:>2} "
        f"win_rate={result['win_rate']:>5.1f}% "
        f"avg_diff={result['avg_diff']:>6.2f} "
        f"avg_nodes={result['avg_nodes']:>8.1f} "
        f"avg_time_ms={result['avg_time_ms']:>7.2f}"
    )


def run_experiments():
    depths = (2, 3, 4)
    opponents = (
        ("Random", RandomAgent),
        ("Greedy", GreedyAgent),
    )
    agents = (
        ("Minimax", MinimaxAgent),
        ("AlphaBeta", AlphaBetaAgent),
    )

    for agent_name, agent_class in agents:
        for depth in depths:
            for opponent_name, opponent_class in opponents:
                result = evaluate_agent(
                    lambda cls=agent_class, d=depth: cls(depth=d),
                    opponent_class,
                    games=20,
                    size=6,
                )
                print_result(agent_name, depth, opponent_name, result)


if __name__ == "__main__":
    run_experiments()
