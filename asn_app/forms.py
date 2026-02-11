# asn_app/forms.py
from django import forms
from .models import (
    ASN, SuratPerintahTugas, KopSurat, SuratSantunanKorpri, 
    NotaDinas, HariLibur, SuratCuti, SisaCuti, Siswa, 
    SuratKeterangan, SuratResmi, SPTJM, SPMT, FotoKegiatan, SuratUmum
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
    class Meta:
        model = NotaDinas
        fields = '__all__'
        widgets = {
            'kepada': forms.TextInput(attrs={'class': 'form-control'}),
            'dari': forms.TextInput(attrs={'class': 'form-control'}),
            'tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nomor': forms.TextInput(attrs={'class': 'form-control'}),
            'sifat': forms.TextInput(attrs={'class': 'form-control'}),
            'lampiran': forms.TextInput(attrs={'class': 'form-control'}),
            'hal': forms.TextInput(attrs={'class': 'form-control'}),
            'isi_surat': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'pegawai': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'penutup_surat': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'kop_surat': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pegawai'].queryset = ASN.objects.all().order_by('nama')
        self.fields['penanda_tangan'].queryset = ASN.objects.all().order_by('nama')
        self.fields['pegawai'].label_from_instance = lambda obj: obj.nama
        self.fields['penanda_tangan'].label_from_instance = lambda obj: obj.nama

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
        exclude = ('total_sisa_cuti',) # Exclude total_sisa_cuti as it's calculated automatically
        widgets = {
            'pegawai': forms.Select(attrs={'class': 'form-control'}),
            'sisa_tahun_n': forms.NumberInput(attrs={'class': 'form-control'}),
            'sisa_tahun_n_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sisa_tahun_n_2': forms.NumberInput(attrs={'class': 'form-control'}),
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

class SPMTForm(forms.ModelForm):
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
            'sebagai': forms.TextInput(attrs={'class': 'form-control'}),
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