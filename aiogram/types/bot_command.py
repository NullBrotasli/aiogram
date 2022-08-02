from . import base
from . import fields


class BotCommand(base.TelegramObject):
    """
    This object represents a bot command.

    https://core.telegram.org/bots/api#botcommand
    """
    command: base.String = fields.Field()
    description: base.String = fields.Field()
