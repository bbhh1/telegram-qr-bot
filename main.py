import qrcode
import os
from dotenv import load_dotenv
from telegram import Update, ChatMember
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# تحميل التوكن واسم القناة من ملف .env
load_dotenv()
TOKEN = os.getenv("6934967536:AAHeSGRKANKoc417TvGZn5ZDHAyKwP-JjvU")
CHANNEL_USERNAME = os.getenv("@VV333K")  # مثال: "@mychannel"

# التحقق من الاشتراك
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]
    except:
        return False

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text("👋 أهلاً! أرسل أي رابط أو نص وسأرجعه لك كـ QR 🔲")
    else:
        await update.message.reply_text(
            f"🔒 لاستخدام هذا البوت، يرجى الاشتراك أولاً في القناة:\n{CHANNEL_USERNAME}\nثم أرسل /start من جديد."
        )

# توليد QR
async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        await update.message.reply_text(
            f"🚫 لا يمكنك استخدام البوت حتى تشترك في القناة: {CHANNEL_USERNAME}"
        )
        return

    text = update.message.text
    img = qrcode.make(text)
    img.save("qr.png")
    await update.message.reply_photo(photo=open("qr.png", "rb"))

# إعداد البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))
app.run_polling()
