import os
import stat 
import shutil
from sys import prefix
import tempfile
from git import Repo

def clone_repository(repo_url:str) -> str:
    try:
        target_dir = tempfile.mkdtemp(prefix = "agent_review_")
        print(f"Cloning repository {repo_url} into {target_dir}")

        repo = Repo.clone_from(repo_url, target_dir)
        repo.close()

        print("Clone successful")
        return target_dir
    
    except Exception as e:
        print(f"!! Error cloning repository:: {e}")
        raise e
    
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def cleanup_repository(dir_path : str):
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path, onexc = remove_readonly)
            print(f"Cleaned up directory : {dir_path}")
        
        except TypeError:
            shutil.rmtree(dir_path, onerror=remove_readonly)
            print(f"Cleaned up directory : {dir_path}")