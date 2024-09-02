import discord
from discord.ext import commands
import os
import yt_dlp as youtube_dl

# Configuração de permissões (intents)
permissoes = discord.Intents.default()
permissoes.message_content = True
permissoes.members = True
permissoes.voice_states = True

bot = commands.Bot(command_prefix='/', intents=permissoes)


logging.basicConfig(level=logging.DEBUG)

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Dicionário para mapear guildas (servidores) e canais padrão
guild_channel_map = {}

@bot.event
async def on_ready():
    await carregar_cogs()
    await bot.tree.sync()
    print('Estou Pronto!!')

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'source_address': None,
    'default_search': 'auto',
    'extract_flat': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}



ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'source_address': None,
            'default_search': 'auto',
            'extract_flat': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [cls.progress_hook]
        }
        if stream:
            ydl_opts['noplaylist'] = False

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
        if 'entries' in info:
            info = info['entries'][0]

        filename = info['formats'][0]['url']
        data = {
            'url': filename,
            'title': info.get('title', 'Unknown'),
        }
        return cls(discord.FFmpegPCMAudio(filename), data=data)

    @staticmethod
    def progress_hook(d):
        if d['status'] == 'finished':
            print(f'Download finished: {d["filename"]}')

@bot.tree.command(name='join')
async def join(interact:discord.Interaction):
    if interact.user.voice:
        channel = interact.user.voice.channel
        if interact.guild.voice_client is None:
            await channel.connect()
            await interact.response.send_message(f'Conectado ao canal: {channel.name}', ephemeral=True)
        else:
            await interact.response.send_message(f'O bot já está conectado a {interact.guild.voice_client.channel.name}', ephemeral=True)
    else:
        await interact.response.send_message("Você precisa estar em um canal de voz para usar este comando.", ephemeral=True)

@bot.tree.command(name='leave')
async def leave(interact:discord.Interaction):
    voice_client = interact.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await interact.response.send_message("Desconectado do canal de voz.", ephemeral=True)
    else:
        await interact.response.send_message("O bot não está conectado a nenhum canal de voz.", ephemeral=True)

@bot.tree.command(name='play', description='Reproduz uma música a partir de uma URL.')
async def play(interact:discord.Interaction, url:str):
    try:
        await interact.response.defer()  # Defer the interaction to avoid timeouts
        voice_channel = interact.guild.voice_client

        if not voice_channel:
            if interact.user.voice:
                channel = interact.user.voice.channel
                voice_channel = await channel.connect()
            else:
                await interact.followup.send("Você não está em um canal de voz.", ephemeral=True)
                return

        async with interact.channel.typing():
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            voice_channel.play(player, after=lambda e: print(f'Erro: {e}') if e else None)

        await interact.followup.send(f'Tocando: {player.title}', ephemeral=True)
    
    except Exception as e:
        await interact.followup.send(f'Erro ao tentar tocar a música: {e}', ephemeral=True)

async def carregar_cogs():
    for arquivo in os.listdir('cogs'):
        if arquivo.endswith('.py'):
            await bot.load_extension(f'cogs.{arquivo[:-3]}')


@bot.command()
async def sincronizar(ctx:commands.Context):
    if ctx.author.id == 424351151534768128:
        server = discord.Object(id=1123842079169192016)
        sincs = await bot.tree.sync(guild=server)
        await ctx.reply(f'{len(sincs)} comandos sincronizados')
    else:
        await ctx.reply('Apenas o meu criador pode usar esse comando')

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print('O bot não tem permissão para apagar mensagens')
        except discord.HTTPException as e:
            print(f'Erro ao tentar apagar a mensagem: {e}')
    
    await ctx.send('Desculpe, esse comando não existe. Tente outro comando.', delete_after=3)


bot.run('MTI3ODI0MzUwNTQ1MzY2MjI0Mg.Gyoa4Q.gIix4GNcX0kwSv33JahQVl7HL3hXPNfzYGbV3M')
    