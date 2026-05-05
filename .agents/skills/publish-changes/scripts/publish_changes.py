import subprocess
import datetime
import sys
import os

def run_command(command, cwd=None):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def main():
    # 1. Verify changes exist
    status = run_command(["git", "status", "--porcelain"])
    if not status:
        print("No changes to publish.")
        return

    # 2. Prepare branch name
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    branch_name = f"publish-{date_str}"
    
    print(f"Targeting branch: {branch_name}")

    # 3. Create and switch to new branch
    run_command(["git", "checkout", "-b", branch_name])

    # 4. Add and Commit
    run_command(["git", "add", "."])
    commit_msg = "Standardizing Modular Skill Architecture and Final Sync"
    run_command(["git", "commit", "-m", commit_msg])

    # 5. Push to origin
    run_command(["git", "push", "origin", branch_name])

    # 6. Create Pull Request
    pr_title = f"Standardize Skills and Localization - {date_str}"
    pr_body = "Automated PR: Standardizing modular skill architecture, normalizing Spanish translations, and syncing site data."
    
    pr_url = run_command([
        "gh", "pr", "create",
        "--title", pr_title,
        "--body", pr_body,
        "--head", branch_name
    ])

    if pr_url:
        print(f"PR Created: {pr_url}")
        
        # 7. Merge PR
        print("Attempting to merge PR...")
        # Use --auto --merge to merge as soon as checks pass
        merge_result = run_command(["gh", "pr", "merge", "--merge", "--delete-branch", "--auto"])
        if merge_result:
            print("Successfully set PR to auto-merge.")
        else:
            print("Auto-merge failed. You can check status with 'gh pr status'")
    else:
        print("Failed to create PR.")

if __name__ == "__main__":
    main()
