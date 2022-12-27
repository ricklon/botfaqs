from tortoise.models import Model
from tortoise import fields
from tortoise.expressions import F
import json



class FAQ(Model):
    """Model for frequently asked questions."""
    id = fields.IntField(pk=True)
    message_id = fields.CharField(max_length=64)
    channel_id = fields.CharField(max_length=64)
    question = fields.TextField()
    answer = fields.TextField()
    likes = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

async def add_faq(channel_id, message_id, question, answer):
    """Create a new FAQ entry."""
    faq = await FAQ.create(channel_id=channel_id, message_id=message_id, question=question, answer=answer)

async def list_faqs(channel_id):
    """Retrieve a list of all FAQ entries for a particular channel."""
    return await FAQ.filter(channel_id=channel_id).all()

async def update_faq(faq_id, question, answer):
    """Update the question and answer for a particular FAQ entry."""
    await FAQ.filter(id=faq_id).update(question=question, answer=answer)

async def delete_faq(faq_id):
    """Delete a particular FAQ entry."""
    await FAQ.filter(id=faq_id).delete()

async def get_faq(faq_id):
    """Retrieve a particular FAQ entry."""
    return await FAQ.get(id=faq_id)

async def like_faq(faq_id):
    """Increment the number of likes for an FAQ entry."""
    # await FAQ.filter(id=faq_id).update(likes=FAQ.likes + 1)
    await FAQ.filter(id=faq_id).update(likes=F('likes') + 1)      

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

# #Reset all FAQs in a channel
# async def reset_faqs(channel_id):
#     """Delete all FAQ entries for a particular channel."""
#     await FAQ.filter(channel_id=channel_id).delete()

#Reset all FAQs
async def reset_all():
    """Delete all FAQ entries."""
    await FAQ.all().delete()

