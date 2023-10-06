# pylint: disable=invalid-name

"""
Entry point for server
"""
import uvicorn
from envparse import Env

env = Env(
    FEEDLER_HOST=str,
    FEEDLER_PORT=int,
)

env.read_envfile(".env")

app_name = "app.main:app"


if __name__ == "__main__":
    uvicorn.run(app_name, host=env("FEEDLER_HOST"), port=env("FEEDLER_PORT"))
