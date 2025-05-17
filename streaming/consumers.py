import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.ffmpeg_process = None

    async def disconnect(self, close_code):
        await self._stop_ffmpeg()

    async def receive(self, text_data):
        data = json.loads(text_data)
        rtsp_url = data.get('url')

        if not rtsp_url:
            await self.send(json.dumps({'error': 'RTSP URL not provided'}))
            return

        await self.send(json.dumps({"status": "Streaming started"}))

        await self._start_ffmpeg(rtsp_url)

    async def _start_ffmpeg(self, rtsp_url):
        if self.ffmpeg_process:
            await self._stop_ffmpeg()

        self.ffmpeg_process = await asyncio.create_subprocess_exec(
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', rtsp_url,
            '-f', 'mjpeg',
            '-q:v', '5',
            'pipe:1',
            stdout=asyncio.subprocess.PIPE,
            # stderr=asyncio.subprocess.PIPE  # Uncomment if you want to capture ffmpeg errors
            stderr=asyncio.subprocess.DEVNULL
        )

        buffer = bytearray()

        try:
            while True:
                chunk = await self.ffmpeg_process.stdout.read(4096)
                if not chunk:
                    break

                buffer.extend(chunk)

                while True:
                    start = buffer.find(b'\xff\xd8')  # SOI
                    end = buffer.find(b'\xff\xd9')    # EOI

                    if start == -1 or end == -1 or end <= start:
                        break

                    frame = buffer[start:end + 2]
                    buffer = buffer[end + 2:]
                    await self.send(bytes_data=bytes(frame))
        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))
        finally:
            await self._stop_ffmpeg()

    async def _stop_ffmpeg(self):
        if self.ffmpeg_process and self.ffmpeg_process.returncode is None:
            self.ffmpeg_process.kill()
            await self.ffmpeg_process.wait()
            self.ffmpeg_process = None
