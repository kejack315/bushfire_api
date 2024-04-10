from datetime import datetime


def log(level: str, text: str, end="\n") -> None:
    current_time = datetime.now().strftime("%d%m%y %H:%M:%S:%f")
    level_str = f"{level.upper()}:".ljust(10)
    print(f"{level_str}[{current_time}] {text}", end=end)
