from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,    
    ConversationHandler,
)
from app.algorithm.Pair import Pair
from app.algorithm.utils import convert_distances, perform_pca, quick_select
from app.model.user import User, Base
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv

from app.utils.utils import format_handle_list

ASKING_GENDER, GENDER, ASKING_AGE, AGE, STARTING_QUIZ, QUIZ, MATCH = range(7)


load_dotenv()
#Basic setup and database 
Token = os.getenv('TOKEN')
print(Token)
engine = create_engine("sqlite:///data.db", echo=True)
Base.metadata.create_all(engine)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    with Session(engine) as session:
        user = User(update.effective_user.username)
        if session.query(User).filter(User.telegram_handle == user.telegram_handle).count() == 0:
            session.add(user)
            session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Hi {update.effective_user.first_name} {update.effective_user.last_name} I'm Cupid carrying arrows of love. I will help you find the best matches. To begin, use /gender to choose your gender.",
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Hi {update.effective_user.first_name} {update.effective_user.last_name} has been memorisied by me already. Just wait for others to text you or you can be forgotten by me using /deleteme!",
            )
    return ASKING_GENDER

# conversational bot
async def asking_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! I am Cupid."
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )

    return GENDER

async def cancel(update, context):
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    input = update.message.text
    if input == "Girl":
        input_gender = 0
    elif input == "Boy":
        input_gender = 1
    else:
        input_gender = -1
    
    with Session(engine) as session:
        stmt = select(User).where(User.telegram_handle == user.username)
        target = session.scalars(stmt).one()
        target.set_gender(input_gender)
        session.commit()
        
    await update.message.reply_text(
        f"I see! So {user.first_name} {user.last_name} is a {input}. Now you can tell me your age using /age. ",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ASKING_AGE

async def asking_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user about their age."""
    await update.message.reply_text(
        "Hi! Cupid again."
        "Send /cancel to stop talking to me.\n\n"
        "What is your age?",
        reply_markup=ReplyKeyboardRemove()
    )

    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    user = update.message.from_user
    if user_input.isdigit():
        age = int(user_input)
        with Session(engine) as session:
            stmt = select(User).where(User.telegram_handle == user.username)
            target = session.scalars(stmt).one()
            target.set_age(age)
            session.commit()
        await update.message.reply_text(f"Thanks! I have recorded your age as {age}. Next you can take the quiz using /quiz. If you want to roll back your answer, using /age again.")
        return STARTING_QUIZ
    else: 
        await update.message.reply_text("Please enter a valid number.")
        return AGE

    
async def starting_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["1", "2", "3", "4", "5"]]
    context.user_data["answers"] = []
    context.user_data["curr_question"] = 0
    context.user_data["questions"] = [
        "How important is physical attraction to you in a relationship?",
        "I prefer a partner who shares my hobbies and interests and similar values and beliefs(e.g. religious)",
        "How much do you value deep, meaningful conversations with your partner?",
        "How important is it for your partner to share your long-term goals?",
        "I enjoy being physically active and doing outdoor activities.",
        "I feel comfortable discussing my emotions and feelings with a partner.",
        "I prefer having a structured and organized lifestyle.",
        "How often do you prioritize alone time for yourself?"
    ]

    await update.message.reply_text(
        "Now you can answer a series of questions to let me help you find the best matches \n\n"
        "1 = Least Extent, 5 = Most Extent\n\n"
        f"Question 1: {context.user_data["questions"][0]} \n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Choose a number between 1 and 5."
        )
    )
    return QUIZ

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    user = update.message.from_user
    reply_keyboard = [["1", "2", "3", "4", "5"]]
    curr_ans = int(update.message.text)
    context.user_data["answers"].append(curr_ans)
    context.user_data["curr_question"] +=1
    curr_question = context.user_data["curr_question"]
    
    if context.user_data["curr_question"] < len(context.user_data["questions"]):
        curr_question_task = context.user_data["questions"][curr_question]
        await update.message.reply_text(
            f"Question {curr_question + 1}: {curr_question_task} \n\n",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="Choose a number between 1 and 5."
            )
        )
        return QUIZ
    else:
        answers = context.user_data["answers"]
        with Session(engine) as session:
            stmt = select(User).where(User.telegram_handle == user.username)
            target = session.scalars(stmt).one() # execute the stmt n return the user
            target.set_score(answers)
            session.commit()
        await update.message.reply_text(
            "Thank you for completing the quiz. Cupid will help you match if you input /match",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.clear()
        return MATCH
    
async def match(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    # user object
    with Session(engine) as session:
        stmt = select(User).where(User.telegram_handle == user.username)
        target = session.scalars(stmt).one()
        session.commit()
        
        date_gender = target.gender ^ 1
        stmt = select(User).where(User.gender == date_gender)
        opp_gender_users_tmp = session.scalars(stmt).all()
        session.commit()
    
        # Extract vector of score including age
        target_xs = [Pair(target.id, target.vectorize_scores())]
    
        for u in opp_gender_users_tmp:
            p = Pair(u.id, u.vectorize_scores())
            target_xs.append(p)
        
        reduced_target_xs = perform_pca(target_xs)
        distance_xs = convert_distances(reduced_target_xs)
        top_3 = quick_select(distance_xs, 3)
        final_list = []
        for each in top_3:
            with Session(engine) as session:
                stmt = select(User).where(User.id == each[0])
                curr_user = session.scalars(stmt).one()
                session.commit()
                final_list.append(curr_user.telegram_handle)
    await update.message.reply_text(
        "I have helped you find out the top 3 fittest dates for you. Their telegram handles are:\n"
        f"{format_handle_list(final_list)}\n"
        "Please feel free to strike a conversation and begin with a hello.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    user = update.message.from_user
    with Session(engine) as session:
        stmt = select(User).where(User.telegram_handle == user.username)
        target = session.scalars(stmt).one_or_none()
    
        if target:
            session.delete(target)
            session.commit()
            await update.message.reply_text(
                "I have erased all the memories about you. See you next time. If you want to start again, using /start.",
                reply_markup=ReplyKeyboardRemove()
            ) 
        else:
            await update.message.reply_text(
                "I have never chatted with you before. No memories about you can be erased from me. You can start the conversation with me using /start.",
                reply_markup=ReplyKeyboardRemove()
            )
    return ConversationHandler.END
            
    



async def help(update, context):
    user = update.message.from_user
    await update.message.reply_text(
        "I am Cupid who can help you match with the top fits of possible dates after you tell us your gender, age and finishing 8 quizes.",
        
    )
    return ConversationHandler.END





def main():
    application = ApplicationBuilder().token(Token).build()
    application.add_handler(CommandHandler("help", help))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASKING_GENDER: [CommandHandler("gender", asking_gender)],
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)"), gender)],
            ASKING_AGE: [CommandHandler("age", asking_age)],
            AGE: [MessageHandler(filters.TEXT, age)],
            STARTING_QUIZ: [CommandHandler("quiz", starting_quiz), CommandHandler("age", asking_age)],
            QUIZ: [MessageHandler(filters.Regex(r'^[1-5]$'), quiz)],
            MATCH: [CommandHandler("match", match)]
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("deleteme", delete)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("deleteme", delete))

    application.run_polling()

if __name__ == "__main__":
    main()

   










