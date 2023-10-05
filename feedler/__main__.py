# pylint: disable=invalid-name

"""
Entry point for server
"""
import os

import uvicorn

host = os.getenv("FEEDLER_HOST", "0.0.0.0")
port = int(os.getenv("FEEDLER_PORT", "8000"))

app_name = "app.main:app"


if __name__ == "__main__":
    uvicorn.run(app_name, host=host, port=port)
