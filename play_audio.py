import os
import tempfile
import subprocess
import sys


def check_readmdict_availability():
    """Check if readmdict is available and properly configured."""
    try:
        import readmdict
        from readmdict import MDD

        return True, None
    except Exception as e:
        return False, str(e)


def play_audio_file(audio_data, filename):
    """Play audio data using system audio player."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        print(f"Playing {filename}...")

        # Try different audio players based on the system
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", temp_path], check=True)
        elif sys.platform == "linux":
            # Try common Linux audio players
            players = ["mpg123", "mpv", "vlc", "mplayer"]
            for player in players:
                try:
                    subprocess.run(
                        [player, temp_path],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            else:
                print(
                    "No suitable audio player found. Please install mpg123, mpv, vlc, or mplayer."
                )
                return False
        elif sys.platform == "win32":  # Windows
            os.startfile(temp_path)
        else:
            print(f"Unsupported platform: {sys.platform}")
            return False

        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass

        return True

    except subprocess.CalledProcessError:
        print(f"Error playing {filename}")
        return False
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False


def main():
    # Path to the webster MDD file
    mdd_file = "/Users/gerenkai/renkai-lab/rust-readmdict/example_resources/webster.mdd"

    # Check if readmdict is available
    is_available, error_msg = check_readmdict_availability()

    if not is_available:
        print("Error: readmdict library is not properly installed or configured.")
        print("This is likely due to missing python-lzo dependency.")
        print("\nTo fix this issue:")
        print("1. Install LZO library: brew install lzo")
        print("2. Install python-lzo: uv add python-lzo")
        if error_msg:
            print(f"\nError details: {error_msg}")
        return

    try:
        from readmdict import MDD

        # Check if MDD file exists
        if not os.path.exists(mdd_file):
            print(f"MDD file not found at {mdd_file}")
            return

        # Load MDD file
        print(f"Loading MDD file: {mdd_file}")
        mdd = MDD(mdd_file)

        # Find all audio files
        audio_files = []
        for filename, content in mdd.items():
            filename_str = filename.decode("utf-8", errors="ignore")
            if filename_str.lower().endswith((".mp3", ".wav", ".ogg", ".m4a")):
                audio_files.append((filename_str, content))

        print(f"Found {len(audio_files)} audio files")

        if not audio_files:
            print("No audio files found in the MDD file.")
            return

        # Play first 10 audio files automatically
        files_to_play = audio_files[:10]
        print(f"\nPlaying {len(files_to_play)} audio files sequentially...")

        for i, (filename, content) in enumerate(files_to_play):
            print(f"\n[{i + 1}/{len(files_to_play)}] {filename} ({len(content)} bytes)")
            success = play_audio_file(content, filename)
            if not success:
                print(f"Failed to play {filename}")

        print("\nFinished playing all audio files.")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        print("Please check if the file path is correct.")
    except Exception as e:
        print(f"Error reading MDD file: {e}")
        if "lzo" in str(e).lower():
            print("\nThis error is likely related to missing LZO compression support.")
            print("Please install the LZO library and python-lzo package.")


if __name__ == "__main__":
    main()
