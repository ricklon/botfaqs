from tortoise import Tortoise

async def create_database():
    # Connect to the database
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['faqorm']}
    )

    # Create the database tables
    await Tortoise.generate_schemas()

