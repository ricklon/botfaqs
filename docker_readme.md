## This Dockerfile does the following:

    * Uses the python:3.10 base image, which is a lightweight Python image based on Debian.

    * Sets the working directory to /app.

    * Copies the pyproject.toml and poetry.lock files to the working directory.

    * Runs the poetry install command to install the dependencies specified in the pyproject.toml file.

    * Copies the rest of the project files to the working directory.

    * Runs the command poetry run python src/bot.py when the container starts.
