over_keywords = ["완료", r"\b완\b", r"\(완\)", r"\[완\]", r"<완>", r"-완-", r"-완\b", r"\b완-", "마감", "완판", "판완", "예약"]
both_keywords = ["사고"]
buy_keywords = ["삽니", "삼", "ㅅㅅ", "구입", "구매", "사요", "사는", "구합", "구해요", "구함", "괌", "찾아", "매입", "찾습"]
buy_keywords_light = ["삽니", "삼", "ㅅㅅ", "구입", "구매"]
sell_keywords = ["팝니", "팔아", "ㅍㅍ", "팜", "판매", "파는", "일괄", "정리", "떨이", "급처", "털어", "텁니", "터는", "세일"]
sell_keywords_light = ["팝니", "팔아", "ㅍㅍ", "팜", "판매"]

def get_post_type(title: str) -> str:
    t = title.replace(" ", "")

    for keyword in over_keywords:
        if keyword in t:
            return "over"

    for keyword in both_keywords:
        if keyword in t:
            return "both"

    for keyword in buy_keywords:
        if keyword in t:
            return "buy"

    for keyword in sell_keywords:
        if keyword in t:
            return "sell"

    return "none"

