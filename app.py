import streamlit as st
import os
from openai import OpenAI
from groq import Groq
import os

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()


