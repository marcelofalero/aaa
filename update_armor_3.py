import json

def update_armor_batch_3():
    en_file = 'site/data/armor.json'
    es_file = 'site/data/armor.es.json'

    # Load English
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # Updates for existing items (Fixing cut descriptions and data)
    for g in en_data['powered']['groups']:
        for item in g['items']:
            if item['name'] == "ABS-11 Dragoon Recon Armor":
                item['description'] = "Also known as a recon or scout body tank, the Dragoon is a lighter and more mobile powered suit. It has all the built-in features described above [referring to systems like targeting, optics, and trauma packs], with one key addition—a gravity induction drive, providing flight capability at a maximum speed of 180 kph (or meters per phase). Since this is powered flight, the wearer suffers no fatigue damage for flying. On the ground, the Dragoon can move at 30 kph (or 30 meters per phase) in broken terrain, or 60 kph on open ground. Typically, one squad of troops in an armor platoon is equipped with recon armor."
            if item['name'] == "AAS-23 Titan Assault Armor":
                item['description'] = "Fully space-to-ground capable, the Titan is also known as zero-g armor. It can be fitted with an ablative reentry shroud (cost $500) for orbital insertion, descending from an altitude of 200 km to the ground in about five minutes. It has limited flight capability and is rated up to an airspeed of 100 kph or ground speeds of 20 to 40 kph. The Titan features an air/space radar similar to the radar gauntlet, and its weapon hardpoint can be used to mount any of the following: a grenade launcher with a 12-round magazine, a bantam launcher, any direct-fire heavy weapon, or any powered melee weapon."

    # New Alien Armors
    new_alien_items_en = [
        {
            "name": "Bellweyn Sil (Fraal)",
            "mass": "2",
            "ap": "0",
            "lhe": "d6/d6-1/d6-1",
            "type": "O",
            "hide": "+3",
            "avail": "Con",
            "cost": "6500",
            "description": "The bellweyn sil ('battle-coat' in the fraal tongue) is a protective garment that embodies some of the elegance and aesthetics of the species. It consists of a light arming suit of engineered molecular weave. Over this, layers of stiffened molecular weave are fashioned into soft, overlapping bands that vaguely resemble ancient human armors. Richly adorned with embroidery and metallic finishes, the bellweyn sil is a spectacular garment suitable for many diplomatic or formal affairs. Fraal leaders, guards, and emissaries often wear this garment when dealing with less developed species."
        },
        {
            "name": "Had'Niltas (Mechalus)",
            "mass": "12",
            "ap": "+1",
            "lhe": "2d4/d6+1/2d4+1",
            "type": "G",
            "avail": "Res",
            "cost": "25000",
            "description": "An outstanding example of alien technology, the had'niltas is a superior suit of powered armor. Unlike the bulky plated suits developed by human armorers, the had'niltas is light and flexible. It consists of a full-body jumpsuit or wrap of advanced fabric. Inside the suit's fabric is a layer of liquid metal containing millions of nanocircuits. These instantly respond to any attack, hardening the suit at the point of impact and dissipating heat or energy. The had'niltas is nearly impervious to slashing attacks or energy weapons, but high-velocity projectiles can sometimes penetrate before the suit reacts. It adds an effective Strength of 15."
        }
    ]

    # Add Bellweyn to Light PL 7
    for g in en_data['light']['groups']:
        if g['name'] == "PL 7":
            if not any(i['name'] == "Bellweyn Sil (Fraal)" for i in g['items']):
                g['items'].append(new_alien_items_en[0])

    # Add Had'Niltas to Powered PL 7
    for g in en_data['powered']['groups']:
        if g['name'] == "PL 7":
            if not any(i['name'] == "Had'Niltas (Mechalus)" for i in g['items']):
                g['items'].append(new_alien_items_en[1])

    # Harmonize Spanish
    translations = {
        "Hide armor": "Armaduera de piel",
        "Leather armor": "Armadura de cuero",
        "Helm": "Yelmo",
        "Shield, small": "Escudo pequeño",
        "Shield, medium": "Escudo mediano",
        "Leather coat": "Abrigo de cuero",
        "Shield, large": "Escudo grande",
        "CF short coat": "Abrigo corto CF",
        "CF softsuit": "Ropa de infiltración CF",
        "Deflection harness": "Arnés de deflexión",
        "Ablative harness": "Arnés ablativo",
        "Displacer softsuit": "Softsuit desplazador",
        "Energy web": "Red de energía",
        "Stealth softsuit": "Softsuit de sigilo",
        "BodyGuard Ballistic Vest": "Chaleco balístico BodyGuard",
        "Landsknecht 34 Ballistic Jacket": "Chaqueta balística Landsknecht 34",
        "Haramaki long coat": "Abrigo largo Haramaki",
        "Haramaki short jacket": "Chaqueta corta Haramaki",
        "Milano GX CF Bodysuit": "Mono CF Milano GX",
        "Battlehawk Zero-G Assault Gear": "Armadura de asalto Battlehawk Zero-G",
        "Scout 230 AET Assault Gear": "Armadura de explorador Scout 230 AET",
        "Dauntless 29 Attack Armor": "Armadura de ataque Dauntless 29",
        "Chain mail": "Cota de malla",
        "Plate, full": "Armadura de placas",
        "Plate, partial": "Placas parciales",
        "Flak jacket": "Chaleco antiflac",
        "Assault gear": "Equipo de asalto",
        "Battle vest": "Chaleco de batalla",
        "Riot helmet": "Casco antidisturbios",
        "Riot shield": "Escudo antidisturbios",
        "Assault gear, hvy": "Equipo de asalto pesado",
        "Attack armor": "Armadura de ataque",
        "Battle jacket": "Chaqueta de batalla",
        "CF long coat": "Abrigo largo CF",
        "Cerametal armor": "Armadura de cerametal",
        "ACN 4 Cerametal Armor": "Armadura de cerametal ACN 4",
        "Bushmaster Cerametal Mail": "Cota de cerametal Bushmaster",
        "Attack armor, pow": "Armadura de ataque motorizada",
        "Body tank": "Tanque de cuerpo",
        "Body tank, recon": "Tanque de cuerpo, recon",
        "Body tank, zero-g": "Tanque de cuerpo, gravedad-0",
        "Body tank, over.": "Tanque de cuerpo terrestre",
        "Tiger Mod 6 Powered Armor": "Servoarmadura Tiger Mod 6",
        "ABM-5 Paladin Battle Armor": "Armadura de batalla ABM-5 Paladin",
        "Aegis 650 Cerametal Shield": "Escudo de cerametal Aegis 650",
        "SAI Powered Shield": "Escudo motorizado SAI",
        "Rampart Deflection Inducer": "Inductor de deflexion Rampart",
        "Anvil 44 Magnetic Screen": "Pantalla magnetica Anvil 44",
        "Alpha 50 Particle Screen": "Pantalla de particulas Alpha 50",
        "SCM-16 Capacitor Screen": "Pantalla de capacitadores SCM-16",
        "Ptokh K'se (T'sa armor)": "Ptokh K'se (Armadura T'sa)",
        "Khe! Burund (Weren mail)": "Khe! Burund (Malla Weren)",
        "ABS-11 Dragoon Recon Armor": "Armadura de reconocimiento Dragoon ABS-11",
        "AAS-23 Titan Assault Armor": "Armadura de asalto Titan AAS-23",
        "Bellweyn Sil (Fraal)": "Bellweyn Sil (Fraal)",
        "Had'Niltas (Mechalus)": "Had'Niltas (Mechalus)"
    }

    descriptions_es = {
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
        "ABS-11 Dragoon Recon Armor": "También conocido como tanque de cuerpo de reconocimiento o exploración, el Dragoon es un traje motorizado más ligero y móvil. Tiene todas las funciones integradas de los tanques de cuerpo estándar, con una adición clave: un impulso de inducción por gravedad, que proporciona capacidad de vuelo a una velocidad máxima de 180 km/h (o metros por fase). Dado que se trata de un vuelo motorizado, el usuario no sufre daños por fatiga al volar. En tierra, el Dragoon puede moverse a 30 km/h (o 30 metros por fase) en terreno accidentado, o a 60 km/h en terreno abierto. Normalmente, un escuadrón de tropas en un pelotón de armaduras está equipado con armadura de reconocimiento.",
        "AAS-23 Titan Assault Armor": "Totalmente capaz de despliegue orbital, el Titán también se conoce como armadura de gravedad cero. Puede equiparse con una cubierta ablativa de reentrada (coste 500 $) para inserción orbital, descendiendo desde una altitud de 200 km hasta el suelo en unos cinco minutos. Tiene una capacidad de vuelo limitada y está clasificado para una velocidad aérea de hasta 100 km/h o velocidades terrestres de 20 a 40 km/h. El Titán cuenta con un radar aire/espacio similar al guantelete de radar, y su punto de anclaje de armas puede usarse para montar cualquiera de los siguientes: un lanzagranadas con un cargador de 12 rondas, un lanzador bantam, cualquier arma pesada de fuego directo o cualquier arma cuerpo a cuerpo motorizada.",
        "Bellweyn Sil (Fraal)": "El bellweyn sil (“abrigo de batalla” en lengua fraal) es una prenda protectora que encarna parte de la elegancia y estética de la especie. Consiste en un traje ligero de tejido molecular diseñado. Sobre este, capas de tejido molecular endurecido se disponen en bandas suaves y superpuestas que se asemejan vagamente a las antiguas armaduras humanas. Ricamente adornado con bordados y acabados metálicos, el bellweyn sil es una prenda espectacular adecuada para muchos asuntos diplomáticos o formales. Los líderes, guardias y emisarios fraal suelen usar esta prenda cuando tratan con especies menos desarrolladas.",
        "Had'Niltas (Mechalus)": "Un ejemplo sobresaliente de tecnología alienígena, el had'niltas es un traje superior de armadura motorizada. A diferencia de los voluminosos trajes de placas desarrollados por los armeros humanos, el had'niltas es ligero y flexible. Consiste en un mono de cuerpo completo o envoltura de tela avanzada. Dentro de la tela del traje hay una capa de metal líquido que contiene millones de nanocircuitos. Estos responden instantáneamente a cualquier ataque, endureciendo el traje en el punto de impacto y disipando el calor o la energía. El had'niltas es casi impermeable a los ataques cortantes o a las armas de energía, pero los proyectiles de alta velocidad a veces pueden penetrar antes de que el traje reaccione. Proporciona una Fuerza efectiva de 15.",
        "Tiger Mod 6 Powered Armor": "Incluye sistemas de puntería, mejora de imagen, comunicaciones, láser de señalización y dos trauma packs.",
        "ABM-5 Paladin Battle Armor": "Traje estándar de los Marines de la Concordia. Sus baterías permiten 12 horas de acción intensa o 72 de actividad intermitente.",
        "Aegis 650 Cerametal Shield": "Ligero y extremadamente resistente. Incluye mira de vision y puerto de disparo. Proporciona un aumento de +1 al modificador de resistencia contra ataques a distancia cuando se utiliza como cobertura portatil.",
        "SAI Powered Shield": "Unidad de flotacion libre propulsada por un motor de induccion. Sus sensores inteligentes detectan ataques entrantes y dirigen el escudo para interponerse automaticamente.",
        "Rampart Deflection Inducer": "Version economica del modelo estandar, el Rampart sacrifica potencia defensiva por una construccion ligera. Crea un campo cilindrico de energia gravitatoria alrededor del usuario.",
        "Anvil 44 Magnetic Screen": "Proporciona una excelente proteccion contra armas cuerpo a cuerpo metalicas, proyectiles metalicos y armas electricas. Nota: solo eficaz contra ataques metalicos/electricos. Las celdas duran 6 asaltos.",
        "Alpha 50 Particle Screen": "Genera una cáscara de partículas alfa. La pantalla 'parpadea' cuando el heroe dispara su propia arma, por lo que no tiene efecto en ninguna fase en la que el heroe ataque. Resistencia máxima: 10 asaltos.",
        "SCM-16 Capacitor Screen": "Crea un campo de partículas ionizadas. Reduce el daño de energía en 4 a 2 heridas antes de tener en cuenta el daño secundario. Dureza Buena contra LI/HI, Asombrosa contra Energía.",
        "Ptokh K'se (T'sa armor)": "Version T'sa de un chaleco antibalas. Consiste en un tejido denso de hilo de aleacion extruido, tejido en una tela gruesa y comprimido entre capas artificiales resistentes.",
        "Khe! Burund (Weren mail)": "Camisote de malla ligera con tiras de cuero rigido tejidas entre los eslabones, usado sobre una chaqueta de cuero. Favorito de los mercenarios Weren."
    }

    # Generate ES data
    es_data = {
        "light": { "columns": en_data['light']['columns'], "groups": [] },
        "combat": { "columns": en_data['combat']['columns'], "groups": [] },
        "powered": { "columns": en_data['powered']['columns'], "groups": [] }
    }

    # Rename columns names to Spanish for the ES version
    for cat in ['light', 'combat', 'powered']:
        for col in es_data[cat]['columns']:
            if col['name'] == 'Armor': col['name'] = 'Armadura'
            elif col['name'] == 'Mass': col['name'] = 'Masa'
            elif col['name'] == 'AP': col['name'] = 'Pena.'
            elif col['name'] == 'Type': col['name'] = 'Tipo'
            elif col['name'] == 'Hide': col['name'] = 'Ocult.'
            elif col['name'] == 'Avail': col['name'] = 'Disp.'
            elif col['name'] == 'Cost ($)': col['name'] = 'Coste ($)'
            elif col['name'] == 'Description': col['name'] = 'Descripción'

    # Populate groups
    for cat in ['light', 'combat', 'powered']:
        for en_group in en_data[cat]['groups']:
            es_group = { "name": en_group['name'], "items": [] }
            for en_item in en_group['items']:
                es_item = en_item.copy()
                es_item['name'] = translations.get(en_item['name'], en_item['name'])
                if en_item['name'] in descriptions_es:
                    es_item['description'] = descriptions_es[en_item['name']]
                es_group['items'].append(es_item)
            es_data[cat]['groups'].append(es_group)

    # Save files
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, indent=2, ensure_ascii=False)
    with open(es_file, 'w', encoding='utf-8') as f:
        json.dump(es_data, f, indent=2, ensure_ascii=False)

    print("Armor data successfully updated, fixed and localized!")

if __name__ == '__main__':
    update_armor_batch_3()
