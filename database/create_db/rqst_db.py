import warnings
warnings.filterwarnings("ignore")

import pandas as pd
print("importing chromadb...")
import chromadb
print("importing langchain...")

from langchain.text_splitter import RecursiveCharacterTextSplitter
print("importing chromadb...")

import tensorflow_hub as hub
print("importing tesnorflowhub...")

from chromadb.config import Settings

print("importing numpy...")

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import time 
import argparse
import numpy as np
import json


def chuncker(text):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=30)
  texts = text_splitter.split_text(text)
  return texts