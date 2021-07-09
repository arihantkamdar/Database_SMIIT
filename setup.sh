mkdir -p ~/.streamlit/
echo "\
[general]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
