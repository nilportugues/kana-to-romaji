# coding=utf-8
import MeCab
from pykakasi import kakasi,wakati
import json
import re

class KakasiSingleton:
   __instance = None

   @staticmethod 
   def getInstance():
      """ Static access method. """
      if KakasiSingleton.__instance == None:
         KakasiSingleton()
      return KakasiSingleton.__instance

   def __init__(self):
      """ Virtually private constructor. """
      if KakasiSingleton.__instance != None:
         raise Exception("This class is a KakasiSingleton!")
      else:
        _kakasi = kakasi()
        _kakasi.setMode("H","a") # Hiragana to ascii, default: no conversion
        _kakasi.setMode("K","a") # Katakana to ascii, default: no conversion
        _kakasi.setMode("J","a") # Japanese to ascii, default: no conversion
        KakasiSingleton.__instance = _kakasi


class KakasiConverterSingleton:
   __instance = None

   @staticmethod 
   def getInstance():
      """ Static access method. """
      if KakasiConverterSingleton.__instance == None:
         KakasiConverterSingleton()
      return KakasiConverterSingleton.__instance

   def __init__(self):
      """ Virtually private constructor. """
      if KakasiConverterSingleton.__instance != None:
         raise Exception("This class is a KakasiConverterSingleton!")
      else:
        KakasiConverterSingleton.__instance = KakasiSingleton.getInstance().getConverter()


class MeCabSingleton:
   __instance = None

   @staticmethod 
   def getInstance():
      """ Static access method. """
      if MeCabSingleton.__instance == None:
         MeCabSingleton()
      return MeCabSingleton.__instance

   def __init__(self):
      """ Virtually private constructor. """
      if MeCabSingleton.__instance != None:
         raise Exception("This class is a MeCabSingleton!")
      else:      
        MeCabSingleton.__instance = MeCab.Tagger("")




def is_number(s):
    """ Returns True is string is a number. """
    return s.replace('.','',1).isdigit()


def is_cjk(char):
    ranges = [
      {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
      {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
      {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
      {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
      {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
      {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
      {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
      {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
      {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
      {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
      {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
      {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
      {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
    ]    

    return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def is_japanese(string):
    i = 0
    while i<len(string):
        if is_cjk(string[i]):
            return True
        i += 1

    return False    

conv = KakasiConverterSingleton.getInstance() 

class JapaneseToRomaji():

    def convert(self, inputText):
      
        input = inputText
        input = input.replace(" ", "**SPACE**")
        lines = input.splitlines()

        ## Prepare response with dict
        romanized = []

        for line in lines:
            text = line
          
            chunklines = MeCabSingleton.getInstance().parse(text).splitlines()[:-1]    
            parsed = [[chunk.split('\t')[0], tuple(chunk.split('\t')[1].split(',')) ] for chunk in chunklines]

            ## Parse
            romanizedLine = []
            for i in parsed:
                #now for each i[0] do romaji
               
                finalResult = None

                # ignore calculation if initial string is numeric
                if is_number(i[0]):
                    finalResult = ""+i[0]

                # ignore calculation if string has non JP chars
                if finalResult == None and is_japanese(i[0]) == False:
                    finalResult = i[0]                    

                if finalResult == None:    
                    result1 = None
                    if len(i) == 2 and len(i[1]) > 8:
                        result1 = conv.do(i[1][7])

                    result2 = conv.do(i[0])

                    if result1 == None:
                        finalResult = result2+" "
                    elif result1 != None and result2 != result1:
                        finalResult = result1+" "
                    else:
                        finalResult = result2+" "

#                print("r1 "+result1)
#                print("r2 "+result2)
                romanizedLine.append(finalResult)


            pair = {}    
            romanizedLine = "".join(romanizedLine)
                

            romanizedLine = romanizedLine.replace("\nkunga ", "\nkimi ")
            romanizedLine = romanizedLine.replace(" kunga ", " kimi ")

            romanizedLine = romanizedLine.replace(" ha ", " wa ")

            ## Collapse っ
            #k
            romanizedLine = romanizedLine.replace("tsu ka ", "tsuka")
            romanizedLine = romanizedLine.replace("tsu ke ", "kke")
            romanizedLine = romanizedLine.replace("tsu ki ", "kki")
            romanizedLine = romanizedLine.replace("tsu ko ", "kko")
            romanizedLine = romanizedLine.replace("tsu ku ", "kku")

            ## Collapse っ
            #s
            romanizedLine = romanizedLine.replace("tsu sa ", "ssa")
            romanizedLine = romanizedLine.replace("tsu se ", "sse")
            romanizedLine = romanizedLine.replace("tsu si ", "ssi")
            romanizedLine = romanizedLine.replace("tsu so ", "sso")
            romanizedLine = romanizedLine.replace("tsu su ", "ssu")

            ## Collapse っ
            #t
            romanizedLine = romanizedLine.replace("tsu ta ", "tta")
            romanizedLine = romanizedLine.replace("tsu te ", "tte")
            romanizedLine = romanizedLine.replace("tsu ti ", "tti")
            romanizedLine = romanizedLine.replace("tsu to ", "tto")
            romanizedLine = romanizedLine.replace("tsu tu ", "ttu")

            ## Collapse っ
            #p
            romanizedLine = romanizedLine.replace("tsu pa ", "ppa")
            romanizedLine = romanizedLine.replace("tsu pe ", "ppe")
            romanizedLine = romanizedLine.replace("tsu pi ", "ppi")
            romanizedLine = romanizedLine.replace("tsu po ", "ppo")

            ## Dangling letters
            romanizedLine = romanizedLine.replace(" u ", "u ")
            romanizedLine = romanizedLine.replace(" i ", "i ")

            ## Other fixes, after tsu particle
            romanizedLine = romanizedLine.replace(" nai ", "nai ")
            romanizedLine = romanizedLine.replace(" ta ", "ta ")
            romanizedLine = romanizedLine.replace(" te ", "te ")
            romanizedLine = romanizedLine.replace(" ten ", "ten ")
            romanizedLine = romanizedLine.replace(" ku ", "ku ")
            romanizedLine = romanizedLine.replace(" ba ", "ba ")
            romanizedLine = romanizedLine.replace(" ka ", "ka ")
            romanizedLine = romanizedLine.replace(" ze ", "ze ")
            romanizedLine = romanizedLine.replace(" ga ", "ga ")
            romanizedLine = romanizedLine.replace(" re ", "re ")

            ## Extended letters
            romanizedLine = romanizedLine.replace("a-", "ā")
            romanizedLine = romanizedLine.replace("e-", "ē")
            romanizedLine = romanizedLine.replace("i-", "ī")
            romanizedLine = romanizedLine.replace("o-", "ō")
            romanizedLine = romanizedLine.replace("u-", "ū")
            
            ## Special characters / Punctuation
            ## https://en.wikipedia.org/wiki/List_of_Japanese_typographic_symbols

            romanizedLine = romanizedLine.replace("「", "'")
            romanizedLine = romanizedLine.replace("」", "'")
            romanizedLine = romanizedLine.replace("『", "\"")
            romanizedLine = romanizedLine.replace("』", "\"")
            romanizedLine = romanizedLine.replace("（", "(")
            romanizedLine = romanizedLine.replace("）", ")")
            romanizedLine = romanizedLine.replace("〔", "[")
            romanizedLine = romanizedLine.replace("〕", "]")
            romanizedLine = romanizedLine.replace("［", "[")
            romanizedLine = romanizedLine.replace("］", "]")
            romanizedLine = romanizedLine.replace("｛", "{")
            romanizedLine = romanizedLine.replace("｝", "}")
            romanizedLine = romanizedLine.replace("｟", "((")
            romanizedLine = romanizedLine.replace("｠", "))")
            romanizedLine = romanizedLine.replace("〈", "‹")
            romanizedLine = romanizedLine.replace("〉", "›")
            romanizedLine = romanizedLine.replace("《", "«")
            romanizedLine = romanizedLine.replace("》", "»")
            romanizedLine = romanizedLine.replace("【", "[")
            romanizedLine = romanizedLine.replace("】", "]")
            romanizedLine = romanizedLine.replace("〖", "[")
            romanizedLine = romanizedLine.replace("〗", "]")
            romanizedLine = romanizedLine.replace("〘", "[")
            romanizedLine = romanizedLine.replace("〙", "]")
            romanizedLine = romanizedLine.replace("〚", "[")
            romanizedLine = romanizedLine.replace("〛", "]")
            romanizedLine = romanizedLine.replace("。", ".")
            romanizedLine = romanizedLine.replace("、", ",")
            romanizedLine = romanizedLine.replace("・", "·")
            romanizedLine = romanizedLine.replace("゠", "–")
            romanizedLine = romanizedLine.replace("＝", "—")
            romanizedLine = romanizedLine.replace("…", "...")
            romanizedLine = romanizedLine.replace("‥", "..")            
            
            ## Custom tokens and fixes
            romanizedLine = romanizedLine.replace("**SPACE**", " ")
            text = text.replace("**SPACE**", " ")

            ## Remove multiple spaces
            romanizedLine = romanizedLine.strip()
            romanizedLine = " ".join(romanizedLine.split())

            

            pair[text] = romanizedLine.strip()
            romanized.append(pair)

        return romanized


input = u'''
クラクションに佇む灯り
命を差し出して
今にも崩れそうになる
時にディストラクション

甘い甘いキスを呼ぶように
暗い深い闇に溺れてくんだ

クラクションの音を食した
渋谷街頭の夜に
色づく髪つかみ飛ばす
潔く死にたい人
渦巻く性の欲望
途端にこだまさせて

ワガママで誤摩化さないで
ワガママは勝手でしょ？
誰かを守りたいと独り嘆く
ワガママで誤摩化さないで
ワガママに嫉妬して
沈んでは浮かぶ子供の匂いがした

甘い甘いキスで確かめて
暗い深い愛に溺れてく

また飛ぶ考えられない霧中浮遊
解放する
今にも崩れそうな面影
誰のために今を生きて
誰のために愛を確かめる？
時に視界映る美には
リスクの逆さ言葉が似合う

ワガママで誤摩化さないで
ワガママは勝手でしょ？
思いもよらない言葉降り注ぐ
ワガママの意味を知らない
ワガママが合図でしょ？
沈んでは浮かぶ子供の血を好んだ

クラクションの音は止まらない
交差点突き抜けて
光に合わせ踊った幻覚と現実を
重ね狂う

失ってやっと気づいた
本当のその意味に
独りきりの夜が朝を迎える
誰かに愛され　そして
誰かを愛す時
今までの過去にさよなら告げて
ワガママにそっと愛を付け足して

甘い甘いキスを呼ぶように

足下コンクリートの香り
ほら　また始まる
あの日の見苦しい僕の姿は
もう此処にはないから
'''


