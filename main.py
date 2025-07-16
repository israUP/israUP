import discord
from discord import app_commands
from discord.ui import View, Select
import os
from dotenv import load_dotenv

# --- CONFIGURAÇÃO INICIAL ---
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID'))) # Coloque o ID do seu servidor no .env

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)

intents = discord.Intents.default()
client = MyClient(intents=intents)

# --- LÓGICA DO BOT ---

# View que contém o menu de seleção
class ElojobSetupView(View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout None para a view ser persistente

    @discord.ui.select(
        placeholder="Selecione um jogo ou serviço",
        custom_id="game_select",
        options=[
            discord.SelectOption(label="Valorant", emoji="<:valorant:12345>", value="valorant"), # Placeholder de emoji
            discord.SelectOption(label="Fortnite", emoji="<:fortnite:12345>", value="fortnite"),
            discord.SelectOption(label="Rainbow Six Siege X", emoji="<:r6:12345>", value="r6"),
            discord.SelectOption(label="Clash Royale", emoji="<:cr:12345>", value="clash_royale"),
            discord.SelectOption(label="Old School RuneScape", emoji="<:osrs:12345>", value="osrs"),
            discord.SelectOption(label="Call of Duty", emoji="<:cod:12345>", value="cod"),
            discord.SelectOption(label="Rocket League", emoji="<:rl:12345>", value="rocket_league"),
            discord.SelectOption(label="Roblox", emoji="<:roblox:12345>", value="roblox"),
            discord.SelectOption(label="League of Legends", emoji="<:lol:12345>", value="lol"),
            discord.SelectOption(label="EA Sports FC", emoji="<:fc:12345>", value="ea_fc"),
            discord.SelectOption(label="Marvel Rivals", emoji="<:mr:12345>", value="marvel_rivals"),
            discord.SelectOption(label="Apex Legends", emoji="<:apex:12345>", value="apex"),
            discord.SelectOption(label="Brawl Stars", emoji="<:brawl:12345>", value="brawl_stars"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: Select):
        # Esta é a função que será chamada quando o usuário escolher um jogo
        # O próximo passo será implementado aqui
        jogo_selecionado = select.values[0]
        await interaction.response.send_message(f"Você selecionou {jogo_selecionado}. Agora vamos pedir os ranks...", ephemeral=True)


# Comando para iniciar o painel
@client.tree.command(name="setupelojobb", description="Configura o painel de vendas de Elojob no canal.")
@app_commands.checks.has_permissions(administrator=True) # Só admins podem usar
async def setupelojobb(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✨ Bem-vindo(a) à IsraBuy!",
        description="Pronto para a melhor experiência de compra?\n\nSelecione um jogo ou serviço no menu abaixo para abrir um ticket ou clique no botão para ver todos os preços.",
        color=discord.Color.purple()
    )
    
    view = ElojobSetupView()
    
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("Painel de Elojob configurado!", ephemeral=True)


@client.event
async def on_ready():
    print(f'Bot {client.user} está online e pronto!')
# iniciando o bot

client.run(TOKEN)
