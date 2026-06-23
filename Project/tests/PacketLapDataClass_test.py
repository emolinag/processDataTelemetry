from packets.PacketLapDataClass import PacketLapDataClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex( 'A0 42 00 00 96 42 00 00 E8 03 D0 07 00 00 48 45 00 00 A0 45 00 00 40 40 03 05 01 00 01 00 00 00 00 00 02 01 02 00 00 00 00 00 00 ' + ' 00'*21*43 )

data = PacketLapDataClass(  bytes.fromhex( '00 ' *24 ), test_bytes )

print( f"m_lastLapTimeInMS : {data.m_lapData[0].m_lastLapTimeInMS}" )
print( f"m_currentLapTimeInMS : {data.m_lapData[0].m_currentLapTimeInMS}" )
print( f"m_sector1TimeInMS : {data.m_lapData[0].m_sector1TimeInMS}" )
print( f"m_sector2TimeInMS : {data.m_lapData[0].m_sector2TimeInMS}" )
print( f"m_lapDistance : {data.m_lapData[0].m_lapDistance}" )
print( f"m_totalDistance : {data.m_lapData[0].m_totalDistance}" )
print( f"m_safetyCarDelta : {data.m_lapData[0].m_safetyCarDelta}" )
print( f"m_carPosition : {data.m_lapData[0].m_carPosition}" )
print( f"m_currentLapNum : {data.m_lapData[0].m_currentLapNum}" )
print( f"m_pitStatus : {data.m_lapData[0].m_pitStatus}" )
print( f"m_numPitStops : {data.m_lapData[0].m_numPitStops}" )
print( f"m_sector : {data.m_lapData[0].m_sector}" )
print( f"m_currentLapInvalid : {data.m_lapData[0].m_currentLapInvalid}" )
print( f"m_penalties : {data.m_lapData[0].m_penalties}" )
print( f"m_warnings : {data.m_lapData[0].m_warnings}" )
print( f"m_numUnservedDriveThroughPens : {data.m_lapData[0].m_numUnservedDriveThroughPens}" )
print( f"m_numUnservedStopGoPens : {data.m_lapData[0].m_numUnservedStopGoPens}" )
print( f"m_gridPosition : {data.m_lapData[0].m_gridPosition}" )
print( f"m_driverStatus : {data.m_lapData[0].m_driverStatus}" )
print( f"m_resultStatus : {data.m_lapData[0].m_resultStatus}" )
print( f"m_pitLaneTimerActive : {data.m_lapData[0].m_pitLaneTimerActive}" )
print( f"m_pitLaneTimeInLaneInMS : {data.m_lapData[0].m_pitLaneTimeInLaneInMS}" )
print( f"m_pitStopTimerInMS : {data.m_lapData[0].m_pitStopTimerInMS}" )
print( f"m_pitStopShouldServePen : {data.m_lapData[0].m_pitStopShouldServePen}" )





