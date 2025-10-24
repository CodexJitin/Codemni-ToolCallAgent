"""
Color utilities for terminal output.
Reusable across all agents.
"""


class Colors:
    """ANSI color codes for terminal output."""
    
    # Basic colors
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    
    # Additional colors
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    @staticmethod
    def colorize(text: str, color: str, bold: bool = False) -> str:
        """
        Colorize text with the specified color.
        
        Args:
            text: Text to colorize
            color: Color name (e.g., 'blue', 'green', 'red')
            bold: Whether to make text bold
            
        Returns:
            Colorized text string
        """
        color_map = {
            'blue': Colors.BLUE,
            'green': Colors.GREEN,
            'red': Colors.RED,
            'yellow': Colors.YELLOW,
            'cyan': Colors.CYAN,
            'magenta': Colors.MAGENTA,
            'white': Colors.WHITE,
        }
        
        color_code = color_map.get(color.lower(), '')
        bold_code = Colors.BOLD if bold else ''
        
        return f"{bold_code}{color_code}{text}{Colors.ENDC}"
    
    @staticmethod
    def print_header(text: str, width: int = 70, color: str = 'cyan'):
        """Print a formatted header."""
        color_code = getattr(Colors, color.upper(), Colors.CYAN)
        print(f"\n{color_code}{'─' * width}{Colors.ENDC}")
        print(f"{Colors.BOLD}{color_code}{text}{Colors.ENDC}")
        print(f"{color_code}{'─' * width}{Colors.ENDC}\n")
    
    @staticmethod
    def print_box(text: str, width: int = 70):
        """Print text in a box."""
        lines = text.split('\n')
        print("╔" + "═" * (width - 2) + "╗")
        for line in lines:
            padding = width - len(line) - 4
            print(f"║ {line}{' ' * padding} ║")
        print("╚" + "═" * (width - 2) + "╝")
