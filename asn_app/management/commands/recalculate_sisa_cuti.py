# asn_app/management/commands/recalculate_sisa_cuti.py
from django.core.management.base import BaseCommand
from asn_app.models import ASN, SisaCuti, SuratCuti


class Command(BaseCommand):
    help = 'Recalculate all SisaCuti records with dynamic continuous logic'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting SisaCuti recalculation with dynamic continuous logic...')
        self.stdout.write('')
        self.stdout.write('Rules:')
        self.stdout.write('  - Year N (current): 12 days - used')
        self.stdout.write('  - Year N-1: 6 days - used, BUT if N usage > 6, then N-1 = 0')
        self.stdout.write('  - Year N-2: 6 days - used, BUT if N-1 usage > 6, then N-2 = 0')
        self.stdout.write('')
        
        # Get all ASN that have or should have SisaCuti
        all_pegawai = ASN.objects.all()
        
        count_updated = 0
        count_created = 0
        count_n1_zero = 0
        count_n2_zero = 0
        
        for pegawai in all_pegawai:
            # Get or create SisaCuti
            sisa_cuti, created = SisaCuti.objects.get_or_create(
                pegawai=pegawai,
                defaults={
                    'sisa_tahun_n': 12,
                    'sisa_tahun_n_1': 6,
                    'sisa_tahun_n_2': 6,
                }
            )
            
            # Recalculate based on SuratCuti records
            sisa_cuti.recalculate_and_save()
            
            # Track statistics
            if sisa_cuti.sisa_tahun_n_1 == 0:
                count_n1_zero += 1
            if sisa_cuti.sisa_tahun_n_2 == 0:
                count_n2_zero += 1
            
            if created:
                count_created += 1
            else:
                count_updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully recalculated SisaCuti for {count_updated} existing records '
                f'and created {count_created} new records.'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f'{count_n1_zero} records have N-1 = 0 (due to N usage > 6) | '
                f'{count_n2_zero} records have N-2 = 0 (due to N-1 usage > 6)'
            )
        )
