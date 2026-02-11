# asn_app/admin.py
from django.contrib import admin
from .models import ASN, KopSurat, SuratPerintahTugas, SuratSantunanKorpri, NotaDinas, HariLibur, SuratCuti, SisaCuti, Siswa, SuratKeterangan, SuratResmi


@admin.register(ASN)
class ASNAdmin(admin.ModelAdmin):
    list_display = ('nip', 'nama', 'jabatan', 'unit_kerja', 'created_at')
    list_filter = ('jenis_kelamin', 'agama', 'unit_kerja')
    search_fields = ('nip', 'nama', 'jabatan')
    ordering = ('nama',)

@admin.register(KopSurat)
class KopSuratAdmin(admin.ModelAdmin):
    list_display = ('nama', 'created_at', 'updated_at')
    search_fields = ('nama',)

@admin.register(SuratPerintahTugas)
class SuratPerintahTugasAdmin(admin.ModelAdmin):
    list_display = ('nomor_spt', 'nama_kegiatan', 'tanggal_pelaksanaan', 'tempat_pelaksanaan', 'created_at')
    list_filter = ('tanggal_pelaksanaan', 'tempat_pelaksanaan')
    search_fields = ('nomor_spt', 'nama_kegiatan')
    filter_horizontal = ('peserta',)

@admin.register(SuratSantunanKorpri)
class SuratSantunanKorpriAdmin(admin.ModelAdmin):
    list_display = ('nomor_surat', 'tanggal_surat', 'perihal', 'pegawai', 'created_at')
    list_filter = ('tanggal_surat',)
    search_fields = ('nomor_surat', 'perihal', 'pegawai__nama')

@admin.register(NotaDinas)
class NotaDinasAdmin(admin.ModelAdmin):
    list_display = ('hal', 'nomor', 'tanggal', 'dari', 'kepada')
    list_filter = ('tanggal',)
    search_fields = ('hal', 'nomor', 'dari', 'kepada')
    filter_horizontal = ('pegawai',)

@admin.register(HariLibur)
class HariLiburAdmin(admin.ModelAdmin):
    list_display = ('tanggal', 'nama_hari', 'created_at', 'updated_at')
    list_filter = ('tanggal',)
    search_fields = ('nama_hari',)
    ordering = ('tanggal',)

@admin.register(SuratCuti)
class SuratCutiAdmin(admin.ModelAdmin):
    list_display = ('pegawai', 'tanggal_surat', 'tanggal_awal', 'tanggal_akhir', 'penandatangan', 'created_at')
    list_filter = ('tanggal_surat', 'tanggal_awal', 'tanggal_akhir')
    search_fields = ('pegawai__nama', 'penandatangan__nama')
    raw_id_fields = ('pegawai', 'penandatangan', 'kop_surat') # Use raw_id_fields for ForeignKey to ASN for better performance with many ASNs

@admin.register(SisaCuti)
class SisaCutiAdmin(admin.ModelAdmin):
    list_display = ('pegawai', 'sisa_tahun_n', 'sisa_tahun_n_1', 'sisa_tahun_n_2', 'total_sisa_cuti', 'created_at')
    list_filter = ('pegawai',)
    search_fields = ('pegawai__nama',)
    readonly_fields = ('total_sisa_cuti',) # total_sisa_cuti is calculated automatically
    raw_id_fields = ('pegawai',)

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'kelas', 'jurusan')
    search_fields = ('nama', 'nis')
    list_filter = ('kelas', 'jurusan')

@admin.register(SuratKeterangan)
class SuratKeteranganAdmin(admin.ModelAdmin):
    list_display = ('nomor_surat', 'pegawai', 'siswa', 'tanggal_ditetapkan', 'created_at')
    list_filter = ('tanggal_ditetapkan',)
    search_fields = ('nomor_surat', 'pegawai__nama', 'siswa__nama')
    raw_id_fields = ('penandatangan', 'pegawai', 'siswa')

@admin.register(SuratResmi)
class SuratResmiAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'perihal', 'tanggal_ditetapkan', 'penandatangan', 'kop_surat', 'created_at')
    list_filter = ('tanggal_ditetapkan', 'sifat', 'penandatangan')
    search_fields = ('nomor', 'perihal', 'pejabat_tujuan_surat', 'penandatangan__nama')
    filter_horizontal = ('pegawai',)
    raw_id_fields = ('penandatangan', 'kop_surat')