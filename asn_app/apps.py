# asn_app/apps.py
from django.apps import AppConfig

class AsnAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'asn_app'
    verbose_name = 'Manajemen ASN'