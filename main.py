import discord
import requests
import asyncio
from discord.ext import commands, tasks
from discord import app_commands
import yt_dlp as youtube_dl

# ID server discord
GUILD_ID = 1166227158805516400 


intents = discord.Intents.default()
intents.message_content = True 

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, intents=intents)
        self.loop_mode = False  
        self.current_song = None 

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"✅ Slash commands synced in guild: {GUILD_ID}")

    async def on_ready(self):
        print(f'✅ Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send(f'Halo {message.author} apa kabar')

        if message.content.startswith('$baik'):
            await message.channel.send(f'Semoga {message.author} selalu diberi kesehatan oleh Tuhan Yang Maha Kuasa')

        if message.content.startswith('$sombong lu byan'):
            await message.channel.send(f'Apalah')

        if message.content.startswith('$roblox'):
            await message.channel.send(f'Gas mabar')

        if message.content.startswith('$hero favorit'):
            await message.channel.send(f'Harith') 

        if message.content.startswith('$parah lu byan'):
            await message.channel.send(f'Apalah si {message.author}')    
            ///////////////////////////////////

            
    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            await reaction.message.channel.send('wkwkwkwk')


client = MyClient()

    
# FFMPEG Options
FFMPEG_OPTIONS = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

#Bagian setel musik
def search_youtube(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            return info['url']
        except Exception as e:
            print(f"Error: {e}")
            return None

@client.tree.command(name="join", description="Bot masuk ke voice channel")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await channel.connect()
            await interaction.response.send_message(f"✅ Bergabung ke {channel}")
        else:
            await interaction.response.send_message("❌ Bot sudah ada di voice channel!")
    else:
        await interaction.response.send_message("❌ Kamu harus berada di voice channel dulu!")

@client.tree.command(name="play", description="Putar musik dari YouTube")
@app_commands.describe(query="Judul atau URL YouTube")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()  # Mencegah interaksi kadaluarsa

    if interaction.guild.voice_client is None:
        await interaction.followup.send("❌ Bot belum join ke voice channel. Gunakan `/join` terlebih dahulu.")
        return

    url = search_youtube(query)
    if url is None:
        await interaction.followup.send("❌ Gagal mencari lagu!")
        return

    voice_client = interaction.guild.voice_client

    def after_playing(error):
        if error is None and client.loop_mode:
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            voice_client.play(discord.FFmpegPCMAudio(client.current_song, **ffmpeg_options), after=after_playing)

    if not voice_client.is_playing():
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        client.current_song = url
        voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=after_playing)
        await interaction.followup.send(f"🎶 Memutar: {query}")
    else:
        await interaction.followup.send("❌ Bot sedang memutar musik lain. Gunakan `/stop` terlebih dahulu.")


@client.tree.command(name="loop", description="Aktifkan/nonaktifkan mode loop")
async def loop(interaction: discord.Interaction):
    client.loop_mode = not client.loop_mode
    status = "AKTIF" if client.loop_mode else "NONAKTIF"
    await interaction.response.send_message(f"🔁 Mode loop: {status}")

@client.tree.command(name="stop", description="Hentikan musik yang sedang diputar")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        client.loop_mode = False
        voice_client.stop()
        await interaction.response.send_message("⏹ Musik dihentikan.")
    else:
        await interaction.response.send_message("❌ Tidak ada musik yang sedang diputar.")

@client.tree.command(name="leave", description="Bot keluar dari voice channel")
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        client.loop_mode = False
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 Keluar dari voice channel.")
    else:
        await interaction.response.send_message("❌ Bot tidak ada di voice channel!")


# Slash Command (/)
@client.tree.command(name="hello", description="Say hello")
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Halo bro")

@client.tree.command(name="mabar", description="Ajak mabar")
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Ayo kita mabar bro")

@client.tree.command(name="ucup", description="sapa ucup")
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Ucup sigma")

@client.tree.command(name="imanuel", description="menghentikan imanuel")
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("CUKUP IMANUEL")

@client.tree.command(name="kucai", description="anak kucai")
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("TOHAPOK KAU ANAK KUCAI")   


# Tanda kalau bot sudah aktif
@client.event
async def on_ready():
    print(f'✅ Bot telah login sebagai {client.user}')


client.run('TOKEN')
