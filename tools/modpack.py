#!/usr/bin/env python3
"""Build, verify, or materialize the locked Fabric 26.2 modpack."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "pack" / "mods.lock.json"
INDEX_PATH = ROOT / "pack" / "modrinth.index.json"
RELEASE_PATH = ROOT / "release" / "devformed-fabric-26.2.mrpack"
USER_AGENT = "devformed-minecraft-server/26.2 modpack materializer"
ENV_VALUES = {"required", "optional", "unsupported"}


class PackError(RuntimeError):
    pass


def read_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise PackError(f"cannot read {path}: {exc}") from exc


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def expected_index(lock: dict) -> dict:
    files = []
    for artifact in lock["artifacts"]:
        files.append(
            {
                "path": artifact["path"],
                "hashes": {
                    "sha1": artifact["hashes"]["sha1"],
                    "sha512": artifact["hashes"]["sha512"],
                },
                "env": artifact["env"],
                "downloads": [artifact["downloadUrl"]],
                "fileSize": artifact["fileSize"],
            }
        )
    return {
        "formatVersion": 1,
        "game": "minecraft",
        "versionId": lock["versionId"],
        "name": lock["name"],
        "summary": lock["summary"],
        "files": files,
        "dependencies": {
            "fabric-loader": lock["runtime"]["fabricLoader"],
            "minecraft": lock["runtime"]["minecraft"],
        },
    }


def validate_lock(lock: dict) -> None:
    if lock.get("schemaVersion") != 1:
        raise PackError("unsupported lock schemaVersion")
    artifacts = lock.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise PackError("lock has no artifacts")

    paths: set[str] = set()
    mod_ids: set[str] = set()
    kinds = {"requested": 0, "replacement": 0, "dependency": 0}
    for artifact in artifacts:
        path = artifact.get("path", "")
        if not path.startswith("mods/") or Path(path).name != path.removeprefix("mods/"):
            raise PackError(f"unsafe artifact path: {path!r}")
        if path in paths:
            raise PackError(f"duplicate path: {path}")
        paths.add(path)

        mod_id = artifact.get("modId", "")
        if not mod_id or mod_id in mod_ids:
            raise PackError(f"missing or duplicate mod id: {mod_id!r}")
        mod_ids.add(mod_id)

        kind = artifact.get("kind")
        if kind not in kinds:
            raise PackError(f"invalid kind for {mod_id}: {kind!r}")
        kinds[kind] += 1

        env = artifact.get("env", {})
        if set(env) != {"client", "server"} or not set(env.values()) <= ENV_VALUES:
            raise PackError(f"invalid environment for {mod_id}: {env!r}")

        download = artifact.get("downloadUrl", "")
        if not download.startswith("https://"):
            raise PackError(f"non-HTTPS download for {mod_id}")
        if not isinstance(artifact.get("fileSize"), int) or artifact["fileSize"] <= 0:
            raise PackError(f"invalid file size for {mod_id}")

        hashes = artifact.get("hashes", {})
        if len(hashes.get("sha1", "")) != 40 or len(hashes.get("sha512", "")) != 128:
            raise PackError(f"invalid hashes for {mod_id}")
        try:
            int(hashes["sha1"], 16)
            int(hashes["sha512"], 16)
        except ValueError as exc:
            raise PackError(f"non-hex hash for {mod_id}") from exc

    artifacts_by_id = {artifact["modId"]: artifact for artifact in artifacts}
    for artifact in artifacts:
        missing = sorted(set(artifact.get("requires", [])) - mod_ids)
        if missing:
            raise PackError(f"{artifact['modId']} has missing dependencies: {', '.join(missing)}")
        for side in ("client", "server"):
            if artifact["env"][side] == "unsupported":
                continue
            unavailable = sorted(
                dependency
                for dependency in artifact.get("requires", [])
                if artifacts_by_id[dependency]["env"][side] == "unsupported"
            )
            if unavailable:
                raise PackError(
                    f"{artifact['modId']} is enabled on {side}, but its dependencies are not: "
                    + ", ".join(unavailable)
                )

    declared = lock.get("counts", {})
    actual = {
        "requested": kinds["requested"],
        "replacements": kinds["replacement"],
        "dependencies": kinds["dependency"],
        "totalFiles": len(artifacts),
    }
    if declared != actual:
        raise PackError(f"count mismatch: declared={declared}, actual={actual}")


def validate_index(lock: dict, index: dict) -> None:
    expected = expected_index(lock)
    if index != expected:
        raise PackError("pack/modrinth.index.json is stale relative to pack/mods.lock.json")


def verify_release(index: dict) -> None:
    if not RELEASE_PATH.is_file():
        raise PackError(f"release archive is missing: {RELEASE_PATH}")
    try:
        with zipfile.ZipFile(RELEASE_PATH) as archive:
            names = archive.namelist()
            if names != ["modrinth.index.json"]:
                raise PackError(f"unexpected mrpack entries: {names}")
            packed_index = json.loads(archive.read("modrinth.index.json"))
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        raise PackError(f"invalid release archive: {exc}") from exc
    if packed_index != index:
        raise PackError("release archive contains a stale index")


def build_release(lock: dict, index: dict) -> None:
    validate_lock(lock)
    validate_index(lock, index)
    RELEASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=RELEASE_PATH.parent,
        prefix=f".{RELEASE_PATH.name}.",
        suffix=".part",
        delete=False,
    ) as temporary_stream:
        temporary = Path(temporary_stream.name)
    info = zipfile.ZipInfo("modrinth.index.json", date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            archive.writestr(info, canonical_json(index))
        temporary.replace(RELEASE_PATH)
    finally:
        temporary.unlink(missing_ok=True)
    verify_release(index)
    digest = file_hashes(RELEASE_PATH)["sha256"]
    print(f"built {RELEASE_PATH.relative_to(ROOT)} ({RELEASE_PATH.stat().st_size} bytes, sha256 {digest})")


def file_hashes(path: Path) -> dict[str, str]:
    digests = {name: hashlib.new(name) for name in ("sha1", "sha256", "sha512")}
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            for digest in digests.values():
                digest.update(chunk)
    return {name: digest.hexdigest() for name, digest in digests.items()}


def verify_artifact(path: Path, artifact: dict) -> None:
    if not path.is_file():
        raise PackError(f"missing artifact: {path}")
    if path.stat().st_size != artifact["fileSize"]:
        raise PackError(f"size mismatch: {path.name}")
    hashes = file_hashes(path)
    for algorithm in ("sha1", "sha512"):
        if hashes[algorithm] != artifact["hashes"][algorithm]:
            raise PackError(f"{algorithm} mismatch: {path.name}")
    try:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member:
                raise PackError(f"broken ZIP member in {path.name}: {bad_member}")
            metadata = json.loads(archive.read("fabric.mod.json"))
    except (zipfile.BadZipFile, KeyError, json.JSONDecodeError) as exc:
        raise PackError(f"invalid Fabric JAR {path.name}: {exc}") from exc
    if metadata.get("id") != artifact["modId"]:
        raise PackError(
            f"mod id mismatch for {path.name}: expected {artifact['modId']!r}, got {metadata.get('id')!r}"
        )


def download_artifact(destination: Path, artifact: dict) -> None:
    request = urllib.request.Request(artifact["downloadUrl"], headers={"User-Agent": USER_AGENT})
    with tempfile.NamedTemporaryFile(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".part",
        delete=False,
    ) as temporary_stream:
        temporary = Path(temporary_stream.name)
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        verify_artifact(temporary, artifact)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def materialize(lock: dict, side: str, destination: Path, allow_extra: bool) -> None:
    validate_lock(lock)
    selected = [artifact for artifact in lock["artifacts"] if artifact["env"][side] != "unsupported"]
    destination.mkdir(parents=True, exist_ok=True)
    expected_names = {Path(artifact["path"]).name for artifact in selected}
    extras = sorted(path.name for path in destination.glob("*.jar") if path.name not in expected_names)
    if extras and not allow_extra:
        raise PackError("unexpected JAR files in destination: " + ", ".join(extras))

    for number, artifact in enumerate(selected, start=1):
        target = destination / Path(artifact["path"]).name
        if target.exists():
            verify_artifact(target, artifact)
            state = "verified"
        else:
            download_artifact(target, artifact)
            state = "downloaded"
        print(f"[{number:02d}/{len(selected):02d}] {state}: {target.name}")
    print(f"materialized {len(selected)} verified JAR files for {side} in {destination}")


def verify_all(lock: dict, index: dict) -> None:
    validate_lock(lock)
    validate_index(lock, index)
    verify_release(index)
    release_hash = file_hashes(RELEASE_PATH)["sha256"]
    client_count = sum(a["env"]["client"] != "unsupported" for a in lock["artifacts"])
    server_count = sum(a["env"]["server"] != "unsupported" for a in lock["artifacts"])
    print(
        f"verified lock/index/mrpack: {len(lock['artifacts'])} files "
        f"({client_count} client, {server_count} server), release sha256 {release_hash}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build", help="build the deterministic .mrpack release")
    subparsers.add_parser("verify", help="verify lock, index, and .mrpack release")
    materialize_parser = subparsers.add_parser("materialize", help="download and verify a side's JAR files")
    materialize_parser.add_argument("side", choices=("client", "server"))
    materialize_parser.add_argument("destination", type=Path)
    materialize_parser.add_argument("--allow-extra", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        lock = read_json(LOCK_PATH)
        index = read_json(INDEX_PATH)
        if args.command == "build":
            build_release(lock, index)
        elif args.command == "verify":
            verify_all(lock, index)
        else:
            materialize(lock, args.side, args.destination, args.allow_extra)
    except PackError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
