from datetime import datetime
from pyfiglet import Figlet

def date(fmt="%Y %d %b %A", font="graceful"):
    time_str = datetime.now().strftime(fmt)
    f = Figlet(font=font)
    return f.renderText(time_str)
