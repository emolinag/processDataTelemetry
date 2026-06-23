import struct
from .HeaderClass import HeaderClass

class LapDataClass :

    sizeBytes = 43
    
    FORMAT = '<IIHHfffBBBBBBBBBBBBBBHHB'

    FIELDS = [	
                'm_lastLapTimeInMS',	       	    # Last lap time in milliseconds
                'm_currentLapTimeInMS', 	        # Current time around the lap in milliseconds
                'm_sector1TimeInMS',                # Sector 1 time in milliseconds
                'm_sector2TimeInMS',                # Sector 2 time in milliseconds
                'm_lapDistance',		            # Distance vehicle is around current lap in metres – could
                                                    # be negative if line hasn’t been crossed yet
                'm_totalDistance',		            # Total distance travelled in session in metres – could
                                                    # be negative if line hasn’t been crossed yet
                'm_safetyCarDelta',                 # Delta in seconds for safety car
                'm_carPosition',   	                # Car race position
                'm_currentLapNum',		            # Current lap number
                'm_pitStatus',            	        # 0 = none, 1 = pitting, 2 = in pit area
                'm_numPitStops',            	    # Number of pit stops taken in this race
                'm_sector',               	        # 0 = sector1, 1 = sector2, 2 = sector3
                'm_currentLapInvalid',    	        # Current lap invalid - 0 = valid, 1 = invalid
                'm_penalties',            	        # Accumulated time penalties in seconds to be added
                'm_warnings',                       # Accumulated number of warnings issued
                'm_numUnservedDriveThroughPens',    # Num drive through pens left to serve
                'm_numUnservedStopGoPens',          # Num stop go pens left to serve
                'm_gridPosition',         	        # Grid position the vehicle started the race in
                'm_driverStatus',         	        # Status of driver - 0 = in garage, 1 = flying lap
                                                    # 2 = in lap, 3 = out lap, 4 = on track
                'm_resultStatus',                   # Result status - 0 = invalid, 1 = inactive, 2 = active
                                                    # 3 = finished, 4 = didnotfinish, 5 = disqualified
                                                    # 6 = not classified, 7 = retired
                'm_pitLaneTimerActive',     	    # Pit lane timing, 0 = inactive, 1 = active
                'm_pitLaneTimeInLaneInMS',   	    # If active, the current time spent in the pit lane in ms
                'm_pitStopTimerInMS',        	    # Time of the actual pit stop in ms
                'm_pitStopShouldServePen'   	    # Whether the car should serve a penalty at this stop
             ]
    
    def len_payload( self ) :
        return self.sizeBytes
    
    def __init__ ( self, payload_data ) :
    
        try :
        
            offset = 0
            
            unpacked_values = struct.unpack_from( self.FORMAT, payload_data, offset )
            offset += self.sizeBytes
            
            for name, value in zip(self.FIELDS, unpacked_values):
                setattr(self, name, value)
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")
            
            
            
            
            
class PacketLapDataClass :

    sizeBytes = 970
    
    FORMAT = ''
    

    FIELDS = [	
                'm_header', # Header
                'm_lapData'   # Lap data for all cars on track
             ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
        
        self.m_lapData = []
    
        try :
            
            offset = 0
    
            setattr(self, self.FIELDS[0], header )
        
            for i in range(22):
                self.m_lapData.append( LapDataClass( payload[offset:offset+LapDataClass.sizeBytes] ) )
                offset += LapDataClass.sizeBytes
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")