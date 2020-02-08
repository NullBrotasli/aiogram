from . import base
from . import fields
import typing


class WebhookInfo(base.TelegramObject):
    """
    Contains information about the current status of a webhook.
    All types used in the Bot API responses are represented as JSON-objects.
    It is safe to use 32-bit signed integers for storing all Integer fields unless otherwise noted.
    Optional fields may be not returned when irrelevant.

    https://core.telegram.org/bots/api#webhookinfo
    """
    url: base.String = fields.Field()
    has_custom_certificate: base.Boolean = fields.Field()
    pending_update_count: base.Integer = fields.Field()
    last_error_date: base.Integer = fields.Field()
    last_error_message: base.String = fields.Field()
    max_connections: base.Integer = fields.Field()
    allowed_updates: typing.List[base.String] = fields.ListField()

