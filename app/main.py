from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,    
    ConversationHandler,
)
from app.model.user import User, Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os 
from dotenv import load_dotenv



load_dotenv()
#Basic setup and database 
Token = os.getenv('TOKEN')
print(Token)
engine = create_engine("sqlite:///data.db", echo=True)
Base.metadata.create_all(engine)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with Session(engine) as session:
        user = User(update.effective_user.username)
        if session.query(User).filter(User.telegram_handle == user.telegram_handle).count() == 0:
            session.add(user)
            session.commit()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Hi {update.effective_user.first_name} {update.effective_user.last_name} I'm a bot, please talk to me!",
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Hi {update.effective_user.first_name} {update.effective_user.last_name} has registered already",
            )

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

    return 0

async def cancel(update, context):
    user = update.message.from_user
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
        f"I see! So {user.first_name} {user.last_name} is a {input}",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END

async def asking_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks the user about their age."""
    reply_keyboard=[["Cancel"]]

    await update.message.reply_text(
        "Hi! I am Cupid."
        "Send /cancel to stop talking to me.\n\n"
        "What is your age?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Let me know your age.",
        ),
    )

    return 0

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
        await update.message.reply_text(f"Thanks! I have recorded your age as {age}.")
    else: 
        await update.message.reply_text("Please enter a valid number.")
    return ConversationHandler.END

    
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
    return 0

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
        return 0
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
        return ConversationHandler.END 
    
async def match(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    # user object
    with Session(engine) as session:
        stmt = select(User).where(User.telegram_handle == user.username)
        target = session.scalars(stmt).one()
        date_gender = target.gender ^ 1
        stmt = select(User).where(User.gender == date_gender)
        opp_gender_users = session.scalars(stmt).all()

    await update.message.reply_text(
        "I have helped you find out the top 3 fittest dates for you. Their telegram handles are:"
        ""
        "Please feel free to strike a conversation and begin with a hello.",
        reply_markup=ReplyKeyboardRemove()
    )


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    user = update.message.from_user
    await update.message.reply_text(
        "I have erased all the memories about you. See you next time.",
        reply_markup=ReplyKeyboardRemove()
    )



async def help(update, context):
    user = update.message.from_user
    await update.message.reply_text(
        "I am cupid who can help you match with the top fits of possible dates after you tell us your gender, age and finishing the quiz.",
        
    )
    return ConversationHandler.END





def main():
    application = ApplicationBuilder().token(Token).build()
    application.add_handler(CommandHandler("start", start))
    """application.add_handler(CommandHandler("quiz", quiz))"""
    application.add_handler(CommandHandler("match", match))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("deleteaccount", delete))

    gender_handler = ConversationHandler(
        entry_points=[CommandHandler("gender", asking_gender)],
        states={0: [MessageHandler(filters.Regex("^(Boy|Girl|Other)"), gender)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(gender_handler)

    age_handler = ConversationHandler(
        entry_points=[CommandHandler("age", asking_age)],
        states={0: [MessageHandler(filters.Regex(r'^\d+$'), age)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(age_handler)

    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler("quiz", starting_quiz)],
        states={0: [MessageHandler(filters.Regex(r'^[1-5]$'), quiz)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(quiz_handler)

    application.run_polling()

if __name__ == "__main__":
    main()

   










