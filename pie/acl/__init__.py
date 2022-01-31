from __future__ import annotations

from typing import Callable, TypeVar

from nextcord.ext import commands

from pie import i18n
from pie.exceptions import (
    NegativeUserOverwrite,
    NegativeChannelOverwrite,
    NegativeRoleOverwrite,
    InsufficientACLevel,
)
from pie.acl.database import ACDefault, ACLevel, ACLevelMappping
from pie.acl.database import UserOverwrite, ChannelOverwrite, RoleOverwrite

_ = i18n.Translator(__file__).translate
T = TypeVar("T")


def acl(ctx: commands.Context) -> bool:
    """Fallback ACL."""
    return True


def acl2(level: ACLevel) -> Callable[[T], T]:
    """A decorator that adds ACL check to a command.

    Each command has its preferred ACL group set in the decorator. Bot owner
    can add user and channel overwrites to these decorators, to allow detailed
    controll over the system with sane defaults provided by the system itself.

    Usage:

    . code-block:: python
        :linenos:

        from core import check

        ...

        @check.acl2(check.ACLevel.SUBMOD)
        @commands.command()
        async def repeat(self, ctx, *, input: str):
            await ctx.reply(utils.text.sanitise(input, escape=False))
    """

    def predicate(ctx: commands.Context) -> bool:
        return _acl2(ctx, level)

    return commands.check(predicate)


def _acl2(ctx: commands.Context, level: ACLevel) -> bool:
    """Check function based on Access Control."""
    # Allow invocations in DM.
    # Wrap the function in `@commands.guild_only()` to change this behavior.
    if ctx.guild is None:
        return True

    command: str = ctx.command.qualified_name

    uo = UserOverwrite.get(ctx.guild.id, ctx.author.id, command)
    if uo is not None:
        if uo.allow:
            return True
        raise NegativeUserOverwrite()

    co = ChannelOverwrite.get(ctx.guild.id, ctx.channel.id, command)
    if co is not None:
        if co.allow:
            return True
        raise NegativeChannelOverwrite(channel=ctx.channel)

    for role in ctx.author.roles:
        ro = RoleOverwrite.get(ctx.guild.id, role.id, command)
        if ro is not None:
            if ro.allow:
                return True
            raise NegativeRoleOverwrite(role=role)

    mapped_level = ACLevel.EVERYONE
    for role in ctx.author.roles[::-1]:
        m = ACLevelMappping.get(ctx.guild.id, role.id)
        if m is not None:
            mapped_level = m.level
            break

    custom_level = ACDefault.get(ctx.guild.id, command)
    if custom_level:
        level = custom_level.level

    if mapped_level >= level:
        return True
    raise InsufficientACLevel(required=level, actual=mapped_level)
