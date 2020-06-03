from .kill import Kill


def setup(bot):
    bot.add_cog(Kill(bot))
