from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asn_app', '0077_replace_pangkat_golongan_with_pangkat_golongan'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SuratUndanganSiswa',
            new_name='SuratUndangan',
        ),
        migrations.AddField(
            model_name='suratundangan',
            name='kepada_yth',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Kepada Yth.'),
        ),
        migrations.AddField(
            model_name='suratundangan',
            name='acara',
            field=models.TextField(blank=True, null=True, verbose_name='Acara'),
        ),
    ]
