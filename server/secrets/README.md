# Docker secrets

Create two local files before the first `docker compose up`:

```bash
mkdir -p server/secrets
[ -f server/secrets/rcon-password.txt ] || \
  openssl rand -base64 -out server/secrets/rcon-password.txt 32
[ -f server/secrets/restic-password.txt ] || \
  openssl rand -base64 -out server/secrets/restic-password.txt 32
chmod 600 server/secrets/*.txt
```

Both `*.txt` files are ignored by Git. Preserve the Restic password somewhere outside this repository: without it, snapshots cannot be restored. Never replace it while a repository exists; generating a new password does not re-key old snapshots.
