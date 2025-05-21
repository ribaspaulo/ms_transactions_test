#!/bin/bash

# Executar o aplicativo Python
streamlit run app.py  --server.enableXsrfProtection=false --server.enableCORS=false --server.headless=true --client.showSidebarNavigation=false

