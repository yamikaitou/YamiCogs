# -*- coding: utf-8 -*-
from .tube import Tube

async def setup(bot):
    bot.add_cog(Tube(bot))