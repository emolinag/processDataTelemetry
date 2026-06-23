import struct

class HeaderClass :

    sizeBytes = 24
    
    FORMAT = '<HBBBBQfIBB'

    FIELDS = [	
                'm_packetFormat',            # 2021
                'm_gameMajorVersion',        # Game major version - "X.00"
                'm_gameMinorVersion',        # Game minor version - "1.XX"
                'm_packetVersion',           # Version of this packet type,
                                             # all start from 1
                'm_packetId',                # Identifier for the packet type,
                                             # see below
                'm_sessionUID',              # Unique identifier for the session
                'm_sessionTime',             # Session timestamp
                'm_frameIdentifier',         # Identifier for the frame the data
                'm_playerCarIndex',          # Index of player's car in the array
                                             # was retrieved on
                'm_secondaryPlayerCarIndex'  # Index of secondary player's car in
                                             # the array (split-screen)
                                             # 255 if no second player
             ]
    
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload_data ) :
        # 2. Desempaquetamos los datos en una tupla
        unpacked_values = struct.unpack(self.FORMAT, payload_data[:self.sizeBytes])
        
        # 3. El Bucle de Asignación Automática
        # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
        for name, value in zip(self.FIELDS, unpacked_values):
            setattr(self, name, value)