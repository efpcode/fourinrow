from fourinrow.fourinrow import create_board, Players


def test_board_defaults():
    board = create_board()
    none_vals = sum([value.count(None) for value in board])
    expected_value = len(board) * len(board[0])
    assert none_vals == expected_value


def test_default_tokens():
    assert Players.NO_PLAYER.value == "\u2610"
    assert Players.PLAYER_1.value == "\U0001F534"
    assert Players.PLAYER_2.value == "\U0001F535"
    assert Players.CPU.value == "\U0001F916"
