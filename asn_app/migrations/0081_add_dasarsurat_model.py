from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asn_app', '0080_suratundangan_pembuka_surat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DasarSurat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urutan', models.PositiveIntegerField(default=0, verbose_name='Urutan')),
                ('isi', models.TextField(verbose_name='Dasar Surat')),
                ('spt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dasar_surat_items', to='asn_app.suratperintahtugas', verbose_name='SPT')),
            ],
            options={
                'verbose_name': 'Dasar Surat',
                'verbose_name_plural': 'Dasar Surat',
                'ordering': ['urutan'],
            },
        ),
    ]
