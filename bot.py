# ============================================================
# NANO-TEMPLAR COMPLIANCE + ANTI-BAN SAFETY LAYER (DROP-IN)
# ============================================================

class Compliance:
    def __init__(self):
        # Keywords that trigger bans if detected in user messages
        self.forbidden_keywords = [
            "hack", "hacking", "breach", "crack", "exploit", "payload",
            "sqlmap", "nmap", "masscan", "hydra", "dirbuster",
            "token_dump", "session_steal", "admin_override",
            "unauthorized", "bypass", "penetration", "scrape_protected"
        ]

        # Actions your bot should NEVER perform
        self.forbidden_actions = [
            "unauthorized_access",
            "endpoint_probe",
            "restricted_api_call",
            "mass_messaging",
            "credential_guessing",
            "automated_login",
            "tos_violation",
            "rate_limit_break"
        ]

        # Rate limit protection (prevents Telegram bans)
        self.max_messages_per_minute = 20
        self.message_log = []

    # Log each message to enforce rate limits
    def log_message(self, user_id):
        from time import time
        now = time()
        self.message_log.append((user_id, now))
        # Keep only last 60 seconds of logs
        self.message_log = [(uid, ts) for (uid, ts) in self.message_log if now - ts < 60]

    # Check if message rate is safe
    def rate_limit_ok(self):
        return len(self.message_log) <= self.max_messages_per_minute

    # Check for forbidden keywords
    def safe_text(self, text):
        lowered = text.lower()
        for keyword in self.forbidden_keywords:
            if keyword in lowered:
                return False
        return True

    # Check for forbidden action types
    def safe_action(self, action):
        return action not in self.forbidden_actions

    # Main compliance check
    def check(self, text, action="message"):
        if not self.safe_text(text):
            return False, "⚠️ Forbidden keywords detected. Action blocked."
        if not self.safe_action(action):
            return False, "⚠️ Forbidden action type. Blocked."
        if not self.rate_limit_ok():
            return False, "⚠️ Rate limit exceeded. Slow down to avoid bans."
        return True, "OK"


# Instantiate compliance layer
compliance = Compliance()

# ============================================================
# SAFE REPLY WRAPPER — USE THIS INSTEAD OF update.message.reply_text
# ============================================================

async def safe_reply(update, context, text):
    ok, msg = compliance.check(text)x
    if not ok:
        await update.message.reply_text(msg)
        return
    compliance.log_message(update.effective_user.id)
    await update.message.reply_text(text)

# ============================================================
# EXAMPLE COMMAND USING SAFETY LAYER
# ============================================================

async def start(update, context):
    await safe_reply(update, context,
        "Nano-Templar Wealth System Online.\n"
        "All actions lawful. All operations logged."
    )

# Add this handler in your bot setup:
# app.add_handler(CommandHandler('start', start))

# ============================================================
# END OF BLOCK
# ============================================================
