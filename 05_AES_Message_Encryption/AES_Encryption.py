import os
import base64
import tkinter as tk
from tkinter import ttk, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESTool:
    def __init__(self, key_size=256, mode='CBC'):
        self.key_bytes = key_size // 8
        self.mode = mode.upper()

    def _derive_key(self, password: str) -> bytes:
        encoded = password.encode('utf-8')
        if len(encoded) >= self.key_bytes:
            return encoded[:self.key_bytes]
        return encoded.ljust(self.key_bytes, b'\0')

    def encrypt(self, plain_text: str, password: str) -> str:
        key = self._derive_key(password)
        data = plain_text.encode('utf-8')

        if self.mode == 'CBC':
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
            return base64.b64encode(iv + encrypted_data).decode('utf-8')
            
        elif self.mode == 'GCM':
            nonce = os.urandom(12)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            encrypted_data, tag = cipher.encrypt_and_digest(data)
            return base64.b64encode(nonce + tag + encrypted_data).decode('utf-8')

    def decrypt(self, cipher_text: str, password: str) -> str:
        key = self._derive_key(password)
        try:
            raw_data = base64.b64decode(cipher_text.encode('utf-8'))
        except Exception:
            raise ValueError("Invalid Base64 string.")

        if self.mode == 'CBC':
            if len(raw_data) < 16:
                raise ValueError("Ciphertext too short.")
            iv = raw_data[:16]
            encrypted_data = raw_data[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
            
        elif self.mode == 'GCM':
            if len(raw_data) < 28:
                raise ValueError("Ciphertext too short.")
            nonce = raw_data[:12]
            tag = raw_data[12:28]
            encrypted_data = raw_data[28:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(encrypted_data, tag).decode('utf-8')


class AESDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AES Crypto Dashboard")
        self.geometry("600Dimensions" if not hasattr(self, 'geometry') else "620x580")
        self.resizable(False, False)
        
        # Apply a clean, flat style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()

    def create_widgets(self):
        # --- Main Container ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_lbl = ttk.Label(main_frame, text="AES Encryption / Decryption Tool", font=("Helvetica", 16, "bold"))
        title_lbl.pack(pady=(0, 20))

        # --- Configurations Frame ---
        config_frame = ttk.LabelFrame(main_frame, text=" 1. Configure AES Options ", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Cipher Mode Choice
        ttk.Label(config_frame, text="Cipher Mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.mode_var = tk.StringVar(value="GCM")
        mode_combo = ttk.Combobox(config_frame, textvariable=self.mode_var, values=["GCM", "CBC"], state="readonly", width=10)
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Key Size Choice
        ttk.Label(config_frame, text="Key Size (Bits):").grid(row=0, column=2, sticky=tk.W, padx=25, pady=5)
        self.keysize_var = tk.IntVar(value=256)
        keysize_combo = ttk.Combobox(config_frame, textvariable=self.keysize_var, values=[128, 192, 256], state="readonly", width=10)
        keysize_combo.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        # Action Choice (Encrypt vs Decrypt)
        ttk.Label(config_frame, text="Operation:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.action_var = tk.StringVar(value="Encrypt")
        action_combo = ttk.Combobox(config_frame, textvariable=self.action_var, values=["Encrypt", "Decrypt"], state="readonly", width=10)
        action_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Inputs Frame ---
        input_frame = ttk.LabelFrame(main_frame, text=" 2. Inputs ", padding="15")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Password Input
        ttk.Label(input_frame, text="Secret Password / Key:").pack(anchor=tk.W, padx=5, pady=(0, 2))
        self.pass_entry = ttk.Entry(input_frame, show="*", font=("Helvetica", 11))
        self.pass_entry.pack(fill=tk.X, padx=5, pady=(0, 10))

        # Data Input Textbox
        ttk.Label(input_frame, text="Data (Plaintext to Encrypt OR Base64 Ciphertext to Decrypt):").pack(anchor=tk.W, padx=5, pady=(0, 2))
        self.input_text = tk.Text(input_frame, height=5, font=("Helvetica", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5)

        # --- Action Button ---
        self.process_btn = ttk.Button(main_frame, text="RUN OPERATION", command=self.process_crypto)
        self.process_btn.pack(fill=tk.X, pady=(0, 15))

        # --- Outputs Frame ---
        output_frame = ttk.LabelFrame(main_frame, text=" 3. Output Result ", padding="15")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(output_frame, height=5, font=("Helvetica", 10), bg="#f4f4f4")
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5)

    def process_crypto(self):
        # Clear previous output
        self.output_text.delete("1.0", tk.END)

        # Gather inputs
        mode = self.mode_var.get()
        key_size = self.keysize_var.get()
        action = self.action_var.get()
        password = self.pass_entry.get()
        data = self.input_text.get("1.0", tk.END).strip()

        # Input validations
        if not password:
            messagebox.showerror("Error", "Password/Key field cannot be empty.")
            return
        if not data:
            messagebox.showerror("Error", "Data input field cannot be empty.")
            return

        try:
            # Instantiate engine dynamically based on chosen GUI configurations
            crypto_engine = AESTool(key_size=key_size, mode=mode)
            
            if action == "Encrypt":
                result = crypto_engine.encrypt(data, password)
            else:
                result = crypto_engine.decrypt(data, password)

            # Insert resulting string into the output box
            self.output_text.insert("1.0", result)

        except Exception as e:
            # Catch standard padding errors, incorrect keys, or corrupt base64 strings safely
            messagebox.showerror("Cryptographic Failure", f"Failed to {action.lower()} data.\n\nReason: {str(e)}")

if __name__ == "__main__":
    app = AESDashboard()
    app.mainloop()
