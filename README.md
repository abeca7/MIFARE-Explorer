# RFID Card Management and Analysis Application

This project is a software tool for identifying, reading, and performing advanced operations on MIFARE RFID cards. The application includes a graphical user interface (GUI) to facilitate user interaction and manage functionalities such as authentication, key management, and card data exploration.

**Academic Purpose**: This project has been developed for academic purposes. Full details of the work can be found at [link to the project].

---

## **Project Structure**

The project is organized into the following files and directories:

- **`src/debug_tool.py`**: Internal script for testing and debugging various components, such as the reader manager and card utilities. Not intended for end-user operation.
- **`src/gui_app.py`**: Main application file containing the graphical user interface for interacting with RFID cards.
- **`src/brute_force.py`**: Module for performing brute-force attacks on MIFARE Classic cards to discover access keys.
- **`src/cards/`**: Contains submodules specific to interaction with different types of RFID cards.
  - **`src/cards/DesFire/`**: Functionalities and utilities specific to MIFARE DESFire cards.
- **`src/dictionary/`**: Includes tools for creating and searching ATR dictionaries for card identification.
- **`src/icons/`** and **`src/img/`**: Visual resources such as icons and images used in the GUI.
- **`src/readers/`**: Modules for managing communication with RFID readers.
- **`src/utils/`**: General utility functions used across the application.
- **`.gitignore`**: Specifies files and directories to exclude from version control.
- **`launch.json`**: Configuration for the development environment.

---

## **Prerequisites**

### **Hardware**
- **RFID Card Reader**: ACS ACR122U model.

### **Software**
- **Operating System**: Windows 11.
- **Python Libraries**:
  - `smartcard` for RFID communication.
  - `PySide6` for the graphical user interface.
  - `pycryptodome` for cryptographic operations, including DES encryption.

---

## **Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/abeca7/rfid-card-tool.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Connect the RFID reader to your computer and ensure drivers are installed.

---

## **Usage Guide**

1. Run the main application:
   ```bash
   python src/gui_app.py
   ```
2. Use the GUI to:
   - Identify and read MIFARE cards.
   - Authenticate and perform operations on card sectors.
   - Manage keys and view detailed card information.

---

## **Key Features**

### **MIFARE Classic**
- **Identification**: Retrieve the UID and basic details.
- **Authentication**: Verify sectors with keys.
- **Reading and Writing**: Access and modify authenticated data blocks.
- **Brute-Force Attacks**: Discover keys through exhaustive trials.

### **MIFARE DESFire**
- **Advanced Authentication**: Authenticate using AES and 3DES algorithms.
- **Key Management**: Securely modify keys and manage applications on the card.
- **Detailed Information Retrieval**: Parse and display metadata and card-specific details.

---

## **Contributing**

If you wish to contribute to this project:
1. Fork the repository.
2. Create a branch for your contribution:
   ```bash
   git checkout -b new-feature
   ```
3. Submit a pull request with a detailed description of the changes made.

---

## **License**

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License.

You are free to:
- **Share** — copy and redistribute the material in any medium or format.
- **Adapt** — remix, transform, and build upon the material.

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes without explicit permission from the author.

For full details, visit: [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
