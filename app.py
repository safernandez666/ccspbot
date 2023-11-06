import telegram
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import sqlite3
import random
from telegram.ext import CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the token you received from the BotFather
updater = Updater(token=os.environ['TOKEN_BOT'], use_context=True)
dispatcher = updater.dispatcher

# Dictionary to store user responses
user_responses = {}

# Add a variable to specify the number of questions in the challenge
NUM_QUESTIONS = 3

def get_random_question():
    # Connect to your SQLite database
    conn = sqlite3.connect('QuestionsAnswersDB')
    cursor = conn.cursor()

    # Count the total number of questions in the Questions table
    cursor.execute("SELECT COUNT(*) FROM Questions")
    total_questions = cursor.fetchone()[0]

    # Generate a random question ID
    random_question_id = random.randint(1, total_questions)
    
    # Select the random question's QuestionText
    cursor.execute("SELECT QuestionText FROM Questions WHERE QuestionID = ?;", (random_question_id,))
    question_text = cursor.fetchone()[0]

    # Select the answer options for the random question
    cursor.execute("SELECT AnswerText, IsCorrect FROM Answers WHERE QuestionID = ?;", (random_question_id,))
    answer_options = cursor.fetchall()
    
    # Close the database connection
    conn.close()

    return question_text, answer_options

def start(update, context):
    update.message.reply_text("Welcome! Type /askchallenge to start the challenge.")

# Command to start the challenge
def start_challenge(update, context: CallbackContext):
    user_id = update.effective_user.id
    user_responses[user_id] = {'current_question_index': 0, 'questions': []}

    # Add questions to the challenge until the desired number is reached
    for _ in range(NUM_QUESTIONS):
        question_text, answer_options = get_random_question()
        user_responses[user_id]['questions'].append((question_text, answer_options))

    # Display the first question
    display_question(update, user_id)

def display_question(update, user_id):
    current_question_index = user_responses[user_id]['current_question_index']

    if current_question_index < NUM_QUESTIONS:
        question_text = user_responses[user_id]['questions'][current_question_index][0]
        answer_options = user_responses[user_id]['questions'][current_question_index][1]

        options = [answer[0] for answer in answer_options]
        keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Use the user_id to send the message
        updater.bot.send_message(user_id, text=question_text, reply_markup=reply_markup)
    else:
        # All questions have been answered
        updater.bot.send_message(user_id, text="Challenge is over! Thank you for participating.")
        del user_responses[user_id]

# Update the receive_choice function
def receive_choice(update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    choice = update.callback_query.data

    if user_id not in user_responses:
        # Handle the case where the user hasn't started the challenge or the challenge is over.
        update.callback_query.answer("No active challenge.")
        return

    current_question_index = user_responses[user_id]['current_question_index']

    if current_question_index < NUM_QUESTIONS:
        is_correct = False

        # Check if the choice is correct
        for answer in user_responses[user_id]['questions'][current_question_index][1]:
            if answer[0] == choice and answer[1] == 1:
                is_correct = True
                break

        if is_correct:
            update.callback_query.answer("Correct answer!", show_alert=True)
        else:
            update.callback_query.answer("Incorrect answer. Try the next question.", show_alert=True)

        # Move to the next question or finish the challenge
        user_responses[user_id]['current_question_index'] += 1
        display_question(update, user_id)
    else:
        # All questions have been answered
        update.callback_query.answer("Challenge is over!", show_alert=True)

# Create a command handler for starting the challenge
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('askchallenge', start_challenge))
# Create a callback query handler for processing the user's choice
dispatcher.add_handler(CallbackQueryHandler(receive_choice))

# Add a message handler to handle text input
def text_input(update, context):
    update.message.reply_text("Please type /askchallenge to start the challenge.")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_input))

# Start the bot
updater.start_polling()

# Keep the bot running
updater.idle()
