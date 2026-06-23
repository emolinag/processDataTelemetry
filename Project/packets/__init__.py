# Mejoras
# 1. Leer los datos por offset

# importando clases

from .HeaderClass import HeaderClass
from .PacketCarDamageDataClass import PacketCarDamageDataClass
from .PacketCarSetupDataClass import PacketCarSetupDataClass
from .PacketCarStatusDataClass import PacketCarStatusDataClass
from .PacketCarTelemetryDataClass import PacketCarTelemetryDataClass
from .PacketEventDataClass import PacketEventDataClass
from .PacketFinalClassificationDataClass import PacketFinalClassificationDataClass
from .PacketLapDataClass import PacketLapDataClass
from .PacketLobbyInfoDataClass import PacketLobbyInfoDataClass
from .PacketMotionDataClass import PacketMotionDataClass
from .PacketParticipantsDataClass import PacketParticipantsDataClass
from .PacketSessionDataClass import PacketSessionDataClass
from .PacketSessionHistoryDataClass import PacketSessionHistoryDataClass


# HeaderClass
# PacketCarDamageDataClass
# PacketCarSetupDataClass
# PacketCarStatusDataClass
# PacketCarTelemetryDataClass
# PacketEventDataClass
# PacketFinalClassificationDataClass
# PacketLapDataClass
# PacketLobbyInfoDataClass
# PacketMotionDataClass
# PacketParticipantsDataClass
# PacketSessionDataClass
# PacketSessionHistoryDataClass

# Session 1:
#   Track 1:
#       Lap 1:
#           Time
#           Sector1
#           Sector2
#           Sector3
#           Laps 1:
#           CarTelemetry 1:
#           CarSetup 1:1

# sessions {
#       id  : "",
#       fecini  : ""
#       fecfin  : ""
#       tracks : [  {
#                       id : "",
#                       name : "",
#                       laps : [{
#                               laps : [],
#                               car_setup : []
#                               car_telemetry : []
#                               motions : []
#                       },]
#                   },] 
# }

# Session es igual al anterior se mantiene de lo contrario se debe crear session nueva
#   Una session nueva implica
#       - Pista nueva


MAPPER = {
            0  : PacketMotionDataClass,
            1  : PacketSessionDataClass,
            2  : PacketLapDataClass,
            3  : PacketEventDataClass,
            4  : PacketParticipantsDataClass,
            5  : PacketCarSetupDataClass,
            6  : PacketCarTelemetryDataClass,
            7  : PacketCarStatusDataClass,
            8  : PacketFinalClassificationDataClass,
            9  : PacketLobbyInfoDataClass,
            10 : PacketCarDamageDataClass,
            11 : PacketSessionHistoryDataClass
         }


NATIONALITIES = {
    1  :   'American',
    2  :   'Argentinean',
    3  :   'Australian',
    4  :   'Austrian',
    5  :   'Azerbaijani',
    6  :   'Bahraini',
    7  :   'Belgian',
    8  :   'Bolivian',
    9  :   'Brazilian',
    10 :   'British',
    11 :   'Bulgarian',
    12 :   'Cameroonian',
    13 :   'Canadian',
    14 :   'Chilean',
    15 :   'Chinese',
    16 :   'Colombian',
    17 :   'Costa Rican',
    18 :   'Croatian',
    19 :   'Cypriot',
    20 :   'Czech',
    21 :   'Danish',
    22 :   'Dutch',
    23 :   'Ecuadorian',
    24 :   'English',
    25 :   'Emirian',
    26 :   'Estonian',
    27 :   'Finnish',
    28 :   'French',
    29 :   'German',
    30 :   'Ghanaian',
    31 :   'Greek',
    32 :   'Guatemalan',
    33 :   'Honduran',
    34 :   'Hong Konger',
    35 :   'Hungarian',
    36 :   'Icelander',
    37 :   'Indian',
    38 :   'Indonesian',
    39 :   'Irish',
    40 :   'Israeli',
    41 :   'Italian',
    42 :   'Jamaican',
    43 :   'Japanese',
    44 :   'Jordanian',
    45 :   'Kuwaiti',
    46 :   'Latvian',
    47 :   'Lebanese',
    48 :   'Lithuanian',
    49 :   'Luxembourger',
    50 :   'Malaysian',
    51 :   'Maltese',
    52 :   'Mexican',
    53 :   'Monegasque',
    54 :   'New Zealander',
    55 :   'Nicaraguan',
    56 :   'Northern Irish',
    57 :   'Norwegian',
    58 :   'Omani',
    59 :   'Pakistani',
    60 :   'Panamanian',
    61 :   'Paraguayan',
    62 :   'Peruvian',
    63 :   'Polish',
    64 :   'Portuguese',
    65 :   'Qatari',
    66 :   'Romanian',
    67 :   'Russian',
    68 :   'Salvadoran',
    69 :   'Saudi',
    70 :   'Scottish',
    71 :   'Serbian',
    72 :   'Singaporean',
    73 :   'Slovakian',
    74 :   'Slovenian',
    75 :   'South Korean',
    76 :   'South African',
    77 :   'Spanish',
    78 :   'Swedish',
    79 :   'Swiss',
    80 :   'Thai',
    81 :   'Turkish',
    82 :   'Uruguayan',
    83 :   'Ukrainian',
    84 :   'Venezuelan',
    85 :   'Barbadian',
    86 :   'Welsh',
    87 :   'Vietnamese'
}

TRACKS = {
    0   : 'Melbourne',
    1   : 'Paul Ricard',
    2   : 'Shanghai',
    3   : 'Bahrain', # 'Sakhir (Bahrain)',
    4   : 'Catalunya',
    5   : 'Monaco',
    6   : 'Montreal',
    7   : 'Silverstone',
    8   : 'Hockenheim',
    9   : 'Hungaroring',
    10  : 'Spa',
    11  : 'Monza',
    12  : 'Singapore',
    13  : 'Suzuka',
    14  : 'Abu Dhabi',
    15  : 'Texas',
    16  : 'Brazil',
    17  : 'Austria',
    18  : 'Sochi',
    19  : 'Mexico',
    20  : 'Baku (Azerbaijan)',
    21  : 'Sakhir Short',
    22  : 'Silverstone Short',
    23  : 'Texas Short',
    24  : 'Suzuka Short',
    25  : 'Hanoi',
    26  : 'Zandvoort',
    27  : 'Imola',
    28  : 'Portimão',
    29  : 'Jeddah'
}


def get_packet(packet_id , header, payload ) :
    # Función de conveniencia para instanciar la clase correcta
    if packet_id in MAPPER:
        return MAPPER[packet_id]( header, payload )
    return None