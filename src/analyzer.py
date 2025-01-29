def get_post_type(title: str) -> str:
    t = title.replace(" ", "")

    over_keywords = ["완료", r"\b완\b", r"\(완\)", r"\[완\]", r"<완>", r"-완-", r"-완\b", r"\b완-", "마감", "완판", "판완", "예약"]
    for keyword in over_keywords:
        if keyword in t:
            return "over"

    both_keywords = ["사고"]
    for keyword in both_keywords:
        if keyword in t:
            return "both"

    buy_keywords = ["삽니", "삼", "ㅅㅅ", "구입", "구매", "사요", "사는", "구합", "구해요", "구함", "괌", "찾아", "매입", "찾습"]
    for keyword in buy_keywords:
        if keyword in t:
            return "buy"

    sell_keywords = ["팝니", "팔아", "ㅍㅍ", "팜", "판매", "파는", "일괄", "정리", "떨이", "급처", "털어", "텁니", "터는", "세일"]
    for keyword in sell_keywords:
        if keyword in t:
            return "sell"

    return "none"

