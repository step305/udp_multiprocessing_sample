import socket
from multiprocessing import Queue
from multiprocessing import Event
import queue


def client(input_queue: Queue, quit_event: Event):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    address = ('127.0.0.1', 5000)

    while True:
        try:
            if quit_event.is_set():
                break
            try:
                data = input_queue.get(True, 0.5)
                client_socket.sendto(data, address)
                print('Client: sent data to server', input_queue.qsize())
            except queue.Empty:
                pass
        except KeyboardInterrupt:
            break

    print('Client stopped')
    client_socket.close()
