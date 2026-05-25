def get_legal_moves(board, player):
    """Returns the legal moves the bot can do."""
    moves = []

    for i in range(len(board.field_collection.fields)):
        if board.field_collection.can_seed_from(i, player):
            moves.append(i)

    return moves


def choose_move(board, player, depth):
    """Lets the bot pick a move."""
    legal_moves = get_legal_moves(board, player)

    best_move = None
    best_score = float("-inf")

    opponent = next(p for p in board.bank if p is not player)

    for move in legal_moves:
        clone = board.clone_deep()

        clone.seed_from_field(move, player)

        if depth <= 1:
            score = clone.bank[player] - clone.bank[opponent]
        else:
            opponent_move = choose_move(clone, opponent, depth - 1)
            if opponent_move is not None:
                clone.seed_from_field(opponent_move, opponent)

            score = clone.bank[player] - clone.bank[opponent]

        if score > best_score:
            best_score = score
            best_move = move

    return best_move
