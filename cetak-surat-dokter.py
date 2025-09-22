import tkinter as tk
from tkinter import messagebox
from datetime import date, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Image
import os
import platform

# --- Fungsi untuk mengubah format tanggal ke Bahasa Indonesia ---
def format_tanggal_indonesia(tanggal_obj):
    nama_bulan = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    hari = tanggal_obj.day
    bulan = nama_bulan[tanggal_obj.month - 1]
    tahun = tanggal_obj.year
    return f"{hari} {bulan} {tahun}"

# --- Fungsi utama untuk membuat PDF (dipanggil oleh tombol) ---
def cetak_surat():
    nama_pasien = entry_nama_pasien.get()
    jenis_kelamin = var_jenis_kelamin.get()
    umur_pasien = entry_umur.get()
    alamat_pasien = entry_alamat.get()
    
    if not all([nama_pasien, jenis_kelamin, umur_pasien, alamat_pasien, entry_jumlah_hari.get(), entry_nama_dokter.get(), entry_nip_dokter.get()]):
        messagebox.showwarning("Input Kurang", "Mohon lengkapi semua data!")
        return
    
    try:
        jumlah_hari = int(entry_jumlah_hari.get())
    except ValueError:
        messagebox.showerror("Input Salah", "Jumlah hari harus berupa angka!")
        return

    nama_dokter = entry_nama_dokter.get()
    nip_dokter = entry_nip_dokter.get()

    tanggal_terbit_obj = date.today()
    tanggal_terbit = format_tanggal_indonesia(tanggal_terbit_obj)
    tanggal_mulai_obj = date.today()
    tanggal_mulai = format_tanggal_indonesia(tanggal_mulai_obj)
    tanggal_selesai_obj = tanggal_mulai_obj + timedelta(days=jumlah_hari - 1)
    tanggal_selesai = format_tanggal_indonesia(tanggal_selesai_obj)

    nama_file_pdf = f"Surat_Sakit_{nama_pasien.replace(' ', '_')}.pdf"

    doc = SimpleDocTemplate(
        nama_file_pdf,
        pagesize=A4,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Header1', fontSize=12, leading=14, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Header2', fontSize=8, leading=12, alignment=TA_CENTER, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='JudulSurat', fontSize=14, leading=16, alignment=TA_CENTER, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='NormalLeft', fontSize=10, leading=14, alignment=TA_LEFT, fontName='Helvetica'))
    styles.add(ParagraphStyle(name='NormalRight', fontSize=10, leading=14, alignment=TA_RIGHT, fontName='Helvetica'))

    story = []

    # Tambahkan logo di kiri & kanan
    logo_kalbar = Image("logo-kalbar.png", width=50, height=50)
    logo_rsud = Image("logo-rsud.png", width=50, height=50)

    from reportlab.platypus import Table

    # Buat tabel 1 baris, 3 kolom: logo kiri, teks tengah, logo kanan
    header_table = Table(
        [[logo_kalbar,
        Paragraph(
            "<b>PEMERINTAH PROVINSI KALIMANTAN BARAT<br/>"
            "RUMAH SAKIT UMUM DAERAH DOKTER SOEDARSO</b>",
            styles['Header1']),
        logo_rsud]],
        colWidths=[1*inch, 4.5*inch, 1*inch]
    )
    header_table.hAlign = 'CENTER'

    story.append(header_table)
    story.append(Paragraph("JL. DOKTER SOEDARSO NO. 1 - TELP. (0561) 737701 PONTIANAK 78124", styles['Header2']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("<hr/>", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("<b>SURAT KETERANGAN SAKIT</b>", styles['JudulSurat']))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Yang bertanda tangan di bawah ini. Dokter RSUD dr. Soedarso, menerangkan bahwa :", styles['NormalLeft']))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"Nama &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {nama_pasien} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Jenis Kelamin : {jenis_kelamin}", styles['NormalLeft']))
    story.append(Paragraph(f"Umur &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {umur_pasien} tahun", styles['NormalLeft']))
    story.append(Paragraph(f"Alamat &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {alamat_pasien}", styles['NormalLeft']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Berhubung sakit, perlu istirahat / dirawat selama {jumlah_hari} hari.", styles['NormalLeft']))
    story.append(Paragraph(f"Terhitung mulai tanggal {tanggal_mulai} s/d {tanggal_selesai}.", styles['NormalLeft']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Demikian surat keterangan ini dibuat untuk dapat dipergunakan seperlunya.", styles['NormalLeft']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"Pontianak, {tanggal_terbit}", styles['NormalRight']))
    story.append(Paragraph("Dokter yang merawat,", styles['NormalRight']))
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph(f"( {nama_dokter} )", styles['NormalRight']))
    story.append(Paragraph(f"NIP. {nip_dokter}", styles['NormalRight']))

    try:
        doc.build(story)
        messagebox.showinfo("Berhasil!", f"Surat berhasil dibuat dan disimpan di file PDF: {nama_file_pdf}")
        if platform.system() == 'Windows':
            os.startfile(nama_file_pdf)
        elif platform.system() == 'Darwin':
            os.system(f'open {nama_file_pdf}')
        else:
            os.system(f'xdg-open {nama_file_pdf}')
    except Exception as e:
        messagebox.showerror("Terjadi Kesalahan", f"Terjadi kesalahan saat membuat PDF: {e}")

# Membuat Jendela Utama GUI
root = tk.Tk()
root.title("Aplikasi Cetak Surat Keterangan Sakit")
root.geometry("600x550")
root.config(bg="#f0f0f0")

# Membuat frame utama untuk konten
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(expand=True, padx=20, pady=20)

# Label judul aplikasi
title_label = tk.Label(main_frame, text="Surat Keterangan Sakit", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=(0, 20))

# --- FRAME UNTUK DATA PASIEN ---
pasien_frame = tk.LabelFrame(main_frame, text="Data Pasien", font=("Helvetica", 12, "bold"), bg="white", padx=15, pady=10)
pasien_frame.pack(fill="x", pady=10)

labels_pasien = ["Nama Pasien:", "Jenis Kelamin:", "Umur Pasien (angka):", "Alamat Pasien:"]
entries_pasien = {}
entry_list_pasien = []
row_num = 0

for label_text in labels_pasien:
    label = tk.Label(pasien_frame, text=label_text, font=("Helvetica", 10), bg="white")
    label.grid(row=row_num, column=0, sticky="w", padx=5, pady=5)
    
    if label_text == "Jenis Kelamin:":
        var_jenis_kelamin = tk.StringVar(value="Laki-laki")
        radio_frame = tk.Frame(pasien_frame, bg="white")
        radio_frame.grid(row=row_num, column=1, sticky="w", padx=5, pady=5)
        tk.Radiobutton(radio_frame, text="Laki-laki", variable=var_jenis_kelamin, value="Laki-laki", bg="white", font=("Helvetica", 10)).pack(side="left", padx=(0, 15))
        tk.Radiobutton(radio_frame, text="Perempuan", variable=var_jenis_kelamin, value="Perempuan", bg="white", font=("Helvetica", 10)).pack(side="left")
    else:
        entry = tk.Entry(pasien_frame, width=40, font=("Helvetica", 10))
        entry.grid(row=row_num, column=1, padx=5, pady=5)
        entry_list_pasien.append(entry)
        if label_text == "Nama Pasien:":
            entry_nama_pasien = entry
        elif label_text == "Umur Pasien (angka):":
            entry_umur = entry
        elif label_text == "Alamat Pasien:":
            entry_alamat = entry
            
    row_num += 1

# --- FRAME UNTUK KETERANGAN MEDIS & DOKTER ---
medis_frame = tk.LabelFrame(main_frame, text="Keterangan Medis & Dokter", font=("Helvetica", 12, "bold"), bg="white", padx=15, pady=10)
medis_frame.pack(fill="x", pady=10)

labels_medis = ["Jumlah Hari Istirahat:", "Nama Dokter:", "NIP Dokter:"]
entries_medis = {}
entry_list_medis = []
row_num = 0

for label_text in labels_medis:
    label = tk.Label(medis_frame, text=label_text, font=("Helvetica", 10), bg="white")
    label.grid(row=row_num, column=0, sticky="w", padx=5, pady=5)
    entry = tk.Entry(medis_frame, width=40, font=("Helvetica", 10))
    entry.grid(row=row_num, column=1, padx=5, pady=5)
    entry_list_medis.append(entry)
    
    if label_text == "Jumlah Hari Istirahat:":
        entry_jumlah_hari = entry
    elif label_text == "Nama Dokter:":
        entry_nama_dokter = entry
    elif label_text == "NIP Dokter:":
        entry_nip_dokter = entry
        
    row_num += 1

# Tombol untuk mencetak surat
tombol_cetak = tk.Button(main_frame, text="Cetak Surat", command=cetak_surat, bg="#4CAF50", fg="white", font=('Helvetica', 12, 'bold'), activebackground="#45a049")
tombol_cetak.pack(pady=20, ipadx=20, ipady=5)

root.mainloop()
