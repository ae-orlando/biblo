#!/usr/bin/env python3
"""Create notes from the vault templates at canonical paths."""
from __future__ import annotations

import argparse
import calendar
from datetime import date, datetime
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]


class NotesError(RuntimeError):
    """A user-facing note factory error."""


def slugify(value: str) -> str:
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    slug = slug[:64].rstrip("-")
    return slug or "untitled"


def moment_tokens(day: date, now: datetime) -> list[tuple[str, str]]:
    iso = day.isocalendar()
    values = {
        "YYYY": f"{day.year:04d}",
        "YY": f"{day.year % 100:02d}",
        "MMMM": calendar.month_name[day.month],
        "MMM": calendar.month_abbr[day.month],
        "MM": f"{day.month:02d}",
        "M": str(day.month),
        "DD": f"{day.day:02d}",
        "D": str(day.day),
        "dddd": calendar.day_name[day.weekday()],
        "ddd": calendar.day_abbr[day.weekday()],
        "GGGG": f"{iso.year:04d}",
        "WW": f"{iso.week:02d}",
        "HH": now.strftime("%H"),
        "mm": now.strftime("%M"),
        "ss": now.strftime("%S"),
    }
    return sorted(values.items(), key=lambda item: len(item[0]), reverse=True)


def format_moment(template: str, day: date, now: datetime) -> str:
    tokens = moment_tokens(day, now)
    output: list[str] = []
    index = 0
    while index < len(template):
        char = template[index]
        if char == "[":
            end = template.find("]", index + 1)
            if end == -1:
                raise NotesError(f"unclosed literal in date format: {template}")
            output.append(template[index + 1 : end])
            index = end + 1
            continue
        for token, value in tokens:
            if template.startswith(token, index):
                output.append(value)
                index += len(token)
                break
        else:
            if char.isalpha():
                raise NotesError(
                    f"unsupported date token {template[index:]!r} in {template!r}"
                )
            output.append(char)
            index += 1
    return "".join(output)


def render_template(text: str, title: str, day: date, now: datetime, source: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1).strip()
        if token == "title":
            return title
        if token == "date":
            return day.isoformat()
        if token == "time":
            return now.strftime("%H:%M")
        if token.startswith("date:"):
            return format_moment(token[5:], day, now)
        raise NotesError(f"unknown template token {{" + token + "}} in " + str(source))

    rendered = re.sub(r"\{\{([^{}]+)\}\}", replace, text)
    if "{{" in rendered or "}}" in rendered:
        raise NotesError(f"unclosed template token in {source}")
    return rendered


def git_remote(repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def fill_project_fields(text: str, repo: Path | None) -> str:
    if repo is None:
        return text
    repo_path = repo.expanduser().resolve()
    remote = git_remote(repo_path)
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "repo:":
            lines[index] = f"repo: {repo_path}"
        elif stripped == "remote:" and remote:
            lines[index] = f"remote: {remote}"
    result = "\n".join(lines)
    if text.endswith("\n"):
        result += "\n"
    return result


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid date {value!r}; use YYYY-MM-DD") from exc


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=argparse.SUPPRESS, help="vault root")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=argparse.SUPPRESS,
        help="print the target path without writing",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Paths:\n"
            "  capture  00-inbox/YYYY-MM-DD-<slug>.md\n"
            "  daily    06-journal/YYYY/YYYY-MM-DD-dddd.md\n"
            "  weekly   06-journal/YYYY/YYYY-Www.md\n"
            "  concept  02-notes/<track>/<slug>.md\n"
            "  evidence 01-roadmap/evidence/YYYY-MM-DD-<slug>.md\n"
            "  review   01-roadmap/reviews/YYYY-MM-DD-<slug>.md\n"
            "  project  04-projects/<slug>.md"
        ),
    )
    parser.add_argument("--root", type=Path, default=None, help="vault root override")
    parser.add_argument("--dry-run", action="store_true", help="print without writing")
    subparsers = parser.add_subparsers(dest="command", required=True)

    capture = subparsers.add_parser("capture", help="create an inbox capture")
    capture.add_argument("title", nargs="+")
    add_common(capture)

    daily = subparsers.add_parser("daily", help="create the daily journal note")
    daily.add_argument("--date", type=parse_date, default=None, metavar="YYYY-MM-DD")
    add_common(daily)

    weekly = subparsers.add_parser("weekly", help="create the weekly journal note")
    weekly.add_argument("--date", type=parse_date, default=None, metavar="YYYY-MM-DD")
    add_common(weekly)

    concept = subparsers.add_parser("concept", help="create a concept note")
    concept.add_argument("--track", required=True, help="folder under 02-notes/")
    concept.add_argument("title", nargs="+")
    add_common(concept)

    evidence = subparsers.add_parser("evidence", help="create an evidence note")
    evidence.add_argument("title", nargs="+")
    add_common(evidence)

    review = subparsers.add_parser("review", help="create a review note")
    review.add_argument("title", nargs="+")
    add_common(review)

    project = subparsers.add_parser("project", help="create a project note")
    project.add_argument("--repo", type=Path, default=None)
    project.add_argument("title", nargs="*")
    add_common(project)

    return parser


def target_for(args: argparse.Namespace, root: Path, day: date) -> tuple[Path, str, str]:
    if args.command == "capture":
        title = " ".join(args.title).strip()
        if not title:
            raise NotesError("capture needs a non-empty title")
        return root / "00-inbox" / f"{day.isoformat()}-{slugify(title)}.md", title, "note"

    if args.command == "daily":
        weekday = calendar.day_name[day.weekday()]
        target = root / "06-journal" / str(day.year) / f"{day.isoformat()}-{weekday}.md"
        return target, f"{day.isoformat()} {weekday}", "daily"

    if args.command == "weekly":
        iso = day.isocalendar()
        week = f"{iso.year}-W{iso.week:02d}"
        return root / "06-journal" / str(iso.year) / f"{week}.md", week, "journal-weekly"

    if args.command == "evidence":
        title = " ".join(args.title).strip()
        if not title:
            raise NotesError("evidence needs a non-empty title")
        target = root / "01-roadmap" / "evidence" / f"{day.isoformat()}-{slugify(title)}.md"
        return target, title, "evidence"

    if args.command == "review":
        title = " ".join(args.title).strip()
        if not title:
            raise NotesError("review needs a non-empty title")
        target = root / "01-roadmap" / "reviews" / f"{day.isoformat()}-{slugify(title)}.md"
        return target, title, "review"

    if args.command == "concept":
        title = " ".join(args.title).strip()
        if not title:
            raise NotesError("concept needs a non-empty title")
        track = args.track.strip()
        if not track or Path(track).name != track:
            raise NotesError(f"invalid track name: {args.track!r}")
        track_dir = root / "02-notes" / track
        if not track_dir.is_dir():
            parent = root / "02-notes"
            available = (
                ", ".join(sorted(p.name for p in parent.iterdir() if p.is_dir()))
                if parent.is_dir()
                else "none"
            )
            raise NotesError(f"unknown track {track!r}; available: {available}")
        return track_dir / f"{slugify(title)}.md", title, "concept"

    if args.command == "project":
        title = " ".join(args.title).strip()
        repo = args.repo
        if repo is not None:
            repo_path = repo.expanduser().resolve()
            slug = slugify(repo_path.name)
            if not title:
                title = repo_path.name.replace("-", " ").replace("_", " ")
        else:
            if not title:
                raise NotesError("project needs a title or --repo")
            slug = slugify(title)
        if not title:
            raise NotesError("project needs a non-empty title")
        return root / "04-projects" / f"{slug}.md", title, "project"

    raise NotesError(f"unknown command: {args.command}")


def run(args: argparse.Namespace) -> int:
    root = (args.root or DEFAULT_ROOT).expanduser().resolve()
    now = datetime.now()
    day = getattr(args, "date", None) or now.date()
    target, title, template_name = target_for(args, root, day)

    if not args.dry_run:
        if target.exists():
            print(target)
            return 0

        template_path = root / "99-templates" / f"{template_name}.md"
        if not template_path.is_file():
            raise NotesError(f"missing template: {template_path}")
        text = template_path.read_text(encoding="utf-8")
        rendered = render_template(text, title, day, now, template_path)
        if args.command == "project":
            rendered = fill_project_fields(rendered, args.repo)

        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(rendered)
        except FileExistsError:
            pass

    print(target)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except NotesError as exc:
        print(f"notes.py: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
