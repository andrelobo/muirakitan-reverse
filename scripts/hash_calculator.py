#!/usr/bin/env python3
"""
Muirakitan RE - Hash Calculator Utility
Calculates and validates SHA-256 hashes for evidence integrity.
"""

import hashlib
import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class HashRecord:
    """Record of a file hash with metadata."""
    sha256: str
    file_path: str
    file_size: int
    calculated_by: str
    stage: str
    timestamp: str
    purpose: str
    algorithm: str = "sha256"


class HashCalculator:
    """Calculates and manages SHA-256 hashes for evidence files."""

    def __init__(self, evidence_dir: str = "/evidence", registry_path: str = "/evidence/hash-registros/registry.json"):
        self.evidence_dir = Path(evidence_dir)
        self.registry_path = Path(registry_path)
        self.registry: Dict[str, HashRecord] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Load existing hash registry."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                    self.registry = {k: HashRecord(**v) for k, v in data.items()}
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load registry: {e}", file=sys.stderr)
                self.registry = {}

    def _save_registry(self) -> None:
        """Save hash registry to disk."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.registry.items()}, f, indent=2)

    def calculate_hash(self, file_path: Path, algorithm: str = "sha256") -> str:
        """Calculate hash of a file."""
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def register_file(
        self,
        file_path: str,
        calculated_by: str,
        stage: str,
        purpose: str,
        algorithm: str = "sha256"
    ) -> HashRecord:
        """Calculate and register hash for a file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        sha256 = self.calculate_hash(path, algorithm)
        file_size = path.stat().st_size

        record = HashRecord(
            sha256=sha256,
            file_path=str(path.absolute()),
            file_size=file_size,
            calculated_by=calculated_by,
            stage=stage,
            timestamp=datetime.utcnow().isoformat() + "Z",
            purpose=purpose,
            algorithm=algorithm
        )

        # Use relative path as key for registry
        try:
            rel_path = path.relative_to(self.evidence_dir)
            key = str(rel_path)
        except ValueError:
            key = str(path.absolute())

        self.registry[key] = record
        self._save_registry()

        # Also save individual hash file
        hash_file = self.evidence_dir / "hash-registros" / f"{path.name}.{algorithm}"
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        with open(hash_file, 'w') as f:
            f.write(f"{sha256}  {path.name}\n")

        return record

    def verify_file(self, file_path: str, expected_hash: Optional[str] = None) -> bool:
        """Verify file hash against registry or expected value."""
        path = Path(file_path)
        if not path.exists():
            return False

        # Calculate current hash
        current_hash = self.calculate_hash(path)

        # Check against expected hash if provided
        if expected_hash:
            return current_hash == expected_hash

        # Check against registry
        try:
            rel_path = path.relative_to(self.evidence_dir)
            key = str(rel_path)
        except ValueError:
            key = str(path.absolute())

        if key in self.registry:
            return current_hash == self.registry[key].sha256

        return False

    def verify_all(self) -> Dict[str, bool]:
        """Verify all registered files."""
        results = {}
        for key, record in self.registry.items():
            path = Path(record.file_path)
            if path.exists():
                current_hash = self.calculate_hash(path)
                results[key] = current_hash == record.sha256
            else:
                results[key] = False
        return results

    def get_record(self, file_path: str) -> Optional[HashRecord]:
        """Get hash record for a file."""
        path = Path(file_path)
        try:
            rel_path = path.relative_to(self.evidence_dir)
            key = str(rel_path)
        except ValueError:
            key = str(path.absolute())
        return self.registry.get(key)

    def list_records(self, stage: Optional[str] = None) -> List[HashRecord]:
        """List all hash records, optionally filtered by stage."""
        records = list(self.registry.values())
        if stage:
            records = [r for r in records if r.stage == stage]
        return records


def main():
    parser = argparse.ArgumentParser(description="Muirakitan RE Hash Calculator")
    parser.add_argument("action", choices=["calculate", "verify", "verify-all", "list", "register"],
                        help="Action to perform")
    parser.add_argument("file", nargs="?", help="File path (for calculate/verify/register)")
    parser.add_argument("--expected", help="Expected hash for verification")
    parser.add_argument("--agent", default="unknown", help="Agent name")
    parser.add_argument("--stage", default="unknown", help="RE stage (RE-01 to RE-06)")
    parser.add_argument("--purpose", default="integrity", help="Purpose of hash")
    parser.add_argument("--evidence-dir", default="/evidence", help="Evidence directory")
    parser.add_argument("--registry", help="Registry file path")
    parser.add_argument("--algorithm", default="sha256", choices=["sha256", "sha512"],
                        help="Hash algorithm")

    args = parser.parse_args()

    calculator = HashCalculator(
        evidence_dir=args.evidence_dir,
        registry_path=args.registry or "/evidence/hash-registros/registry.json"
    )

    if args.action == "calculate":
        if not args.file:
            parser.error("File path required for calculate action")
        hash_value = calculator.calculate_hash(Path(args.file), args.algorithm)
        print(hash_value)

    elif args.action == "register":
        if not args.file:
            parser.error("File path required for register action")
        record = calculator.register_file(
            args.file,
            calculated_by=args.agent,
            stage=args.stage,
            purpose=args.purpose,
            algorithm=args.algorithm
        )
        print(f"Registered: {record.sha256}  {args.file}")
        print(f"  Agent: {record.calculated_by}")
        print(f"  Stage: {record.stage}")
        print(f"  Purpose: {record.purpose}")
        print(f"  Timestamp: {record.timestamp}")

    elif args.action == "verify":
        if not args.file:
            parser.error("File path required for verify action")
        result = calculator.verify_file(args.file, args.expected)
        print("VERIFIED" if result else "FAILED")
        sys.exit(0 if result else 1)

    elif args.action == "verify-all":
        results = calculator.verify_all()
        all_ok = all(results.values())
        for key, ok in results.items():
            status = "OK" if ok else "FAIL"
            print(f"[{status}] {key}")
        print(f"\nAll verified: {all_ok}")
        sys.exit(0 if all_ok else 1)

    elif args.action == "list":
        records = calculator.list_records(args.stage if args.stage != "unknown" else None)
        for record in records:
            print(f"{record.sha256}  {record.file_path}  [{record.stage}] {record.purpose}")


if __name__ == "__main__":
    main()