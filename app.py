import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from utils import move_file, del_folder
import tempfile
from parse_txt import exec_parse, prepare_tree_data

# Configuração da aplicação Streamlit

st.set_page_config(page_title='Teste parseamento de dados Morgan Stanley',
                page_icon=':bar_chart:',
                layout='wide'
    )

bt_disable_mode = True

st.title('Teste parseamento de dados Morgan Stanley')

ufile = st.file_uploader('Arquivo de dados do tipo txt',accept_multiple_files=False, type=['xlsx','xls', 'txt', 'docx'])


if ufile is not None:
    dispmsg = ""
    # Cria um diretório temporário
    temp_dir = tempfile.mkdtemp()
    # Salva o arquivo carregado pelo usuário no diretório temporário
    xlsx_path = os.path.join(temp_dir, ufile.name)
    mov_path = f"./uploads/"
    with open(xlsx_path, "wb") as f:
        f.write(ufile.getbuffer())
    bt_disable_mode = False
    dispmsg = f"\n" + dispmsg + f"\n" + move_file(xlsx_path, mov_path)
    dispmsg = f"\n" + dispmsg + f"\n" +  del_folder(temp_dir)

# Criação do botão
    
if st.button('Extrair e Parsear', disabled=bt_disable_mode):
    # st.write('Alterações efetivadas!')
    txt_file = ufile.name
    data = exec_parse(txt_file)  
    
    df_txt_content = pd.read_excel(f'./{mov_path}/{txt_file[:-4]}.xlsx',  index_col=None, header=0)

    # Preparar os dados
    # st.write(data)
    df = prepare_tree_data(data)
    
    
    tabs = st.tabs(["Extraído", "Parseado"])
    tab_extraido = tabs[0]
    tab_parseado = tabs[1]
        
    with tab_extraido:
        st.subheader('Conteúdo extraído')
        AgGrid(
            df_txt_content,
            height=400,
            width='100%',
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme='alpine'
        )

    # Configurar a grid
    gb = GridOptionsBuilder.from_dataframe(df)


    # Configuração corrigida da coluna de grupo
    auto_group_column_def = {
        'headerName': "Type/Period/Account/CUSIP",
        'minWidth': 300,
        'cellRenderer': 'agGroupCellRenderer',
        'cellRendererParams': {
            'suppressCount': True,
            'innerRenderer': JsCode('''
                function(params) {
                    if (params.node.group) {
                        return params.value;
                    }
                    return params.value;
                }
            ''')
        }
    }

    # Configurar agrupamento
    gb.configure_selection('single')
    
    gb.configure_default_column(
        flex=1,
        minWidth=100,
        maxWidth=300,
        resizable=True,
    )

    # Configurar colunas para agrupamento
    gb.configure_column('period', rowGroup=True, hide=True)
    gb.configure_column('gaccount',  rowGroup=True, hide=True)
    gb.configure_column('gcusip',  rowGroup=True, hide=True)
    gb.configure_column('cusip',  hide=True)
    gb.configure_column('account',  hide=True)
    gb.configure_column('bank_report_type', rowGroup=True, hide=True)
    gb.configure_column('type', hide=True)
    gb.configure_column('user_date', hide=True)
    gb.configure_column('sic', hide=True)
    gb.configure_column('mmc', hide=True)
    gb.configure_column('checksum', hide=True)
    gb.configure_column('id', hide=True)
    gb.configure_column('payee', hide=True)
    

    # Configurar formatação
    gb.configure_column('amount', type=["numericColumn"], valueFormatter="'US$ ' + value.toFixed(2)")


    for col in ['type', 'date', 'amount', 'memo']:
        gb.configure_column(col)
    
    grid_options = gb.build()
    gb.configure_grid_options(
        groupDefaultExpanded=1,
        autoGroupColumnDef=auto_group_column_def,
        rowGroup=True        
    ) 

    with tab_parseado:
        st.subheader('Conteúdo parseado')        
        AgGrid(
            df,
            gridOptions=grid_options,
            height=400,
            width='100%',
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme='alpine'
        )
    
    
    #####    
else:
    st.write('Clique no botão para executar a extração e parseamento dos dados.')