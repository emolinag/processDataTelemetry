import struct
from .HeaderClass import HeaderClass

class MarshalZoneClass :

    sizeBytes = 5
    
    FORMAT = '<fB'

    FIELDS = [	
                'm_zoneStart',   # Fraction (0..1) of way through the lap the marshal zone starts
                'm_zoneFlag'     # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red    
             ]
    
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload ) :
    
        try : 
            offset = 0
            
            # 2. Desempaquetamos los datos en una tupla
            unpacked_values = struct.unpack_from(self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS, unpacked_values):
                setattr(self, name, value)
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
 

 
            
class WeatherForecastSampleClass :

    sizeBytes = 8
    
    FORMAT = '<BBBBBBBB'

    FIELDS = [	
                'm_sessionType',              # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1
                                              # 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2
                                              # 12 = Time Trial
                'm_timeOffset',               # Time in minutes the forecast is for
                'm_weather',                  # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                              # 3 = light rain, 4 = heavy rain, 5 = storm
                'm_trackTemperature',         # Track temp. in degrees Celsius
                'm_trackTemperatureChange',   # Track temp. change – 0 = up, 1 = down, 2 = no change
                'm_airTemperature',           # Air temp. in degrees celsius
                'm_airTemperatureChange',     # Air temp. change – 0 = up, 1 = down, 2 = no change
                'm_rainPercentage'            # Rain percentage (0-100)
             ]
    
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload ) :
        
        try :
            offset = 0
        
            # 2. Desempaquetamos los datos en una tupla
            unpacked_values = struct.unpack_from( self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS, unpacked_values):
                setattr(self, name, value)
                
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
            
            
            
class PacketSessionDataClass :

    sizeBytes = 625
    
    FORMATS = [
                '<BbbBHBbBHHBBBBBB',
                '<BBB',
                '<BBIIIBBBBBBBBBBBB'
              ]
              
    FORMAT = '<BbbBHBbBHHBBBBBBBBBBBIIIBBBBBBBBBBBB'
    
    m_marshalZones = []
    m_weatherForecastSamples = []

    FIELDS = [	
                'm_header',               	   # Header               

                'm_weather',              	   # Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                               # 3 = light rain, 4 = heavy rain, 5 = storm
                'm_trackTemperature',    	   # Track temp. in degrees celsius
                'm_airTemperature',      	   # Air temp. in degrees celsius
                'm_totalLaps',           	   # Total number of laps in this race
                'm_trackLength',           	   # Track length in metres
                'm_sessionType',         	   # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P
                                               # 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ
                                               # 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
                'm_trackId',         		   # -1 for unknown, 0-21 for tracks, see appendix
                'm_formula',                   # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2,
                                               # 3 = F1 Generic
                'm_sessionTimeLeft',    	   # Time left in session in seconds
                'm_sessionDuration',     	   # Session duration in seconds
                'm_pitSpeedLimit',      	   # Pit speed limit in kilometres per hour
                'm_gamePaused',                # Whether the game is paused
                'm_isSpectating',        	   # Whether the player is spectating
                'm_spectatorCarIndex',  	   # Index of the car being spectated
                'm_sliProNativeSupport',	   # SLI Pro support, 0 = inactive, 1 = active
                'm_numMarshalZones',           # Number of marshal zones to follow
                'm_marshalZones',         	   # List of marshal zones – max 21
                'm_safetyCarStatus',           # 0 = no safety car, 1 = full
                                               # 2 = virtual, 3 = formation lap
                'm_networkGame',               # 0 = offline, 1 = online
                'm_numWeatherForecastSamples', # Number of weather samples to follow
                'm_weatherForecastSamples',    # Array of weather forecast samples
                'm_forecastAccuracy',          # 0 = Perfect, 1 = Approximate
                'm_aiDifficulty',              # AI Difficulty rating – 0-110
                'm_seasonLinkIdentifier',      # Identifier for season - persists across saves
                'm_weekendLinkIdentifier',     # Identifier for weekend - persists across saves
                'm_sessionLinkIdentifier',     # Identifier for session - persists across saves
                'm_pitStopWindowIdealLap',     # Ideal lap to pit on for current strategy (player)
                'm_pitStopWindowLatestLap',    # Latest lap to pit on for current strategy (player)
                'm_pitStopRejoinPosition',     # Predicted position to rejoin at (player)
                'm_steeringAssist',            # 0 = off, 1 = on
                'm_brakingAssist',             # 0 = off, 1 = low, 2 = medium, 3 = high
                'm_gearboxAssist',             # 1 = manual, 2 = manual & suggested gear, 3 = auto
                'm_pitAssist',                 # 0 = off, 1 = on
                'm_pitReleaseAssist',          # 0 = off, 1 = on
                'm_ERSAssist',                 # 0 = off, 1 = on
                'm_DRSAssist',                 # 0 = off, 1 = on
                'm_dynamicRacingLine',         # 0 = off, 1 = corners only, 2 = full
                'm_dynamicRacingLineType'      # 0 = 2D, 1 = 3D
             ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
    
        try :
        
            offset = 0
    
            setattr( self, self.FIELDS[0], header )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            
            unpacked_values = struct.unpack_from( self.FORMATS[0], payload, offset )
            offset += struct.calcsize( self.FORMATS[0] )
            
            for name, value in zip(self.FIELDS[1:17], unpacked_values):
                setattr(self, name, value)
                
            for i in range(21):
                self.m_marshalZones.append( MarshalZoneClass( payload[offset:offset+MarshalZoneClass.sizeBytes] ) )
                offset += MarshalZoneClass.sizeBytes
                
                
            unpacked_values = struct.unpack_from( self.FORMATS[1], payload, offset )
            offset += struct.calcsize( self.FORMATS[1] )
            
            for name, value in zip(self.FIELDS[18:21], unpacked_values ):
                setattr( self, name, value)
                
            for i in range(56):
                self.m_weatherForecastSamples.append( WeatherForecastSampleClass( payload[offset:offset+WeatherForecastSampleClass.sizeBytes] ) )
                offset += WeatherForecastSampleClass.sizeBytes
                
            unpacked_values = struct.unpack_from( self.FORMATS[2], payload, offset )
            offset += struct.calcsize( self.FORMATS[2] )
            
            for name, value in zip(self.FIELDS[22:], unpacked_values ):
                setattr(self, name, value)
                
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
            