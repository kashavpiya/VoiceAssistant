#This script will collect data for the wake word training

import pyaudio
import wave
import argparse
import time
import os


class Listener:

    def __init__(self, args):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.channels = 1
        self.sampleRate = args.sample_rate
        self.record_seconds = args.seconds

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.channels,
                                  rate=self.sampleRate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk)

    def save_audio(self, file_name, frames):
        print("saving the file to {}".format(file_name))
        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()

        wf = wave.open(file_name, "wb") #open as write bytes
        wf.setnchannels(self.channels)
        wf.setsamplewidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.sampleRate)
        wf.writeframes(b"".join(frames))
        wf.close()

def interactive(args):
    index = 0
    try:
        while True:
            listener = Listener(args)
            frames = []
            print('begin recording....')
            input('press enter to continue. the recoding will be {} seconds. press ctrl + c to exit'.format(args.seconds))
            time.sleep(0.2)
            for i in range(int((listener.sampleRate/listener.chunk)* listener.record_seconds)):
                data = listener.stream.read(listener.chunk, exception_on_overflow=False)
                frames.append(data)
            save_path = os.path.join(args.interactive_save_path, "{}.wav".format(index))
            listener.save_audio(save_path, frames)
            index += 1
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    except Exception as e:
        print(str(e))


def main(args):
    listener = Listener(args)
    frames = []
    print("recording")
    try:
        while True:
            if listener.record_seconds == None:
                print("Recording until Ctrl + C is pressed", end="\r")
                data = listener.stream.read(listener.chunk)
                frames.append(data)
            else:
                for i in range(int((listener.sampleRate/listener.chunk) * listener.record_seconds)):
                    data = listener.stream.read(listener.chunk)
                    frames.append(data)
                raise Exception('done recording')
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
    except Exception as e:
        print(str(e))

    print('finish recording...')
    listener.save_audio(args.save_path, frames)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Script to collect data for wake word training.''')

    parser.add_argument('--sample_rate', type=int, default=8000, help='the samplerate to record at')
    parser.add_argument('--seconds', type=int, default=None, help='if set to None, then will record forever until keyboard interrupt')
    parser.add_argument('--save_path', type=str, default=None, required=False, help='full path to save file. i.e. /to/path/sound.wav')
    parser.add_argument('--interactive_save_path', type=str, default=None, required=False, help='directory to save all the interactive 2 second samples. i.e. /to/path/')
    parser.add_argument('--interactive', default=False, action='store_true', required=False, help='sets to interactive mode')

    args = parser.parse_args()

    if args.interactive:
        if args.interactive_save_path is None:
            raise Exception('need to set --interactive_save_path')
        interactive(args)
    else:
        if args.save_path is None:
            raise Exception('Need to set --save_path')
        main(args)