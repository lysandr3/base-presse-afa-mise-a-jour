# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from pdf_to_df import pdf_to_df
import os
import boto3
from io import StringIO
from tempfile import NamedTemporaryFile
import pandas as pd

LOGGER = get_logger(__name__)


def run():
  st.set_page_config(
    page_title="BP MAJ",
    page_icon="",
  )
  st.header("Base Presse AFA - Mise à jour :")
  s3 = boto3.client('s3', aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'], aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])

  uploaded_file = st.file_uploader("Veuillez importer la dernière copie numérique transmise", type=["pdf"])
  if uploaded_file is not None:
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    db = pdf_to_df(temp_file.name)
    st.write(db)

    if st.button('Ajouter à la base de donnée ?'):
      response = s3.get_object(Bucket='base-presse-afa', Key='bp.csv')
      df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')))
      csv_buffer = StringIO()
      pd.concat([db,df],ignore_index=True).to_csv(csv_buffer, index=False)
      s3.put_object(Body=csv_buffer.getvalue(), Bucket='base-presse-afa', Key='bp.csv')
      st.success("Base de donnée mise à jour !")

if __name__ == "__main__":
    run()
