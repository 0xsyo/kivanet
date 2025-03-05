# Kivanet Bot

Kivanet Automation is a Python-based script designed to automate interactions with the Kivanet platform. This script can perform tasks such as logging in, retrieving user information, and displaying account balances. It utilizes various Python libraries to achieve these functionalities, making it a powerful tool for automating routine tasks on Kivanet.

## Features

- **Automated Login**: Securely log in to Kivanet using stored credentials.
- **User Information Retrieval**: Fetch and display user information and account balance.
- **Proxy Support**: Optionally use proxies for network requests.
- **Rich Output**: Utilize the `rich` library for colorful and structured console output.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/0xsyo/kivanet.git
    cd kivanet
    ```

2. Create a virtual environment (recommended to avoid module conflicts):
    ```bash
    python -m venv venv  # For Windows
    python3 -m venv venv  # For Linux
    ```

3. Activate the virtual environment:
    - Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Ensure you have the necessary files (`acc.txt`, `proxy.txt`) in the same directory as the script.

2. Run the script:
    - Windows:
        ```bash
        python main.py
        ```
    - Linux:
        ```bash
        python3 main.py
        ```

### Important Notes

- **File Structure**:
    - `acc.txt`: Contains account credentials in the format `email:password`.
    - `proxy.txt`: Contains proxy addresses (optional).

### Disclaimer

The use of this script is at your own risk. The author assumes no responsibility for any misuse or damage caused by this script. Ensure you comply with all relevant terms of service and legal requirements when using this script. Use it responsibly and ethically.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

# Kivanet Bot

Kivanet Automation adalah skrip berbasis Python yang dirancang untuk mengotomatisasi interaksi dengan platform Kivanet. Skrip ini dapat melakukan tugas-tugas seperti login, mengambil informasi pengguna, dan menampilkan saldo akun. Skrip ini memanfaatkan berbagai pustaka Python untuk mencapai fungsi-fungsi tersebut, menjadikannya alat yang kuat untuk mengotomatisasi tugas rutin di Kivanet.

## Fitur

- **Login Otomatis**: Login ke Kivanet dengan aman menggunakan kredensial yang disimpan.
- **Pengambilan Informasi Pengguna**: Mengambil dan menampilkan informasi pengguna dan saldo akun.
- **Dukungan Proxy**: Opsional menggunakan proxy untuk permintaan jaringan.
- **Output Kaya**: Memanfaatkan pustaka `rich` untuk output konsol yang berwarna dan terstruktur.

## Memulai

### Prasyarat

- Python 3.10 atau lebih tinggi
- `pip` (penginstal paket Python)

### Instalasi

1. Clone repositori:
    ```bash
    git clone https://github.com/0xsyo/kivanet.git
    cd kivanet
    ```

2. Buat lingkungan virtual (disarankan untuk menghindari konflik modul):
    ```bash
    python -m venv venv  # Untuk Windows
    python3 -m venv venv  # Untuk Linux
    ```

3. Aktivasi lingkungan virtual:
    - Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - Linux:
        ```bash
        source venv/bin/activate
        ```

4. Instal paket yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

### Penggunaan

1. Pastikan Anda memiliki file yang diperlukan (`acc.txt`, `proxy.txt`) di direktori yang sama dengan skrip.

2. Jalankan skrip:
    - Windows:
        ```bash
        python main.py
        ```
    - Linux:
        ```bash
        python3 main.py
        ```

### Catatan Penting

- **Struktur File**:
    - `acc.txt`: Berisi kredensial akun dalam format `email:password`.
    - `proxy.txt`: Berisi alamat proxy (opsional).

### Disclaimer

Penggunaan skrip ini sepenuhnya menjadi tanggung jawab Anda. Penulis tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh skrip ini. Pastikan Anda mematuhi semua ketentuan layanan dan persyaratan hukum yang relevan saat menggunakan skrip ini. Gunakan dengan bertanggung jawab dan etis.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.
