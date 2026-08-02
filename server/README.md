# Fabric 26.2 server

The server uses digest-pinned multi-architecture images with native Apple Silicon support:

- `itzg/minecraft-server:2026.7.2-java25@sha256:6ec1110…`
- `itzg/mc-backup:2026.7.3@sha256:e1b9133…`

## Start

From the repository root:

```bash
python3 tools/modpack.py materialize server build/server/mods --clean
[ -f server/.env ] || cp server/.env.example server/.env

mkdir -p server/secrets
[ -f server/secrets/rcon-password.txt ] || \
  openssl rand -base64 -out server/secrets/rcon-password.txt 32
[ -f server/secrets/restic-password.txt ] || \
  openssl rand -base64 -out server/secrets/restic-password.txt 32
chmod 600 server/secrets/*.txt

docker compose -f server/docker-compose.yml config --quiet
docker compose -f server/docker-compose.yml up -d
docker compose -f server/docker-compose.yml logs -f minecraft
```

The server is ready when the container becomes healthy and the log contains `Done`. RCON is available only to the internal Compose network; port `25575` is not published.

Never regenerate `restic-password.txt` while snapshots exist. A new password does not re-key the repository; it makes every existing snapshot inaccessible unless the old password is recovered.

## Incremental backups

The backup sidecar coordinates `save-off`, `save-all flush`, filesystem sync, Restic snapshot, then `save-on`. Restic snapshots are logically complete but physically content-deduplicated, so unchanged world data is not stored again.

Default retention keeps all snapshots for 48 hours, 14 daily, 8 weekly, and 12 monthly snapshots.

```bash
# Create an on-demand consistent snapshot.
docker compose -f server/docker-compose.yml exec backups backup now

# Inspect and verify the repository.
docker compose -f server/docker-compose.yml exec backups restic snapshots
docker compose -f server/docker-compose.yml exec backups restic check

# List this server's snapshots without starting Minecraft or creating a new backup.
docker compose -f server/docker-compose.yml run --rm --no-deps \
  --entrypoint restic backups snapshots --host minecraft-26-2 --path /data

# Replace this placeholder with an explicit ID from the list above.
snapshot_id=PUT_SNAPSHOT_ID_HERE
test ! -e "server/restore/$snapshot_id" && \
  docker compose -f server/docker-compose.yml run --rm --no-deps \
    --entrypoint restic backups restore "$snapshot_id" \
      --path /data --target "/restore/$snapshot_id"
```

Use a new restore directory for each attempt. Do not use `latest` during disaster recovery: starting the normal backup service first could snapshot an empty or damaged `/data` and make that bad state the newest one.

`server/backups/restic` protects from accidental deletion and world corruption, but not from loss of the Mac or its SSD. For disaster recovery, replicate this repository off-host or extend the Compose service with an S3/B2/rest-server repository and backend credentials; the checked-in profile intentionally stays local-only.

## Stop

```bash
docker compose -f server/docker-compose.yml down
```

The world remains in `server/data`; Restic snapshots remain in `server/backups/restic`.
