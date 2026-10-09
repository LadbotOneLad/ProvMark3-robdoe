import qrcode
import json
import os

def generate_sovereign_qr():
    # Target URL pointing to your live proof or robdoe.com repository endpoint
    target_url = "https://github.com/backupsonbackupsrobby-cyber/robdoerootauthority/blob/master/SOVEREIGN_VALUE_MANIFEST.md"
    
    print(f"[*] Generating sovereign QR code for: {target_url}")
    
    # Configure QR code layout for high density and reliability
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    # Generate image and save to disk
    img = qr.make_image(fill_color="black", back_color="white")
    output_path = "sovereign_proof_qr.png"
    img.save(output_path)
    
    print(f"[✔] QR Code locked to disk: {output_path}")

if __name__ == "__main__":
    generate_sovereign_qr()
