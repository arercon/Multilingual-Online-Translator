import requests, sys
from bs4 import BeautifulSoup


def get_words(soup, lang, word, len):
    with open(f"{word}.txt", "a") as file:
        file.write(f"\n{lang} Translations:\n")
        words_raw = soup.select("#translations-content .translation")[:len]
        for w in words_raw:
            file.write(w.text.strip() + "\n")


def get_sentences(soup, lang, word, len):
    with open(f"{word}.txt", "a") as file:
        file.write(f"\n{lang} Examples: \n")
        sentences_raw = soup.select("#examples-content .example .text")[:len * 2]
        div_counter = 0
        for sentence in sentences_raw:
            file.write(sentence.text.strip() + "\n")
            div_counter += 1
            if div_counter % 2 == 0:
                file.write("")


def get_translation(url, lang, word, len):
    user_agent = 'Mozilla/5.0'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if r.status_code == 404:
        print("Sorry, unable to find " + word)
        sys.exit()
    elif r.status_code != 200:
        print("Sorry, something is wrong with your connection")
        sys.exit()
    soup = BeautifulSoup(r.content, "html.parser")
    get_words(soup, lang, word, len)
    get_sentences(soup, lang, word, len)


def lang_dic(lang1):
    languages = {0:"all", 1: "Arabic", 2: "German", 3: "English", 4: "Spanish",
                 5: "French", 6: "Hebrew", 7: "Japanese", 8: "Dutch", 9: "Polish",
                 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}
    return languages[lang1]


def choose_lang(lang1, lang2, word=None):
    if word == None:  # first start
        args = sys.argv
        lang1 = args[1]
        lang2 = args[2]
        word = args[3]
        if lang1 not in [lang_dic(i).lower() for i in range(14)]:
            print("ERROR! Sorry, the program doesn't support " + lang1)
            sys.exit()
        elif lang2 not in [lang_dic(i).lower() for i in range(14)]:
            print("ERROR! Sorry, the program doesn't support " + lang2)
            sys.exit()
        with open(f"{word}.txt", "w") as file:
            file.write(f"You coose '{lang2}' as the language to translate '{word}' to.\n")
            return lang1, lang2, word
    else:
        url = f"https://context.reverso.net/translation/{lang1.lower()}-" \
              f"{lang2.lower()}/{word.lower()}"
        return url, lang2, word


def translator():
    lang1, lang2, word = choose_lang(0, 0)
    if lang2 != "all":
        url, lang, word = choose_lang(lang1, lang2, word)
        get_translation(url, lang2, word, 5)
    else:
        for i in range(13):
            if lang_dic(i + 1).lower() != lang1:
                url, lang2, word = choose_lang(lang1, lang_dic(i + 1).lower(), word)
                get_translation(url, lang2, word, 1)
    with open(f"{word}.txt") as file:
        print(file.read())


translator()
