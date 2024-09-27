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
