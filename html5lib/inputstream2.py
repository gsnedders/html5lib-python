from codecs import getincrementaldecoder
from io import TextIOBase, UnsupportedOperation

class ChangeableEncodingStream(TextIOBase):
    """A text IO type that support changing encoding"""
    def __init__(self, buffer, encoding=None, detectEncoding=None,
                 errors=None):
        # Detect encoding if we have to
        if encoding is None and detectEncoding is not None:
            encoding, remaining = detectEncoding(buffer)
        else:
            remaining = None

        # Set properties on obj
        self.buffer = buffer
        self.decoder = None
        self._encoding = encoding
        self._errors = errors if errors is not None else "strict"
        self.remaining = remaining
        self.rawChunks = []
        self.chunkStates = [(b"", 0)]
        self.chunkLengths = []
        self.currentChunk = -1
        self.chunkSize = 512
        self.decodedChunk = None
        self.decodedChunkOffset = 0

        # Create initial decoder
        if encoding:
            self.decoder = getincrementaldecoder(encoding)(self._errors)

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, v):
        newDecoder = getincrementaldecoder(v)(self._errors)

        if self.rawChunks:
            assert self.decodedChunkOffset > 0
            self.decoder.setstate(self.chunkStates[self.currentChunk])
            currentChunk = self.rawChunks[self.currentChunk]
            charCount = 0
            byteCount = 0
            for byte in currentChunk:
                charCount += len(self.decoder.decode(byte))
                byteCount += 1
                if charCount >= self.decodedChunkOffset:
                    break
            self.decoded = newDecoder.decode(currentChunk[byteCount:], False)
            self.decodedChunkOffset = 0
        else:
            self.decoded = None
            self.decodedChunkOffset = 0

        self.decoder = newDecoder

    @property
    def errors(self):
        return self._errors
    
    @errors.setter
    def errors(self, v):
        # XXX: this somehow needs to handle the case where it is set
        # before the encoding (and hence we have no encoding)
        self.decoder.errors = v

    @property
    def newlines(self):
        raise UnsupportedOperation()

    def detach(self):
        buffer = self.buffer
        self.buffer = None
        return buffer

    def read(self, n=-1):
        if n is None or n < 0:
            n = float("Infinity")

        data = []
        remaining = n

        # Read what we can from the current chunk
        chunk = self.decodedChunk
        if chunk:
            offset = self.decodedChunkOffset
            remainderOfChunk = len(chunk) - offset
            if remaining < remainderOfChunk:
                data.append(chunk[offset:offset + remaining])
                self.decodedChunkOffset += remaining
                remaining = 0
            else:
                data.append(chunk[offset:])
                self.decodedChunkOffset += remainderOfChunk
                remaining -= remainderOfChunk

        # Read more data
        chunkOffset = self.chunkOffset
        chunkNumber = self.chunkNumber
        chunkSize = self.chunkSize
        while remaining > 0:
            readBytes = self.buffer.read(chunkSize)
            if readBytes == 0:
                decoded = self.decoder(b"", True)
            else:
                decoded = self.decoder(readBytes, False)
            self.rawChunks.append(readBytes)
            self.chunkStates.append(self.decoder.getstate())
            self.chunkLengths.append(len(decoded))
            self.currentChunk += 1
            self.decodedChunk = decoded
            if remaining < len(decoded):
                data.append(decoded[:remaining])
                remaining = 0
                self.decodedChunkOffset = remaining
            else:
                data.append(decoded)
                remaining -= len(decoded)
                self.decodedChunkOffset = len(decoded)

        # Eventually we have enough data
        assert n == float("Infinity") or sum(map(len, data)) == n
        return "".join(data)

    def readline(self, limit):
        # TODO: this
        pass

    def seek(self, offset, whence):
        # TODO: this
        pass

    def tell(self):
        return (sum(self.chunkLengths[:self.currentChunk]) +
                self.decodedChunkOffset)
