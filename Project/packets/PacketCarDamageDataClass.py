from .HeaderClass import HeaderClass

class PacketCarDamageDataClass :

    sizeBytes = 882
    
    FORMAT = ''
    
    FIELDS = [	
                'm_header'  # Header
             ]
    
    def len_payload( self ) :
        return self.sizeBytes - HeaderClass.sizeBytes
    
    def __init__ ( self, header, payload ) :
        
        setattr( self, self.FIELDS[0], header )