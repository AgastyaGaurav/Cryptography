import tkinter as tk
from tkinter import messagebox
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generate RSA Keys
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# Encryption Function
def encrypt():
    message = txtMessage.get("1.0", tk.END).strip()

    if message == "":
        messagebox.showerror("Error", "Enter a message")
        return

    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(message.encode())

    txtResult.delete("1.0", tk.END)
    txtResult.insert(tk.END, base64.b64encode(encrypted).decode())

# Decryption Function
def decrypt():
    encrypted_text = txtResult.get("1.0", tk.END).strip()

    if encrypted_text == "":
        messagebox.showerror("Error", "Nothing to decrypt")
        return

    try:
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_text))

        txtMessage.delete("1.0", tk.END)
        txtMessage.insert(tk.END, decrypted.decode())

    except Exception:
        messagebox.showerror("Error", "Invalid encrypted text")

# GUI
root = tk.Tk()
root.title("RSA Encryption")
root.geometry("600x450")

tk.Label(root, text="Message").pack()

txtMessage = tk.Text(root, height=6, width=60)
txtMessage.pack(pady=5)

frame = tk.Frame(root)
frame.pack()

btnEncrypt = tk.Button(frame, text="Encrypt", command=encrypt)
btnEncrypt.grid(row=0, column=0, padx=10)

btnDecrypt = tk.Button(frame, text="Decrypt", command=decrypt)
btnDecrypt.grid(row=0, column=1, padx=10)

tk.Label(root, text="Encrypted Text").pack()

txtResult = tk.Text(root, height=8, width=60)
txtResult.pack(pady=5)

root.mainloop()
