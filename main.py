import time

from server import server
from client import client
import multiprocessing as mp
import time

if __name__ == '__main__':
    data_queue_from_car = mp.Queue()
    data_queue_to_interface = mp.Queue()
    data_ready = mp.Event()
    quit_signal = mp.Event()
    server_proc = mp.Process(target=server, args=(data_queue_to_interface, data_ready, quit_signal))
    client_proc = mp.Process(target=client, args=(data_queue_from_car, quit_signal))
    server_proc.start()
    client_proc.start()
    while True:
        try:
            message = 'Test data: 0.9, 0.3\n'.encode('UTF-8')
            data_queue_from_car.put(message, False)
            print('Sent data from car to server', data_queue_from_car.qsize())
            while not data_ready.is_set():
                pass
            while not data_queue_to_interface.empty():
                data = data_queue_to_interface.get()
                print('Got from server to interface:', data_queue_to_interface.qsize(), data.decode('UTF-8'))
            time.sleep(0.2)
        except KeyboardInterrupt:
            quit_signal.set()
            print('Interrupt')
            break
    while not data_queue_to_interface.empty():
        data = data_queue_to_interface.get()
        print('Got from server to interface:', data_queue_to_interface.qsize(), data.decode('UTF-8'))
    server_proc.join()
    client_proc.join()
    print("End")