#!/usr/bin/env python3
"""Deploy MarketinAI backend to VPS via SSH/Paramiko."""
import argparse
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import paramiko

REMOTE_DIR = "/opt/marketinai-api"
STACK_NAME = "v10v-core_marketinai-api"


def make_tar_bytes(source_dir: Path) -> bytes:
    """Create a gzipped tar of source_dir excluding local artifacts."""
    excludes = {".venv", ".git", "__pycache__", "data", "logs", ".pytest_cache", "*.pyc"}
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for item in source_dir.iterdir():
            if item.name in excludes:
                continue
            arcname = item.name
            tar.add(item, arcname=arcname)
    return buf.getvalue()


def run_remote(client: paramiko.SSHClient, command: str, timeout: int = 60):
    print(f"\n$ {command}")
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    rc = stdout.channel.recv_exit_status()
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    if rc != 0:
        raise RuntimeError(f"Remote command failed with rc={rc}: {command}")
    return out, err


def main():
    parser = argparse.ArgumentParser(description="Deploy MarketinAI API")
    parser.add_argument("--host", default="72.61.193.34")
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", required=True)
    parser.add_argument("--source", default=str(Path(__file__).parent.resolve()))
    args = parser.parse_args()

    source_dir = Path(args.source)
    print(f"Packing {source_dir} ...")
    archive = make_tar_bytes(source_dir)
    print(f"Archive size: {len(archive) / 1024:.1f} KB")

    print(f"Connecting to {args.user}@{args.host} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=args.host, username=args.user, password=args.password, timeout=15)

    # Ensure remote directory and upload archive
    run_remote(client, f"mkdir -p {REMOTE_DIR}/data {REMOTE_DIR}/logs")
    sftp = client.open_sftp()
    remote_archive = f"{REMOTE_DIR}/deploy.tar.gz"
    print(f"Uploading archive to {remote_archive} ...")
    with sftp.file(remote_archive, "wb") as f:
        f.write(archive)

    # Extract and set permissions
    run_remote(client, f"cd {REMOTE_DIR} && tar -xzf deploy.tar.gz && rm deploy.tar.gz && chmod +x entrypoint.sh deploy.sh")

    # Upload .env only if missing
    env_exists = run_remote(client, f"test -f {REMOTE_DIR}/.env && echo yes || echo no")[0].strip()
    if env_exists != "yes":
        local_env = source_dir / ".env"
        if local_env.exists():
            print("Uploading .env (placeholders) ...")
            sftp.put(str(local_env), f"{REMOTE_DIR}/.env")
        else:
            print("No local .env found; remote .env must be created manually.")
    else:
        print("Remote .env already exists; keeping it.")

    sftp.close()

    # Docker Swarm deploy
    print("Checking Docker Swarm ...")
    try:
        run_remote(client, "docker info --format '{{.Swarm.ControlAvailable}}'")
    except Exception:
        print("Docker Swarm not active; attempting docker compose fallback ...")
        run_remote(client, f"cd {REMOTE_DIR} && docker compose up -d", timeout=120)
    else:
        print("Deploying stack marketinai ...")
        run_remote(client, f"cd {REMOTE_DIR} && docker stack deploy -c stack.yml {STACK_NAME}", timeout=120)

    # Health check
    print("Waiting for health check ...")
    import time
    time.sleep(8)
    try:
        run_remote(client, f"curl -fsS -L https://go.marketinai.net/api/marketinai/health")
        print(f"\nMarketinAI API is live at https://go.marketinai.net/api/marketinai/health")
    except Exception as exc:
        print(f"\nHealth check did not pass yet: {exc}", file=sys.stderr)
        print(f"Check logs with: ssh {args.user}@{args.host} 'docker service logs {STACK_NAME}_marketinai-api'", file=sys.stderr)

    client.close()


if __name__ == "__main__":
    main()
