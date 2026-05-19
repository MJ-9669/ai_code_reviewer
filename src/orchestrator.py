import os
from ingestion import clone_repository, cleanup_repository
from parser import ASTAnalyzer

def run_pipeline(repo_url: str):
    repo_path = None
    try:
        repo_path = clone_repository(repo_url)

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, repo_path)

                    print(f"Processing file: {relative_path}")

                    try:
                        analyzer = ASTAnalyzer(full_path)
                        structures = analyzer.extract_structures()

                        if not structures:
                            print(f"No functions or class found")

                        for struct in structures:
                            print(f"Found {struct['type'].upper()} : {struct['name']} (Lines{struct['start_line']}-{struct['end_line']})")

                    except Exception as parse_error:
                        print(f"Could not parse {relative_path}:: {parse_error}")
    finally:
        if repo_path:
            cleanup_repository(repo_path)

if __name__ == "__main__":
    test_repo = "https://github.com/psf/requests-html" 
    run_pipeline(test_repo)