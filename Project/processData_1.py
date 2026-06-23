from packets import *

packets = {
    0: 1464,    # Motion
    1: 625,     # Session
    2: 970,     # Lap Data
    3: 36,      # Event
    4: 1257,    # Participants
    5: 1102,    # Car Setups
    6: 1347,    # Car Telemetry
    7: 1058,    # Car Status
    8: 839,     # Final Classification
    9: 1191,    # Lobby Info
    10: 882,    # Car Damage
    11: 1155    # Session History
}

for i in range(12) :

    r = get_packet( i )
    # print( f"{r.__name__} - {r.len_payload(r)} - {packets[i]}" )
    if packets[i] - HeaderClass.len_payload(HeaderClass) != r.len_payload(r)  :
        print(f"Hay un error en {r.__name__} len payload : {packets[i] - HeaderClass.len_payload(HeaderClass)} leídos {r.len_payload(r)}")
    else :
        print(f"Clase {r.__name__} longitiud correcta : {r.len_payload(r)}")