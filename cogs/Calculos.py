import discord 
from discord.ext import commands
from discord import app_commands

class Calculos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    @app_commands.command(description='Comando para somar dois números')
    async def somar(self, interact:discord.Interaction, n1:float, n2:float):
        resultado = n1 + n2
        await interact.response.send_message(f'{resultado:.2f}')
    
    @app_commands.command(description='Comando para subtrair dois números')
    async def sub(self, interact:discord.Interaction, n1:float, n2:float):
        resultado = n1 - n2
        await interact.response.send_message(f'{resultado:.2f}')
    
    @app_commands.command(description='Comando para multiplicar dois números')
    async def mult(self, interact:discord.Interaction, n1:float, n2:float):
        resultado = n1 * n2
        await interact.response.send_message(f'{resultado:.2f}')
    
    @app_commands.command(description='Comando para dividir dois números')
    async def div(self, interact:discord.Interaction, n1:float, n2:float):
        if n2 == 0:
            await interact.response.send_message('Não existe divisao por 0')
        resultado = n1 / n2
        await interact.response.send_message(f'{resultado:.2f}')
    
   
        
        
      


async def setup(bot):
    await bot.add_cog(Calculos(bot))
    