#import pdb
import os
import asyncio
import logging
import toml

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import csv
import faqorm 
import setupdb

#load secrets
import creds

# Load the settings from the settings.toml file
settings = toml.load("settings.toml")

# Extract the values from the settings dictionary
allowed_channel_name = settings["allowed_channel_name"]
allowed_channel_id = settings["allowed_channel_id"]


# Get the list of default intents
intents = discord.Intents.all()

# Create a Bot instance with the specified command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Define the on_ready event handler
@bot.event
async def on_ready():
    await setupdb.create_database()
    # Print the bot's name
    print(f"Logged in as {bot.user.name}")

    # Get the channel object for the allowed channel
    channel = bot.get_channel(allowed_channel_id)
    await channel.send(f"Logged in as {bot.user.name}")

@bot.command()
async def hello(ctx):
    name = ctx.message.author.name
    await ctx.send(f'Nice to meet you, {name}!')

@bot.command()
async def exit(ctx):
    """Shut down the bot."""
    # Check if the user has the "administrator" permission
    if ctx.author.guild_permissions.administrator:
        await ctx.send('Shutting down...')
        await bot.logout()
    else:
        await ctx.send('You do not have permission to shut down the bot.')



@bot.command()
async def add_faq(ctx, channel: discord.TextChannel = None):
    """Add a new FAQ entry."""
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel
    print(f"Adding FAQ for channel: {ctx.channel.name}, id: {channel.id}, msg.id: {ctx.message.id}")
    # Set the channel_id to the channel's ID
    channel_id = channel.id


    # Prompt the user for the question
    await ctx.send('What is the question you would like to add to the FAQ?')
    question_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    question = question_response.content

    # Prompt the user for the answer
    await ctx.send('What is the answer to the question?')
    answer_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    answer = answer_response.content

    # Add the FAQ entry
    await faqorm.add_faq(channel_id, ctx.message.id, question, answer)
    await ctx.send('FAQ added successfully!')


@bot.command()
async def list_faqs(ctx,  channel: discord.TextChannel = None):
    """List all FAQ entries for a particular channel."""
    # If no channel is provided, use the current channel
    if channel is None:
        channel = ctx.channel
    print(f"Adding FAQ for channel: {ctx.channel.name}, id: {channel.id}, msg.id: {ctx.message.id}")
    # Set the channel_id to the channel's ID
    channel_id = channel.id

    faqs = await faqorm.list_faqs(str(channel_id))
    if not faqs:
        await ctx.send('There are no FAQs for this channel.')
    else:
        for faq in faqs:
            await ctx.send(f'id: {faq.id}, channel: {bot.get_channel(int(faq.channel_id))}, msg_id: {faq.message_id}, {faq.question}: {faq.answer}, likes: {faq.likes}')

@bot.command()
async def update_faq(ctx, faq_id: int = None):
    # If no faq_id is provided, prompt the user for the faq_id
    if faq_id is None:
        await ctx.send('Please enter the ID of the FAQ you want to update:')
        faq_id_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        try:
            faq_id = int(faq_id_message.content)
        except ValueError:
            await ctx.send('Invalid FAQ ID. Please enter a valid ID.')
            return

    # Get the faq for the given faq_id
    faq = await faqorm.get_faq(faq_id)
    if faq is None:
        await ctx.send(f'No FAQ found with ID {faq_id}')
        return

    # Display the current question and answer to the user in an embed
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=faq.question)
    embed.add_field(name='Answer', value=faq.answer)
    await ctx.send(embed=embed)

    # Prompt the user for the new question
    await ctx.send('What is the new question?')
    question_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    question = question_response.content
    
    # Prompt the user for the new answer
    await ctx.send('What is the new answer?')
    answer_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    answer = answer_response.content

    # Display the new question and answer to the user in an embed
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=question)
    embed.add_field(name='Answer', value=answer)
    await ctx.send(embed=embed)

    # Prompt the user to confirm the update
    await ctx.send('Are you sure you want to update this FAQ? (y/n)')
    confirmation_response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    if confirmation_response.content.lower() != 'y':
        await ctx.send('FAQ update cancelled.')
        return

    # Update the FAQ entry
    await faqorm.update_faq(faq_id, question, answer)
    await ctx.send('FAQ updated successfully!')



@bot.command()
async def delete_faq(ctx, faq_id: int = None):
    # If no faq_id is provided, prompt the user for the faq_id
    if faq_id is None:
        await ctx.send('Please enter the ID of the FAQ you want to delete:')
        faq_id_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        try:
            faq_id = int(faq_id_message.content)
        except ValueError:
            await ctx.send('Invalid FAQ ID. Please enter a valid ID.')
            return

    # Get the faq for the given faq_id
    faq = await faqorm.get_faq(faq_id)
    if faq is None:
        await ctx.send(f'No FAQ found with ID {faq_id}')
        return

    # Display the current question and answer to the user
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=faq.question)
    embed.add_field(name='Answer', value=faq.answer)
    await ctx.send(embed=embed)

    # Prompt the user to confirm the deletion
    await ctx.send('Are you sure you want to delete this FAQ? (yes/no)')

    # Wait for the user's response
    delete_confirm_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    delete_confirm = delete_confirm_message.content.lower()

    # If the user confirms the deletion, delete the FAQ
    if delete_confirm == 'yes':
        await faqorm.delete_faq(faq_id)
        await ctx.send('FAQ deleted successfully!')
    elif delete_confirm == 'no':
        await ctx.send('Deletion cancelled')
    else:
        await ctx.send('Invalid response. Deletion cancelled.')

    

@bot.command()
async def get_faq(ctx, faq_id: int = None):
    # If no faq_id is provided, prompt the user for the faq_id
    if faq_id is None:
        await ctx.send('Please enter the ID of the FAQ you want to retrieve:')
        faq_id_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        try:
            faq_id = int(faq_id_message.content)
        except ValueError:
            await ctx.send('Invalid FAQ ID. Please enter a valid ID.')
            return

    # Get the faq for the given faq_id
    faq = await faqorm.get_faq(faq_id)
    if faq:
        # Display the faq_id, question, and answer to the user
        embed = discord.Embed(title=f'FAQ #{faq_id}', description=faq.question)
        embed.add_field(name='Answer', value=faq.answer)
        embed.add_field(name='Likes', value=f':thumbsup: {faq.likes}')
        await ctx.send(embed=embed)
    else:
        await ctx.send('FAQ not found.')


@bot.command()
async def like_faq(ctx, faq_id: int = None):
    # If no faq_id is provided, prompt the user for the faq_id
    if faq_id is None:
        await ctx.send('Please enter the ID of the FAQ you want to like:')
        faq_id_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        try:
            faq_id = int(faq_id_message.content)
        except ValueError:
            await ctx.send('Invalid FAQ ID. Please enter a valid ID.')
            return

    # Get the faq for the given faq_id
    faq = await faqorm.get_faq(faq_id)
    if faq is None:
        await ctx.send(f'No FAQ found with ID {faq_id}')
        return

    # Display the current question and answer to the user
    embed = discord.Embed(title=f'FAQ #{faq_id}', description=faq.question)
    embed.add_field(name='Answer', value=faq.answer)
    embed.add_field(name='Likes', value=faq.likes)
    await ctx.send(embed=embed)

    # Confirm with the user that they want to like this FAQ
    confirm_message = await ctx.send('Do you want to like this FAQ? (y/n)')
    # Wait for the user's response
    response_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    if response_message.content.lower() == 'y':
        # Increment the number of likes for the FAQ
        await faqorm.like_faq(faq_id)
        await ctx.send('FAQ liked successfully!')
    else:
        await ctx.send('FAQ not liked.')
    # Delete the confirm message
    await confirm_message.delete()
    # Delete the user's response message
    await response_message.delete()

import csv

@bot.command()
async def bulk_add(ctx):
    # Prompt the user for the CSV text
    await ctx.send('Please enter the CSV text:')

    # Wait for the user's response
    csv_text_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    csv_text = csv_text_message.content

    # Parse the CSV text
    csv_reader = csv.reader(csv_text.splitlines())
    questions_and_answers = list(csv_reader)

    # Add the questions and answers to the database
    for question, answer in questions_and_answers:
        await faqorm.add_faq(channel_id=ctx.channel.id, message_id=ctx.message.id, question=question, answer=answer)

    # Confirm that the FAQs were added successfully
    await ctx.send('FAQs added successfully!')


@bot.command()
async def bulk_add_csv(ctx):
    # Prompt the user for the CSV file
    await ctx.send('Please enter the CSV file containing the FAQs:')
    csv_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    csv_file = csv_message.content
    # Process the CSV file
    await process_csv(ctx.channel.id, ctx.message.id, csv_file)
    # Send a success message to the user
    await ctx.send('FAQs added successfully!')

async def process_csv(channel_id, message_id, csv_file: str):
    """Process a CSV file containing FAQs and add them to the database."""
    # Parse the CSV file
    faqs = []
    try:
        reader = csv.reader(csv_file.splitlines())
        for row in reader:
            # Check if the first column is a question number
            if row[0].isdigit():
                # If it is a question number, use the second and third columns as the question and answer
                question = row[1]
                answer = row[2]
            else:
                # If it is not a question number, use the first and second columns as the question and answer
                question = row[0]
                answer = row[1]
            # Add the FAQ to the list
            faqs.append((question, answer))
    except csv.Error as e:
        print(f'Error parsing CSV file: {e}')
        return

    # Add the FAQs to the database
    for question, answer in faqs:
        await faqorm.add_faq(channel_id, message_id, question, answer)


@bot.command()
async def bulk_add_json(ctx):
    """Add multiple FAQ entries from a JSON object."""
    # Prompt the user for the JSON object
    await ctx.send('Please enter the JSON object containing the list of FAQs:')
    json_message = await bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
    # Add the FAQs to the database
    result = await faqorm.bulk_add_faqs(str(ctx.channel.id), ctx.message.id, json_message.content)
    await ctx.send(result)

def run():
    # run the tortoise orm setup
    asyncio.run(setupdb.create_database())
    # Use the Discord bot token variable when starting the bot
    bot.run(creds.discord_bot_token)

if __name__ == "__main__":
    run()
