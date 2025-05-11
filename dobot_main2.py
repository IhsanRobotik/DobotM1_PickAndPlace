import socket
ptpMode = dType.PTPMode.PTPMOVLXYZMode
dType.SetQueuedCmdStartExec(api)

pickingPointZ = 90
pickingPointR = 0
dropPoint = [71, 374, 90, 20]

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
    x, y, z, rHead = dropPoint
    dropIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]

    if socket_connected:
        while byte_sent == 0:
            byte_sent = sock.send('ok'.encode())
            print("sent ok")

        while byte_received == 0:
            byte_received = sock.recv(1024)
            coord_str = byte_received.decode().strip().strip("b'").strip("()")
            x_str, y_str = coord_str.split(',')
            rx = float(x_str)
            ry = float(y_str)
            print("received coordinates: ", rx, ry)

        # move to picking point
        x, y, z, rHead = pickingPoint
        pickIndex = dType.SetPTPCmd(api, ptpMode, x, y, z, rHead, isQueued=1)[0]
        
        byte_sent = 0
        byte_received = 0


    # Wait until the last queued command is executed
    while True:
        lastExecutedIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
        if lastExecutedIndex >= pickIndex:
            break
