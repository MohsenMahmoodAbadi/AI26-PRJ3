from game.othello import Othello, BLACK, WHITE


def play_game(agent_black, agent_white, size=6, return_history=False):
    game = Othello(size)
    player = BLACK
    history = []

    while not game.game_over():
        moves = game.get_valid_moves(player)
        if moves:
            agent = agent_black if player == BLACK else agent_white
            move = agent.choose_move(game, player)
            if move not in moves:
                raise ValueError(f"Illegal move {move} by player {player}")
            game.make_move(player, *move)
            history.append((player, move, game.score()))
        else:
            history.append((player, None, game.score()))

        if player == BLACK:
            player = WHITE
        else:
            player = BLACK

    if return_history:
        return game.score(), history
    return game.score()
