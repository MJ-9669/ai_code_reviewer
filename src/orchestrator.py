import os
import json
from ingestion import clone_repository, cleanup_repository
from parser import ASTAnalyzer
from reviewer import CodeReviewer

# def analyze_git_repo(repo_url: str) -> list:

#     repo_path = None
#     all_review_comment = []
#     reviewer = CodeReviewer()

#     try:
#         repo_path = clone_repository(repo_url)






def analyze_git_repo(repo_url: str) -> list:
    repo_path = None
    all_review_comment = []
    reviewer = CodeReviewer()

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

                        for struct in structures:
                            print(f"  -> Sending {struct['type'].upper()} '{struct['name']}' to LLM Reviewer")

                            raw_reviews = reviewer.review_code_chunk(
                                file_name = relative_path,
                                chunk_type = struct["type"],
                                chunk_name = struct["name"],
                                code_content = struct["code"]
                            )
                            
                            for review in raw_reviews:
                                review["file"] = relative_path,
                                review["scope"] = struct["name"]

                                if review["line_number"] is not None:
                                    review["absolute_line"] = struct["start_line"] + review["line_number"] - 1
                                else:
                                    review["absolute_line"] = struct["start_line"]

                                all_review_comment.append(review)

                    except Exception as e:
                        print(f"Failed processing file context for {relative_path}: {e}")

        return all_review_comment
    
    finally:
        if repo_path:
            cleanup_repository(repo_path)

if __name__ == "__main__":

    test_repo = "https://github.com/psf/requests-html" 
    print("=== STARTING FULL AGENT CONTEXT TEST ===")
    results = analyze_git_repo(test_repo)
    
    print("\n=== AGGREGATED CODE REVIEW RESULTS ===")
    print(json.dumps(results, indent=2))