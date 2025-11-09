"""
Network Printer Backend
========================

Questo modulo gestisce la stampa via rete TCP/IP.

Molte stampanti termiche moderne hanno una porta Ethernet o WiFi
e accettano connessioni TCP sulla porta 9100 (protocollo RAW/JetDirect).
"""

import socket
from typing import Optional


class NetworkPrinter:
    """
    Backend per stampare via rete TCP/IP.

    Questa classe invia i comandi ESC/POS alla stampante
    tramite una connessione TCP socket.

    Esempio:
        >>> printer = NetworkPrinter('192.168.1.100', 9100)
        >>> printer.print(escpos_commands)
        >>> printer.close()
    """

    def __init__(self, host: str, port: int = 9100, timeout: float = 10.0):
        """
        Inizializza la connessione di rete.

        Args:
            host (str): Indirizzo IP o hostname della stampante.
                Esempio: '192.168.1.100' o 'printer.local'

            port (int): Porta TCP (default: 9100).
                9100 è la porta standard per stampanti di rete (RAW/JetDirect)

            timeout (float): Timeout in secondi per la connessione.
                Se la stampante non risponde entro questo tempo, genera errore.
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None

    def connect(self) -> bool:
        """
        Stabilisce la connessione con la stampante.

        Returns:
            bool: True se la connessione è riuscita, False altrimenti

        Processo:
            1. Crea un socket TCP
            2. Imposta il timeout
            3. Tenta la connessione all'indirizzo host:port
        """
        try:
            # Crea un socket TCP/IP
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Imposta timeout per evitare di rimanere bloccati
            self.socket.settimeout(self.timeout)

            # Connetti alla stampante
            print(f"🔌 Connessione a {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))

            print(f"✅ Connesso a {self.host}:{self.port}")
            return True

        except socket.timeout:
            print(f"❌ Errore: Timeout connessione a {self.host}:{self.port}")
            print(f"   La stampante non risponde entro {self.timeout} secondi.")
            return False

        except socket.error as e:
            print(f"❌ Errore di connessione: {e}")
            print(f"   Verifica che:")
            print(f"   - La stampante sia accesa")
            print(f"   - L'indirizzo IP sia corretto")
            print(f"   - La stampante sia sulla stessa rete")
            return False

        except Exception as e:
            print(f"❌ Errore imprevisto: {e}")
            return False

    def print(self, data: bytes) -> bool:
        """
        Invia i dati alla stampante.

        Args:
            data (bytes): Comandi ESC/POS da inviare

        Returns:
            bool: True se la stampa è riuscita, False altrimenti

        Processo:
            1. Connette alla stampante (se non già connesso)
            2. Invia tutti i byte dei comandi
            3. Attende conferma (opzionale)
        """
        # Se non siamo connessi, prova a connettersi
        if self.socket is None:
            if not self.connect():
                return False

        try:
            # Invia i dati
            print(f"📤 Invio {len(data)} bytes alla stampante...")
            self.socket.sendall(data)

            print(f"✅ Dati inviati con successo")
            return True

        except socket.error as e:
            print(f"❌ Errore durante l'invio: {e}")
            return False

        except Exception as e:
            print(f"❌ Errore imprevisto: {e}")
            return False

    def close(self):
        """
        Chiude la connessione con la stampante.

        È importante chiamare sempre questo metodo quando hai finito
        di usare la stampante, per rilasciare la connessione.
        """
        if self.socket:
            try:
                self.socket.close()
                print(f"🔌 Disconnesso da {self.host}:{self.port}")
            except:
                pass
            finally:
                self.socket = None

    def __enter__(self):
        """
        Supporto per context manager (with statement).

        Permette di usare:
            with NetworkPrinter('192.168.1.100') as printer:
                printer.print(data)
            # Chiude automaticamente
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Chiusura automatica quando si esce dal context manager"""
        self.close()

    def __del__(self):
        """Chiude la connessione quando l'oggetto viene distrutto"""
        self.close()

    @staticmethod
    def discover_printers(timeout: float = 2.0) -> list:
        """
        Tenta di scoprire stampanti sulla rete locale.

        Nota: Questo è un metodo semplificato che prova indirizzi comuni.
        Per discovery più sofisticato, usa protocolli come mDNS/Bonjour.

        Args:
            timeout (float): Timeout per ogni tentativo di connessione

        Returns:
            list: Lista di tuple (host, port) delle stampanti trovate

        Esempio:
            >>> printers = NetworkPrinter.discover_printers()
            >>> for host, port in printers:
            ...     print(f"Trovata stampante: {host}:{port}")
        """
        found_printers = []

        # Ottieni l'indirizzo IP locale
        try:
            # Trucco per ottenere l'IP locale senza connettersi davvero
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()

            # Estrai la subnet (es: 192.168.1.x)
            ip_parts = local_ip.split('.')
            subnet = '.'.join(ip_parts[:3])

            print(f"🔍 Ricerca stampanti sulla subnet {subnet}.x...")

            # Prova gli indirizzi più comuni
            common_addresses = [
                f"{subnet}.100",  # Spesso le stampanti hanno IP fissi tipo .100
                f"{subnet}.101",
                f"{subnet}.200",
                f"{subnet}.201",
            ]

            for host in common_addresses:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    result = sock.connect_ex((host, 9100))
                    sock.close()

                    if result == 0:
                        print(f"   ✅ Trovata: {host}:9100")
                        found_printers.append((host, 9100))

                except:
                    pass

        except Exception as e:
            print(f"❌ Errore durante discovery: {e}")

        if not found_printers:
            print(f"   ❌ Nessuna stampante trovata")

        return found_printers


if __name__ == "__main__":
    # Test del backend di rete
    print("🧪 Test Network Printer Backend\n")

    # Nota: Cambia questo indirizzo con quello della tua stampante!
    TEST_HOST = "192.168.1.100"
    TEST_PORT = 9100

    print(f"Test connessione a {TEST_HOST}:{TEST_PORT}")
    print("(Cambia l'indirizzo nel codice se hai una stampante diversa)\n")

    # Test 1: Discovery
    print("Test 1: Discovery stampanti")
    printers = NetworkPrinter.discover_printers(timeout=1.0)
    print()

    # Test 2: Connessione
    if printers:
        host, port = printers[0]
        print(f"Test 2: Connessione alla prima stampante trovata ({host}:{port})")

        with NetworkPrinter(host, port) as printer:
            # Comando semplice: ESC @ (init) + newline
            test_data = b'\x1b@\n\n\n'
            printer.print(test_data)
    else:
        print("Nessuna stampante trovata per il test di connessione.")
