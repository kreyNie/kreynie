from typing import List, Literal, Optional

from config import api, ban_group_id, ban_reason_group_id
from utils.info_classes import UserInfo
from vkbottle import VKAPIError
from vkbottle.tools import PhotoWallUploader

from .functions import get_id_from_text


class VKHandler:
    @staticmethod
    async def upload_image(photo: str | bytes) -> str | List[dict]:
        return await PhotoWallUploader(api).upload(photo)

    @staticmethod
    async def get_user_info(
        user: str,
        name_case: Optional[Literal["nom", "gen", "dat", "acc", "ins", "abl"]] = None,
    ) -> UserInfo | None:
        matched = await get_id_from_text(user)
        if not matched:
            return None

        info = await api.users.get(matched, name_case)
        if not info:
            return None

        return UserInfo(
            id=info[0].id,
            first_name=info[0].first_name,
            last_name=info[0].last_name,
        )

    @staticmethod
    async def ban(*args, **kwargs) -> int:
        return await api.groups.ban(group_id=abs(ban_group_id), *args, **kwargs)

    @staticmethod
    async def check_if_banned(user_id: int) -> bool:
        try:
            await api.groups.get_banned(group_id=abs(ban_group_id), owner_id=user_id)
            return True
        except VKAPIError[104]:
            return False

    @staticmethod
    async def post(**kwargs):
        return await api.wall.post(owner_id=ban_reason_group_id, **kwargs)

    @staticmethod
    async def get_posts(count: int = 1) -> list:
        posts = await api.wall.get(owner_id=ban_group_id, count=count)
        return posts.items

    @staticmethod
    async def get_comments(**kwargs):
        return await api.wall.get_comments(owner_id=ban_group_id, sort="desc", **kwargs)

    @staticmethod
    async def send_message(*args, **kwargs) -> int:
        return await api.messages.send(*args, **kwargs)
