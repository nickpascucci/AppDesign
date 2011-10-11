#! /usr/bin/env python

"""This is a Python file."""

__author__ = "Nick Pascucci (npascut1@gmail.com)"

from collections import namedtuple
import struct
import wave

frame = namedtuple("frame", ["channel", "amplitude"])

class FormatError(Exception):
    """General error class for format problems."""
    pass

class Wave(object):
    """Audio wave supporting normalization."""
    
    def __init__(self):
        self.audio = None
        self.frames = 0
        self.channels = 0
        self.sample_width = 0
        self.sample_rate = 0
        self.max_amplitude = 0

    def load(self, filename):
        """Read a wave object from a file.
        
        @param filename: The file to read from.
        """
        wv_read = wave.open(filename, "r")
        self.frames = wv_read.getnframes()
        self.channels = wv_read.getnchannels()
        parameters = wv_read.getparams()
        self.sample_width = parameters[1]
        self.sample_rate = parameters[2]
        self.max_amplitude = 0
        audio = wv_read.readframes(self.frames)
        self.audio = self._to_frames(audio)

    def save(self, filename):
        """Write the wave to a file.

        @param filename: The file to write to.
        """
        out_file = wave.open(filename, "w")
        out_file.setnchannels(self.channels)
        out_file.setsampwidth(self.sample_width)
        out_file.setframerate(self.sample_rate)
        data = self.raw()
        out_file.writeframes(data)

    def raw(self):
        """Get the value of this wave as a series of raw bytes.

        @return: A string containing the byte values.
        """
        encode = _get_encoder(self.sample_width)
        data = [encode(audio_frame.amplitude) for audio_frame in self.audio]
        return "".join(data)

    # Unfortunately, this method runs very slowly. There's probably a lot that
    # could be done to optimize it.
    def _to_frames(self, audio):
        """Convert a string containing audio data into a series of frames.

        @param audio: The audio data to encode.
        """
        frames = []
        decode = _get_decoder(self.sample_width)
        # We'll iterate over the audio string and extract each frame,
        # minding channels.
        curr_channel = 0
        for frame_num in range(0, len(audio), self.sample_width):
            sample_data = audio[frame_num:frame_num+self.sample_width]
            sample_amplitude = decode(sample_data)
            if abs(sample_amplitude) > self.max_amplitude:
                self.max_amplitude = abs(sample_amplitude)
            frames.append(frame(channel=curr_channel,
                                amplitude=sample_amplitude))
            curr_channel = (curr_channel + 1) % self.channels
        return frames

    def normalize(self):
        """Normalize the volume of the wave."""
        max_possible = float(_get_max_value(self.sample_width))
        scale_factor = max_possible/self.max_amplitude
        for index, audio_frame in enumerate(self.audio):
            normalized_amplitude = int(audio_frame.amplitude * scale_factor)
            if abs(normalized_amplitude) > self.max_amplitude:
                self.max_amplitude = abs(normalized_amplitude)
            self.audio[index] = frame(channel=audio_frame.channel,
                                      amplitude=normalized_amplitude)
            

def _get_max_value(num_bytes):
    """Get the maximum value representable in a two's complement integer."""
    if num_bytes == 1:
        return 255
    else:
        return 2 ** (8 * num_bytes - 1) - 1
        
def _get_decoder(sample_width):
    """Get a function to decode audio data."""
    # Implementation of both Factory and Strategy patterns.
    if sample_width == 1:
        return _decode_byte
    elif sample_width == 2:
        return _decode_short
    elif sample_width == 3:
        return _decode_int
    else:
        raise FormatError("Sample width not supported. Supported widths: 8bit,"
                          " 16bit, 32bit.")

def _decode_byte(sample_data):
    """Decode a single byte value."""
    return int(sample_data)

def _decode_short(sample_data):
    """Decode a two-byte signed short integer value."""
    return struct.unpack("<h", sample_data)[0]

def _decode_int(sample_data):
    """Decode a four-byte signed integer value."""
    return struct.unpack("<i", sample_data)[0]

def _get_encoder(sample_width):
    """Get a function to decode audio data."""
    # Implementation of both Factory and Strategy patterns.
    if sample_width == 1:
        return _encode_byte
    elif sample_width == 2:
        return _encode_short
    elif sample_width == 3:
        return _encode_int
    else:
        raise FormatError("Sample width not supported. Supported widths: 8bit,"
                          " 16bit, 32bit.")

def _encode_byte(sample_data):
    """Decode a single byte value."""
    return struct.pack("B", sample_data)

def _encode_short(sample_data):
    """Decode a two-byte signed short integer value."""
    return struct.pack("<h", sample_data)

def _encode_int(sample_data):
    """Decode a four-byte signed integer value."""
    return struct.pack("<i", sample_data)

def main():
    pass

if __name__ == "__main__":
    main()
