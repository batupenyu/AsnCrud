from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asn_app', '0081_add_dasarsurat_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suratperintahtugas',
            name='dasar_surat',
        ),
    ]
