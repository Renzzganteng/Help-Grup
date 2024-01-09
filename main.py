import telebot
from datetime import datetime, timedelta

# Masukkan token bot Telegram langsung
bot = telebot.TeleBot("TOKEN_BOT")

# Fungsi untuk menghapus pesan yang tidak pantas
def delete_message(message):
    # Cek apakah pesan mengandung kata-kata yang tidak pantas
    keywords = ["anjg", "babi", "taik", "kontol", "pepek", "memek", "suki", "anj", "woi", "Kon", "ppk", "kau", "gblk","Anjeng","tai","asu"]
    for keyword in keywords:
        if keyword in message.text.lower():
            # Hapus pesan
            bot.delete_message(message.chat.id, message.message_id)

            # Mute pengguna selama 5 menit
            bot.restrict_chat_member(
                message.chat.id, message.from_user.id,
                permissions=telebot.types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                ),
                until_date=datetime.now() + timedelta(minutes=5),
            )

            # Dapatkan nama pengguna Telegram pengirim pesan
            username = message.from_user.username

            # Kirim pesan tanggapan dengan menyebutkan nama pengguna
            bot.send_message(
                message.chat.id,
                "Yeah, Renn tidak suka dengan kata-katamu, {}. {{username}} dimute selama 5 menit.".format(username)
            )
            return

# Fungsi untuk menyapa anggota baru dan mendeteksi username
def welcome_new_member(message):
    # Cek apakah anggota baru
    if message.new_chat_members:
        # Ambil username anggota baru
        new_members = [member.username for member in message.new_chat_members if member.username is not None]

        # Jika ada username yang ditemukan
        if new_members:
            # Gabungkan username menjadi satu string dengan pemisah koma
            usernames = ', '.join(new_members)

            # Kirim pesan selamat datang dengan menyebutkan username
            bot.send_message(message.chat.id, "Selamat datang di grup ini, {}".format(usernames))
        else:
            # Jika tidak ada username yang ditemukan, kirim pesan selamat datang tanpa menyebutkan username
            bot.send_message(message.chat.id, "Selamat datang di grup ini!")

# Fungsi untuk membalas pesan "/help"
def help(message):
    # Kirim pesan bantuan
    bot.send_message(message.chat.id, "Bot ini digunakan untuk menjaga grup agar tetap bersih dan sopan.")

# Fungsi untuk melacak IP pengguna
def track_ip(message):
    # Cek apakah pesan adalah perintah "/ip"
    if message.text.startswith("/ip"):
        # Ambil username pengguna dari pesan
        username = message.text[4:]

        # Gunakan API Telegram untuk mendapatkan ID pengguna
        id = bot.get_chat_member(message.chat.id, username).user.id

        # TODO: Gunakan metode lain untuk mendapatkan IP pengguna

        # Kirim pesan berisi IP pengguna
        bot.send_message(message.chat.id, "IP pengguna: {}".format(ip))

# Buat handler untuk pesan masuk
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Cek apakah pesan berasal dari admin
    if message.from_user.id == 6699838375:
        # Lakukan tindakan sesuai perintah admin
        return

    # Cek apakah pesan mengandung kata-kata yang tidak pantas
    delete_message(message)

    # Cek apakah anggota baru dan deteksi username
    welcome_new_member(message)

    # Cek apakah pesan adalah perintah "/help"
    if message.text == "/help":
        help(message)

    # Cek apakah pesan adalah perintah "/ip"
    if message.text.startswith("/ip"):
        track_ip(message)

# Mulai bot
bot.polling()