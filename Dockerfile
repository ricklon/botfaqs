FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the project files
COPY . .

# Run the bot
CMD ["poetry", "run", "python", "src/bot.py"]
