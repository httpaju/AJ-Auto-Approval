from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

pr0fess0r_99 = Client(
    "Auto Approved Bot",
    bot_token=environ["BOT_TOKEN"],
    api_id=int(environ["API_ID"]),
    api_hash=environ["API_HASH"]
)

CHAT_ID = [int(chat_id) for chat_id in environ.get("CHAT_ID", "").split()]
TEXT = environ.get("APPROVED_WELCOME_TEXT", "✨ Hello {mention} 👋\n🎉 Welcome to {title} 💬\n\n✅ You’ve been auto-approved! 🔓")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client: Client, message: Message):
    approvedbot = await client.get_me()
    button = [
        [
            InlineKeyboardButton("📦 Repo", url="https://github.com/httpaju/AJ-Auto-Approval"),
            InlineKeyboardButton("Updates 📢", url="https://t.me/AHMEN_BOTZZ")
        ],
        [
            InlineKeyboardButton("➕️ Add Me To Your Chat ➕️", url=f"https://t.me/{approvedbot.username}?startgroup=true")
        ]
    ]
    await message.reply_text(
        f"**__Hello {message.from_user.mention}, I am the Auto Approver Join Request Bot!__**\n\n"
        f"✅ Just [add me to your group/channel](https://t.me/{approvedbot.username}?startgroup=true) "
        f"and I will handle join requests automatically.\n\n"
        f"🔗 Repo: https://github.com/httpaju/AJ-Auto-Approval",
        reply_markup=InlineKeyboardMarkup(button),
        disable_web_page_preview=True
    )

@pr0fess0r_99.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client: Client, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} joined 🤝")
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=chat.id, text=TEXT.format(mention=user.mention, title=chat.title))

print("Auto Approved Bot is running ✅")
pr0fess0r_99.run()
