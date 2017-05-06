from main import ESCENARIO


TIME_TO_PRIVATE_PHARMACY = 11

demanda_caso_base = read file escenario

demanda = read file escenario

for year
    for zones
        total = demanda[year][zones]
        total_caso_base = demanda_caso_base[year][zones]
        nuevos = max(total - total_caso_base, 0)
        iban_farmacia_privada = %_farmacia_priv * nuevos
        no_compraba = (1 - %_farmacia_priv) * nuevos
        ya_van_farmacia_comunal = total_caso_base
        b_zona += beneficio_ya_van_farmacia_comunal(ya_van_farmacia_comunal)
        b_zona += beneficio_no_compraba(no_compraba)
        b_zona += beneficio_compraba_privada(iban_farmacia_privada)




beneficio_ya_van_farmacia_comunal(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    tiempo_antes = tiempo_a(municipalidad)
    tiempo_ganado =  tiempo_antes - tiempo
    return tiempo_ganado * valor_del_tiempo * cantidad

beneficio_no_compraba(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    costo_en_tiempo = tiempo * valor_del_tiempo
    costo_en_dinero = gasto_promedio('Comunitaria')
    return cantidad * (ganancia_en_vida - costo_en_tiempo - costo_en_dinero)

beneficio_compraba_privada(cantidad):
    tiempo = max_tiempo
    for farmacia in escenario.farmacias:
        tiempo = min(tiempo_a(farmacia), tiempo)
    delta_tiempo = tiempo_a('Privada') - tiempo
    ahorro = gasto_promedio('Privada') - gasto_promedio('Comunitaria')
    return (ahorro + delta_tiempo * valor_del_tiempo) * cantidad
