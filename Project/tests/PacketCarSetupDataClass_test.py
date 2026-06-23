from packets.PacketCarSetupDataClass import PacketCarSetupDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex( '06 04 4B 32 00 00 A0 41 00 00 20 41 00 00 80 3E 00 00 00 3F 02 07 02 07 03 07 64 3A 00 00 B0 41 00 00 B0 41 00 00 B8 41 00 00 B8 41 32 00 00 00 64' + ' 00'*1029 )

data = PacketCarSetupDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"m_frontWing : {data.m_carSetups[0].m_frontWing}"  )
print( f"m_rearWing : {data.m_carSetups[0].m_rearWing}"  )
print( f"m_onThrottle : {data.m_carSetups[0].m_onThrottle}"  )
print( f"m_offThrottle : {data.m_carSetups[0].m_offThrottle}"  )
print( f"m_frontCamber : {data.m_carSetups[0].m_frontCamber}"  )
print( f"m_rearCamber : {data.m_carSetups[0].m_rearCamber}"  )
print( f"m_frontToe : {data.m_carSetups[0].m_frontToe}"  )
print( f"m_rearToe : {data.m_carSetups[0].m_rearToe}"  )
print( f"m_frontSuspension : {data.m_carSetups[0].m_frontSuspension}"  )
print( f"m_rearSuspension : {data.m_carSetups[0].m_rearSuspension}"  )
print( f"m_frontAntiRollBar : {data.m_carSetups[0].m_frontAntiRollBar}"  )
print( f"m_rearAntiRollBar : {data.m_carSetups[0].m_rearAntiRollBar}"  )
print( f"m_frontSuspensionHeight : {data.m_carSetups[0].m_frontSuspensionHeight}"  )
print( f"m_rearSuspensionHeight : {data.m_carSetups[0].m_rearSuspensionHeight}"  )
print( f"m_brakePressure : {data.m_carSetups[0].m_brakePressure}"  )
print( f"m_brakeBias : {data.m_carSetups[0].m_brakeBias}"  )
print( f"m_rearLeftTyrePressure : {data.m_carSetups[0].m_rearLeftTyrePressure}"  )
print( f"m_rearRightTyrePressure : {data.m_carSetups[0].m_rearRightTyrePressure}"  )
print( f"m_frontLeftTyrePressure : {data.m_carSetups[0].m_frontLeftTyrePressure}"  )
print( f"m_frontRightTyrePressure : {data.m_carSetups[0].m_frontRightTyrePressure}"  )
print( f"m_ballast : {data.m_carSetups[0].m_ballast}"  )
print( f"m_fuelLoad : {data.m_carSetups[0].m_fuelLoad}"  )




