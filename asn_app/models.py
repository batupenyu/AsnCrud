# asn_app/models.py
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class ASN(models.Model):
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    
    AGAMA_CHOICES = [
        ('ISLAM', 'Islam'),
        ('KRISTEN', 'Kristen'),
        ('KATOLIK', 'Katolik'),
        ('HINDU', 'Hindu'),
        ('BUDDHA', 'Buddha'),
        ('KONGHUCU', 'Konghucu'),
    ]
    
    nip = models.CharField(max_length=18, unique=True, null=True, blank=True)
    nama = models.CharField(max_length=100)
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICES)
    agama = models.CharField(max_length=10, choices=AGAMA_CHOICES)
    alamat = models.TextField()
    email = models.EmailField()
    telepon = models.CharField(max_length=15)
    jabatan = models.CharField(max_length=100)
    pangkat = models.CharField(max_length=50)
    golongan = models.CharField(max_length=5)
    nama_istri_suami = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Istri/Suami')
    unit_kerja = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='asn_fotos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nip} - {self.nama}"


class KopSurat(models.Model):
    nama = models.CharField(max_length=100, verbose_name='Nama Kop Surat')
    gambar = models.ImageField(upload_to='kop_surat/', verbose_name='Gambar Kop Surat')
    deskripsi = models.TextField(blank=True, null=True, verbose_name='Deskripsi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama


class SuratPerintahTugas(models.Model):
    peserta = models.ManyToManyField(ASN, related_name='spt_peserta', verbose_name='Peserta')
    dasar_surat = models.TextField(verbose_name='Dasar Surat')
    nomor_spt = models.CharField(max_length=50, verbose_name='Nomor SPT')
    tempat_pelaksanaan = models.CharField(max_length=100, verbose_name='Tempat Pelaksanaan')
    waktu_pelaksanaan = models.DateTimeField(verbose_name='Waktu Pelaksanaan')
    tanggal_pelaksanaan = models.DateField(verbose_name='Tanggal Pelaksanaan')
    tanggal_akhir_pelaksanaan = models.DateField(verbose_name='Tanggal Akhir Pelaksanaan', null=True, blank=True)
    nama_kegiatan = models.CharField(max_length=200, verbose_name='Nama Kegiatan')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, blank=True, null=True, related_name='spt_penandatangan', verbose_name='Penandatangan')
    kuasa_pengguna_anggaran = models.ForeignKey(ASN, on_delete=models.SET_NULL, blank=True, null=True, related_name='spt_kuasa_pengguna_anggaran', verbose_name='Kuasa Pengguna Anggaran')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Kop Surat')
    latar_belakang = models.TextField(verbose_name='Latar Belakang', blank=True, null=True)
    maksud_dan_tujuan = models.TextField(verbose_name='Maksud dan Tujuan', blank=True, null=True)
    hasil_yang_dicapai = models.TextField(verbose_name='Hasil yang Dicapai', blank=True, null=True)
    kesimpulan_dan_saran = models.TextField(verbose_name='Kesimpulan dan Saran', blank=True, null=True)
    penutup = models.TextField(verbose_name='Penutup', blank=True, null=True)

    tanggal_dibuat_laporan = models.DateField(verbose_name='Tanggal Dibuat Laporan', blank=True, null=True)
    
    SIFAT_SURAT_CHOICES = [
        ('Biasa', 'Biasa'),
        ('Penting', 'Penting'),
        ('Rahasia', 'Rahasia'),
    ]
    sifat_surat = models.CharField(max_length=10, choices=SIFAT_SURAT_CHOICES, default='Biasa', verbose_name='Sifat Surat')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SPT {self.nomor_spt} - {self.nama_kegiatan}"


class FotoKegiatan(models.Model):
    spt = models.ForeignKey(SuratPerintahTugas, related_name='foto_kegiatan', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='foto_kegiatan/')
    keterangan = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto untuk SPT {self.spt.nomor_spt}"


class SuratSantunanKorpri(models.Model):
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    tanggal_surat = models.DateField(verbose_name='Tanggal Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    instansi_tujuan_surat = models.CharField(max_length=200, verbose_name='Instansi Tujuan Surat')
    kota_tujuan_surat = models.CharField(max_length=100, verbose_name='Kota Tujuan Surat')
    sifat = models.CharField(max_length=100, verbose_name='Sifat')
    lampiran = models.CharField(max_length=100, verbose_name='Lampiran')
    perihal = models.CharField(max_length=200, verbose_name='Perihal')
    pegawai = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='surat_santunan', verbose_name='Pegawai')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='penandatangan_santunan', verbose_name='Penandatangan')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomor_surat

class NotaDinas(models.Model):
    kepada = models.CharField(max_length=255)
    dari = models.CharField(max_length=255)
    tanggal = models.DateField()
    nomor = models.CharField(max_length=255)
    sifat = models.CharField(max_length=255)
    lampiran = models.CharField(max_length=255)
    hal = models.CharField(max_length=255)
    isi_surat = models.TextField()
    pegawai = models.ManyToManyField(ASN, blank=True)
    penutup_surat = models.TextField()
    penanda_tangan = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='penanda_tangan_nota_dinas')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.hal

class HariLibur(models.Model):
    tanggal = models.DateField(unique=True, verbose_name='Tanggal Libur')
    nama_hari = models.CharField(max_length=100, verbose_name='Nama Hari Libur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hari Libur"
        ordering = ['tanggal']

    def __str__(self):
        return f"{self.nama_hari} ({self.tanggal})"

from datetime import date, timedelta

class SuratCuti(models.Model):
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_surat = models.DateField(verbose_name='Tanggal Surat')
    nomor_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nomor Surat')
    sifat_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sifat Surat')
    lampiran_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Lampiran Surat')
    perihal_surat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Perihal Surat')
    tujuan_surat = models.CharField(max_length=200, verbose_name='Tujuan Surat')
    pegawai = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='surat_cuti_pegawai', verbose_name='Pegawai')
    tanggal_awal = models.DateField(verbose_name='Tanggal Awal Cuti')
    tanggal_akhir = models.DateField(verbose_name='Tanggal Akhir Cuti')
    alasan_cuti = models.TextField(blank=True, null=True, verbose_name='Alasan Cuti')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='surat_cuti_penandatangan', verbose_name='Penandatangan')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat Cuti"
        ordering = ['-tanggal_surat']

    def __str__(self):
        return f"Surat Cuti {self.pegawai.nama} - {self.tanggal_surat}"

    def calculate_effective_leave_days(self):
        if not self.tanggal_awal or not self.tanggal_akhir:
            return 0

        total_days = 0
        current_date = self.tanggal_awal
        while current_date <= self.tanggal_akhir:
            # Check if it's a weekend (Saturday = 5, Sunday = 6)
            if current_date.weekday() < 5:  # Monday to Friday
                # Check if it's a holiday
                if not HariLibur.objects.filter(tanggal=current_date).exists():
                    total_days += 1
            current_date += timedelta(days=1)
        return total_days

class SisaCuti(models.Model):
    pegawai = models.OneToOneField(ASN, on_delete=models.CASCADE, related_name='sisa_cuti', verbose_name='Pegawai')
    sisa_tahun_n = models.IntegerField(default=12, verbose_name='Sisa Tahun N')
    sisa_tahun_n_1 = models.IntegerField(default=0, verbose_name='Sisa Tahun N-1')
    sisa_tahun_n_2 = models.IntegerField(default=0, verbose_name='Sisa Tahun N-2')
    total_sisa_cuti = models.IntegerField(default=0, verbose_name='Total Sisa Cuti')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sisa Cuti"
        ordering = ['pegawai__nama']

    def save(self, *args, **kwargs):
        self.total_sisa_cuti = self.sisa_tahun_n + self.sisa_tahun_n_1 + self.sisa_tahun_n_2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sisa Cuti {self.pegawai.nama} - Total: {self.total_sisa_cuti}"


class Siswa(models.Model):
    nama = models.CharField(max_length=100, null=True, blank=True)
    nis = models.CharField(max_length=20, null=True, blank=True)
    kelas = models.CharField(max_length=20)
    jurusan = models.CharField(max_length=50, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    no_hp = models.CharField(max_length=15, blank=True, null=True)
    nama_orang_tua = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Orang Tua')
    foto = models.ImageField(upload_to='siswa_fotos/', blank=True, null=True)

    def __str__(self):
        return self.nama


    def get_absolute_url(self):
        return reverse('siswa_detail', kwargs={'pk': self.pk})


class SuratKeterangan(models.Model):
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='penandatangan_sk', verbose_name='Penandatangan')
    pegawai = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='pegawai_sk', verbose_name='Pegawai (ASN)')
    siswa = models.ForeignKey(Siswa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Siswa')
    isi_surat = models.TextField(blank=True, verbose_name='Isi Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        subject = "[Tanpa Subjek]" # Default value
        if self.pegawai:
            subject = self.pegawai.nama
        elif self.siswa:
            subject = self.siswa.nama
        return f"Surat Keterangan untuk {subject} - {self.nomor_surat}"

    def get_absolute_url(self):
        return reverse('surat_keterangan_detail', kwargs={'pk': self.pk})


class SuratResmi(models.Model):
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    pejabat_tujuan_surat = models.CharField(max_length=200, verbose_name='Pejabat Tujuan Surat')
    kota_tujuan_surat = models.CharField(max_length=100, verbose_name='Kota Tujuan Surat')
    nomor = models.CharField(max_length=50, verbose_name='Nomor Surat')
    sifat = models.CharField(max_length=100, verbose_name='Sifat Surat')
    lampiran = models.CharField(max_length=100, blank=True, null=True, verbose_name='Lampiran')
    perihal = models.CharField(max_length=200, verbose_name='Perihal')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='surat_resmi_penandatangan', verbose_name='Penandatangan')
    pegawai = models.ManyToManyField(ASN, blank=True, related_name='surat_resmi_pegawai', verbose_name='Pegawai Terkait')
    pembuka_surat = models.TextField(verbose_name='Pembuka Surat')
    isi_surat = models.TextField(verbose_name='Isi Surat')
    penutup_surat = models.TextField(verbose_name='Penutup Surat')
    tanggal_kegiatan = models.DateField(blank=True, null=True, verbose_name='Tanggal Kegiatan')
    waktu_kegiatan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Waktu Kegiatan')
    tempat_kegiatan = models.CharField(max_length=200, blank=True, null=True, verbose_name='Tempat Kegiatan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat Resmi"
        ordering = ['-tanggal_ditetapkan']

    def __str__(self):
        return f"Surat Resmi {self.nomor} - {self.perihal}"


class SPTJM(models.Model):
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, related_name='sptjm_penandatangan', verbose_name='Penandatangan')
    pegawai = models.ManyToManyField(ASN, related_name='sptjm_pegawai', verbose_name='Pegawai')
    isi_surat = models.TextField(verbose_name='Isi Surat')
    penutup_surat = models.TextField(verbose_name='Penutup Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomor_surat

    def get_absolute_url(self):
        return reverse('sptjm_detail', kwargs={'pk': self.pk})

# Model untuk Surat Perintah Melaksanakan Tugas (SPMT)
class SPMT(models.Model):
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_surat = models.DateField(verbose_name='Tanggal Surat')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, related_name='spmt_penandatangan', verbose_name='Penandatangan')
    pegawai = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, related_name='spmt_pegawai', verbose_name='Pegawai')
    peraturan = models.CharField(max_length=255, verbose_name='Peraturan')
    nomor_peraturan = models.CharField(max_length=100, verbose_name='Nomor Peraturan')
    tahun_peraturan = models.CharField(max_length=4, verbose_name='Tahun Peraturan')
    tentang = models.TextField(verbose_name='Tentang')
    tanggal_terhitung = models.DateField(verbose_name='Tanggal Terhitung Mulai')
    sebagai = models.CharField(max_length=255, verbose_name='Sebagai')
    tempat_tugas = models.CharField(max_length=255, verbose_name='Tempat Tugas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomor_surat

    def get_absolute_url(self):
        return reverse('spmt_detail', kwargs={'pk': self.pk})

class SuratUmum(models.Model):
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    pegawai = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='surat_umum_pegawai', verbose_name='Pegawai')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='surat_umum_penandatangan', verbose_name='Penandatangan')
    pembuka_surat = models.TextField(verbose_name='Pembuka Surat')
    isi_surat = models.TextField(verbose_name='Isi Surat')
    penutup_surat = models.TextField(verbose_name='Penutup Surat')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Surat Umum untuk {self.pegawai.nama}"