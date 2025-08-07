from django.shortcuts import render
from django.http import HttpResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

def home(request):
    return render(request, 'home.html')

# Initialize ChatBot with a BestMatch adapter
bot = ChatBot(
    'bot',
    read_only=True,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "I'm sorry, I don't know the answer to that. I haven't trained on it yet.",
            'maximum_similarity_threshold': 0.65
        }
    ]
)

# Read training data from a text file in pairs
custom_training_file_path = os.path.join(os.path.dirname(__file__), 'training_data.txt')

if os.path.exists(custom_training_file_path):
    with open(custom_training_file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    # Group lines into pairs
    trainer = ListTrainer(bot)
    for i in range(0, len(lines) - 1, 2):
        trainer.train([lines[i], lines[i + 1]])

# Strict response handling
def index(request):
    return render(request, 'index.html')

def getResponse(request):
    user_message = request.GET.get('userMessage')
    bot_response = bot.get_response(user_message)

    # Manually check confidence score
    if bot_response.confidence < 0.65:
        return HttpResponse("I'm sorry, I don't know the answer to that. I haven't trained on it yet.")

    return HttpResponse(str(bot_response))
