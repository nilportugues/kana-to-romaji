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

    try:
        return any([range["from"] <= ord(char) <= range["to"] for range in ranges])
    except:
        return True

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
                    result1 = ""
                    if len(i) == 2 and len(i[1]) > 8:
                        try:
                            wordType = conv.do(i[1][2])
                            # family name. This is VERY Important.
                            if wordType == "jinmei": 
                                result1 = conv.do(i[1][7])                            
                            else:
                                result = ""
                        except:
                            result1 = "";                                

                    try:
                        result2 = conv.do(i[0])
                    except:
                        result2 = ""

                    if result1 == "":
                        # print("1-->r1: "+result1)
                        # print("1-->r2: "+result2)                        
                        finalResult = result2+" "
                    elif result2 != "" and result1 == "":
                        # print("2-->r1: "+result1)
                        # print("2-->r2: "+result2)                        
                        finalResult = result2+" "
                    elif result1 != "" and result2 == "":
                        # print("3-->r1: "+result1)
                        # print("3-->r2: "+result2)                                                
                        finalResult = result1+" "  
                    elif result1 != "" and result2 !="" and result2 != result1:    
                        # print(i)                                          
                        # print("5-->r1: "+result1)
                        # print("5-->r2: "+result2)                        
                        finalResult = result1+" "
                    else:
                        # print("4-->r1: "+result1)
                        # print("4-->r2: "+result2)                        
                        finalResult = result1+" "

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

# Test this with input:  "化身の獣, 馬飼野康二", output: "keshin no kemono , makaino kouji"