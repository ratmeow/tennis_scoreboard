import random

from src.schemas import Score
from src.match_manager.match_observer import MatchObserver


def test_win_point_at_40_40():
    score = Score(points=[40, 40])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.games[0] == [0, 0]
    assert new_score.points == [-1, 40]  # -1 equals AD


def test_win_point_at_ad_40():
    score = Score(points=[-1, 40])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.games[0] == [1, 0]
    assert new_score.points == [0, 0]


def test_lose_point_at_ad_40():
    score = Score(points=[-1, 40])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=1)
    new_score = match_observer.get_data()

    assert new_score.games[0] == [0, 0]
    assert new_score.points == [40, 40]


def test_win_point_at_40_and_40_less():
    score = Score(points=[40, random.choice([0, 15, 30])])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.games[0] == [1, 0]


def test_set_win_after_6_and_less():
    score = Score(games=[[5, random.choice(range(0, 5))]], points=[40, 0])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.sets == [1, 0]


def test_set_win_after_6_and_5():
    score = Score(games=[[6, 5]], points=[40, 0])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.sets == [1, 0]


def test_tiebreak_start():
    score = Score(games=[[6, 6]])
    match_observer = MatchObserver(match_data=score)
    assert match_observer.games.is_tiebreak() is True


def test_set_win_after_tiebreak_win():
    score = Score(games=[[6, 6]], points=[6, 5])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.games[0] == [7, 6]
    assert new_score.sets == [1, 0]


def test_tiebreak_2point_advantage_to_win():
    score = Score(games=[[6, 6]], points=[6, 6])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert match_observer.games.is_tiebreak() is True
    assert new_score.games[0] == [6, 6]
    assert new_score.sets == [0, 0]


def test_match_win():
    score = Score(sets=[1, 0], games=[[7, 6], [5, 3]], points=[40, 15])
    match_observer = MatchObserver(match_data=score)
    match_observer.add_points(player_idx=0)
    new_score = match_observer.get_data()

    assert new_score.sets == [2, 0]
    assert match_observer.check_winner_exists() is True


