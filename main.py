import socket
import server
import client



padding = '#'*10
print('\n%s Project 01 - Fragmentation and Control %s'%(padding,padding))
while(True):
    print('\n# EXECUTION MODE')
    print('> [S] SERVER Mode\n> [C] CLIENT Mode\n> [Q] Quit')
    mode = str(input('Enter the key: '))
    print('')

    if mode == 'S' or mode == 's':
        servidor = server.Server()
        servidor.listen("127.0.0.5", 8090)
        pass
    elif mode == 'C' or mode == 'c':
        cliente = client.Client()
        cliente.start() 
        pass
    elif mode == 'q' or mode == 'Q': break
    else: print('!!! Invalid key, try again.')
    pass