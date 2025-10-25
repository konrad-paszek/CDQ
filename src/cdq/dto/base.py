from dataclasses import asdict, dataclass


@dataclass
class Dto:
    def to_dict(self):
        return asdict(self)
