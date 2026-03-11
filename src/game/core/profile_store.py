from __future__ import annotations

import json
import time
from pathlib import Path

from game.core.profile import PlayerProfile


class ProfileStore:
    """Local JSON persistence for PlayerProfile."""

    CURRENT_SCHEMA_VERSION = 1

    def __init__(
        self,
        save_path: Path | None = None,
        schema_version: int = CURRENT_SCHEMA_VERSION,
    ) -> None:
        self.save_path = save_path or Path("save/profile.json")
        self.schema_version = schema_version

    def load_or_create_profile(self, save_if_missing: bool = True) -> PlayerProfile:
        profile = self.load_profile()
        if profile is not None:
            return profile

        profile = PlayerProfile()
        if save_if_missing:
            self.save_profile(profile)
        return profile

    def load_profile(self) -> PlayerProfile | None:
        if not self.save_path.exists():
            print(f"[ProfileStore] Save file not found at {self.save_path}. Using default profile.")
            return None

        try:
            raw_text = self.save_path.read_text(encoding="utf-8")
            payload = json.loads(raw_text)
        except OSError as error:
            print(f"[ProfileStore] Could not read save file: {error}. Using default profile.")
            return None
        except json.JSONDecodeError as error:
            print(
                "[ProfileStore] Malformed JSON save file: "
                f"{error}. Falling back to default profile."
            )
            self._stash_invalid_file("malformed")
            return None

        if not isinstance(payload, dict):
            print("[ProfileStore] Save data is not an object. Falling back to default profile.")
            self._stash_invalid_file("invalid_root")
            return None

        schema_version = payload.get("schema_version")
        if schema_version != self.schema_version:
            print(
                f"[ProfileStore] Unsupported schema version {schema_version!r}. "
                f"Expected {self.schema_version}. Falling back to default profile."
            )
            self._stash_invalid_file("unsupported_schema")
            return None

        profile_payload = payload.get("profile")
        if not isinstance(profile_payload, dict):
            print(
                "[ProfileStore] Missing/invalid profile payload. Falling back to default profile."
            )
            self._stash_invalid_file("invalid_profile")
            return None

        try:
            return PlayerProfile.from_dict(profile_payload)
        except Exception as error:  # defensive fallback for partial/corrupt data
            print(
                "[ProfileStore] Failed to parse profile payload: "
                f"{error}. Falling back to default profile."
            )
            self._stash_invalid_file("parse_error")
            return None

    def save_profile(self, profile: PlayerProfile) -> bool:
        payload = {
            "schema_version": self.schema_version,
            "profile": profile.to_dict(),
        }

        try:
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = self.save_path.with_suffix(self.save_path.suffix + ".tmp")
            tmp_path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            tmp_path.replace(self.save_path)
            return True
        except OSError as error:
            print(f"[ProfileStore] Failed to save profile: {error}")
            return False

    def _stash_invalid_file(self, reason: str) -> None:
        if not self.save_path.exists():
            return

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = self.save_path.with_suffix(
            self.save_path.suffix + f".{reason}.{timestamp}.bak"
        )
        try:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            self.save_path.replace(backup_path)
            print(f"[ProfileStore] Moved invalid save file to {backup_path}")
        except OSError as error:
            print(f"[ProfileStore] Could not back up invalid save file: {error}")
