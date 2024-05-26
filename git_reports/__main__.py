import typer
import requests
from bs4 import BeautifulSoup
from rich import print
from dotenv import load_dotenv
import os

load_dotenv()
app = typer.Typer()

class DolarScrapper:
    """
    Scrap dollar buy and sell values from the provider URL
    """
    def __init__(self,url) -> None:
        self.url = url

    def scrape_dolar_values(self) -> tuple[float, float]:
        try:
            page = requests.get(self.url)
            page.raise_for_status()
            soup = BeautifulSoup(page.content, 'html.parser')
            dolar_values = soup.find_all("div", class_="val")
            compra = int(dolar_values[0].get_text()[1:])
            venta = int(dolar_values[1].get_text()[1:])
            return compra, venta
        except (requests.RequestException, ValueError, IndexError) as e:
            print(f"Error al obtener los valores del dólar: {e}")
            return None, None

    def find_middle_number(self, number1:float, number2: float) -> float:
        """
        Returns the middle value between two numbers.
        """
        return (number1 + number2) / 2

scraper = DolarScrapper(os.getenv("DOLAR_URL"))

compra,venta = scraper.scrape_dolar_values()



@app.command()
def get_blue_price():
    """
    Displays the current blue dollar price.
    """
    if compra is not None and venta is not None:
        promedio = scraper.find_middle_number(compra, venta)
        print(f"El precio del dólar blue actual es: [bold blue]${promedio:.2f}[/bold blue]")
    else:
        print("No se puede obtener el valor del dolar.")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()