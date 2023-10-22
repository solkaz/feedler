# pylint: disable=invalid-name

"""
Entry point for server
"""
import uvicorn
from app.env import EnvVarEnum, env

app_name = "app.main:app"


if __name__ == "__main__":
    uvicorn.run(
        app_name,
        host=env(EnvVarEnum.FEEDLER_HOST),
        port=env(EnvVarEnum.FEEDLER_PORT),
    )
