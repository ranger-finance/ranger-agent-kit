from ranger_mcp.hub import ranger_mcp
import sys
from pathlib import Path

# Ensure the 'src' directory is in the Python path
# This is sometimes necessary when running as a script vs installed package
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now import the hub server


def main():
    # Run the main hub server
    # This will use stdio by default, compatible with Claude Desktop
    ranger_mcp.run(transport="sse")

if __name__ == "__main__":
    main()
