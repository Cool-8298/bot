import subprocess
import sys
import re

# === Analyze a Python file to detect expected input() types ===
def detect_inputs(script_path):
    """
    Check how many and what type of inputs the target script asks for.
    Returns a list like ['link', 'yes', 'yes'].
    """
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    input_types = []
    lines = content.splitlines()
    for line in lines:
        if 'input' in line:
            if re.search(r'target\s*link|url|website|enter\s+link', line):
                input_types.append('link')
            elif re.search(r'\(y/n\)|yes\s*or\s*no|do you want|confirm', line):
                input_types.append('yes')
            else:
                input_types.append('yes')  # Default to 'yes' if unknown

    return input_types

# === Run one or more Python files and automatically respond to input() prompts ===
def run_python_files(file_paths, user_link="https://example.com"):
    """
    Executes each script and sends 'y' or a URL to input() based on detection.
    """
    for path in file_paths:
        print(f"\n▶️ Running {path}...")

        try:
            input_prompts = detect_inputs(path)

            # Prepare inputs for the script
            input_values = []
            for prompt in input_prompts:
                if prompt == 'link':
                    input_values.append(user_link)
                elif prompt == 'yes':
                    input_values.append('y')

            injected_input = '\n'.join(input_values) + '\n'

            # Run the script and send prepared inputs
            process = subprocess.Popen(
                ['python', path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=injected_input)

            # Show output and errors
            print(f"✅ Output of {path}:\n{stdout}")
            if stderr:
                print(f"❗ Errors in {path}:\n{stderr}")
        except Exception as e:
            print(f"❌ Failed to run {path}: {e}")

# === Show command-line help menu ===
def show_help():
    """
    Display all supported commands with usage examples.
    """
    print("""
🔧  Help Menu

Usage:
  python automation_bot.py <command> [arguments]

Available Commands:

  run <file1.py> <file2.py> ... [link]
    → Runs one or more Python scripts.
    → Automatically responds to input() prompts with 'y' or the provided link.

    Example:
      python automation_bot.py run script1.py script2.py https://example.com

  help
    → Shows this help menu.

📌 Notes:
- The bot auto-detects if a script wants a URL or confirmation (Y/N).
- Default link is: https://github.com/cool-8298 if none is provided.
""")

# === Entry Point ===
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "run":
            files = []
            link = "https://github.com/cool-8298"  # Default link
            for arg in sys.argv[2:]:
                if arg.endswith('.py'):
                    files.append(arg)
                elif arg.startswith('http'):
                    link = arg

            if not files:
                print("⚠️ No Python files specified. Usage: python automation_bot.py run file1.py file2.py https://yourlink.com")
            else:
                run_python_files(files, user_link=link)

        elif cmd == "help":
            show_help()

        else:
            print(f"❌ Unknown command: {cmd}. Use 'help' to see valid options.")
    else:
        show_help()
