from .core import PokemonGo


def setup(bot):
    bot.add_cog(PokemonGo(bot))
