import os
import zipfile

def create_submission_zip(output_zip="SurakshaKavach_AI_R4C_Submission.zip"):
    # Target files and folders to include
    include_paths = [
        "app.py",
        "requirements.txt",
        "README.md",
        "ACTION_PLAN_SUBMISSION.md",
        "SURAKSHAKAVACH_ACTION_PLAN_RPA_2026.pdf",
        "SurakshaKavach_AI_Presentation.pptx",
        "PRESENTATION_CHEATSHEET.md",
        "run_acceptance_tests.py",
        ".gitignore",
        "forensic_engine",
        "templates",
        "sample_apks"
    ]

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for item in include_paths:
            if os.path.isfile(item):
                z.write(item, arcname=item)
                print(f"Added file: {item}")
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    # Skip __pycache__
                    if "__pycache__" in root:
                        continue
                    for file in files:
                        if file.endswith(('.pyc', '.pyo', '.db', '.log')):
                            continue
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, start=".")
                        z.write(full_path, arcname=rel_path)
                        print(f"Added dir file: {rel_path}")

    size_kb = round(os.path.getsize(output_zip) / 1024, 2)
    print(f"\n[SUCCESS] Clean submission zip created: {output_zip} ({size_kb} KB)")

if __name__ == '__main__':
    create_submission_zip()
