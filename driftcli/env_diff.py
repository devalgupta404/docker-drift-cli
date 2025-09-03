import subprocess, json

def get_env(container_or_image):
    """Fetch environment variables from a container or image."""
    result = subprocess.run(
        ["docker", "inspect", container_or_image, "--format", "{{json .Config.Env}}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    return json.loads(result.stdout.strip() or "[]")

def compare_env(container_id, image_name):
    """Compare env vars between container and image."""
    container_env = get_env(container_id)
    image_env = get_env(image_name)

    container_set = set(container_env)
    image_set = set(image_env)

    added = container_set - image_set
    removed = image_set - container_set
    modified = []

    for env in (container_set & image_set):
        key = env.split("=")[0]
        c_val = next((e.split("=",1)[1] for e in container_env if e.startswith(key+"=")), None)
        i_val = next((e.split("=",1)[1] for e in image_env if e.startswith(key+"=")), None)
        if c_val != i_val:
            modified.append((key, i_val, c_val))

    return {"added": list(added), "removed": list(removed), "modified": modified}
