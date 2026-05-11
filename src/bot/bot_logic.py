from game_logic.Board import Board

def get_legal_moves(board, player):
    moves = []

    for i in range(len(board.field_collection.fields)):
        if board.field_collection.can_seed_from(i, player):
            moves.append(i)

    return moves


def choose_move(board, player, get_legal_moves):
    legal_moves = get_legal_moves(board, player)

    best_move = None
    best_score = float("-inf")

    opponent = next(p for p in board.bank if p is not player)

    for move in legal_moves:
        clone = board.clone_deep()

        clone.seed_from_field(move, player)

        score = clone.bank[player] - clone.bank[opponent]

        if score > best_score:
            best_score = score
            best_move = move

    return best_move