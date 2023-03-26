import pyopenjtalk, re
from packaging.version import parse as V



def pyopenjtalk_g2p_prosody_with_questioin(text, drop_unvoiced_vowels=True):

    labels = _extract_fullcontext_label(text)
    N = len(labels)

    with_question_ph_list = []
    
    kana = pyopenjtalk.g2p(text, True)
    for word in " ".join(kana).split(" "):
        ph = pyopenjtalk.g2p(word, kana=False)

        # ?があれば、?を追加して終わり
        if word == "?" or word=="？":
            with_question_ph_list.append("?")
            continue

        # その他の""は
        if ph == "":
            continue

        for t in ph.split(" "):
            with_question_ph_list.append(t)
            continue
        

    phones = []

    for n in range(N):


        lab_curr = labels[n]

        # current phoneme
        p3 = re.search(r"\-(.*?)\+", lab_curr).group(1)

        # deal unvoiced vowels as normal vowels
        if drop_unvoiced_vowels and p3 in "AEIOU":
            p3 = p3.lower()

        # 公式g2pと、質問文ありのやつを合体
        try:
            check_ph = with_question_ph_list[0]
        except:
            check_ph = "ENDENDEND"
            
        if len(with_question_ph_list) != 0:
            if check_ph == "?":
                phones.append("?")
                with_question_ph_list.pop(0)
            if p3 == check_ph:
                with_question_ph_list.pop(0)
        # deal with sil at the beginning and the end of text
        if p3 == "sil":
            assert n == 0 or n == N - 1
            if n == 0:
                phones.append("^")
            elif n == N - 1:
                # check question form or not
                e3 = _numeric_feature_by_regex(r"!(\d+)_", lab_curr)
                if e3 == 0:
                    phones.append("$")
                elif e3 == 1:
                    phones.append("?")
            continue
        elif p3 == "pau":
            phones.append("_")
            continue
        else:
            phones.append(p3)

        # accent type and position info (forward or backward)
        a1 = _numeric_feature_by_regex(r"/A:([0-9\-]+)\+", lab_curr)
        a2 = _numeric_feature_by_regex(r"\+(\d+)\+", lab_curr)
        a3 = _numeric_feature_by_regex(r"\+(\d+)/", lab_curr)

        # number of mora in accent phrase
        f1 = _numeric_feature_by_regex(r"/F:(\d+)_", lab_curr)

        a2_next = _numeric_feature_by_regex(r"\+(\d+)\+", labels[n + 1])
        # accent phrase border
        if a3 == 1 and a2_next == 1 and p3 in "aeiouAEIOUNcl":
            phones.append("#")
        # pitch falling
        elif a1 == 0 and a2_next == a2 + 1 and a2 != f1:
            phones.append("]")
        # pitch rising
        elif a2 == 1 and a2_next == 2:
            phones.append("[")
    
    rmv_idx_list= list()
    for idx in range(len(phones) -1):
        ph_1 = phones[idx]
        ph_2 = phones[idx+1]

        if ph_1 == "?" and ph_2 == "_":
            rmv_idx_list.append(idx+1)
        elif ph_1 == "?" and ph_2 == "?":
            rmv_idx_list.append(idx+1)
    
    for idx, rmv_idx in enumerate(rmv_idx_list):
        phones.pop(rmv_idx - idx)
    
    return phones

def _numeric_feature_by_regex(regex, s):
    match = re.search(regex, s)
    if match is None:
        return -50
    return int(match.group(1))

def _extract_fullcontext_label(text):

    if V(pyopenjtalk.__version__) >= V("0.3.0"):
        return pyopenjtalk.make_label(pyopenjtalk.run_frontend(text))
    else:
        return pyopenjtalk.run_frontend(text)[1]

def main():
    phonome = pyopenjtalk_g2p_prosody_with_questioin("とてもつらい。なぜつらいか？それも分からない。")
    print(phonome)
    return 0



if __name__ =="__main__":
    main()