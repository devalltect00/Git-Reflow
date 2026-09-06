# app/core/reflow/tag_converter.py

"""Safe, bidirectional conversion of version-shaped Git tags.

The converter supports canonical PEP 440 and Semantic Versioning tags whose
release component is ``MAJOR.MINOR.PATCH``. Conversion is deliberately strict:
unsupported or lossy suffix combinations are reported and skipped instead of
being rewritten into malformed tag names.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class TagFormat(StrEnum):
    """Version-tag formats supported by :class:`TagConverter`."""

    SEMVER = "semver"
    PEP440 = "pep440"

    @classmethod
    def from_value(cls, value: TagFormat | str) -> TagFormat:
        """Normalize a CLI or configuration value into a supported format.

        Args:
            value:
                Enum value or a case-insensitive format name. ``pep-440`` and
                ``pep_440`` are accepted aliases for ``pep440``.

        Returns:
            TagFormat:
                Normalized target format.

        Raises:
            ValueError:
                If the value does not name a supported tag format.
        """

        if isinstance(value, cls):
            return value

        normalized = str(value).strip().lower().replace("-", "").replace("_", "")
        aliases = {
            "semver": cls.SEMVER,
            "semanticversioning": cls.SEMVER,
            "pep440": cls.PEP440,
        }

        try:
            return aliases[normalized]
        except KeyError as exc:
            supported = ", ".join(item.value for item in cls)
            raise ValueError(
                f"Unsupported tag format '{value}'. Choose one of: {supported}."
            ) from exc


@dataclass(frozen=True, slots=True)
class TagConversion:
    """One safe source-to-destination tag mapping."""

    source: str
    destination: str


@dataclass(frozen=True, slots=True)
class SkippedTag:
    """A tag excluded from a conversion plan with a user-facing reason."""

    tag: str
    reason: str


@dataclass(frozen=True, slots=True)
class TagConversionPlan:
    """Collision-aware conversion plan created before Git is modified."""

    target_format: TagFormat
    conversions: tuple[TagConversion, ...]
    skipped: tuple[SkippedTag, ...]


_PEP440_TAG_PATTERN = re.compile(
    r"^(?P<prefix>v?)"
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:(?P<pre>a|b|rc)(?P<pre_number>\d+))?"
    r"(?:\.post(?P<post_number>\d+))?"
    r"(?:\.dev(?P<dev_number>\d+))?"
    r"(?:\+(?P<local>[a-z0-9]+(?:[._-][a-z0-9]+)*))?$",
    re.IGNORECASE,
)

_SEMVER_TAG_PATTERN = re.compile(
    r"^(?P<prefix>v?)"
    r"(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>"
    r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
    r"))?"
    r"(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def _release_from_match(match: re.Match[str]) -> str:
    """Return a normalized three-component release from a regex match."""

    return ".".join(str(int(match.group(name))) for name in ("major", "minor", "patch"))


def _normalize_pep_local_for_semver(value: str) -> str:
    """Convert PEP 440 local separators into SemVer build separators."""

    return ".".join(part for part in re.split(r"[._-]+", value) if part)


def _normalize_semver_build_for_pep(value: str) -> str:
    """Convert SemVer build metadata into a valid PEP 440 local version."""

    return ".".join(part.lower() for part in re.split(r"[.-]+", value) if part)


class TagConverter:
    """Plan safe name conversions between PEP 440 and SemVer tags.

    Responsibilities:
        - Parse supported version-shaped Git tags.
        - Convert in either supported direction.
        - Skip already-conforming, colliding, or unsupported tags.
        - Remain independent from local and remote Git mutations.
    """

    def pep440_to_semver_tag(self, tag: str) -> str:
        """Convert one supported PEP 440 tag into SemVer.

        Supported mappings include ``aN`` to ``alpha.N``, ``bN`` to
        ``beta.N``, ``rcN`` to ``rc.N``, ``.devN`` to ``dev.N``, and
        ``.postN`` to ``+post.N``. Local metadata becomes SemVer build
        metadata.

        Args:
            tag:
                PEP 440 tag with a three-component release.

        Returns:
            str:
                Equivalent SemVer tag.

        Raises:
            ValueError:
                If the tag is not supported or combines phases that cannot be
                represented safely in SemVer.
        """

        match = _PEP440_TAG_PATTERN.fullmatch(tag)
        if match is None:
            raise ValueError(f"Tag '{tag}' is not a supported PEP 440 tag.")

        prerelease = match.group("pre")
        post_number = match.group("post_number")
        dev_number = match.group("dev_number")

        phase_count = sum(
            item is not None for item in (prerelease, post_number, dev_number)
        )
        if phase_count > 1:
            raise ValueError(
                f"Tag '{tag}' combines PEP 440 phases that cannot be mapped "
                "to SemVer without changing their ordering semantics."
            )

        converted = f"{match.group('prefix')}{_release_from_match(match)}"

        if prerelease is not None:
            names = {"a": "alpha", "b": "beta", "rc": "rc"}
            converted += (
                f"-{names[prerelease.lower()]}.{int(match.group('pre_number'))}"
            )
        elif dev_number is not None:
            converted += f"-dev.{int(dev_number)}"

        build_parts: list[str] = []
        if post_number is not None:
            build_parts.extend(("post", str(int(post_number))))

        local = match.group("local")
        if local is not None:
            build_parts.append(_normalize_pep_local_for_semver(local))

        if build_parts:
            converted += f"+{'.'.join(build_parts)}"

        return converted

    def semver_to_pep440_tag(self, tag: str) -> str:
        """Convert one supported SemVer tag into PEP 440.

        The prerelease identifiers ``alpha.N``, ``beta.N``, ``rc.N``, and
        ``dev.N`` have direct supported mappings. Generic SemVer build metadata
        becomes PEP 440 local metadata; ``post.N`` build metadata becomes a
        PEP 440 post release.

        Args:
            tag:
                Semantic Versioning tag.

        Returns:
            str:
                Equivalent PEP 440 tag.

        Raises:
            ValueError:
                If a prerelease identifier has no safe PEP 440 equivalent.
        """

        match = _SEMVER_TAG_PATTERN.fullmatch(tag)
        if match is None:
            raise ValueError(f"Tag '{tag}' is not a supported SemVer tag.")

        converted = f"{match.group('prefix')}{_release_from_match(match)}"
        prerelease = match.group("prerelease")

        if prerelease is not None:
            phase_match = re.fullmatch(
                r"(?P<phase>alpha|beta|rc|dev)\.(?P<number>0|[1-9]\d*)",
                prerelease,
                flags=re.IGNORECASE,
            )
            if phase_match is None:
                raise ValueError(
                    f"SemVer prerelease '{prerelease}' in tag '{tag}' has no "
                    "safe PEP 440 equivalent."
                )

            phase = phase_match.group("phase").lower()
            number = int(phase_match.group("number"))
            phase_names = {"alpha": "a", "beta": "b", "rc": "rc"}
            converted += (
                f".dev{number}" if phase == "dev" else f"{phase_names[phase]}{number}"
            )

        build = match.group("build")
        if build is None:
            return converted

        build_parts = build.split(".")
        is_post_release = (
            len(build_parts) >= 2
            and build_parts[0].lower() == "post"
            and build_parts[1].isdigit()
        )

        if is_post_release:
            if prerelease is not None:
                raise ValueError(
                    f"Tag '{tag}' combines prerelease and post-release metadata "
                    "that cannot be mapped safely to PEP 440."
                )

            converted += f".post{int(build_parts[1])}"
            remaining_build = ".".join(build_parts[2:])
            if remaining_build:
                converted += f"+{_normalize_semver_build_for_pep(remaining_build)}"
            return converted

        converted += f"+{_normalize_semver_build_for_pep(build)}"
        return converted

    def convert_tag_name(
        self,
        tag: str,
        target_format: TagFormat | str = TagFormat.SEMVER,
    ) -> str:
        """Convert a tag name to the requested format without modifying Git.

        Args:
            tag:
                Existing version tag.

            target_format:
                Destination format. Defaults to SemVer.

        Returns:
            str:
                Converted tag, or the original tag when it already conforms to
                the requested format.

        Raises:
            ValueError:
                If the tag cannot be converted safely.
        """

        resolved_format = TagFormat.from_value(target_format)

        if resolved_format is TagFormat.SEMVER:
            if _SEMVER_TAG_PATTERN.fullmatch(tag):
                return tag
            return self.pep440_to_semver_tag(tag)

        if _PEP440_TAG_PATTERN.fullmatch(tag):
            return tag
        return self.semver_to_pep440_tag(tag)

    def plan_conversions(
        self,
        tags: Iterable[str],
        target_format: TagFormat | str = TagFormat.SEMVER,
    ) -> TagConversionPlan:
        """Build a mutation-free, collision-aware conversion plan.

        Existing destination tags are reserved before planning begins. This is
        what prevents ``v1.2.3b1`` from attempting to recreate an existing
        ``v1.2.3-beta.1`` tag.

        Args:
            tags:
                Repository tag names.

            target_format:
                Requested destination format.

        Returns:
            TagConversionPlan:
                Safe mappings and skipped tags with reasons.
        """

        resolved_format = TagFormat.from_value(target_format)
        source_tags = tuple(tags)
        reserved_tags = set(source_tags)
        conversions: list[TagConversion] = []
        skipped: list[SkippedTag] = []

        for tag in source_tags:
            try:
                destination = self.convert_tag_name(tag, resolved_format)
            except ValueError as exc:
                skipped.append(SkippedTag(tag=tag, reason=str(exc)))
                continue

            if destination == tag:
                skipped.append(
                    SkippedTag(
                        tag=tag,
                        reason=f"already matches {resolved_format.value}",
                    )
                )
                continue

            if destination in reserved_tags:
                skipped.append(
                    SkippedTag(
                        tag=tag,
                        reason=f"destination tag already exists: {destination}",
                    )
                )
                continue

            conversions.append(TagConversion(source=tag, destination=destination))
            reserved_tags.add(destination)

        return TagConversionPlan(
            target_format=resolved_format,
            conversions=tuple(conversions),
            skipped=tuple(skipped),
        )
