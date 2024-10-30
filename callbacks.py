from aiogram.filters.callback_data import CallbackData


class Curs(CallbackData, prefix="curs"):
    pass

class Calc(CallbackData, prefix="calc"):
    pass


class FAQ(CallbackData, prefix="faq"):
    num: int = None


class MakeOffer(CallbackData, prefix="MakeOffer"):
    pass

class FindOffer(CallbackData, prefix="FindOffer"):
    pass

class Back(CallbackData, prefix="Back"):
    pass


