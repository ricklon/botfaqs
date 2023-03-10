from tortoise.models import Model
from tortoise import fields
from tortoise.expressions import F
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

import creds

openai.api_key = creds.open_ai_token
embed_model_engine = "text-embedding-ada-002"

class FAQ(Model):
    """Model for frequently asked questions."""
    id = fields.IntField(pk=True)
    message_id = fields.CharField(max_length=64)
    channel_id = fields.CharField(max_length=64)
    question = fields.TextField()
    answer = fields.TextField()
    likes = fields.IntField(default=0)
    dislikes = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


async def get_votes(faq_id):
    faq = await FAQ.get(id=faq_id)
    votes_up = faq.likes
    votes_down = faq.dislikes
    return votes_up, votes_down

async def add_faq(channel_id, message_id, question, answer):
    """Create a new FAQ entry."""
    faq = await FAQ.create(channel_id=channel_id, message_id=message_id, question=question, answer=answer)
    return faq.id

async def list_faqs(channel_id):
    """Retrieve a list of all FAQ entries for a particular channel."""
    return await FAQ.filter(channel_id=channel_id).all()

async def update_faq(faq_id, question, answer):
    """Update the question and answer for a particular FAQ entry."""
    await FAQ.filter(id=faq_id).update(question=question, answer=answer)

async def update_message_id(faq_id, message_id):
    """Update the message_id for a particular FAQ entry."""
    await FAQ.filter(id=faq_id).update(message_id=message_id)

async def delete_faq(faq_id):
    """Delete a particular FAQ entry."""
    await FAQ.filter(id=faq_id).delete()

async def get_faq(faq_id):
    """Retrieve a particular FAQ entry."""
    return await FAQ.get(id=faq_id)

async def like_faq(faq_id):
    """Increment the number of likes for an FAQ entry."""
    await FAQ.filter(id=faq_id).update(likes=F('likes') + 1)   

async def unlike_faq(faq_id):
    """Increment the number of likes for an FAQ entry."""
    await FAQ.filter(id=faq_id).update(likes=F('likes') - 1)     

async def dislike_faq(faq_id):
    """Increment the number of dislikes for an FAQ entry."""
    await FAQ.filter(id=faq_id).update(dislikes=F('likes') + 1)

async def undislike_faq(faq_id):
    # Get the FAQ with the specified ID
     """Decriment the number of dislikes for an FAQ entry."""
     await FAQ.filter(id=faq_id).update(dislikes=F('likes') - 1)

async def bulk_add_faqs(channel_id, message_id, faqs):
    """Create multiple new FAQ entries from a JSON object."""
    # Parse the JSON object
    try:
        faqs = json.loads(faqs)
    except json.JSONDecodeError:
        return 'Invalid JSON format.'

    # Iterate through the list of FAQs and add them to the database
    for faq in faqs:
        await add_faq(channel_id, message_id, faq['question'], faq['answer'])
    return 'FAQs added successfully!'

async def search_questions_and_answers(query):
    embedding = get_embedding(query, model='text-embedding-ada-002')
    # Initialize a list to store the results
    results = []

    # Retrieve the questions and answers from the database
    faqs = await FAQ.all()
    questions = [faq.question for faq in faqs]
    answers = [faq.answer for faq in faqs]

    # Iterate through the questions and answers in the database
    for question, answer in zip(questions, answers):
        # Generate an embedding vector for the question
        response = openai.Encode.create(engine=model_engine, prompt=question)
        question_vector = response['data'][0]['vector']

        # Compute the cosine similarity between the query vector and the question vector
        cosine_similarity = cosine(query_vector, question_vector)
        if cosine_similarity > 0.5:
            # Add the question and answer to the results list if the cosine similarity is above a certain threshold
            results.append((question, answer))

    return results

#Reset all FAQs
async def reset_all():
    """Delete all FAQ entries."""
    await FAQ.all().delete()

