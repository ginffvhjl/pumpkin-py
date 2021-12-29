from __future__ import annotations

import enum
from typing import Any, Dict, Optional, List

from sqlalchemy import BigInteger, Boolean, Column, Enum, String, Integer

from pie.database import database, session


class ACLevel(enum.IntEnum):
    BOT_OWNER: int = 5
    OWNER: int = 4
    MOD: int = 3
    SUBMOD: int = 2
    MEMBER: int = 1
    EVERYONE: int = 0


class RoleOverwrite(database.base):
    __tablename__ = "pie_acl_role_overwrite"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    role_id = Column(BigInteger)
    command = Column(String)
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, role_id: int, command: str, allow: bool
    ) -> Optional[RoleOverwrite]:
        pass

    @staticmethod
    def get(guild_id: int, role_id: int, command: str) -> Optional[RoleOverwrite]:
        pass

    @staticmethod
    def get_all(guild_id: int) -> List[RoleOverwrite]:
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> Dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "role_id": self.role_id,
            "allow": self.allow,
        }


class UserOverwrite(database.base):
    __tablename__ = "pie_acl_user_overwrite"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    user_id = Column(BigInteger)
    command = Column(String)
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, user_id: int, command: str, allow: bool
    ) -> Optional[UserOverwrite]:
        pass

    @staticmethod
    def get(guild_id: int, user_id: int, command: str) -> Optional[UserOverwrite]:
        pass

    @staticmethod
    def get_all(guild_id: int) -> List[UserOverwrite]:
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> Dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "user_id": self.user_id,
            "allow": self.allow,
        }


class ChannelOverwrite(database.base):
    __tablename__ = "pie_acl_channel_overwrite"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    command = Column(String)
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, channel_id: int, command: str, allow: bool
    ) -> Optional[ChannelOverwrite]:
        pass

    @staticmethod
    def get(guild_id: int, channel_id: int, command: str) -> Optional[ChannelOverwrite]:
        pass

    @staticmethod
    def get_all(guild_id: int) -> List[ChannelOverwrite]:
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> Dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "allow": self.allow,
        }


class ACLevelMappping(database.base):
    __tablename__ = "pie_acl_aclevel_mapping"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger)
    role_id = Column(BigInteger)
    level = Column(Enum(ACLevel))

    def add(guild_id: int, role_id: int, level: ACLevel) -> Optional[ACLevelMappping]:
        pass

    def get(guild_id: int, role_id: int) -> Optional[ACLevelMappping]:
        pass

    def get_all(guild_id: int) -> List[ACLevelMappping]:
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"guild_id='{self.guild_id}' role_id='{self.role_id}' "
            f"level='{self.level.name}'>"
        )

    def dump(self) -> Dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "role_id": self.role_id,
            "level": self.level,
        }
