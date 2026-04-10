import subprocess
import os
import sys
import time

def main():
    # Render assigns the main entry port to the 'PORT' environment variable
    # This is where external traffic will be routed.
    frontend_port = os.getenv("PORT", "10000")
    
    # We assign an internal port for the backend (FastAPI)
    backend_port = "8000"
    
    # Let the frontend know where the backend is via environment variables
    # The Streamlit frontend looks for PORT_BACKEND
    os.environ["PORT_BACKEND"] = backend_port
    
    print(f"Starting Backend on internal port {backend_port}...")
    backend_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "ai_assistant.backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", backend_port
    ])
    
    # Give the backend a few seconds to initialize its Database and AI components
    time.sleep(4)
    
    print(f"Starting Frontend on Render's external port {frontend_port}...")
    frontend_proc = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", 
        "ai_assistant/frontend/app.py",
        "--server.port", frontend_port,
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true"
    ])
    
    try:
        # Wait for the frontend to complete or fail
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down processes...")
    finally:
        # Ensure cleanup of both processes
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
