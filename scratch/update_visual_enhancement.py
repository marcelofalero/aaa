import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

def main():
    yaml_path = 'sources/data_sources/psionics.yaml'
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 80
    yaml.indent(mapping=2, sequence=4, offset=2)

    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f)

    biokinesis_items = data['items']['Biokinesis']['items']

    # 1. Delete intangibility if present
    if 'intangibility' in biokinesis_items:
        del biokinesis_items['intangibility']
        print("Deleted 'intangibility' from YAML.")

    # 2. Add visual-enhancement
    en_desc = (
        "By psionically reshaping your visual organs and rewriting the neural\n"
        "pathways of the visual cortex, the character can shift their vision across\n"
        "different bands of the electromagnetic spectrum and map structural\n"
        "environments through biological signatures.\n\n"
        "To activate this power, the character makes a skill check. For the duration\n"
        "of the power, the character gains **low-light vision** (equivalent to a\n"
        "feline's *tapetum lucidum*), allowing them to see in near-total darkness as\n"
        "if it were twilight. Additionally, the character receives a step bonus to all\n"
        "Awareness-perception checks involving sight (normal or augmented) based on\n"
        "the level of success:\n\n"
        "* **Ordinary Success:** Grants a -1 step bonus.\n"
        "* **Good Success:** Grants a -2 step bonus.\n"
        "* **Amazing Success:** Grants a -3 step bonus.\n\n"
        "**Physiological Side Effects:** The activation of this power causes visible,\n"
        "often disturbing biological shifts. At a minimum, the character’s pupils dilate\n"
        "fully and a reflective membrane covers the iris, making the eyes glow in\n"
        "ambient light. Specific modes (see below) may cause the eyes to become\n"
        "faceted, multi-lensed, or cause sensory pits to open on the face, which can\n"
        "impair social interactions at the Gamemaster's discretion.\n\n"
        "**Operational Limitation:** Only one additional sight mode can be active at\n"
        "any given time. Shifting ocular biology is mutually exclusive; if the eyes\n"
        "are currently modified for infrared pit detection, they cannot simultaneously\n"
        "utilize the compound structure like those of mantis shrimp. Switching between\n"
        "active modes requires a new activation of the power.\n\n"
        "Navigating while actively scanning through solid barriers slows the character\n"
        "to the \"easy swim\" rate.\n\n"
        "**Rank Benefits:**\n\n"
        "* **At rank 3 [Infrared Pit Detection]**, modeled after the loreal pits of\n"
        "  vipers, the character integrates thermal imaging into their visual field.\n"
        "  Specialized heat-sensing pits may visibly open near the tear ducts or temples.\n"
        "  The character can trace heat signatures, detect thermal footprints, and see\n"
        "  living targets through low-density barriers (such as thin walls or foliage).\n\n"
        "* **At rank 6 [Foveal Resolution]**, utilizing the dual-fovea structure and\n"
        "  deep-pit anatomy found in raptors like eagles, the character’s eyes function\n"
        "  as an integrated telescopic scope. The character ignores the first +1 step\n"
        "  penalty for range (Medium or Long). This benefit does **not** stack with scopes\n"
        "  or binoculars. Additionally, the high-resolution clarity allows the character\n"
        "  to detect involuntary microexpressions, granting a -1 step bonus to Awareness\n"
        "  or Interaction checks made to discern lies or emotional states. And\n"
        "  Investigation-Search checks.\n\n"
        "* **At rank 8 [Wide-Spectrum Sensorium]**, replicating the advanced eyes of the\n"
        "  mantis shrimp, the character’s eyes become visibly faceted and compound.\n"
        "  They can simultaneously perceive polarized light, ultraviolet radiation, and\n"
        "  active electromagnetic emissions (radio waves and sensor frequencies). This\n"
        "  allows them to \"see\" active transmittors, like radio equipment, active sensors.\n\n"
        "* **At rank 12 [Cortical Integration]**, the character's is able to seamlessly\n"
        "  morph this visual organs making impossible to notice them at plain sight,\n"
        "  eliminating any social penalty. Additionally, the character can switch\n"
        "  between modes as an action."
    )

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

    visual_enhancement_node = {
        'attribute': 'CON',
        'cost': 3,
        'url': '/psionics/biokinesis/#visual-enhancement',
        'trained_only': False,
        'rank_benefits': [
            {'rank': 3, 'title': 'Infrared Pit Detection'},
            {'rank': 6, 'title': 'Foveal Resolution'},
            {'rank': 8, 'title': 'Wide-Spectrum Sensorium'},
            {'rank': 12, 'title': 'Cortical Integration'}
        ],
        'extended_duration': True,
        'localized': [
            {
                'en': {
                    'name': 'Sensory Attunement',
                    'description': LiteralScalarString(en_desc)
                }
            },
            {
                'es': {
                    'name': 'Sintonía Sensorial',
                    'description': LiteralScalarString(es_desc)
                }
            }
        ]
    }

    # Insert visual-enhancement in place of intangibility or at the end
    biokinesis_items['visual-enhancement'] = visual_enhancement_node
    print("Added 'visual-enhancement' to YAML.")

    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    print("Successfully saved YAML.")

if __name__ == '__main__':
    main()
