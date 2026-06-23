from packets.PacketSessionDataClass import PacketSessionDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex( '00 19 14 4E 60 0D 0A 11 00 E8 03 3C 00 64 00 00 00 00 00 00 00 00 00 00 00 80 3F 01 00' + ' 00' * 5 * 19 + '00 00 01 00 05 00 19 00 14 00 00' + ' 00' * 8 * 55 + '00 01 AA BB CC DD 01 00 00 00 01 00 00 00 01 05 02 01 01 01 01 01 01 00 00 00' )

data = PacketSessionDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"m_trackTemperature : {data.m_trackTemperature}" )
print( f"m_airTemperature : {data.m_airTemperature}" )
print( f"m_totalLaps : {data.m_totalLaps}" )
print( f"m_trackLength : {data.m_trackLength}" )
print( f"m_sessionType : {data.m_sessionType}" )







