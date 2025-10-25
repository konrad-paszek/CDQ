import os
from functools import lru_cache

from dotenv import load_dotenv

from cdq.environment import Environment


class Configuration:
    prefix = "CDQ"

    @classmethod
    def inspect(cls):
        return {k: v for k, v in os.environ.items() if k.startswith(cls.prefix)}

    def get(self, section_option: str, default=None, raises=True, astype=None):
        section, option = tuple(section_option.split("."))
        var = f"{self.prefix}__{section}__{option}".upper()
        val = os.getenv(var, default=None)
        if not val and raises:
            raise ValueError(f"{var} not found")
        if astype:
            return astype(val)
        return val

    @classmethod
    def from_dotenv(cls, dotenv_path: str):
        load_dotenv(dotenv_path=dotenv_path)
        return cls()


@lru_cache(maxsize=1)
def get_config() -> Configuration:
    dotenv_path = Environment.node()
    if not dotenv_path:
        raise RuntimeError("Unable to resolve configuration")
    return Configuration.from_dotenv(dotenv_path=dotenv_path)
