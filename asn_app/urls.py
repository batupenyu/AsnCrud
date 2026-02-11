from django.urls import path
from . import views

urlpatterns = [
    path('', views.asn_list, name='asn_list'),
    path('<int:pk>/', views.asn_detail, name='asn_detail'),
    path('create/', views.asn_create, name='asn_create'),
    path('<int:pk>/update/', views.asn_update, name='asn_update'),
    path('<int:pk>/delete/', views.asn_delete, name='asn_delete'),
    # Tambahkan routes untuk cetak
    path('<int:pk>/pdf/', views.asn_export_pdf, name='asn_export_pdf'),
    path('<int:pk>/print/', views.asn_print_view, name='asn_print_view'),
    # SPT routes
    path('spt/', views.spt_list, name='spt_list'),
    path('spt/<int:pk>/', views.spt_detail, name='spt_detail'),
    path('spt/create/', views.spt_create, name='spt_create'),
    path('spt/<int:pk>/update/', views.spt_update, name='spt_update'),
    path('spt/<int:pk>/delete/', views.spt_delete, name='spt_delete'),
    path('spt/<int:pk>/pdf/', views.spt_export_pdf, name='spt_export_pdf'),
    path('spt/<int:pk>/pdf/large/', views.spt_export_pdf_large, name='spt_export_pdf_large'),
    path('spt/<int:pk>/print/', views.spt_print_view, name='spt_print_view'),
    path('spt/<int:pk>/laporan/', views.spt_laporan, name='spt_laporan'),
    path('spt/<int:spt_pk>/upload_foto/', views.upload_foto_kegiatan, name='upload_foto_kegiatan'),
    path('foto_kegiatan/<int:foto_pk>/delete/', views.delete_foto_kegiatan, name='delete_foto_kegiatan'),
    path('spt/<int:spt_pk>/cetak_foto_pdf/', views.cetak_foto_kegiatan_pdf, name='cetak_foto_kegiatan_pdf'),

    # Kop Surat routes
    path('kop_surat/', views.kop_surat_list, name='kop_surat_list'),
    path('kop_surat/create/', views.kop_surat_create, name='kop_surat_create'),
    path('kop_surat/<int:pk>/', views.kop_surat_detail, name='kop_surat_detail'),
    path('kop_surat/<int:pk>/update/', views.kop_surat_update, name='kop_surat_update'),
    path('kop_surat/<int:pk>/delete/', views.kop_surat_delete, name='kop_surat_delete'),
    path('export/excel/', views.export_asn_excel, name='export_asn_excel'),
    path('import/excel/', views.import_asn_excel, name='import_asn_excel'),

    # Surat Santunan Korpri routes
    path('surat_santunan_korpri/', views.surat_santunan_korpri_list, name='surat_santunan_korpri_list'),
    path('surat_santunan_korpri/create/', views.surat_santunan_korpri_create, name='surat_santunan_korpri_create'),
    path('surat_santunan_korpri/<int:pk>/', views.surat_santunan_korpri_detail, name='surat_santunan_korpri_detail'),
    path('surat_santunan_korpri/<int:pk>/update/', views.surat_santunan_korpri_update, name='surat_santunan_korpri_update'),
    path('surat_santunan_korpri/<int:pk>/delete/', views.surat_santunan_korpri_delete, name='surat_santunan_korpri_delete'),
    path('surat_santunan_korpri/<int:pk>/pdf/', views.surat_santunan_korpri_export_pdf, name='surat_santunan_korpri_export_pdf'),

    # Nota Dinas routes
    path('nota_dinas/', views.nota_dinas_list, name='nota_dinas_list'),
    path('nota_dinas/create/', views.nota_dinas_create, name='nota_dinas_create'),
    path('nota_dinas/<int:pk>/', views.nota_dinas_detail, name='nota_dinas_detail'),
    path('nota_dinas/<int:pk>/update/', views.nota_dinas_update, name='nota_dinas_update'),
    path('nota_dinas/<int:pk>/delete/', views.nota_dinas_delete, name='nota_dinas_delete'),
    path('nota_dinas/<int:pk>/pdf/', views.nota_dinas_export_pdf, name='nota_dinas_export_pdf'),

    # Hari Libur routes
    path('hari_libur/', views.HariLiburListView.as_view(), name='hari_libur_list'),
    path('hari_libur/create/', views.HariLiburCreateView.as_view(), name='hari_libur_create'),
    path('hari_libur/<int:pk>/', views.HariLiburDetailView.as_view(), name='hari_libur_detail'),
    path('hari_libur/<int:pk>/update/', views.HariLiburUpdateView.as_view(), name='hari_libur_update'),
    path('hari_libur/<int:pk>/delete/', views.HariLiburDeleteView.as_view(), name='hari_libur_delete'),

    # Surat Cuti routes
    path('surat_cuti/', views.SuratCutiListView.as_view(), name='surat_cuti_list'),
    path('surat_cuti/create/', views.SuratCutiCreateView.as_view(), name='surat_cuti_create'),
    path('surat_cuti/<int:pk>/', views.SuratCutiDetailView.as_view(), name='surat_cuti_detail'),
    path('surat_cuti/<int:pk>/update/', views.SuratCutiUpdateView.as_view(), name='surat_cuti_update'),
    path('surat_cuti/<int:pk>/delete/', views.SuratCutiDeleteView.as_view(), name='surat_cuti_delete'),
    path('surat_cuti/<int:pk>/pdf/', views.surat_cuti_export_pdf, name='surat_cuti_export_pdf'),

    # Sisa Cuti routes
    path('sisa_cuti/', views.SisaCutiListView.as_view(), name='sisa_cuti_list'),
    path('sisa_cuti/create/', views.SisaCutiCreateView.as_view(), name='sisa_cuti_create'),
    path('sisa_cuti/<int:pk>/', views.SisaCutiDetailView.as_view(), name='sisa_cuti_detail'),
    path('sisa_cuti/<int:pk>/update/', views.SisaCutiUpdateView.as_view(), name='sisa_cuti_update'),
    path('sisa_cuti/<int:pk>/delete/', views.SisaCutiDeleteView.as_view(), name='sisa_cuti_delete'),

    # Laporan Cuti routes
    path('laporan_cuti/<int:pk>/pdf/', views.laporan_cuti_pdf, name='laporan_cuti_pdf'),

    # Siswa routes
    path('siswa/', views.siswa_list, name='siswa_list'),
    path('siswa/create/', views.siswa_create, name='siswa_create'),
    path('siswa/<int:pk>/', views.siswa_detail, name='siswa_detail'),
    path('siswa/<int:pk>/update/', views.siswa_update, name='siswa_update'),
    path('siswa/<int:pk>/delete/', views.siswa_delete, name='siswa_delete'),
    path('siswa/export/excel/', views.export_siswa_excel, name='export_siswa_excel'),
    path('siswa/import/excel/', views.import_siswa_excel, name='import_siswa_excel'),
    path('siswa/delete_all/', views.siswa_delete_all, name='siswa_delete_all'),

    # Surat Keterangan routes
    path('surat_keterangan/', views.surat_keterangan_list, name='surat_keterangan_list'),
    path('surat_keterangan/create/', views.surat_keterangan_create, name='surat_keterangan_create'),
    path('surat_keterangan/<int:pk>/', views.surat_keterangan_detail, name='surat_keterangan_detail'),
    path('surat_keterangan/<int:pk>/update/', views.surat_keterangan_update, name='surat_keterangan_update'),
    path('surat_keterangan/<int:pk>/delete/', views.surat_keterangan_delete, name='surat_keterangan_delete'),
    path('surat_keterangan/<int:pk>/pdf/', views.surat_keterangan_export_pdf, name='surat_keterangan_export_pdf'),

    # Surat Resmi routes
    path('surat_resmi/', views.SuratResmiListView.as_view(), name='surat_resmi_list'),
    path('surat_resmi/create/', views.SuratResmiCreateView.as_view(), name='surat_resmi_create'),
    path('surat_resmi/<int:pk>/', views.SuratResmiDetailView.as_view(), name='surat_resmi_detail'),
    path('surat_resmi/<int:pk>/update/', views.SuratResmiUpdateView.as_view(), name='surat_resmi_update'),
    path('surat_resmi/<int:pk>/delete/', views.SuratResmiDeleteView.as_view(), name='surat_resmi_delete'),
    path('surat_resmi/<int:pk>/pdf/', views.surat_resmi_export_pdf, name='surat_resmi_export_pdf'),

    # SPTJM routes
    path('sptjm/', views.SPTJMListView.as_view(), name='sptjm_list'),
    path('sptjm/create/', views.SPTJMCreateView.as_view(), name='sptjm_create'),
    path('sptjm/<int:pk>/', views.SPTJMDetailView.as_view(), name='sptjm_detail'),
    path('sptjm/<int:pk>/update/', views.SPTJMUpdateView.as_view(), name='sptjm_update'),
    path('sptjm/<int:pk>/delete/', views.SPTJMDeleteView.as_view(), name='sptjm_delete'),
    path('sptjm/<int:pk>/pdf/', views.sptjm_export_pdf, name='sptjm_export_pdf'),

    # SPMT routes
    path('spmt/', views.SPMTListView.as_view(), name='spmt_list'),
    path('spmt/create/', views.SPMTCreateView.as_view(), name='spmt_create'),
    path('spmt/<int:pk>/', views.SPMTDetailView.as_view(), name='spmt_detail'),
    path('spmt/<int:pk>/update/', views.SPMTUpdateView.as_view(), name='spmt_update'),
    path('spmt/<int:pk>/delete/', views.SPMTDeleteView.as_view(), name='spmt_delete'),
    path('spmt/<int:pk>/pdf/', views.spmt_export_pdf, name='spmt_export_pdf'),

    # Surat Umum routes
    path('surat_umum/', views.SuratUmumListView.as_view(), name='surat_umum_list'),
    path('surat_umum/create/', views.SuratUmumCreateView.as_view(), name='surat_umum_create'),
    path('surat_umum/<int:pk>/', views.SuratUmumDetailView.as_view(), name='surat_umum_detail'),
    path('surat_umum/<int:pk>/update/', views.SuratUmumUpdateView.as_view(), name='surat_umum_update'),
    path('surat_umum/<int:pk>/delete/', views.SuratUmumDeleteView.as_view(), name='surat_umum_delete'),
    path('surat_umum/<int:pk>/pdf/', views.surat_umum_export_pdf, name='surat_umum_export_pdf'),
]