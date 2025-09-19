from datetime import date, timedelta, datetime
from reportlab.lib.pagesizes import A4 # Menggunakan ukuran kertas A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch # Untuk mengatur margin atau spasi jika perlu
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT # Untuk perataan teks
import os

# --- Bagian 1: Mengumpulkan Input dari Pengguna ---
nama_pasien = input("Nama pasien: ")
jenis_kelamin = input("Jenis kelamin pasien (L/P): ")
umur_pasien = input("Umur pasien (angka): ")
alamat_pasien = input("Alamat pasien: ")
jumlah_hari = int(input("Jumlah hari istirahat (angka): "))

nama_dokter = input("Nama dokter: ")
nip_dokter = input("NIP dokter: ")

# --- Bagian 2: Menghitung Tanggal Otomatis ---
# Tanggal penerbitan surat otomatis diisi dengan tanggal hari ini
tanggal_terbit = date.today().strftime("%d-%m-%Y")

# Mengubah tanggal mulai dari string ke objek date
tanggal_mulai_str = date.today().strftime("%d-%m-%Y")
tanggal_mulai_obj = datetime.strptime(tanggal_mulai_str, "%d-%m-%Y").date()

# Menghitung tanggal selesai dengan menambahkan jumlah hari ke tanggal mulai
# timedelta(days=jumlah_hari - 1) karena hari pertama sudah dihitung
tanggal_selesai_obj = tanggal_mulai_obj + timedelta(days=jumlah_hari - 1)
tanggal_selesai = tanggal_selesai_obj.strftime("%d-%m-%Y")

# --- Bagian 3: Mengatur Format dan Gaya untuk PDF ---
# Nama file PDF
nama_file_pdf = f"Surat_Sakit_{nama_pasien.replace(' ', '_')}.pdf"

# Buat objek dokumen PDF
# margin: left, right, top, bottom
doc = SimpleDocTemplate(
    nama_file_pdf,
    pagesize=A4,
    leftMargin=0.8*inch,
    rightMargin=0.8*inch,
    topMargin=0.5*inch,
    bottomMargin=0.5*inch
)

styles = getSampleStyleSheet()

# Gaya kustom untuk judul (bold, tengah)
styles.add(ParagraphStyle(name='Header1',
                          fontSize=12,
                          leading=14,
                          alignment=TA_CENTER,
                          fontName='Helvetica-Bold'))

styles.add(ParagraphStyle(name='Header2',
                          fontSize=10,
                          leading=12,
                          alignment=TA_CENTER,
                          fontName='Helvetica'))

styles.add(ParagraphStyle(name='JudulSurat',
                          fontSize=14,
                          leading=16,
                          alignment=TA_CENTER,
                          fontName='Helvetica-Bold'))

styles.add(ParagraphStyle(name='NormalLeft',
                          fontSize=10,
                          leading=14,
                          alignment=TA_LEFT,
                          fontName='Helvetica'))

styles.add(ParagraphStyle(name='NormalJustify',
                          fontSize=10,
                          leading=14,
                          alignment=TA_LEFT, # Bisa juga TA_JUSTIFY kalau ingin rata kanan kiri
                          fontName='Helvetica'))

styles.add(ParagraphStyle(name='NormalRight',
                          fontSize=10,
                          leading=14,
                          alignment=TA_RIGHT,
                          fontName='Helvetica'))

# List untuk menampung elemen-elemen yang akan masuk ke PDF
story = []

# --- Bagian 4: Menambahkan Konten ke PDF ---

# Header Surat
story.append(Paragraph("<b>PEMERINTAH PROVINSI KALIMANTAN BARAT</b>", styles['Header1']))
story.append(Paragraph("<b>RUMAH SAKIT UMUM DAERAH DOKTER SOEDARSO</b>", styles['Header1']))
story.append(Paragraph("JL. DOKTER SOEDARSO NO. 1 - TELP. (0561) 737701 PONTIANAK 78124", styles['Header2']))
story.append(Spacer(1, 0.2 * inch)) # Spasi
story.append(Paragraph("<hr/>", styles['Normal'])) # Garis pemisah
story.append(Spacer(1, 0.2 * inch))

# Judul Surat
story.append(Paragraph("<b>SURAT KETERANGAN SAKIT</b>", styles['JudulSurat']))
story.append(Spacer(1, 0.3 * inch))

# Isi Surat
story.append(Paragraph("Yang bertanda tangan di bawah ini. Dokter RSUD dr. Soedarso, menerangkan bahwa :", styles['NormalLeft']))
story.append(Spacer(1, 0.1 * inch))

# Detail Pasien (menggunakan spasi manual untuk perataan sederhana)
story.append(Paragraph(f"Nama &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {nama_pasien} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; L / P : {jenis_kelamin}", styles['NormalLeft']))
story.append(Paragraph(f"Umur &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {umur_pasien} tahun", styles['NormalLeft']))
story.append(Paragraph(f"Alamat &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {alamat_pasien}", styles['NormalLeft']))
story.append(Spacer(1, 0.2 * inch))

# Keterangan Istirahat
story.append(Paragraph(f"Berhubung sakit, perlu istirahat / dirawat selama {jumlah_hari} hari.", styles['NormalLeft']))
story.append(Paragraph(f"Terhitung mulai tanggal {tanggal_mulai_str} s/d {tanggal_selesai}.", styles['NormalLeft']))
story.append(Spacer(1, 0.2 * inch))
story.append(Paragraph("Demikian surat keterangan ini dibuat untuk dapat dipergunakan seperlunya.", styles['NormalLeft']))
story.append(Spacer(1, 0.5 * inch))

# Bagian Penutup (lokasi dan tanda tangan)
story.append(Paragraph(f"Pontianak, {tanggal_terbit}", styles['NormalRight']))
story.append(Paragraph("Dokter yang merawat,", styles['NormalRight']))
story.append(Spacer(1, 0.8 * inch)) # Spasi untuk tanda tangan
story.append(Paragraph(f"( {nama_dokter} )", styles['NormalRight']))
story.append(Paragraph(f"NIP. {nip_dokter}", styles['NormalRight']))

# --- Bagian 5: Membuat PDF ---
try:
    doc.build(story)
    print(f"\nSurat berhasil dibuat dan disimpan di file PDF: {nama_file_pdf}")
    print("Silakan cek folder tempat program dijalankan.")
except Exception as e:
    print(f"\nTerjadi kesalahan saat membuat PDF: {e}")

# Opsional: Membuka file PDF setelah dibuat (tergantung OS)
import platform
if platform.system() == 'Windows':
    os.startfile(nama_file_pdf)
elif platform.system() == 'Darwin': # macOS
    os.system(f'open {nama_file_pdf}')
else: # Linux
    os.system(f'xdg-open {nama_file_pdf}')
