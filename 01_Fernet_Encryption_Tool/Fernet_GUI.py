import os
import wave
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.fernet import Fernet

# ---------------- CRYPTOGRAPHY & STEGO LOGIC ----------------

def generate_fernet_key():
    """Generates a random Fernet key."""
    return Fernet.generate_key().decode()

def encrypt_message(message, key_str):
    """Encrypts text using a Fernet key."""
    try:
        f = Fernet(key_str.encode())
        encrypted_bytes = f.encrypt(message.encode())
        return encrypted_bytes.decode()  # Return as string
    except Exception:
        raise ValueError("Invalid Fernet Key! Must be a 32-byte base64 string.")

def decrypt_message(ciphertext, key_str):
    """Decrypts ciphertext using a Fernet key."""
    try:
        f = Fernet(key_str.encode())
        decrypted_bytes = f.decrypt(ciphertext.encode())
        return decrypted_bytes.decode()
    except Exception:
        raise ValueError("Decryption failed. Invalid key or corrupted data.")

def encode_audio(input_audio_path, output_audio_path, secret_message):
    song = wave.open(input_audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    secret_message += "###"
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    
    if len(binary_message) > len(frame_bytes):
        song.close()
        raise ValueError("Audio file is too small for this message!")

    for i, bit in enumerate(binary_message):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)
        
    modified_frames = bytes(frame_bytes)

    with wave.open(output_audio_path, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(modified_frames)
        
    song.close()

def decode_audio(encoded_audio_path):
    song = wave.open(encoded_audio_path, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    extracted_bits = [str(frame_bytes[i] & 1) for i in range(len(frame_bytes))]
    extracted_bits = "".join(extracted_bits)

    all_bytes = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]

    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if decoded_message.endswith("###"):
            break

    song.close()
    return decoded_message[:-3]


# ---------------- GUI APPLICATION ----------------

class EncryptedStegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Encrypted Audio Steganography")
        self.root.geometry("600x480")
        self.root.resizable(False, False)
        
        tab_control = ttk.Notebook(root)
        
        self.key_tab = ttk.Frame(tab_control)
        self.encode_tab = ttk.Frame(tab_control)
        self.decode_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.key_tab, text='  1. Key Generator  ')
        tab_control.add(self.encode_tab, text='  2. Encrypt & Hide  ')
        tab_control.add(self.decode_tab, text='  3. Extract & Decrypt  ')
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.setup_key_tab()
        self.setup_encode_tab()
        self.setup_decode_tab()

    # --- Key Gen Tab ---
    def setup_key_tab(self):
        ttk.Label(self.key_tab, text="Fernet Encryption Key Tool", font=("Arial", 12, "bold")).pack(pady=15)
        ttk.Label(self.key_tab, text="You need a key to encrypt or decrypt messages.\nGenerate one below and keep it secret!", justify="center").pack(pady=5)
        
        self.key_display = ttk.Entry(self.key_tab, width=50, justify="center")
        self.key_display.pack(pady=15)
        
        ttk.Button(self.key_tab, text="Generate New Key", command=self.generate_key_action).pack(pady=5)

    def generate_key_action(self):
        new_key = generate_fernet_key()
        self.key_display.delete(0, tk.END)
        self.key_display.insert(0, new_key)

    # --- Encode Tab ---
    def setup_encode_tab(self):
        # File Selection
        ttk.Label(self.encode_tab, text="Carrier WAV File:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.encode_input_entry = ttk.Entry(self.encode_tab, width=40)
        self.encode_input_entry.grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.encode_tab, text="Browse", command=self.browse_encode_input).grid(row=0, column=2, padx=5, pady=10)

        # Fernet Key Input
        ttk.Label(self.encode_tab, text="Encryption Key:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.encode_key_entry = ttk.Entry(self.encode_tab, width=40, show="*")
        self.encode_key_entry.grid(row=1, column=1, padx=5, pady=5)

        # Secret Message Input
        ttk.Label(self.encode_tab, text="Secret Message:").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.message_text = tk.Text(self.encode_tab, width=38, height=8, wrap="word")
        self.message_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # Action Button
        ttk.Button(self.encode_tab, text="Encrypt & Save As...", command=self.process_encoding).grid(row=3, column=1, pady=15, sticky="e")

    def browse_encode_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Wav Files", "*.wav")])
        if file_path:
            self.encode_input_entry.delete(0, tk.END)
            self.encode_input_entry.insert(0, file_path)

    def process_encoding(self):
        input_file = self.encode_input_entry.get()
        key = self.encode_key_entry.get().strip()
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid carrier WAV file.")
            return
        if not key:
            messagebox.showerror("Error", "Please enter a valid Fernet Key.")
            return
        if not message:
            messagebox.showerror("Error", "Please enter a message.")
            return
            
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wav Files", "*.wav")])
        if output_file:
            try:
                # First step: Encrypt the message text
                encrypted_message = encrypt_message(message, key)
                # Second step: Hide the encrypted text into the audio
                encode_audio(input_file, output_file, encrypted_message)
                
                messagebox.showinfo("Success", "Message encrypted and hidden successfully!")
                self.message_text.delete("1.0", tk.END)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # --- Decode Tab ---
    def setup_decode_tab(self):
        # File Selection
        ttk.Label(self.decode_tab, text="Stego WAV File:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.decode_input_entry = ttk.Entry(self.decode_tab, width=40)
        self.decode_input_entry.grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(self.decode_tab, text="Browse", command=self.browse_decode_input).grid(row=0, column=2, padx=5, pady=10)

        # Fernet Key Input
        ttk.Label(self.decode_tab, text="Decryption Key:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.decode_key_entry = ttk.Entry(self.decode_tab, width=40, show="*")
        self.decode_key_entry.grid(row=1, column=1, padx=5, pady=5)

        # Decode Button
        ttk.Button(self.decode_tab, text="Extract & Decrypt Message", command=self.process_decoding).grid(row=2, column=1, pady=10, sticky="w")

        # Result Output
        ttk.Label(self.decode_tab, text="Decrypted Text:").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
        self.result_text = tk.Text(self.decode_tab, width=38, height=8, wrap="word", state="disabled")
        self.result_text.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

    def browse_decode_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("Wav Files", "*.wav")])
        if file_path:
            self.decode_input_entry.delete(0, tk.END)
            self.decode_input_entry.insert(0, file_path)

    def process_decoding(self):
        input_file = self.decode_input_entry.get()
        key = self.decode_key_entry.get().strip()
        
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Please select a valid audio file.")
            return
        if not key:
            messagebox.showerror("Error", "Please enter the decryption key.")
            return
            
        try:
            # First step: Pull raw text from the audio's LSB bytes
            hidden_ciphertext = decode_audio(input_file)
            
            if not hidden_ciphertext:
                raise ValueError("No hidden data payload detected in this audio.")
                
            # Second step: Decrypt the text back to normal string
            decrypted_msg = decrypt_message(hidden_ciphertext, key)
            
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", decrypted_msg)
            self.result_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptedStegoApp(root)
    root.mainloop()
