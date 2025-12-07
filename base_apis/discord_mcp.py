import os
import sys
import subprocess
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

class DiscordAPI:
    def __init__(self):
        """
        Initialize Discord API client.
        Requires DISCORD_BOT_TOKEN in environment variables.
        """
        self.token = os.getenv('DISCORD_BOT_TOKEN')
        self.base_url = "https://discord.com/api/v10"
        
        if not self.token:
            print("Warning: DISCORD_BOT_TOKEN not found in environment variables.")

    def _get_headers(self):
        return {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/SivaNithishKumar/socials-mcp, 1.0)"
        }

    def send_message(self, channel_id: str, content: str) -> dict:
        """
        Send a message to a specific channel.
        """
        if not self.token:
            return {"error": "DISCORD_BOT_TOKEN not configured"}
            
        url = f"{self.base_url}/channels/{channel_id}/messages"
        payload = {"content": content}
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg = f"HTTP {e.response.status_code}: {e.response.json()}"
                except:
                    error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            return {"error": error_msg}

    def get_channel(self, channel_id: str) -> dict:
        """
        Get details about a channel.
        """
        if not self.token:
            return {"error": "DISCORD_BOT_TOKEN not configured"}

        url = f"{self.base_url}/channels/{channel_id}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_guild(self, guild_id: str) -> dict:
        """
        Get details about a guild (server).
        """
        if not self.token:
            return {"error": "DISCORD_BOT_TOKEN not configured"}

        url = f"{self.base_url}/guilds/{guild_id}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                 return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
            return {"error": str(e)}

    def get_guild_channels(self, guild_id: str) -> list | dict:
        """
        Get all channels in a guild.
        """
        if not self.token:
            return {"error": "DISCORD_BOT_TOKEN not configured"}

        url = f"{self.base_url}/guilds/{guild_id}/channels"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                 return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
            return {"error": str(e)}

    def run_bot(self):
        """
        Run the bot in persistent mode (WebSocket/Gateway) to appear Online.
        """
        try:
            import discord
        except ImportError:
            print("Error: discord.py is not installed. Please run 'pip install discord.py'")
            return

        if not self.token:
            print("Error: DISCORD_BOT_TOKEN not configured")
            return

        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'Logged in as {client.user} (Online!)')
            print('Press Ctrl+C to stop.')

        try:
            client.run(self.token)
        except Exception as e:
            print(f"Error running bot: {e}")

# --- MCP Server Setup ---

# Initialize FastMCP server
mcp = FastMCP("discord")

# Global Discord API instance
discord_client = None

def get_discord_client():
    """Get or create Discord client instance."""
    global discord_client
    if discord_client is None:
        discord_client = DiscordAPI()
    return discord_client

@mcp.tool()
async def send_discord_message(channel_id: str, message: str) -> str:
    """Send a message to a Discord channel.

    Args:
        channel_id: The ID of the Discord channel to send to.
        message: The content of the message to send.
    """
    try:
        client = get_discord_client()
        result = client.send_message(channel_id, message)
        
        if "error" in result:
            return f"Error sending message: {result['error']}"
        
        return f"""
Message sent successfully!
Message ID: {result.get('id')}
Channel ID: {result.get('channel_id')}
Content: {result.get('content')}
"""
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def get_discord_channel_info(channel_id: str) -> str:
    """Get information about a specific Discord channel.

    Args:
        channel_id: The ID of the Discord channel.
    """
    try:
        client = get_discord_client()
        result = client.get_channel(channel_id)
        
        if "error" in result:
            return f"Error fetching channel: {result['error']}"
            
        return f"""
Channel Info:
Name: {result.get('name')}
ID: {result.get('id')}
Type: {result.get('type')}
Guild ID: {result.get('guild_id')}
Topic: {result.get('topic', 'None')}
"""
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def get_discord_guild_info(guild_id: str) -> str:
    """Get information about a specific Discord Guild (Server).

    Args:
        guild_id: The ID of the Discord guild/server.
    """
    try:
        client = get_discord_client()
        result = client.get_guild(guild_id)
        
        if "error" in result:
            return f"Error fetching guild: {result['error']}"
            
        return f"""
Guild Info:
Name: {result.get('name')}
ID: {result.get('id')}
Owner ID: {result.get('owner_id')}
Region: {result.get('region', 'Unknown')}
Description: {result.get('description', 'None')}
"""
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def list_discord_channels(guild_id: str) -> str:
    """List all channels in a specific Discord Guild (Server).

    Args:
        guild_id: The ID of the Discord guild/server.
    """
    try:
        client = get_discord_client()
        result = client.get_guild_channels(guild_id)
        
        if isinstance(result, dict) and "error" in result:
             return f"Error fetching channels: {result['error']}"
        
        if not result or not isinstance(result, list):
            return "No channels found or invalid response."

        # Filter and format
        formatted = "Channels:\n"
        # Sort by type (Category=4, Text=0, Voice=2) then position
        result.sort(key=lambda x: (x.get('type', 99), x.get('position', 0)))
        
        for ch in result:
            c_type = ch.get('type')
            type_str = "Unknown"
            if c_type == 0: type_str = "Text"
            elif c_type == 2: type_str = "Voice"
            elif c_type == 4: type_str = "Category"
            
            formatted += f"- {ch.get('name')} (ID: {ch.get('id')}) [{type_str}]\n"
            
        return formatted

    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def app_discord_status_online() -> str:
    """Start the Discord bot process in the background.
    
    This will make the bot appear "Online" in Discord.
    The process runs independently.
    """
    try:
        # Launch THIS file with the --run-bot argument in a separate process
        script_path = os.path.abspath(__file__)
        
        subprocess.Popen(
            [sys.executable, script_path, "--run-bot"],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0,
            close_fds=True
        )
        
        return "Bot started in background! It should appear Online in a few seconds."
    except Exception as e:
        return f"Failed to start bot process: {str(e)}"

if __name__ == "__main__":
    # Check for --run-bot flag to run as standalone bot
    if "--run-bot" in sys.argv:
        api = DiscordAPI()
        api.run_bot()
    else:
        # Otherwise run as MCP server
        mcp.run(transport='stdio')
