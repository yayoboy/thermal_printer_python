"""
USB Printer Backend
====================

Questo modulo gestisce la stampa via USB raw (comunicazione diretta).

Usa la libreria PyUSB per comunicare direttamente con dispositivi USB
senza passare per driver del sistema operativo.
"""

from typing import Optional, List, Tuple


class USBPrinter:
    """
    Backend per stampare via USB raw.

    Questa classe usa PyUSB per comunicare direttamente con stampanti
    USB tramite bulk transfer.

    Richiede conoscere Vendor ID e Product ID della stampante.
    Puoi trovarli con lsusb (Linux), System Information (Mac), o Device Manager (Windows).

    Esempio:
        >>> # Per stampante Epson (vendor: 0x04b8, product: 0x0e15)
        >>> printer = USBPrinter(0x04b8, 0x0e15)
        >>> printer.print(escpos_commands)
    """

    def __init__(
        self,
        vendor_id: int,
        product_id: int,
        interface: int = 0,
        out_endpoint: int = 0x01
    ):
        """
        Inizializza la connessione USB.

        Args:
            vendor_id (int): Vendor ID del dispositivo USB (es: 0x04b8 per Epson).
                Formato esadecimale con prefisso 0x.

            product_id (int): Product ID del dispositivo USB.
                Formato esadecimale con prefisso 0x.

            interface (int): Numero dell'interfaccia USB (default: 0).
                Solitamente 0 per stampanti semplici.

            out_endpoint (int): Endpoint OUT per inviare dati (default: 0x01).
                Questo è l'indirizzo dove inviare i dati alla stampante.
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface = interface
        self.out_endpoint = out_endpoint
        self.device = None
        self.endpoint = None

    def connect(self) -> bool:
        """
        Trova e apre il dispositivo USB.

        Returns:
            bool: True se la connessione è riuscita, False altrimenti

        Processo:
            1. Cerca il dispositivo con vendor_id:product_id
            2. Configura il dispositivo
            3. Rivendica l'interfaccia
            4. Trova l'endpoint OUT
        """
        try:
            # Importa PyUSB (solo quando serve)
            import usb.core
            import usb.util

            # Cerca il dispositivo USB
            print(f"🔍 Ricerca dispositivo USB {hex(self.vendor_id)}:{hex(self.product_id)}...")

            self.device = usb.core.find(
                idVendor=self.vendor_id,
                idProduct=self.product_id
            )

            if self.device is None:
                print(f"❌ Dispositivo non trovato")
                print(f"\n   Verifica:")
                print(f"   - La stampante è collegata e accesa")
                print(f"   - Vendor ID e Product ID sono corretti")
                print(f"\n   Dispositivi USB disponibili:")
                self._list_usb_devices()
                return False

            print(f"✅ Dispositivo trovato")

            # Su Linux, potrebbe essere necessario detach il kernel driver
            try:
                if self.device.is_kernel_driver_active(self.interface):
                    print(f"   Detaching kernel driver...")
                    self.device.detach_kernel_driver(self.interface)
            except:
                pass  # Non tutti i sistemi hanno questa funzionalità

            # Configura il dispositivo
            try:
                self.device.set_configuration()
            except:
                pass  # Potrebbe essere già configurato

            # Rivendica l'interfaccia
            usb.util.claim_interface(self.device, self.interface)
            print(f"   Interface {self.interface} claimed")

            # Trova l'endpoint OUT (per inviare dati)
            cfg = self.device.get_active_configuration()
            intf = cfg[(self.interface, 0)]

            self.endpoint = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )

            if self.endpoint is None:
                print(f"❌ Endpoint OUT non trovato")
                return False

            print(f"   Endpoint OUT: {hex(self.endpoint.bEndpointAddress)}")
            print(f"✅ Connessione USB stabilita")
            return True

        except ImportError:
            print(f"❌ Errore: PyUSB non installato")
            print(f"   Installa con: pip install pyusb")
            print(f"\n   Nota: Su Windows potrebbe servire anche:")
            print(f"   - libusb: scarica da https://libusb.info/")
            print(f"   - Zadig: per installare driver WinUSB")
            return False

        except Exception as e:
            print(f"❌ Errore connessione USB: {e}")
            print(f"\n   Su Linux, potresti aver bisogno di permessi sudo o")
            print(f"   aggiungere una regola udev per il dispositivo.")
            return False

    def print(self, data: bytes) -> bool:
        """
        Invia i dati alla stampante via USB.

        Args:
            data (bytes): Comandi ESC/POS da inviare

        Returns:
            bool: True se la stampa è riuscita, False altrimenti
        """
        # Se non siamo connessi, prova a connettersi
        if self.device is None or self.endpoint is None:
            if not self.connect():
                return False

        try:
            # Invia i dati in bulk transfer
            print(f"📤 Invio {len(data)} bytes via USB...")

            # PyUSB bulk write
            bytes_written = self.endpoint.write(data)

            print(f"✅ {bytes_written} bytes inviati con successo")
            return True

        except Exception as e:
            print(f"❌ Errore durante l'invio USB: {e}")
            return False

    def close(self):
        """
        Chiude la connessione USB e rilascia l'interfaccia.
        """
        if self.device:
            try:
                import usb.util
                # Rilascia l'interfaccia
                usb.util.release_interface(self.device, self.interface)

                # Riattacca il kernel driver se necessario
                try:
                    self.device.attach_kernel_driver(self.interface)
                except:
                    pass

                print(f"🔌 Connessione USB chiusa")
            except:
                pass
            finally:
                self.device = None
                self.endpoint = None

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
    def list_usb_devices() -> List[Tuple[int, int, str]]:
        """
        Elenca tutti i dispositivi USB connessi.

        Returns:
            list: Lista di tuple (vendor_id, product_id, description)

        Esempio:
            >>> devices = USBPrinter.list_usb_devices()
            >>> for vid, pid, desc in devices:
            ...     print(f"{hex(vid)}:{hex(pid)} - {desc}")
        """
        try:
            import usb.core

            devices = []
            print("🔍 Dispositivi USB connessi:\n")

            # Trova tutti i dispositivi USB
            all_devices = usb.core.find(find_all=True)

            for dev in all_devices:
                try:
                    # Ottieni informazioni sul dispositivo
                    vendor_id = dev.idVendor
                    product_id = dev.idProduct

                    # Prova a ottenere manufacturer e product string
                    try:
                        manufacturer = usb.util.get_string(dev, dev.iManufacturer)
                    except:
                        manufacturer = "Unknown"

                    try:
                        product = usb.util.get_string(dev, dev.iProduct)
                    except:
                        product = "Unknown"

                    desc = f"{manufacturer} {product}".strip()

                    print(f"   📌 {hex(vendor_id)}:{hex(product_id)}")
                    print(f"      {desc}")
                    print()

                    devices.append((vendor_id, product_id, desc))

                except:
                    # Alcuni dispositivi potrebbero dare errore, skippa
                    continue

            if not devices:
                print("   ❌ Nessun dispositivo USB trovato")

            return devices

        except ImportError:
            print("❌ PyUSB non installato. Installa con: pip install pyusb")
            return []

    def _list_usb_devices(self):
        """Versione interna per stampare dispositivi"""
        USBPrinter.list_usb_devices()


if __name__ == "__main__":
    # Test del backend USB
    print("🧪 Test USB Printer Backend\n")

    # Test 1: Lista dispositivi USB
    print("Test 1: Elenco dispositivi USB\n")
    devices = USBPrinter.list_usb_devices()

    # Test 2: Trova stampanti termiche comuni
    print("\nTest 2: Ricerca stampanti termiche comuni\n")

    # Vendor ID comuni per stampanti termiche
    common_vendors = {
        0x04b8: "Epson",
        0x0fe6: "ICS Advent (Star)",
        0x0519: "Star Micronics",
        0x0dd4: "Custom Engineering",
        0x1504: "Citizen",
    }

    print("   Stampanti comuni da cercare:")
    for vid, name in common_vendors.items():
        print(f"   - {hex(vid)}: {name}")

    # Cerca se c'è qualche stampante
    found_printers = []
    for dev_vid, dev_pid, desc in devices:
        if dev_vid in common_vendors:
            print(f"\n   ✅ Possibile stampante trovata:")
            print(f"      Vendor: {common_vendors[dev_vid]}")
            print(f"      ID: {hex(dev_vid)}:{hex(dev_pid)}")
            print(f"      Descrizione: {desc}")
            found_printers.append((dev_vid, dev_pid))

    # Test 3: Connessione (se trovata una stampante)
    if found_printers:
        vid, pid = found_printers[0]
        print(f"\n\nTest 3: Tentativo connessione a {hex(vid)}:{hex(pid)}\n")

        printer = USBPrinter(vid, pid)
        if printer.connect():
            # Comando semplice: ESC @ (init) + newline
            test_data = b'\x1b@\n\n\n'
            printer.print(test_data)
            printer.close()
    else:
        print("\n\n❌ Nessuna stampante termica trovata per test connessione.")
        print("   Verifica che la stampante sia collegata e accesa.")
