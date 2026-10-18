"""Copy published APKs verbatim, checking recorded upstream SHA-256 digests."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

root = Path(__file__).resolve().parents[1]
repository = os.environ['GITHUB_REPOSITORY']
commit = os.environ['GITHUB_SHA']
manifest = json.loads((root / 'docs/upstream-releases.json').read_text())
for release in manifest:
    destination = root / 'build/preserved' / release['tag']
    destination.mkdir(parents=True, exist_ok=True)
    for asset in release['assets']:
        path = destination / asset['name']
        subprocess.run(['curl', '-fsSL', '--retry', '3', asset['url'], '-o', str(path)], check=True)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != asset['sha256'] or path.stat().st_size != asset['size']:
            raise SystemExit(f'Upstream verification failed: {release["tag"]}/{path.name}')
        print(f'VERIFIED {path.name}: {digest}', flush=True)
    subprocess.run(['git', 'archive', '--format=zip', f'--output={destination / "Schulte-Flow-Source.zip"}', 'HEAD'], cwd=root, check=True)
    notes = destination.parent / (release['tag'] + '-notes.md')
    notes.write_text(
        '本次为独立仓库迁移发布，APK、签名和原有验证附件按 SHA-256 原样保留，未重新签名。'
        '附带源码为本仓库整理后的原生与 Godot 完整工程。\n\n'
        f'原始发布：https://github.com/azfiles/apkGo/releases/tag/{release["upstream_tag"]}\n\n'
        f'整理后源码：`{commit}`。此次迁移不等同于重新执行 Android 设备验证。\n\n'
        + release['body']
    )
    existing = subprocess.run(['gh', 'release', 'view', release['tag'], '--repo', repository], capture_output=True)
    if existing.returncode == 0:
        print(f'Already published; preserved unchanged: {release["tag"]}', flush=True)
        continue
    subprocess.run([
        'gh', 'release', 'create', release['tag'], *[str(p) for p in sorted(destination.iterdir())],
        '--repo', repository, '--target', commit, '--title', release['title'],
        '--notes-file', str(notes), '--prerelease', '--latest=false',
    ], check=True)
    print(f'PUBLISHED {repository} {release["tag"]}', flush=True)
