from ..exceptions import GurpsError


class DiceError(GurpsError):
    pass


class DiceParseError(DiceError, ValueError):
    pass
