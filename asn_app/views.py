from django.conf import settings
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Count 
from .models import ASN, SuratPerintahTugas, KopSurat, SuratSantunanKorpri, NotaDinas, HariLibur, SuratCuti, SisaCuti, Siswa, SuratKeterangan, SuratResmi, SPTJM, SPMT, FotoKegiatan, SuratUmum
from .forms import ASNForm, SPTForm, KopSuratForm, SuratSantunanKorpriForm, NotaDinasForm, HariLiburForm, SuratCutiForm, SisaCutiForm, SiswaForm, SuratKeteranganForm, SuratResmiForm, SPTJMForm, SPMTForm, FotoKegiatanForm, SuratUmumForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
import base64
import os



def asn_list(request):
    """Menampilkan daftar semua ASN"""
    query = request.GET.get('q')
    if query:
        asn_queryset = ASN.objects.filter(nama__icontains=query).order_by('nama')
    else:
        asn_queryset = ASN.objects.all().order_by('nama')

    paginator = Paginator(asn_queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'asn_app/asn_list.html', {'page_obj': page_obj, 'query': query})

def asn_detail(request, pk):
    """Menampilkan detail ASN"""
    asn = get_object_or_404(ASN, pk=pk)
    return render(request, 'asn_app/asn_detail.html', {'asn': asn})

def asn_create(request):
    """Membuat ASN baru"""
    if request.method == 'POST':
        form = ASNForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asn_list')
    else:
        form = ASNForm()
    return render(request, 'asn_app/asn_form.html', {'form': form, 'title': 'Tambah ASN'})

def asn_update(request, pk):
    """Mengupdate data ASN"""
    asn = get_object_or_404(ASN, pk=pk)
    if request.method == 'POST':
        form = ASNForm(request.POST, request.FILES, instance=asn)
        if form.is_valid():
            form.save()
            return redirect('asn_detail', pk=asn.pk)
    else:
        form = ASNForm(instance=asn)
    return render(request, 'asn_app/asn_form.html', {'form': form, 'title': 'Edit ASN'})

def asn_delete(request, pk):
    """Menghapus data ASN"""
    asn = get_object_or_404(ASN, pk=pk)
    if request.method == 'POST':
        asn.delete()
        return redirect('asn_list')
    return render(request, 'asn_app/asn_confirm_delete.html', {'asn': asn})

def asn_export_pdf(request, pk):
    """Export profil ASN ke PDF"""
    import os
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    asn = get_object_or_404(ASN, pk=pk)

    # Render template HTML dengan current time
    html_string = render_to_string('asn_app/asn_pdf_template.html', {
        'asn': asn,
        'current_time': now(),
        'request': request,
    })

    # Create PDF
    try:
        html = HTML(string=html_string)
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)


    # Create HTTP response dgn PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=profil_{asn.nip}_{asn.nama}.pdf'

    return response

def asn_print_view(request, pk):
    """Tampilan khusus untuk print"""
    asn = get_object_or_404(ASN, pk=pk)
    return render(request, 'asn_app/asn_print.html', {
        'asn': asn,
        'current_time': now()
    })

# SPT Views
def spt_list(request):
    """Menampilkan daftar semua SPT"""
    spt_list = SuratPerintahTugas.objects.all().order_by('-created_at')
    return render(request, 'asn_app/spt_list.html', {'spt_list': spt_list})

def spt_detail(request, pk):
    """Menampilkan detail SPT"""
    spt = get_object_or_404(SuratPerintahTugas, pk=pk)
    fotos = spt.foto_kegiatan.all()
    return render(request, 'asn_app/spt_detail.html', {'spt': spt, 'fotos': fotos})


def spt_laporan(request, pk):
    """Menampilkan laporan SPT"""
    spt = get_object_or_404(SuratPerintahTugas, pk=pk)
    fotos = spt.foto_kegiatan.all()

    # Group photos into sets of 4
    grouped_fotos = []
    for i in range(0, len(fotos), 4):
        grouped_fotos.append(fotos[i:i + 4])
        
    return render(request, 'asn_app/spt_laporan.html', {'spt': spt, 'grouped_fotos': grouped_fotos})


def upload_foto_kegiatan(request, spt_pk):
    spt = get_object_or_404(SuratPerintahTugas, pk=spt_pk)
    if request.method == 'POST':
        # Form ini sekarang hanya berisi 'keterangan'
        form = FotoKegiatanForm(request.POST) 
        if form.is_valid():
            files = request.FILES.getlist('foto')
            
            # Cek jika tidak ada file yang di-upload
            if not files:
                messages.error(request, 'Tidak ada file foto yang dipilih untuk diupload.')
                # Render kembali halaman dengan form yang ada
                return render(request, 'asn_app/upload_foto_kegiatan.html', {'form': form, 'spt': spt})

            for f in files:
                instance = FotoKegiatan(
                    spt=spt,
                    foto=f,
                    keterangan=form.cleaned_data['keterangan']
                )
                instance.save()
            
            messages.success(request, f'{len(files)} foto berhasil diupload.')
            return redirect('spt_detail', pk=spt.pk)
    else:
        form = FotoKegiatanForm()
    return render(request, 'asn_app/upload_foto_kegiatan.html', {'form': form, 'spt': spt})


def delete_foto_kegiatan(request, foto_pk):
    foto = get_object_or_404(FotoKegiatan, pk=foto_pk)
    spt_pk = foto.spt.pk
    if request.method == 'POST':
        foto.delete()
        return redirect('spt_detail', pk=spt_pk)
    return render(request, 'asn_app/delete_foto_kegiatan.html', {'foto': foto})


def cetak_foto_kegiatan_pdf(request, spt_pk):
    """Export activity photos to PDF"""
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    spt = get_object_or_404(SuratPerintahTugas, pk=spt_pk)
    fotos = spt.foto_kegiatan.all()

    # Encode images to base64
    encoded_fotos = []
    for foto in fotos:
        if foto.foto and os.path.exists(foto.foto.path):
            try:
                with open(foto.foto.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = foto.foto.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    encoded_foto = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
                    encoded_fotos.append({
                        'base64': encoded_foto,
                        'keterangan': foto.keterangan
                    })
            except Exception as e:
                logging.error(f"Error encoding image to base64: {e}")

    # Group photos into sets of four for display on A4 page (2x2 grid)
    grouped_fotos = []
    for i in range(0, len(encoded_fotos), 4):
        grouped_fotos.append(encoded_fotos[i:i + 4])

    # Render template HTML
    html_string = render_to_string('asn_app/cetak_foto_kegiatan_pdf.html', {
        'spt': spt,
        'grouped_fotos': grouped_fotos,
    })

    # Create PDF
    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    # Create HTTP response dgn PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=foto_kegiatan_{spt.nomor_spt}.pdf'

    return response


def spt_create(request):
    """Membuat SPT baru"""
    if request.method == 'POST':
        form = SPTForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('spt_list')
    else:
        form = SPTForm()
    return render(request, 'asn_app/spt_form.html', {'form': form, 'title': 'Tambah SPT'})

def spt_update(request, pk):
    """Mengupdate data SPT"""
    spt = get_object_or_404(SuratPerintahTugas, pk=pk)
    if request.method == 'POST':
        form = SPTForm(request.POST, instance=spt)
        if form.is_valid():
            form.save()
            return redirect('spt_detail', pk=spt.pk)
    else:
        form = SPTForm(instance=spt)
    return render(request, 'asn_app/spt_form.html', {'form': form, 'title': 'Edit SPT'})

def spt_delete(request, pk):
    """Menghapus data SPT"""
    spt = get_object_or_404(SuratPerintahTugas, pk=pk)
    if request.method == 'POST':
        spt.delete()
        return redirect('spt_list')
    return render(request, 'asn_app/spt_confirm_delete.html', {'spt': spt})

def spt_export_pdf(request, pk):
    """Export SPT ke PDF"""
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    spt = get_object_or_404(SuratPerintahTugas, pk=pk)

    # Debug logging
    logger = logging.getLogger(__name__)
    logger.info(f"spt: {spt}")
    logger.info(f"spt.kop_surat: {spt.kop_surat}")

    kop_surat_base64 = None
    if spt.kop_surat and spt.kop_surat.gambar:
        logger.info(f"spt.kop_surat.gambar: {spt.kop_surat.gambar}")
        logger.info(f"spt.kop_surat.gambar.url: {spt.kop_surat.gambar.url}")
        logger.info(f"spt.kop_surat.gambar.path: {spt.kop_surat.gambar.path}")

        # Cek apakah file benar-benar ada
        if os.path.exists(spt.kop_surat.gambar.path):
            logger.info("File gambar KOP SURAT ADA di filesystem")
            # Encode gambar ke base64
            try:
                with open(spt.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = spt.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
                    logger.info("Gambar berhasil di-encode ke base64")
            except Exception as e:
                logger.error(f"Error encoding image to base64: {e}")
        else:
            logger.error("File gambar KOP SURAT TIDAK ADA di filesystem")

    # Choose template based on participant count
    template_name = 'asn_app/spt_pdf_template_large.html' if spt.peserta.all().count() > 3 else 'asn_app/spt_pdf_template.html'

    # Render template HTML
    html_string = render_to_string(template_name, {
        'spt': spt,
        'current_time': now(),
        'request': request,
        'MEDIA_URL': '/media/',  # Tambahkan MEDIA_URL secara manual
        'kop_surat_base64': kop_surat_base64,
    })

    # Create PDF
    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logger.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    # Create HTTP response dgn PDF
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=spt_{spt.nomor_spt}_{spt.nama_kegiatan}.pdf'

    return response

def spt_print_view(request, pk):
    """Tampilan khusus untuk print SPT"""
    spt = get_object_or_404(SuratPerintahTugas, pk=pk)
    return render(request, 'asn_app/spt_print.html', {
        'spt': spt,
        'current_time': now()
    })

def spt_export_pdf_large(request, pk):
    """Export SPT ke PDF dengan daftar peserta lengkap"""
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    spt = get_object_or_404(SuratPerintahTugas, pk=pk)

    logger = logging.getLogger(__name__)

    kop_surat_base64 = None
    if spt.kop_surat and spt.kop_surat.gambar:
        if os.path.exists(spt.kop_surat.gambar.path):
            try:
                with open(spt.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = spt.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logger.error(f"Error encoding image to base64 for large PDF: {e}")

    html_string = render_to_string('asn_app/spt_pdf_template_large.html', {
        'spt': spt,
        'current_time': now(),
        'request': request,
        'MEDIA_URL': '/media/',
        'kop_surat_base64': kop_surat_base64,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logger.error(f"Error writing large PDF: {e}")
        return HttpResponse(f"Error writing large PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=spt_lengkap_{spt.nomor_spt}_{spt.nama_kegiatan}.pdf'

    return response


# Kop Surat Views
def kop_surat_list(request):
    """Menampilkan daftar semua Kop Surat"""
    kop_surat_list = KopSurat.objects.all().order_by('-created_at')
    return render(request, 'asn_app/kop_surat_list.html', {'kop_surat_list': kop_surat_list})

def kop_surat_detail(request, pk):
    """Menampilkan detail Kop Surat"""
    kop_surat = get_object_or_404(KopSurat, pk=pk)
    return render(request, 'asn_app/kop_surat_detail.html', {'kop_surat': kop_surat})

def kop_surat_create(request):
    """Membuat Kop Surat baru"""
    if request.method == 'POST':
        form = KopSuratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kop_surat_list')
    else:
        form = KopSuratForm()
    return render(request, 'asn_app/kop_surat_form.html', {'form': form, 'title': 'Tambah Kop Surat'})

def kop_surat_update(request, pk):
    """Mengupdate data Kop Surat"""
    kop_surat = get_object_or_404(KopSurat, pk=pk)
    if request.method == 'POST':
        form = KopSuratForm(request.POST, request.FILES, instance=kop_surat)
        if form.is_valid():
            form.save()
            return redirect('kop_surat_detail', pk=kop_surat.pk)
    else:
        form = KopSuratForm(instance=kop_surat)
    return render(request, 'asn_app/kop_surat_form.html', {'form': form, 'title': 'Edit Kop Surat'})

def kop_surat_delete(request, pk):
    """Menghapus data Kop Surat"""
    kop_surat = get_object_or_404(KopSurat, pk=pk)
    if request.method == 'POST':
        kop_surat.delete()
        return redirect('kop_surat_list')
    return render(request, 'asn_app/kop_surat_confirm_delete.html', {'kop_surat': kop_surat})

def export_asn_excel(request):
    """Export all ASN data to an Excel file."""
    import openpyxl
    from openpyxl.utils import get_column_letter

    asns = ASN.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'ASN Data'

    # Write headers
    headers = [
        'NIP', 'Nama', 'Tempat Lahir', 'Tanggal Lahir', 'Jenis Kelamin',
        'Agama', 'Alamat', 'Email', 'Telepon', 'Jabatan', 'Pangkat',
        'Golongan', 'Unit Kerja'
    ]
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = header

    # Write data
    for row_num, asn in enumerate(asns, 2):
        sheet[f'A{row_num}'] = asn.nip
        sheet[f'B{row_num}'] = asn.nama
        sheet[f'C{row_num}'] = asn.tempat_lahir
        sheet[f'D{row_num}'] = asn.tanggal_lahir.strftime('%Y-%m-%d') if asn.tanggal_lahir else ''
        sheet[f'E{row_num}'] = asn.get_jenis_kelamin_display()
        sheet[f'F{row_num}'] = asn.agama
        sheet[f'G{row_num}'] = asn.alamat
        sheet[f'H{row_num}'] = asn.email
        sheet[f'I{row_num}'] = asn.telepon
        sheet[f'J{row_num}'] = asn.jabatan
        sheet[f'K{row_num}'] = asn.pangkat
        sheet[f'L{row_num}'] = asn.golongan
        sheet[f'M{row_num}'] = asn.unit_kerja

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=asn_data.xlsx'
    workbook.save(response)
    return response

def import_asn_excel(request):
    """Import ASN data from an Excel file."""
    if request.method == 'POST':
        import openpyxl
        from datetime import datetime

        excel_file = request.FILES['excel_file']
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            (
                nip, nama, tempat_lahir, tanggal_lahir_val, jenis_kelamin,
                agama, alamat, email, telepon, jabatan, pangkat,
                golongan, unit_kerja
            ) = row

            # Handle date conversion
            tanggal_lahir = None
            if isinstance(tanggal_lahir_val, datetime):
                tanggal_lahir = tanggal_lahir_val.date()
            elif isinstance(tanggal_lahir_val, str):
                try:
                    tanggal_lahir = datetime.strptime(tanggal_lahir_val, '%Y-%m-%d').date()
                except ValueError:
                    # Handle other date formats if necessary
                    pass

            # Handle choices
            jenis_kelamin_code = jenis_kelamin[0].upper() if jenis_kelamin else ''
            agama_code = agama.upper() if agama else ''

            ASN.objects.create(
                nip=nip,
                nama=nama,
                tempat_lahir=tempat_lahir,
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin_code,
                agama=agama_code,
                alamat=alamat,
                email=email,
                telepon=telepon,
                jabatan=jabatan,
                pangkat=pangkat,
                golongan=golongan,
                unit_kerja=unit_kerja
            )
        return redirect('asn_list')
    return render(request, 'asn_app/import_form.html')


# Surat Santunan Korpri Views
def surat_santunan_korpri_list(request):
    surat_list = SuratSantunanKorpri.objects.all().order_by('-created_at')
    return render(request, 'asn_app/surat_santunan_korpri_list.html', {'surat_list': surat_list})

def surat_santunan_korpri_detail(request, pk):
    surat = get_object_or_404(SuratSantunanKorpri, pk=pk)
    return render(request, 'asn_app/surat_santunan_korpri_detail.html', {'surat': surat})

def surat_santunan_korpri_create(request):
    if request.method == 'POST':
        form = SuratSantunanKorpriForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('surat_santunan_korpri_list')
    else:
        form = SuratSantunanKorpriForm()
    return render(request, 'asn_app/surat_santunan_korpri_form.html', {'form': form, 'title': 'Tambah Surat Santunan Korpri'})

def surat_santunan_korpri_update(request, pk):
    surat = get_object_or_404(SuratSantunanKorpri, pk=pk)
    if request.method == 'POST':
        form = SuratSantunanKorpriForm(request.POST, instance=surat)
        if form.is_valid():
            form.save()
            return redirect('surat_santunan_korpri_detail', pk=surat.pk)
    else:
        form = SuratSantunanKorpriForm(instance=surat)
    return render(request, 'asn_app/surat_santunan_korpri_form.html', {'form': form, 'title': 'Edit Surat Santunan Korpri'})

def surat_santunan_korpri_delete(request, pk):
    surat = get_object_or_404(SuratSantunanKorpri, pk=pk)
    if request.method == 'POST':
        surat.delete()
        return redirect('surat_santunan_korpri_list')
    return render(request, 'asn_app/surat_santunan_korpri_confirm_delete.html', {'surat': surat})

def surat_santunan_korpri_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    surat = get_object_or_404(SuratSantunanKorpri, pk=pk)
    
    kop_surat_base64 = None
    if surat.kop_surat and surat.kop_surat.gambar:
        if os.path.exists(surat.kop_surat.gambar.path):
            try:
                with open(surat.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = surat.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64 for large PDF: {e}")

    html_string = render_to_string('asn_app/surat_santunan_korpri_pdf_template.html', {
        'surat': surat,
        'request': request,
        'kop_surat_base64': kop_surat_base64,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=surat_santunan_{surat.nomor_surat}.pdf'

    return response

# Nota Dinas Views
def nota_dinas_list(request):
    nota_dinas_list = NotaDinas.objects.all().order_by('-tanggal')
    return render(request, 'asn_app/nota_dinas_list.html', {'nota_dinas_list': nota_dinas_list})

def nota_dinas_detail(request, pk):
    nota_dinas = get_object_or_404(NotaDinas, pk=pk)
    return render(request, 'asn_app/nota_dinas_detail.html', {'nota_dinas': nota_dinas})

def nota_dinas_create(request):
    if request.method == 'POST':
        form = NotaDinasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nota_dinas_list')
    else:
        form = NotaDinasForm()
    return render(request, 'asn_app/nota_dinas_form.html', {'form': form, 'title': 'Tambah Nota Dinas'})

def nota_dinas_update(request, pk):
    nota_dinas = get_object_or_404(NotaDinas, pk=pk)
    if request.method == 'POST':
        form = NotaDinasForm(request.POST, instance=nota_dinas)
        if form.is_valid():
            form.save()
            return redirect('nota_dinas_detail', pk=nota_dinas.pk)
    else:
        form = NotaDinasForm(instance=nota_dinas)
    return render(request, 'asn_app/nota_dinas_form.html', {'form': form, 'title': 'Edit Nota Dinas'})

def nota_dinas_delete(request, pk):
    nota_dinas = get_object_or_404(NotaDinas, pk=pk)
    if request.method == 'POST':
        nota_dinas.delete()
        return redirect('nota_dinas_list')
    return render(request, 'asn_app/nota_dinas_confirm_delete.html', {'nota_dinas': nota_dinas})

def nota_dinas_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    nota_dinas = get_object_or_404(NotaDinas, pk=pk)
    
    kop_surat_base64 = None
    if nota_dinas.kop_surat and nota_dinas.kop_surat.gambar:
        if os.path.exists(nota_dinas.kop_surat.gambar.path):
            try:
                with open(nota_dinas.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = nota_dinas.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64 for large PDF: {e}")

    html_string = render_to_string('asn_app/nota_dinas_pdf_template.html', {
        'nota_dinas': nota_dinas,
        'request': request,
        'kop_surat_base64': kop_surat_base64,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    return response

# Hari Libur Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class HariLiburListView(ListView):
    model = HariLibur
    template_name = 'asn_app/hari_libur_list.html'
    context_object_name = 'hari_libur_list'
    paginate_by = 10

class HariLiburDetailView(DetailView):
    model = HariLibur
    template_name = 'asn_app/hari_libur_detail.html'
    context_object_name = 'hari_libur'

class HariLiburCreateView(CreateView):
    model = HariLibur
    form_class = HariLiburForm
    template_name = 'asn_app/hari_libur_form.html'
    success_url = reverse_lazy('hari_libur_list')

class HariLiburUpdateView(UpdateView):
    model = HariLibur
    form_class = HariLiburForm
    template_name = 'asn_app/hari_libur_form.html'
    context_object_name = 'hari_libur'

    def get_success_url(self):
        return reverse_lazy('hari_libur_detail', kwargs={'pk': self.object.pk})

class HariLiburDeleteView(DeleteView):
    model = HariLibur
    template_name = 'asn_app/hari_libur_confirm_delete.html'
    success_url = reverse_lazy('hari_libur_list')
    context_object_name = 'hari_libur'

# Surat Cuti Views
class SuratCutiListView(ListView):
    model = SuratCuti
    template_name = 'asn_app/surat_cuti_list.html'
    context_object_name = 'surat_cuti_list'
    paginate_by = 10

class SuratCutiDetailView(DetailView):
    model = SuratCuti
    template_name = 'asn_app/surat_cuti_detail.html'
    context_object_name = 'surat_cuti'

class SuratCutiCreateView(CreateView):
    model = SuratCuti
    form_class = SuratCutiForm
    template_name = 'asn_app/surat_cuti_form.html'
    success_url = reverse_lazy('surat_cuti_list')

class SuratCutiUpdateView(UpdateView):
    model = SuratCuti
    form_class = SuratCutiForm
    template_name = 'asn_app/surat_cuti_form.html'
    context_object_name = 'surat_cuti'

    def get_success_url(self):
        return reverse_lazy('surat_cuti_detail', kwargs={'pk': self.object.pk})

class SuratCutiDeleteView(DeleteView):
    model = SuratCuti
    template_name = 'asn_app/surat_cuti_confirm_delete.html'
    success_url = reverse_lazy('surat_cuti_list')
    context_object_name = 'surat_cuti'

# Sisa Cuti Views
class SisaCutiListView(ListView):
    model = SisaCuti
    template_name = 'asn_app/sisa_cuti_list.html'
    context_object_name = 'sisa_cuti_list'
    paginate_by = 10

class SisaCutiDetailView(DetailView):
    model = SisaCuti
    template_name = 'asn_app/sisa_cuti_detail.html'
    context_object_name = 'sisa_cuti'

class SisaCutiCreateView(CreateView):
    model = SisaCuti
    form_class = SisaCutiForm
    template_name = 'asn_app/sisa_cuti_form.html'
    success_url = reverse_lazy('sisa_cuti_list')

class SisaCutiUpdateView(UpdateView):
    model = SisaCuti
    form_class = SisaCutiForm
    template_name = 'asn_app/sisa_cuti_form.html'
    context_object_name = 'sisa_cuti'

    def get_success_url(self):
        return reverse_lazy('sisa_cuti_detail', kwargs={'pk': self.object.pk})

class SisaCutiDeleteView(DeleteView):
    model = SisaCuti
    template_name = 'asn_app/sisa_cuti_confirm_delete.html'
    success_url = reverse_lazy('sisa_cuti_list')
    context_object_name = 'sisa_cuti'

def surat_cuti_export_pdf(request, pk):
    import os
    import base64
    from datetime import date, timedelta
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    surat_cuti = get_object_or_404(SuratCuti, pk=pk)

    logger = logging.getLogger(__name__)
    logger.info(f"Generating PDF for SuratCuti: {surat_cuti}")

    # Calculate leave duration
    try:
        leave_days = surat_cuti.calculate_effective_leave_days()

        # Convert number to Indonesian words
        number_words = {
            1: "satu", 2: "dua", 3: "tiga", 4: "empat", 5: "lima",
            6: "enam", 7: "tujuh", 8: "delapan", 9: "sembilan", 10: "sepuluh",
            11: "sebelas", 12: "dua belas", 13: "tiga belas", 14: "empat belas",
            15: "lima belas", 16: "enam belas", 17: "tujuh belas", 18: "delapan belas",
            19: "sembilan belas", 20: "dua puluh"
        }

        if leave_days in number_words:
            written_number = number_words[leave_days]
        else:
            written_number = str(leave_days)  # fallback for larger numbers

        # Define Indonesian month names
        month_names = {
            'January': 'Januari', 'February': 'Februari', 'March': 'Maret', 'April': 'April',
            'May': 'Mei', 'June': 'Juni', 'July': 'Juli', 'August': 'Agustus',
            'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Desember'
        }

        # Format dates with English month names first, then replace with Indonesian names
        start_date_str = surat_cuti.tanggal_awal.strftime('%d %B %Y')
        end_date_str = surat_cuti.tanggal_akhir.strftime('%d %B %Y')

        # Replace English month names with Indonesian
        for eng_month, indo_month in month_names.items():
            start_date_str = start_date_str.replace(eng_month, indo_month)
            end_date_str = end_date_str.replace(eng_month, indo_month)

        if surat_cuti.tanggal_awal == surat_cuti.tanggal_akhir:
            leave_duration_text = f"selama {leave_days} ({written_number}) hari kerja, terhitung mulai tanggal {start_date_str}"
        else:
            leave_duration_text = f"selama {leave_days} ({written_number}) hari kerja, terhitung mulai tanggal {start_date_str} sampai dengan tanggal {end_date_str}"
        logger.info(f"Leave duration: {leave_duration_text}")
    except Exception as e:
        logger.error(f"Error calculating leave duration: {e}")
        leave_duration_text = "durasi cuti tidak dapat dihitung"

    # Handle kop surat
    kop_surat_base64 = None
    if surat_cuti.kop_surat and surat_cuti.kop_surat.gambar:
        logger.info(f"Kop surat: {surat_cuti.kop_surat}, gambar: {surat_cuti.kop_surat.gambar}")
        if os.path.exists(surat_cuti.kop_surat.gambar.path):
            try:
                with open(surat_cuti.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = surat_cuti.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
                    logger.info("Kop surat encoded successfully")
            except Exception as e:
                logger.error(f"Error encoding image to base64: {e}")
        else:
            logger.error("Kop surat file does not exist")

    try:
        html_string = render_to_string('asn_app/surat_cuti_pdf_template.html', {
            'surat_cuti': surat_cuti,
            'leave_duration_text': leave_duration_text,
            'kop_surat_base64': kop_surat_base64,
            'request': request,
        })
        logger.info("HTML template rendered successfully")
        # Write rendered HTML to a debug file to inspect template rendering
        try:
            from django.conf import settings
            debug_path = getattr(settings, 'BASE_DIR', '.')
            debug_file = os.path.join(debug_path, f'debug_surat_cuti_{surat_cuti.pk}.html')
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html_string)
            logger.info(f"Wrote debug HTML to {debug_file}")
        except Exception as e:
            logger.error(f"Error writing debug HTML file: {e}")
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        return HttpResponse(f"Error rendering template: {e}", status=500)

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
        logger.info(f"PDF generated successfully, size: {len(result)} bytes")
    except Exception as e:
        logger.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    # Sanitize filename to avoid issues with special characters
    safe_name = "".join(c for c in surat_cuti.pegawai.nama if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f'surat_cuti_{safe_name}.pdf'

    response = HttpResponse(result, content_type='application/pdf')
    # Explicitly delete any existing Content-Disposition header before setting our own
    if 'Content-Disposition' in response:
        del response['Content-Disposition']
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def laporan_cuti_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    asn = get_object_or_404(ASN, pk=pk)
    # Order by tanggal_awal to ensure correct running balance calculation
    surat_cuti_queryset = SuratCuti.objects.filter(pegawai=asn).order_by('tanggal_awal')
    sisa_cuti_obj = SisaCuti.objects.filter(pegawai=asn).first()

    # Initialize running balances with initial values
    # These will represent the balance *before* the current leave is applied
    initial_sisa_tahun_n = sisa_cuti_obj.sisa_tahun_n if sisa_cuti_obj else 0
    initial_total_sisa_cuti = sisa_cuti_obj.total_sisa_cuti if sisa_cuti_obj else 0

    # Create a list to hold processed leave data
    processed_surat_cuti_list = []

    # Start with the initial balances for the first row's "before leave" state
    current_sisa_tahun_n_balance = initial_sisa_tahun_n # This will be the running balance for sisa_tahun_n
    current_total_sisa_cuti_balance = initial_total_sisa_cuti # This will be the running balance for total_sisa_cuti

    for surat_cuti in surat_cuti_queryset:
        lhc = surat_cuti.calculate_effective_leave_days()

        # ATB for this row is the total accumulated leave *before* this leave is taken
        atb_for_row = current_total_sisa_cuti_balance

        # STB for this row is ATB for this row minus LHC for this row
        stb_for_row = atb_for_row - lhc

        # Update running balances for the *next* iteration
        current_sisa_tahun_n_balance -= lhc
        current_total_sisa_cuti_balance -= lhc

        processed_surat_cuti_list.append({
            'surat_cuti': surat_cuti,
            'lhc': lhc,
            'atb_for_row': atb_for_row, # This is the ATB value to display in the current row
            'stb_for_row': stb_for_row, # This is the STB value to display in the current row
        })

    # Default penandatangan if not found
    penandatangan = ASN.objects.filter(jabatan__icontains="kepala sekolah").first()
    if not penandatangan:
        penandatangan = ASN(nama="[Nama Kepala Sekolah]", nip="[NIP Kepala Sekolah]", pangkat="[Pangkat]", golongan="[Golongan]", jabatan="Kepala Sekolah")

    html_string = render_to_string('asn_app/laporan_cuti_pdf_template.html', {
        'asn': asn,
        'processed_surat_cuti_list': processed_surat_cuti_list, # Pass the processed list
        'sisa_cuti': sisa_cuti_obj, # Still pass the original sisa_cuti for the summary below the table
        'penandatangan': penandatangan,
        'request': request,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing Laporan Cuti PDF: {e}")
        return HttpResponse(f"Error writing Laporan Cuti PDF: {e}", status=500)

    safe_name = "".join(c for c in asn.nama if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f'laporan_cuti_{safe_name}.pdf'

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


# Siswa Views
def siswa_list(request):
    """Menampilkan daftar semua Siswa"""
    query = request.GET.get('q')
    if query:
        siswa_queryset = Siswa.objects.filter(nama__icontains=query).order_by('nama')
    else:
        siswa_queryset = Siswa.objects.all().order_by('nama')

    # Dashboard data
    total_siswa = Siswa.objects.count() # Corrected: Count all students
    
    # Counts by jurusan, excluding null/blank
    siswa_by_jurusan = Siswa.objects.filter(jurusan__isnull=False).exclude(jurusan__exact='').values('jurusan').annotate(count=Count('jurusan')).order_by('jurusan')
    
    # Counts by kelas, excluding null/blank
    siswa_by_kelas = Siswa.objects.filter(kelas__isnull=False).exclude(kelas__exact='').values('kelas').annotate(count=Count('kelas')).order_by('kelas')


    paginator = Paginator(siswa_queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'total_siswa': total_siswa,
        'siswa_by_jurusan': siswa_by_jurusan,
        'siswa_by_kelas': siswa_by_kelas,
    }

    return render(request, 'asn_app/siswa_list.html', context)

def siswa_detail(request, pk):
    """Menampilkan detail Siswa"""
    siswa = get_object_or_404(Siswa, pk=pk)
    return render(request, 'asn_app/siswa_detail.html', {'siswa': siswa})

def siswa_create(request):
    """Membuat Siswa baru"""
    if request.method == 'POST':
        form = SiswaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('siswa_list')
    else:
        form = SiswaForm()
    return render(request, 'asn_app/siswa_form.html', {'form': form, 'title': 'Tambah Siswa'})

def siswa_update(request, pk):
    """Mengupdate data Siswa"""
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        form = SiswaForm(request.POST, request.FILES, instance=siswa)
        if form.is_valid():
            form.save()
            return redirect('siswa_detail', pk=siswa.pk)
    else:
        form = SiswaForm(instance=siswa)
    return render(request, 'asn_app/siswa_form.html', {'form': form, 'title': 'Edit Siswa'})

def siswa_delete(request, pk):
    """Menghapus data Siswa"""
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        siswa.delete()
        return redirect('siswa_list')
    return render(request, 'asn_app/siswa_confirm_delete.html', {'siswa': siswa})

def siswa_delete_all(request):
    """Menghapus semua data Siswa"""
    if request.method == 'POST':
        count, _ = Siswa.objects.all().delete()
        messages.success(request, f'{count} data Siswa berhasil dihapus.')
        return redirect('siswa_list')
    return redirect('siswa_list') # Redirect to list if GET request

# Surat Keterangan Views
def surat_keterangan_list(request):
    logger = logging.getLogger(__name__)
    queryset = SuratKeterangan.objects.filter(pk__isnull=False).order_by('-created_at')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'asn_app/surat_keterangan_list.html', {'page_obj': page_obj})

def surat_keterangan_detail(request, pk):
    surat = get_object_or_404(SuratKeterangan, pk=pk)
    return render(request, 'asn_app/surat_keterangan_detail.html', {'surat': surat})

def surat_keterangan_create(request):
    logger = logging.getLogger(__name__)
    if request.method == 'POST':
        logger.info(f"Surat Keterangan POST data: {request.POST}")
        form = SuratKeteranganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('surat_keterangan_list')
        else:
            logger.error(f"Surat Keterangan form errors: {form.errors.as_json()}")
    else:
        form = SuratKeteranganForm()
    return render(request, 'asn_app/surat_keterangan_form.html', {'form': form, 'title': 'Tambah Surat Keterangan'})

def surat_keterangan_update(request, pk):
    surat = get_object_or_404(SuratKeterangan, pk=pk)
    if request.method == 'POST':
        form = SuratKeteranganForm(request.POST, instance=surat)
        if form.is_valid():
            form.save()
            return redirect('surat_keterangan_detail', pk=surat.pk)
    else:
        form = SuratKeteranganForm(instance=surat)
    return render(request, 'asn_app/surat_keterangan_form.html', {'form': form, 'title': 'Edit Surat Keterangan'})

def surat_keterangan_delete(request, pk):
    surat = get_object_or_404(SuratKeterangan, pk=pk)
    if request.method == 'POST':
        surat.delete()
        return redirect('surat_keterangan_list')
    return render(request, 'asn_app/surat_keterangan_confirm_delete.html', {'surat': surat})

def surat_keterangan_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    surat = get_object_or_404(SuratKeterangan, pk=pk)

    kop_surat_base64 = None
    if surat.kop_surat and surat.kop_surat.gambar:
        if os.path.exists(surat.kop_surat.gambar.path):
            try:
                with open(surat.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = surat.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64: {e}")

    html_string = render_to_string('asn_app/surat_keterangan_pdf_template.html', {
        'surat': surat,
        'request': request,
        'kop_surat_base64': kop_surat_base64,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=surat_keterangan_{surat.nomor_surat}.pdf'

    return response

# Surat Resmi Views
def surat_resmi_list(request):
    surat_list = SuratResmi.objects.all().order_by('-created_at')
    return render(request, 'asn_app/surat_resmi_list.html', {'surat_list': surat_list})

def surat_resmi_detail(request, pk):
    surat = get_object_or_404(SuratResmi, pk=pk)
    return render(request, 'asn_app/surat_resmi_detail.html', {'surat': surat})

def surat_resmi_create(request):
    if request.method == 'POST':
        form = SuratResmiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('surat_resmi_list')
    else:
        form = SuratResmiForm()
    return render(request, 'asn_app/surat_resmi_form.html', {'form': form, 'title': 'Tambah Surat Resmi'})

def surat_resmi_update(request, pk):
    surat = get_object_or_404(SuratResmi, pk=pk)
    if request.method == 'POST':
        form = SuratResmiForm(request.POST, instance=surat)
        if form.is_valid():
            form.save()
            return redirect('surat_resmi_detail', pk=surat.pk)
    else:
        form = SuratResmiForm(instance=surat)
    return render(request, 'asn_app/surat_resmi_form.html', {'form': form, 'title': 'Edit Surat Resmi'})

def surat_resmi_delete(request, pk):
    surat = get_object_or_404(SuratResmi, pk=pk)
    if request.method == 'POST':
        surat.delete()
        return redirect('surat_resmi_list')
    return render(request, 'asn_app/surat_resmi_confirm_delete.html', {'surat': surat})

def surat_resmi_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML

    surat = get_object_or_404(SuratResmi, pk=pk)

    kop_surat_base64 = None
    if surat.kop_surat and surat.kop_surat.gambar:
        if os.path.exists(surat.kop_surat.gambar.path):
            try:
                with open(surat.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = surat.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64: {e}")

    html_string = render_to_string('asn_app/surat_resmi_pdf_template.html', {
        'surat': surat,
        'request': request,
        'kop_surat_base64': kop_surat_base64,
    })

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=surat_resmi_{surat.nomor}.pdf'

    return response

def export_siswa_excel(request):
    """Export all Siswa data to an Excel file."""
    import openpyxl
    from openpyxl.utils import get_column_letter

    siswas = Siswa.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Siswa Data'

    # Write headers
    headers = [
        'NIS', 'Nama', 'Kelas', 'Jurusan', 'Alamat', 'No HP', 'Nama Orang Tua'
    ]
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = header

    # Write data
    for row_num, siswa in enumerate(siswas, 2):
        sheet[f'A{row_num}'] = siswa.nis
        sheet[f'B{row_num}'] = siswa.nama
        sheet[f'C{row_num}'] = siswa.kelas
        sheet[f'D{row_num}'] = siswa.jurusan
        sheet[f'E{row_num}'] = siswa.alamat
        sheet[f'F{row_num}'] = siswa.no_hp
        sheet[f'G{row_num}'] = siswa.nama_orang_tua

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=siswa_data.xlsx'
    workbook.save(response)
    return response

def import_siswa_excel(request):
    """Import Siswa data from an Excel file."""
    if request.method == 'POST':
        import openpyxl
        excel_file = request.FILES['excel_file']
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            (
                nama, nis, kelas, jurusan, alamat, no_hp, nama_orang_tua
            ) = row # Assuming these are the columns in the excel

            Siswa.objects.create(
                nama=nama,
                nis=nis,
                kelas=kelas,
                jurusan=jurusan,
                alamat=alamat,
                no_hp=no_hp,
                nama_orang_tua=nama_orang_tua
            )
        return redirect('siswa_list')
    return render(request, 'asn_app/import_form.html')



class SuratResmiListView(ListView):
    model = SuratResmi
    template_name = 'asn_app/surat_resmi_list.html'
    context_object_name = 'surat_resmi_list'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nomor__icontains=query) |
                Q(perihal__icontains=query) |
                Q(pejabat_tujuan_surat__icontains=query)
            )
        return queryset.order_by('-created_at')


class SuratResmiDetailView(DetailView):
    model = SuratResmi
    template_name = 'asn_app/surat_resmi_detail.html'
    context_object_name = 'surat_resmi'


class SuratResmiCreateView(CreateView):
    model = SuratResmi
    form_class = SuratResmiForm
    template_name = 'asn_app/surat_resmi_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Surat Resmi berhasil dibuat.')
        return reverse_lazy('surat_resmi_detail', kwargs={'pk': self.object.pk})


class SuratResmiUpdateView(UpdateView):
    model = SuratResmi
    form_class = SuratResmiForm
    template_name = 'asn_app/surat_resmi_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Surat Resmi berhasil diperbarui.')
        return reverse_lazy('surat_resmi_detail', kwargs={'pk': self.object.pk})


class SuratResmiDeleteView(DeleteView):
    model = SuratResmi
    template_name = 'asn_app/surat_resmi_confirm_delete.html'
    success_url = reverse_lazy('surat_resmi_list')
    context_object_name = 'surat_resmi'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Surat Resmi berhasil dihapus.')
        return super().delete(request, *args, **kwargs)


# SPTJM Views
class SPTJMListView(ListView):
    model = SPTJM
    template_name = 'asn_app/sptjm_list.html'
    context_object_name = 'sptjm_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nomor_surat__icontains=query) |
                Q(isi_surat__icontains=query)
            )
        return queryset.order_by('-created_at')


class SPTJMDetailView(DetailView):
    model = SPTJM
    template_name = 'asn_app/sptjm_detail.html'
    context_object_name = 'sptjm'


class SPTJMCreateView(CreateView):
    model = SPTJM
    form_class = SPTJMForm
    template_name = 'asn_app/sptjm_form.html'

    def get_success_url(self):
        messages.success(self.request, 'SPTJM berhasil dibuat.')
        return reverse_lazy('sptjm_detail', kwargs={'pk': self.object.pk})


class SPTJMUpdateView(UpdateView):
    model = SPTJM
    form_class = SPTJMForm
    template_name = 'asn_app/sptjm_form.html'

    def get_success_url(self):
        messages.success(self.request, 'SPTJM berhasil diperbarui.')
        return reverse_lazy('sptjm_detail', kwargs={'pk': self.object.pk})


class SPTJMDeleteView(DeleteView):
    model = SPTJM
    template_name = 'asn_app/sptjm_confirm_delete.html'
    success_url = reverse_lazy('sptjm_list')
    context_object_name = 'sptjm'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'SPTJM berhasil dihapus.')
        return super().delete(request, *args, **kwargs)


def sptjm_export_pdf(request, pk):
    import os
    import base64
    import logging # Import logging
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML, CSS

    logger = logging.getLogger(__name__) # Get logger instance

    sptjm = get_object_or_404(SPTJM, pk=pk);

    kop_surat_base64 = None
    if sptjm.kop_surat and sptjm.kop_surat.gambar:
        logger.info(f"Kop surat found: {sptjm.kop_surat.nama}, image path: {sptjm.kop_surat.gambar.path}")
        if os.path.exists(sptjm.kop_surat.gambar.path):
            try:
                with open(sptjm.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = sptjm.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
                    logger.info("Kop surat image encoded to Base64 successfully.")
            except Exception as e:
                logger.error(f"Error encoding image to base64 for SPTJM PDF: {e}")
        else:
            logger.warning(f"Kop surat image file not found at: {sptjm.kop_surat.gambar.path}")
    else:
        logger.info("No kop surat or image found for this SPTJM.")

    html_string = render_to_string('asn_app/sptjm_pdf_template.html', {
        'sptjm': sptjm,
        'kop_surat_base64': kop_surat_base64,
    })

    # Adding CSS for layout as requested
    css_string = """
        @page {
            size: A4;
            margin: 2.5cm;
        }
        body {
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.5;
        }
        .text-center {
            text-align: center;
        }
        .text-left {
            text-align: left;
        }
        .signer-section {
            padding-left: 250pt;
            text-align: left;
        }
        .signer-details {
            margin-top: 50pt;
        }
        .employee-list {
            list-style-type: decimal;
            padding-left: 40px;
        }
        .details-table {
            border-collapse: collapse;
            width: 100%;
        }
        .details-table td {
            padding: 2px 0;
            vertical-align: top;
        }
        .details-table .label {
            width: 120px;
        }
        .details-table .colon {
            width: 10px;
        }
        /* Kop Surat specific styles - already in template, but ensuring consistency */
        .kop-surat {
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }
        .kop-surat img {
            max-width: 100%;
            height: auto;
        }
    """

    try:
        # For Base64 images, often base_url=None works better as it prevents WeasyPrint
        # from trying to resolve the base64 string as a relative URL.
        html = HTML(string=html_string, base_url=None)
        result = html.write_pdf(stylesheets=[CSS(string=css_string)])
        logger.info("SPTJM PDF generated successfully.")
    except Exception as e:
        logger.error(f"Error writing SPTJM PDF: {e}", exc_info=True)
        return HttpResponse(f"Error writing SPTJM PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=sptjm_{sptjm.nomor_surat}.pdf'

    return response

# SPMT Views
class SPMTListView(ListView):
    model = SPMT
    template_name = 'asn_app/spmt_list.html'
    context_object_name = 'spmt_list'
    paginate_by = 10

class SPMTDetailView(DetailView):
    model = SPMT
    template_name = 'asn_app/spmt_detail.html'
    context_object_name = 'spmt'

class SPMTCreateView(CreateView):
    model = SPMT
    form_class = SPMTForm
    template_name = 'asn_app/spmt_form.html'
    success_url = reverse_lazy('spmt_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah SPMT'
        return context

class SPMTUpdateView(UpdateView):
    model = SPMT
    form_class = SPMTForm
    template_name = 'asn_app/spmt_form.html'
    context_object_name = 'spmt'

    def get_success_url(self):
        return reverse_lazy('spmt_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit SPMT'
        return context

class SPMTDeleteView(DeleteView):
    model = SPMT
    template_name = 'asn_app/spmt_confirm_delete.html'
    success_url = reverse_lazy('spmt_list')
    context_object_name = 'spmt'

def spmt_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML, CSS

    spmt = get_object_or_404(SPMT, pk=pk)

    kop_surat_base64 = None
    if spmt.kop_surat and spmt.kop_surat.gambar:
        if os.path.exists(spmt.kop_surat.gambar.path):
            try:
                with open(spmt.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = spmt.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64: {e}")

    html_string = render_to_string('asn_app/spmt_pdf_template.html', {
        'spmt': spmt,
        'kop_surat_base64': kop_surat_base64,
    })

    css_string = """
        body { font-family: 'Times New Roman', serif; font-size: 12pt; }
        .center { text-align: center; }
        .left { text-align: left; }
        .justify { text-align: justify; }
        .signature { padding-left: 250pt; }
        table { border-collapse: collapse; width: 100%; }
        td { vertical-align: top; }
        .label { width: 150px; }
        .colon { width: 10px; }
        .kop-surat img { max-width: 100%; height: auto; }
    """

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf(stylesheets=[CSS(string=css_string)])
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=SPMT_{spmt.nomor_surat}.pdf'

    return response

def spmt_export_excel(request):
    """Export all SPMT data to an Excel file."""
    import openpyxl
    from openpyxl.utils import get_column_letter
    from datetime import datetime

    spmts = SPMT.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'SPMT Data'

    # Write headers
    headers = [
        'Nomor Surat', 'Tempat Ditetapkan', 'Tanggal Surat', 
        'Penandatangan (Nama)', 'Penandatangan (NIP)', 'Pegawai (Nama)', 'Pegawai (NIP)',
        'Peraturan', 'Nomor Peraturan', 'Tahun Peraturan', 'Tentang',
        'Tanggal Terhitung Mulai', 'Sebagai', 'Tempat Tugas',
        'Created At', 'Updated At'
    ]
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = header

    # Write data
    for row_num, spmt in enumerate(spmts, 2):
        penandatangan_nama = spmt.penandatangan.nama if spmt.penandatangan else ''
        penandatangan_nip = spmt.penandatangan.nip if spmt.penandatangan else ''
        pegawai_nama = spmt.pegawai.nama if spmt.pegawai else ''
        pegawai_nip = spmt.pegawai.nip if spmt.pegawai else ''
        
        sheet[f'A{row_num}'] = spmt.nomor_surat
        sheet[f'B{row_num}'] = spmt.tempat_ditetapkan
        sheet[f'C{row_num}'] = spmt.tanggal_surat.strftime('%Y-%m-%d') if spmt.tanggal_surat else ''
        sheet[f'D{row_num}'] = penandatangan_nama
        sheet[f'E{row_num}'] = penandatangan_nip
        sheet[f'F{row_num}'] = pegawai_nama
        sheet[f'G{row_num}'] = pegawai_nip
        sheet[f'H{row_num}'] = spmt.peraturan
        sheet[f'I{row_num}'] = spmt.nomor_peraturan
        sheet[f'J{row_num}'] = spmt.tahun_peraturan
        sheet[f'K{row_num}'] = spmt.tentang
        sheet[f'L{row_num}'] = spmt.tanggal_terhitung.strftime('%Y-%m-%d') if spmt.tanggal_terhitung else ''
        sheet[f'M{row_num}'] = spmt.sebagai
        sheet[f'N{row_num}'] = spmt.tempat_tugas
        sheet[f'O{row_num}'] = spmt.created_at.strftime('%Y-%m-%d %H:%M:%S') if spmt.created_at else ''
        sheet[f'P{row_num}'] = spmt.updated_at.strftime('%Y-%m-%d %H:%M:%S') if spmt.updated_at else ''

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=spmt_data.xlsx'
    workbook.save(response)
    return response


def spmt_import_excel(request):
    """Import SPMT data from an Excel file."""
    if request.method == 'POST':
        import openpyxl
        from datetime import datetime

        excel_file = request.FILES['excel_file']
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

        success_count = 0
        error_count = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            try:
                (
                    nomor_surat, tempat_ditetapkan, tanggal_surat_val,
                    penandatangan_nama, penandatangan_nip, pegawai_nama, pegawai_nip,
                    peraturan, nomor_peraturan, tahun_peraturan, tentang,
                    tanggal_terhitung_val, sebagai, tempat_tugas
                ) = row

                # Handle date conversion
                tanggal_surat = None
                if isinstance(tanggal_surat_val, datetime):
                    tanggal_surat = tanggal_surat_val.date()
                elif isinstance(tanggal_surat_val, str):
                    try:
                        tanggal_surat = datetime.strptime(tanggal_surat_val, '%Y-%m-%d').date()
                    except ValueError:
                        pass

                tanggal_terhitung = None
                if isinstance(tanggal_terhitung_val, datetime):
                    tanggal_terhitung = tanggal_terhitung_val.date()
                elif isinstance(tanggal_terhitung_val, str):
                    try:
                        tanggal_terhitung = datetime.strptime(tanggal_terhitung_val, '%Y-%m-%d').date()
                    except ValueError:
                        pass

                # Find penandatangan and pegawai by name (or NIP if available)
                penandatangan = None
                if penandatangan_nama:
                    penandatangan = ASN.objects.filter(nama=penandatangan_nama).first()
                    if not penandatangan and penandatangan_nip:
                        penandatangan = ASN.objects.filter(nip=penandatangan_nip).first()

                pegawai = None
                if pegawai_nama:
                    pegawai = ASN.objects.filter(nama=pegawai_nama).first()
                    if not pegawai and pegawai_nip:
                        pegawai = ASN.objects.filter(nip=pegawai_nip).first()

                SPMT.objects.create(
                    nomor_surat=nomor_surat,
                    tempat_ditetapkan=tempat_ditetapkan,
                    tanggal_surat=tanggal_surat,
                    penandatangan=penandatangan,
                    pegawai=pegawai,
                    peraturan=peraturan,
                    nomor_peraturan=nomor_peraturan,
                    tahun_peraturan=str(tahun_peraturan) if tahun_peraturan else '',
                    tentang=tentang,
                    tanggal_terhitung=tanggal_terhitung,
                    sebagai=sebagai,
                    tempat_tugas=tempat_tugas
                )
                success_count += 1
            except Exception as e:
                logging.error(f"Error importing SPMT row: {e}")
                error_count += 1

        messages.success(request, f'Successfully imported {success_count} SPMT records. {error_count} errors.')
        return redirect('spmt_list')
    
    return render(request, 'asn_app/spmt_import_form.html')


# Surat Umum Views
class SuratUmumListView(ListView):
    model = SuratUmum
    template_name = 'asn_app/surat_umum_list.html'
    context_object_name = 'surat_umum_list'
    paginate_by = 10

class SuratUmumDetailView(DetailView):
    model = SuratUmum
    template_name = 'asn_app/surat_umum_detail.html'
    context_object_name = 'surat'

class SuratUmumCreateView(CreateView):
    model = SuratUmum
    form_class = SuratUmumForm
    template_name = 'asn_app/surat_umum_form.html'
    success_url = reverse_lazy('surat_umum_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Surat Umum'
        return context

class SuratUmumUpdateView(UpdateView):
    model = SuratUmum
    form_class = SuratUmumForm
    template_name = 'asn_app/surat_umum_form.html'
    context_object_name = 'surat'

    def get_success_url(self):
        return reverse_lazy('surat_umum_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Surat Umum'
        return context

class SuratUmumDeleteView(DeleteView):
    model = SuratUmum
    template_name = 'asn_app/surat_umum_confirm_delete.html'
    success_url = reverse_lazy('surat_umum_list')
    context_object_name = 'surat'

def surat_umum_export_pdf(request, pk):
    import os
    import base64
    os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib'
    from weasyprint import HTML, CSS

    surat = get_object_or_404(SuratUmum, pk=pk)

    kop_surat_base64 = None
    if surat.kop_surat and surat.kop_surat.gambar:
        if os.path.exists(surat.kop_surat.gambar.path):
            try:
                with open(surat.kop_surat.gambar.path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_format = surat.kop_surat.gambar.name.split('.')[-1].lower()
                    if image_format == 'jpg':
                        image_format = 'jpeg'
                    kop_surat_base64 = f"data:image/{image_format};base64,{base64.b64encode(image_data).decode('utf-8')}"
            except Exception as e:
                logging.error(f"Error encoding image to base64: {e}")

    html_string = render_to_string('asn_app/surat_umum_pdf_template.html', {
        'surat': surat,
        'kop_surat_base64': kop_surat_base64,
    })

    css_string = """
        body { font-family: 'Times New Roman', serif; font-size: 12pt; }
        .center { text-align: center; }
        .left { text-align: left; }
        .justify { text-align: justify; }
        .signature { padding-left: 250pt; }
    """

    try:
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf(stylesheets=[CSS(string=css_string)])
    except Exception as e:
        logging.error(f"Error writing PDF: {e}")
        return HttpResponse(f"Error writing PDF: {e}", status=500)

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=surat_umum_{surat.pk}.pdf'

    return response
