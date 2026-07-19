"""Update META_ACCESS_TOKEN on VPS from local Cerebro V10/.env without exposing secrets."""
import paramiko
from pathlib import Path

LOCAL_ENV = Path("E:/Cerebro V10/.env")
REMOTE_ENV = "/opt/marketinai-api/.env"
KEY_PATH = "C:/Users/rober/.ssh/id_vps_cerebro"
HOST = "72.61.193.34"
USER = "root"
SERVICE = "v10v-core_marketinai-api_marketinai-api"

def main():
    token = None
    if LOCAL_ENV.exists():
        for line in LOCAL_ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith("META_ACCESS_TOKEN="):
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not token:
        print("ERROR: META_ACCESS_TOKEN not found in local .env")
        return 1

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    ssh.connect(HOST, username=USER, pkey=pkey, timeout=15)
    print("OK: connected to VPS")

    # Read remote .env
    stdin, stdout, stderr = ssh.exec_command(f"cat {REMOTE_ENV}")
    remote_lines = stdout.read().decode(errors="replace").splitlines()

    # Replace or append META_ACCESS_TOKEN
    new_lines = []
    found = False
    for line in remote_lines:
        if line.startswith("META_ACCESS_TOKEN="):
            new_lines.append(f"META_ACCESS_TOKEN={token}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"META_ACCESS_TOKEN={token}")
    new_content = "\n".join(new_lines) + "\n"

    # Write remote .env
    sftp = ssh.open_sftp()
    with sftp.file(REMOTE_ENV, "w") as f:
        f.write(new_content.encode("utf-8"))
    sftp.close()
    print("OK: remote .env updated")

    # Redeploy
    print("Forcing service redeploy...")
    stdin, stdout, stderr = ssh.exec_command(f"docker service update --force {SERVICE}", timeout=120)
    out = stdout.read().decode(errors="replace").strip()
    err = stderr.read().decode(errors="replace").strip()
    if out:
        print(out[-500:])
    if err:
        print("ERR:", err[-500:])

    # Health check
    print("Waiting for health check...")
    stdin, stdout, stderr = ssh.exec_command("sleep 6 && curl -fsS https://go.marketinai.net/api/marketinai/health")
    health = stdout.read().decode(errors="replace").strip()
    print("Health:", health)

    # Token validation (metadata only)
    stdin, stdout, stderr = ssh.exec_command(
        f"curl -sSL 'https://graph.facebook.com/debug_token?input_token={token}&access_token={token}' | "
        "python3 -c \"import sys,json; d=json.load(sys.stdin).get('data',{}); "
        "print('valid:', d.get('is_valid'), 'app:', d.get('app_id'), 'type:', d.get('type'), 'expires:', d.get('expires_at'))\""
    )
    validation = stdout.read().decode(errors="replace").strip()
    print("Token validation:", validation)

    ssh.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
