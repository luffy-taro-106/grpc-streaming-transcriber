# client.py
from pydub import AudioSegment
from io import BytesIO
import grpc
import transcriber_pb2
import transcriber_pb2_grpc

def generate_chunks(file_path, chunk_length=10000):
    audio = AudioSegment.from_wav(file_path)
    for i in range(0, len(audio), chunk_length):
        chunk = audio[i:i + chunk_length]
        buffer = BytesIO()
        chunk.export(buffer, format="wav")
        buffer.seek(0)
        
        streamchunk = transcriber_pb2.AudioChunk()
        streamchunk.audio = buffer.read()
        buffer.close()
        yield streamchunk

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = transcriber_pb2_grpc.TranscriberStub(channel)

        responses = stub.StreamTranscribe(generate_chunks("output_mono.wav"))

        print("Streaming Transcription:")
        for response in responses:
            print(response.text)

if __name__ == "__main__":
    run()
