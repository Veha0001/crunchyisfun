import os
import re

SMALI_ROOT = os.environ["BASE_SMALI"]


def main():
    enable_ads_field = None
    smali_file_path = None

    for root, _, files in os.walk(SMALI_ROOT):
        for file in files:
            if file.endswith(".smali"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if '", enableAds="' in line:
                            # Look only in the next 8 lines
                            for j in range(1, 9):
                                if i + j >= len(lines):
                                    break
                                candidate_line = lines[i + j]
                                match = re.search(
                                    r"iget-boolean\s+\S+,\s+\S+,\s+(\S+)",
                                    candidate_line,
                                )
                                if match:
                                    enable_ads_field = match.group(1)
                                    smali_file_path = path
                                    break
                        if enable_ads_field:
                            break
                if enable_ads_field:
                    break
        if enable_ads_field:
            break

    if not enable_ads_field or not smali_file_path:
        raise ValueError(
            "Could not find enableAds field within 8 lines in smali files."
        )

    print(f"Found enableAds field: {enable_ads_field} in {smali_file_path}")

    # Patch logic remains unchanged
    with open(smali_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_constructor = False
    patched = False
    field_name_only = enable_ads_field.split("->")[1]

    for line in lines:
        if re.search(rf"\.field .* final {re.escape(field_name_only)}", line):
            line = line.replace(" final", "")

        if line.startswith(".method public constructor"):
            in_constructor = True

        if in_constructor and "return-void" in line and not patched:
            new_lines.append("    move-object/from16 v0, p0\n")
            new_lines.append("    const/4 v1, 0x0\n")
            new_lines.append(f"    iput-boolean v1, v0, {enable_ads_field}\n")
            patched = True

        new_lines.append(line)

    with open(smali_file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Patch applied successfully in {smali_file_path}")


if __name__ == "__main__":
    main()
