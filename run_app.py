import subprocess
import time
import os
import sys
import webbrowser
import signal

def kill_process_on_port(port):
    """Kills any process listening on the specified port (Windows only)."""
    try:
        # Get PID of the process on the port
        cmd = f'netstat -ano | findstr :{port}'
        output = subprocess.check_output(cmd, shell=True).decode()
        for line in output.strip().split('\n'):
            if 'LISTENING' in line:
                pid = line.strip().split()[-1]
                print(f"Killing process {pid} on port {port}...")
                subprocess.run(['taskkill', '/F', '/T', '/PID', pid], capture_output=True)
    except Exception:
        pass

def start_backend(port):
    print(f"Starting Backend on port {port}...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "ai_assistant.backend.main:app", "--port", str(port), "--host", "0.0.0.0"])

def start_frontend(port):
    print(f"Starting Frontend on port {port}...")
    return subprocess.Popen(["streamlit", "run", "ai_assistant/frontend/app.py", "--server.port", str(port), "--browser.gatherUsageStats", "false", "--server.headless", "true"])

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    backend_port = int(os.getenv("PORT_BACKEND", 8600))
    frontend_port = int(os.getenv("PORT_FRONTEND", 3600))
    
    # Clean up old processes
    kill_process_on_port(backend_port)
    kill_process_on_port(frontend_port)
    
    backend_proc = start_backend(backend_port)
    time.sleep(3)  # Give backend time to start
    
    frontend_proc = start_frontend(frontend_port)
    time.sleep(2)
    
    print("\n" + "="*50)
    print("AI Document Assistant is starting!")
    print(f"Opening browser at http://localhost:{frontend_port}")
    print("="*50 + "\n")
    
    webbrowser.open(f"http://localhost:{frontend_port}")
    
    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend stopped unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend stopped unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nShutting down AI Assistant...")
    finally:
        # Cleanup
        if backend_proc.poll() is None:
            backend_proc.terminate()
        if frontend_proc.poll() is None:
            frontend_proc.terminate()
        
        # Force kill if needed
        kill_process_on_port(backend_port)
        kill_process_on_port(frontend_port)
        print("Done.")
