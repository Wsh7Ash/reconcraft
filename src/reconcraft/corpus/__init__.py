"""reconcraft corpus: pack metadata plus 50 authored recon skills.

Skills are authored as plain dicts in ``part1``..``part3`` so each file
stays readable, then loaded once into the validated
:class:`~reconcraft.model.Skill` shape.
"""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "reconcraft",
    "version": "1.0.0",
    "category": "bug-bounty-tooling",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated bug-bounty reconnaissance skills: authorized scope handling, "
        "enumeration, content discovery, fingerprinting, validation and hand-off, "
        "with a plan/coverage CLI for hunters and agents."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase", "assets"),
    "requires_verification": False,
}

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]