from loguru import logger
from vkbottle.user import User

from blueprints import labelers
from blueprints.autoai import ai_activate
from config import api, labeler

logger.remove()
logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="00:00",
    compression=zip,
)

bot = User(api=api, labeler=labeler)

for level in labelers:
    labeler.load(level)

bot.loop_wrapper.add_task(ai_activate)
bot.run_forever()
