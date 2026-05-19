import os
import shutil
from sys import prefix
import tempfile
from git import Repo

def clone_repository(repo_url:str) -> str:
    try:
        target_dir = tempfile.mkdtemp(prefix - "agent_review_")
        print(f"Cloning repository {repo_url} into {target_dir}")

        Repo.clone_from(repo_url, target_dir)
        print("[+] Clone successful")
        return target_dir
    
    except Exception as e:
        print(f"[-] Error cloning repository:: {e}")
        raise e
    
def cleanup_repository(dir_path :str):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"[+] Cleaned up directory {dir_path}")