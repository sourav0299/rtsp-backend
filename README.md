# RTSP STREAM - BACKEND
Docker method
## Step 1
Install Dependency and running server
```bash
mdkdir rtsp-backend
cd rtsp-backend
git clone https://github.com/sourav0299/rtsp-backend.git .
docker build -t rtsp-backend .
docker run -p 8000:8000 rtsp-backend
```
Through Daphne
## Step 1
Setting up Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
## Step 2
Installation of dependency
```bash
pip install -r requirements.txt
```
## Step 3
Run server
```bash
daphne -p 8000 core.asgi:application
```
Major changes in streaming/consumers.py, core/asgi.py, core/settings.py
