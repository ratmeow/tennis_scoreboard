class Points:
    points_range = [0, 15, 30, 40, -1]

    def __init__(self, initial_points, tiebreak_mode: bool = False):
        self.game_win: bool = False
        self.tiebreak_mode = tiebreak_mode
        self.points = initial_points  # [15, 30]
        self.positions = [0, 0]
        if not tiebreak_mode:
            self.positions = [self.points_range.index(self.points[0]), self.points_range.index(self.points[1])]

    def add(self, player_idx):
        if self.tiebreak_mode:
            self.add_tiebreak(player_idx=player_idx)
        else:
            self.add_common(player_idx=player_idx)

    def add_common(self, player_idx):
        opponent_idx = 1 - player_idx

        if self.positions[player_idx] < 3:
            self.positions[player_idx] += 1
        elif self.positions[player_idx] == 3:
            if self.positions[opponent_idx] < 3:
                self.game_win = True
                return
            elif self.positions[opponent_idx] == 3:
                self.positions[player_idx] += 1
            elif self.positions[opponent_idx] == 4:
                self.positions[opponent_idx] -= 1
        elif self.positions[player_idx] == 4:
            self.game_win = True
            return

    def add_tiebreak(self, player_idx):
        opponent_idx = 1 - player_idx
        self.points[player_idx] += 1
        if self.points[player_idx] >= 7 and (self.points[player_idx] - self.points[opponent_idx]) >= 2:
            self.game_win = True
            return

    def is_game_win(self) -> bool:
        return self.game_win

    def reset(self):
        if self.tiebreak_mode:
            self.points = [0, 0]
        self.positions = [0, 0]

    def get(self):
        if self.tiebreak_mode:
            return self.points
        return [self.points_range[i] for i in self.positions]


class Games:

    def __init__(self, initial_games):
        self.set_win: bool = False
        self.games: list[list[int]] = initial_games  # [[6, 1], [0, 4]]
        self.current_game: list[int] = self.games[-1]  # [0, 4]

    def add(self, player_idx, tiebreak_win: bool = False):
        opponent_idx = 1 - player_idx
        self.current_game[player_idx] += 1
        if tiebreak_win or (self.current_game[player_idx] >= 6 and (
                self.current_game[player_idx] - self.current_game[opponent_idx] >= 2)):
            self.set_win = True
            return

    def is_set_win(self) -> bool:
        return self.set_win

    def reset(self):
        self.games.append([0, 0])

    def get(self):
        return self.games

    def is_tiebreak(self) -> bool:
        if self.current_game == [6, 6]:
            return True
        return False


class Sets:
    def __init__(self, initial_sets, num_sets: int = 3):
        self.match_win: bool = False
        self.sets = initial_sets  # [1, 2]
        self.num_sets = num_sets

    def add(self, player_idx):
        self.sets[player_idx] += 1
        if self.sets[player_idx] == (self.num_sets - 1):
            self.match_win = True

    def is_match_win(self) -> bool:
        return self.match_win

    def get(self):
        return self.sets
