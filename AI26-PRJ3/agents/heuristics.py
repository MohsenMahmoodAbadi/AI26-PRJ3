def evaluate_othello(game, player):
    opponent = -player
    black_score, white_score = game.score()
    player_discs = black_score if player == 1 else white_score
    opponent_discs = white_score if player == 1 else black_score
    disc_diff = player_discs - opponent_discs

    if game.game_over():
        if disc_diff > 0:
            return 100000 + disc_diff
        if disc_diff < 0:
            return -100000 + disc_diff
        return 0

    player_moves = len(game.get_valid_moves(player))
    opponent_moves = len(game.get_valid_moves(opponent))
    mobility = player_moves - opponent_moves

    board = game.board
    size = game.size

    position_score = 0
    edge_score = 0
    frontier_score = 0
    for r in range(size):
        for c in range(size):
            cell = board[r][c]
            if cell == 0:
                continue

            sign = 1 if cell == player else -1
            position_score += sign * square_weight(size, r, c)

            if r in (0, size - 1) or c in (0, size - 1):
                edge_score += sign

            if has_empty_neighbor(game, r, c):
                frontier_score += sign

    corners = [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
    corner_score = sum(corner_value(board[r][c], player) for r, c in corners)

    corner_risk = 0
    for r, c in corners:
        if board[r][c] != 0:
            continue
        for ar, ac in adjacent_to_corner(size, r, c):
            corner_risk += corner_value(board[ar][ac], player)

    empty_count = sum(cell == 0 for row in board for cell in row)
    total_cells = size * size
    early_game = empty_count > total_cells * 0.45

    disc_weight = 2 if early_game else 12
    mobility_weight = 12 if early_game else 6

    return (
        disc_weight * disc_diff
        + mobility_weight * mobility
        + 4 * position_score
        + 25 * corner_score
        - 12 * corner_risk
        + 5 * edge_score
        - 4 * frontier_score
    )


def square_weight(size, row, col):
    last = size - 1
    if (row, col) in ((0, 0), (0, last), (last, 0), (last, last)):
        return 30

    near_top_or_bottom = row in (1, last - 1)
    near_left_or_right = col in (1, last - 1)
    on_edge = row in (0, last) or col in (0, last)

    if near_top_or_bottom and near_left_or_right:
        return -14
    if on_edge and (near_top_or_bottom or near_left_or_right):
        return -8
    if on_edge:
        return 8
    return 2


def has_empty_neighbor(game, row, col):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if game.inside(nr, nc) and game.board[nr][nc] == 0:
                return True
    return False


def corner_value(cell, player):
    if cell == player:
        return 1
    if cell == -player:
        return -1
    return 0


def adjacent_to_corner(size, row, col):
    rows = [0, 1] if row == 0 else [size - 2, size - 1]
    cols = [0, 1] if col == 0 else [size - 2, size - 1]
    return [(r, c) for r in rows for c in cols if (r, c) != (row, col)]
