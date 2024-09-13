from m7_python.models import Inmuebles

def get_all_inmuebles():
    Inm = Inmuebles.objects.all()
    return Inm

def insertar_inmueble(data):
    id_user = data[0]
    id_tipo_inmueble = data[1]
    id_comuna = data[2]
    id_region = data[3]
    nombre_inmueble = data[4]
    descripcion = data[5]
    m2_construido = data[6]
    num_banos = data[7]
    num_hab = data[8]
    direccion = data[9]

    inm = Inmuebles(
        id_user = id_user,
        id_tipo_inmueble = id_tipo_inmueble,
        id_comuna = id_comuna,
        id_region = id_region,
        nombre_inmueble = nombre_inmueble,
        descripcion = descripcion,
        m2_construido = m2_construido,
        num_banos = num_banos,
        num_hab = num_hab,
        direccion = direccion)
    inm.save()

def actualizar_descrip_inmueble(id_inmueble,new_descrip):
    Inmuebles.objects.filter(pk=id_inmueble).update(descripcion=new_descrip)

def eliminar_inmueble(id_inmueble):
    Inmuebles.objects.get(id=id_inmueble).delete()