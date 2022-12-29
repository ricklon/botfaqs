
#BOT FAQs

Q&A for your Discord Server

Users choose do like the command structure below? I can implement if there's demand. Right now it's just the function names as the commands.

## Style 1

!faq add: This command allows users to add a new FAQ to the list. It may require additional arguments, such as the question and answer text, as well as the category to which the FAQ belongs.

!faq remove: This command allows users to remove an FAQ from the list. It may require the user to specify the question or answer text of the FAQ they want to remove.

!faq list: This command displays a list of all FAQs in the system, organized by category. Users may be able to filter the list by category or search for specific FAQs using keywords.

!faq search: This command allows users to search the FAQ list for a specific question or answer. It may require the user to specify a search query as an argument.

!faq categories: This command displays a list of all categories in the FAQ system. Users may be able to filter the list by category name or browse FAQs within a specific category.

!faq help: This command displays a list of all available commands and provides a brief description of each one. It can be used to help users understand how to use the Discord bot.

You may also want to consider adding additional commands, such as !faq update to allow users to edit existing FAQs or !faq random to display a random FAQ from the list.


###
bulk add csv
```csv
question1,answer1
question2,answer2
```

bulk add json
```json
[
    { "question": "What is Discord?", "answer": "Discord is a communication platform for gamers and communities." },
    { "question": "How do I use Discord?", "answer": "To use Discord, you need to create an account and join a server. You can then communicate with other members using voice, text, or video." }
]
```

## Internals

Tortoise ORM

Documentation:
https://tortoise.github.io/

