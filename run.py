import os
import sys
from pathlib import Path
import uvicorn

# إضافة مسار ai_dev_academy إلى PYTHONPATH لضمان استمراريتها مع SpawnProcess
BASE_DIR = Path(__file__).resolve().parent
ACADEMY_DIR = BASE_DIR / "ai_dev_academy"

os.environ["PYTHONPATH"] = str(ACADEMY_DIR) + os.pathsep + os.environ.get("PYTHONPATH", "")

if str(ACADEMY_DIR) not in sys.path:
    sys.path.insert(0, str(ACADEMY_DIR))

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(ACADEMY_DIR)
    )