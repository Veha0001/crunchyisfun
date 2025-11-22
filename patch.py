"""
Search smali files for a boolean field related to "enableAds"
and force its constructor initialization to always be false.
"""

import os
import re
from pathlib import Path

SMALI_ROOT = Path(os.environ["BASE_SMALI"])


def find_enable_ads(root_dir: Path):
    """Locate the enableAds field and the smali file that contains it."""
    for path in root_dir.rglob("*.smali"):
        lines = path.read_text(encoding="utf-8").splitlines()

        for i, line in enumerate(lines):
            if '", enableAds="' not in line:
                continue

            # Search the next 8 lines for iget-boolean
            for j in range(1, 9):
                if i + j >= len(lines):
                    break

                candidate = lines[i + j]
                match = re.search(r"iget-boolean\s+\S+,\s+\S+,\s+(\S+)", candidate)
                if match:
                    return match.group(1), path

    return None, None


def patch_smali(path: Path, enable_ads: str):
    """Patch the smali constructor to set enableAds to false."""
    lines = path.read_text(encoding="utf-8").splitlines()
    new = []

    in_constructor = False
    patched = False
    field_name = enable_ads.split("->")[1]

    for line in lines:
        # Remove "final" if present on the field
        if re.search(rf"\.field .* final {re.escape(field_name)}", line):
            line = line.replace(" final", "")

        # Detect constructor
        if line.startswith(".method public constructor"):
            in_constructor = True

        # Insert our patch before return-void
        if in_constructor and "return-void" in line and not patched:
            new.append("    move-object/from16 v0, p0")
            new.append("    const/4 v1, 0x0")
            new.append(f"    iput-boolean v1, v0, {enable_ads}")
            patched = True

        new.append(line)

    path.write_text("\n".join(new), encoding="utf-8")


def main():
    """Main function to find and patch enableAds field."""
    enable_ads, path = find_enable_ads(SMALI_ROOT)

    if not enable_ads or not path:
        raise ValueError(
            "Could not find enableAds field within 8 lines in smali files."
        )

    print(f"Found enableAds field: {enable_ads}")
    print(f"Located in: {path}")

    patch_smali(path, enable_ads)

    print(f"Patch applied successfully: {path}")


if __name__ == "__main__":
    main()
