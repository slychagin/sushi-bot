import hashlib
from aiogram import types, Dispatcher


async def inline_handler(query: types.InlineQuery):
    """Send to user articles from Wikipedia by request"""
    text = query.query or 'echo'
    link = 'https://ru.wikipedia.org/wiki/' + text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id=result_id,
        title='Статья Wikipedia:',
        url=link,
        input_message_content=types.InputTextMessageContent(
            message_text=link))]
    await query.answer(articles, cache_time=1, is_personal=True)


def register_handlers_inline(dp: Dispatcher):
    """Register all inline handlers"""
    dp.register_inline_handler(inline_handler)
