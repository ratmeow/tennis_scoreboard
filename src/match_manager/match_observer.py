from src.schemas import Score
from src.match_manager.match_components import Sets, Games, Points


class MatchObserver:

    def __init__(self, match_data: Score):

        self.games = Games(initial_games=match_data.games)
        self.points = Points(initial_points=match_data.points, tiebreak_mode=self.games.is_tiebreak())
        self.sets = Sets(initial_sets=match_data.sets)
        self.winner_exists: bool = False

    def add_points(self, player_idx: int):
        self.points.add(player_idx=player_idx)
        if self.points.game_win:
            self.points.reset()
            self.games.add(player_idx=player_idx, tiebreak_win=self.games.is_tiebreak())
        if self.games.set_win:
            self.sets.add(player_idx=player_idx)
            if self.sets.match_win:
                self.winner_exists = True
            else:
                self.games.reset()

    def check_winner_exists(self):
        return self.winner_exists

    def get_data(self) -> Score:

        score = Score(points=self.points.get(),
                      games=self.games.get(),
                      sets=self.sets.get())
        return score
