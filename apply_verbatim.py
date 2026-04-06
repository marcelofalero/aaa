import json

def apply_verbatim_descriptions():
    en_file = 'site/data/armor.json'
    es_file = 'site/data/armor.es.json'

    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    with open(es_file, 'r', encoding='utf-8') as f:
        es_data = json.load(f)

    # Verbatim Map
    verbatim_descriptions = {
        "Aegis 650 Cerametal Shield": "The Aegis 650 is the kind of shield an ancient warrior would have treasured. Light and unbelievably strong, it can stop a 9mm round cold at point-blank range. The Aegis includes a vision slit of bulletproof polymere and a firing port, allowing the user to crouch behind it for portable hard cover. When used in this fashion, the Aegis provides a +1 increase to the user's resistance modifier against ranged attacks as well as providing its normal benefit of enhancing armor rolls. Naturally, the shield doesn't contribute to armor rolls against attacks from behind.",
        "SAI Powered Shield": "The conventional shield's drawbacks are bulk and the problem of tying up the user's second hand. The SAI solves that; it's actually a free-floating unit powered by an induction motor. Its smart sensors detect incoming attacks and direct the shield to interpose itself automatically. The user of the SAI shield may even apply the shield's benefit against flank or rear attacks. However, there's a catch—the SAI automatically moves to parry the first attack that is directed at the user in any given phase of combat, hit or miss, and provides no benefit to subsequent attacks in the same phase that strike from a different quarter.",
        "Rampart Deflection Inducer": "A cheaper version than the standard model, the Rampart sacrifices defensive power for light construction. Creates a cylindrical field of gravitational energy surrounding the wearer at a range of 1 meter. Objects passing through this field in either direction are deflected from their course, inflicting a +2 step penalty to projectile or melee weapon attacks, and a +1 step penalty to energy attacks. The inducer's cells can maintain the field for 5 rounds; turning the field on or off requires an action.",
        "Anvil 44 Magnetic Screen": "The electromagnetic screen (or magnetic screen, for short) resembles the deflection inducer in operation, but protects the wearer with magnetic force. It provides excellent protection against metallic melee weapons, metallic rounds (charge, sabot, and flechette ammo), and weapons that fire electrical discharges, such as the arc gun. It provides no protection against other types of weapons or attacks. Since the screen is set to repel incoming attacks, it has no deleterious effect on the wearer's own attack rolls. Its energy cells last for 6 rounds of continuous use.",
        "Alpha 50 Particle Screen": "The Alpha 50 generates a shell of alpha particles—helium nuclei stripped of their electrons. When a character wearing a particle screen is struck by a weapon, he may add the screen's protective value to the protection of his armor. For example, a hero wearing Paladin Body Armor and a particle screen actually stops 2d4+2 (for the armor), plus an additional d8-2, versus energy attacks.\nThe screen \"blinks out\" when a hero fires his own weapon, so it automatically has no effect in any phase in which a hero attacks. It has a maximum endurance of 10 rounds before it shuts down.",
        "SCM-16 Capacitor Screen": "The Scam-16, as it's commonly known, creates a field of ionized particles from the air molecules in the user's vicinity. Against low impact and high impact attacks, the capacitor screen is considered to have a toughness of Good; against energy attacks, its toughness is Amazing. In addition, the screen automatically reduces the damage of an attack by the amount listed, so an energy attack that inflicts 6 wounds is reduced by 4 to 2 wounds before secondary damage or the user's armor is taken into account.\nThe screen can absorb d6+1 attacks before its capacitors are full and it's forced to shut down for at least 2 hours.",
        "ABS-11 Dragoon Recon Armor": "Also known as a recon or scout body tank, the Dragoon is a lighter and more mobile powered suit. It has all the features described above, with one key addition—a gravity induction drive, providing flight capability at a maximum speed of 180 kph (or meters per phase). Since this is powered flight, the wearer suffers no fatigue damage for flying. On the ground, the Dragoon can move at 30 kph (or 30 meters per phase) in broken terrain, or 60 kph on open ground. Typically, one squad of troops in an armor platoon is equipped with recon armor.",
        "AAS-23 Titan Assault Armor": "Fully space-to-ground capable, the Titan is also known as zero-g armor. It can be fitted with an ablative reentry shroud (cost $500) for orbital insertion, descending from an altitude of 200 km to the ground in about five minutes. It has limited flight capability and is rated up to an airspeed of 100 kph or ground speeds of 20 to 40 kph. The Titan features an air/space radar similar to the radar gauntlet (see page 37), and its weapon hardpoint can be used to mount any of the following: a grenade launcher with a 12-round magazine, a bantam launcher, any direct-fire heavy weapon, or any powered melee weapon.",
        "Ptokh K'se (T'sa armor)": "The ptokh k'se (pronounced TAHKK-see, more or less) is the t'sa version of a bulletproof vest. It consists of a dense weave of extruded alloy wire, woven into a heavy cloth and sandwiched between tough artificial weaves. When worn, the ptokh k'se improves the t'sa's natural armor value from d4+1 (LI), d4 (HI), d4-1 (En) to the values given in the statistics. (This is an exception to the rule about layering armor.) While its mass is noticeable, the vest is thin and flexible enough to be worn under almost any other garment. Few t'sa like to wear heavy battle armor, but the ptokh k'se is a good compromise between ease of movement and protection.",
        "Khe! Burund (Weren mail)": "Developed within the last hundred years to resist musket balls, the khe! burund is a hauberk of light chain mail with stiff leather strips woven between the links, worn over a leather arming coat. The coat covers the wearer's arms to the elbow, his legs to the knee, and includes a hood. Favored by many weren mercenaries and expatriates because it's an element of weren technology that stands up to human weapons, the khe! burund (the exclamation mark signifies that the first word is vocalized as a cough) has become an emblem of weren tradition in the face of overwhelming change.",
        "Bellweyn Sil (Fraal)": "The bellweyn sil ('battle-coat' in the fraal tongue) is a protective garment that embodies some of the elegance and aesthetics of the species. It consists of a light arming suit of engineered molecular weave. Over this, layers of stiffened molecular weave are fashioned into soft, overlapping bands that vaguely resemble ancient human armors. Richly adorned with embroidery and metallic finishes, the bellweyn sil is a spectacular garment suitable for many diplomatic or formal affairs. Fraal leaders, guards, and emissaries often wear this garment when dealing with less developed species.",
        "Had'Niltas (Mechalus)": "An outstanding example of alien technology, the had'niltas is a superior suit of powered armor. Unlike the bulky plated suits developed by human armorers, the had'niltas is light and flexible. It consists of a full-body jumpsuit or wrap of advanced fabric. Inside the suit's fabric is a layer of liquid metal containing millions of nanocircuits. These instantly respond to any attack, hardening the suit at the point of impact and dissipating heat or energy. The had'niltas is nearly impervious to slashing attacks or energy weapons, but high-velocity projectiles can sometimes penetrate before the suit reacts.",
        "ACN 4 Cerametal Armor": "The ACN-4 has been adopted as the standard armor for the Concord Marines' famous Recon/Marauder teams. It is designed as a low-maintenance, low-mass nonpowered armor that can be packed into a compact bundle.",
        "Bushmaster Cerametal Mail": "The Bushmaster is a tight-fitting garment of extremely fine cerametal chain mail. It is especially resistant to cutting, slashing, and tearing-type attacks, and it is tougher than any lighter armor.",
        "Tiger Mod 6 Powered Armor": "The Tiger's systems include a targeting system, image enhancement system, comm gear, signal laser, and two trauma packs. A microcomputer of Marginal quality manages its systems; the armor operation utility program requires 1 slot of active memory.",
        "ABM-5 Paladin Battle Armor": "The Paladin is the standard powered armor suit of the Concord Marines and Planetary Defense Force. Its batteries can power 12 hours of intense action or 72 hours of intermittent activity."
    }

    # Spanish Verbatim Map
    verbatim_descriptions_es = {
        "Aegis 650 Cerametal Shield": "El Aegis 650 es el tipo de escudo que un guerrero antiguo habría atesorado. Con una ligereza y resistencia increíbles, puede detener una bala de 9 mm en frío a quemarropa. El Aegis incluye una mira de polímero a prueba de balas y un puerto de disparo, lo que permite al usuario agacharse detrás de él para obtener una cobertura portátil. Cuando se usa de esta manera, el Aegis proporciona un aumento de +1 al modificador de resistencia del usuario contra ataques a distancia, además de brindar su beneficio normal de mejorar las tiradas de armadura. Naturalmente, el escudo no contribuye a las tiradas de armadura contra ataques por la espalda.",
        "SAI Powered Shield": "Los inconvenientes del escudo convencional son el volumen y el problema de atar la mano secundaria del usuario. El SAI soluciona eso; en realidad es una unidad de flotación libre impulsada por un motor de inducción. Sus sensores inteligentes detectan ataques entrantes y dirigen el escudo para interponerse automáticamente. El usuario del escudo SAI puede incluso aplicar el beneficio del escudo contra ataques de flanco o retaguardia. Sin embargo, hay un inconveniente: el SAI se mueve automáticamente para detener el primer ataque que se dirija al usuario en cualquier fase dada del combate, con éxito o sin él, y no proporciona beneficios a ataques posteriores en la misma fase que golpeen desde un cuadrante diferente.",
        "Rampart Deflection Inducer": "Una versión más económica que el modelo estándar, el Rampart sacrifica potencia defensiva por una construcción ligera. Crea un campo cilíndrico de energía gravitatoria que rodea al usuario a un rango de 1 metro. Los objetos que pasan a través de este campo en cualquier dirección se desvían de su curso, infligiendo una penalización de +2 pasos a los ataques de proyectiles o armas cuerpo a cuerpo, y una penalización de +1 paso a los ataques de energía. Las celdas del inductor pueden mantener el campo durante 5 asaltos; encender o apagar el campo requiere una acción.",
        "Anvil 44 Magnetic Screen": "La pantalla electromagnética (o pantalla magnética, para abreviar) se asemeja al inductor de deflexión en su funcionamiento, pero protege al usuario con fuerza magnética. Proporciona una excelente protección contra armas cuerpo a cuerpo metálicas, proyectiles metálicos (munición de carga, con núcleo y flechette) y armas que disparan descargas eléctricas, como la pistola de arco. No proporciona protección contra otros tipos de armas o ataques. Dado que la pantalla está configurada para repeler ataques entrantes, no tiene efecto deletéreo en las tiradas de ataque del propio usuario. Sus celdas de energía duran 6 asaltos de uso continuo.",
        "Alpha 50 Particle Screen": "El Alpha 50 genera una cáscara de partículas alfa: núcleos de helio despojados de sus electrones. Cuando un personaje que lleva una pantalla de partículas es golpeado por un arma, puede añadir el valor protector de la pantalla a la protección de su armadura. Por ejemplo, un héroe que lleva una armadura corporal Paladin y una pantalla de partículas en realidad detiene 2d4+2 (por la armadura), más un d8-2 adicional, contra ataques de energía.\nLa pantalla \"parpadea\" cuando un héroe dispara su propia arma, por lo que automáticamente no tiene efecto en ninguna fase en la que un héroe ataque. Tiene una resistencia máxima de 10 asaltos antes de apagarse.",
        "SCM-16 Capacitor Screen": "La Scam-16, como se la conoce comúnmente, crea un campo de partículas ionizadas a partir de las moléculas de aire en las cercanías del usuario. Contra ataques de bajo y alto impacto, se considera que la pantalla de capacitores tiene una dureza Buena; contra ataques de energía, su dureza es Asombrosa. Además, la pantalla reduce automáticamente el daño de un ataque por la cantidad indicada, de modo que un ataque de energía que inflige 6 heridas se reduce de 4 a 2 heridas antes de que se tenga en cuenta el daño secundario o la armadura del usuario.\nLa pantalla puede absorber d6+1 ataques antes de que sus capacitores se llenen y se vea obligada a apagarse durante al menos 2 horas.",
        "ABS-11 Dragoon Recon Armor": "También conocido como tanque de cuerpo de reconocimiento o exploración, el Dragoon es un traje motorizado más ligero y móvil. Tiene todas las funciones integradas de los tanques de cuerpo estándar, con una adición clave: un impulso de inducción por gravedad, que proporciona capacidad de vuelo a una velocidad máxima de 180 km/h (o metros por fase). Dado que se trata de un vuelo motorizado, el usuario no sufre daños por fatiga al volar. En tierra, el Dragoon puede moverse a 30 km/h (o 30 metros por fase) en terreno accidentado, o a 60 km/h en terreno abierto. Normalmente, un escuadrón de tropas en un pelotón de armaduras está equipado con armadura de reconocimiento.",
        "AAS-23 Titan Assault Armor": "Totalmente capaz de despliegue orbital, el Titán también se conoce como armadura de gravedad cero. Puede equiparse con una cubierta ablativa de reentrada (coste 500 $) para inserción orbital, descendiendo desde una altitud de 200 km hasta el suelo en unos cinco minutos. Tiene una capacidad de vuelo limitada y está clasificado para una velocidad aérea de hasta 100 km/h o velocidades terrestres de 20 a 40 km/h. El Titán cuenta con un radar aire/espacio similar al guantelete de radar (ver página 37), y su punto de anclaje de armas puede usarse para montar cualquiera de los siguientes: un lanzagranadas con un cargador de 12 rondas, un lanzador bantam, cualquier arma pesada de fuego directo o cualquier arma cuerpo a cuerpo motorizada.",
        "Ptokh K'se (T'sa armor)": "El ptokh k'se (pronunciado TAHKK-si, más o menos) es la versión t'sa de un chaleco antibalas. Consiste en un tejido denso de hilo de aleación extruido, tejido en una tela gruesa y comprimido entre capas artificiales resistentes. Cuando se usa, el ptokh k'se mejora el valor natural de la armadura del t'sa de d4+1 (LI), d4 (HI), d4-1 (En) a los valores dados en las estadísticas. (Esta es una excepción a la regla sobre la superposición de armaduras). Si bien su masa es notable, el chaleco es lo suficientemente delgado y flexible como para usarlo debajo de casi cualquier otra prenda. A pocos t'sa les gusta usar armaduras de batalla pesadas, pero el ptokh k'se es un buen compromiso entre la facilidad de movimiento y la protección.",
        "Khe! Burund (Weren mail)": "Desarrollada en los últimos cien años para resistir las balas de mosquete, la khe! burund es un camisote de malla ligera con tiras de cuero rígido tejidas entre los eslabones, usado sobre una chaqueta de cuero. La capa cubre los brazos del usuario hasta el codo, sus piernas hasta la rodilla e incluye una capucha. Favorecida por muchos mercenarios weren y expatriados porque es un elemento de la tecnología weren que resiste las armas humanas, la khe! burund (el signo de exclamación significa que la primera palabra se vocaliza como una tos) se ha convertido en un emblema de la tradición weren frente a un cambio abrumador.",
        "Bellweyn Sil (Fraal)": "El bellweyn sil (“abrigo de batalla” en lengua fraal) es una prenda protectora que encarna parte de la elegancia y estética de la especie. Consiste en un traje ligero de tejido molecular diseñado. Sobre este, capas de tejido molecular endurecido se disponen en bandas suaves y superpuestas que se asemejan vagamente a las antiguas armaduras humanas. Ricamente adornado con bordados y acabados metálicos, el bellweyn sil es una prenda espectacular adecuada para muchos asuntos diplomáticos o formales. Los líderes, guardias y emisarios fraal suelen usar esta prenda cuando tratan con especies menos desarrolladas.",
        "Had'Niltas (Mechalus)": "Un ejemplo sobresaliente de tecnología alienígena, el had'niltas es un traje superior de armadura motorizada. A diferencia de los voluminosos trajes de placas desarrollados por los armeros humanos, el had'niltas es ligero y flexible. Consiste en un mono de cuerpo completo o envoltura de tela avanzada. Dentro de la tela del traje hay una capa de metal líquido que contiene millones de nanocircuitos. Estos responden instantáneamente a cualquier ataque, endureciendo el traje en el punto de impacto y disipando el calor o la energía. El had'niltas es casi impermeable a los ataques cortantes o a las armas de energía, pero los proyectiles de alta velocidad a veces pueden penetrar antes de que el traje reaccione."
    }

    # Apply to English Data
    for category in ['light', 'combat', 'powered']:
        for group in en_data[category]['groups']:
            for item in group['items']:
                if item['name'] in verbatim_descriptions:
                    item['description'] = verbatim_descriptions[item['name']]

    # Spanish Mapping
    core_translations = {
        "Hide armor": "Armadura de piel", "Leather armor": "Armadura de cuero", "Helm": "Yelmo",
        "Shield, small": "Escudo pequeño", "Shield, medium": "Escudo mediano", "Leather coat": "Abrigo de cuero",
        "Shield, large": "Escudo grande", "CF short coat": "Abrigo corto CF", "CF softsuit": "Ropa de infiltración CF",
        "Deflection harness": "Arnés de deflexión", "Ablative harness": "Arnés ablativo", 
        "Displacer softsuit": "Softsuit desplazador", "Energy web": "Red de energía", 
        "Stealth softsuit": "Softsuit de sigilo", "BodyGuard Ballistic Vest": "Chaleco balístico BodyGuard",
        "Landsknecht 34 Ballistic Jacket": "Chaqueta balística Landsknecht 34", "Haramaki long coat": "Abrigo largo Haramaki",
        "Haramaki short jacket": "Chaqueta corta Haramaki", "Milano GX CF Bodysuit": "Mono CF Milano GX",
        "Battlehawk Zero-G Assault Gear": "Armadura de asalto Battlehawk Zero-G", 
        "Scout 230 AET Assault Gear": "Armadura de explorador Scout 230 AET",
        "Dauntless 29 Attack Armor": "Armadura de ataque Dauntless 29", "Chain mail": "Cota de malla",
        "Plate, full": "Armadura de placas", "Plate, partial": "Placas parciales", "Flak jacket": "Chaleco antiflac",
        "Assault gear": "Equipo de asalto", "Battle vest": "Chaleco de batalla", "Riot helmet": "Casco antidisturbios",
        "Riot shield": "Escudo antidisturbios", "Assault gear, hvy": "Equipo de asalto pesado",
        "Attack armor": "Armadura de ataque", "Battle jacket": "Chaqueta de batalla", "CF long coat": "Abrigo largo CF",
        "Cerametal armor": "Armadura de cerametal", "ACN 4 Cerametal Armor": "Armadura de cerametal ACN 4",
        "Bushmaster Cerametal Mail": "Cota de cerametal Bushmaster", "Attack armor, pow": "Armadura de ataque motorizada",
        "Body tank": "Tanque de cuerpo", "Body tank, recon": "Tanque de cuerpo, recon",
        "Body tank, zero-g": "Tanque de cuerpo, gravedad-0", "Body tank, over.": "Tanque de cuerpo terrestre",
        "Tiger Mod 6 Powered Armor": "Servoarmadura Tiger Mod 6", "ABM-5 Paladin Battle Armor": "Armadura de batalla ABM-5 Paladin",
        "Aegis 650 Cerametal Shield": "Escudo de cerametal Aegis 650", "SAI Powered Shield": "Escudo motorizado SAI",
        "Rampart Deflection Inducer": "Inductor de deflexion Rampart", "Anvil 44 Magnetic Screen": "Pantalla magnetica Anvil 44",
        "Alpha 50 Particle Screen": "Pantalla de particulas Alpha 50", "SCM-16 Capacitor Screen": "Pantalla de capacitadores SCM-16",
        "Ptokh K'se (T'sa armor)": "Ptokh K'se (Armadura T'sa)", "Khe! Burund (Weren mail)": "Khe! Burund (Malla Weren)",
        "ABS-11 Dragoon Recon Armor": "Armadura de reconocimiento Dragoon ABS-11", 
        "AAS-23 Titan Assault Armor": "Armadura de asalto Titan AAS-23",
        "Bellweyn Sil (Fraal)": "Bellweyn Sil (Fraal)", "Had'Niltas (Mechalus)": "Had'Niltas (Mechalus)"
    }

    core_descriptions_es = {
        "Hide armor": "Esta armadura utiliza pieles de animales, que se cosen o sujetan para ajustarse aproximadamente al cuerpo del individuo que la lleva. La protección que proporciona es mínima y su uso durante esta era es poco común.",
        "Leather armor": "Esta protección es fácil de fabricar y mantener, y hace un trabajo decente protegiendo al portador de las armas de la época.",
        "Helm": "El centro de los órganos sensoriales recibe protección adicional. Un yelmo no puede usarse con otra armadura si la armadura contiene un casco o capucha integral.",
        "Shield, small": "En una era de espadas y flechas, los escudos son un medio de defensa común y eficaz. Un escudo pequeño suele ser redondo, de unos 50 cm de diámetro.",
        "Shield, medium": "Un escudo mediano es más pesado que uno pequeño y suele tener un metro o más de diámetro. Puede ser redondo o cuadrado.",
        "Leather coat": "El abrigo de cuero no es la mejor armadura, pero es mejor que nada en la batalla. Los abrigos de cuero tienen la ventaja de ser naturalmente ocultables.",
        "Shield, large": "Un escudo grande es rectangular, generalmente de 1 metro de ancho y 1,5 metros de alto.",
        "CF short coat": "Diseñado para parecerse a una chaqueta, el abrigo de CF utiliza tejidos extensos de fibras de carbonato resistentes.",
        "BodyGuard Ballistic Vest": "Es una de las protecciones personales más populares. Significativamente más ligera y duradera que sus predecesoras, se ajusta perfectamente bajo la ropa de calle sin señales externas.",
        "Landsknecht 34 Ballistic Jacket": "Es la armadura más pesada que se puede llevar en un puerto espacial agitado sin atraer atención no deseada. Incluye capucha con sellado facial y máscara de vacío.",
        "Haramaki long coat": "Diseñada para un uso cómodo durante todo el día, proporciona un aumento modesto en protección al cubrir una mayor parte del cuerpo.",
        "Haramaki short jacket": "Versión corta de la serie Haramaki, para entornos menos amenazadores pero manteniendo el tejido de fibra de carbono de alta calidad.",
        "Milano GX CF Bodysuit": "Versión más pesada del popular softsuit, con paneles moldeados y apariencia elegante. Es el tope de gama.",
        "Battlehawk Zero-G Assault Gear": "Diseñada para gravedad baja, se ajusta ceñida e incluye máscara de vacío con 8 horas de reserva y propulsores de bota.",
        "Scout 230 AET Assault Gear": "Versión blindada de un traje ambiental suave (e-suit), diseñada para uso prolongado en entornos peligrosos.",
        "Dauntless 29 Attack Armor": "Última versión del blindaje de placas de polímero no motorizado. Incluye máscara respiradora y dos trauma packs.",
        "Tiger Mod 6 Powered Armor": "Incluye sistemas de puntería, mejora de imagen, comunicaciones, láser de señalización y dos trauma packs.",
        "ABM-5 Paladin Battle Armor": "Traje estándar de los Marines de la Concordia. Sus baterías permiten 12 horas de acción intensa o 72 de actividad intermitente.",
        "Chain mail": "Diversos tipos de armadura laminada, de escamas, bergantina y de bandas entran en la categoría general de cota de malla."
    }
    core_descriptions_es.update(verbatim_descriptions_es)

    # Rebuild ES data
    new_es_data = {
        "light": { "columns": es_data['light']['columns'], "groups": [] },
        "combat": { "columns": es_data['combat']['columns'], "groups": [] },
        "powered": { "columns": es_data['powered']['columns'], "groups": [] }
    }

    for cat in ['light', 'combat', 'powered']:
        for en_group in en_data[cat]['groups']:
            es_group = { "name": en_group['name'], "items": [] }
            for en_item in en_group['items']:
                es_item = en_item.copy()
                es_item['name'] = core_translations.get(en_item['name'], en_item['name'])
                if en_item['name'] in core_descriptions_es:
                    es_item['description'] = core_descriptions_es[en_item['name']]
                es_group['items'].append(es_item)
            new_es_data[cat]['groups'].append(es_group)

    # Save
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, indent=2, ensure_ascii=False)
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(new_es_data, f, indent=2, ensure_ascii=False)

    print("Verbatim descriptions applied successfully!")

if __name__ == '__main__':
    apply_verbatim_descriptions()
