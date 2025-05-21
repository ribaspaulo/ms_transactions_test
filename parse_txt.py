import pandas as pd
import codecs
from docx import Document

import sys
import re
import json

UPLOAD_DIR = 'uploads'

def read_docx_tables(filename:str, idx_data:int, row_ini:int, has_header=True):
    """Lê tabelas existentes em um arquivo do tipo docx

    Args:
        filename (str): caminho e nome do arquivo a ser analisado.
        idx_data (int): posição do array onde se encontram os dados.
        row_ini (int): linha da qual deve ser iniciada a leitura dos dados.
        has_header (bool, optional): existe cabeçalho na tabela? Defaults to True.

    Returns:
        list: lista de DataFrames com o conteúdo das tabelas encontradas.
    """    
    doc = Document(filename)
    tables = []
    
    for table in doc.tables:
        data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            data.append(row_data)
        
        if has_header and data:
            df = pd.DataFrame(data[row_ini:], columns=data[idx_data])
        else:
            df = pd.DataFrame(data[row_ini:])
        tables.append(df)
        
    return tables


def extract_txt_to_dataframe(tables:list, data_file:str, no_cols:list, desc_col:int, start_col:int, end_col:int): 
    """Extrai dados de um arquivo txt e gera um arquivo xlsx

    Args:
        tables (list): lista de Dataframes com o dicionário de dados.
        data_file (str): caminho e nome do arquivo txt de onde os dados devem ser extraídos.
        no_cols (list): colunas do dicionário de dados que devem ser ignoradas.
        desc_col (int): coluna do dicionário onde se encontra o rótulo da coluna de dados.
        start_col (int): posição de início de uma coluna de dados.
        end_col (int): posição final de uma coluna de dados.

    Returns:
        Dataframe: Dataframe contendo os dados extraídos do arquivo txt
    """ 
    try:
        with codecs.open(data_file) as fileobj:
            data = fileobj.readlines()
        
        ishead = True
        reportdata = []
        for d in data:
            ds = d.strip().replace(';',' ')
            lin = ""
            cols_name = ""
            for col in tables[0].itertuples():
                if col[desc_col].strip() not in no_cols:
                    cols_name = cols_name + col[desc_col] + ';'
                    lin = lin + ds[int(col[start_col])-1:int(col[end_col])] + ';'
            if ishead:
                lables = cols_name.split(";")
                ishead = False
            reportdata.append(lin.split(";"))
        df = pd.DataFrame(data=reportdata[1:],columns=lables)
        df_clean = df.map(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)       
        try:
            return df_clean
        except:
            return
    except:
        print("File does not exist or cannot be parsed")   


def get_txt_init_info(data_txt):
    try:
        account_list = data_txt.iloc[0, 1]
        start_date = data_txt.iloc[:-1, 5].min()
        end_date = data_txt.iloc[:-1, 5].max()

        return {'bank_report_type': 'Transactions', 'start_date': start_date, 'end_date': end_date, 'account': account_list, "transactions": []}
    except:
        return ValueError("File does not exist or cannot be parsed")

def get_txt(data_txt):
    transactions_list = []
    for data_row in data_txt[:-1].itertuples():
        try:
            total_amount = float(data_row[16].replace('+','').replace('-',''))
            accrued_interest = float(data_row[11].replace('+','').replace('-',''))
        except:
            total_amount = 0.00
        if(total_amount > 0.0):
            transactions_list.append(
                                    {
                                        'account': data_row[2],
                                        'cusip': data_row[3],
                                        'payee': data_row[1],
                                        'type': 'N/A',
                                        'date': str(data_row[6]),
                                        'user_date': 'N/A',
                                        'memo': data_row[46],
                                        'amount': total_amount,
                                        'id': data_row[2],
                                        'sic': 'N/A',
                                        'mmc': 'N/A',
                                        'checksum': 'N/A',
                                    })
        if(accrued_interest > 0.0):
            transactions_list.append(
                                    {
                                        'account': data_row[2],
                                        'cusip': data_row[3],
                                        'payee': data_row[1],
                                        'type': 'N/A',
                                        'date': str(data_row[6]),
                                        'user_date': 'N/A',
                                        'memo': 'ACCURED',
                                        'amount': accrued_interest,
                                        'id': data_row[2],
                                        'sic': 'N/A',
                                        'mmc': 'N/A',
                                        'checksum': 'N/A',
                                    })            
    return transactions_list

# if __name__ == '__main__':
def exec_parse(txt_file:str, form_file = 'Formats-TRANSACTION.docx'): 
    form_file = form_file

    tables = read_docx_tables(f'./{UPLOAD_DIR}/{form_file}', 2, 8)
    no_cols = ['','Blank', 'Delimiter', 'Trailer Record']
    desc_col = 1
    start_col = 2 
    end_col = 3
    data_file = f'./{UPLOAD_DIR}/{txt_file}'
    data_txt = extract_txt_to_dataframe(tables,data_file, no_cols, desc_col, start_col, end_col)
    data_txt.to_excel(f'{data_file[:-4]}.xlsx')
    ini_info = get_txt_init_info(data_txt)
    trans_info = get_txt(data_txt)
    
    ini_info["transactions"] = trans_info
       
    return    ini_info

# Preprocessamento dos dados para criar estrutura hierárquica
def prepare_tree_data(json_data):
    # Criar DataFrame das transações
    transactions_df = pd.DataFrame(json_data['transactions'])
    
    # Adicionar informações da conta a cada transação
    transactions_df['bank_report_type'] = json_data['bank_report_type']
    transactions_df['period'] = f"{json_data['start_date']} to {json_data['end_date']}"
    transactions_df['gaccount'] = transactions_df['account']
    transactions_df['gcusip'] = transactions_df['cusip']
    
    return transactions_df