"""Fail closed on changed build inputs or outputs; optionally package allowlisted files."""
from pathlib import Path
import argparse
import json
import shutil
from release_support import PUBLIC, EDITION, digest, input_paths

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--package',action='store_true')
args=parser.parse_args()
manifest=json.loads((ROOT/'output/release-manifest.json').read_text())
assert manifest['edition']==EDITION
assert manifest['public_files']==PUBLIC
assert set(manifest['inputs'])==set(input_paths(ROOT)), 'Build inputs changed; rebuild.'
assert set(manifest['outputs'])==set(PUBLIC.values())
for section in ['inputs','outputs']:
    for name,expected in manifest[section].items():
        path=ROOT/name
        assert path.is_file() and not path.is_symlink(), f'Missing or linked file: {name}'
        assert digest(path)==expected, f'Stale release: {name}. Rebuild and visually inspect PDFs.'
if args.package:
    target=ROOT/'_site'
    assert not target.is_symlink()
    target.mkdir(exist_ok=True)
    assert not any(target.iterdir()), '_site must be empty before packaging.'
    for name,source in PUBLIC.items(): shutil.copyfile(ROOT/source,target/name)
    assert {p.name for p in target.iterdir()}==set(PUBLIC)
print(f'Edition {EDITION}: inputs and outputs match; {len(PUBLIC)} public files allowlisted.')
