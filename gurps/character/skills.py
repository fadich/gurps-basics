from abc import abstractmethod
from typing import Optional

from gurps.exceptions import GurpsError


class PointsError(GurpsError):
    pass


class Difficulty:

    def __init__(self, name: str):
        self.name = name

    def calculate_bonus(self, points: int):
        return self._calculate_bonus(points)

    @abstractmethod
    def _calculate_bonus(self, points: int):
        pass


class MediumDifficulty(Difficulty):

    def __init__(self):
        super().__init__(name='medium')

    def _calculate_bonus(self, points: int) -> int:
        # TODO: Implement it
        return 0


class Skill:

    def __init__(
        self,
        name: str,
        description: str,
        based_on_name: str,
        based_on_reference: int,
        default_modifier: int = -5,
        difficulty: [Difficulty] = None,
        points: int = 0
    ):
        if difficulty is None:
            difficulty = MediumDifficulty()

        self.name = name
        self.description = description
        self.based_on_name = based_on_name
        self.based_on_reference = based_on_reference
        self.difficulty = difficulty
        self.points = points
        self.default_modifier = default_modifier

        self._override_level: Optional[int] = None

    @property
    def bonus(self):
        if self.points <= 0:
            return self.default_modifier

        return self.difficulty.calculate_bonus(self.points)

    @property
    def level(self):
        if self._override_level is not None:
            return self._override_level

        return self.based_on_reference + self.bonus

    @level.setter
    def level(self, value: int):
        self._override_level = value

    def __str__(self):
        symb = '+' if self.bonus > 0 else '-'
        string = f'{self.name} '
        if self._override_level is None:
            string += f'{self.based_on_name.upper()}{symb}{abs(self.bonus)} '
            string += f'[{self.points}] '
        string += f' -> {self.level}'

        return string

    def __hash__(self):
        return hash(self.name)
