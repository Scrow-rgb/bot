import discord
from discord.ext import commands
import os
import logging



permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
permissoes.voice_states = True
bot = commands.Bot(command_prefix='/', intents=permissoes)


logging.basicConfig(level=logging.DEBUG)



@bot.event
async def on_ready():
    await carregar_cogs()
    await bot.tree.sync()
    print(f'{bot.user} está online')

# @bot.command()
# async def sync(ctx:commands.Context):
#     if ctx.author.id == 424351151534768128:
#         server = discord.Object(id=1123842079169192016)
#         sincs = await bot.tree.sync(guild=server)
#         await ctx.reply(f'{len(sincs)} comandos sincronizados')
#     else:
#         await ctx.reply('Apenas o meu criador pode usar esse comando')

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print('O bot não tem permissão para apagar mensagens')
        except discord.HTTPException as e:
            print(f'Erro ao tentar apagar a mensagem: {e}')

    await ctx.send('Desculpe, esse comando não existe. Tente `/ajuda`, para ver a minha lista de comandos', delete_after=5)


async def carregar_cogs():

    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')


bot.run('SEU_TOKEN_AQUI')
