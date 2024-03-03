from symbol_dto import SymbolDto

class CandlestickDto:
    Symbol      : SymbolDto
    Open        : str
    Close       : str
    High        : str
    Low         : str
    Volume      : str
    Interval    : str
    Start       : int
    End         : int
    Timestamp   : int
    Confirm     : bool