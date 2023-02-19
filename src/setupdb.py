import os
from tortoise import Tortoise

# Use the DATA_PATH environment variable if it is set,
# otherwise use the relative path "../data/db.sqlite3"
db_path = os.environ.get("DATA_PATH", "../data/db.sqlite3")

async def create_database():
    # Connect to the database
    await Tortoise.init(
        db_url=f'sqlite:///{db_path}',
        modules={'models': ['faqorm']}
    )

    # Create the database tables
    await Tortoise.generate_schemas()
