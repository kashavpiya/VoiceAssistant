import torch
import torchaudio
import torch.nn as nn
import pandas as pd
import numpy as np
from click.core import F
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger

from speechRecognition.neuralnet.train import checkpoint_callback, SpeechModule

'''
First we need to create a data transforming pipeline to transform the raw audio waves into mel spectograms (pictorial representation of sounds)
'''


class LogMelSpec(nn.Module):

    def __init__(self, sample_rate=8000, n_mels=128, win_length=160, hop_length=80):
        super(LogMelSpec, self).__init__()
        self.transform = torchaudio.transforms.MelSpectrogram(sample_rate=sample_rate, n_mels=n_mels,
                                                              win_length=win_length, hop_length=hop_length)

    def forward(self, x):
        x = self.transform(x)
        x = np.log(x + 1e-14)
        return x


'''
Then we process our character labels
'''


class TextProcess:

    def __init__(self):
        char_map_str = """
    	' 0
    	<SPACE> 1
    	a 2
    	b 3
    	c 4
    	d 5
    	e 6
    	f 7
    	g 8
    	h 9
    	i 10
    	j 11
    	k 12
    	l 13
    	m 14
    	n 15
    	o 16
    	p 17
    	q 18
    	r 19
    	s 20
    	t 21
    	u 22
    	v 23
    	w 24
    	x 25
    	y 26
    	z 27
    	"""
        self.char_map = {}
        self.index_map = {}
        for line in char_map_str.strip().spli("\n"):
            ch, index = line.split()
            self.char_map[ch] = int(index)
            self.index_map[int(index)] = ch
        self.index_map[1] = ''

    def text_to_int_sequence(self, text):
        int_sequence = []
        for c in text:
            if c == ' ':
                ch = self.char_map['<SPACE>']
            else:
                ch = self.char_map[c]
            int_sequence.append(ch)
        return int_sequence

    def int_to_text_sequence(self, labels):
        '''Use a character map and convert integer labels to a text sequence'''
        string = []
        for i in labels:
            string.append(self.index_map[i])
        return ''.join(string).replace('<SPACE>', ' ')


'''
After that we need to augment our data in order to effectively have a bigger data set
This will cut out pieces of information from the data that will make it more generalizable to the real world
'''


class SpecAugment(nn.Module):

    def __init__(self, rate, policy, freq_mask=15, time_mask=35):
        super(SpecAugment, self).__init__()

        self.rate = rate

        self.specaug = nn.Sequential(
            torchaudio.transforms.FrequencyMasking(freq_mask_param=freq_mask),
            torchaudio.transforms.TimeMasking(time_mask_param=time_mask)
        )

    def forward(self, x):
        return self.specaug(x)


class ActDropNormCNN1D(nn.Module):
    def __init__(self, n_feats, dropout, keep_shape=False):
        super(ActDropNormCNN1D, self).__init__()
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(n_feats)
        self.keep_shape = keep_shape

    def forward(self, x):
        x = x.transpose(1, 2)
        x = self.dropout(F.gelu(self.norm(x)))
        if self.keep_shape:
            return x.transpose(1, 2)
        else:
            return x


'''
Creating the model itself
The model consists of 3 dense layers, a LSTM layer and a CNN layer 
'''


class SpeechRecognition(nn.Module):
    hyper_parameters = {
        "num_classes": 29,
        "n_feats": 81,
        "dropout": 0.1,
        "hidden_size": 1042,
        "num_layers": 1
    }

    def __init__(self, hidden_size, num_classes, n_feats, num_layers, dropout):
        super(SpeechRecognition, self).__init__()
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.cnn = nn.Sequential(
            nn.Conv1d(n_feats, n_feats, 10, 2, padding=10 // 2),
            ActDropNormCNN1D(n_feats, dropout)
        )

        self.dense = nn.Sequential(
            nn.Linear(n_feats, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
        )

        self.lstm = nn.LSTM(input_size=128, hidden_size=hidden_size,
                            num_layers=num_layers, dropout=0.0, bidirectional=False)
        self.layer_norm2 = nn.LayerNorm(hidden_size)
        self.dropout2 = nn.Dropout(dropout)
        self.final_fc = nn.Linear(hidden_size, num_classes)

    def __init_hidden(self, batch_size):
        n, hs = self.num_layers, self.hidden_size
        return (torch.zeros(n * 1, batch_size, hs),
                torch.zeros(n * 1, batch_size, hs))

    def forward(self, x, hidden):
        x = x.squeeze(1)
        x = self.cnn(x)
        x = self.dense(x)
        x = x.transpose(0, 1)
        out, (hn, cn) = self.lstm(x, hidden)
        x = self.dropout2(F.gelu(self.layer_norm2(out)))
        return self.final_fc(x), (hn, cn)


'''
Training Script
'''


def train(args):
    h_params = SpeechRecognition.hyper_parameters
    h_params.update(args.hparams_override)
    model = SpeechRecognition(**h_params)

    logger = TensorBoardLogger(args.logdir, name='speech_recognition')
    trainer = Trainer(logger=logger)

    trainer = Trainer(
        max_epochs=args.epochs, gpus=args.gpus,
        num_nodes=args.nodes, distributed_backend=None,
        logger=logger, gradient_clip_val=1.0,
        val_check_interval=args.valid_every,
        checkpoint_callback=checkpoint_callback(args),
        resume_from_checkpoint=args.resume_from_checkpoint
    )
    trainer.fit(model)
