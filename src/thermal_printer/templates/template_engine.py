"""
Motore di Templating con Jinja2
================================

Questo modulo gestisce il rendering dei template HTML usando Jinja2,
che è l'equivalente Python di Nunjucks.
"""

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pathlib import Path
from typing import Dict, Any, Optional
import random
import string


class TemplateEngine:
    """
    Motore per il rendering di template HTML con Jinja2.

    Jinja2 funziona in modo simile a Nunjucks:
    - {{ variabile }} per stampare valori
    - {% if condizione %} per logica condizionale
    - {% for item in lista %} per cicli
    - Filtri: {{ testo|upper }} per trasformazioni

    Esempio:
        >>> engine = TemplateEngine()
        >>> html = engine.render_string("<h1>Ciao {{ nome }}!</h1>", {"nome": "Mario"})
        >>> print(html)
        <h1>Ciao Mario!</h1>
    """

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Inizializza il motore di templating.

        Args:
            templates_dir (str, opzionale): Cartella dove cercare i template.
                Se None, usa solo render_string per template inline.
        """
        self.templates_dir = templates_dir

        # Se abbiamo una cartella template, configuriamo Jinja2 per caricarli da lì
        if templates_dir:
            # Crea l'environment Jinja2 con caricamento da file
            self.env = Environment(
                loader=FileSystemLoader(templates_dir),  # Carica template da questa cartella
                autoescape=select_autoescape(['html', 'xml']),  # Escape automatico per sicurezza
                trim_blocks=True,  # Rimuove spazi bianchi inutili
                lstrip_blocks=True
            )
        else:
            # Crea environment senza loader (solo per stringhe)
            self.env = Environment(
                autoescape=select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )

        # Aggiungi filtri custom (funzioni utilizzabili nei template)
        self._add_custom_filters()

    def _add_custom_filters(self):
        """
        Aggiunge filtri personalizzati ai template.

        I filtri sono funzioni che trasformano i valori nei template.
        Esempio: {{ nome|uppercase }} chiamerà il filtro 'uppercase'
        """

        # Filtro per convertire in maiuscolo
        def uppercase(text: str) -> str:
            """Converte testo in maiuscolo"""
            return str(text).upper()

        # Filtro per convertire in minuscolo
        def lowercase(text: str) -> str:
            """Converte testo in minuscolo"""
            return str(text).lower()

        # Filtro per troncare testo
        def truncate_text(text: str, length: int = 50, suffix: str = "...") -> str:
            """
            Tronca il testo a una lunghezza specifica.

            Args:
                text: Testo da troncare
                length: Lunghezza massima
                suffix: Cosa aggiungere alla fine se troncato
            """
            text = str(text)
            if len(text) <= length:
                return text
            return text[:length].rstrip() + suffix

        # Filtro per formattare numeri
        def format_number(value: float, decimals: int = 2) -> str:
            """
            Formatta un numero con decimali.

            Args:
                value: Numero da formattare
                decimals: Numero di decimali
            """
            return f"{float(value):.{decimals}f}"

        # Registra i filtri nell'environment
        self.env.filters['uppercase'] = uppercase
        self.env.filters['lowercase'] = lowercase
        self.env.filters['truncate'] = truncate_text
        self.env.filters['format_number'] = format_number

    def render_file(self, template_filename: str, data: Dict[str, Any]) -> str:
        """
        Renderizza un template da file.

        Args:
            template_filename (str): Nome del file template (es: 'ricevuta.html')
            data (dict): Dizionario con i dati da passare al template

        Returns:
            str: HTML renderizzato

        Esempio:
            >>> engine = TemplateEngine('templates/')
            >>> html = engine.render_file('ricevuta.html', {'totale': 19.99})
        """
        if not self.templates_dir:
            raise ValueError("templates_dir non specificato. Usa render_string invece.")

        # Carica il template dal file
        template = self.env.get_template(template_filename)

        # Renderizza il template con i dati
        return template.render(**data)

    def render_string(self, template_string: str, data: Dict[str, Any]) -> str:
        """
        Renderizza un template da stringa.

        Args:
            template_string (str): Template HTML come stringa
            data (dict): Dizionario con i dati da passare al template

        Returns:
            str: HTML renderizzato

        Esempio:
            >>> engine = TemplateEngine()
            >>> html = engine.render_string(
            ...     '<p>Ciao {{ nome }}, hai {{ eta }} anni</p>',
            ...     {'nome': 'Luca', 'eta': 25}
            ... )
            >>> print(html)
            <p>Ciao Luca, hai 25 anni</p>
        """
        # Crea template dalla stringa
        template = self.env.from_string(template_string)

        # Renderizza il template con i dati
        return template.render(**data)

    def add_global_variable(self, name: str, value: Any):
        """
        Aggiunge una variabile globale disponibile in tutti i template.

        Args:
            name (str): Nome della variabile
            value: Valore della variabile

        Esempio:
            >>> engine = TemplateEngine()
            >>> engine.add_global_variable('app_name', 'My Thermal Printer')
            >>> # Ora {{ app_name }} sarà disponibile in tutti i template
        """
        self.env.globals[name] = value

    def add_global_function(self, name: str, func: callable):
        """
        Aggiunge una funzione globale chiamabile dai template.

        Args:
            name (str): Nome della funzione
            func (callable): Funzione Python

        Esempio:
            >>> engine = TemplateEngine()
            >>> def dice_roll(sides=6):
            ...     return random.randint(1, sides)
            >>> engine.add_global_function('roll', dice_roll)
            >>> # Ora nei template puoi usare: {{ roll(20) }}
        """
        self.env.globals[name] = func


def create_complete_html(body_html: str, width: int = 384) -> str:
    """
    Crea un documento HTML completo partendo dal contenuto body.

    Aggiunge tutti i tag necessari (DOCTYPE, html, head, body) e il CSS
    di base per il rendering corretto nella stampante.

    Args:
        body_html (str): Contenuto HTML del body
        width (int): Larghezza in pixel della stampante

    Returns:
        str: HTML completo pronto per il rendering

    Esempio:
        >>> html = create_complete_html("<h1>Test</h1>", 384)
        >>> print(html[:50])
        <!DOCTYPE html>
        <html lang="it">
        <head>
    """
    # Template HTML base
    html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stampa Termica</title>
    <style>
        /* Reset CSS per rimuovere margini/padding del browser */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        /* Imposta dimensioni della pagina */
        @page {{
            margin: 0;
            size: {width}px auto;
        }}

        body {{
            margin: 0;
            padding: 10px;
            width: {width}px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            line-height: 1.4;
            color: #000000;
            background: #ffffff;
        }}

        /* Utility classes */
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
        .bold {{ font-weight: bold; }}
        .italic {{ font-style: italic; }}
        .underline {{ text-decoration: underline; }}

        /* Responsive images */
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    {body_html}
</body>
</html>"""

    return html_template


# Funzioni di utilità per template comuni

def generate_random_id(length: int = 8) -> str:
    """
    Genera un ID casuale alfanumerico.

    Args:
        length (int): Lunghezza dell'ID

    Returns:
        str: ID casuale

    Esempio:
        >>> id = generate_random_id(10)
        >>> len(id)
        10
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == "__main__":
    # Test del motore di templating
    print("🧪 Test del Template Engine\n")

    # Test 1: Rendering da stringa
    engine = TemplateEngine()
    html = engine.render_string(
        "<h1>Ciao {{ nome }}!</h1><p>Hai {{ eta }} anni.</p>",
        {"nome": "Mario", "eta": 30}
    )
    print("Test 1 - Rendering semplice:")
    print(html)
    print()

    # Test 2: Uso di filtri
    html = engine.render_string(
        "<p>{{ testo|uppercase }}</p>",
        {"testo": "questo sarà maiuscolo"}
    )
    print("Test 2 - Filtro uppercase:")
    print(html)
    print()

    # Test 3: Ciclo for
    html = engine.render_string(
        """<ul>
        {% for item in lista %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>""",
        {"lista": ["Mele", "Pere", "Banane"]}
    )
    print("Test 3 - Ciclo for:")
    print(html)
    print()

    # Test 4: HTML completo
    html = create_complete_html("<h1>Test Stampante</h1>", 384)
    print("Test 4 - HTML completo (prime 200 caratteri):")
    print(html[:200] + "...")
