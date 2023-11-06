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
    update.message.reply_text("Welcome! Type /askquestion to start the quiz.")

# Command to start the multiple-choice question
def start_question(update, context: CallbackContext):
    user_id = update.effective_user.id
    user_responses[user_id] = {'current_question_index': -1, 'questions': []}

    # Generate a new question
    question_text, answer_options = get_random_question()
    user_responses[user_id]['questions'].append((question_text, answer_options))
    user_responses[user_id]['current_question_index'] += 1

    question = question_text
    options = [answer[0] for answer in answer_options]
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(question, reply_markup=reply_markup)

def receive_choice(update, context: CallbackContext):
    user_id = update.callback_query.from_user.id
    choice = update.callback_query.data

    if user_id not in user_responses:
        # Handle the case where the user hasn't started the quiz or the quiz is over.
        update.callback_query.answer("No active quiz.")
        return

    user_responses[user_id]['choice'] = choice

    # Get the IsCorrect value of the selected answer from the answer_options list
    is_correct = next(answer[1] for answer in user_responses[user_id]['questions'][user_responses[user_id]['current_question_index']][1] if answer[0] == choice)

    if is_correct:
        update.callback_query.answer("Correct answer!", show_alert=True)
    else:
        correct_answer = next(answer[0] for answer in user_responses[user_id]['questions'][user_responses[user_id]['current_question_index']][1] if answer[1] == 1)
        update.callback_query.answer("Incorrect answer. The correct answer is: " + correct_answer, show_alert=True)

    # Generate and show a new question
    question_text, answer_options = get_random_question()
    user_responses[user_id]['questions'].append((question_text, answer_options))
    user_responses[user_id]['current_question_index'] += 1

    if user_responses[user_id]['current_question_index'] < len(user_responses[user_id]['questions']):
        question = question_text
        options = [answer[0] for answer in answer_options]
        keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.callback_query.message.reply_text(question, reply_markup=reply_markup)
        update.callback_query.message.reply_text(answer_message)
    else:
        # No more questions, finish the quiz
        update.callback_query.message.reply_text("Quiz is over! Thank you for participating.")
        del user_responses[user_id]


# Create a command handler for starting the multiple-choice question
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('askquestion', start_question))
# Create a callback query handler for processing the user's choice
dispatcher.add_handler(CallbackQueryHandler(receive_choice))

# Add a message handler to handle text input
def text_input(update, context):
    update.message.reply_text("Please type /askquestion to start the quiz.")

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_input))

# Start the bot
updater.start_polling()

# Keep the bot running
updater.idle()