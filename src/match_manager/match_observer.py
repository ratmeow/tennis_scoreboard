from src.match_manager.match_components import Games, Points, Sets
from src.schemas.match import Score


class MatchObserver:
    def __init__(self, match_data: Score):
        self.is_best_of_five = match_data.is_best_of_five
        self.games = Games(initial_games=match_data.games)
        self.points = Points(
            initial_points=match_data.points, tiebreak_mode=self.games.is_tiebreak()
        )
        self.sets = Sets(initial_sets=match_data.sets, num_sets=5 if self.is_best_of_five else 3)
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
        score = Score(
            points=self.points.get(),
            games=self.games.get(),
            sets=self.sets.get(),
            is_best_of_five=self.is_best_of_five,
        )
        return score
