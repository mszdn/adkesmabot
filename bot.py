import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ChatAction
import asyncio

TOKEN = "8014177596:AAE0hUz7TGnNF2kWp01lEnRMj_T0m-Eajzs"

user_status = {}
visited_users = set()


# menu button
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📌 Layanan Kemahasiswaan", callback_data="layanan")],
        [InlineKeyboardButton("📝 Aspirasi & Pengaduan", callback_data="aspirasi")],
        [InlineKeyboardButton("🎓 Informasi Beasiswa", callback_data="beasiswa")],
        [InlineKeyboardButton("📢 Kebijakan Kampus", callback_data="kebijakan")],
        [InlineKeyboardButton("☎️ Kontak Admin", callback_data="kontak")],
    ]
    return InlineKeyboardMarkup(keyboard)


# typing effect
async def typing_effect(msg):
    await msg.chat.send_action(action=ChatAction.TYPING)
    await asyncio.sleep(1)


# end
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_status[user_id] = False
    
    await typing_effect(update.message)
    await update.message.reply_text(
        "terimakasih sudah menggunakan layanan MinMate, sampai jumpa lagi!"
    )


# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id
    name = user.first_name if user.first_name else "Sahabat ADKES"

    user_status[user_id] = True

    if user_id not in visited_users:
        visited_users.add(user_id)

        greeting = (
            f"Halo {name}! 👋\n\n"
            "Selamat datang di layanan resmi ADKESMA.\n\n"
            "Aku *MinMate*, asisten virtual ADKESMA yang siap membantu kamu 😊\n\n"
            "Kamu bisa:\n"
            "1️⃣ Layanan Kemahasiswaan\n"
            "2️⃣ Aspirasi & Pengaduan\n"
            "3️⃣ Informasi Beasiswa\n"
            "4️⃣ Kebijakan Kampus\n"
            "5️⃣ Kontak Admin\n\n"
            "Silakan pilih menu atau ketik kebutuhanmu ya."
        )

    else:
        greeting = (
            f"Halo lagi {name}! 👋\n\n"
            "MinMate siap membantu kamu kembali 😊\n\n"
            "Kamu bisa:\n"
            "1️⃣ Layanan Kemahasiswaan\n"
            "2️⃣ Aspirasi & Pengaduan\n"
            "3️⃣ Informasi Beasiswa\n"
            "4️⃣ Kebijakan Kampus\n"
            "5️⃣ Kontak Admin\n\n"
            "Silakan pilih menu atau ketik kebutuhanmu ya."
        )

    await typing_effect(update.message)

    await update.message.reply_text(
        greeting,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


# menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not user_status.get(user_id, False):
        await typing_effect(update.message)
        await update.message.reply_text(
            "Sesi kamu sudah berakhir.\nKetik /start untuk memulai kembali."
        )
        return
    await typing_effect(update.message)
    await update.message.reply_text(
        "Silakan pilih layanan berikut 😊",
        reply_markup=main_menu(),
    )


# RESPON MENU
async def layanan(update: Update, msg):
    await typing_effect(msg)

    await msg.reply_text(
        "📌 *Layanan Kemahasiswaan*\n\n"
        "Sahabat ADKES dapat mengajukan layanan administrasi melalui formulir berikut.\n\n"
        "Silakan isi formulir di bawah ini 👇\n\n"
        "🔗 link layanan",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def aspirasi(update: Update, msg):
    await typing_effect(msg)
    await msg.reply_text(
        "📝 *Aspirasi & Pengaduan*\n\n"
        "Sahabat ADKES dapat menyampaikan aspirasi atau pengaduan.\n\n"
        "Identitas kamu dijamin rahasia.\n\n"
        "Silakan isi formulir berikut 👇\n\n"
        "🔗 https://forms.gle/5TKQfaXQCUWZaF9fA",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def beasiswa(update: Update, msg):
    await typing_effect(msg)
    await msg.reply_text(
        "🎓 *Informasi Beasiswa*\n\n"
        "Informasi beasiswa terbaru dapat dilihat melalui link berikut 👇\n\n"
        "🔗 https://bit.ly/4siCDSN\n\n"
        "Jangan lupa cek secara berkala ya 😊",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def kebijakan(update: Update, msg):
    await typing_effect(msg)
    await msg.reply_text(
        "📢 *Kebijakan Kampus*\n\n"
        "Update kebijakan kampus terbaru tersedia di link berikut 👇\n\n"
        "🔗 https://bit.ly/4r5XBU0",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def kontak(update: Update, msg):
    await typing_effect(msg)
    await msg.reply_text(
        "☎️ *Kontak Admin ADKESMA*\n\n"
        "Jika membutuhkan bantuan lebih lanjut:\n\n"
        "📱 WA: +6281221748221\n"
        "📧 Email: adkesmate.unnes@gmail.com\n\n"
        "🕒 Jam layanan:\n"
        "Senin – Jumat\n"
        "08.00 – 16.00 WIB",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


# button handle
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_status.get(user_id, False):
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            "Sesi kamu sudah berakhir.\nKetik /start untuk memulai kembali."
        )
        return

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "layanan":
        await layanan(update, query.message)

    elif data == "aspirasi":
        await aspirasi(update, query.message)

    elif data == "beasiswa":
        await beasiswa(update, query.message)

    elif data == "kebijakan":
        await kebijakan(update, query.message)

    elif data == "kontak":
        await kontak(update, query.message)


# text handle
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # cek apakah user masih aktif
    if not user_status.get(user_id, False):
        await typing_effect(update.message)
        await update.message.reply_text(
            "Sesi kamu sudah berakhir.\nKetik /start untuk memulai kembali."
        )
        return

    text = update.message.text.lower()
    if "layanan" in text or "kemahasiswaan" in text or text == "1":
        await layanan(update, update.message)
    elif "aspirasi" in text or "pengaduan" in text or "lapor" in text or text == "2":
        await aspirasi(update, update.message)
    elif "beasiswa" in text or "info beasiswa" in text or text == "3":
        await beasiswa(update, update.message)
    elif "kebijakan" in text or "aturan" in text or text == "4":
        await kebijakan(update, update.message)
    elif "admin" in text or "kontak" in text or "cs" in text or text == "5":
        await kontak(update, update.message)
    elif "menu" in text:
        await update.message.reply_text(
            "Silakan pilih layanan berikut 😊",
            reply_markup=main_menu(),
        )
    elif text in ["halo", "hai", "minmate"]:
        await update.message.reply_text(
            "Halo juga Sahabat ADKES! 👋\n\n"
            "MinMate siap membantu kamu.\n"
            "Silakan pilih layanan di bawah ya 😊",
            reply_markup=main_menu(),
        )
    else:
        await typing_effect(update.message)
        await update.message.reply_text(
            "Maaf MinMate belum memahami pesan kamu.\n\n"
            "Silakan pilih menu atau ketik kebutuhanmu ya 😊",
            reply_markup=main_menu(),
        )


if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("end", end))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot berjalan...")
    app.run_polling()
