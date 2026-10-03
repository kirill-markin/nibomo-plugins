import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def write_archive(root: Path, destination: Path, files: list[Path]) -> None:
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, path.relative_to(root))


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    version = json.loads((root / "plugin.json").read_text())["version"]
    destination = root / "dist"
    destination.mkdir(exist_ok=True)
    shared = [root / "README.md", root / "LICENSE"]
    shared += [path for folder in ["skills", "assets"] for path in (root / folder).rglob("*") if path.is_file()]
    write_archive(root, destination / f"nibomo-{version}-claude.zip", shared + [root / ".claude-plugin/plugin.json", root / ".mcp.json"])
    write_archive(root, destination / f"nibomo-{version}-openai.zip", shared + [root / "plugin.json", root / "mcp.json"])


if __name__ == "__main__":
    main()
