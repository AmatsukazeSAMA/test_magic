"""Bind independently verified visible equivalents to an actually reviewed owner.

This creates no artwork and never establishes dynamic or user acceptance.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent.parent / 'art/full_character_redraw_1080p_v01'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
save = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
alias_path = base / 'VISIBLE_ASSET_ALIASES.json'
registry_path = base / 'ASSET_REGISTRY.json'
aliases = read(alias_path)
registry = read(registry_path)
if not aliases['primary_source_pairs_viewed']:
    raise SystemExit('Source pairs must have actual primary and independent review first.')
history = base / 'ALIAS_BINDING_HISTORY.jsonl'
updated = []
for group in aliases['groups']:
    owner_id = group['asset_owner_id']
    owner = registry.get(owner_id)
    if not owner or owner.get('status') != 'reviewed_static_candidate':
        continue
    if not owner.get('primary_static_pass') or not owner.get('independent_static_pass'):
        continue
    if owner.get('requires_whole_imggen') and not owner.get('whole_imggen_completed'):
        raise ValueError('Locally repaired intermediate cannot supply an alias.')
    if hashlib.sha256(Path(owner['image']).read_bytes()).hexdigest() != owner['sha256']:
        raise ValueError('Owner pixels changed after review.')
    for member in group['members']:
        if member == owner_id:
            continue
        record = {**owner, 'id': member, 'reused_visible_asset_from': owner_id,
                  'visible_equivalence_group': group['asset_key'],
                  'visible_equivalence_review': group['review'],
                  'primary_source_pairs_viewed': True, 'new_image_generation_for_alias': False,
                  'source_registration_and_occlusion_review': 'pending per exposure',
                  'user_accepted': False, 'dynamic_validated': False}
        if registry.get(member) == record:
            continue
        with history.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'at_utc': datetime.now(timezone.utc).isoformat(),
                                     'id': member, 'previous': registry.get(member), 'new': record},
                                    ensure_ascii=False) + '\n')
        registry[member] = record
        updated.append({'id': member, 'owner': owner_id})
    group['owner_static_reviewed'] = True
    group['owner_current_image_sha256'] = owner['sha256']
    group['user_accepted'] = False
    group['dynamic_redraw_review'] = False
save(registry_path, registry)
save(alias_path, aliases)
print(json.dumps({'aliases_bound': updated, 'new_generation_calls': 0, 'dynamic_validated': False}))
