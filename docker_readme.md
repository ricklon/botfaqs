## This Dockerfile does the following:

    * Uses the python:3.10 base image, which is a lightweight Python image based on Debian.

    * Sets the working directory to /app.

    * Copies the pyproject.toml and poetry.lock files to the working directory.

    * Runs the poetry install command to install the dependencies specified in the pyproject.toml file.

    * Copies the rest of the project files to the working directory.

    * Runs the command poetry run python src/bot.py when the container starts.

## Updated docker commands

```

  992  docker build -t botfaqs-image .\n
  995  docker stop $(docker ps -q)\n
  996  docker run -it -v my-volume:/data -e DATA_PATH=/data/db.sqlite3 notfaqs-image
 1001  docker save botfaqs-image > botfaqs-image.tar
 1002  scp botfaqs-image.tar root@1droplet:/root
 1003  ssh root@droplet
 ```
 