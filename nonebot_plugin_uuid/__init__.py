from re import findall
import uuid

from nonebot.params import CommandArg
from nonebot import get_driver, on_command, on_keyword
from nonebot.adapters.onebot.v11 import MessageSegment, Message, MessageEvent, Bot

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

summon = on_command("uuid")
summon5 = on_command("uuid5")

rm_hyphens = on_keyword({"rhs"}, priority=1, block=True)


@summon.handle()
async def _(event: MessageEvent):
    await summon.finish(reply_out(event.message_id, str(uuid.uuid4())))


@summon5.handle()
async def _(event: MessageEvent, keywd=CommandArg()):
    await summon5.finish(
        reply_out(
            event.message_id,
            str(uuid.uuid5(uuid.NAMESPACE_DNS, keywd.extract_plain_text()))
        )
    )


@rm_hyphens.handle()
async def _(bot: Bot, event: MessageEvent):
    # sourcery skip: use-named-expression
    reply_msg = event.reply
    if reply_msg and (event.message.extract_plain_text() == "rhs"):
        raw_txt = reply_msg.message.extract_plain_text()
        raw_uuids = findall(
            r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', raw_txt)

        if raw_uuids:
            await rm_hyphens.finish(
                reply_out(
                    event.message_id,
                    "\n\n".join(raw_uuid.replace("-", "")
                                for raw_uuid in raw_uuids)
                )
            )


def reply_out(msg_id: int, output: str) -> Message:
    """给消息包装上“回复”

    Args:
        msg_id (int): 所要回复的消息id
        output (str): 所要包装的消息原文

    Returns:
        Message
    """
    return MessageSegment.reply(id_=msg_id) + MessageSegment.text(output)
