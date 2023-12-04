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
    FEEDLER_PG_URL = "FEEDLER_PG_URL"
    PROJECT_NAME = "PROJECT_NAME"


env = Env(FEEDLER_HOST=str, FEEDLER_PORT=int, FEEDLER_PG_URL=str, PROJECT_NAME=str)

env.read_envfile(".env")
