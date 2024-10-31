# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "eth-account",
#     "logging",
#     "requests",
#     "rich",
#     "web3",
# ]
# ///

#############################################
# Source - https://github.com/xyizko/xo-wgs #
# Pupose - Testnet ONLY !                   # 
#############################################

# --- Imports ---

import logging
import requests as rq
from rich import print as rprint
from rich.logging import RichHandler
from rich.panel import Panel
from rich.console import Console
from rich.traceback import install
from web3 import Web3
from eth_account import Account
from datetime import datetime

# --- Import Configs ---

# Tracebacks
install(show_locals=True)

# Initialize Console Function
console = Console()

# Configure logging
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger(__name__)

# Initialize Web3 instance (no need to connect to a provider just for generating wallets)
w3 = Web3()


# --- Functions ----


# Banner Function
def banr() -> str:
    """
    Function for grabbing the banner via curl and printing it
    """
    url = "https://snips.sh/f/ZuwtQ3Pk0x?r=1"
    try:
        r = rq.get(url)
        r.raise_for_status()
        banner_text = r.text
        print(banner_text)  # Print the banner to the screen
        return banner_text  # Return the banner text for later use
    except rq.RequestException as e:
        error_message = f"Failed to fetch banner. Error: {str(e)}"
        console.print(f"[bold red]{error_message}[/bold red]")
        return error_message


# Warning Function
def warning() -> None:
    rprint(
        Panel(
            """[bold red]Generating 10 eth wallets strictly for testing purposes (TestNet). [/bold red]""",
            title="[#87ff00][italic]Warning",
            border_style="#d700d7",
        )
    )


# Wallet Generation
def generate_and_save_eth_wallets(num_wallets):
    wallet_data = []

    for _ in range(num_wallets):
        account = Account.create()
        wallet_info = {
            "address": account.address,
            "private_key": account._private_key.hex(),
        }
        wallet_data.append(wallet_info)

    # Generate filename with current date and time
    now = datetime.now()
    filename = f"generated_wallets_{now.strftime('%Y%m%d_%H%M%S')}.txt"

    # Write wallet data to the file
    with open(filename, "w") as file:
        for wallet in wallet_data:
            file.write(f"Address: {wallet['address']}\n")
            file.write(f"Private Key: {wallet['private_key']}\n")
            file.write("\n")

    # Log success message
    logger.info(
        f"[green] Success! {num_wallets} wallets have been generated and saved to {filename}[/green]"
    )
    console.line()
    console.rule("[green]Success![/green]", style="green")


# --- Main Function  ---
def main() -> None:
    print("Hello from w1.py!")
    banr()
    warning()
    generate_and_save_eth_wallets(10)


if __name__ == "__main__":
    main()
