
import datetime
import json
import os
from pathlib import Path
import signal
import uuid
import secrets
import asyncio
import subprocess
from typing import Dict, List

from fastapi import FastAPI, Security, WebSocket, UploadFile, File, Form, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

origins = [
    "http://localhost:5173", # The hostname of the frontend, add to the exclusion list
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

running_processes: Dict[str, subprocess.Popen] = {}

projects = {

}

users = {
    
}

@app.get("/")
async def index():
    return {"status": "Service is up and Running!"}

def get_project(project_id: str, username: str):
    if username not in projects or project_id not in projects[username]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return projects[username][project_id]

def verify_token(token: str):
    try:
        for username, user_data in users.items():
            if user_data.get("api_key") == token:
                return username
            
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def get_current_username(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = users.get(username) # replace with you database query.
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return username

@app.post("/signup/")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username in users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {username} already exists.")
    hashed_password = pwd_context.hash(password)
    api_key = secrets.token_hex(16)
    users[username] = {"password_hash": hashed_password, "api_key": api_key}
    return {"message": "Signup successful", "api_key": api_key}


@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = users.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    correct_password = pwd_context.verify(password, user["password_hash"])
    if not correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    api_key = user["api_key"]
    return {"message": "Login successful", "api_key": api_key}

@app.get("/projects")
def get_user_projects(username: str = Depends(get_current_username)):
    user_projects = projects.get(username, {})

    if user_projects is None:
        return {"message": "User does not have any projects."}
    
    formatted_projects = []
    for project_id, project_data in user_projects.items():
        formatted_projects.append({
            "id": project_id,
            "name": project_data.get("name", {}),
            "description": project_data.get("description", ""),
            "lastUpdated": project_data.get("last_updated", ""),
            "devices": project_data.get("devices", []),
            "apkPath": project_data.get("apk_path", ""),
            "running_instances": project_data.get("running_instances")
        })
    return formatted_projects

@app.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_name: str = Form(...),
    project_description: str = Form(...),
    username: str = Depends(get_current_username)
):
    if username not in projects:
        projects[username] = {}

    if project_name in projects[username]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Project already exists")
    
    project_id = str(uuid.uuid4())
    projects[username][project_id] = {
        "name": project_name,
        "description": project_description,
        "last_updated": "",
        "devices": [],
        "apk_path": "",
        "running_instances": {},
    }
    return {"message": f"Project '{project_name}' created successfully", "id": project_id}

@app.put("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def update_project(
    project_id: str,
    project_name: str = Form(...),
    project_description: str = Form(...),
    username: str = Depends(get_current_username),
):
    if username not in projects or project_id not in projects[username]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    projects[username][project_id]["name"] = project_name
    projects[username][project_id]["description"] = project_description
    projects[username][project_id]["last_updated"] = datetime.datetime.now().isoformat()

    return  {"message": f"Project '{project_name}' updated successfully"}

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, username: str = Depends(get_current_username)):
    if username not in projects or project_id not in projects[username]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    del projects[username][project_id]
    return {"message": f"Project deleted."}

@app.post("/projects/{project_id}/devices/", status_code=status.HTTP_201_CREATED)
async def add_device(project_id: str, device_id: str = Form(...), username:str = Depends(get_current_username)):
    project = get_project(project_id, username)

    if device_id in project["devices"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Device already exists in project")
    
    project["devices"].append(device_id)
    project["last_updated"] = datetime.datetime.now().isoformat()

    return {"message": f"Device '{device_id}' added to project '{project.get('name', '')}'", "projectId": project_id}

@app.post("/projects/{project_id}/upload_apk/")
async def upload_apk(project_id: str, apk_file: UploadFile = File(...), username: str = Depends(get_current_username)):
    project = get_project(project_id, username)

    uploads_dir = f"uploads/{username}/{project_id}"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, apk_file.filename)

    with open(file_path, 'wb') as f:
        f.write(await apk_file.read())

    project["apk_path"] = file_path
    project["last_updated"] = datetime.datetime.now().isoformat()
    return {"filename": apk_file.filename, "path": file_path}

@app.post("/projects/{project_id}/run/{device_id}/")
async def run_droidbot(
    project_id: str,
    device_id: str,
    workflow_json: str = Form(...),
    username: str = Depends(get_current_username)
):
    project = get_project(project_id, username)
    
    if device_id not in project["devices"]:
        raise HTTPException(status_code=404, detail="Device not found in project.")
    if device_id in project["running_instances"]:
        raise HTTPException(status_code=409, detail=f"A Droidbot instance is already running on device {device_id}")
    
    
    try:
        workflow_data = json.loads(workflow_json)
        run_id = str(uuid.uuid4())
        output_dir = f"output/{run_id}"
        os.makedirs(output_dir, exist_ok=True)

        workflow_file_path = os.path.join(output_dir, "workflow.json")
        with open(workflow_file_path, "w") as f:
            json.dump(workflow_data, f, indent=4)

        command = ["python", "start.py", "-a", project["apk_path"], "-o", output_dir, "-workflow", workflow_file_path, "-keep_app", "-interval", "10"]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        project["last_updated"] = datetime.datetime.now().isoformat()
        project["running_instances"][device_id] = {"process": process, "run_id": run_id}
        return {"run_id": run_id}
    
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid workflow JSON"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
@app.post("/projects/{project_id}/stop/{device_id}/")
async def stop_droidbot(project_id: str, device_id: str, username: str = Depends(get_current_username)):

    project = get_project(project_id, username)  # Use helper function

    if device_id not in project["running_instances"]:
        raise HTTPException(status_code=404, detail="No Droidbot instance running on this device for this project")
    
    instance_data = project["running_instances"][device_id]
    process = instance_data["process"]

    try:
        os.kill(process.pid, signal.SIGTERM)
        process.wait()
        del project["running_instances"][device_id]
        project["last_updated"] = datetime.datetime.now().isoformat()

        return {"message": f"Scooper instance on {device_id} stopped successfully"}
    except ProcessLookupError:
        del project["running_instances"][device_id]
        return {"message": f"Scooper process on {device_id} was not found or has already finished."}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/output/{run_id}")
async def get_output(run_id: str):
    return StaticFiles(directory=f"output/{run_id}")

@app.get("/output/{run_id}/utg")
async def get_utg(run_id: str):
    try:
        utg_path = Path(f"output/{run_id}/utg.js")
        if not utg_path.exists():
            raise HTTPException(status_code=404, detail="UTG file not found")
        
        content = utg_path.read_text()
        json_str = content.replace("var utg = ", "").strip()
        utg_data = json.loads(json_str)

        base_url = f"/runs/{run_id}/states/"
        for node in utg_data["nodes"]:
            if "image" in node:
                # Convert Windows path to URL path
                image_name = node["image"].replace("states\\", "").replace("\\", "/")
                node["image"] = f"{base_url}{image_name}"
        return utg_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid UTG data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{username}/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str, username: str):
    await websocket.accept()
    try:
        process = None
        project_id = None
        device_id = None

        for project_id_iter, project_data in projects.get(username, {}).items():
            for device_id_iter, instance_data in project_data["running_instances"].items():
                if instance_data.get("run_id") == run_id:
                    process = instance_data["process"]
                    project_id = project_id_iter
                    device_id = device_id_iter
                    break
            if process:
                break

        if not process:
            await websocket.send_json({"error": "Invalid run_id or unauthorized access"})
            return
        
        async def send_output(stream):
            while True:
                line = await asyncio.to_thread(stream.readline)
                if not line:
                    break
                await websocket.send_text(line.decode())

        await asyncio.gather(send_output(process.stdout), send_output(process.stderr))

        returncode = process.wait()
        await websocket.send_json({"status": "completed", "return_code": returncode})

    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        if project_id and device_id and project_id in projects.get(username, {}) and device_id in projects[username][project_id]["running_instances"]:
            del projects[username][project_id]["running_instances"][device_id]


@app.on_event("startup")
async def startup_event():
    base_dir = Path("output")
    # Dynamically mount all run directories
    for run_dir in base_dir.glob("*"):
        if run_dir.is_dir():
            states_dir = run_dir / "states"
            if states_dir.exists():
                app.mount(
                    f"/runs/{run_dir.name}/states",
                    StaticFiles(directory=str(states_dir)),
                    name=f"states_{run_dir.name}"
                )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

