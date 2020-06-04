from .core import MinecraftCasino


def setup(bot):
    bot.add_cog(MinecraftCasino(bot))
