import subprocess

def build_executable():
    print("Building the executable...")

    # Command to build the .exe using PyInstaller
    command = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--add-data=attachments:attachments",  # Include meta files
        "--add-data=meta_tool:meta_tool",      # Include meta_tool module
        "meta_tool_gui.py"
    ]

    # Add debug logging to capture PyInstaller errors
    command.extend(['--log-level', 'DEBUG'])

    try:
        subprocess.run(command, check=True)
        print("\nExecutable built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}")

if __name__ == "__main__":
    build_executable()
