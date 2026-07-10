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
    pangkat = models.CharField(max_length=50, null=True, blank=True)
    golongan = models.CharField(max_length=5, null=True, blank=True)
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

    @property
    def jumlah_hari(self):
        from .models import HariLibur
        if self.tanggal_pelaksanaan and self.tanggal_akhir_pelaksanaan:
            total = 0
            d = self.tanggal_pelaksanaan
            while d <= self.tanggal_akhir_pelaksanaan:
                if d.weekday() < 5 and not HariLibur.objects.filter(tanggal=d).exists():
                    total += 1
                d += timedelta(days=1)
            return total
        elif self.tanggal_pelaksanaan:
            d = self.tanggal_pelaksanaan
            if d.weekday() < 5 and not HariLibur.objects.filter(tanggal=d).exists():
                return 1
            return 0
        return 1


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
    siswa = models.ManyToManyField('Siswa', blank=True, related_name='nota_dinas_siswa')
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
    JENIS_CUTI_CHOICES = [
        ('Cuti Tahunan', 'Cuti Tahunan'),
        ('Cuti Sakit', 'Cuti Sakit'),
        ('Cuti Alasan Penting', 'Cuti Alasan Penting'),
        ('Cuti Diluar Tanggungan Negara', 'Cuti Diluar Tanggungan Negara'),
        ('Cuti Melahirkan', 'Cuti Melahirkan'),
        ('Cuti Besar', 'Cuti Besar'),
    ]

    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_surat = models.DateField(verbose_name='Tanggal Surat')
    nomor_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nomor Surat')
    sifat_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Sifat Surat')
    lampiran_surat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Lampiran Surat')
    perihal_surat = models.CharField(max_length=255, blank=True, null=True, verbose_name='Perihal Surat')
    tujuan_surat = models.CharField(max_length=200, verbose_name='Tujuan Surat')
    jenis_cuti = models.CharField(max_length=50, choices=JENIS_CUTI_CHOICES, default='Cuti Tahunan', verbose_name='Jenis Cuti')
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
        """
        Hitung jumlah hari cuti efektif (hari kerja).
        
        Logic:
        - Hari Sabtu dan Minggu TIDAK dihitung (bukan hari kerja)
        - Hari libur nasional/resmi TIDAK dihitung (dari tabel HariLibur)
        - Hanya hari Senin-Jumat yang bukan hari libur yang dihitung
        
        Returns:
            int: Jumlah hari kerja efektif
        """
        if not self.tanggal_awal or not self.tanggal_akhir:
            return 0

        # Fetch all holidays in range once (avoid N+1 queries)
        holidays = set(
            HariLibur.objects.filter(
                tanggal__gte=self.tanggal_awal,
                tanggal__lte=self.tanggal_akhir
            ).values_list('tanggal', flat=True)
        )

        total_days = 0
        current_date = self.tanggal_awal
        while current_date <= self.tanggal_akhir:
            # Skip weekend (Sabtu=5, Minggu=6) dan hari libur
            if current_date.weekday() < 5 and current_date not in holidays:
                total_days += 1
            current_date += timedelta(days=1)
        return total_days

class SisaCuti(models.Model):
    pegawai = models.OneToOneField(ASN, on_delete=models.CASCADE, related_name='sisa_cuti', verbose_name='Pegawai')
    # Initial allocation (editable manually)
    initial_tahun_n = models.IntegerField(default=12, verbose_name='Alokasi Awal Tahun N')
    initial_tahun_n_1 = models.IntegerField(default=6, verbose_name='Alokasi Awal Tahun N-1')
    initial_tahun_n_2 = models.IntegerField(default=6, verbose_name='Alokasi Awal Tahun N-2')
    # Calculated remaining balance (auto-calculated)
    sisa_tahun_n = models.IntegerField(default=12, verbose_name='Sisa Tahun N')
    sisa_tahun_n_1 = models.IntegerField(default=6, verbose_name='Sisa Tahun N-1')
    sisa_tahun_n_2 = models.IntegerField(default=6, verbose_name='Sisa Tahun N-2')
    total_sisa_cuti = models.IntegerField(default=24, verbose_name='Total Sisa Cuti')
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

    @staticmethod
    def get_current_year():
        from datetime import date
        return date.today().year

    def calculate_sisa_cuti_from_surat(self):
        """
        Calculate remaining leave (sisa cuti) for years N, N-1, N-2 based on approved SuratCuti records.
        Uses initial allocation values (editable) and subtracts used leave.

        Dynamic Continuous Logic:
        - Year N: Initial allocation - used in year N
        - Year N-1: Initial allocation - used in year N-1, BUT if year N usage > initial N-1, then N-1 = 0
        - Year N-2: Initial allocation - used in year N-2, BUT if year N-1 usage > initial N-2, then N-2 = 0
        """
        current_year = self.get_current_year()
        year_n = current_year
        year_n_1 = current_year - 1
        year_n_2 = current_year - 2

        # Get initial allocation (editable values)
        initial_n = self.initial_tahun_n
        initial_n_1 = self.initial_tahun_n_1
        initial_n_2 = self.initial_tahun_n_2

        # Get all approved surat cuti for this pegawai
        surat_cuti_list = SuratCuti.objects.filter(pegawai=self.pegawai)

        # Calculate used leave days per year
        used_n = 0
        used_n_1 = 0
        used_n_2 = 0

        for surat_cuti in surat_cuti_list:
            # Get the year from tanggal_awal
            leave_year = surat_cuti.tanggal_awal.year
            leave_days = surat_cuti.calculate_effective_leave_days()

            if leave_year == year_n:
                used_n += leave_days
            elif leave_year == year_n_1:
                used_n_1 += leave_days
            elif leave_year == year_n_2:
                used_n_2 += leave_days

        # Calculate remaining leave for year N (current year)
        self.sisa_tahun_n = max(0, initial_n - used_n)

        # Dynamic continuous logic for N-1:
        # If year N usage > initial N-1, then N-1 becomes 0
        # Otherwise, N-1 = initial - used in N-1
        if used_n > initial_n_1:
            self.sisa_tahun_n_1 = 0
        else:
            self.sisa_tahun_n_1 = max(0, initial_n_1 - used_n_1)

        # Dynamic continuous logic for N-2:
        # If year N-1 usage > initial N-2, then N-2 becomes 0
        # Otherwise, N-2 = initial - used in N-2
        if used_n_1 > initial_n_2:
            self.sisa_tahun_n_2 = 0
        else:
            self.sisa_tahun_n_2 = max(0, initial_n_2 - used_n_2)

        self.total_sisa_cuti = self.sisa_tahun_n + self.sisa_tahun_n_1 + self.sisa_tahun_n_2

        return {
            'initial_tahun_n': self.initial_tahun_n,
            'initial_tahun_n_1': self.initial_tahun_n_1,
            'initial_tahun_n_2': self.initial_tahun_n_2,
            'sisa_tahun_n': self.sisa_tahun_n,
            'sisa_tahun_n_1': self.sisa_tahun_n_1,
            'sisa_tahun_n_2': self.sisa_tahun_n_2,
            'total_sisa_cuti': self.total_sisa_cuti,
        }

    def recalculate_and_save(self):
        """Recalculate sisa cuti from surat cuti records and save."""
        self.calculate_sisa_cuti_from_surat()
        self.save()


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


class PesertaNotaDinas(models.Model):
    PERAN_CHOICES = [
        ('Peserta', 'Peserta'),
        ('Pendamping', 'Pendamping'),
        ('Toolman', 'Toolman'),
        ('Kepsek', 'Kepsek / Penanggungjawab'),
        ('Bendahara', 'Bendahara'),
    ]
    nota_dinas = models.ForeignKey(NotaDinas, on_delete=models.CASCADE, related_name='peserta_nota_dinas')
    pegawai = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Pegawai')
    siswa = models.ForeignKey(Siswa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Siswa')
    bidang_lomba = models.CharField(max_length=255, blank=True, verbose_name='Bidang Lomba')
    peran = models.CharField(max_length=50, choices=PERAN_CHOICES, default='Peserta', verbose_name='Peran')

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.pegawai:
            return f"{self.pegawai.nama} - {self.peran}"
        elif self.siswa:
            return f"{self.siswa.nama} - {self.peran}"
        return f"Peserta {self.id}"


class SiswaKeluar(models.Model):
    """Model untuk mencatat siswa yang keluar/drop out (DO)"""
    
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='keluar', verbose_name='Siswa')
    tanggal_keluar = models.DateField(verbose_name='Tanggal Keluar')
    alasan_keluar = models.TextField(verbose_name='Alasan Keluar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Siswa Keluar'
        verbose_name_plural = 'Siswa Keluar'
        ordering = ['-tanggal_keluar']
    
    def __str__(self):
        return f"{self.siswa.nama} - Keluar {self.tanggal_keluar}"
    
    def get_absolute_url(self):
        return reverse('siswa_keluar_detail', kwargs={'pk': self.pk})


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


class SuratRekomendasiStudiLanjut(models.Model):
    """Model untuk Surat Rekomendasi Studi Lanjut yang diberikan pimpinan kepada pegawai."""
    DEFAULT_PERTIMBANGAN = (
        "Pegawai yang bersangkutan memiliki dedikasi dan kinerja yang baik selama bekerja di instansi kami.\n"
        "Bidang ilmu yang akan dipelajari relevan dengan kebutuhan pengembangan kompetensi serta peningkatan efektivitas pelayanan di unit kerja kami.\n"
        "Pegawai memiliki potensi akademik yang baik serta kemampuan untuk mengaplikasikan ilmu yang didapat bagi kemajuan instansi."
    )

    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='rekomendasi_penandatangan', verbose_name='Pimpinan (Atasan)')
    instansi = models.CharField(max_length=200, verbose_name='Nama Instansi/Sekolah/Organisasi')
    pegawai = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='rekomendasi_pegawai', verbose_name='Pegawai')
    nama_universitas = models.CharField(max_length=200, verbose_name='Nama Universitas/Kampus')
    program_studi = models.CharField(max_length=200, verbose_name='Nama Program Studi')
    pertimbangan = models.TextField(blank=True, default=DEFAULT_PERTIMBANGAN, verbose_name='Pertimbangan Rekomendasi')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat Rekomendasi Studi Lanjut"
        ordering = ['-tanggal_ditetapkan']

    def __str__(self):
        subject = self.pegawai.nama if self.pegawai else "[Tanpa Pegawai]"
        return f"Surat Rekomendasi Studi Lanjut - {subject} - {self.nomor_surat}"

    def get_absolute_url(self):
        return reverse('surat_rekomendasi_detail', kwargs={'pk': self.pk})


class SuratKP4(models.Model):
    """Model untuk KP4 - Surat Keterangan untuk mendapatkan pembayaran tunjangan keluarga."""
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    pegawai = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='kp4_pegawai', verbose_name='Pegawai (Yang Menerangkan)')
    penandatangan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='kp4_penandatangan', verbose_name='Kepala (Mengetahui)')
    status_kepegawaian = models.CharField(max_length=100, blank=True, null=True, verbose_name='Status Kepegawaian')
    masa_kerja_golongan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Masa Kerja Golongan')
    digaji_menurut = models.CharField(max_length=255, blank=True, null=True, default='PP Nomor 05 Tahun 2024 (CPNS dan PNS), Perpres Nomor 11 Tahun 2024 (PPPK)', verbose_name='Digaji Menurut')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat KP4 (Tunjangan Keluarga)"
        ordering = ['-tanggal_ditetapkan']

    def __str__(self):
        subject = self.pegawai.nama if self.pegawai else "[Tanpa Pegawai]"
        return f"KP4 - {subject}"

    def get_absolute_url(self):
        return reverse('surat_kp4_detail', kwargs={'pk': self.pk})


class AnggotaKeluargaKP4(models.Model):
    """Model untuk anggota keluarga pada Surat KP4."""
    surat = models.ForeignKey(SuratKP4, on_delete=models.CASCADE, related_name='anggota_keluarga', verbose_name='Surat KP4')
    nama = models.CharField(max_length=200, verbose_name='Nama Istri/Suami/Tanggungan')
    tanggal_kelahiran = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tanggal Kelahiran')
    tanggal_perkawinan = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tanggal Perkawinan')
    pekerjaan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Pekerjaan')
    keterangan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Keterangan')
    mendapat_tunjangan = models.BooleanField(default=True, verbose_name='Mendapat Tunjangan')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nama


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


class SuratPanggilanSiswa(models.Model):
    """Model untuk Surat Panggilan Siswa"""
    
    KETERANGAN_PANGGILAN_CHOICES = [
        ('1', 'ke-1 (Satu)'),
        ('2', 'ke-2 (Dua)'),
        ('3', 'ke-3 (Tiga)'),
        ('4', 'ke-4 (Empat)'),
    ]
    
    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='surat_panggilan', verbose_name='Siswa')
    orang_tua = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Orang Tua')
    keterangan_panggilan = models.CharField(max_length=1, choices=KETERANGAN_PANGGILAN_CHOICES, default='1', verbose_name='Panggilan Ke-')
    alasan_panggilan = models.TextField(verbose_name='Alasan Panggilan')
    tempat_panggilan = models.CharField(max_length=100, verbose_name='Tempat Panggilan')
    tanggal_panggilan = models.DateField(verbose_name='Tanggal Panggilan')
    waktu_panggilan = models.TimeField(verbose_name='Waktu Panggilan')
    wali_kelas = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='wali_kelas_panggilan', verbose_name='Wali Kelas')
    guru_bk = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='guru_bk_panggilan', verbose_name='Guru BK')
    wakasek_kesiswaan = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='wakasek_kesiswaan_panggilan', verbose_name='Wakasek Kesiswaan')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat Panggilan Siswa"
        ordering = ['-tanggal_ditetapkan']

    def __str__(self):
        return f"Surat Panggilan - {self.siswa.nama} - {self.nomor_surat}"

    def get_absolute_url(self):
        return reverse('surat_panggilan_siswa_detail', kwargs={'pk': self.pk})


class SuratUndanganSiswa(models.Model):
    """Model untuk Surat Undangan Siswa (hanya ditandatangani Kepala Sekolah)"""

    kop_surat = models.ForeignKey(KopSurat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kop Surat')
    nomor_surat = models.CharField(max_length=100, verbose_name='Nomor Surat')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True, related_name='surat_undangan', verbose_name='Siswa')
    orang_tua = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Orang Tua')
    perihal = models.CharField(max_length=200, default='Undangan Orang Tua Siswa', verbose_name='Perihal')
    isi_undangan = models.TextField(verbose_name='Isi/Maksud Undangan')
    tempat = models.CharField(max_length=100, verbose_name='Tempat')
    tanggal = models.DateField(verbose_name='Tanggal Undangan')
    waktu = models.TimeField(verbose_name='Waktu Undangan')
    kepala_sekolah = models.ForeignKey(ASN, on_delete=models.SET_NULL, null=True, blank=True, related_name='kepala_sekolah_undangan', verbose_name='Kepala Sekolah')
    tempat_ditetapkan = models.CharField(max_length=100, verbose_name='Tempat Ditetapkan')
    tanggal_ditetapkan = models.DateField(verbose_name='Tanggal Ditetapkan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Surat Undangan Siswa"
        ordering = ['-tanggal_ditetapkan']

    def __str__(self):
        return f"Surat Undangan - {self.siswa.nama} - {self.nomor_surat}"

    def get_absolute_url(self):
        return reverse('surat_undangan_siswa_detail', kwargs={'pk': self.pk})