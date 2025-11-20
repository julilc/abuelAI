import warnings
warnings.filterwarnings("ignore")

import pandas as pd
print("importing chromadb...")

print("importing chromadb...")

import chromadb
from chromadb.config import Settings


print("importing langchain...")

from langchain.text_splitter import RecursiveCharacterTextSplitter

print("importing tesnorflowhub...")
import tensorflow_hub as hub

print("Importing sentence-transformer...")
from sentence_transformers import SentenceTransformer



import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import time 
import argparse
print("importing numpy...")

import numpy as np
import json


def chuncker(text):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=30)
  texts = text_splitter.split_text(text)
  return texts