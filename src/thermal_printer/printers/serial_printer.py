"""
Serial Printer Backend
=======================

Questo modulo gestisce la stampa via porta seriale (RS232/USB-Serial).

Molte stampanti termiche si collegano via cavo USB che emula
una porta seriale (COM su Windows, /dev/ttyUSB su Linux).
"""

from typing import Optional


class SerialPrinter:
    """
    Backend per stampare via porta seriale.

    Questa classe usa pyserial per comunicare con stampanti
    collegate tramite porta seriale o adattatore USB-Seriale.

    Esempio Windows:
        >>> printer = SerialPrinter('COM3')
        >>> printer.print(escpos_commands)

    Esempio Linux/Mac:
        >>> printer = SerialPrinter('/dev/ttyUSB0')
        >>> printer.print(escpos_commands)
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        timeout: float = 5.0,
        bytesize: int = 8,
        parity: str = 'N',
        stopbits: int = 1
    ):
        """
        Inizializza la connessione seriale.

        Args:
            port (str): Porta seriale da usare.
                - Windows: 'COM1', 'COM3', etc.
                - Linux: '/dev/ttyUSB0', '/dev/ttyACM0', etc.
                - Mac: '/dev/cu.usbserial', etc.

            baudrate (int): Velocità di comunicazione (default: 9600).
                Valori comuni: 9600, 19200, 38400, 57600, 115200.
                Verifica sul manuale della tua stampante.

            timeout (float): Timeout in secondi per lettura/scrittura.

            bytesize (int): Numero di bit per byte (default: 8).
                Quasi sempre 8, raramente 7.

            parity (str): Controllo di parità (default: 'N' = None).
                Opzioni: 'N' (None), 'E' (Even), 'O' (Odd)

            stopbits (int): Bit di stop (default: 1).
                Opzioni: 1, 1.5, 2
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.serial = None

    def connect(self) -> bool:
        """
        Apre la connessione seriale.

        Returns:
            bool: True se la connessione è riuscita, False altrimenti
        """
        try:
            # Importa pyserial (solo quando serve)
            import serial

            # Converti parametri nel formato pyserial
            parity_map = {
                'N': serial.PARITY_NONE,
                'E': serial.PARITY_EVEN,
                'O': serial.PARITY_ODD,
                'M': serial.PARITY_MARK,
                'S': serial.PARITY_SPACE
            }

            stopbits_map = {
                1: serial.STOPBITS_ONE,
                1.5: serial.STOPBITS_ONE_POINT_FIVE,
                2: serial.STOPBITS_TWO
            }

            # Crea connessione seriale
            print(f"🔌 Apertura porta {self.port} a {self.baudrate} baud...")
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=parity_map.get(self.parity, serial.PARITY_NONE),
                stopbits=stopbits_map.get(self.stopbits, serial.STOPBITS_ONE),
                timeout=self.timeout
            )

            print(f"✅ Porta {self.port} aperta con successo")
            return True

        except ImportError:
            print(f"❌ Errore: pyserial non installato")
            print(f"   Installa con: pip install pyserial")
            return False

        except Exception as e:
            print(f"❌ Errore apertura porta {self.port}: {e}")
            print(f"\n   Possibili cause:")
            print(f"   - Porta non esistente (verifica il nome)")
            print(f"   - Porta già in uso da altro programma")
            print(f"   - Permessi insufficienti (prova come amministratore)")
            print(f"\n   Porte disponibili:")
            try:
                import serial.tools.list_ports
                ports = serial.tools.list_ports.comports()
                for p in ports:
                    print(f"   - {p.device}: {p.description}")
            except:
                pass

            return False

    def print(self, data: bytes) -> bool:
        """
        Invia i dati alla stampante.

        Args:
            data (bytes): Comandi ESC/POS da inviare

        Returns:
            bool: True se la stampa è riuscita, False altrimenti
        """
        # Se non siamo connessi, prova a connettersi
        if self.serial is None or not self.serial.is_open:
            if not self.connect():
                return False

        try:
            # Invia i dati
            print(f"📤 Invio {len(data)} bytes alla stampante...")
            bytes_written = self.serial.write(data)

            # Assicurati che tutti i dati siano inviati
            self.serial.flush()

            print(f"✅ {bytes_written} bytes inviati con successo")
            return True

        except Exception as e:
            print(f"❌ Errore durante l'invio: {e}")
            return False

    def close(self):
        """
        Chiude la connessione seriale.

        È importante chiamare sempre questo metodo quando hai finito,
        altrimenti la porta rimane bloccata.
        """
        if self.serial and self.serial.is_open:
            try:
                self.serial.close()
                print(f"🔌 Porta {self.port} chiusa")
            except:
                pass
            finally:
                self.serial = None

    def __enter__(self):
        """Supporto per context manager (with statement)"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Chiusura automatica quando si esce dal context manager"""
        self.close()

    def __del__(self):
        """Chiude la connessione quando l'oggetto viene distrutto"""
        self.close()

    @staticmethod
    def list_available_ports():
        """
        Elenca tutte le porte seriali disponibili sul sistema.

        Returns:
            list: Lista di porte seriali disponibili

        Esempio:
            >>> ports = SerialPrinter.list_available_ports()
            >>> for port in ports:
            ...     print(f"Porta: {port.device} - {port.description}")
        """
        try:
            import serial.tools.list_ports

            ports = serial.tools.list_ports.comports()

            print("🔍 Porte seriali disponibili:\n")

            if not ports:
                print("   ❌ Nessuna porta seriale trovata")
                return []

            for p in ports:
                print(f"   📌 {p.device}")
                print(f"      Descrizione: {p.description}")
                print(f"      Hardware ID: {p.hwid}")
                print()

            return ports

        except ImportError:
            print("❌ pyserial non installato. Installa con: pip install pyserial")
            return []


if __name__ == "__main__":
    # Test del backend seriale
    print("🧪 Test Serial Printer Backend\n")

    # Test 1: Lista porte disponibili
    print("Test 1: Elenco porte seriali\n")
    ports = SerialPrinter.list_available_ports()

    # Test 2: Connessione (se ci sono porte disponibili)
    if ports:
        first_port = ports[0].device
        print(f"\nTest 2: Connessione alla porta {first_port}\n")

        printer = SerialPrinter(first_port, baudrate=9600)

        if printer.connect():
            # Comando semplice: ESC @ (init) + newline
            test_data = b'\x1b@\n\n\n'
            printer.print(test_data)
            printer.close()
    else:
        print("\nNessuna porta seriale disponibile per il test di connessione.")
