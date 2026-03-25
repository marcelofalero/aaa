import json

en_file = 'site/data/weapons.json'
es_file = 'site/data/weapons.es.json'

with open(en_file, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

with open(es_file, 'r', encoding='utf-8') as f:
    es_data = json.load(f)

en_ranged = [
    {
        "name": "AAMG-12 Mass Rifle", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "4/12/30",
        "type": "En/G", "damage": "d6+1w/d8+1w/d6+1m", "act": "2", "clip": "8 shots", "mass": "4", "hide": "-",
        "avail": "Mil", "cost": "2450",
        "description": "A larger and more powerful version of the mass pistol, the mass rifle sacrifices range and rate of fire for unbeatable armor penetration. The AAMG is a brand-new design from Karadnya-Brusilev. It's the most accurate mass rifle on the market today, and its new charge cell technology doubles its magazine capacity compared to others of its type. (Payload: Gravity point-source)"
    },
    {
        "name": "Ninja 600 Laser Pistol", "skill": "Ranged-pistol", "acc": "-1", "md": "F", "range": "20/40/150",
        "type": "En/O", "damage": "d4+1w/d6+1w/d4m", "act": "4", "clip": "20 shots", "mass": "0.5", "hide": "+4",
        "avail": "Con", "cost": "1225",
        "description": "The Ninja 600 is a small and easily concealable laser pistol built to the flush-front design. Like all lasers, it's extremely accurate and offers the best range characteristics of any handgun. The Ninja line is very popular with corporate execs and other affluent celebrities who want to carry a weapon for self-defense without advertising the fact that they're armed. Most combat specs prefer a heavier weapon. (Payload: Coherent light)"
    },
    {
        "name": "CLR-19 Laser Rifle", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "100/600/1500",
        "type": "En/O", "damage": "d6+1w/d6+3w/d4+1m", "act": "3", "clip": "12 shots", "mass": "4", "hide": "-",
        "avail": "Mil", "cost": "1800",
        "description": "The standard infantry firearm of the Orion League, CLR-19 (Combat Laser Rifle-19) is a weapon of extraordinary range and accuracy. It's proven its value in numerous engagements against older charge weapons, especially in relatively open terrain. In close quarters, the weapon's length and low rate of fire are distinct drawbacks compared to the faster-firing and harder-hitting 11mm charge rifle. (Payload: Coherent light)"
    },
    {
        "name": "Valkyrie 9 Autolaser", "skill": "Ranged-SMG", "acc": "0", "md": "B/A", "range": "20/80/200",
        "type": "En/O", "damage": "d6+1w/d6+3w/d4+1m", "act": "4", "clip": "10 bursts", "mass": "3.25", "hide": "-",
        "avail": "Con", "cost": "1725",
        "description": "The largest and most powerful autolaser available, the Valkyrie offers damage equal to a laser rifle with full automatic fire. While many people refer to the autolaser as a laser submachine gun, this is a misnomer-the device is not a machine gun and has little in common with any conventional firearm. Bursts or full-auto attacks with this weapon are actually sweeps and slashes of its white-hot beam. (Payload: Coherent light)"
    },
    {
        "name": "Falcon T9 Stutter Pistol", "skill": "Ranged-pistol", "acc": "0", "md": "F", "range": "4/8/20",
        "type": "LI/O", "damage": "d6+2s/d8+2s/d8+4s", "act": "3", "clip": "10 shots", "mass": "0.75", "hide": "+4",
        "avail": "Com", "cost": "375",
        "description": "One of the most popular handguns in human space, the Falcon T9 is synonymous with reasonably priced, nonlethal personal defense. It's lighter and slimmer than the standard stutter pistol, trading range and clip capacity for easy concealment and use by people who aren't highly trained. 'Point and say good-night' is the tag line for SekureTek's Falcon ads, and it's just about that easy. (Payload: Compressed air)"
    },
    {
        "name": "Condor X7 Stutter Pistol", "skill": "Ranged-pistol", "acc": "0", "md": "F", "range": "8/16/40",
        "type": "LI/O", "damage": "d6+3s/d8+3s/d12+3s", "act": "3", "clip": "8 shots", "mass": "1.25", "hide": "+1",
        "avail": "Com", "cost": "850",
        "description": "Professional peacekeepers prefer a more capable weapon than the light stutter pistols favored for personal defense. The Condor is an example of the heavy stutter pistol, a weapon designed for the subdual of armed, dangerous criminals. One hit almost always dazes or knocks out an unarmored opponent, and even armored targets can be brought down with accurate and sustained fire. (Payload: Compressed air)"
    },
    {
        "name": "Cyclone 700 Stutter SMG", "skill": "Ranged-SMG", "acc": "0", "md": "B/A", "range": "10/20/80",
        "type": "LI/O", "damage": "d6+2s/d8+2s/d8+4s", "act": "4", "clip": "20 bursts", "mass": "3", "hide": "+1",
        "avail": "Con", "cost": "1000",
        "description": "The stutter SMG isn't a real submachine gun, of course; it's referred to as an SMG because of its high cyclic rate of fire. It's intended for use in close-quarters riot control or police raid situations in which the authorities must subdue a large number of people in a very short time. Stutter SMGs are also favored by special forces teams attempting to take prisoners instead of simply killing their enemies. (Payload: Compressed air)"
    },
    {
        "name": "Sirocco 100 Stutter Rifle", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "20/40/200",
        "type": "LI/O", "damage": "d6+3s/d8+3s/d12+3s", "act": "2", "clip": "12 shots", "mass": "3.5", "hide": "-",
        "avail": "Con", "cost": "750",
        "description": "In situations where you're only going to get one chance to stun an opponent, the stutter rifle's a good choice. It offers a longer range, more hitting power, and better accuracy than any other stutter weapon, making it perfect for taking out a problem with one clean shot at distance. The Sirocco is renowned as a scout's weapon, durable and effective; last year it won Merrick's Triple-Bullseye for best in class. (Payload: Compressed air)"
    },
    {
        "name": "Tauri 9 Impact Pistol", "skill": "Ranged-pistol", "acc": "0", "md": "F/B", "range": "4/12/36",
        "type": "LI/O", "damage": "2d4s/d6+1w/d6+3w", "act": "4", "clip": "12 shots/4 bursts", "mass": "1", "hide": "+2",
        "avail": "Con", "cost": "1150",
        "description": "A deadly refinement of stutter weapon technology, the impact pistol fires an even more powerful blast of compressed air that can powder concrete at close range. It can be set for a high-speed mode that allows burst fire (but not full automatic), or for low-speed, single-shot mode. Like any stutter weapon, the impact pistol doesn't work in vacuum due to the lack of air to compress. (Payload: Compressed air)"
    },
    {
        "name": "Apache LX Reflex Bow", "skill": "Ranged-bow", "acc": "0", "md": "F", "range": "50/100/250",
        "type": "LI/O", "damage": "d4+2w/d6+2w/d4+1m", "act": "2", "clip": "1 shot", "mass": "1", "hide": "-",
        "avail": "Com", "cost": "650",
        "description": "The bow's greatest advantage is silence and stealth. It has no muzzle flash or loud report to give away the user's location, making it perfect for dense terrain such as jungle or heavy brush. Its disadvantage is the low rate of fire (after each 'shot', the user must waste an action to ready another arrow, or shoot with a +2 step penalty) and its size, which prevents it from being fired from a prone position. (Payload: Razor-tipped arrow)"
    }
]

en_heavy = [
    {
        "name": "Supernova XI Mass Cannon", "skill": "Heavy-direct fire", "acc": "0", "md": "F", "range": "6/20/60",
        "type": "En/G", "damage": "d8+1w/d12+1w/d8+1m", "act": "2", "clip": "8 shots", "mass": "8.75", "hide": "-",
        "avail": "Res", "cost": "6825",
        "description": "The mass cannon is something of a white elephant. While it's a powerful, hard-hitting gun, other heavy weapons hit just as hard with better range characteristics. The weapon's designers hoped to follow up on the success of its smaller cousins by designing a true man-portable antivehicular mass weapon, but they weren't able to achieve the kind of armor penetration increase they had hoped for. (Payload: Gravity point-source)"
    },
    {
        "name": "Roc Z1 Stutter Cannon", "skill": "Heavy-direct fire", "acc": "-1", "md": "F", "range": "20/40/80",
        "type": "LI/O", "damage": "d6+2s/d8+3s/2d6+3s", "act": "2", "clip": "10 shots", "mass": "15", "hide": "-",
        "avail": "Con", "cost": "2500",
        "description": "When it's important to subdue a number of people in a hurry, the stutter cannon is the best tool for the job. The cannon affects all targets in a 3-meter radius, inflicting damage one category less than the damage inflicted to the primary target. For example, if the user scores a Good hit (d8+3s) against one rioter, all other people within 3 meters suffer Ordinary damage (d6+2s). Ordinary hits inflict no damage to nearby targets. (Payload: Compressed air)"
    }
]

es_ranged = [
    {
        "name": "Rifle de Masa AAMG-12", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "4/12/30",
        "type": "En/G", "damage": "d6+1w/d8+1w/d6+1m", "act": "2", "clip": "8 disparos", "mass": "4", "hide": "-",
        "avail": "Mil", "cost": "2450",
        "description": "Una versión más grande y potente de la pistola de masa. Sacrifica alcance y cadencia de fuego por una penetración de armadura imbatible. El AAMG es un diseño moderno de Karadnya-Brusilev con características innovadoras: es el rifle de masa más preciso del mercado y su nueva tecnología de células duplica su cargador respecto a armas similares. (Carga: Fuente puntual de gravedad)"
    },
    {
        "name": "Pistola Láser Ninja 600", "skill": "Ranged-pistol", "acc": "-1", "md": "F", "range": "20/40/150",
        "type": "En/O", "damage": "d4+1w/d6+1w/d4m", "act": "4", "clip": "20 disparos", "mass": "0.5", "hide": "+4",
        "avail": "Con", "cost": "1225",
        "description": "La Ninja 600 es una pistola láser pequeña y muy ocultable con un diseño de frente liso. Como todos los láseres, es extremadamente precisa y ofrece el mejor alcance en pistolas. Es muy popular entre ejecutivos corporativos y celebridades que quieren un arma de autodefensa sin gritar que están armados. (Carga: Luz coherente)"
    },
    {
        "name": "Rifle Láser CLR-19", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "100/600/1500",
        "type": "En/O", "damage": "d6+1w/d6+3w/d4+1m", "act": "3", "clip": "12 disparos", "mass": "4", "hide": "-",
        "avail": "Mil", "cost": "1800",
        "description": "Arma de infantería estándar de la Liga de Orión, el CLR-19 (Combat Laser Rifle-19) es de un alcance y precisión extraordinarios. Ha probado su valor en numerosos enfrentamientos ante armas antiguas. En distancias cortas, su longitud y baja cadencia son desventajas frente a escopetas o el rápido rifle de carga de 11mm. (Carga: Luz coherente)"
    },
    {
        "name": "Autoláser Valkyrie 9", "skill": "Ranged-SMG", "acc": "0", "md": "B/A", "range": "20/80/200",
        "type": "En/O", "damage": "d6+1w/d6+3w/d4+1m", "act": "4", "clip": "10 ráfag.", "mass": "3.25", "hide": "-",
        "avail": "Con", "cost": "1725",
        "description": "El autoláser más potente del mercado. Ofrece daño igual a un rifle láser pero con fuego automático. Aunque lo llamen 'subfusil láser', no es una ametralladora real; lanza un chorro candente, realizando barridos y cortes continuos con su rayo blanco ardiente para simular enormes ráfagas contra el objetivo. (Carga: Luz coherente)"
    },
    {
        "name": "Pistola Stutter Falcon T9", "skill": "Ranged-pistol", "acc": "0", "md": "F", "range": "4/8/20",
        "type": "LI/O", "damage": "d6+2s/d8+2s/d8+4s", "act": "3", "clip": "10 disparos", "mass": "0.75", "hide": "+4",
        "avail": "Com", "cost": "375",
        "description": "Una de las pistolas de mano más populares. La Falcon T9 es el súmmum de defensa personal a buen precio. Más ligera y esbelta que su hermana estándar, cambia alcance y eficacia en un encuentro por ser muy portable. Ocultable y fácil para uso civil sin apenas entrenamiento. (Carga: Aire comprimido)"
    },
    {
        "name": "Pistola Stutter Condor X7", "skill": "Ranged-pistol", "acc": "0", "md": "F", "range": "8/16/40",
        "type": "LI/O", "damage": "d6+3s/d8+3s/d12+3s", "act": "3", "clip": "8 disparos", "mass": "1.25", "hide": "+1",
        "avail": "Com", "cost": "850",
        "description": "Las fuerzas de paz profesionales prefieren pistolas algo más pesadas a las de venta cotidiana. La Condor es de marco pesado diseñada para someter criminales no letalmente. Un impacto ordinario aturde o noquea, e incuso un hombre fuertemente armado puede tropezar. (Carga: Aire comprimido)"
    },
    {
        "name": "SMG Stutter Cyclone 700", "skill": "Ranged-SMG", "acc": "0", "md": "B/A", "range": "10/20/80",
        "type": "LI/O", "damage": "d6+2s/d8+2s/d8+4s", "act": "4", "clip": "20 ráfag.", "mass": "3", "hide": "+1",
        "avail": "Con", "cost": "1000",
        "description": "El SMG stutter no es un subfusil real; se le llama así por su alta cadencia. Diseñado para control de disturbios o redadas donde se debe doblegar a multitudes a rápida escala. Equipos tácticos lo usan para capturar rehenes sin sacrificar sus vidas por su baja letalidad. (Carga: Aire comprimido)"
    },
    {
        "name": "Rifle Stutter Sirocco 100", "skill": "Ranged-rifle", "acc": "-1", "md": "F", "range": "20/40/200",
        "type": "LI/O", "damage": "d6+3s/d8+3s/d12+3s", "act": "2", "clip": "12 disparos", "mass": "3.5", "hide": "-",
        "avail": "Con", "cost": "750",
        "description": "Si solo tienes una oportunidad para inhabilitar un objetivo con fuego no letal, el Sirocco 100 es perfecto. Mayor alcance, impacto y puntería que cualquier arma stun parecida. Conocida entre los scouts por su durabilidad. Ganador de Triple-Diana para el modelo de su rama del año anterior. (Carga: Aire comprimido)"
    },
    {
        "name": "Pistola de Impacto Tauri 9", "skill": "Ranged-pistol", "acc": "0", "md": "F/B", "range": "4/12/36",
        "type": "LI/O", "damage": "2d4s/d6+1w/d6+3w", "act": "4", "clip": "12 tiros/4 ráfag.", "mass": "1", "hide": "+2",
        "avail": "Con", "cost": "1150",
        "description": "Un refinamiento mortal del arma stutter, esta pistola lanza aire comprimido tan violento capaz de pulverizar hormigón a corta distancia. Tiene modo de ráfaga limitada y daño abismal. Al igual que con el aire, el arma fallará irremediablemente al intentar ser disparada en pleno vacío. (Carga: Aire comprimido)"
    },
    {
        "name": "Arco Reflejo Apache LX", "skill": "Ranged-bow", "acc": "0", "md": "F", "range": "50/100/250",
        "type": "LI/O", "damage": "d4+2w/d6+2w/d4+1m", "act": "2", "clip": "1 dispa.", "mass": "1", "hide": "-",
        "avail": "Com", "cost": "650",
        "description": "Su mayor ventaja es el sigilo y mutismo, sin ráfagas de luz ni retroceso ruidoso que revele la posición, haciéndolo perfecto y letal en lo salvaje de la jungla espesa. Cada reabastecimiento requiere 1 acción. Así mismo se requiere total control de ambos brazos, inhabilitando su disparo tendido en suelo por completo. (Carga: Flecha punta navaja)"
    }
]

es_heavy = [
    {
        "name": "Cañón de Masa Supernova XI", "skill": "Heavy-direct fire", "acc": "0", "md": "F", "range": "6/20/60",
        "type": "En/G", "damage": "d8+1w/d12+1w/d8+1m", "act": "2", "clip": "8 disparos", "mass": "8.75", "hide": "-",
        "avail": "Res", "cost": "6825",
        "description": "El cañón de masa es un arma estruendosa en el campo de batalla. Poderoso y demoledor pero su poco avance es innegable. Los diseñadores intentaban replicar una versión antílope de la armadura ligera en algo antivehicular portátil, pero sacrificando muchísimas características para ello dejándola en nicho. (Carga: Fuente puntual gravedad)"
    },
    {
        "name": "Cañón Stutter Roc Z1", "skill": "Heavy-direct fire", "acc": "-1", "md": "F", "range": "20/40/80",
        "type": "LI/O", "damage": "d6+2s/d8+3s/2d6+3s", "act": "2", "clip": "10 disparos", "mass": "15", "hide": "-",
        "avail": "Con", "cost": "2500",
        "description": "Herramienta definitiva de control de masas por repulsión. Afectando en un radio de 3 metros, sus ráfagas rebotan causando dolor secundario a cualquiera a merced. Los alcanzados en impacto de grado Bueno (d8+3s) salpicarán un impacto indirecto grado Ordinario de (d6+2s) a todos a 3m. El caso inferior no produce daño indirecto del todo. (Carga: Aire comprimido)"
    }
]

def add_weapons(data, section, weapons, group_name):
    for group in data[section]['groups']:
        if group['name'] == group_name:
            group['items'].extend(weapons)
            break

add_weapons(en_data, "ranged", en_ranged, "PL 7: Gravity Age")
add_weapons(en_data, "heavy", en_heavy, "PL 7: Gravity Age")

add_weapons(es_data, "ranged", es_ranged, "PL 7: Era de la gravedad")
add_weapons(es_data, "heavy", es_heavy, "PL 7: Era de la gravedad")

with open(en_file, 'w', encoding='utf-8') as f:
    json.dump(en_data, f, indent=4, ensure_ascii=False)

with open(es_file, 'w', encoding='utf-8') as f:
    json.dump(es_data, f, indent=4, ensure_ascii=False)

print("Add successful!")
