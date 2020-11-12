class log:
    RESET = '\u001b[0m'

    FG_BLACK = '\u001b[30m'
    FG_ED = '\u001b[31m'
    FG_GREEN = '\u001b[32m'
    FG_YELLOW = '\u001b[33m'
    FG_BLUE = '\u001b[34m'
    FG_MAGENTA = '\u001b[35m'
    FG_CYAN = '\u001b[36m'
    FG_WHITE = '\u001b[37m'

    BG_BLACK = '\u001b[40m'
    BG_RED = '\u001b[41m'
    BG_GREEN = '\u001b[42m'
    BG_YELLOW = '\u001b[43m'
    BG_BLUE = '\u001b[44m'
    BG_MAGENTA = '\u001b[45m'
    BG_CYAN = '\u001b[46m'
    BG_WHITE = '\u001b[47m'

    BOLD = '\u001b[1m'
    UNDERLINE = '\u001b[4m'
    REVERSED = '\u001b[7m'

    @staticmethod
    def warning(message):
        log.colourprint('WARNING: ' + message, log.FG_YELLOW, log.UNDERLINE)

    @staticmethod
    def error(message):
        log.colourprint(message, log.FG_BLACK, log.BG_RED)

    @staticmethod
    def colourprint(message, *args):
        print(''.join(args) + message + log.RESET)