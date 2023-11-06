import telegram
from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import random, logging, sqlite3, random
from telegram.ext import CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the token you received from the BotFather
updater = Updater(token=config('TOKEN_BOT'), use_context=True)
dispatcher = updater.dispatcher

# Configure the logging module
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for your bot
logger = logging.getLogger(__name__)

# Dictionary to store user responses
user_responses = {}

# Add a variable to specify the number of questions in the challenge
NUM_QUESTIONS = 3

# Add variables to keep track of correct and incorrect answers
correct_answers_count = {}
incorrect_answers_count = {}

def get_random_question():
    # Connect to your SQLite database
    conn = sqlite3.connect('sql/QuestionsAnswersDB')
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

    # Log when a new user starts a challenge
    logger.info(f"New user (ID: {user_id}) started a challenge.")

    # Clear the user's previous responses before starting a new challenge
    user_responses[user_id] = {}
    user_responses[user_id]['current_question_index'] = 0
    user_responses[user_id]['questions'] = []

    # Reset the counts for correct and incorrect answers
    correct_answers_count[user_id] = 0
    incorrect_answers_count[user_id] = 0

    # Add questions to the challenge until the desired number is reached
    for _ in range(NUM_QUESTIONS):
        question_text, answer_options = get_random_question()
        random.shuffle(answer_options)  # Shuffle the answer options randomly
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
        display_results(update, user_id)
def display_results(update, user_id):
    # Calculate the percentage of correct answers
    total_questions = NUM_QUESTIONS
    correct_count = correct_answers_count.get(user_id, 0)
    incorrect_count = incorrect_answers_count.get(user_id, 0)

    if total_questions > 0:
        percentage_correct = (correct_count / total_questions) * 100
        percentage_incorrect = (incorrect_count / total_questions) * 100
    else:
        percentage_correct = 0
        percentage_incorrect = 0

    # Define emojis
    correct_emoji = "✅"
    incorrect_emoji = "❌"

    # Display the results with emojis
    results_message = "Challenge is over!\n\n"
    results_message += f"Total questions: {total_questions}\n"
    results_message += f"Correct answers: {correct_emoji} {correct_count} ({percentage_correct:.2f}%)\n"
    results_message += f"Incorrect answers: {incorrect_emoji} {incorrect_count} ({percentage_incorrect:.2f}%)"

    updater.bot.send_message(user_id, text=results_message)
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
        correct_answers = []

        # Check if the choice is correct
        for answer in user_responses[user_id]['questions'][current_question_index][1]:
            if answer[0] == choice and answer[1] == 1:
                is_correct = True
            if answer[1] == 1:
                correct_answers.append(answer[0])

        if is_correct:
            update.callback_query.answer("Correct answer!", show_alert=True)
            # Increment the correct answers count for the user
            correct_answers_count[user_id] = correct_answers_count.get(user_id, 0) + 1
        else:
            # Display the correct answer(s) in the alert message
            correct_answer_str = "Correct answer(s): " + ", ".join(correct_answers)
            update.callback_query.answer(f"Incorrect answer. {correct_answer_str}. Try the next question.", show_alert=True)
            # Increment the incorrect answers count for the user
            incorrect_answers_count[user_id] = incorrect_answers_count.get(user_id, 0) + 1

        # Move to the next question or finish the challenge
        user_responses[user_id]['current_question_index'] += 1
        display_question(update, user_id)

# ...

def display_results(update, user_id):
    # Calculate the percentage of correct answers
    total_questions = NUM_QUESTIONS
    correct_count = correct_answers_count.get(user_id, 0)
    incorrect_count = incorrect_answers_count.get(user_id, 0)

    if total_questions > 0:
        percentage_correct = (correct_count / total_questions) * 100
        percentage_incorrect = (incorrect_count / total_questions) * 100
    else:
        percentage_correct = 0
        percentage_incorrect = 0

    # Define emojis
    correct_emoji = "✅"
    incorrect_emoji = "❌"

    # Display the results with emojis
    results_message = "Challenge is over!\n\n"
    results_message += f"Total questions: {total_questions}\n"
    results_message += f"Correct answers: {correct_emoji} {correct_count} ({percentage_correct:.2f}%)\n"
    results_message += f"Incorrect answers: {incorrect_emoji} {incorrect_count} ({percentage_incorrect:.2f}%)"


    updater.bot.send_message(user_id, text=results_message)
    # Log when a user finishes a challenge
    logger.info(f"User (ID: {user_id}) finished a challenge with {correct_count} correct answers and {incorrect_count} incorrect answers.")

    del user_responses[user_id]

# ...

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
