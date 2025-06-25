import uvicorn
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).absolute().parent.parent))

if __name__ == "__main__":
    uvicorn.run("routers.main:app", host="0.0.0.0", port=4001, reload=True)
