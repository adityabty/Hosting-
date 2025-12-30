from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, ConversationHandler,
    MessageHandler, filters, ContextTypes
)

from config import BOT_TOKEN, ADMIN_IDS
from database import get_or_create_user
from deploy import deploy_music_bot, deploy_chat_bot


FORM = {}

ASK_TOKEN, ASK_STRING, ASK_LOGGER, ASK_OWNER = range(4)
ASK_CHAT_TOKEN, ASK_CHAT_OWNER = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    get_or_create_user(update.effective_user.id)

    kb = [
        [InlineKeyboardButton("🎵 Host Music Bot", callback_data="music")],
        [InlineKeyboardButton("💬 Host Chat Bot", callback_data="chat")],
        [InlineKeyboardButton("💰 My Credits", callback_data="credits")]
    ]

    await update.message.reply_text(
        "Welcome! Choose an option:",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def menu_buttons(update: Update, context):
    q = update.callback_query
    await q.answer()

    uid = update.from_user.id

    if q.data == "music":
        FORM[uid] = {}
        await q.message.reply_text("Send Music Bot Token:")
        return ASK_TOKEN

    if q.data == "chat":
        FORM[uid] = {}
        await q.message.reply_text("Send Chat Bot Token:")
        return ASK_CHAT_TOKEN

    if q.data == "credits":
        user = get_or_create_user(uid)
        await q.message.reply_text(f"Your credits: {user[2]}")
        return ConversationHandler.END


# MUSIC BOT FORM FLOW

async def music_token(update, context):
    uid = update.effective_user.id
    FORM[uid]["token"] = update.message.text
    await update.message.reply_text("Send String Session:")
    return ASK_STRING


async def music_string(update, context):
    uid = update.effective_user.id
    FORM[uid]["string"] = update.message.text
    await update.message.reply_text("Send Logger ID:")
    return ASK_LOGGER


async def music_logger(update, context):
    uid = update.effective_user.id
    FORM[uid]["logger"] = update.message.text
    await update.message.reply_text("Send Owner ID:")
    return ASK_OWNER


async def music_owner(update, context):
    uid = update.effective_user.id
    FORM[uid]["owner"] = update.message.text

    user = get_or_create_user(uid)

    process = deploy_music_bot(user[0], uid, FORM[uid])

    await update.message.reply_text(
        f"🎉 Music Bot Deployed!\nProcess: `{process}`",
        parse_mode="Markdown"
    )

    return ConversationHandler.END


# CHAT BOT FORM FLOW

async def chat_token(update, context):
    uid = update.effective_user.id
    FORM[uid]["token"] = update.message.text
    await update.message.reply_text("Send Owner ID:")
    return ASK_CHAT_OWNER


async def chat_owner(update, context):
    uid = update.effective_user.id
    FORM[uid]["owner"] = update.message.text

    user = get_or_create_user(uid)

    process = deploy_chat_bot(user[0], uid, FORM[uid])

    await update.message.reply_text(
        f"🎉 Chat Bot Deployed!\nProcess: `{process}`",
        parse_mode="Markdown"
    )

    return ConversationHandler.END



app = ApplicationBuilder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(menu_buttons)],
    states={

        # music bot flow
        ASK_TOKEN: [MessageHandler(filters.TEXT, music_token)],
        ASK_STRING: [MessageHandler(filters.TEXT, music_string)],
        ASK_LOGGER: [MessageHandler(filters.TEXT, music_logger)],
        ASK_OWNER: [MessageHandler(filters.TEXT, music_owner)],

        # chat bot flow
        ASK_CHAT_TOKEN: [MessageHandler(filters.TEXT, chat_token)],
        ASK_CHAT_OWNER: [MessageHandler(filters.TEXT, chat_owner)],
    },
    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)

app.run_polling()
