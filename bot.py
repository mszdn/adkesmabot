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

TOKEN = os.getenv("TOKEN")

user_status = {}
visited_users = set()
user_state = {}


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


def back_menu():
    keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)


# typing effect
async def typing_effect(msg):
    await msg.chat.send_action(action=ChatAction.TYPING)
    await asyncio.sleep(1)


# end
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_status[user_id] = False

    # await typing_effect(update.message)
    await update.message.reply_text(
        "terimakasih sudah menggunakan layanan ACA, sampai jumpa lagi!"
    )


# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id
    name = user.first_name if user.first_name else "Sahabat MATES"

    user_status[user_id] = True
    user_state[user_id] = "ASK_MENU"

    if user_id not in visited_users:
        visited_users.add(user_id)

        greeting = (
            f"Halo {name}! 👋\n\n"
            "Saya Aca dari Teman Berarti. Saya siap membantu memberikan informasi serta menampung aspirasi, keluhan, dan saran dari teman-teman terkait kehidupan kampus.\n\n"
            "Jangan ragu untuk bercerita ya, karena setiap suara mahasiswa berarti untuk didengar dan diperjuangkan.\n\n"
            "Eh sebelumnya, kamu sudah tau belum menu yang tersedia? 😊"
        )

    else:
        greeting = (
            f"Halo lagi {name}! 👋\n\n"
            "Aca siap membantu kamu kembali 😊\n\n"
            "Eh sebelumnya, kamu masih ingat menu yang tersedia? 😊"
        )

    # await typing_effect(update.message)

    await update.message.reply_text(
        greeting,
    )


# menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not user_status.get(user_id, False):
        # await typing_effect(update.message)
        await update.message.reply_text(
            "Sesi kamu sudah berakhir.\nKetik /start untuk memulai kembali."
        )
        return
    # await typing_effect(update.message)
    await update.message.reply_text(
        "Silakan pilih layanan berikut 😊",
        reply_markup=main_menu(),
    )


# RESPON MENU
async def layanan(update: Update, msg):
    # await typing_effect(msg)

    await msg.reply_text(
        "📌 *Layanan Kemahasiswaan*\n\n"
        "Sahabat MATES dapat mengajukan layanan administrasi melalui tempalate berikut.\n\n"
        "Silakan gunakan template di bawah ini 👇\n\n"
        "🔗 https://bit.ly/4c98Jv1",
        parse_mode="Markdown",
        reply_markup=back_menu(),
    )


async def aspirasi(update: Update, msg):
    # await typing_effect(msg)
    await msg.reply_text(
        "📝 *Aspirasi & Pengaduan*\n\n"
        "Sahabat MATES dapat menyampaikan aspirasi atau pengaduan.\n\n"
        "Identitas kamu dijamin rahasia.\n\n"
        "Silakan isi formulir berikut 👇\n\n"
        "🔗 https://forms.gle/Z1CDTEbkDLfY5u4YA",
        parse_mode="Markdown",
        reply_markup=back_menu(),
    )


async def beasiswa(update: Update, msg):
    # await typing_effect(msg)
    await msg.reply_text(
        "🎓 *Informasi Beasiswa*\n\n"
        "Informasi beasiswa terbaru dapat dilihat melalui link berikut 👇\n\n"
        "🔗 https://bit.ly/4siCDSN\n\n"
        "Jangan lupa cek secara berkala ya 😊",
        parse_mode="Markdown",
        reply_markup=back_menu(),
    )


async def kebijakan(update: Update, msg):
    # await typing_effect(msg)
    await msg.reply_text(
        "📢 *Kebijakan Kampus*\n\n"
        "Update kebijakan kampus terbaru tersedia di link berikut 👇\n\n"
        "🔗 https://bit.ly/4r5XBU0",
        parse_mode="Markdown",
        reply_markup=back_menu(),
    )


async def kontak(update: Update, msg):
    # await typing_effect(msg)
    await msg.reply_text(
        "☎️ *Kontak Admin ADKESMA*\n\n"
        "Jika membutuhkan bantuan lebih lanjut:\n\n"
        "📱 WA: +6281221748221 (zaky rinov)\n"
        "📧 Email: adkesmate.unnes@gmail.com\n\n"
        "🕒 Jam layanan:\n"
        "Senin – Jumat\n"
        "08.00 – 16.00 WIB",
        parse_mode="Markdown",
        reply_markup=back_menu(),
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

    elif data == "menu":
        await query.message.reply_text(
            "Silakan pilih layanan berikut 😊",
            reply_markup=main_menu(),
        )


# text handle
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # cek apakah user masih aktif
    if not user_status.get(user_id, False):
        # await typing_effect(update.message)
        await update.message.reply_text(
            "Sesi kamu sudah berakhir.\nKetik /start untuk memulai kembali."
        )
        return

    text = update.message.text.lower()
    state = user_state.get(user_id)

    if state == "ASK_MENU":
        if any(
            kata in text for kata in ["belum", "tidak", "engga", "gak", "ngga", "ga"]
        ):
            user_state[user_id] = "MAIN_MENU"
            await update.message.reply_text(
                "Tenang Mates! 😊\n\nIni dia menu yang bisa kamu pilih 👇",
                reply_markup=main_menu(),
            )
            return
        elif any(kata in text for kata in ["masih", "iyaa", "iya", "ingat", "inget"]):
            user_state[user_id] = "MAIN_MENU"
            await update.message.reply_text(
                "Mantap! 😎\n\nLangsung pilih menu yang kamu butuhkan ya 👇",
                reply_markup=main_menu(),
            )
            return
        else:
            await update.message.reply_text(
                "Hehe, jawab dulu ya Mates 🙌\nSudah tau menunya atau belum? 😊"
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
    elif text in ["halo", "hai", "ACA", "hi", "hello", "alo", "allo"]:
        await update.message.reply_text(
            "Halo juga Sahabat ADKES! 👋\n\n"
            "ACA siap membantu kamu.\n"
            "Silakan pilih layanan di bawah ya 😊",
            reply_markup=main_menu(),
        )
    elif text in ["terimakasih", "thanks", "thank you", "makasih"]:
        await update.message.reply_text(
            "Sama-sama Sahabat ADKES! 😉\n\n"
            "Jika ada yang bisa ACA bantu lagi, jangan ragu untuk bertanya ya!",
        )
    else:
        # await typing_effect(update.message)
        await update.message.reply_text(
            "Maaf ACA belum memahami pesan kamu.\n\n"
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
