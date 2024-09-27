# Nusantara-AI-
Nusantara AI offline mode
# LLaMA 3.1 di Raspberry Pi 5 (8GB) - Panduan Instalasi Offline

Panduan ini menjelaskan cara menginstall dan menjalankan versi lebih kecil dari **LLaMA 3.1** (seperti **7B** atau **13B**) di **Raspberry Pi 5 (8GB)** dalam mode offline. Mengingat keterbatasan hardware, menjalankan model dengan **405B parameter** tidak praktis. Sebagai gantinya, kita akan menggunakan teknik kuantisasi untuk mengoptimalkan performa.

## Daftar Isi
- [Kebutuhan](#kebutuhan)
- [Instalasi](#instalasi)
  - [Langkah 1: Siapkan Raspberry Pi OS](#langkah-1-siapkan-raspberry-pi-os)
  - [Langkah 2: Instalasi Dependensi](#langkah-2-instalasi-dependensi)
  - [Langkah 3: Clone LLaMA dari GitHub](#langkah-3-clone-llama-dari-github)
  - [Langkah 4: Unduh Model LLaMA yang Lebih Kecil](#langkah-4-unduh-model-llama-yang-lebih-kecil)
  - [Langkah 5: Kuantisasi Model (Opsional)](#langkah-5-kuantisasi-model-opsional)
  - [Langkah 6: Konfigurasi Swap Memory](#langkah-6-konfigurasi-swap-memory)
  - [Langkah 7: Jalankan Model](#langkah-7-jalankan-model)
- [Optimasi Performa](#optimasi-performa)
- [Kesimpulan](#kesimpulan)

## Kebutuhan

- **Raspberry Pi 5 (8GB)**
- **Kartu MicroSD** atau **Penyimpanan Eksternal SSD** (untuk tambahan ruang penyimpanan)
- Sistem pendingin aktif (untuk mencegah panas berlebih)
- Koneksi **internet sementara** untuk mengunduh model dan dependensi

## Instalasi

### Langkah 1: Siapkan Raspberry Pi OS
1. Instal **Raspberry Pi OS (64-bit)** atau **Ubuntu Server** pada Raspberry Pi 5.
2. Perbarui sistem:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

### Langkah 2: Instalasi Dependensi
Instal dependensi yang diperlukan seperti Python, PyTorch, dan transformers.

1. Instal Python dan pip:
    ```bash
    sudo apt install python3 python3-pip -y
    ```

2. Instal PyTorch (versi CPU) dan Transformers:
    ```bash
    pip install torch torchvision torchaudio transformers
    ```

### Langkah 3: Clone LLaMA dari GitHub
Clone repository LLaMA dari GitHub untuk mendapatkan kode dan model yang diperlukan.

1. Clone repository LLaMA:
    ```bash
    git clone https://github.com/facebookresearch/llama.git
    cd llama
    ```

2. Instal dependensi Python yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

### Langkah 4: Unduh Model LLaMA yang Lebih Kecil
Unduh model LLaMA yang lebih kecil (seperti 7B) dari Hugging Face atau sumber lain.

1. Kunjungi Hugging Face untuk mengunduh **LLaMA 7B** atau **LLaMA 13B**.
2. Pindahkan model ke **SSD Eksternal** jika tersedia untuk menghemat ruang penyimpanan.

### Langkah 5: Kuantisasi Model (Opsional)
Anda dapat mengkuantisasi model menggunakan **Bitsandbytes** untuk mengurangi penggunaan memori dan meningkatkan performa.

1. Instal Bitsandbytes:
    ```bash
    pip install bitsandbytes
    ```

2. Modifikasi kode pemuatan model untuk menggunakan kuantisasi 8-bit:
    ```python
    from transformers import LLaMATokenizer, LLaMAForCausalLM
    import bitsandbytes as bnb

    model_path = "/path/to/7B-model"
    tokenizer = LLaMATokenizer.from_pretrained(model_path)
    model = LLaMAForCausalLM.from_pretrained(model_path, load_in_8bit=True)

    def generate_text(prompt):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=100)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    if __name__ == "__main__":
        prompt = input("Masukkan prompt Anda: ")
        print(generate_text(prompt))
    ```

### Langkah 6: Konfigurasi Swap Memory
Untuk menghindari kekurangan memori, tambahkan swap memory menggunakan penyimpanan SSD sebagai RAM virtual.

1. Buat file swap 4GB:
    ```bash
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    ```

2. Pastikan swap diaktifkan saat boot dengan menambahkan baris berikut ke `/etc/fstab`:
    ```bash
    /swapfile none swap sw 0 0
    ```

### Langkah 7: Jalankan Model
1. Jalankan skrip untuk menghasilkan teks berdasarkan prompt:
    ```bash
    python run_llama.py
    ```

2. Masukkan prompt Anda dan biarkan model menghasilkan respons.

## Optimasi Performa
- **Batasi panjang input dan output** untuk menghindari overload pada Raspberry Pi.
- **Pastikan pendinginan yang baik** untuk Raspberry Pi agar tidak terjadi throttling.
- **Gunakan penyimpanan SSD** untuk mempercepat baca/tulis dan meningkatkan kapasitas swap memory.

## Kesimpulan
Meskipun menjalankan model **LLaMA 3.1 405B** penuh di Raspberry Pi 5 tidak memungkinkan, Anda dapat menggunakan **model yang lebih kecil** seperti **LLaMA 7B** atau **13B** dengan kuantisasi untuk bereksperimen dengan LLaMA di perangkat berdaya rendah seperti Raspberry Pi. Pastikan untuk mengoptimalkan performa dengan mengkonfigurasi swap memory dan pendinginan perangkat secara efisien.
