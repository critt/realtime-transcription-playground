import asyncio

import socketio
from aiohttp import web

from settings import BACKEND_PORT
from google_speech_wrapper import GoogleSpeechWrapper

app = web.Application()
routes = web.RouteTableDef()

@routes.get('/getSupportedLanguages')
async def get_supported_languages(request):
    return web.json_response(GoogleSpeechWrapper.get_supported_languages())

@routes.get('/detectLanguage')
async def detect_language(request):
    text = request.query['text']
    return web.json_response(GoogleSpeechWrapper.detect_language(text))

app.add_routes(routes)

# Bind our Socket.IO server to our web app instance
sio = socketio.AsyncServer(cors_allowed_origins=[])  # * is bad
sio.attach(app)

# Define the SubjectNamespace
@sio.on('connect', namespace='/subject')
async def connect_subject(sid, environ):
    print(f'Client connected to /subject: {sid}')

@sio.on('disconnect', namespace='/subject')
async def disconnect_subject(sid):
    print(f'Client disconnected from /subject: {sid}')

@asyncio.coroutine
@sio.on('startGoogleCloudStream', namespace='/subject')
async def start_google_stream_subject(sid, config):
    print(f'Starting streaming audio data from client {sid} on /subject')
    await GoogleSpeechWrapper.start_recognition_stream(sio, sid, config, '/subject')

@sio.on('binaryAudioData', namespace='/subject')
async def receive_binary_audio_data_subject(sid, message):
    GoogleSpeechWrapper.receive_data(sid, message)

@sio.on('endGoogleCloudStream', namespace='/subject')
async def close_google_stream_subject(sid):
    print(f'Closing streaming data from client {sid} on /subject')
    await GoogleSpeechWrapper.stop_recognition_stream(sid)

# Define the ObjectNamespace
@sio.on('connect', namespace='/object')
async def connect_object(sid, environ):
    print(f'Client connected to /object: {sid}')

@sio.on('disconnect', namespace='/object')
async def disconnect_object(sid):
    print(f'Client disconnected from /object: {sid}')

@asyncio.coroutine
@sio.on('startGoogleCloudStream', namespace='/object')
async def start_google_stream_object(sid, config):
    print(f'Starting streaming audio data from client {sid} on /object')
    await GoogleSpeechWrapper.start_recognition_stream(sio, sid, config, '/object')

@sio.on('binaryAudioData', namespace='/object')
async def receive_binary_audio_data_object(sid, message):
    GoogleSpeechWrapper.receive_data(sid, message)

@sio.on('endGoogleCloudStream', namespace='/object')
async def close_google_stream_object(sid):
    print(f'Closing streaming data from client {sid} on /object')
    await GoogleSpeechWrapper.stop_recognition_stream(sid)


web.run_app(app, port=BACKEND_PORT)