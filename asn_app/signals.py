# asn_app/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SuratCuti, SisaCuti


@receiver(post_save, sender=SuratCuti)
def update_sisa_cuti_on_surat_cuti_save(sender, instance, created, **kwargs):
    """
    Automatically update SisaCuti when a SuratCuti is created or updated.
    This ensures sisa cuti is always in sync with approved leave letters.
    """
    # Get or create SisaCuti for this pegawai
    sisa_cuti, created = SisaCuti.objects.get_or_create(
        pegawai=instance.pegawai,
        defaults={
            'sisa_tahun_n': 12,
            'sisa_tahun_n_1': 6,
            'sisa_tahun_n_2': 6,
        }
    )
    
    # Recalculate and save
    sisa_cuti.recalculate_and_save()


@receiver(post_delete, sender=SuratCuti)
def update_sisa_cuti_on_surat_cuti_delete(sender, instance, **kwargs):
    """
    Automatically update SisaCuti when a SuratCuti is deleted.
    This restores the leave days that were used by the deleted leave letter.
    """
    # Get SisaCuti for this pegawai if it exists
    try:
        sisa_cuti = SisaCuti.objects.get(pegawai=instance.pegawai)
        # Recalculate and save
        sisa_cuti.recalculate_and_save()
    except SisaCuti.DoesNotExist:
        # No SisaCuti record, nothing to update
        pass
