import discord
from discord.ext import commands
import json
import os
from discord import app_commands

class Server_Canal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_settings = self.load_channel_settings()  # Carregar configurações ao iniciar o bot

    def load_channel_settings(self):
        """Carrega configurações de canal de um arquivo JSON."""
        if os.path.exists('channel_settings.json'):
            with open('channel_settings.json', 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_channel_settings(self):
        """Salva as configurações de canal em um arquivo JSON."""
        with open('channel_settings.json', 'w') as f:
            json.dump(self.channel_settings, f)

    @app_commands.command(name='set_welcome_channel')
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, interact:discord.Interaction, channel: discord.TextChannel):
        """Define o canal de boas-vindas para o servidor."""
        guild_id = str(interact.guild.id)
        if guild_id not in self.channel_settings:
            self.channel_settings[guild_id] = {}

        self.channel_settings[guild_id]['welcome_channel'] = channel.id
        self.save_channel_settings()
        print(f'O canal de entrada é {channel.name}')
        await interact.response.send_message(f'Canal de boas-vindas definido para {channel.mention}.', ephemeral=True)

    @app_commands.command(name='set_leave_channel')
    @commands.has_permissions(administrator=True)
    async def set_leave_channel(self, interact:discord.Interaction, channel: discord.TextChannel):
        """Define o canal de saída para o servidor."""
        guild_id = str(interact.guild.id)
        if guild_id not in self.channel_settings:
            self.channel_settings[guild_id] = {}

        self.channel_settings[guild_id]['leave_channel'] = channel.id
        self.save_channel_settings()
        print(f'O canal de saída é {channel.name}')
        await interact.response.send_message(f'Canal de saída definido para {channel.mention}.', ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, membro: discord.Member):
        guild_id = str(membro.guild.id)
        welcome_channel_id = self.channel_settings.get(guild_id, {}).get('welcome_channel')

        if welcome_channel_id:
            channel = self.bot.get_channel(welcome_channel_id)
            if channel:
                mensagem = f'Bem-vindo, {membro.name}!!'
                embed = discord.Embed(title=mensagem, description='Aproveite a estadia')
                avatar_url = membro.avatar.url if membro.avatar else discord.Embed.Empty
                embed.set_thumbnail(url=avatar_url)
                await channel.send(embed=embed)
            else:
                print(f"Canal de boas-vindas com ID {welcome_channel_id} não encontrado.")
        else:
            print(f"Canal de boas-vindas não está configurado para o servidor '{membro.guild.name}'.")

    @commands.Cog.listener()
    async def on_member_remove(self, membro: discord.Member):
        guild_id = str(membro.guild.id)
        leave_channel_id = self.channel_settings.get(guild_id, {}).get('leave_channel')

        if leave_channel_id:
            channel = self.bot.get_channel(leave_channel_id)
            if channel:
                mensagem = f'{membro.name} saiu do servidor. Já vai tarde!'
                embed = discord.Embed(title=mensagem)
                embed.set_thumbnail(url=membro.avatar.url if membro.avatar else discord.Embed.Empty)
                await channel.send(embed=embed)
            else:
                print(f"Canal de saída com ID {leave_channel_id} não encontrado.")
        else:
            print(f"Canal de saída não está configurado para o servidor '{membro.guild.name}'.")

async def setup(bot):
    await bot.add_cog(Server_Canal(bot))
