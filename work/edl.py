"""Edit decision list for the housewarming 'Bref' montage.
Each entry: (start, end, kind, payload)
kind in {photo, text, twocol, number, dark}
"""

AVANT = list(range(52, 73)) + list(range(99, 105))
DEMOLITION = list(range(26, 49)) + [97, 98]
PLANS = [24, 25, 49, 50, 51, 73]
TRAVAUX = [n for n in range(74, 121) if n not in (97, 98, 113)] + [1] + list(range(8, 24))
DEMENAGEMENT = list(range(2, 8))
FUITE = [113]
CUISINE_TROUVEE = 121
REVEAL = list(range(121, 127))
ENDING_PHOTOS = list(range(127, 133))

_rapid_pool = DEMOLITION[4:] + TRAVAUX[10:]

def _take(pool, n):
    out, i = [], 0
    while len(out) < n:
        out.append(pool[i % len(pool)])
        i += 1
    return out

avant_it = iter(_take(AVANT, 12))
demolition_it = iter(_take(DEMOLITION, 4))
plans_it = iter(PLANS)
travaux_it = iter(_take(TRAVAUX, 8))
demenagement_it = iter(DEMENAGEMENT)
rapid_it = iter(_take(_rapid_pool, 19))
reveal_it = iter(REVEAL)
ending_it = iter(ENDING_PHOTOS)

def nx(it):
    return next(it)

EDL = []

def add(start, end, kind, payload=None):
    EDL.append((round(start, 3), round(end, 3), kind, payload))

# INTRO
add(0.00, 1.82, 'text', ['BREF.'])
add(1.82, 4.84, 'dark', None)
add(5.12, 7.94, 'dark', None)

# VISITES
add(8.26, 9.54, 'text', ['SANS FENÊTRE.'])
add(9.54, 10.82, 'text', ['TROP BRUYANT.'])
add(11.12, 12.06, 'text', ['TROP LOIN.'])
add(12.06, 13.00, 'text', ['AU REZ-DE-CHAUSSÉE.'])
add(13.42, 15.38, 'text', ['ON A REVU NOS CRITÈRES.'])

# ON A TROUVE / AVANT
add(15.90, 16.89, 'photo', nx(avant_it))
add(16.89, 17.88, 'photo', nx(avant_it))
add(18.44, 19.55, 'photo', nx(avant_it))
add(19.55, 20.66, 'photo', nx(avant_it))
add(20.98, 22.20, 'photo', nx(avant_it))
add(22.20, 23.20, 'photo', nx(avant_it))
add(23.20, 24.22, 'photo', nx(avant_it))
add(24.54, 25.80, 'photo', nx(avant_it))
add(26.34, 27.37, 'photo', nx(avant_it))
add(27.37, 28.40, 'photo', nx(avant_it))
add(28.40, 30.30, 'photo', nx(avant_it))

# DEMOLITION
add(30.30, 31.64, 'photo', nx(demolition_it))
add(31.64, 32.75, 'photo', nx(demolition_it))
add(32.75, 33.86, 'photo', nx(demolition_it))

# PLANS
add(34.66, 35.85, 'photo', nx(plans_it))
add(35.85, 37.04, 'photo', nx(plans_it))
add(37.36, 38.21, 'photo', nx(plans_it))
add(38.21, 39.06, 'photo', nx(plans_it))
add(39.06, 41.16, 'photo', nx(plans_it))
add(41.68, 48.90, 'photo', nx(plans_it))

# CUISINISTES
add(49.34, 52.68, 'text', ['TOUS LES CUISINISTES DU COIN.'])
add(53.20, 54.88, 'photo', CUISINE_TROUVEE)
add(55.22, 56.66, 'photo', nx(travaux_it))
add(57.04, 60.48, 'photo', FUITE[0])
add(60.80, 62.02, 'photo', nx(travaux_it))

# MATHIAS & ALISEE
add(62.60, 65.40, 'text', ['MATHIAS & ALISÉE :', '40 PAQUETS DE PARQUET.'])
add(65.84, 66.14, 'number', '40')
add(66.42, 68.08, 'text', ['ILS ÉTAIENT ENCORE NOS AMIS.'])

# MACON x3
add(68.58, 70.42, 'text', ['LE MEUBLE DE SALLE DE BAIN...'])
add(70.42, 70.84, 'text', ['TROP COMPLIQUÉ.'])
add(71.60, 72.24, 'text', ['LE MAÇON L’A FAIT.'])
add(72.42, 73.40, 'text', ['ON A VOULU PEINDRE.'])
add(73.40, 73.78, 'text', ['TROP COMPLIQUÉ.'])
add(74.08, 74.72, 'text', ['LE MAÇON L’A FAIT.'])
add(74.90, 76.16, 'text', ['ON A VOULU POSER LE PARQUET.'])
add(76.16, 76.64, 'text', ['TROP COMPLIQUÉ.'])
add(77.02, 77.66, 'text', ['LE MAÇON L’A FAIT.'])
add(78.04, 80.20, 'twocol', None)

# CHANGEMENTS D'AVIS rapide
_rapid_times = [80.20, 80.94, 81.68, 82.42, 82.98, 83.62, 84.26, 84.64, 85.30, 85.95,
                 86.20, 86.70, 87.16, 87.75, 88.32, 89.10, 89.88, 90.38, 91.36, 92.10]
for i in range(len(_rapid_times) - 1):
    add(_rapid_times[i], _rapid_times[i + 1], 'photo', nx(rapid_it))

# DEMENAGEMENT
add(92.46, 93.98, 'photo', nx(demenagement_it))
add(95.42, 96.36, 'photo', nx(demenagement_it))
add(96.56, 97.56, 'photo', nx(demenagement_it))
add(97.56, 98.77, 'photo', nx(demenagement_it))
add(98.77, 99.98, 'photo', nx(demenagement_it))
add(100.62, 102.56, 'photo', nx(demenagement_it))
add(103.02, 104.15, 'photo', nx(travaux_it))
add(104.15, 105.28, 'photo', nx(travaux_it))
add(105.52, 106.98, 'text', ['ILS ONT FAIT DES TROUS.', 'BEAUCOUP DE TROUS.'])

# PAS DE CUISINE
add(107.50, 109.16, 'photo', nx(travaux_it))
add(109.16, 110.42, 'text', ['ON A IMPROVISÉ.'])
add(110.42, 111.04, 'text', ['DES PÂTES.'])
add(111.04, 111.66, 'text', ['DES SANDWICHS.'])
add(111.66, 112.28, 'text', ['DES TRUCS.'])
add(112.48, 113.94, 'text', ['ON A ARRÊTÉ DE CUISINER.'])
add(113.94, 114.64, 'text', ['ON A JUSTE MANGÉ.'])

# REVELATION
add(114.84, 115.78, 'photo', nx(reveal_it))
add(116.36, 117.54, 'photo', nx(reveal_it))
add(117.74, 118.49, 'photo', nx(reveal_it))
add(118.49, 119.19, 'photo', nx(reveal_it))
add(119.19, 119.88, 'photo', nx(reveal_it))
add(119.88, 120.86, 'photo', nx(reveal_it))

# FIN
add(121.28, 122.92, 'photo', nx(ending_it))
add(123.58, 125.00, 'text', ['BREF.', 'ON A FAIT UNE CRÉMAILLÈRE. \U0001F942'])
add(125.38, 126.94, 'dark', None)
add(127.32, 128.90, 'text', ['FAIS ×2.'])

TOTAL_DURATION = 128.917333
