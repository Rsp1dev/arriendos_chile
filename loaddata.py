import json
from django.core.management.base import BaseCommand
from myapp.models import Region, Comuna, Tipo_inmueble, Tipo_user, Inmuebles

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('regiones_data.json') as f:
            regions_data = json.load(f)
            for region_data in regions_data:
                region, created = Region.objects.get_or_create(region=region_data['fields']['region'])
                region.save()

        with open('comunas_data.json') as f:
            comunas_data = json.load(f)
            for comuna_data in comunas_data:
                comuna, created = Comuna.objects.get_or_create(comuna=comuna_data['fields']['comuna'])
                region = Region.objects.get(region=comuna_data['fields']['region'])
                comuna.region = region
                comuna.save()

        with open('tipo_inmueble_data.json') as f:
            tipo_inmueble_data = json.load(f)
            for tipo_inmueble_data in tipo_inmueble_data:
                tipo_inmueble, created = Tipo_inmueble.objects.get_or_create(tipo_inmueble=tipo_inmueble_data['fields']['tipo_inmueble'])
                tipo_inmueble.save()

        with open('tipo_usuario_data.json') as f:
            tipo_usuario_data = json.load(f)
            for tipo_usuario_data in tipo_usuario_data:
                tipo_usuario, created = Tipo_user.objects.get_or_create(tipo_user=tipo_usuario_data['fields']['tipo_user'])
                tipo_usuario.save()

        with open('inmuebles_data.json') as f:
            inmuebles_data = json.load(f)
            for inmueble_data in inmuebles_data:
                tipo_inmueble = Tipo_inmueble.objects.get(pk=inmueble_data['fields']['id_tipo_inmueble_id'])
                comuna = Comuna.objects.get(pk=inmueble_data['fields']['id_comuna_id'])
                region = Region.objects.get(pk=inmueble_data['fields']['id_region_id'])
                tipo_usuario = Tipo_user.objects.get(pk=inmueble_data['fields']['id_user_id'])
                inmueble = Inmuebles(
                    nombre_inmueble=inmueble_data['fields']['nombre_inmueble'],
                    descripcion=inmueble_data['fields']['descripcion'],
                    m2_construido=inmueble_data['fields']['m2_construido'],
                    numero_banos=inmueble_data['fields']['numero_banos'],
                    direccion=inmueble_data['fields']['direccion'],
                    m2_terreno=inmueble_data['fields']['m2_terreno'],
                    numero_est=inmueble_data['fields']['numero_est'],
                    id_tipo_inmueble=tipo_inmueble,
                    id_comuna=comuna,
                    id_region=region,
                    id_user=tipo_usuario
                )
                inmueble.save()