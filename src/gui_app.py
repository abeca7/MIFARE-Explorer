from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMenu, QMessageBox, QLineEdit, QWidgetAction, QToolButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QDialog, QTextEdit, QInputDialog, QGridLayout
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap, QGuiApplication
from readers.reader_manager import NFCReader
from cards.DesFire.desfire_utils import get_parsed_info
from dictionary.create_dictionary import create_atr_dictionary
from dictionary.search_atr import search_atr
import sys
from brute_force import BruteForceThread

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nfc_reader = NFCReader()  # Initialize the reader instance
        self.setup_ui()
        self.nfc_connect()  # Initial connection attempt
        self.version_bool = False
        self.current_page = "main"

    def setup_ui(self):
        # Set the window title
        self.setWindowTitle("RFID Analyzer Tool")
        self.setWindowIcon(QIcon("icons/icon.ico"))

        # Ajustar automáticamente a High-DPI Scaling
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

        # Configurar un tamaño mínimo razonable
        self.setMinimumSize(1280, 720)

        # Hacer que la ventana se abra en tamaño máximo
        self.showMaximized()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout (top bar + content)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Top bar
        self.create_top_bar()

        # Main page content
        self.create_main_page()

        # Apply different styles to all buttons
        self.set_cursor_to_all_buttons(Qt.PointingHandCursor)

    def set_cursor_to_all_buttons(self, cursor_shape):
        """Apply a specific cursor to all buttons in the application."""
        for button in self.central_widget.findChildren(QPushButton):
            button.setCursor(cursor_shape)

    def create_top_bar(self):
        """Create a top bar with enhanced design."""
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(55)  # Height of the top bar
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Different style for the top bar
        self.top_bar.setStyleSheet("background-color: #2C2C2C;")

        # Home button
        home_path = "icons/home.png"
        self.home_button = QPushButton()
        self.home_button.setIcon(QIcon(home_path))
        self.home_button.setCursor(Qt.PointingHandCursor)
        self.home_button.setIconSize(QSize(32, 32))
        self.home_button.clicked.connect(self.show_main_page)
        self.top_bar_layout.addWidget(self.home_button)

        self.top_bar_layout.addStretch()

        # Add the top bar to the main layout
        self.main_layout.addWidget(self.top_bar)

    def create_main_page(self):
        """Create the main page content."""
        self.main_page = QWidget()
        self.main_page_layout = QHBoxLayout(self.main_page)
        self.main_page_layout.setContentsMargins(15, 15, 15, 15)  # Set margins for the layout
        self.main_page_layout.setSpacing(15)  # Space between left and right sections  

        ###################################
        ###### Left side of the page ######
        ###################################

        self.left_side = QWidget()
        self.left_side.setStyleSheet("background-color: #2C2C2C;")
        self.left_layout = QVBoxLayout(self.left_side)
        self.left_layout.setAlignment(Qt.AlignCenter)

        # Title label
        self.title_label = QLabel("RFID Analyzer Tool")
        self.title_label.setStyleSheet("font-size: 44px; font-weight: bold; color: #FFFFFF;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Description label
        self.description_label = QLabel(
            "RFID Analyzer Tool is an advanced application designed \n"
            "to enable in-depth analysis of RFID cards. \n"
            "It provides comprehensive inspection capabilities, \n"
            "allowing users to access and examine data stored on the cards. \n"
            "Additionally, the tool offers secure information modification \n"
            "features based on authentication, along with the ability \n"
            "to perform key attack simulations to assess the security of the cards."
        )
        font = self.description_label.font()
        font.setItalic(True)
        self.description_label.setFont(font)
        self.description_label.setStyleSheet("color: #FFFFFF;")
        self.description_label.setAlignment(Qt.AlignCenter)

        # Add widgets to the left layout
        self.left_layout.addWidget(self.title_label)
        self.left_layout.addSpacing(50)
        self.left_layout.addWidget(self.description_label)
        self.left_layout.addSpacing(150)


        ####################################
        ###### Right side of the page ######
        ####################################

        self.right_side = QWidget()
        self.right_side.setStyleSheet("background-color: #2C2C2C;")
        self.right_layout = QVBoxLayout(self.right_side)

        # Add info of the app to the right layout
        self.info_label = QLabel(
            "This tool supports the following RFID card types:\n"
            "\n"
            "- MIFARE Classic 1K, 4K\n"
            "- MIFARE DESFire EV1, EV2, EV3\n"
            "\n"
        )
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 20px; color: #FFFFFF;")

        # Button to start the analysis
        self.start_button = QPushButton("RUN ANALYSIS")
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.setStyleSheet(
            "font-size: 20px;"
            "font-family: Roboto;" 
            "padding: 25px 150px;"
            "background-color: #5A5A5A;"
            )   
        self.start_button.clicked.connect(self.first_analysis) # Connect the button to the main function

        # Add future functionality of the App
        self.future_label = QLabel(
            "Future updates will include support for additional card types.\n"
        )
        self.future_label.setFont(font)
        self.future_label.setStyleSheet("font-size: 18px; color: #FFFFFF;")
        self.future_label.setWordWrap(True)        
        
        self.right_layout.addWidget(self.info_label, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        self.right_layout.addWidget(self.start_button, alignment=Qt.AlignHCenter)
        self.right_layout.addWidget(self.future_label, alignment=Qt.AlignCenter | Qt.AlignBottom)

        # Add both sides to the main layout
        self.main_page_layout.addWidget(self.left_side)
        self.main_page_layout.addWidget(self.right_side)        

        self.main_layout.addWidget(self.main_page)

    def show_results_page(self):
        """Display the results page with the same format as the main page."""
        # Clear the main layout (except for the top bar)
        while self.main_layout.count() > 1:
            widget = self.main_layout.takeAt(1).widget()
            if widget:
                widget.deleteLater()

        self.results_page = QWidget()
        self.results_page_layout = QHBoxLayout(self.results_page)
        self.results_page_layout.setContentsMargins(15, 15, 15, 15)  # Set margins for the layout
        self.results_page_layout.setSpacing(15)

        ###################################
        ###### Left side of the page ######
        ###################################

        # Crear el lado izquierdo
        self.results_left_side = QWidget()
        self.results_left_side.setStyleSheet("background-color: #2C2C2C;")
        self.results_left_layout = QVBoxLayout(self.results_left_side)
        self.results_left_layout.setAlignment(Qt.AlignTop)

        # Añadir el título centrado (Card Type)
        if self.card_type == "MIFARE Classic":
            card_type_label = QLabel(self.card_type)
        elif self.card_type == "MIFARE DESFire":
            card_type_label = QLabel(self.card_type + " " + self.card_version)
        card_type_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFFFFF;")
        card_type_label.setAlignment(Qt.AlignCenter)
        self.results_left_layout.addSpacing(20)
        self.results_left_layout.addWidget(card_type_label)
        self.results_left_layout.addSpacing(40)

        # Añadir el título y la caja de texto de UID
        uid_text_label = QLabel("UID:")
        uid_text_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        uid_text_label.setAlignment(Qt.AlignLeft)
        self.results_left_layout.addWidget(uid_text_label)
        self.results_left_layout.addSpacing(10)

        uid_value_box = QLineEdit()
        uid_value_box.setText(self.uid)
        uid_value_box.setReadOnly(True)
        uid_value_box.setStyleSheet(
            "font-size: 20px; color: #00FF00; background-color: #444444; "
            "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
        )
        self.results_left_layout.addWidget(uid_value_box)
        self.results_left_layout.addSpacing(20)


        # Añadir el ATR
        atr_label = QLabel(f"ATR:")
        atr_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        atr_label.setAlignment(Qt.AlignLeft)
        self.results_left_layout.addWidget(atr_label)
        self.results_left_layout.addSpacing(10)

        atr_value_box = QLineEdit()
        atr_value_box.setText(self.atr)
        atr_value_box.setReadOnly(True)
        atr_value_box.setStyleSheet(
            "font-size: 20px; color: #00FF00; background-color: #444444; "
            "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
        )
        self.results_left_layout.addWidget(atr_value_box)
        self.results_left_layout.addSpacing(20)

        if self.version_bool == False:
            # Añadir la descripción
            description_title = QLabel(f"Description:")
            description_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
            description_title.setAlignment(Qt.AlignLeft)
            self.results_left_layout.addWidget(description_title)
            self.results_left_layout.addSpacing(10)

            description_label = QLabel(self.description)
            description_label.setStyleSheet("font-size: 20px; color: #FFFFFF;")
            description_label.setWordWrap(True)
            self.results_left_layout.addWidget(description_label)
            self.results_left_layout.addSpacing(40)

            if self.card_type == "MIFARE Classic":
                # Añadir la tabla de comparación
                memory_structure = QLabel("Memory structure:")
                memory_structure.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                memory_structure.setAlignment(Qt.AlignLeft)

                self.results_left_layout.addWidget(memory_structure)
                self.results_left_layout.addSpacing(10)
                if self.table:
                    self.results_left_layout.addWidget(self.table)

                # Añadir imagen estructura de memoria
                memory_structure_img = QLabel("MIFARE Classic 1k memory structure:")
                memory_structure_img.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                memory_structure_img.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(memory_structure_img)
                self.results_left_layout.addSpacing(10)

                # Crear un QLabel para la imagen
                image_label = QLabel()
                image_label.setPixmap(QPixmap("img/memory_classic_1k.png"))
                image_label.setAlignment(Qt.AlignCenter)  # Centrar la imagen
                image_label.setStyleSheet("background-color: transparent;")  # Opcional: fondo transparente

                # Añadir la imagen al layout debajo de la tabla
                self.results_left_layout.addWidget(image_label)
                self.results_left_layout.addSpacing(100)

            elif self.card_type == "MIFARE DESFire":
                # Añadir la tabla de comparación
                memory_structure = QLabel("Memory structure:")
                memory_structure.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                memory_structure.setAlignment(Qt.AlignLeft)

                self.results_left_layout.addWidget(memory_structure)
                self.results_left_layout.addSpacing(10)
                if self.table:
                    self.results_left_layout.addWidget(self.table)
        else:

                # Añadir el vendor
                self.current_page = "results"
                vendor_label = QLabel(f"Vendor:")
                vendor_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                vendor_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(vendor_label)
                self.results_left_layout.addSpacing(10)

                vendor_value_box = QLineEdit()
                vendor_value_box.setText(self.vendor)
                vendor_value_box.setReadOnly(True)
                vendor_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(vendor_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el type
                type_label = QLabel(f"Type:")
                type_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                type_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(type_label)
                self.results_left_layout.addSpacing(10)

                type_value_box = QLineEdit()
                type_value_box.setText(self.type)
                type_value_box.setReadOnly(True)
                type_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(type_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el storage size
                storage_size_label = QLabel(f"Storage Size:")
                storage_size_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                storage_size_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(storage_size_label)
                self.results_left_layout.addSpacing(10)
                
                storage_size_value_box = QLineEdit()
                storage_size_value_box.setText(self.storage_size)
                storage_size_value_box.setReadOnly(True)
                storage_size_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(storage_size_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el protocol
                protocol_label = QLabel(f"Protocol:")
                protocol_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                protocol_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(protocol_label)
                self.results_left_layout.addSpacing(10)

                protocol_value_box = QLineEdit()
                protocol_value_box.setText(self.protocol)
                protocol_value_box.setReadOnly(True)
                protocol_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(protocol_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el hard version
                hard_version_label = QLabel(f"Hard Version:")
                hard_version_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                hard_version_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(hard_version_label)
                self.results_left_layout.addSpacing(10)

                hard_version_value_box = QLineEdit()
                hard_version_value_box.setText(self.hard_version)
                hard_version_value_box.setReadOnly(True)
                hard_version_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(hard_version_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el soft version
                soft_version_label = QLabel(f"Soft Version:")
                soft_version_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                soft_version_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(soft_version_label)
                self.results_left_layout.addSpacing(10)

                soft_version_value_box = QLineEdit()
                soft_version_value_box.setText(self.soft_version)
                soft_version_value_box.setReadOnly(True)
                soft_version_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(soft_version_value_box)
                self.results_left_layout.addSpacing(20)

                # Añadir el card version
                card_version_label = QLabel(f"Card Version:")
                card_version_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
                card_version_label.setAlignment(Qt.AlignLeft)
                self.results_left_layout.addWidget(card_version_label)
                self.results_left_layout.addSpacing(10)

                card_version_value_box = QLineEdit()
                card_version_value_box.setText(self.card_version)
                card_version_value_box.setReadOnly(True)
                card_version_value_box.setStyleSheet(
                    "font-size: 20px; color: #ffff00; background-color: #444444; "
                    "padding: 5px; border: 1px solid #888888; border-radius: 5px;"
                )
                self.results_left_layout.addWidget(card_version_value_box)
                self.results_left_layout.addSpacing(20)


        ###################################
        ###### Right side of the page #####
        ###################################

        # Crear el lado derecho (vacío por ahora)
        self.results_right_side = QWidget()
        self.results_right_side.setStyleSheet("background-color: #2C2C2C;")
        self.results_right_layout = QVBoxLayout(self.results_right_side)

        if self.card_type == "MIFARE DESFire":
            # Button to start get version info
            self.card_information = QPushButton("CARD INFORMATION")
            self.card_information.setCursor(Qt.PointingHandCursor)
            self.card_information.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.card_information.clicked.connect(self.set_version_bool)

            self.results_right_layout.addWidget(self.card_information, alignment=Qt.AlignHCenter)

            # Button to start authentication process
            self.authentication = QPushButton("AUTHENTICATION PROCESS")
            self.authentication.setCursor(Qt.PointingHandCursor)
            self.authentication.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.authentication.clicked.connect(self.authentication_process_popup)

            self.results_right_layout.addWidget(self.authentication, alignment=Qt.AlignHCenter)

        else:
            # Button to start load key process
            self.load_key = QPushButton("LOAD KEY")
            self.load_key.setCursor(Qt.PointingHandCursor)
            self.load_key.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.load_key.clicked.connect(self.load_key_pop_up)

            self.results_right_layout.addWidget(self.load_key, alignment=Qt.AlignHCenter)

            # Button to start authentication process
            self.auth_key = QPushButton("AUTHENTICATION")
            self.auth_key.setCursor(Qt.PointingHandCursor)
            self.auth_key.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.auth_key.clicked.connect(self.authentication_classic_popup)

            self.results_right_layout.addWidget(self.auth_key, alignment=Qt.AlignHCenter)

            # Button to read block
            self.read_block = QPushButton("READ BLOCK AUTHENTICATED")
            self.read_block.setCursor(Qt.PointingHandCursor)
            self.read_block.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.read_block.clicked.connect(self.read_info_classic)

            self.results_right_layout.addWidget(self.read_block, alignment=Qt.AlignHCenter)

            # Button to write block
            self.write_block = QPushButton("WRITE BLOCK AUTHENTICATED")
            self.write_block.setCursor(Qt.PointingHandCursor)
            self.write_block.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.write_block.clicked.connect(self.write_binary_pop_up)

            self.results_right_layout.addWidget(self.write_block, alignment=Qt.AlignHCenter)

            # Button to change key
            self.change_key = QPushButton("CHANGE KEY")
            self.change_key.setCursor(Qt.PointingHandCursor)
            self.change_key.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.change_key.clicked.connect(self.change_key_pop_up)

            self.results_right_layout.addWidget(self.change_key, alignment=Qt.AlignHCenter)            

            # Button to brute force attack
            self.read_block = QPushButton("BRUTE FORCE ATTACK")
            self.read_block.setCursor(Qt.PointingHandCursor)
            self.read_block.setStyleSheet(
                "font-size: 20px;"
                "font-family: Roboto;" 
                "padding: 25px 150px;"
                "background-color: #5A5A5A;"
                )   
            self.read_block.clicked.connect(self.brute_force_sector_pop_up)

            self.results_right_layout.addWidget(self.read_block, alignment=Qt.AlignHCenter)

        # Button to go back
        self.back_button = QPushButton("BACK")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet(
            "font-size: 20px;"
            "font-family: Roboto;" 
            "padding: 25px 150px;"
            "background-color: #5A5A5A;"
            )   
        self.back_button.clicked.connect(self.reset_and_back)
        
        self.results_right_layout.addWidget(self.back_button, alignment=Qt.AlignHCenter)

        # Añadir ambos lados al layout principal con proporciones
        self.results_page_layout.addWidget(self.results_left_side, 1)  # Lado izquierdo (proporción 1)
        self.results_page_layout.addWidget(self.results_right_side, 1)  # Lado derecho (proporción 1)

        self.main_layout.addWidget(self.results_page)


    def nfc_connect(self):
        """Connect to the NFC reader."""
        try:
            self.nfc_reader.connect()
            if not self.nfc_reader:
                raise Exception("Failed to connect to the NFC reader")
        except Exception as e:
            self.show_error_message(str(e))

    def show_error_message(self, message):
        """Display an error message in a message box."""
        error_box = QMessageBox(self)
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Connection Error")
        error_box.setText(message)
        error_box.exec()
    
    def set_version_bool(self):
        """Set version_bool to True."""
        self.version_bool = True
        self.show_results_page()

    def reset_and_back(self):
        """Reset the version_bool and show the main page."""
        self.version_bool = False
        if self.current_page == "analysis":
            self.show_main_page()
        else:
            self.first_analysis()

    def first_analysis(self):
        """Run the first analysis function of the cards"""
        try:
            # Connect to the NFC reader
            self.nfc_connect()
            self.current_page = "analysis"

            # Get UID and ATR
            self.uid = self.nfc_reader.get_card_uid()
            self.atr = self.nfc_reader.get_atr()

            # Create the ATR dictionary
            dict = create_atr_dictionary()
            atr_finded = search_atr(dict, self.atr)

            # Get the card type and description from ATR dictionary
            card_type = atr_finded['card_type']

            # Double check if the card is MIFARE Classic or MIFARE DESFire
            card_type_bool = self.nfc_reader.get_version()

            # Set the card type based on the ATR dictionary and the double check
            if card_type_bool and card_type == "DESFIRE":
                self.get_version_info_DESFire()
                self.card_type = "MIFARE DESFire"
                self.description = """MIFARE DESFire cards are advanced RFID technology solutions designed for high-security applications such as public transportation, access control, and electronic payment systems. They support AES, 3DES, and DES encryption standards, providing robust authentication and data protection mechanisms. Unlike MIFARE Classic cards, DESFire cards feature a flexible file system, allowing multiple applications to coexist on a single card. Thanks to their high level of security and fast data transfer capabilities, MIFARE DESFire cards are widely adopted in environments requiring enhanced security and performance."""
                self.table = self.table_analysis_DESFire()
            elif card_type_bool == False and card_type == "CLASSIC":             
                self.card_type = "MIFARE Classic"
                self.description = """MIFARE Classic cards are a widely used type of RFID technology in applications such as access control, public transportation, and contactless payment systems. They operate using a proprietary encryption algorithm known as CRYPTO1, which, while offering basic security with 48-bit keys, has been proven vulnerable to various attacks, including brute-force and side-channel analysis."""
                self.table = self.table_analysis_Classic()

            self.show_results_page()
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            self.handle_analysis_error()

    def get_version_info_DESFire(self):
        """Get the version information of a MIFARE DESFire card."""
        # Get the version information
        bool, version_info = self.nfc_reader.get_version()
        self.vendor, self.type, self.storage_size, self.protocol, self.hard_version, self.soft_version, self.card_version = get_parsed_info(version_info)


    def table_analysis_Classic(self):
        """Create and return a table widget with the comparison of MIFARE Classic 1K and 4K cards."""
        table_widget = QTableWidget()
        table_widget.setRowCount(6)  # Number of rows
        table_widget.setColumnCount(3)  # Number of columns
        table_widget.setHorizontalHeaderLabels(["Characteristic", "MIFARE Classic 1K", "MIFARE Classic 4K"])

        # Data for the table
        data = [
            ["Total capacity", "1 KB", "4 KB"],
            ["Number of sectors", "16", "40"],
            ["Blocks per sector", "4 blocks per sector", "4 blocks (sectors 0-31) / 16 blocks (sectors 32-39)"],
            ["Block size", "16 bytes", "16 bytes"],
            ["Usable memory", "48 blocks (~768 bytes)", "224 blocks (~3584 bytes)"],
            ["Control blocks", "1 per sector", "1 per sector"]
        ]

        # Populate the table with data
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                table_widget.setItem(row, column, QTableWidgetItem(value))

        # Set styles for the table
        table_widget.setStyleSheet(
            "font-size: 16px; color: #FFFFFF; background-color: #2C2C2C; gridline-color: #888888;"
        )
        table_widget.horizontalHeader().setStyleSheet("color: #FFFFFF; font-weight: bold;")
        table_widget.verticalHeader().setVisible(False)  # Hide row numbers

        # Set size policy to make the table expand horizontally while keeping a fixed height
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return table_widget
        
    def table_analysis_DESFire(self):
        """Create and return a table widget with the comparison of MIFARE DESFire EV1, EV2, and EV3 cards."""
        
        # Crear el QTableWidget
        table_widget = QTableWidget()

        self.differences_table_data = [
        ["Characteristic", "MIFARE DESFire EV1", "MIFARE DESFire EV2", "MIFARE DESFire EV3"],
        ["Memory capacity", "2 KB, 4 KB, 8 KB", "2 KB, 4 KB, 8 KB", "2 KB, 4 KB, 8 KB"],
        ["Max applications", "28", "32", "32"],
        ["Max files per application", "16", "32", "32"],
        ["Supported encryption", "DES, 3DES, AES", "DES, 3DES, AES", "DES, 3DES, AES + CMAC"],
        ["Delegated authentication", "No", "Yes", "Yes"],
        ["Protection against attacks", "Basic", "Replay attack protection", "Enhanced relay attack and bit error protection"],
        ["Multiple transactions", "No", "Yes", "Yes"],
        ["Extended lifespan", "No", "Yes", "Yes"],
        ["Compatibility", "With DESFire-compatible readers", "Backward compatible with EV1", "Backward compatible with EV1 and EV2"],
        ["Improved reading distance", "No", "No", "Yes"],
        ["Transaction mechanism", "Basic rollback", "Advanced rollback", "Advanced rollback"]
        ]

        table_widget.setRowCount(len(self.differences_table_data) - 1)  # Número de filas (excluye el encabezado)
        table_widget.setColumnCount(len(self.differences_table_data[0]))  # Número de columnas
        table_widget.setHorizontalHeaderLabels(self.differences_table_data[0])  # Encabezados de columna

        # Rellenar la tabla con los datos
        for row_idx, row_data in enumerate(self.differences_table_data[1:], start=0):
            for col_idx, value in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(value))

        # Establecer el modo de redimensionamiento de columnas para que se ajusten al ancho del widget
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ocultar los números de fila
        table_widget.verticalHeader().setVisible(False)

        # Aplicar estilos a la tabla
        table_widget.setStyleSheet(
            "font-size: 16px; color: #FFFFFF; background-color: #2C2C2C; gridline-color: #888888;"
        )
        table_widget.horizontalHeader().setStyleSheet("color: #FFFFFF; font-weight: bold;")

        # Establecer la política de tamaño
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return table_widget

    def handle_analysis_error(self):
        """Handle errors during analysis by attempting to reconnect."""
        self.show_error_message("Error during analysis. Retrying connection...")
        self.nfc_connect()
    
    def show_main_page(self):
        """Display the main page."""
        # Clear the main layout (except for the top bar)
        while self.main_layout.count() > 1:
            widget = self.main_layout.takeAt(1).widget()
            if widget:
                widget.deleteLater()
        self.version_bool = False
        self.create_main_page()
        self.main_layout.addWidget(self.main_page)

    def authentication_process_popup(self):
        """Show a pop-up dialog to input values for the authentication process."""

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Authentication Process")
        dialog.setWindowIcon(QIcon("img/candado.png"))
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiquetas y campos de entrada para los tres valores
        labels = ["Key (DES format)", "Key Number (Hex)", "IV (Initialization Vector)"]
        placeholders = [
            "e.g., 00 00 00 00 00 00 00 00",  # Placeholder para el campo Key
            "e.g., 00",                       # Placeholder para el campo Key Number
            "e.g., 00 00 00 00 00 00 00 00"   # Placeholder para el campo IV
        ]
        input_fields = []

        for label_text, placeholder in zip(labels, placeholders):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px;")
            input_field.setPlaceholderText(placeholder)  # Establecer el texto de ejemplo
            layout.addWidget(label)
            layout.addWidget(input_field)
            input_fields.append(input_field)

        if(self.card_type == "MIFARE DESFire"):
            # Botones para autenticar o usar valores predeterminados
            button_layout = QHBoxLayout()

            authenticate_button = QPushButton("Authenticate")
            authenticate_button.setCursor(Qt.PointingHandCursor)
            authenticate_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
            authenticate_button.clicked.connect(lambda: self.authenticate(dialog, input_fields))
            button_layout.addWidget(authenticate_button)

            default_button = QPushButton("Default")
            default_button.setCursor(Qt.PointingHandCursor)
            default_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
            default_button.clicked.connect(lambda: self.use_default_values(dialog))
            button_layout.addWidget(default_button)

            layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()

    def authenticate(self, dialog, input_fields):
        """Handle the authentication process using the input values."""
        
        # Obtener los valores ingresados por el usuario
        self.key_des = input_fields[0].text()
        self.key_number = input_fields[1].text()
        self.iv = input_fields[2].text()

        # Verificar que todos los valores hayan sido ingresados
        if not self.key_des or not self.key_number or not self.iv:
            QMessageBox.critical(self, "Error", "All fields must be filled out.")
            return

        # Verificar el formato de los valores ingresados
        if len(self.key_des.split()) != 8:
            QMessageBox.critical(self, "Error", "Key must be 8 bytes in hexadecimal format (e.g., '00 00 00 00 00 00 00 00').")
            return

        if not (len(self.key_number) == 2 and self.key_number.isalnum()):
            QMessageBox.critical(self, "Error", "Key Number must be a 2-digit hexadecimal value (e.g., '00').")
            return

        if len(self.iv.split()) != 8:
            QMessageBox.critical(self, "Error", "IV must be 8 bytes in hexadecimal format (e.g., '00 00 00 00 00 00 00 00').")
            return

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.authentication = self.nfc_reader.authentication(self.key_des, self.key_number, self.iv)
            
            if self.authentication == False:
                raise Exception("Authentication failed.")
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Authentication Success", "Authentication was successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Authentication Failed", f"Authentication could not be completed.\nError: {str(e)}")

        # Cerrar el diálogo después de la autenticación
        dialog.accept()

    def use_default_values(self, dialog):
        """Use default values for the authentication process."""
        
        self.key_des    = "00 00 00 00 00 00 00 00"
        self.key_number = "00"
        self.iv         = "00 00 00 00 00 00 00 00"

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.authentication = self.nfc_reader.authentication(self.key_des, self.key_number, self.iv)
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Authentication Success", "Authentication was successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Authentication Failed", f"Authentication could not be completed.\nError: {str(e)}")

        # Cerrar el diálogo después de usar valores predeterminados
        dialog.accept()

    def load_key_pop_up(self):
        """Show a pop-up dialog to input values for the load key process."""

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Load Key Process")
        dialog.setWindowIcon(QIcon("img/candado.png"))
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiquetas y campos de entrada para los tres valores
        labels = ["Key"]
        placeholders = [
            "e.g., 00 00 00 00 00 00",  # Placeholder para el campo Key
        ]
        input_fields = []

        for label_text, placeholder in zip(labels, placeholders):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px;")
            input_field.setPlaceholderText(placeholder)  # Establecer el texto de ejemplo
            layout.addWidget(label)
            layout.addWidget(input_field)
            input_fields.append(input_field)

        # Botones para autenticar o usar valores predeterminados
        button_layout = QHBoxLayout()

        authenticate_button = QPushButton("Load Key")
        authenticate_button.setCursor(Qt.PointingHandCursor)
        authenticate_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        authenticate_button.clicked.connect(lambda: self.load_key_cla(dialog, input_fields))
        button_layout.addWidget(authenticate_button)

        default_button = QPushButton("Default")
        default_button.setCursor(Qt.PointingHandCursor)
        default_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        default_button.clicked.connect(lambda: self.use_default_values_classic(dialog))
        button_layout.addWidget(default_button)

        layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()

    def load_key_cla(self, dialog, input_fields):
        """Handle the load key process using the input values."""
        
        # Obtener los valores ingresados por el usuario
        self.key_clas = input_fields[0].text()

        # Verificar que todos los valores hayan sido ingresados
        if not self.key_clas:
            QMessageBox.critical(self, "Error", "All fields must be filled out.")
            return

        # Verificar el formato de los valores ingresados
        if len(self.key_clas.split()) != 6:
            QMessageBox.critical(self, "Error", "Key must be 6 bytes in hexadecimal format (e.g., '00 00 00 00 00 00 00 00').")
            return

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.key_load = self.nfc_reader.loadKey(self.key_clas)
            
            if self.key_load == False:
                raise Exception("Load key failed.")

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Key Loaded", "Key was loaded successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Key Loading Failed", f"Key could not be loaded.\nError: {str(e)}")

        # Cerrar el diálogo después de la autenticación
        dialog.accept()

    def use_default_values_classic(self, dialog):
        
        self.key_clas = "FF FF FF FF FF FF"

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.key_load = self.nfc_reader.loadKey(self.key_clas)
        
            if self.key_load == False:
                raise Exception("Authentication failed.")
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Key Loaded", "Key was loaded successful!")
            
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Key Failed", f"Key could not be loaded.\nError: {str(e)}")
        
        # Cerrar el diálogo después de usar valores predeterminados
        dialog.accept()

    def authentication_classic_popup(self):
        """Show a pop-up dialog to input values for the authentication process."""

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Authentication Process")
        dialog.setWindowIcon(QIcon("img/candado.png"))
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiquetas y campos de entrada para los tres valores
        labels = ["Block Number", "Key Number"]
        placeholders = [
            "e.g., 00",     # Placeholder para el campo Key
            "e.g., A or B", # Placeholder para el campo Key Number
        ]
        input_fields = []

        for label_text, placeholder in zip(labels, placeholders):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px;")
            input_field.setPlaceholderText(placeholder)  # Establecer el texto de ejemplo
            layout.addWidget(label)
            layout.addWidget(input_field)
            input_fields.append(input_field)

        # Botones para autenticar o usar valores predeterminados
        button_layout = QHBoxLayout()

        authenticate_button = QPushButton("Authenticate Block")
        authenticate_button.setCursor(Qt.PointingHandCursor)
        authenticate_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        authenticate_button.clicked.connect(lambda: self.authentication_classic(dialog, input_fields))
        button_layout.addWidget(authenticate_button)

        default_button = QPushButton("Default")
        default_button.setCursor(Qt.PointingHandCursor)
        default_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        default_button.clicked.connect(lambda: self.use_default_values_classic_auth(dialog))
        button_layout.addWidget(default_button)

        layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()


    def authentication_classic(self, dialog, input_fields):
        """Handle the authentication process using the input values."""
        
        # Obtener los valores ingresados por el usuario
        self.key_block = input_fields[0].text()
        self.key_number = input_fields[1].text()
        self.key_block_test = self.key_block.strip()

        # Verificar que el input contiene solo dígitos y está en el rango correcto
        if not self.key_block_test.isdigit():
            QMessageBox.critical(self, "Input Error", "Block must be a numeric value between 00 and 63.")
            return

        # Convertir el input a un número entero
        block_number = int(self.key_block_test)

        # Validar que el bloque esté entre 0 y 63 (decimal)
        if block_number < 0 or block_number > 63:
            QMessageBox.critical(self, "Input Error", "Block must be between 0 and 63 (Decimal).")
            return
        
        if self.key_number not in ["A", "B"]:
            QMessageBox.critical(self, "Error", "Key Number must be 'A' or 'B'.")
            return

        self.block_bytes = int(self.key_block)
        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.authentication_cla = self.nfc_reader.authentication_classic(self.block_bytes, self.key_number)
            
            if self.authentication_cla == False:
                raise Exception("Load key failed.")

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Authentication Successful", "Authentication was successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Authentication Failed", f"Authentication could not be completed.\nError: {str(e)}")

        # Cerrar el diálogo después de la autenticación
        dialog.accept()

    def use_default_values_classic_auth(self, dialog):
        
        self.block_bytes = 0x00
        self.key_number = "A"

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.authentication_cla = self.nfc_reader.authentication_classic(self.block_bytes, self.key_number)
        
            if self.authentication_cla == False:
                raise Exception("Authentication failed.")
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Authentication Successful", "Authentication was successful!")
            
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Authentication Failed", f"Authentication could not be completed.\nError: {str(e)}")
        
        # Cerrar el diálogo después de usar valores predeterminados
        dialog.accept()


    def read_info_classic(self, dialog):
        """Read binary information from the block and display a popup based on the result."""
            
        # Verificar si el atributo `block_bytes` está definido
        if not hasattr(self, 'block_bytes') or self.block_bytes is None:
            QMessageBox.critical(self, "Error", "Block bytes are not authenticated. Please ensure the block is set before reading.")
            return
    
        else:
            try:
                # Llamar a la función `read_binary` usando el valor ya almacenado en `self.block_number_byte`
                response, aux = self.nfc_reader.read_binary(self.block_bytes)
                
                # Mostrar un popup con los datos en hexadecimal si la lectura fue exitosa
                if aux:
                    # Convertir la lista de decimales a formato hexadecimal
                    response_hex = " ".join(f"{byte:02X}" for byte in response)  # Ejemplo: "F9 B1 30 03 7B 08 04 00"

                    # Crear un diálogo personalizado
                    popup = QDialog(self)
                    popup.setWindowTitle("Read Successful")
                    popup.setFixedWidth(800)
                    popup.adjustSize()  

                    # Layout principal del popup
                    layout = QVBoxLayout(popup)

                    # Título opcional
                    title = QLabel(f"The binary data of block {self.block_bytes} is:")
                    title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
                    layout.addWidget(title)

                    # Crear un QTextEdit para mostrar el texto copiable
                    text_edit = QTextEdit()
                    text_edit.setText(response_hex)
                    text_edit.setReadOnly(True)  # Solo lectura
                    text_edit.setStyleSheet("""
                        font-size: 26px;
                        font-family: Consolas, monospace;
                        color: #00FF00;
                        background-color: #333333;
                        border: none;
                    """)
                    layout.addWidget(text_edit)

                    # Botón para cerrar el diálogo
                    close_button = QPushButton("Close")
                    close_button.setStyleSheet("font-size: 14px; padding: 10px;")
                    close_button.clicked.connect(popup.close)
                    layout.addWidget(close_button)

                    popup.exec()
                else:
                    QMessageBox.critical(self, "Read Failed", "Failed to read the binary data.")

            except Exception as e:
                # Mostrar mensaje de error en caso de excepción
                QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{str(e)}")

            # Cerrar el diálogo
            dialog.accept()

    def change_key_pop_up(self):
        """Show a pop-up dialog to input values for the change key process."""

        # Verificar si el atributo `block_bytes` está definido
        if not hasattr(self, 'block_bytes') or self.block_bytes is None:
            QMessageBox.critical(self, "Error", "Block bytes are not authenticated. Please ensure the block is set before reading.")
            return

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Key Process")
        dialog.setWindowIcon(QIcon("img/candado.png"))
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiquetas y campos de entrada para los tres valores
        labels = ["KeyA", "KeyB"]
        placeholders = [
            "e.g., 00 00 00 00 00 00",  # Placeholder para el campo KeyA
            "e.g., 00 00 00 00 00 00",  # Placeholder para el campo KeyB
        ]
        input_fields = []

        for label_text, placeholder in zip(labels, placeholders):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px;")
            input_field.setPlaceholderText(placeholder)  # Establecer el texto de ejemplo
            layout.addWidget(label)
            layout.addWidget(input_field)
            input_fields.append(input_field)

        # Botones para autenticar o usar valores predeterminados
        button_layout = QHBoxLayout()

        change_key_button = QPushButton("Change Keys")
        change_key_button.setCursor(Qt.PointingHandCursor)
        change_key_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        change_key_button.clicked.connect(lambda: self.change_key_logic(dialog, input_fields))
        button_layout.addWidget(change_key_button)

        layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()

    def change_key_logic(self, dialog, input_fields):
        """Handle the load key process using the input values."""
    
        # Obtener los valores ingresados por el usuario
        self.keyA = input_fields[0].text()
        self.keyB = input_fields[1].text()

        # Verificar que todos los valores hayan sido ingresados
        if not self.keyA or not self.keyB:
            QMessageBox.critical(self, "Error", "All fields must be filled out.")
            return      

        # Verificar el formato de los valores ingresados
        if len(self.keyA.split()) != 6:
            QMessageBox.critical(self, "Error", "Key must be 6 bytes in hexadecimal format (e.g., '00 00 00 00 00 00').")
            return
        
        if len(self.keyB.split()) != 6:
            QMessageBox.critical(self, "Error", "Key must be 6 bytes in hexadecimal format (e.g., '00 00 00 00 00 00').")
            return

        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.sector, self.key_load = self.nfc_reader.change_key(int(self.block_bytes), self.keyA, self.keyB)
            
            if self.key_load == False:
                raise Exception("Change Key failed.")

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Keys changed", f"Keys of the sector {self.sector} were changed successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Key Changed Failed", f"Key could not be changed.\nError: {str(e)}")

        # Cerrar el diálogo después de la autenticación
        dialog.accept()


    def write_binary_pop_up(self):
        """Show a pop-up dialog to input values for the load key process."""

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Write Binary Process")
        dialog.setWindowIcon(QIcon("img/candado.png"))
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiquetas y campos de entrada para los tres valores
        labels = ["Block", "Data"]
        placeholders = [
            "e.g., 01",                 # Placeholder para el campo Sector
            "e.g., 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",  # Placeholder para el campo KeyA
        ]
        input_fields = []

        for label_text, placeholder in zip(labels, placeholders):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 16px;")
            input_field.setPlaceholderText(placeholder)  # Establecer el texto de ejemplo
            layout.addWidget(label)
            layout.addWidget(input_field)
            input_fields.append(input_field)

        # Botones para autenticar o usar valores predeterminados
        button_layout = QHBoxLayout()

        write_binary_button = QPushButton("Write Data")
        write_binary_button.setCursor(Qt.PointingHandCursor)
        write_binary_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        write_binary_button.clicked.connect(lambda: self.write_binary(dialog, input_fields))
        button_layout.addWidget(write_binary_button)

        layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()

    def write_binary(self, dialog, input_fields):
        """Handle the load key process using the input values."""
    
        # Obtener los valores ingresados por el usuario
        self.block_number = input_fields[0].text()
        self.data = input_fields[1].text()

        # Verificar que todos los valores hayan sido ingresados
        if not self.block_number or not self.data:
            QMessageBox.critical(self, "Error", "All fields must be filled out.")
            return

        if not self.block_number.isdigit():
            QMessageBox.critical(self, "Error", "Block must be a numeric value between 0 and 63.")
            return
        
        if int(self.block_number) < 0 or int(self.block_number) > 63:
            QMessageBox.critical(self, "Error", "Block must be between 0 and 63.")
            return
        
        if len(self.data.split()) != 16:
            QMessageBox.critical(self, "Error", "Data must be 16 bytes in hexadecimal format (e.g., '00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00').")
            return
        
        # Verificar si el bloque es un sector trailer o el bloque 0 (reservado)
        if int(self.block_number) % 4 == 3:  # Sector trailer
            QMessageBox.critical(self, "Error", f"Block {self.block_number} is a sector trailer and cannot be written to.")
            return

        if int(self.block_number) == 0:  # Bloque reservado
            QMessageBox.critical(self, "Error", "Block 0 is reserved and cannot be written to.")
            return
        
        block_number = int(self.block_number)


        try:
            # Llamar a la función de autenticación principal con valores predeterminados
            self.data_loaded = self.nfc_reader.write_binary(block_number, self.data)
            
            if self.data_loaded == False:
                raise Exception("Write data failed.")

            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Data wrote", "Data was written successful!")
        
        except Exception as e:
            # Mostrar mensaje de error en caso de excepción
            QMessageBox.critical(self, "Write data failed", f"Data could not be written.\nError: {str(e)}")

        # Cerrar el diálogo después de la autenticación
        dialog.accept()


    def brute_force_sector_pop_up(self):
        """Show a pop-up dialog to input a sector or leave it empty for brute-force attack on all sectors."""

        # Crear un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle("Brute Force Attack")
        dialog.setWindowIcon(QIcon("img/candado.png"))  # Icono del diálogo
        dialog.setModal(True)
        dialog.setFixedWidth(400)
        dialog.adjustSize()

        # Layout principal del diálogo
        layout = QVBoxLayout(dialog)

        # Etiqueta y campo de entrada para el sector
        label = QLabel("Sector (0-15) or leave empty for all:")
        label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        input_field = QLineEdit()
        input_field.setStyleSheet("font-size: 16px;")
        input_field.setPlaceholderText("e.g., 3 or leave empty")

        layout.addWidget(label)
        layout.addWidget(input_field)

        # Botón para iniciar el brute-force attack
        button_layout = QHBoxLayout()
        
        start_attack_button = QPushButton("Start Attack")
        start_attack_button.setCursor(Qt.PointingHandCursor)
        start_attack_button.setStyleSheet("background-color: #5A5A5A; color: #FFFFFF; padding: 10px 20px;")
        start_attack_button.clicked.connect(lambda: self.brute_force_attack_gui(dialog, input_field))
        button_layout.addWidget(start_attack_button)

        layout.addLayout(button_layout)

        # Mostrar el diálogo
        dialog.exec()


    def brute_force_attack_gui(self, dialog, input_field):
        """Iniciar el ataque de fuerza bruta con progreso en la GUI."""
        key_file_path = "utils/keys.txt"  # Ruta al archivo de claves

        # Obtener el sector ingresado
        sector_text = input_field.text().strip()
        sector = int(sector_text) if sector_text.isdigit() and 0 <= int(sector_text) <= 15 else None

        # Cerrar el diálogo después de la selección
        dialog.accept()

        # Crear el popup de progreso
        popup = QDialog(self)
        popup.setWindowTitle("Brute Force Progress")
        popup.setFixedWidth(400)
        popup.adjustSize()

        layout = QVBoxLayout(popup)
        progress_label = QLabel("Progress: 0/0")
        progress_label.setStyleSheet("font-size: 22px;")
        layout.addWidget(progress_label)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(popup.reject)
        layout.addWidget(cancel_button)

        # Crear el hilo para la fuerza bruta con el sector seleccionado
        thread = BruteForceThread(
            key_file_path, 
            self.nfc_reader.loadKey, 
            self.nfc_reader.authentication_classic,
            sector=sector
        )

        # Conectar señales
        thread.update_progress.connect(
            lambda current, total: progress_label.setText(f"Progress: {current}/{total}")
        )
        thread.finished.connect(lambda key, block, key_type, success: self.on_brute_force_finished(key, block, key_type, success, popup))

        # Iniciar el hilo
        thread.start()
        popup.exec()

        # Cancelar el hilo si se cierra el popup
        if not popup.result():
            thread.terminate()


    def show_keys_popup(self, key_A, key_B, sector):
        """Mostrar un popup con ambas claves encontradas."""
        popup = QDialog(self)
        popup.setWindowTitle("Keys Found")
        popup.setStyleSheet("background-color: #222222; color: white;")  
        popup.resize(600, 300)

        layout = QVBoxLayout(popup)

        title = QLabel(f"Valid keys found for sector {sector}:")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Mostrar clave A
        key_a_label = QLabel("Key A:")
        key_a_label.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(key_a_label)

        key_a_text = QTextEdit()
        key_a_text.setText(key_A if key_A else "Not found")
        key_a_text.setReadOnly(True)
        key_a_text.setStyleSheet("font-size: 26px; font-family: Consolas, monospace; background-color: #333333; color: #00FF00; border: none;")
        layout.addWidget(key_a_text)

        # Mostrar clave B
        key_b_label = QLabel("Key B:")
        key_b_label.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(key_b_label)

        key_b_text = QTextEdit()
        key_b_text.setText(key_B if key_B else "Not found")
        key_b_text.setReadOnly(True)
        key_b_text.setStyleSheet("font-size: 26px; font-family: Consolas, monospace; background-color: #333333; color: #00FF00; border: none;")
        layout.addWidget(key_b_text)

        # Botón de cierre
        close_button = QPushButton("Close")
        close_button.setStyleSheet("font-size: 14px; padding: 10px; background-color: #444444; color: white;")
        close_button.clicked.connect(popup.close)
        layout.addWidget(close_button)

        popup.exec()

    def show_all_sectors_popup(self, key_A, key_B):
        """Mostrar un popup con las claves de todos los sectores."""
        popup = QDialog(self)
        popup.setWindowTitle("All Found Keys for Sectors")
        popup.setStyleSheet("background-color: #222222; color: white;")
        popup.resize(800, 600)

        layout = QVBoxLayout(popup)

        # Título
        title = QLabel("Valid keys found for all sectors:")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title)

        # Crear un GridLayout para organizar los sectores y claves
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Encabezados
        header_sector = QLabel("Sector")
        header_sector.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        grid_layout.addWidget(header_sector, 0, 0, alignment=Qt.AlignCenter)

        header_key_a = QLabel("Key A")
        header_key_a.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        grid_layout.addWidget(header_key_a, 0, 1, alignment=Qt.AlignCenter)

        header_key_b = QLabel("Key B")
        header_key_b.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        grid_layout.addWidget(header_key_b, 0, 2, alignment=Qt.AlignCenter)

        # Agregar claves para cada sector
        for sector in range(16):  # Iterar por los sectores (0-15)
            # Sector
            sector_label = QLabel(f"{sector}")
            sector_label.setStyleSheet("font-size: 18px; color: white;")
            grid_layout.addWidget(sector_label, sector + 1, 0, alignment=Qt.AlignCenter)

            # Key A
            key_a_text = QTextEdit()
            key_a_text.setText(key_A[sector] if sector < len(key_A) and key_A[sector] else "Not found")
            key_a_text.setReadOnly(True)
            key_a_text.setAlignment(Qt.AlignCenter)
            key_a_text.setStyleSheet("""
                font-size: 20px;
                font-family: Consolas, monospace;
                color: #00FF00;
                background-color: #333333;
                border: none;
            """)
            grid_layout.addWidget(key_a_text, sector + 1, 1)

            # Key B
            key_b_text = QTextEdit()
            key_b_text.setText(key_B[sector] if sector < len(key_B) and key_B[sector] else "Not found")
            key_b_text.setReadOnly(True)
            key_b_text.setAlignment(Qt.AlignCenter)
            key_b_text.setStyleSheet("""
                font-size: 20px;
                font-family: Consolas, monospace;
                color: #00FF00;
                background-color: #333333;
                border: none;
            """)
            grid_layout.addWidget(key_b_text, sector + 1, 2)

        layout.addLayout(grid_layout)

        # Botón para cerrar el popup
        close_button = QPushButton("Close")
        close_button.setStyleSheet("font-size: 14px; padding: 10px; background-color: #444444; color: white; margin-top: 10px;")
        close_button.clicked.connect(popup.close)
        layout.addWidget(close_button)

        popup.exec()


    def on_brute_force_finished(self, key_A, key_B, sector, success, popup):
        """Manejar el resultado final del ataque de fuerza bruta."""
        popup.accept()  # Cerrar el popup de progreso
        if success:
            if len(key_A) > 1 or len(key_B) > 1:
                self.show_all_sectors_popup(key_A, key_B)
            else:
                self.show_keys_popup(key_A[0], key_B[0], sector)
        else:
            QMessageBox.warning(self, "Failed", "No valid key found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainApp()
    window.show()

    app.exec()