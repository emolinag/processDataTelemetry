from packets.PacketMotionDataClass import PacketMotionDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex( '00 00 48 44 00 00 00 00 00 00 7A 44 00 00 10 42 00 00 00 00 00 00 20 42 00 00 00 00 FF 7F 00 00 00 00 FF 7F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00' + ' 00'*21*60 + ' 00' * 120 )

data = PacketMotionDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"m_worldPositionX : {data.m_carMotionData[0].m_worldPositionX}" )

print( f"m_worldPositionX : {data.m_carMotionData[0].m_worldPositionX}")
print( f"m_worldPositionY : {data.m_carMotionData[0].m_worldPositionY}")
print( f"m_worldPositionZ : {data.m_carMotionData[0].m_worldPositionZ}")
print( f"m_worldVelocityX : {data.m_carMotionData[0].m_worldVelocityX}")
print( f"m_worldVelocityY : {data.m_carMotionData[0].m_worldVelocityY}")
print( f"m_worldVelocityZ : {data.m_carMotionData[0].m_worldVelocityZ}")
print( f"m_worldForwardDirX : {data.m_carMotionData[0].m_worldForwardDirX}")
print( f"m_worldForwardDirY : {data.m_carMotionData[0].m_worldForwardDirY}")
print( f"m_worldForwardDirZ : {data.m_carMotionData[0].m_worldForwardDirZ}")
print( f"m_worldRightDirX : {data.m_carMotionData[0].m_worldRightDirX}")
print( f"m_worldRightDirY : {data.m_carMotionData[0].m_worldRightDirY}")
print( f"m_worldRightDirZ : {data.m_carMotionData[0].m_worldRightDirZ}")
print( f"m_gForceLateral : {data.m_carMotionData[0].m_gForceLateral}")
print( f"m_gForceLongitudinal : {data.m_carMotionData[0].m_gForceLongitudinal}")
print( f"m_gForceVertical : {data.m_carMotionData[0].m_gForceVertical}")
print( f"m_yaw : {data.m_carMotionData[0].m_yaw}")
print( f"m_pitch : {data.m_carMotionData[0].m_pitch}")
print( f"m_roll : {data.m_carMotionData[0].m_roll}")