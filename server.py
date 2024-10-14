import socket
from multiprocessing import Queue
from multiprocessing import Event


def server(output_queue: Queue, output_event: Event, quit_event: Event):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 5000))
    while True:
        try:
            if quit_event.is_set():
                break
            data, address = server_socket.recvfrom(1024)
            if len(data) > 0:
                output_queue.put(data)
                output_event.set()
                print('Server: received data from client', output_queue.qsize())
        except KeyboardInterrupt:
            break

    print('Server stopped')
    server_socket.close()
