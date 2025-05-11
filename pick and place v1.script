import socket
ptpMode = dType.PTPMode.PTPMOVLXYZMode
dType.SetQueuedCmdStartExec(api)

pickingPointZ = 90
pickingPointZDescend = 52
pickingPointR = 0

dropPointZ = 90
dropPointZDescend = 20
dropPointHeightStep = 10
dropPointR = 0

rx = 0
ry = 0
pickingPoint = [rx, ry, pickingPointZ, pickingPointR]

byte_sent = 0
byte_received = 0

# socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(('localhost', 9238))
    socket_connected = True
except:
    print("Could not connect to socket. Continuing without server.")
    socket_connected = False


while True:
    # Move to dropping point
    x, y, z, rHead = 71, 374, dropPointZ, dropPointR
    dropIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

    # Move to dropping point descend
    x, y, z, rHead = 71, 374, dropPointZDescend, dropPointR
    dropIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]	

    # Set output 17 to OFF (release)
    dType.SetIODO(api, 17, 1, isQueued=1)
    dType.dSleep(500)

    # Move to dropping point
    x, y, z, rHead = 71, 374, dropPointZ, dropPointR
    dropIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

    # Wait until the robot finishes moving to drop point
    while True:
        lastExecutedIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
        if lastExecutedIndex >= dropIndex:
            break

    if socket_connected:
        while byte_sent == 0:
            byte_sent = sock.send('ok'.encode())
            print("sent ok")

        while byte_received == 0:
            byte_received = sock.recv(1024)
            coord_str = byte_received.decode().strip().strip("b'").strip("()")
            x_str, y_str, r_str = coord_str.split(',')
            rx = float(x_str)
            ry = float(y_str)
            pickingPointR =  float(r_str)

            print("received coordinates: ", rx, ry, pickingPointR)

            dropPointZDescend += dropPointHeightStep

        # move to picking point
        x, y, z, rHead = rx, ry, pickingPointZ, pickingPointR
        pickIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

        # move to picking point dascend
        x, y, z, rHead = rx, ry, pickingPointZDescend, pickingPointR
        pickIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

        # Set output 17 to OFF (release)
        dType.SetIODO(api, 17, 0, isQueued=1)
        dType.dSleep(2000)

        # move to picking point
        x, y, z, rHead = rx, ry, pickingPointZ, pickingPointR
        pickIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

        byte_sent = 0
        byte_received = 0

    # Wait until the robot finishes moving to pick point
    while True:
        lastExecutedIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
        if lastExecutedIndex >= pickIndex:
            break
