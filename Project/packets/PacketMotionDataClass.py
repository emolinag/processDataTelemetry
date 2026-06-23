import struct
from .HeaderClass import HeaderClass

class CarMotionDataClass :

    sizeBytes = 60
    
    FORMAT = '<ffffffHHHHHHffffff'

    FIELDS = [	
                'm_worldPositionX',           # World space X position
                'm_worldPositionY',           # World space Y position
                'm_worldPositionZ',           # World space Z position
                'm_worldVelocityX',           # Velocity in world space X
                'm_worldVelocityY',           # Velocity in world space Y
                'm_worldVelocityZ',           # Velocity in world space Z
                'm_worldForwardDirX',         # World space forward X direction (normalised)
                'm_worldForwardDirY',         # World space forward Y direction (normalised)
                'm_worldForwardDirZ',         # World space forward Z direction (normalised)
                'm_worldRightDirX',           # World space right X direction (normalised)
                'm_worldRightDirY',           # World space right Y direction (normalised)
                'm_worldRightDirZ',           # World space right Z direction (normalised)
                'm_gForceLateral',            # Lateral G-Force component
                'm_gForceLongitudinal',       # Longitudinal G-Force component
                'm_gForceVertical',           # Vertical G-Force component
                'm_yaw',                      # Yaw angle in radians
                'm_pitch',                    # Pitch angle in radians
                'm_roll'                      # Roll angle in radians
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
            


class PacketMotionDataClass :

    sizeBytes = 1464
    
    FORMAT = '<'+'f'*30

    FIELDS = [
                'm_header',                 # Header
                'm_carMotionData',         # Data for all cars on track
                                            # Extra player car ONLY data
                'm_suspensionPosition',     # Note: All wheel arrays have the following order:
                'm_suspensionVelocity',     # RL, RR, FL, FR
                'm_suspensionAcceleration', # RL, RR, FL, FR
                'm_wheelSpeed',             # Speed of each wheel
                'm_wheelSlip',              # Slip ratio for each wheel
                'm_localVelocityX',         # Velocity in local space
                'm_localVelocityY',         # Velocity in local space
                'm_localVelocityZ',         # Velocity in local space
                'm_angularVelocityX',       # Angular velocity x-component
                'm_angularVelocityY',       # Angular velocity y-component
                'm_angularVelocityZ',       # Angular velocity z-component
                'm_angularAccelerationX',   # Angular velocity x-component
                'm_angularAccelerationY',   # Angular velocity y-component
                'm_angularAccelerationZ',   # Angular velocity z-component
                'm_frontWheelsAngle'        # Current front wheels angle in radians
             ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
    
        try :
            # 2. Desempaquetamos los datos en una tupla
            
            offset = 0
            
            setattr(self, self.FIELDS[0], header )
            
            setattr(self, self.FIELDS[1], [] )

            for i in range(22):
                self.m_carMotionData.append( CarMotionDataClass( payload[ offset: offset + CarMotionDataClass.sizeBytes ] ) )
                offset += CarMotionDataClass.sizeBytes
                
            unpacked_values = struct.unpack_from( self.FORMAT, payload, offset )
            offset += struct.calcsize( self.FORMAT )
            
            for j, i in zip( [ 0, 4, 8, 12, 16 ], [ 2, 3, 4, 5, 6 ] ): 
                setattr( self, self.FIELDS[i], list( unpacked_values[ j:j+4 ] ) )
            
            # 3. El Bucle de Asignación Automática
            # zip() combina nombres con valores: [('packet_format', 2021), ('packet_id', 1)...]
            for name, value in zip(self.FIELDS[7:], unpacked_values[ 7 : ] ):
                setattr( self, name, value )
            
            if offset != self.len_payload() :
                raise validatePayload( f"Se espera {self.len_payload()} y se leyó {offset}" )
        
        except validatePayload as e :
            print( f"{self.__class__.__name__}::Oops, longitud de payload errado: {e}")