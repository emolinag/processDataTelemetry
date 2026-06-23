from packets.HeaderClass import HeaderClass

# Los bytes que confirmamos: E5 07 (2021), 01 (Major), 12 (18 Minor), 01 (PacketID)
# Rellenamos con ceros hasta llegar a los 24 bytes
test_bytes = bytes.fromhex('E5 07 01 12 01 00 00 00 FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00')

header = HeaderClass(test_bytes)

print(f"¿Formato es 2021?: {header.m_packetFormat == 2021}")
print(f"¿Packet ID es 1?: {header.m_packetId == 0}")
print(f"¿Minor Version es 18?: {header.m_gameMinorVersion == 18}")