# Instalasi LLaMA 3.1 sebagai Virtual Assistant Offline di Raspberry Pi 5 (8GB)

Panduan ini menjelaskan bagaimana cara menginstal **LLaMA 3.1** versi yang lebih kecil (misalnya 7B atau 13B) di **Raspberry Pi 5 (8GB)** dan mengkonfigurasinya sebagai virtual assistant dalam mode **offline**. Mengingat keterbatasan hardware, menjalankan model **405B** tidak praktis pada Raspberry Pi 5, jadi kita akan menggunakan model yang lebih ringan dan optimasi seperti kuantisasi.

## Daftar Isi
- [Kebutuhan](#kebutuhan)
- [Instalasi](#instalasi)
  - [Langkah 1: Persiapan Raspberry Pi OS](#langkah-1-persiapan-raspberry-pi-os)
  - [Langkah 2: Instalasi Dependensi](#langkah-2-instalasi-dependensi)
  - [Langkah 3: Clone Repository LLaMA](#langkah-3-clone-repository-llama)
  - [Langkah 4: Unduh Model LLaMA yang Lebih Kecil](#langkah-4-unduh-model-llama-yang-lebih-kecil)
  - [Langkah 5: Kuantisasi Model](#langkah-5-kuantisasi-model-opsional)
  - [Langkah 6: Konfigurasi Swap Memory](#langkah-6-konfigurasi-swap-memory)
  - [Langkah 7: Konfigurasi Virtual Assistant](#langkah-7-konfigurasi-virtual-assistant)
  - [Langkah 8: Jalankan Virtual Assistant](#langkah-8-jalankan-virtual-assistant)
- [Optimasi Performa](#optimasi-performa)
- [Kesimpulan](#kesimpulan)

## Kebutuhan

- **Raspberry Pi 5 (8GB)**
- **MicroSD Card** (minimal 64GB) atau **SSD eksternal** untuk ruang penyimpanan tambahan
- **Koneksi Internet Sementara** (untuk mendownload model dan dependensi)
- Sistem **pendingin aktif** (untuk mencegah panas berlebih)
- **Mikrofon dan speaker** jika ingin menggunakan input/output suara

## Instalasi

### Langkah 1: Persiapan Raspberry Pi OS
1. Siapkan Raspberry Pi dengan **Raspberry Pi OS (64-bit)** atau **Ubuntu Server**.
2. Lakukan pembaruan sistem:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

### Langkah 2: Instalasi Dependensi
Untuk menjalankan LLaMA sebagai virtual assistant, instalasi Python, PyTorch, dan beberapa pustaka lainnya diperlukan.

1. Instal Python dan pip:
    ```bash
    sudo apt install python3 python3-pip -y
    ```

2. Instal pustaka yang dibutuhkan:
    ```bash
    sudo apt install portaudio19-dev build-essential libatlas-base-dev sox -y
    ```

3. Instal PyTorch (CPU-only) dan Transformers:
    ```bash
    pip install torch torchvision torchaudio transformers
    ```

4. Instal pustaka tambahan untuk input/output suara dan speech recognition:
    ```bash
    pip install SpeechRecognition pyaudio
    ```

### Langkah 3: Clone Repository LLaMA
Clone repository LLaMA dari GitHub untuk mendapatkan kode dan file model yang dibutuhkan.

1. Clone repository LLaMA:
    ```bash
    git clone https://github.com/facebookresearch/llama.git
    cd llama
    ```

2. Instal dependensi Python:
    ```bash
    pip install -r requirements.txt
    ```

### Langkah 4: Unduh Model LLaMA yang Lebih Kecil
Unduh model LLaMA yang lebih kecil seperti **7B** atau **13B** dari Hugging Face atau penyedia lainnya.

1. Daftar dan unduh model dari Hugging Face.
2. Pindahkan model ke penyimpanan SSD eksternal jika diperlukan untuk menghemat ruang di kartu MicroSD.

### Langkah 5: Kuantisasi Model (Opsional)
Untuk mengoptimalkan performa di Raspberry Pi, model dapat diubah menjadi kuantisasi 8-bit menggunakan pustaka **bitsandbytes**.

1. Instal bitsandbytes:
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
        prompt = input("Masukkan pertanyaan Anda: ")
        print(generate_text(prompt))
    ```

### Langkah 6: Konfigurasi Swap Memory
Tambahkan swap memory agar Raspberry Pi 5 memiliki memori yang cukup untuk menangani model besar.

1. Buat file swap 4GB:
    ```bash
    sudo fallocate -l 4G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    ```

2. Tambahkan swap ke `/etc/fstab` agar swap aktif setiap kali boot:
    ```bash
    /swapfile none swap sw 0 0
    ```

### Langkah 7: Konfigurasi Virtual Assistant
Siapkan kode untuk menerima input suara dan menghasilkan respons menggunakan model LLaMA.

1. Buat file Python `virtual_assistant.py`:
    ```python
    import speech_recognition as sr
    from transformers import LLaMATokenizer, LLaMAForCausalLM

    # Load LLaMA model and tokenizer
    model_path = "/path/to/7B-model"
    tokenizer = LLaMATokenizer.from_pretrained(model_path)
    model = LLaMAForCausalLM.from_pretrained(model_path)

    def generate_response(prompt):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=100)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Set up microphone and speech recognition
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    def listen_and_respond():
        with microphone as source:
            print("Mendengarkan...")
            audio = recognizer.listen(source)
            try:
                prompt = recognizer.recognize_google(audio, language="id-ID")
                print(f"Anda: {prompt}")
                response = generate_response(prompt)
                print(f"Asisten: {response}")
            except sr.UnknownValueError:
                print("Maaf, saya tidak bisa mendengar dengan jelas.")
            except sr.RequestError:
                print("Tidak dapat terhubung ke layanan pengenalan suara.")

    if __name__ == "__main__":
        while True:
            listen_and_respond()
    ```

### Langkah 8: Jalankan Virtual Assistant
1. Jalankan skrip **virtual_assistant.py**:
    ```bash
    python virtual_assistant.py
    ```

2. Berikan pertanyaan melalui mikrofon, dan LLaMA akan memberikan jawaban berdasarkan input yang diterima.

## Optimasi Performa
- **Batasi panjang prompt dan respons** untuk menghindari overloading pada Raspberry Pi.
- **Gunakan kuantisasi model** untuk menghemat memori.
- **Pastikan Raspberry Pi memiliki pendinginan yang baik** untuk mencegah throttling akibat panas berlebih.
- **Gunakan SSD eksternal** untuk swap memory yang lebih besar dan kecepatan akses yang lebih cepat.

## Kesimpulan
Dengan menggunakan versi LLaMA yang lebih kecil seperti **7B** atau **13B** dan mengoptimalkan model menggunakan kuantisasi serta swap memory, Raspberry Pi 5 dapat digunakan sebagai virtual assistant sederhana dalam mode offline. Namun, Anda harus menyesuaikan ekspektasi terkait performa karena keterbatasan hardware.
