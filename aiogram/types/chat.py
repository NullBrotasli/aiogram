import asyncio
import typing

from . import base
from . import fields
from .chat_photo import ChatPhoto
from ..utils import helper
from ..utils import markdown


class Chat(base.TelegramObject):
    """
    This object represents a chat.

    https://core.telegram.org/bots/api#chat
    """
    id: base.Integer = fields.Field()
    type: base.String = fields.Field()
    title: base.String = fields.Field()
    username: base.String = fields.Field()
    first_name: base.String = fields.Field()
    last_name: base.String = fields.Field()
    all_members_are_administrators: base.Boolean = fields.Field()
    photo: ChatPhoto = fields.Field(base=ChatPhoto)
    description: base.String = fields.Field()
    invite_link: base.String = fields.Field()
    pinned_message: 'Message' = fields.Field(base='Message')
    sticker_set_name: base.String = fields.Field()
    can_set_sticker_set: base.Boolean = fields.Field()

    @property
    def full_name(self):
        if self.type == ChatType.PRIVATE:
            full_name = self.first_name
            if self.last_name:
                full_name += ' ' + self.last_name
            return full_name
        return self.title

    @property
    def mention(self):
        """
        Get mention if dialog have username or full name if this is Private dialog otherwise None
        """
        if self.username:
            return '@' + self.username
        if self.type == ChatType.PRIVATE:
            return self.full_name
        return None

    @property
    def user_url(self):
        if self.type != ChatType.PRIVATE:
            raise TypeError('This property available only in private chats.')

        return f"tg://user?id={self.id}"

    def get_mention(self, name=None, as_html=False):
        if name is None:
            name = self.mention
        if as_html:
            return markdown.hlink(name, self.user_url)
        return markdown.link(name, self.user_url)

    async def set_photo(self, photo):
        """
        Use this method to set a new profile photo for the chat. Photos can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
        setting is off in the target group.

        Source: https://core.telegram.org/bots/api#setchatphoto

        :param photo: New chat photo, uploaded using multipart/form-data
        :type photo: :obj:`base.InputFile`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.set_chat_photo(self.id, photo)

    async def delete_photo(self):
        """
        Use this method to delete a chat photo. Photos can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
        setting is off in the target group.

        Source: https://core.telegram.org/bots/api#deletechatphoto

        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.delete_chat_photo(self.id)

    async def set_title(self, title):
        """
        Use this method to change the title of a chat. Titles can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
        setting is off in the target group.

        Source: https://core.telegram.org/bots/api#setchattitle

        :param title: New chat title, 1-255 characters
        :type title: :obj:`base.String`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.set_chat_title(self.id, title)

    async def set_description(self, description):
        """
        Use this method to change the description of a supergroup or a channel.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Source: https://core.telegram.org/bots/api#setchatdescription

        :param description: New chat description, 0-255 characters
        :type description: :obj:`typing.Union[base.String, None]`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.delete_chat_description(self.id, description)

    async def kick(self, user_id: base.Integer,
                   until_date: typing.Union[base.Integer, None] = None):
        """
        Use this method to kick a user from a group, a supergroup or a channel.
        In the case of supergroups and channels, the user will not be able to return to the group
        on their own using invite links, etc., unless unbanned first.

        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’ setting
        is off in the target group.
        Otherwise members may only be removed by the group's creator or by the member that added them.

        Source: https://core.telegram.org/bots/api#kickchatmember

        :param user_id: Unique identifier of the target user
        :type user_id: :obj:`base.Integer`
        :param until_date: Date when the user will be unbanned, unix time.
        :type until_date: :obj:`typing.Union[base.Integer, None]`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.kick_chat_member(self.id, user_id=user_id, until_date=until_date)

    async def unban(self, user_id: base.Integer):
        """
        Use this method to unban a previously kicked user in a supergroup or channel. `
        The user will not return to the group or channel automatically, but will be able to join via link, etc.

        The bot must be an administrator for this to work.

        Source: https://core.telegram.org/bots/api#unbanchatmember

        :param user_id: Unique identifier of the target user
        :type user_id: :obj:`base.Integer`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.unban_chat_member(self.id, user_id=user_id)

    async def restrict(self, user_id: base.Integer,
                       until_date: typing.Union[base.Integer, None] = None,
                       can_send_messages: typing.Union[base.Boolean, None] = None,
                       can_send_media_messages: typing.Union[base.Boolean, None] = None,
                       can_send_other_messages: typing.Union[base.Boolean, None] = None,
                       can_add_web_page_previews: typing.Union[base.Boolean, None] = None) -> base.Boolean:
        """
        Use this method to restrict a user in a supergroup.
        The bot must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all boolean parameters to lift restrictions from a user.

        Source: https://core.telegram.org/bots/api#restrictchatmember

        :param user_id: Unique identifier of the target user
        :type user_id: :obj:`base.Integer`
        :param until_date: Date when restrictions will be lifted for the user, unix time.
        :type until_date: :obj:`typing.Union[base.Integer, None]`
        :param can_send_messages: Pass True, if the user can send text messages, contacts, locations and venues
        :type can_send_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_send_media_messages: Pass True, if the user can send audios, documents, photos, videos,
            video notes and voice notes, implies can_send_messages
        :type can_send_media_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_send_other_messages: Pass True, if the user can send animations, games, stickers and
            use inline bots, implies can_send_media_messages
        :type can_send_other_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_add_web_page_previews: Pass True, if the user may add web page previews to their messages,
            implies can_send_media_messages
        :type can_add_web_page_previews: :obj:`typing.Union[base.Boolean, None]`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return self.bot.restrict_chat_member(self.id, user_id=user_id, until_date=until_date,
                                             can_send_messages=can_send_messages,
                                             can_send_media_messages=can_send_media_messages,
                                             can_send_other_messages=can_send_other_messages,
                                             can_add_web_page_previews=can_add_web_page_previews)

    async def promote(self, user_id: base.Integer,
                      can_change_info: typing.Union[base.Boolean, None] = None,
                      can_post_messages: typing.Union[base.Boolean, None] = None,
                      can_edit_messages: typing.Union[base.Boolean, None] = None,
                      can_delete_messages: typing.Union[base.Boolean, None] = None,
                      can_invite_users: typing.Union[base.Boolean, None] = None,
                      can_restrict_members: typing.Union[base.Boolean, None] = None,
                      can_pin_messages: typing.Union[base.Boolean, None] = None,
                      can_promote_members: typing.Union[base.Boolean, None] = None) -> base.Boolean:
        """
        Use this method to promote or demote a user in a supergroup or a channel.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        Source: https://core.telegram.org/bots/api#promotechatmember

        :param user_id: Unique identifier of the target user
        :type user_id: :obj:`base.Integer`
        :param can_change_info: Pass True, if the administrator can change chat title, photo and other settings
        :type can_change_info: :obj:`typing.Union[base.Boolean, None]`
        :param can_post_messages: Pass True, if the administrator can create channel posts, channels only
        :type can_post_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_edit_messages: Pass True, if the administrator can edit messages of other users, channels only
        :type can_edit_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_delete_messages: Pass True, if the administrator can delete messages of other users
        :type can_delete_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_invite_users: Pass True, if the administrator can invite new users to the chat
        :type can_invite_users: :obj:`typing.Union[base.Boolean, None]`
        :param can_restrict_members: Pass True, if the administrator can restrict, ban or unban chat members
        :type can_restrict_members: :obj:`typing.Union[base.Boolean, None]`
        :param can_pin_messages: Pass True, if the administrator can pin messages, supergroups only
        :type can_pin_messages: :obj:`typing.Union[base.Boolean, None]`
        :param can_promote_members: Pass True, if the administrator can add new administrators
            with a subset of his own privileges or demote administrators that he has promoted,
            directly or indirectly (promoted by administrators that were appointed by him)
        :type can_promote_members: :obj:`typing.Union[base.Boolean, None]`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return self.bot.promote_chat_member(self.id,
                                            can_change_info=can_change_info,
                                            can_post_messages=can_post_messages,
                                            can_edit_messages=can_edit_messages,
                                            can_delete_messages=can_delete_messages,
                                            can_invite_users=can_invite_users,
                                            can_restrict_members=can_restrict_members,
                                            can_pin_messages=can_pin_messages,
                                            can_promote_members=can_promote_members)

    async def pin_message(self, message_id: int, disable_notification: bool = False):
        """
        Use this method to pin a message in a supergroup.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Source: https://core.telegram.org/bots/api#pinchatmessage

        :param message_id: Identifier of a message to pin
        :type message_id: :obj:`base.Integer`
        :param disable_notification: Pass True, if it is not necessary to send a notification to
            all group members about the new pinned message
        :type disable_notification: :obj:`typing.Union[base.Boolean, None]`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.pin_chat_message(self.id, message_id, disable_notification)

    async def unpin_message(self):
        """
        Use this method to unpin a message in a supergroup chat.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Source: https://core.telegram.org/bots/api#unpinchatmessage

        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.unpin_chat_message(self.id)

    async def leave(self):
        """
        Use this method for your bot to leave a group, supergroup or channel.

        Source: https://core.telegram.org/bots/api#leavechat

        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.leave_chat(self.id)

    async def get_administrators(self):
        """
        Use this method to get a list of administrators in a chat.

        Source: https://core.telegram.org/bots/api#getchatadministrators

        :return: On success, returns an Array of ChatMember objects that contains information about all
            chat administrators except other bots.
            If the chat is a group or a supergroup and no administrators were appointed,
            only the creator will be returned.
        :rtype: :obj:`typing.List[types.ChatMember]`
        """
        return await self.bot.get_chat_administrators(self.id)

    async def get_members_count(self):
        """
        Use this method to get the number of members in a chat.

        Source: https://core.telegram.org/bots/api#getchatmemberscount

        :return: Returns Int on success.
        :rtype: :obj:`base.Integer`
        """
        return await self.bot.get_chat_members_count(self.id)

    async def get_member(self, user_id):
        """
        Use this method to get information about a member of a chat.

        Source: https://core.telegram.org/bots/api#getchatmember

        :param user_id: Unique identifier of the target user
        :type user_id: :obj:`base.Integer`
        :return: Returns a ChatMember object on success.
        :rtype: :obj:`types.ChatMember`
        """
        return await self.bot.get_chat_member(self.id, user_id)

    async def do(self, action):
        """
        Use this method when you need to tell the user that something is happening on the bot's side.
        The status is set for 5 seconds or less
        (when a message arrives from your bot, Telegram clients clear its typing status).

        We only recommend using this method when a response from the bot will take
        a noticeable amount of time to arrive.

        Source: https://core.telegram.org/bots/api#sendchataction

        :param action: Type of action to broadcast.
        :type action: :obj:`base.String`
        :return: Returns True on success.
        :rtype: :obj:`base.Boolean`
        """
        return await self.bot.send_chat_action(self.id, action)

    async def export_invite_link(self):
        """
        Use this method to export an invite link to a supergroup or a channel.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Source: https://core.telegram.org/bots/api#exportchatinvitelink

        :return: Returns exported invite link as String on success.
        :rtype: :obj:`base.String`
        """
        if self.invite_link:
            return self.invite_link
        return await self.bot.export_chat_invite_link(self.id)

    def __int__(self):
        return self.id


class ChatType(helper.Helper):
    """
    List of chat types

    :key: PRIVATE
    :key: GROUP
    :key: SUPER_GROUP
    :key: CHANNEL
    """

    mode = helper.HelperMode.lowercase

    PRIVATE = helper.Item()  # private
    GROUP = helper.Item()  # group
    SUPER_GROUP = helper.Item()  # supergroup
    CHANNEL = helper.Item()  # channel

    @staticmethod
    def _check(obj, chat_types) -> bool:
        if hasattr(obj, 'chat'):
            obj = obj.chat
        if not hasattr(obj, 'type'):
            return False
        return obj.type in chat_types

    @classmethod
    def is_private(cls, obj) -> bool:
        """
        Check chat is private

        :param obj:
        :return:
        """
        return cls._check(obj, [cls.PRIVATE])

    @classmethod
    def is_group(cls, obj) -> bool:
        """
        Check chat is group

        :param obj:
        :return:
        """
        return cls._check(obj, [cls.GROUP])

    @classmethod
    def is_super_group(cls, obj) -> bool:
        """
        Check chat is super-group

        :param obj:
        :return:
        """
        return cls._check(obj, [cls.SUPER_GROUP])

    @classmethod
    def is_group_or_super_group(cls, obj) -> bool:
        """
        Check chat is group or super-group

        :param obj:
        :return:
        """
        return cls._check(obj, [cls.GROUP, cls.SUPER_GROUP])

    @classmethod
    def is_channel(cls, obj) -> bool:
        """
        Check chat is channel

        :param obj:
        :return:
        """
        return cls._check(obj, [cls.CHANNEL])


class ChatActions(helper.Helper):
    """
    List of chat actions

    :key: TYPING
    :key: UPLOAD_PHOTO
    :key: RECORD_VIDEO
    :key: UPLOAD_VIDEO
    :key: RECORD_AUDIO
    :key: UPLOAD_AUDIO
    :key: UPLOAD_DOCUMENT
    :key: FIND_LOCATION
    :key: RECORD_VIDEO_NOTE
    :key: UPLOAD_VIDEO_NOTE
    """

    mode = helper.HelperMode.snake_case

    TYPING: str = helper.Item()  # typing
    UPLOAD_PHOTO: str = helper.Item()  # upload_photo
    RECORD_VIDEO: str = helper.Item()  # record_video
    UPLOAD_VIDEO: str = helper.Item()  # upload_video
    RECORD_AUDIO: str = helper.Item()  # record_audio
    UPLOAD_AUDIO: str = helper.Item()  # upload_audio
    UPLOAD_DOCUMENT: str = helper.Item()  # upload_document
    FIND_LOCATION: str = helper.Item()  # find_location
    RECORD_VIDEO_NOTE: str = helper.Item()  # record_video_note
    UPLOAD_VIDEO_NOTE: str = helper.Item()  # upload_video_note

    @classmethod
    async def _do(cls, action: str, sleep=None):
        from ..dispatcher.ctx import get_bot, get_chat
        await get_bot().send_chat_action(get_chat(), action)
        if sleep:
            await asyncio.sleep(sleep)

    @classmethod
    def calc_timeout(cls, text, timeout=.8):
        """
        Calculate timeout for text

        :param text:
        :param timeout:
        :return:
        """
        return min((len(str(text)) * timeout, 5.0))

    @classmethod
    async def typing(cls, sleep=None):
        """
        Do typing

        :param sleep: sleep timeout
        :return:
        """
        if isinstance(sleep, str):
            sleep = cls.calc_timeout(sleep)
        await cls._do(cls.TYPING, sleep)

    @classmethod
    async def upload_photo(cls, sleep=None):
        """
        Do upload_photo

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.UPLOAD_PHOTO, sleep)

    @classmethod
    async def record_video(cls, sleep=None):
        """
        Do record video

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.UPLOAD_PHOTO, sleep)

    @classmethod
    async def upload_video(cls, sleep=None):
        """
        Do upload video

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.RECORD_VIDEO, sleep)

    @classmethod
    async def record_audio(cls, sleep=None):
        """
        Do record audio

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.UPLOAD_VIDEO, sleep)

    @classmethod
    async def upload_audio(cls, sleep=None):
        """
        Do upload audio

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.RECORD_AUDIO, sleep)

    @classmethod
    async def upload_document(cls, sleep=None):
        """
        Do upload document

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.UPLOAD_AUDIO, sleep)

    @classmethod
    async def find_location(cls, sleep=None):
        """
        Do find location

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.UPLOAD_DOCUMENT, sleep)

    @classmethod
    async def record_video_note(cls, sleep=None):
        """
        Do record video note

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.FIND_LOCATION, sleep)

    @classmethod
    async def upload_video_note(cls, sleep=None):
        """
        Do upload video note

        :param sleep: sleep timeout
        :return:
        """
        await cls._do(cls.RECORD_VIDEO_NOTE, sleep)
