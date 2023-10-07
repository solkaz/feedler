"""
Wrapper to handle environment variables
"""
from envparse import Env

env = Env(
    FEEDLER_HOST=str,
    FEEDLER_PORT=int,
)

env.read_envfile(".env")
