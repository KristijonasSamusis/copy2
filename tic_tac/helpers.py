
def check_win(board, clicked_key, letter):
    values_list = list(board.values())
    click_row = clicked_key // 20
    click_column = clicked_key % 20
    letter = letter
    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    board = list(chunk_list(values_list, 20))
    print(board)
    print(click_row, click_column, letter, board[click_row][click_column])

    height = 16
    width = 20
    score_horizontal = 0
    horizontal_left = 0
    horizontal_right = 0
    line_horizontal = 0
    change = 1
    player = letter
    while (click_column - change in range(width) and
           player in board[click_row][click_column - change]
           and "H" not in board[click_row][click_column - change]):

        horizontal_left += 1
        change += 1
        # print(f"\n\n{line}   {column_change}\n\n")
    else:
        change = 1
    while (click_column + change in range(width) and
           player in board[click_row][click_column + change]
           and "H" not in board[click_row][click_column + change]):
        horizontal_right += 1
        change += 1
    else:
        line_horizontal = horizontal_left + 1 + horizontal_right
        if line_horizontal >= 5:
            for i in range(line_horizontal):
                board[click_row][click_column - horizontal_left + i] = ("H" +
                        board[click_row][click_column - horizontal_left + i])
            score_horizontal = line_horizontal - 4

    score_vertical = 0
    vertical_up = 0
    vertical_down = 0
    line_vertical = 0
    change = 1
    while (click_row - change in range(height) and
           player in board[click_row - change][click_column]
           and "V" not in board[click_row - change][click_column]):

        vertical_up += 1
        change += 1
        # print(f"\n\n{line}   {column_change}\n\n")
    else:
        change = 1
    while (click_row + change in range(height) and
           player in board[click_row + change][click_column]
           and "V" not in board[click_row + change][click_column]):
        vertical_down += 1
        change += 1
    else:
        line_vertical = vertical_up + 1 + vertical_down
        if line_vertical >= 5:
            for i in range(line_vertical):
                board[click_row - vertical_up + i][click_column] = ("V" +
                        board[click_row - vertical_up + i][click_column])
            score_vertical = line_vertical - 4
            print(score_vertical)

    # SLASH

    score_slash = 0
    slash_up = 0
    slash_down = 0
    line_slash = 0
    change = 1
    while (click_row - change in range(height) and click_column + change in range(
            width) and
           player in board[click_row - change][click_column + change]
           and "L" not in board[click_row - change][click_column + change]):

        slash_up += 1
        change += 1
        # print(f"\n\n{line}   {column_change}\n\n")
    else:
        change = 1
    while (click_row + change in range(height) and click_column - change in range(
            width) and
           player in board[click_row + change][click_column - change]
           and "L" not in board[click_row + change][click_column - change]):
        slash_down += 1
        change += 1
    else:
        line_slash = slash_up + 1 + slash_down
        if line_slash >= 5:
            for i in range(line_slash):
                board[click_row + slash_down - i][click_column - slash_down + i] = ("L" +
                        board[click_row + slash_down - i][click_column - slash_down + i])
            score_slash = line_slash - 4
            print(score_slash)

    # SLASH

    score_backslash = 0
    backslash_up = 0
    backslash_down = 0
    line_backslash = 0
    change = 1
    while (click_row - change in range(height) and click_column - change in range(
            width) and
           player in board[click_row - change][click_column - change]
           and "R" not in board[click_row - change][click_column - change]):

        backslash_down += 1
        change += 1
    else:
        change = 1
    while (click_row + change in range(height) and click_column + change in range(
            width) and
           player in board[click_row + change][click_column + change]
           and "R" not in board[click_row + change][click_column + change]):
        backslash_up += 1
        change += 1
    else:
        line_backslash = backslash_up + 1 + backslash_down
        if line_backslash >= 5:
            for i in range(line_backslash):
                board[click_row - backslash_down + i][click_column - backslash_down + i] = ("R" +
                        board[click_row - backslash_down + i][
                            click_column - backslash_down + i])
            score_backslash = line_backslash - 4
            print(score_backslash)

    board_back = {}
    for i in range(16):
        for j in range(20):
            board_back[i*20 + j] = board[i][j]

    score = score_horizontal + score_vertical + score_slash + score_backslash
    print(score)
    return score, board_back







def is_draw(board):
    pass
    # for index in board:
    #     if board[index] == "":
    #         return False
    # return True

# def check_score():
#     big_board = [[""] * 20 for _ in range(15)]
#     print(big_board)
#
# check_score()