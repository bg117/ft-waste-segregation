import socket
import threading

class VoiceControl():

    BUFFERSIZE = 1024
    HOST = '0.0.0.0'
    PORT = 12345

    def __init__(self):
        self._command = None
        self._callbacks = []
        self._lock = threading.Lock()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((VoiceControl.HOST, VoiceControl.PORT))
        self._socket.listen(1)

        self._running = True
        self._thread = threading.Thread(target=self._establish_connection, args=(), daemon=True)
        self._thread.start()


    def __del__(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
        if self._socket is not None:
            self._socket.close()


    def get_command(self):
        if self._command is not None:
            with self._lock:
                return self._command
        return ''


    def add_command_listener(self, callback):
        if callback in self._callbacks:
            return
        self._callbacks.append(callback)


    def remove_command_listener(self, callback):
        if callback not in self._callbacks:
            return
        self._callbacks.remove(callback)


    def _establish_connection(self):
        while self._running:
            conn, _ = self._socket.accept()
            try:           
                full_msg = ''
                # receive data from the client
                while True:
                    msg = conn.recv(VoiceControl.BUFFERSIZE)
                    if len(msg) <= 0:
                        break
                    full_msg += msg.decode("utf-8")

                if len(full_msg) > 0: 
                    with self._lock:
                        self._command = full_msg
                    # executes callbacks
                    for callback in self._callbacks:
                        callback(full_msg) 
            except Exception as e:
                pass
            finally:
                conn.close()
