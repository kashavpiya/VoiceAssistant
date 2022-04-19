from neuralnet.utils import TextProcess
import torch

textprocess = TextProcess()

labels = [
    "'",  # 0
    " ",  # 1
    "a",  # 2
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",  # 27
    "_",  # 28, blank
]


def DecodeGreedy(output, blank_label=28, collapse_repeated=True):
    arg_maxes = torch.argmax(output, dim=2).squeeze(1)
    decode = []
    for i, index in enumerate(arg_maxes):
        if index != blank_label:
            if collapse_repeated and i != 0 and index == arg_maxes[i - 1]:
                continue
            decode.append(index.item())
    return textprocess.int_to_text_sequence(decode)
