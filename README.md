# Canary gRPC Server

This is a streaming transcription system using gRPC. It takes audio chunks from the client and returns real-time transcriptions.

---

## 📦 Clone Canary Dependencies

This project uses NVIDIA's [NeMo](https://github.com/NVIDIA/NeMo) for speech recognition.

Please clone the NeMo repository inside your project directory:

```bash
git clone https://github.com/NVIDIA/NeMo.git
```

> 📝 Make sure it's cloned as a sibling folder inside the root directory (as shown in the file structure below).

---

## 🔧 Requirements

Install dependencies (after activating your virtual environment):

```bash
pip install -r requirements.txt
```

---

## 🛠️ Compile the .proto file

Make sure you're in the directory with `transcriber.proto`, then run:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. transcriber.proto
```

This generates:

- `transcriber_pb2.py`
- `transcriber_pb2_grpc.py`

---

## 🚀 Start the gRPC Server

Run the server with:

```bash
python server.py
```

---

## 🧪 Run the Client

Make sure the server is running first. Then in a separate terminal:

```bash
python client.py
```

---

## 📁 File Structure

```
.
├── NeMo/                     # NVIDIA's NeMo repo for ASR
├── output_mono.wav
├── client.py
├── server.py
├── transcriber.proto
├── transcriber_pb2.py
├── transcriber_pb2_grpc.py
├── requirements.txt
└── README.md
```

---
