import discord 
from discord.ext import commands
from discord import app_commands




class Server_Canal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__
    
    @commands.Cog.listener()
    async def on_member_join(self, membro: discord.Member):
        # Verifica se o membro é um bot
        if membro.bot:
            # Lista todos os cargos disponíveis para depuração
            print(f"Lista de cargos no servidor '{membro.guild.name}':")
            for r in membro.guild.roles:
                print(f"- {r.name} (ID: {r.id})")

            # Tenta encontrar o cargo "BOT"
            role = discord.utils.get(membro.guild.roles, name='BOT')

            if role is None:
                print(f"Erro: Cargo 'BOT' não encontrado no servidor '{membro.guild.name}' (ID: {membro.guild.id})")
            else:
                try:
                    await membro.add_roles(role)
                    print(f"Cargo '{role.name}' atribuído ao bot {membro.name}.")
                except discord.Forbidden:
                    print(f"Erro: O bot não tem permissão para atribuir o cargo '{role.name}' ao bot {membro.name}.")
                except Exception as e:
                    print(f"Erro inesperado ao tentar atribuir o cargo: {e}")
                    
             #Verifica se o membro não é um bot e tenta atribuir o cargo 'membro'
        else:
            role = discord.utils.get(membro.guild.roles, name='membro')
            
            if role is None:
                print(f"Erro: Cargo 'membro' não encontrado no servidor '{membro.guild.name}' (ID: {membro.guild.id})")
            else:
                try:
                    await membro.add_roles(role)
                    print(f"Cargo '{role.name}' atribuído ao membro {membro.name}.")
                except discord.Forbidden:
                    print(f"Erro: O bot não tem permissão para atribuir o cargo '{role.name}' ao membro {membro.name}.")
                except Exception as e:
                    print(f"Erro inesperado ao tentar atribuir o cargo: {e}")


        # Mapeamento de guilda para canais específicos
        guild_channel_map = {
            1123842079169192016: 1278099632974463088,  # Guild 1 -> Canal 1
            876497016904118342: 876499665682567199,    # Guild 2 -> Canal 2
            858532031855853578: 1278411121954390068,   # Guild 3 -> Canal 3
        }

        # Mensagem de boas-vindas
        mensagem = f'Bem-vindo, {membro.name}!!'

        # Obtém o ID da guild (servidor) onde o evento ocorreu
        guild_id = membro.guild.id

        # Verifica se o servidor está no mapeamento e obtém o canal correspondente
        if guild_id in guild_channel_map:
            channel_id = guild_channel_map[guild_id]
            canal = self.bot.get_channel(channel_id)

            if canal:
                embed = discord.Embed(title=mensagem, description='Aproveite a estadia')
                avatar_url = membro.avatar.url if membro.avatar else discord.Embed.Empty
                embed.set_thumbnail(url=avatar_url)
                await canal.send(embed=embed)
            else:
                print(f"Canal com ID {channel_id} não encontrado.")
        else:
            print(f"Guild com ID {guild_id} não está no mapeamento.")
        
    
    @commands.Cog.listener()
    async def on_member_remove(self, membro:discord.Member):
        
        guild_channel_map = {
            1123842079169192016: 1278099648401113139, # Guild 1 -> Canal 1
            876497016904118342: 876499665682567199,   # Guild 2 -> Canal 2
            858532031855853578: 1278413819168686192,  # Guild 3 -> Canal 3
        }
        mensagem = f'{membro.name} Saiu do servidor\nJá vai tarde otário!!'
        # Obtém o ID da guild (servidor) onde o evento ocorreu
        guild_id = membro.guild.id
        
         # Verifica se o servidor está no mapeamento
        if guild_id in guild_channel_map:
            channel_id = guild_channel_map[guild_id]
            canal = self.bot.get_channel(channel_id)
        
        if canal:
                embed = discord.Embed(title=mensagem)
                embed.set_thumbnail(url=membro.avatar.url if membro.avatar else discord.Embed.Empty)
                await canal.send(embed=embed)
    
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, canal:discord.abc.GuildChannel):
        await canal.send(f'Novo canal criado: {canal.name}')
        
    
async def setup(bot):
    await bot.add_cog(Server_Canal(bot))