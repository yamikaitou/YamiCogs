from .core import Lottery


def setup(bot):
    bot.add_cog(Lottery(bot))
