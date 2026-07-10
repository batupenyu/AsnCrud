# asn_app/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (
    ASN, SuratPerintahTugas, KopSurat, SuratSantunanKorpri,
    NotaDinas, HariLibur, SuratCuti, SisaCuti, Siswa,
    SuratKeterangan, SuratResmi, SPTJM, SPMT, FotoKegiatan, SuratUmum,
    SuratPanggilanSiswa, SiswaKeluar, SuratRekomendasiStudiLanjut, SuratKP4, AnggotaKeluargaKP4,
    SuratUndanganSiswa, PesertaNotaDinas
)


class FotoKegiatanForm(forms.ModelForm):
    class Meta:
        model = FotoKegiatan
        fields = ['keterangan']
        widgets = {
            'keterangan': forms.Textarea(attrs={'rows': 2}),
        }








class ASNForm(forms.ModelForm):


    class Meta:


        model = ASN


        fields = '__all__'


        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '18 digit NIP'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'}),
            'agama': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telepon': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan': forms.TextInput(attrs={'class': 'form-control'}),
            'pangkat': forms.TextInput(attrs={'class': 'form-control'}),
            'golongan': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_kerja': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'nama_istri_suami': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nip(self):
        nip = self.cleaned_data.get('nip')
        if nip and len(nip) != 18:
            raise forms.ValidationError("NIP harus terdiri dari 18 digit")
        return nip

    def clean_pangkat(self):
        val = self.cleaned_data.get('pangkat', '')
        return '' if val == '-' else val

    def clean_golongan(self):
        val = self.cleaned_data.get('golongan', '')
        return '' if val == '-' else val


class KopSuratForm(forms.ModelForm):
    class Meta:
        model = KopSurat
        fields = '__all__'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'gambar': forms.FileInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class SPTForm(forms.ModelForm):
    class Meta:
        model = SuratPerintahTugas
        fields = '__all__'
        widgets = {
            'peserta': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'dasar_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nomor_spt': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_pelaksanaan': forms.TextInput(attrs={'class': 'form-control'}),
            'waktu_pelaksanaan': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tanggal_pelaksanaan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_akhir_pelaksanaan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nama_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'kuasa_pengguna_anggaran': forms.Select(attrs={'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'latar_belakang': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'maksud_dan_tujuan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'hasil_yang_dicapai': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'kesimpulan_dan_saran': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'penutup': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tanggal_dibuat_laporan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sifat_surat': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peserta'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kuasa_pengguna_anggaran'].queryset = ASN.objects.all().order_by('nama')
        self.fields['peserta'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama
        self.fields['kuasa_pengguna_anggaran'].label_from_instance = lambda obj: obj.nama

    def clean(self):
        cleaned_data = super().clean()
        tanggal_pelaksanaan = cleaned_data.get('tanggal_pelaksanaan')
        tanggal_akhir_pelaksanaan = cleaned_data.get('tanggal_akhir_pelaksanaan')

        if tanggal_pelaksanaan and tanggal_akhir_pelaksanaan and tanggal_akhir_pelaksanaan < tanggal_pelaksanaan:
            raise forms.ValidationError("Tanggal akhir pelaksanaan tidak boleh sebelum tanggal pelaksanaan.")

        return cleaned_data


class SuratSantunanKorpriForm(forms.ModelForm):
    class Meta:
        model = SuratSantunanKorpri
        fields = '__all__'
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_surat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'instansi_tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'kota_tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'sifat': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal': forms.TextInput(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama

class NotaDinasForm(forms.ModelForm):
    SIFAT_CHOICES = [
        ('Penting', 'Penting'),
        ('Biasa', 'Biasa'),
        ('Segera', 'Segera'),
    ]
    sifat = forms.ChoiceField(choices=SIFAT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = NotaDinas
        fields = '__all__'
        widgets = {
            'kepada': forms.TextInput(attrs={'class': 'form-control'}),
            'dari': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nomor': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control'}),
            'hal': forms.TextInput(attrs={'class': 'form-control'}),
            'isi_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'pegawai': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'siswa': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'penutup_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penanda_tangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penanda_tangan'].label_from_instance = lambda obj: obj.nama
        self.fields['siswa'].label_from_instance = lambda obj: f"{obj.nama} - {obj.kelas}"
        if not self.instance.pk:
            self.fields['kepada'].initial = 'Yth. Gubernur Kepulauan Bangka Belitung'
            self.fields['dari'].initial = 'Kepala SMK Negeri 1 Koba'
            self.fields['lampiran'].initial = '1 (satu) Lembar'
            self.fields['hal'].initial = 'Permohonan penerbitan Surat Tugas dan Surat Perintah Perjalanan Dinas (SPPD)'
            self.fields['penutup_surat'].initial = 'Demikian nota dinas ini kami sampaikan untuk menjadi periksa dan persetujuan lebih lanjut, atas perhatian Bapak, kami ucapkan terima kasih'
            last_nd = NotaDinas.objects.exclude(nomor__isnull=True).exclude(nomor='').order_by('-pk').first()
            if last_nd and last_nd.nomor:
                parts = last_nd.nomor.split('/')
                for i, part in enumerate(parts):
                    if i > 0 and part.isdigit():
                        parts[i] = str(int(part) + 1).zfill(len(part))
                        break
                self.fields['nomor'].initial = '/'.join(parts)
            else:
                self.fields['nomor'].initial = '800.1.11.1/001/SMKN1KB/2026'

class HariLiburForm(forms.ModelForm):
    class Meta:
        model = HariLibur
        fields = '__all__'
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nama_hari': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SuratCutiForm(forms.ModelForm):
    class Meta:
        model = SuratCuti
        fields = '__all__'
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'sifat_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_surat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'jenis_cuti': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_awal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_akhir': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'alasan_cuti': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama

    def clean(self):
        cleaned_data = super().clean()
        tanggal_awal = cleaned_data.get('tanggal_awal')
        tanggal_akhir = cleaned_data.get('tanggal_akhir')

        if tanggal_awal and tanggal_akhir and tanggal_akhir < tanggal_awal:
            raise forms.ValidationError("Tanggal akhir cuti tidak boleh sebelum tanggal awal cuti.")
        return cleaned_data

class SisaCutiForm(forms.ModelForm):
    class Meta:
        model = SisaCuti
        exclude = ('total_sisa_cuti', 'sisa_tahun_n', 'sisa_tahun_n_1', 'sisa_tahun_n_2',) # Exclude calculated fields
        widgets = {
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'initial_tahun_n': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_tahun_n_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_tahun_n_2': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama


class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = '__all__'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nis': forms.TextInput(attrs={'class': 'form-control'}),
            'kelas': forms.TextInput(attrs={'class': 'form-control'}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_orang_tua': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SuratKeteranganForm(forms.ModelForm):
    person = forms.ChoiceField(label='Pilih Pegawai atau Siswa', required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = SuratKeterangan
        fields = '__all__'
        exclude = ['pegawai', 'siswa']
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'isi_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama

        # Build choices for person
        choices = []
        for asn in ASN.objects.all().order_by('nama'):
            choices.append((f'pegawai_{asn.id}', f'Pegawai: {asn.nama}'))
        for siswa in Siswa.objects.all().order_by('nama'):
            choices.append((f'siswa_{siswa.id}', f'Siswa: {siswa.nama}'))
        self.fields['person'].choices = choices

        # Set initial if instance exists
        if self.instance and self.instance.pk:
            if self.instance.pegawai:
                self.fields['person'].initial = f'pegawai_{self.instance.pegawai.id}'
            elif self.instance.siswa:
                self.fields['person'].initial = f'siswa_{self.instance.siswa.id}'

    def clean_person(self):
        person_value = self.cleaned_data.get('person')
        if not person_value:
            raise forms.ValidationError("Anda harus memilih Pegawai atau Siswa.")
        return person_value

    def save(self, commit=True):
        instance = super().save(commit=False)
        person_value = self.cleaned_data.get('person')
        if person_value:
            if person_value.startswith('pegawai_'):
                asn_id = int(person_value.split('_')[1])
                instance.pegawai = ASN.objects.get(id=asn_id)
                instance.siswa = None
            elif person_value.startswith('siswa_'):
                siswa_id = int(person_value.split('_')[1])
                instance.siswa = Siswa.objects.get(id=siswa_id)
                instance.pegawai = None
        else:
            # This case should ideally not be reached if clean_person works
            instance.pegawai = None
            instance.siswa = None

        if commit:
            instance.save()
        return instance


class SuratRekomendasiStudiLanjutForm(forms.ModelForm):
    class Meta:
        model = SuratRekomendasiStudiLanjut
        fields = '__all__'
        widgets = {
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'instansi': forms.TextInput(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'nama_universitas': forms.TextInput(attrs={'class': 'form-control'}),
            'program_studi': forms.TextInput(attrs={'class': 'form-control'}),
            'pertimbangan': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama


class SuratKP4Form(forms.ModelForm):
    class Meta:
        model = SuratKP4
        fields = ['kop_surat', 'pegawai', 'penandatangan', 'status_kepegawaian', 'masa_kerja_golongan', 'digaji_menurut', 'tempat_ditetapkan', 'tanggal_ditetapkan']
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'status_kepegawaian': forms.TextInput(attrs={'class': 'form-control'}),
            'masa_kerja_golongan': forms.TextInput(attrs={'class': 'form-control'}),
            'digaji_menurut': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama


class AnggotaKeluargaKP4Form(forms.ModelForm):
    class Meta:
        model = AnggotaKeluargaKP4
        fields = ['nama', 'tanggal_kelahiran', 'tanggal_perkawinan', 'pekerjaan', 'keterangan', 'mendapat_tunjangan']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_kelahiran': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cth: 23 - 09 - 2000'}),
            'tanggal_perkawinan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cth: 05 - 10 - 2025 / Belum Kawin'}),
            'pekerjaan': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'cth: Istri / anak'}),
            'mendapat_tunjangan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


AnggotaKeluargaKP4FormSet = inlineformset_factory(
    SuratKP4, AnggotaKeluargaKP4,
    form=AnggotaKeluargaKP4Form,
    extra=1,
    can_delete=True
)


class SuratResmiForm(forms.ModelForm):
    class Meta:
        model = SuratResmi
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pejabat_tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'kota_tujuan_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'nomor': forms.TextInput(attrs={'class': 'form-control'}),
            'sifat': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal': forms.TextInput(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'pembuka_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'isi_surat': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'penutup_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'tanggal_kegiatan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'waktu_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_kegiatan': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama


class SPTJMForm(forms.ModelForm):
    class Meta:
        model = SPTJM
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'isi_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'penutup_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama

JABATAN_CHOICES = [
    ('Analis Sumber Daya Manusia Aparatur Ahli Muda', 'Analis Sumber Daya Manusia  Aparatur Ahli Muda'),
    ('Penelaah Teknis Kebijakan', 'Penelaah Teknis Kebijakan'),
    ('Pengolah Data dan Informasi', 'Pengolah Data  dan Informasi'),
    ('Pengadministrasi Perkantoran', 'Pengadministrasi Perkantoran'),
    ('Operator Layanan Operasional', 'Operator Layanan Operasional'),
    ('Pengelola Umum Operasional', 'Pengelola  Umum Operasional'),
    ('Guru Ahli Madya - Bahasa Inggris', 'Guru Ahli Madya  - Bahasa  Inggris'),
    ('Guru Ahli Madya - Teknik Ketenagalistrikan', 'Guru Ahli Madya  -  Teknik Ketenagalistrikan'),
    ('Guru Ahli Madya - Teknik Otomotif', 'Guru Ahli Madya  -  Teknik Otomotif'),
    ('Guru Ahli Muda - Bahasa Indonesia', 'Guru Ahli Muda  -  Bahasa Indonesia'),
    ('Guru Ahli Muda - Bahasa Inggris', 'Guru Ahli Muda  -  Bahasa Inggris'),
    ('Guru Ahli Muda - Teknik Jaringan Komputer dan Telekomunikasi', 'Guru Ahli Muda  -  Teknik Jaringan Komputer dan Telekomunikasi'),
    ('Guru Ahli Muda - Informatika', 'Guru Ahli Muda  -  Informatika'),
    ('Guru Ahli Muda - IPAS', 'Guru Ahli Muda  -  IPAS'),
    ('Guru Ahli Muda - Agama Islam', 'Guru Ahli Muda  -  Agama Islam'),
    ('Guru Ahli Muda - PPKn', 'Guru Ahli Muda  -  PPKn'),
    ('Guru Ahli Muda - Sejarah', 'Guru Ahli Muda  -  Sejarah'),
    ('Guru Ahli Muda - Bimbingan Konseling', 'Guru Ahli Muda  - Bimbingan Konseling'),
    ('Guru Ahli Muda - Teknik Ketenagalistrikan', 'Guru Ahli Muda  -  Teknik Ketenagalistrikan'),
    ('Guru Ahli Muda - Matematika', 'Guru Ahli Muda  -  Matematika'),
    ('Guru Ahli Muda - Teknik Otomotif', 'Guru Ahli Muda  -  Teknik Otomotif'),
    ('Guru Ahli Pertama - Bahasa Indonesia', 'Guru Ahli Pertama  - Bahasa  Indonesia'),
    ('Guru Ahli Pertama - Bahasa Inggris', 'Guru Ahli Pertama  - Bahasa  Inggris'),
    ('Guru Ahli Pertama - Agama Islam', 'Guru Ahli Pertama  - Agama  Islam'),
    ('Guru Ahli Pertama - Penjasorkes', 'Guru Ahli Pertama  - Penjasorkes'),
    ('Guru Ahli Pertama - PPKn', 'Guru Ahli Pertama  -  PPKn'),
    ('Guru Ahli Pertama - Seni Budaya', 'Guru Ahli Pertama  -  Seni Budaya'),
    ('Guru Ahli Pertama - Bimbingan Konseling', 'Guru Ahli Pertama  - Bimbingan Konseling'),
    ('Guru Ahli Pertama - Teknik Ketenagalistrikan', 'Guru Ahli Pertama  - Teknik Ketenagalistrikan'),
    ('Guru Ahli Pertama - Matematika', 'Guru Ahli Pertama  -  Matematika'),
    ('Guru Ahli Pertama - Teknik Pengelasan dan Fabrikasi Logam', 'Guru Ahli Pertama  -  Teknik Pengelasan dan Fabrikasi Logam'),
    ('Guru Ahli Pertama - Teknik Jaringan Komputer dan Telekomunikasi', 'Guru Ahli Pertama  -  Teknik Jaringan Komputer dan Telekomunikasi'),
    ('Asisten Perpustakaan Terampil', 'Asisten Perpustakaan Terampil'),
]

class SPMTForm(forms.ModelForm):
    sebagai = forms.ChoiceField(choices=JABATAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = SPMT
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_surat': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'peraturan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nomor_peraturan': forms.TextInput(attrs={'class': 'form-control'}),
            'tahun_peraturan': forms.TextInput(attrs={'class': 'form-control'}),
            'tentang': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'tanggal_terhitung': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tempat_tugas': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama

class SuratUmumForm(forms.ModelForm):
    class Meta:
        model = SuratUmum
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'penandatangan': forms.Select(attrs={'class': 'form-control'}),
            'pembuka_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'isi_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'penutup_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penandatangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penandatangan'].label_from_instance = lambda obj: obj.nama


class SuratPanggilanSiswaForm(forms.ModelForm):
    class Meta:
        model = SuratPanggilanSiswa
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'orang_tua': forms.TextInput(attrs={'class': 'form-control'}),
            'keterangan_panggilan': forms.Select(attrs={'class': 'form-control'}),
            'alasan_panggilan': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tempat_panggilan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_panggilan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'waktu_panggilan': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'wali_kelas': forms.Select(attrs={'class': 'form-control'}),
            'guru_bk': forms.Select(attrs={'class': 'form-control'}),
            'wakasek_kesiswaan': forms.Select(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['wali_kelas'].queryset = ASN.objects.all().order_by('nama')
        self.fields['guru_bk'].queryset = ASN.objects.all().order_by('nama')
        self.fields['wakasek_kesiswaan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['siswa'].label_from_instance = lambda obj: obj.nama
        self.fields['wali_kelas'].label_from_instance = lambda obj: f'{obj.nama} - {obj.jabatan}'
        self.fields['guru_bk'].label_from_instance = lambda obj: f'{obj.nama} - {obj.jabatan}'
        self.fields['wakasek_kesiswaan'].label_from_instance = lambda obj: f'{obj.nama} - {obj.jabatan}'
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama

class SuratUndanganSiswaForm(forms.ModelForm):
    class Meta:
        model = SuratUndanganSiswa
        fields = '__all__'
        widgets = {
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
            'nomor_surat': forms.TextInput(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'orang_tua': forms.TextInput(attrs={'class': 'form-control'}),
            'perihal': forms.TextInput(attrs={'class': 'form-control'}),
            'isi_undangan': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tempat': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'waktu': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'kepala_sekolah': forms.Select(attrs={'class': 'form-control'}),
            'tempat_ditetapkan': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal_ditetapkan': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['kepala_sekolah'].queryset = ASN.objects.all().order_by('nama')
        self.fields['kop_surat'].queryset = KopSurat.objects.all().order_by('nama')
        self.fields['siswa'].label_from_instance = lambda obj: obj.nama
        self.fields['kepala_sekolah'].label_from_instance = lambda obj: f'{obj.nama} - {obj.jabatan}'
        self.fields['kop_surat'].label_from_instance = lambda obj: obj.nama

class SiswaKeluarForm(forms.ModelForm):
    class Meta:
        model = SiswaKeluar
        fields = '__all__'
        widgets = {
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_keluar': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'alasan_keluar': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Contoh: Pindah sekolah, Drop out, Kelulusan, dll'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['siswa'].label_from_instance = lambda obj: f'{obj.nama} - {obj.kelas} - {obj.jurusan if obj.jurusan else ""}'


class PesertaNotaDinasForm(forms.ModelForm):
    class Meta:
        model = PesertaNotaDinas
        fields = ['pegawai', 'siswa', 'peran', 'bidang_lomba']
        widgets = {
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'peran': forms.Select(attrs={'class': 'form-control'}),
            'bidang_lomba': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['siswa'].label_from_instance = lambda obj: f'{obj.nama} - {obj.kelas}'
        self.fields['pegawai'].empty_label = '-- Pilih Pegawai --'
        self.fields['siswa'].empty_label = '-- Pilih Siswa --'


class PesertaNotaDinasCRUDForm(forms.ModelForm):
    class Meta:
        model = PesertaNotaDinas
        fields = ['nota_dinas', 'pegawai', 'siswa', 'peran', 'bidang_lomba']
        widgets = {
            'nota_dinas': forms.Select(attrs={'class': 'form-control'}),
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'siswa': forms.Select(attrs={'class': 'form-control'}),
            'peran': forms.Select(attrs={'class': 'form-control'}),
            'bidang_lomba': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nota_dinas'].queryset = NotaDinas.objects.all().order_by('tanggal')
        self.fields['nota_dinas'].label_from_instance = lambda obj: f"{obj.nomor} - {obj.hal}"
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['siswa'].queryset = Siswa.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['siswa'].label_from_instance = lambda obj: f'{obj.nama} - {obj.kelas}'
        self.fields['pegawai'].empty_label = '-- Pilih Pegawai --'
        self.fields['siswa'].empty_label = '-- Pilih Siswa --'


BasePesertaNotaDinasFormSet = inlineformset_factory(
    NotaDinas, PesertaNotaDinas,
    form=PesertaNotaDinasForm,
    extra=1,
    can_delete=True
)


class PesertaNotaDinasFormSet(BasePesertaNotaDinasFormSet):
    def save_new(self, form, commit=True):
        if not form.cleaned_data.get('pegawai') and not form.cleaned_data.get('siswa'):
            return None
        return super().save_new(form, commit=commit)
