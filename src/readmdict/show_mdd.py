def check_readmdict_availability():
    """Check if readmdict is available and properly configured."""
    try:
        from .readmdict import MDD
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    import argparse
    import os
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze and display contents of MDD files')
    parser.add_argument('mdd_file', nargs='?', 
                       help='Path to the MDD file to analyze')
    args = parser.parse_args()
    
    # If no MDD file is provided, print help and exit
    if not args.mdd_file:
        parser.print_help()
        return
    
    mdd_file = args.mdd_file

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
        from .readmdict import MDD
        import os

        # Check if MDD file exists
        if not os.path.exists(mdd_file):
            print(f"MDD file not found at {mdd_file}")
            return

        # Load MDD file
        print(f"Loading MDD file: {mdd_file}")
        mdd = MDD(mdd_file)

        # Convert MDD items to a list for easier handling
        mdd_items = list(mdd.items())
        print(f"Successfully loaded MDD file with {len(mdd_items)} items")
        print("=" * 70)

        # Categorize files by type
        image_files = []
        css_files = []
        js_files = []
        audio_files = []
        other_files = []

        for filename, content in mdd_items:
            filename_str = filename.decode("utf-8", errors="ignore")
            if filename_str.lower().endswith((".jpg", ".png", ".gif", ".bmp", ".jpeg")):
                image_files.append((filename_str, content))
            elif filename_str.lower().endswith(".css"):
                css_files.append((filename_str, content))
            elif filename_str.lower().endswith(".js"):
                js_files.append((filename_str, content))
            elif filename_str.lower().endswith((".wav", ".mp3", ".ogg", ".m4a")):
                audio_files.append((filename_str, content))
            else:
                other_files.append((filename_str, content))

        # Display summary
        print(f"File type summary:")
        print(f"  Images: {len(image_files)}")
        print(f"  CSS files: {len(css_files)}")
        print(f"  JavaScript files: {len(js_files)}")
        print(f"  Audio files: {len(audio_files)}")
        print(f"  Other files: {len(other_files)}")
        print()

        # Show first 10 image files
        if image_files:
            print("First 10 image files:")
            for i, (filename, content) in enumerate(image_files[:10]):
                print(f"  {i + 1}. {filename} ({len(content)} bytes)")
            print()

        # Show all CSS files (if any)
        if css_files:
            print("CSS files:")
            for i, (filename, content) in enumerate(css_files):
                try:
                    css_text = content.decode("utf-8", errors="ignore")
                    print(f"  {i + 1}. {filename} ({len(css_text)} characters)")
                    print(
                        f"     Preview: {css_text[:200]}{'...' if len(css_text) > 200 else ''}"
                    )
                except:
                    print(f"  {i + 1}. {filename} ({len(content)} bytes) [Binary]")
            print()

        # Show all JavaScript files (if any)
        if js_files:
            print("JavaScript files:")
            for i, (filename, content) in enumerate(js_files):
                try:
                    js_text = content.decode("utf-8", errors="ignore")
                    print(f"  {i + 1}. {filename} ({len(js_text)} characters)")
                    print(
                        f"     Preview: {js_text[:200]}{'...' if len(js_text) > 200 else ''}"
                    )
                except:
                    print(f"  {i + 1}. {filename} ({len(content)} bytes) [Binary]")
            print()

        # Show first 5 audio files
        if audio_files:
            print("First 5 audio files:")
            for i, (filename, content) in enumerate(audio_files[:5]):
                print(f"  {i + 1}. {filename} ({len(content)} bytes)")
            print()

        # Show first 10 other files
        if other_files:
            print("First 10 other files:")
            for i, (filename, content) in enumerate(other_files[:10]):
                try:
                    # Try to decode as text
                    text_content = content.decode("utf-8", errors="ignore")
                    if len(text_content.strip()) > 0 and all(
                        ord(c) < 128 for c in text_content[:100]
                    ):
                        print(
                            f"  {i + 1}. {filename} (text, {len(text_content)} characters)"
                        )
                        print(
                            f"     Preview: {text_content[:200]}{'...' if len(text_content) > 200 else ''}"
                        )
                    else:
                        print(f"  {i + 1}. {filename} ({len(content)} bytes) [Binary]")
                except:
                    print(f"  {i + 1}. {filename} ({len(content)} bytes) [Binary]")
            print()

        print("\nMDD file analysis complete.")

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
