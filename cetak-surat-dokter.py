from datetime import date, timedelta, datetime

# --- Bagian 1: Mengumpulkan Input dari Pengguna ---
nama_pasien = input("Masukkan nama pasien: ")
jenis_kelamin = input("Masukkan jenis kelamin pasien (Lk/Pr): ")
umur_pasien = input("Masukkan umur pasien (angka): ")
alamat_pasien = input("Masukkan alamat pasien: ")

# Input jumlah hari dan tanggal mulai
jumlah_hari = int(input("Masukkan jumlah hari istirahat (angka): "))
tanggal_mulai_str = date.today().strftime("%d-%m-%Y")

nama_dokter = input("Masukkan nama dokter: ")
nip_dokter = input("Masukkan NIP dokter: ")

# --- Bagian 2: Menghitung Tanggal Otomatis ---
# Tanggal penerbitan surat otomatis diisi dengan tanggal hari ini
tanggal_terbit = date.today().strftime("%d-%m-%Y")

# Mengubah input tanggal mulai dari string ke objek date
tanggal_mulai_obj = datetime.strptime(tanggal_mulai_str, "%d-%m-%Y").date()

# Menghitung tanggal selesai dengan menambahkan jumlah hari ke tanggal mulai
# timedelta(days=jumlah_hari - 1) karena hari pertama sudah dihitung
tanggal_selesai_obj = tanggal_mulai_obj + timedelta(days=jumlah_hari - 1)
tanggal_selesai = tanggal_selesai_obj.strftime("%d-%m-%Y")

# --- Bagian 3: Menyiapkan dan Mengisi Template Surat ---
template_surat = f"""
            PEMERINTAH PROVINSI KALIMANTAN BARAT
        RUMAH SAKIT UMUM DAERAH DOKTER SOEDARSO
        JL. DOKTER SOEDARSO NO. 1 - TELP. (0561) 737701 PONTIANAK 78124

                    SURAT KETERANGAN SAKIT

Yang bertanda tangan di bawah ini. Dokter RSUD dr. Soedarso, menerangkan bahwa :

Nama            : {nama_pasien}                              Lk / Pr : {jenis_kelamin}
Umur            : {umur_pasien} tahun
Alamat          : {alamat_pasien}

Berhubung sakit, perlu istirahat / dirawat selama {jumlah_hari} hari.
Terhitung mulai tanggal {tanggal_mulai_str} s/d {tanggal_selesai}.
Demikian surat keterangan ini dibuat untuk dapat dipergunakan seperlunya.

                                                Pontianak, {tanggal_terbit}
                                                Dokter yang merawat,


                                                ( {nama_dokter} )
                                                NIP. {nip_dokter}
"""

# --- Bagian 4: Mencetak Surat ke File ---
nama_file = f"Surat_Sakit_{nama_pasien.replace(' ', '_')}.txt"
with open(nama_file, "w") as file:
    file.write(template_surat)

print(f"\nSurat berhasil dibuat dan disimpan di file {nama_file}")