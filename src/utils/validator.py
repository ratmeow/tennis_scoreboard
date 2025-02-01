import logging

from src.utils.exceptions import ServiceValidationError

logger = logging.getLogger(__name__)


class FieldValidator:
    @classmethod
    def validate_player_names(cls, player1_name: str, player2_name: str):
        cls.validate_name(name=player1_name, field="Player 1 name")
        cls.validate_name(name=player2_name, field="Player 2 name")
        if player1_name == player2_name:
            raise ServiceValidationError(message="Player can't play with himself")

    @staticmethod
    def validate_name(name: str, field: str = "Player name"):
        FieldValidator.validate_string_only_english_letters(value=name, field_name=field)
        FieldValidator.validate_string_field_less_than_len(value=name, length=50, field_name=field)

    @staticmethod
    def validate_string_only_english_letters(value: str, field_name: str):
        if not all(char.isalpha() and char.isascii() for char in value):
            raise ServiceValidationError(
                message=f"{field_name} [{value}] has extra characters or digits"
            )

    @staticmethod
    def validate_string_field_less_than_len(value: str, length: int, field_name: str):
        if len(value) > length:
            raise ServiceValidationError(message=f"{field_name} length must be less than {length}")
