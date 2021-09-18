from typing import Sequence, Optional

from gurps.character.skills import Skill

from .features import Feature


class Character:

    def __init__(
        self,
        name: str,
        st: int = 10,
        dx: int = 10,
        iq: int = 10,
        ht: int = 10,
        features: Sequence[Feature] = None,
        skills: Sequence[Skill] = None,
        notes: Optional[str] = None
    ):
        self.name = name

        self.st = st
        self.dx = dx
        self.iq = iq
        self.ht = ht

        self.features = [] if features is None else features
        self.skills = [] if skills is None else skills

        self.notes = notes

    @property
    def hp(self):
        return self.ht

    @property
    def will(self):
        return self.iq

    @property
    def perception(self):
        return self.iq

    @property
    def fp(self):
        return self.st

    @property
    def basic_speed(self) -> float:
        return (self.dx + self.hp) / 4

    @property
    def basic_move(self) -> int:
        return int(self.basic_speed)

    def __str__(self):
        return (
            f'{self.name}\n'  # TODO: add points calculator[XYZ]\n'
            f'\t{self.notes}\n'
            f'ST: {self.st} \t\t FP: {self.fp}\n'
            f'DX: {self.dx} \t\t Will: {self.will}\n'
            f'IQ: {self.iq} \t\t Per: {self.perception}\n'
            f'HT: {self.ht} \t\t HP: {self.hp}\n'
            f'Basic Speed: {self.basic_speed}\n'
            f'Basic Move: {self.basic_move}\n\n'
            f'Advantages // Disadvantages:\n'
            '\t' + '\n\t'.join(map(str, self.features)) + '\n\n'
            'Skills:\n'
            '\t' + '\n\t'.join(map(str, self.skills))
        )
