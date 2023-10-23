# pylint: disable=invalid-name

"""
Entry point for server
"""
import uvicorn

from feedler.env import EnvVarEnum, env

app_name = "feedler.app.main:app"


if __name__ == "__main__":
    uvicorn.run(
        app_name,
        host=env(EnvVarEnum.FEEDLER_HOST),
        port=env(EnvVarEnum.FEEDLER_PORT),
    )
