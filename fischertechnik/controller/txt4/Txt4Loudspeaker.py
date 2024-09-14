import threading
import time


from ..Loudspeaker import Loudspeaker


class Txt4Loudspeaker(Loudspeaker):
    PATH_TO_SOUNDFILES = '/opt/ft/workspaces/sounds/'

    _repeat = False
    _running = False
    _stream = None
    _thread = None

    def __init__(self, controller):
        Loudspeaker.__init__(self, controller)

    def play(self, soundId, repeat, path=PATH_TO_SOUNDFILES):
        """@ParamType soundId int
        @ParamType repeat int"""
        if self._thread and self._thread.is_alive():
            self.stop()
            self._thread.join()

        self._running = True
        self._repeat = repeat

        self._thread = threading.Thread(target=self.__play, args=(soundId, path), daemon=True)
        self._thread.start()

    def is_playing(self):
        return self._running

    def set_volume(self, volume):
        """@ParamType volume int"""
        pass

    def get_volume(self):
        """@ReturnType int"""
        pass

    def stop(self):
        self._repeat = False
        self._running = False

    def __play(self, soundId, path):
        self.__stream(soundId, path)
        while self._repeat:
            self._running = True
            self.__stream(soundId, path)

    def __stream(self, soundId, path):
        # Import modules at time of need to decrease init time of controllerobject
        import pyaudio
        import wave

        py_audio = pyaudio.PyAudio()
        wf = wave.open(path + soundId, "rb")

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return data, pyaudio.paContinue

        self._stream = py_audio.open(format=py_audio.get_format_from_width(wf.getsampwidth()),
                                     channels=wf.getnchannels(),
                                     rate=wf.getframerate(), output=True, stream_callback=callback)
        self._stream.start_stream()
        while self._stream.is_active() and self._running:
            time.sleep(0.1)
        self._stream.stop_stream()
        self._stream.close()
        wf.close()
        py_audio.terminate()
        self._running = False
