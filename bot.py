import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")
user_status = {}


# ==============================
# MENU UTAMA
# ==============================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📌 Layanan Kemahasiswaan", callback_data="layanan")],
        [InlineKeyboardButton("📝 Aspirasi & Pengaduan", callback_data="aspirasi")],
        [InlineKeyboardButton("🎓 Informasi Beasiswa", callback_data="beasiswa")],
        [InlineKeyboardButton("📢 Kebijakan Kampus", callback_data="kebijakan")],
        [InlineKeyboardButton("☎️ Kontak Admin", callback_data="kontak")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ==============================
# COMMAND /start
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_status[user_id] = True  # aktifkan user

    await update.message.reply_text(
        "👋 *Selamat datang di ADKESMA Bot*\n\n"
        "Call Center Terpadu ADKESMA.\n"
        "Pelayanan responsif, solutif, dan transparan.\n\n"
        "Silakan pilih layanan di bawah ini:",
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

    # ==============================


# COMMAND /end
# ==============================
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_status[user_id] = False  # nonaktifkan user

    await update.message.reply_text("Bot telah berhenti.")


# ==============================
# BUTTON HANDLER
# ==============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_status.get(user_id, False):
        return  # kalau tidak aktif, abaikan

    query = update.callback_query
    await query.answer()

    if query.data == "layanan":
        await query.message.reply_text(
            "📌 *Layanan Kemahasiswaan*\n\n"
            "Untuk pengajuan surat atau layanan akademik lainnya, "
            "silakan isi formulir berikut:\n\n"
            "🔗 https://link-google-form-kamu.com",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    elif query.data == "aspirasi":
        await query.message.reply_text(
            "📝 *Aspirasi & Pengaduan*\n\n"
            "Sampaikan aspirasi atau pengaduan Anda melalui formulir berikut.\n"
            "Identitas sudah pasti dirahasiakan.\n\n"
            "🔗 https://forms.gle/5TKQfaXQCUWZaF9fA",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    elif query.data == "beasiswa":
        await query.message.reply_text(
            "🎓 *Informasi Beasiswa*\n\n"
            "Informasi beasiswa terbaru dapat dilihat melalui:\n\n"
            "🔗 https://docs.google.com/document/d/1f-rQhkOpVdG82MfyGxskAJUKf-Ft0yPs/edit?usp=sharing&ouid=102753400071035978326&rtpof=true&sd=true",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    elif query.data == "kebijakan":
        await query.message.reply_text(
            "📢 *Kebijakan Kampus*\n\n"
            "Update kebijakan kampus terbaru tersedia melalui channel resmi berikut:\n\n"
            "🔗 https://whatsapp.com/channel/0029VaOmpOX8vd1XgFovkf1c",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    elif query.data == "kontak":
        await query.message.reply_text(
            "☎️ *Kontak Admin ADKESMA*\n\n"
            "Jam Layanan:\n"
            "Senin–Jumat\n"
            "08.00–16.00 WIB\n\n"
            "WA Admin:\n"
            "+62xxxxxxxxxx\n\n"
            "Email:\n"
            "adkesma@kampus.ac.id",
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )


# ==============================
# HANDLE PESAN RANDOM
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not user_status.get(user_id, False):
        return  # kalau bot nonaktif, jangan balas

    await update.message.reply_text(
        "Silakan gunakan menu yang tersedia ya 😊",
        reply_markup=main_menu(),
    )


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("end", end))

    from telegram.ext import MessageHandler, filters

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot berjalan...")
    app.run_polling()
