import os
import platform
import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# --- Bagian 1: Logika Pembuatan PDF (dijadikan sebuah fungsi) ---

def format_tanggal_indonesia(tanggal_obj):
    nama_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{tanggal_obj.day} {nama_bulan[tanggal_obj.month - 1]} {tanggal_obj.year}"

def buat_surat_pdf(nama_pasien, jenis_kelamin, umur_pasien, alamat_pasien, jumlah_hari, nama_dokter, nip_dokter):
    try:
        nama_file_pdf = f"Surat_Sakit_{nama_pasien.replace(' ', '_')}.pdf"
        doc = SimpleDocTemplate(nama_file_pdf, pagesize=A4, leftMargin=0.8*inch, rightMargin=0.8*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='HeaderStyle', fontSize=10, leading=12, alignment=TA_CENTER, fontName='Helvetica'))
        styles.add(ParagraphStyle(name='JudulSurat', fontSize=14, leading=18, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=0.2*inch))
        styles.add(ParagraphStyle(name='NormalLeft', fontSize=11, leading=15, alignment=TA_LEFT, fontName='Helvetica'))
        styles.add(ParagraphStyle(name='NormalRight', fontSize=11, leading=15, alignment=TA_RIGHT, fontName='Helvetica'))

        story = []

        # --- Header / Kop Surat ---
        logo1_path = "logo_kalbar.png"
        logo2_path = "logo_rsud.png"
        if not os.path.exists(logo1_path) or not os.path.exists(logo2_path):
            messagebox.showerror("Error", f"File logo tidak ditemukan! Pastikan '{logo1_path}' dan '{logo2_path}' ada di folder yang sama.")
            return

        logo1 = Image(logo1_path, width=0.8*inch, height=0.8*inch)
        logo2 = Image(logo2_path, width=0.8*inch, height=0.8*inch)
        header_text = Paragraph("<b>PEMERINTAH PROVINSI KALIMANTAN BARAT</b><br/><b>RUMAH SAKIT UMUM DAERAH DOKTER SOEDARSO</b><br/>JL. DOKTER SOEDARSO NO. 1 - TELP. (0561) 737701 PONTIANAK 78124", styles['HeaderStyle'])
        
        doc_width = A4[0] - doc.leftMargin - doc.rightMargin
        col_widths = [0.8*inch, doc_width - 1.6*inch, 0.8*inch]
        header_table = Table([[logo1, header_text, logo2]], colWidths=col_widths)
        header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN', (0,0), (0,0), 'LEFT'), ('ALIGN', (1,0), (1,0), 'CENTER'), ('ALIGN', (2,0), (2,0), 'RIGHT')]))
        story.append(header_table)
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("<hr width='100%' color='black' size='2px'/>", styles['NormalLeft']))
        story.append(Spacer(1, 0.1*inch))

        # --- Isi Surat ---
        tanggal_mulai_obj = date.today()
        tanggal_selesai_obj = tanggal_mulai_obj + timedelta(days=int(jumlah_hari) - 1)
        
        story.append(Paragraph("<u>SURAT KETERANGAN SAKIT</u>", styles['JudulSurat']))
        story.append(Paragraph("Yang bertanda tangan di bawah ini, Dokter RSUD dr. Soedarso, menerangkan bahwa:", styles['NormalLeft']))
        story.append(Spacer(1, 0.2*inch))

        patient_details_data = [
            ['Nama', f': {nama_pasien}', 'L/P', f': {jenis_kelamin}'],
            ['Umur', f': {umur_pasien} tahun', '', ''],
            ['Alamat', f': {alamat_pasien}', '', '']
        ]
        patient_table = Table(patient_details_data, colWidths=[0.8*inch, 3.5*inch, 0.5*inch, 1.5*inch])
        patient_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,0), (-1,-1), 11), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
        story.append(patient_table)
        story.append(Spacer(1, 0.2*inch))

        story.append(Paragraph(f"Berhubung sakit, perlu istirahat / dirawat selama <b>{jumlah_hari} hari</b>.", styles['NormalLeft']))
        story.append(Paragraph(f"Terhitung mulai tanggal {format_tanggal_indonesia(tanggal_mulai_obj)} s/d {format_tanggal_indonesia(tanggal_selesai_obj)}.", styles['NormalLeft']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("Demikian surat keterangan ini dibuat untuk dapat dipergunakan seperlunya.", styles['NormalLeft']))
        story.append(Spacer(1, 0.5*inch))
        
        story.append(Paragraph(f"Pontianak, {format_tanggal_indonesia(date.today())}", styles['NormalRight']))
        story.append(Paragraph("Dokter yang merawat,", styles['NormalRight']))
        story.append(Spacer(1, 0.8*inch))
        story.append(Paragraph(f"<b>( {nama_dokter} )</b>", styles['NormalRight']))
        story.append(Paragraph(f"NIP. {nip_dokter}", styles['NormalRight']))

        doc.build(story)

        # Otomatis membuka file
        if platform.system() == 'Windows': os.startfile(nama_file_pdf)
        elif platform.system() == 'Darwin': os.system(f'open "{nama_file_pdf}"')
        else: os.system(f'xdg-open "{nama_file_pdf}"')
        
        return True
    except Exception as e:
        messagebox.showerror("Pembuatan PDF Gagal", f"Terjadi kesalahan:\n{e}")
        return False

# --- Bagian 2: Form GUI dengan Tkinter ---

# GANTI FUNGSI LAMA ANDA DENGAN YANG INI
def on_generate_click():
    # Ambil semua data dari form
    data = {name: entry.get() for name, entry in entries.items()}
    
    # Validasi input tidak boleh kosong
    for name, value in data.items():
        if not value:
            # Mengubah nama kunci menjadi lebih mudah dibaca untuk pesan error
            friendly_name = name.replace('_', ' ').title()
            messagebox.showwarning("Input Tidak Lengkap", f"Harap isi kolom '{friendly_name}' terlebih dahulu.")
            return

    # --- BAGIAN YANG DIPERBAIKI ---
    try:
        # 1. Validasi menggunakan kunci yang BENAR: 'jumlah_hari_istirahat'
        int(data['jumlah_hari_istirahat'])
    except ValueError:
        messagebox.showwarning("Input Salah", "Kolom 'Jumlah Hari Istirahat' harus diisi dengan angka.")
        return
    
    # 2. Ganti nama kunci agar sesuai dengan parameter fungsi PDF
    data['jumlah_hari'] = data.pop('jumlah_hari_istirahat')
    
    # Panggil fungsi untuk membuat PDF dengan data yang sudah benar
    buat_surat_pdf(**data)

# Setup window utama
root = tk.Tk()
root.title("Generator Surat Sakit")
root.geometry("400x300") # Ukuran window
root.resizable(False, False)

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(fill="both", expand=True)

# Daftar input yang dibutuhkan
labels = [
    "Nama Pasien", "Jenis Kelamin (L/P)", "Umur Pasien",
    "Alamat Pasien", "Jumlah Hari Istirahat", "Nama Dokter", "NIP Dokter"
]

entries = {}
# Buat label dan entry box untuk setiap input
for i, text in enumerate(labels):
    label_key = text.lower().replace(" (l/p)", "").replace(" ", "_")
    
    label = tk.Label(frame, text=f"{text}:")
    label.grid(row=i, column=0, sticky="w", pady=2)
    
    entry = tk.Entry(frame, width=40)
    entry.grid(row=i, column=1, sticky="w", pady=2)
    entries[label_key] = entry

# Tombol untuk membuat PDF
generate_button = tk.Button(frame, text="Buat dan Buka PDF", command=on_generate_click, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
generate_button.grid(row=len(labels), columnspan=2, sticky="ew", pady=15)

# Jalankan aplikasi GUI
root.mainloop()
