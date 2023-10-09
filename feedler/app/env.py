"""
Wrapper to handle environment variables
"""
from enum import Enum

from envparse import Env


class EnvVarEnum(str, Enum):
    """
    Name of environment variable
    """

    FEEDLER_HOST = "FEEDLER_HOST"
    FEEDLER_PORT = "FEEDLER_PORT"


env = Env(
    FEEDLER_HOST=str,
    FEEDLER_PORT=int,
)

env.read_envfile(".env")
