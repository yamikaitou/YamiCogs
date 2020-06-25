from .core import FourInARow


def setup(bot):
    bot.add_cog(FourInARow(bot))
