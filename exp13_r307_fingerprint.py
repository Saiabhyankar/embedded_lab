from pyfingerprint.pyfingerprint import PyFingerprint

f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

if not f.verifyPassword():
    raise ValueError('Fingerprint sensor password is incorrect')

print('Place finger on sensor...')

while not f.readImage():
    pass

f.convertImage(0x01)

result = f.searchTemplate()
positionNumber = result[0]
accuracyScore = result[1]

if positionNumber == -1:
    print('No match found')
else:
    print(f'Match found at position {positionNumber} with score {accuracyScore}')
