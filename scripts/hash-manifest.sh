#!/usr/bin/env bash
# Recalcula SHA-256 de tudo em evidence/ e reescreve o manifesto.
# Uso: ./scripts/hash-manifest.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MANIFEST="evidence/hashes/manifest.json"
mkdir -p "$(dirname "$MANIFEST")"

command -v jq >/dev/null 2>&1 || { echo "erro: jq é necessário" >&2; exit 1; }

entries=()
while IFS= read -r f; do
  hash="$(sha256sum "$f" | awk '{print $1}')"
  size="$(stat -c%s "$f")"
  entries+=("$(jq -nc --arg p "$f" --arg h "$hash" --argjson s "$size" \
    '{path: $p, sha256: $h, bytes: $s}')")
done < <(
  find evidence -type f \
    ! -name '.gitkeep' \
    ! -path "evidence/hashes/manifest.json" \
    ! -path "evidence/tmp/*" \
    | LC_ALL=C sort
)

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ ${#entries[@]} -eq 0 ]; then
  jq -n --arg ts "$ts" '{generated_at: $ts, algorithm: "sha256", files: []}' > "$MANIFEST"
else
  printf '%s\n' "${entries[@]}" \
    | jq -s --arg ts "$ts" '{generated_at: $ts, algorithm: "sha256", files: .}' > "$MANIFEST"
fi

echo "manifesto atualizado: $MANIFEST (${#entries[@]} arquivos)"
