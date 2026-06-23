import sys
import os

# Añade la carpeta superior (Project) al sistema de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from packets.PacketCarTelemetryDataClass import PacketCarTelemetryDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex('1D 01 00 00 80 3F 00 00 00 00 00 00 00 00 00 08 EC2C 64 00 50 50 50 50 46 46 46 46 5A 03 00 00 A0 41 00 00 A0 41 00 00 A0 41 0000 A0 41 01 01 01 01' + ' 00'*1320 + ' 00 00 00' )

data = PacketCarTelemetryDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"speed : {data.m_carTelemetryData[0].m_speed}"  )
print( f"m_throttle : {data.m_carTelemetryData[0].m_throttle}"  )
print( f"m_steer : {data.m_carTelemetryData[0].m_steer}"  )
print( f"m_clutch : {data.m_carTelemetryData[0].m_clutch}"  )
print( f"m_gear : {data.m_carTelemetryData[0].m_gear}"  )
print( f"m_engineRPM : {data.m_carTelemetryData[0].m_engineRPM}"  )
print( f"m_brake : {data.m_carTelemetryData[0].m_brake}"  )
print( f"len payload : "  )
print( data.len_payload() )

