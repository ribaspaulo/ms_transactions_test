FROM python:3.12-slim-bullseye

RUN pip install --upgrade pip 
RUN pip install pandas==2.2.2 
RUN pip install requests==2.31.0 
RUN pip install streamlit==1.36.0 
RUN pip install streamlit-aggrid==1.1.4.post1
RUN pip install python-docx==1.1.2
RUN pip install openpyxl==3.1.5
RUN mkdir ms_transactions_test
RUN mkdir ms_transactions_test/.streamlit
RUN mkdir ms_transactions_test/uploads

COPY  ./*.py /ms_transactions_test
COPY  ./.streamlit/*.toml /ms_transactions_test/.streamlit
COPY  ./start.sh /ms_transactions_test/start.sh
COPY  ./uploads/*.* /ms_transactions_test/uploads

WORKDIR /ms_transactions_test

# Adicione o comando padrão para iniciar a aplicação
CMD ["sh", "start.sh"]