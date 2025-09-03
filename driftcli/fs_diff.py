import subprocess

def get_fs_diff(container_id):
    """Get filesystem changes in the container using docker diff."""
    result = subprocess.run(
        ["docker", "diff", container_id],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    changes = result.stdout.strip().split("\n")
    return [c for c in changes if c]  # filter empty lines
