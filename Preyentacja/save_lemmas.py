# All imports
from pathlib import Path
from Lib import traceback
import os

from time import time
# from IPython.display import Video



# all_folder_names
images = Path("dataset/images")
sw_video = Path("dataset/star_wars_video")
sw_scripts = Path("dataset/star_wars_scripts")
all_scripts = Path("dataset/all_scripts")

sw_lemmas = Path("dataset/lemmas_star_wars")
all_lemmas = Path("dataset/lemmas_all_scripts")

# 1. wczytanie dokumentów

import spacy



def lematize_document(path, nlp):
    with open(path, "r", encoding="UTF-8") as file:
        text = file.read()
    if len(text) > 1000000:
        return []

    tokens = nlp(text)
    tokens = list(filter(lambda token: not (token.is_punct or token.is_space), tokens))
    #     for token in tokens:
    #         print(f"Token: {token.text:15} Lemma: {token.lemma_}")

    lemmas = list(map(lambda token: token.lemma_, tokens))
    return lemmas


def copy_lemmas_from_one_dir_to_another(source_dir, dest_dir):
    nlp = spacy.load('en_core_web_sm')

    cwd = os.getcwd()
    # already_done = set(os.listdir(dest_dir))
    try:
        os.chdir(source_dir)
        file_names = os.listdir()
        for i, doc_path in enumerate(file_names):
            # if doc_path not in already_done:
                doc_lemmas = lematize_document(doc_path, nlp)
                print(f"{doc_path} successfully parsed")

                os.chdir(cwd)
                os.chdir(dest_dir)
                doc_lemma_to_write = list(map(lambda lemma: lemma + "\n", doc_lemmas))
                with open(file_names[i], "w", encoding="UTF-8") as writer:
                    writer.writelines(doc_lemma_to_write)
                os.chdir(cwd)
                os.chdir(source_dir)

    except FileNotFoundError:
        traceback.print_exc()
    finally:
        os.chdir(cwd)

copy_lemmas_from_one_dir_to_another(sw_scripts, sw_lemmas)


# sw_words = get_words_in_scripts_from_dir(sw_scripts)
# doc_indexes = [1, 2, 3, 4, 5, 6, 7]  # from Phantom Menace to Force Awakenes
#
# no_words = sum(list(map(len, sw_words)))  # not neccessarly unique words
# print(f"Total number of words: {no_words}")