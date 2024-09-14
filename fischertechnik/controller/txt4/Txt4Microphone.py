import threading
import time
from math import log10

from ..Microphone import Microphone


class Txt4Microphone(Microphone):

    CHUNK = 4096
    volume = 0

    __running = False
    __thread = None
    __stream = None
    __py_audio = None

    def __init__(self, controller, identifier):
        Microphone.__init__(self, controller, identifier)

    def start(self):
        if self.__thread and self.__thread.is_alive():
            self.stop()
        self.__running = True
        self.__thread = threading.Thread(target=self.__measure_volume)
        self.__thread.start()
        
    def stop(self):
        if self.__thread is None:
            return
        self.__running = False
        self.__thread.join()
        self.__stream.stop_stream()
        self.__stream.close()
        self.__py_audio.terminate()
        self.__thread = None

    def get_volume(self):
        return self.volume

    def __measure_volume(self):
        # Import modules at time of need to decrease init time of controllerobject
        import pyaudio
        import audioop

        self.__py_audio = pyaudio.PyAudio()

        # Select correct index, rate and channels value
        index=-1
        rate=44100
        channels=2
        for i in range(self.__py_audio.get_device_count()):
           dinfo = self.__py_audio.get_device_info_by_index(i)
           max_channels = dinfo["maxInputChannels"]
           if max_channels > 0 and dinfo["name"].startswith("USB"):
               if max_channels < channels:
                   channels = max_channels
               index = i
               rate = int(dinfo["defaultSampleRate"])
               break

        self.__stream = self.__py_audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=index
        )
        
        while self.__stream.is_active() and self.__running:
            data = self.__stream.read(self.CHUNK)
            self.volume = self.__rms_to_db(audioop.rms(data, 2))
            time.sleep(0.01)

    def __rms_to_db(self, rms):
        # Code from fischertechnik
        # https://gitlab.com/fischertechnik/TxtROBOPro/blob/master/ROBOProLib/Microphone.cppSound
        return 20 * log10(rms + 8.5)
