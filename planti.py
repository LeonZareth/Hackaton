import discord
from discord.ext import commands
import random
import os

description = '''An example bot to showcase the discord.ext.commands extension module.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

# Directorio donde se encuentran las imágenes
DIRECTORIO_IMAGENES = 'imagenes'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool."""
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')
@bot.command(name='como_evitar_el_cambio_climatico')
async def random_image(ctx):
    """Sends a random image from the images directory."""
    # Obtener la lista de archivos en el directorio de imágenes
    imagenes = os.listdir(DIRECTORIO_IMAGENES)
    
    if not imagenes:
        await ctx.send('No hay imágenes para enviar.')
        return
    
    # Seleccionar una imagen al azar
    imagen = random.choice(imagenes)
    ruta_imagen = os.path.join(DIRECTORIO_IMAGENES, imagen)
    
    # Enviar la imagen
    await ctx.send("este es un modo de evitar el cambio climatico")
    await ctx.send(file=discord.File(ruta_imagen))
    print(f'Imagen enviada: {imagen}')

bot.run('token')