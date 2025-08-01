

from telegram import Update, MessageEntity
from telegram.ext import Application, CommandHandler, ContextTypes
import re
import random

# Temporary in-memory storage
deal_stats = {
    "total_amount": 0,
    "deal_count": 0,
    "users": {},  # user_id: total_deals_amount
}


BOT_TOKEN = "5854864826:AAE5oKcLlXAu0uyTjo0NQhXqIZCFbS06fok"


# Utility to extract amount
def extract_amount(text: str) -> float:
    match = re.search(r"DEAL AMMOUNT\s*:\s*(\d+)", text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

# Utility to extract user mention or fallback
def get_username(user):
    if user.username:
        return f"@{user.username}"
    else:
        return f"[{user.full_name}](tg://user?id={user.id})"

# ✅ /add command
async def add_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # 1. Check if in group
    if chat.type not in ("group", "supergroup"):
        await update.message.reply_text("Use this command in a group.")
        return

    # 2. Admin-only check
    admins = await chat.get_administrators()
    if user.id not in [admin.user.id for admin in admins]:
        await update.message.reply_text("🚫 Only group admins can use this command.")
        return

    # 3. Must be a reply to a message
    if not update.message.reply_to_message:
        await update.message.reply_text("❗Please reply to a deal message.")
        return

    original_msg = update.message.reply_to_message.text or ""
    amount = extract_amount(original_msg)

    if amount is None:
        await update.message.reply_text("❌ Couldn't find 'DEAL AMMOUNT : <amount>' in replied message.")
        return

    # 4. Escrow Calculations
    fee = round(amount * 0.05, 2)
    release_amount = round(amount - fee, 2)
    trade_id = f"#TID{random.randint(100000,999999)}"
    escrowed_by = get_username(user)

    # 5. Stats Update
    deal_stats["deal_count"] += 1
    deal_stats["total_amount"] += amount
    deal_stats["users"][user.id] = deal_stats["users"].get(user.id, 0) + amount

    # 6. Final reply (replying to original message)
    message = (
        "💰 *P.A.G.A.L INR Transactions*\n\n"
        f"💵 *Received Amount*: ₹{amount}\n"
        f"💸 *Release/Refund Amount*: ₹{release_amount}\n"
        f"⚖️ *Escrow Fee*: ₹{fee}\n"
        f"🆔 *Trade ID*: {trade_id}\n"
        f"🤖 *Escrowed by*: {escrowed_by}"
    )

    await update.message.reply_to_message.reply_text(message, parse_mode="Markdown")

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to P.A.G.A.L Escrow Bot!\n"
        "Use /add by replying to a deal message with 'DEAL AMMOUNT : xxx rs'.\n"
        "Only group admins can initiate escrow.\n\n"
        "Use /stats to view all deals summary."
    )

# ✅ /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive!")

# ✅ /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = deal_stats["total_amount"]
    count = deal_stats["deal_count"]
    msg = f"📊 *Escrow Stats*\n\n"
    msg += f"📦 Total Deals: {count}\n"
    msg += f"💸 Total Volume: ₹{total}\n\n"

    if deal_stats["users"]:
        msg += "👤 *Deal By Users:*\n"
        for uid, amt in deal_stats["users"].items():
            name = f"[User](tg://user?id={uid})"
            msg += f"• {name}: ₹{amt}\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

# Main bot runner
if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("add", add_deal))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()
