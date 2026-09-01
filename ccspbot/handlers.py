"""Telegram handlers. No SQL here; all data access goes through ccspbot.db.

Two Telegram constraints shape this module:

- ``callback_data`` is capped at 64 bytes, so buttons carry the numeric
  AnswerID rather than the answer text. The original bot sent the text and
  crashed on any answer longer than the cap.
- ``answerCallbackQuery`` truncates its alert at roughly 200 characters, which
  is shorter than most explanations. The verdict goes in the alert; the
  explanation is sent as a message.
"""

from __future__ import annotations

import logging
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ccspbot import outline, quiz
from ccspbot.db import Item, QuestionBank, StatsStore

logger = logging.getLogger(__name__)

SESSION_KEY = "session"

WELCOME = (
    "<b>CCSP practice bot</b>\n\n"
    "{total} questions, tagged against the ISC2 exam outline in force since "
    "1 August 2026.\n\n"
    "/askchallenge [n] - n questions (default {default}, max {maximum}), weighted like the exam\n"
    "/domain &lt;1-6&gt; - practise a single domain\n"
    "/exam - {exam}-question mock, scored per domain\n"
    "/stats - your accuracy per domain\n"
    "/weak - only the questions you last got wrong\n"
    "/domains - the six domains and their weights"
)


def _bank(context: ContextTypes.DEFAULT_TYPE) -> QuestionBank:
    return context.application.bot_data["bank"]


def _stats(context: ContextTypes.DEFAULT_TYPE) -> StatsStore:
    return context.application.bot_data["stats"]


def _keyboard(item: Item) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(o.text, callback_data=str(o.answer_id))] for o in item.options]
    )


async def _send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session: quiz.Session = context.user_data[SESSION_KEY]

    if session.finished:
        await context.bot.send_message(
            update.effective_chat.id,
            quiz.format_results(session),
            parse_mode=ParseMode.HTML,
        )
        logger.info(
            "user %s finished %s: %d/%d",
            update.effective_user.id, session.label,
            session.correct_count, len(session.results),
        )
        del context.user_data[SESSION_KEY]
        return

    item = session.current
    await context.bot.send_message(
        update.effective_chat.id,
        f"<b>{session.position}</b>  <i>Domain {item.domain} - {escape(item.subdomain)}</i>\n\n"
        f"{escape(item.text)}",
        parse_mode=ParseMode.HTML,
        reply_markup=_keyboard(item),
    )


async def _start_session(
    update: Update, context: ContextTypes.DEFAULT_TYPE, items: list[Item], label: str
) -> None:
    if not items:
        await update.message.reply_text("No questions matched. Try /askchallenge.")
        return

    context.user_data[SESSION_KEY] = quiz.Session(items=items, label=label)
    logger.info("user %s started %s with %d questions", update.effective_user.id, label, len(items))
    await update.message.reply_text(f"{label.title()}: {len(items)} questions. Good luck.")
    await _send_question(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME.format(
            total=_bank(context).total(),
            default=quiz.DEFAULT_QUESTIONS,
            maximum=quiz.MAX_QUESTIONS,
            exam=quiz.EXAM_QUESTIONS,
        ),
        parse_mode=ParseMode.HTML,
    )


async def domains(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    have = _bank(context).counts_by_domain()
    lines = ["<b>CCSP domains</b> (outline effective 1 August 2026)", ""]
    for d, (title, weight) in outline.DOMAINS.items():
        lines.append(f"{d}. {escape(title)} - {weight:.0%} - {have.get(d, 0)} questions")
    lines += ["", "Practise one with /domain &lt;number&gt;."]
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


def _requested_count(args: list[str], default: int) -> int:
    if not args or not args[0].isdigit():
        return default
    return max(1, min(int(args[0]), quiz.MAX_QUESTIONS))


async def askchallenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    n = _requested_count(context.args, quiz.DEFAULT_QUESTIONS)
    items = _bank(context).sample_weighted(n)
    await _start_session(update, context, items, "challenge")


async def domain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].isdigit() or int(context.args[0]) not in outline.DOMAINS:
        await update.message.reply_text("Usage: /domain <1-6>. See /domains for the list.")
        return

    d = int(context.args[0])
    items = _bank(context).sample(quiz.DEFAULT_QUESTIONS, domain=d)
    await _start_session(update, context, items, f"domain {d}")


async def exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = _bank(context).sample_weighted(quiz.EXAM_QUESTIONS)
    await _start_session(update, context, items, "exam")


async def weak(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    slugs = _stats(context).weak_slugs(update.effective_user.id)
    if not slugs:
        await update.message.reply_text(
            "Nothing to review - you have not got a question wrong yet, or you have "
            "since answered them all correctly. Try /askchallenge."
        )
        return

    items = _bank(context).sample(quiz.DEFAULT_QUESTIONS, slugs=slugs)
    await _start_session(update, context, items, "review")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    accuracy = _stats(context).accuracy_by_domain(update.effective_user.id)
    if not accuracy:
        await update.message.reply_text("No attempts recorded yet. Start with /askchallenge.")
        return

    total_ok = sum(ok for ok, _ in accuracy.values())
    total_n = sum(n for _, n in accuracy.values())

    lines = [f"<b>Your accuracy</b> - {total_ok}/{total_n} ({total_ok / total_n:.0%})", ""]
    for d, (title, _) in outline.DOMAINS.items():
        ok, n = accuracy.get(d, (0, 0))
        if n == 0:
            lines.append(f"{d}. {escape(title)} - not attempted")
        else:
            lines.append(f"{d}. {escape(title)} - {ok}/{n} ({ok / n:.0%})")

    weakest = min(
        (d for d, (_, n) in accuracy.items() if n >= 3),
        key=lambda d: accuracy[d][0] / accuracy[d][1],
        default=None,
    )
    if weakest is not None:
        lines += ["", f"Weakest domain: {weakest}. Practise it with /domain {weakest}."]

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def on_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    session: quiz.Session | None = context.user_data.get(SESSION_KEY)

    if session is None:
        await query.answer("That round is over. Start a new one with /askchallenge.", show_alert=True)
        return

    answer_id = int(query.data)
    if not session.owns(answer_id):
        await query.answer("That button belongs to an earlier question.", show_alert=True)
        return

    correct, item = session.answer(answer_id)
    _stats(context).record(update.effective_user.id, item.slug, item.domain, correct)

    await query.answer("Correct" if correct else f"Wrong - {item.correct.text}"[:200], show_alert=True)
    await query.edit_message_reply_markup(reply_markup=None)

    verdict = "Correct" if correct else "Incorrect"
    body = [
        f"<b>{verdict}</b> - {escape(item.correct.text)}",
        "",
        escape(item.explanation),
    ]
    if item.reference:
        body += ["", f"<i>{escape(item.reference)}</i>"]

    await context.bot.send_message(
        update.effective_chat.id, "\n".join(body), parse_mode=ParseMode.HTML
    )
    await _send_question(update, context)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Not a command I know. Send /start to see the list.")


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("handler failed", exc_info=context.error)
