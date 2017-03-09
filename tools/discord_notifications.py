import discord
import asyncio

from private import TOKEN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Initializing bot")
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
def main():
    
    print("Starting client...")
    client.run(TOKEN)


if __name__ == "__main__":
    main()
