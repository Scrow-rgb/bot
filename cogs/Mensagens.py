import discord 
from discord.ext import commands
from discord import app_commands


class Mensagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
  
    
    @app_commands.command(description='Esse comando é uma saudação')
    async def ola(self ,interact:discord.Interaction):
         await interact.response.send_message(f'Olá, {interact.user.name}', ephemeral=True ,delete_after=5)
    
    @app_commands.command(description= 'Esse comando envia uma mensagem contendo a frase que o usuário escreveu' )
    async def escrever(self, interact:discord.Interaction, frase:str):
        await interact.response.send_message(frase)
    
    @app_commands.command(description='Apaga mensagem')
    async def clear(self, interact:discord.Interaction, amount:int = 100):
        """"Apaga mensagens no canal atual."""
        if amount > 100:
            await interact.response.send_message('Você não pode apagar mais de 100 mensagens de uma vez', ephemeral=True, delete_after=2)
            return 
            
       
        messages = [message async for message in interact.channel.history(limit=amount + 1)]
        
            
        if not messages:
                await interact.response.send_message('Não há mensagens para apagar', ephemeral=True, delete_after=2)
                return
            
        await interact.response.send_message(F'Apagando mensagens...', ephemeral=True, delete_after=2)
        
        deleted = await interact.channel.purge(limit=amount)
        
        await interact.channel.send(f'{len(deleted)} mensagens apagadas', delete_after=2)


async def setup(bot):
    await bot.add_cog(Mensagens(bot))
    