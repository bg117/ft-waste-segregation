import socket
import threading
import json
import time

class RemoteControl():

    BUFFERSIZE = 1024 * 4
    HOST = "0.0.0.0"
    IN_PORT = 10010
    OUT_PORT = 10011

    def __init__(self):

        self._stack = []
        self._listeners = []
        self._in_lock = threading.Lock()
        self._out_lock = threading.Lock()

        self._in_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._in_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._in_socket.bind((RemoteControl.HOST, RemoteControl.IN_PORT))
        self._in_socket.listen(1) 

        self._out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._out_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._out_socket.bind((RemoteControl.HOST, RemoteControl.OUT_PORT))
        self._out_socket.listen(1) 

        self._running = True
        self._in_thread = threading.Thread(target=self._recv, args=(), daemon=True)
        self._in_thread.start()

        self._out_thread = threading.Thread(target=self._send, args=(), daemon=True)
        self._out_thread.start()


    def __del__(self):
        
        self._running = False

        try:     
            if self._in_socket is not None:
                self._in_socket.shutdown()
                self._in_socket.close()
        except Exception as e:
            pass
        finally:
            self._in_socket = None

        try:     
            if self._out_socket is not None:
                self._out_socket.shutdown()
                self._out_socket.close()
        except Exception as e:
            pass
        finally:
            self._out_socket = None

        try:
            if self._in_thread is not None:
                self._in_thread.join()
        except Exception as e:
            pass
        finally:
            self._in_thread = None

        try:
            if self._out_thread is not None:
                self._out_thread.join()
        except Exception as e:
            pass
        finally:
            self._out_thread = None


    def set_attr(self, id, name, value):
        with self._out_lock:
            message = {"id": id, "attributes": [{"name": name, "value": value}]}
            self._stack.append(message)


    def add_listener(self, id, callback):
        with self._in_lock:
            listener = self._get_listener(id, callback)
            if listener is not None:
                return 
            self._listeners.append({
                "id": id,
                "callback": callback
            })


    def remove_listener(self, id, callback):
        with self._in_lock:   
            listener = self._get_listener(id, callback)
            if listener is None:
                return
            self._listeners.remove(listener)


    def _get_listener(self, id, callback):
        for listener in self._listeners:
            if listener["id"] == id and listener["callback"] == callback:
                return listener
        return None


    def _recv(self):

        while self._running:

             # keep accepting connections from clients
            conn, _ = self._in_socket.accept() 

            try:    

                full_msg = ''
                while True:
                    data = conn.recv(RemoteControl.BUFFERSIZE)
                    if len(data) <= 0:
                        break
                    full_msg += data.decode("utf-8")

                if len(full_msg) > 0:

                    message = json.loads(full_msg)
                
                    with self._in_lock:
                        for listener in self._listeners:
                            if listener["id"] == message["id"]:
                                # parse array of attributers to dictionary
                                attributes = {}
                                for attr in message["attributes"]:
                                    attributes[attr["name"]] = attr["value"]
                                listener["callback"](attributes)

            except Exception as e:
                self._running = False
            finally:
                conn.close()

    def _send(self):

        # keep accepting connections from clients
        conn, _ = self._out_socket.accept() 

        while self._running:

            try:    

                with self._out_lock:
                    message = json.dumps(self._stack)
                    conn.send(message.encode('utf-8'))
                    self._stack = []

                time.sleep(1)

            except Exception as e:
                conn, _ = self._out_socket.accept() 
