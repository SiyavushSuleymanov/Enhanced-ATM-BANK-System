import json #we call json file that we create for languages translations
with open ('translations.json', 'r', encoding="utf-8") as file:  #'r'- means, it is just read mode and we cannot modify it, encoding="utf-8" means that it is used for non_English alphabets as Azerbaijanina or Russian chracater
    translations=json.load(file)

current_language="en"  #this is default language of our ATM

def transl(key): #this function gives you values of your keys
    return translations[current_language].get(key,key) #here, you get value of included key name, if there is no any key word as you entered, you will get key in current_language without translations


def lang_changer(lang):
    global current_language #we write global, for calling global variable for changing as local variable
    if lang in translations:  #we check that, is there any language in our translation json
        current_language=lang  #if yes, we change our language
