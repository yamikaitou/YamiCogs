# -*- coding: utf-8 -*-
from .tube import Tube


async def setup(bot):
    await bot.add_cog(Tube(bot))
