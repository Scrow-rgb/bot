import discord
from discord.ext import commands
import os
import logging

# Configuração de permissões (intents)
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
permissoes.voice_states = True

bot = commands.Bot(command_prefix='/', intents=permissoes)

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Dicionário para mapear guildas (servidores) e canais padrão
guild_channel_map = {}

@bot.event
async def on_ready():
    await carregar_cogs()
    await bot.tree.sync()
    print(f'{bot.user} está online')

    # Inicializa o mapeamento de guildas para canais padrão
    for guild in bot.guilds:
        default_channel = guild.text_channels[0] if guild.text_channels else None  # Seleciona o primeiro canal de texto, se disponível
        if default_channel:
            guild_channel_map[guild.id] = default_channel.id
    print("Mapa de Guildas e Canais carregado:", guild_channel_map)


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print('O bot não tem permissão para apagar mensagens')
        except discord.HTTPException as e:
            print(f'Erro ao tentar apagar a mensagem: {e}')
    
    await ctx.send('Desculpe, esse comando não existe. Tente `/ajuda` para ver a minha lista de comandos', delete_after=5)

async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{arquivo[:-3]}')
            except Exception as e:
                print(f'Falha ao carregar cog {arquivo}: {e}')

# Lembre-se de nunca expor seu token publicamente!
bot.run('MTI3ODI0MzUwNTQ1MzY2MjI0Mg.GG4Fp9.VH3wKbAc6HFSRTySUuiaKmHUclV3cCPvk7bx4s')
