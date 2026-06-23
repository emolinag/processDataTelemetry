from .HeaderClass import HeaderClass

class ParticipantDataClass :

    sizeBytes = 56

    FORMAT = '<BBBBBBB' + 's'*56 + 'B'
    
    FIELDS = [	
                'm_aiControlled',   # Whether the vehicle is AI (1) or Human (0) controlled
                'm_driverId',		# Driver id - see appendix, 255 if network human
                'm_networkId',		# Network id – unique identifier for network players
                'm_teamId',         # Team id - see appendix
                'm_myTeam',         # My team flag – 1 = My Team, 0 = otherwise
                'm_raceNumber',     # Race number of the car
                'm_nationality',    # Nationality of the driver
                'm_name',           # Name of participant in UTF-8 format – null terminated
                                    # Will be truncated with … (U+2026) if too long
                'm_yourTelemetry'   # The player's UDP setting, 0 = restricted, 1 = public
             ]
             
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload ) :
    
        try : 
        
            offset = 0
        
            setattr( self, self.FIELDS[0], payload )
            
            unpacked_values = struct.unpack_from( self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS[ 0 : 7 ], unpacked_values):
                setattr(self, name, value)
            
            setattr( self, name, unpacked_values[:-1] )
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")




class PacketParticipantsDataClass :

    sizeBytes = 1257
    
    FORMAT = '<B'
    
    FIELDS = [	
                'm_header',         # Header
                'm_numActiveCars',  # Number of active cars in the data – should match number of
                'm_participants'    # cars on HUD
             ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
        
        try :
            offset = 0
            
            self.m_participants = 0
        
            setattr( self, self.FIELDS[0], header )
            
            unpacked_values = struct.unpack_from( self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            setattr(self, name, unpacked_values[0] )
            
            for i in range(22) :
                self.m_participants.append( ParticipantDataClass( payload[offset:offset+ParticipantDataClass.sizeBytes ] ) )
                offset += ParticipantDataClass.sizeBytes
                
        
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")