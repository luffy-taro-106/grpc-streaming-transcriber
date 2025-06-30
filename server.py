# server.py

import grpc #typed:ignore
from concurrent import futures
import transcriber_pb2
import transcriber_pb2_grpc

import torch #typed:ignore
from nemo.collections.asr.models import EncDecMultiTaskModel    #typed:ignore
import tempfile


class TranscriberServicer(transcriber_pb2_grpc.TranscriberServicer):
    def __init__(self):
        self.model = EncDecMultiTaskModel.from_pretrained('nvidia/canary-1b-flash')
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

    def StreamTranscribe(self, request_iterator, context):
        print("[Server] StreamTranscribe started")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            chunk_count = 0
            for chunk in request_iterator:
                chunk_count += 1
                print(f"[Server] Received chunk {chunk_count}, size: {len(chunk.audio)} bytes")

                tmpfile.write(chunk.audio)
                tmpfile.flush()
                print(f"[Server] Written chunk {chunk_count} to temp file: {tmpfile.name}")

                output = self.model.transcribe([tmpfile.name], batch_size=16, pnc='yes')
                transcription = output[0].text
                print(f"[Server] Transcription for chunk {chunk_count}: {transcription}")

                transcript = transcriber_pb2.Transcript(text=transcription)
                yield transcript
                print(f"[Server] Sent transcript for chunk {chunk_count}")
                tmpfile.seek(0)
                tmpfile.truncate()
                print(f"[Server] Cleared temp file for next chunk")

        print("[Server] StreamTranscribe finished")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    transcriber_pb2_grpc.add_TranscriberServicer_to_server(TranscriberServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Streaming Canary ASR gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
