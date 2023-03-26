""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.
'''


"""
_pad        = '_'
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"


# Export all symbols:
symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

# Special symbol ids
SPACE_ID = symbols.index(" ")

print(SPACE_ID)
"""

# 日本語用
_pad        =  ['_']
_punctuation = ["^","[","#","]","?","$"]
_letters_ipa = ["a","b","by","ch","cl","d","dy","e","f","g","gy","h","hy","i","j","k","ky","m","my","n","N","ny","o","p","py","r","ry","s","sh","t","ts","ty","u","v","w","y","z",]

# シンボル出力:
symbols = list()
symbols.extend(_pad)
symbols.extend(_punctuation)
symbols.extend(_letters_ipa)

# print(symbols)

# スペースシンボル
# SPACE_ID = None    # symbols.index(" ")
