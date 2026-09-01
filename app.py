#!/usr/bin/env python3
"""ccspbot entry point. Wiring only - behaviour lives in the ccspbot package."""

from __future__ import annotations

import logging
import os
import sys

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from ccspbot import handlers
from ccspbot.db import QuestionBank, StatsStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

# httpx logs every request line at INFO, and the Telegram API carries the token
# in the URL path - so at INFO the bot token is written to the container logs on
# every poll. The same secret the Dockerfile and CI keep out of the image would
# then sit in plain text in `docker logs`. Warnings and errors still come out.
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger("ccspbot")


def main() -> int:
    token = os.environ.get("TOKEN_BOT")
    if not token:
        print(
            "TOKEN_BOT is not set.\n\n"
            "Pass it at runtime, never at build time:\n"
            "    docker run -e TOKEN_BOT=... ccspbot",
            file=sys.stderr,
        )
        return 1

    try:
        bank = QuestionBank()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    stats = StatsStore()
    logger.info("question bank loaded: %d questions", bank.total())

    app = Application.builder().token(token).build()
    app.bot_data["bank"] = bank
    app.bot_data["stats"] = stats

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.start))
    app.add_handler(CommandHandler("domains", handlers.domains))
    app.add_handler(CommandHandler("askchallenge", handlers.askchallenge))
    app.add_handler(CommandHandler("domain", handlers.domain))
    app.add_handler(CommandHandler("exam", handlers.exam))
    app.add_handler(CommandHandler("stats", handlers.stats))
    app.add_handler(CommandHandler("weak", handlers.weak))
    app.add_handler(CallbackQueryHandler(handlers.on_answer))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.fallback))
    app.add_error_handler(handlers.on_error)

    app.run_polling()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
