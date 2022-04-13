import torch
import numpy as np
import pandas as pd
from transformers import BertTokenizer

import logging
logging.basicConfig(level=logging.INFO)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
labels = {'Democrat': 0,
          'Republican': 1}



class Dataset(torch.utils.data.Dataset):
    def __init__(self, filename):
        self.labels = []
        self.texts = []

        # get csv to dataframe
        self.df = pd.read_csv(filename)

        # get labels and texts
        self.labels = [labels[label] for label in self.df['Party']]
        self.texts = [tokenizer(text, 
                               padding='max_length', max_length = 512, truncation=True,
                                return_tensors="pt") for text in self.df['Tweet']]
        

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        # Fetch a batch of inputs
        return self.texts[idx]

    def __getitem__(self, idx):

        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)

        return batch_texts, batch_y

dataset = Dataset('ExtractedTweets.csv')