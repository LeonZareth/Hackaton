import discord
from discord.ext import commands
import random
import os

description = '''A bot to educate users on how to prevent climate change.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=':', description=description, intents=intents)

DIRECTORIO_IMAGENES = 'imagenes'

# Preguntas y respuestas para el quiz
QUIZ_QUESTIONS = [
    {
        "question": "¿Cuál es la principal causa del cambio climático?",
        "options": ["A) Uso excesivo de plásticos", "B) Emisiones de gases de efecto invernadero", "C) Deforestación"],
        "answer": "B"
    },
    {
        "question": "¿Qué gas es el mayor contribuyente al efecto invernadero?",
        "options": ["A) Dióxido de carbono (CO2)", "B) Metano (CH4)", "C) Vapor de agua (H2O)"],
        "answer": "A"
    },
    {
        "question": "¿Cuál de las siguientes es una fuente de energía renovable?",
        "options": ["A) Carbón", "B) Energía solar", "C) Gas natural"],
        "answer": "B"
    },
    {
        "question": "¿Qué porcentaje del agua del mundo es potable?",
        "options": ["A) 3%", "B) 10%", "C) 25%"],
        "answer": "A"
    },
    {
        "question": "Cuanto tarda el plastico en degradarce?",
        "options": ["A) 100 a 1000","B) 500 a 5000","C)65 a 75"],
        "answer": "A"
    }
]

@bot.event
async def on_ready():
    print(f'wa desperte (ID: {bot.user.id})')
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
    imagenes = os.listdir(DIRECTORIO_IMAGENES)
    
    if not imagenes:
        await ctx.send('No hay imágenes para enviar.')
        return
    
    imagen = random.choice(imagenes)
    ruta_imagen = os.path.join(DIRECTORIO_IMAGENES, imagen)
    
    await ctx.send("Este es un modo de evitar el cambio climático:")
    await ctx.send(file=discord.File(ruta_imagen))
    print(f'Imagen enviada: {imagen}')

@bot.command(name='climate_quiz')
async def climate_quiz(ctx):
    """Starts a climate change quiz."""
    question = random.choice(QUIZ_QUESTIONS)
    
    options = "\n".join(question["options"])
    await ctx.send(f"{question['question']}\n\n{options}\n\nResponde con la letra correcta.")

    def check(m):
        return m.author == ctx.author and m.content.upper() in ["A", "B", "C"]

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("¡Tiempo agotado! Por favor, inténtalo de nuevo.")
        return
    
    if msg.content.upper() == question["answer"]:
        await ctx.send("¡Correcto! 🎉")
    else:
        await ctx.send(f"Incorrecto. La respuesta correcta es: {question['answer']}.")

bot.run('11111111111111111111111111111')
