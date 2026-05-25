from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

def main():
    yaml_path = 'sources/data_sources/psionics.yaml'
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 1000
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)

    target = data['items']['Biokinesis']['items']['visual-enhancement']
    
    es_desc = (
        "Al remodelar psiónicamente tus órganos visuales y reescribir las vías\n"
        "neuronales de la corteza visual, el personaje puede desplazar su visión a\n"
        "través de diferentes bandas del espectro electromagnético y mapear entornos\n"
        "estructurales mediante firmas biológicas.\n\n"
        "Para activar este poder, el personaje realiza una tirada de habilidad.\n"
        "Durante la duración del poder, el personaje obtiene **visión con poca luz**\n"
        "(equivalente al *tapetum lucidum* de un felino), lo que le permite ver en la\n"
        "oscuridad casi total como si fuera el crepúsculo. Además, el personaje recibe\n"
        "un bonificador de paso a todas las tiradas de Alerta-percepción que involucren\n"
        "la vista (normal o aumentada) según el nivel de éxito:\n\n"
        "* **Éxito Ordinario:** Otorga un bonificador de -1 paso.\n"
        "* **Éxito Bueno:** Otorga un bonificador de -2 pasos.\n"
        "* **Éxito Asombroso:** Otorga un bonificador de -3 pasos.\n\n"
        "**Efectos Secundarios Fisiológicos:** La activación de este poder provoca\n"
        "cambios biológicos visibles y a menudo perturbadores. Como mínimo, las\n"
        "pupilas del personaje se dilatan por completo y una membrana reflectante cubre\n"
        "el iris, haciendo que los ojos brillen con la luz ambiental. Los modos\n"
        "específicos (ver a continuación) pueden hacer que los ojos se vuelvan\n"
        "facetados, multilente, o que se abran fosas sensoriales en el rostro, lo que\n"
        "puede dificultar las interacciones sociales a discreción del Director de Juego.\n\n"
        "**Limitación Operativa:** Solo puede estar activo un modo de visión adicional\n"
        "en cualquier momento dado. Cambiar la biología ocular es mutuamente excluyente;\n"
        "si los ojos están modificados actualmente para la detección de fosas infrarrojas,\n"
        "no pueden utilizar simultáneamente la estructura compuesta como la de un camarón\n"
        "mantis. Cambiar entre modos activos requiere una nueva activación del poder.\n\n"
        "Navegar mientras se escanea activamente a través de barreras sólidas ralentiza\n"
        "al personaje al ritmo de \"nado suave\" (easy swim).\n\n"
        "**Beneficios de Rango:**\n\n"
        "* **Al rango 3 [Detección de Fosas Infrarrojas (Infrared Pit Detection)]**,\n"
        "  modelado a partir de las fosas loreales de las víboras, el personaje integra\n"
        "  la imagen térmica en su campo visual. Pueden abrirse visiblemente fosas\n"
        "  termosensibles especializadas cerca de los lagrimales o las sienes. El\n"
        "  personaje puede rastrear firmas de calor, detectar huellas térmicas y ver\n"
        "  objetivos vivos a través de barreras de baja densidad (como paredes delgadas\n"
        "  o follaje).\n\n"
        "* **Al rango 6 [Resolución Foveal (Foveal Resolution)]**, utilizando la\n"
        "  estructura de doble fóvea y la anatomía de fosa profunda que se encuentra en\n"
        "  rapaces como las águilas, los ojos del personaje funcionan como una mira\n"
        "  telescópica integrada. El personaje ignora el primer penalizador de +1 paso\n"
        "  por rango (Medio o Largo). Este beneficio **no** se acumula con miras o\n"
        "  binoculares. Además, la claridad de alta resolución le permite al personaje\n"
        "  detectar microexpresiones involuntarias, lo que otorga un bonificador de -1\n"
        "  paso a las tiradas de Alerta o Interacción realizadas para discernir mentiras\n"
        "  o estados emocionales, así como a las de Investigar-Buscar.\n\n"
        "* **Al rango 8 [Sensorio de Amplio Espectro (Wide-Spectrum Sensorium)]**,\n"
        "  replicando los ojos avanzados del camarón mantis, los ojos del personaje se\n"
        "  vuelven visiblemente facetados y compuestos. Pueden percibir simultáneamente\n"
        "  luz polarizada, radiación ultravioleta y emisiones electromagnéticas activas\n"
        "  (ondas de radio y frecuencias de sensores). Esto les permite \"ver\"\n"
        "  transmisores activos, como equipos de radio y sensores activos.\n\n"
        "* **Al rango 12 [Integración Cortical (Cortical Integration)]**, el personaje\n"
        "  es capaz de transformar sin problemas estos órganos visuales, haciendo que sea\n"
        "  imposible notarlos a simple vista, eliminando cualquier penalización social.\n"
        "  Además, el personaje puede cambiar entre modos como una acción."
    )

    for loc in target['localized']:
        if 'es' in loc:
            loc['es']['name'] = 'Sintonía Sensorial'
            loc['es']['description'] = LiteralScalarString(es_desc)

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print("Injected Spanish localization successfully.")

if __name__ == '__main__':
    main()
