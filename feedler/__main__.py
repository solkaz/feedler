# pylint: disable=invalid-name

"""
Entry point for server
"""
import uvicorn
from app import env

app_name = "app.main:app"


if __name__ == "__main__":
    uvicorn.run(app_name, host=env.env("FEEDLER_HOST"), port=env.env("FEEDLER_PORT"))
