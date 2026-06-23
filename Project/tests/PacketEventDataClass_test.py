from packets.PacketEventDataClass import PacketEventDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex( '00' )

data = PacketEventDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"len_payload : {data.len_payload()}" )







