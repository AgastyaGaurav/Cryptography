import streamlit as st
import crypto_utils

# Page Config
st.set_page_config(
    page_title="Secure Code Dashboard",
    page_icon="🔒",
    layout="centered"
)

st.title("🔒 Secure Code & File Dashboard")
st.markdown("Encrypt your sensitive source code, decrypt securely, and cross-verify file integrity using SHA-256 hashes.")

# Sidebar Navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Encrypt Code", "Decrypt Code", "Verify Integrity"])

# --- TAB 1: ENCRYPT ---
if choice == "Encrypt Code":
    st.header("📝 Encrypt Code Snippet")
    
    code_input = st.text_area("Enter your code snippet or text:", height=150, placeholder="def secure_function():\n    pass")
    password = st.text_input("Master Password", type="password", placeholder="Enter strong password")
    output_filename = st.text_input("Output Filename", value="secure_code.enc")
    
    if st.button("Encrypt and Generate File", type="primary"):
        if not code_input or not password or not output_filename:
            st.error("Please fill out all fields!")
        else:
            try:
                file_payload, file_hash = crypto_utils.encrypt_code(code_input, password)
                
                st.success("Encryption Successful!")
                st.markdown(f"**SHA-256 Integrity Hash:**")
                st.code(file_hash, language="text")
                
                # Download button for the encrypted file
                st.download_button(
                    label="📥 Download Encrypted File",
                    data=file_payload,
                    file_name=output_filename,
                    mime="application/octet-stream"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- TAB 2: DECRYPT ---
elif choice == "Decrypt Code":
    st.header("🔓 Decrypt Code File")
    
    uploaded_file = st.file_uploader("Upload your `.enc` file", type=["enc", "txt", "bin"])
    password = st.text_input("Master Password", type="password", placeholder="Enter your master password")
    
    if st.button("Decrypt and Authenticate", type="primary"):
        if not uploaded_file or not password:
            st.error("Please upload a file and enter your password.")
        else:
            try:
                file_bytes = uploaded_file.getvalue()
                decrypted_text = crypto_utils.decrypt_code(file_bytes, password)
                
                st.success("Authentication & Decryption Successful!")
                st.markdown("### Decrypted Code Output:")
                st.code(decrypted_text, language="python")
            except Exception as e:
                st.error(f"❌ {e}")

# --- TAB 3: VERIFY INTEGRITY ---
elif choice == "Verify Integrity":
    st.header("🛡️ Verify File Integrity (SHA-256)")
    
    verify_file = st.file_uploader("Upload file to inspect", type=["enc", "txt", "bin"], key="verify")
    expected_hash = st.text_input("Paste Expected SHA-256 Hash String", placeholder="e.g., 8f4343...").strip()
    
    if st.button("Check Integrity", type="primary"):
        if not verify_file or not expected_hash:
            st.error("Please provide both the file and the expected hash string.")
        else:
            file_bytes = verify_file.getvalue()
            current_hash = crypto_utils.calculate_file_hash_from_bytes(file_bytes)
            
            st.markdown(f"**Computed Hash:** `{current_hash}`")
            st.markdown(f"**Expected Hash:** `{expected_hash}`")
            
            if current_hash == expected_hash:
                st.success("✅ Integrity Verified! The file is completely authentic and untampered.")
            else:
                st.error("🚨 Warning: Hash mismatch! The file content has been altered or corrupted.")