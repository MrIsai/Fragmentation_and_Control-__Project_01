import socket
import sys
from server import ServerTCP
from client import ClientTCP

padding = '#'*10

print('\n%s Project 01 - Fragmentation and Control %s' % (padding, padding))
while True:
    print('# Choose the execution mode.')
    print('> [1] Server')
    print('> [2] Client')
    print('> [3] Quit')
    print('> [4] Info')
    tcp_mode = input('Enter the key number: ')

    if tcp_mode == "1":
        address = input('Enter the address (empty to use localhost): ')
        port = input('Enter the port (ej. "IP"): ')
        servidor = ServerTCP()
        servidor.listen(address, port)
        print('')
        pass
    elif tcp_mode == "2":
        print('\n# Enter to use default values *')
        path = input('Choose the image (ej. 500B.jpg): ')
        address = input('Enter the address to send image: ')
        port = input('Enter the port to send image (ej. "IP"): ')

        if len(port) == 0:
            print('\n!!! Insert a port\n') 
            continue
        cliente = ClientTCP()
        cliente.start(
            path=path if len(path) != 0 else '500B.jpg', 
            host=address if len(address) != 0 else 'localhost', 
            port=port )
        print('')
        pass
    elif tcp_mode == "3":
        print('\n# Process finished.\n')
        break
    elif tcp_mode == "4":
        print('\n# Information.')
        print(' * Isai Pashel')
        print(' * CC8')
        print(' * 2020 Year\n')
        pass
print(6*padding)