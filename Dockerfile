FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the requirements file
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the project files
COPY . .

# Create a volume for the SQL data
VOLUME /data

# Copy the settings file into the image
COPY src/settings.toml .

# Run the bot
#CMD ["poetry", "run", "python", "src/bot.py"]
CMD ["poetry", "run", "python", "src/bot.py"]
