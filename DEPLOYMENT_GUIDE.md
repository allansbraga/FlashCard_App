# Guia de Implantação do FlashCard App no PythonAnywhere

Este guia fornece instruções passo a passo para implantar o FlashCard App no PythonAnywhere, uma plataforma de hospedagem gratuita para aplicativos Python.

## Pré-requisitos

- Uma conta no PythonAnywhere (você pode criar uma gratuitamente em [pythonanywhere.com](https://www.pythonanywhere.com/))
- O código-fonte do FlashCard App

## Passos para Implantação

### 1. Criar uma conta no PythonAnywhere

- Acesse [pythonanywhere.com](https://www.pythonanywhere.com/) e crie uma conta gratuita
- Faça login na sua conta

### 2. Fazer upload dos arquivos do projeto

#### Opção 1: Upload direto

1. No painel do PythonAnywhere, clique na guia "Files"
2. Crie uma nova pasta para o projeto (ex: `flashcard_app`)
3. Navegue até a pasta criada
4. Faça upload de todos os arquivos do projeto

#### Opção 2: Usando Git (recomendado)

1. No painel do PythonAnywhere, clique na guia "Consoles" e inicie um novo console Bash
2. Clone o repositório do projeto:
   ```bash
   git clone https://github.com/seu-usuario/flashcard_app.git
   ```
   (Substitua a URL pelo URL do seu repositório Git)

### 3. Configurar o ambiente virtual

1. No console Bash, crie um ambiente virtual:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 flashcard_env
   ```

2. Ative o ambiente virtual (se ainda não estiver ativado):
   ```bash
   workon flashcard_env
   ```

3. Navegue até a pasta do projeto:
   ```bash
   cd ~/flashcard_app
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Inicializar o banco de dados

1. No console Bash, com o ambiente virtual ativado, execute:
   ```bash
   python init_db.py
   ```

### 5. Configurar a aplicação web

1. No painel do PythonAnywhere, clique na guia "Web"
2. Clique em "Add a new web app"
3. Na página de configuração, escolha "Manual configuration"
4. Selecione a versão Python 3.9

### 6. Configurar o ambiente virtual para a aplicação web

1. Na seção "Virtualenv", insira o caminho para o seu ambiente virtual:
   ```
   /home/seu-usuario/.virtualenvs/flashcard_env
   ```
   (Substitua "seu-usuario" pelo seu nome de usuário do PythonAnywhere)

### 7. Configurar o arquivo WSGI

1. Na seção "Code", clique no link para editar o arquivo WSGI
2. Apague todo o conteúdo do arquivo
3. Cole o seguinte código, substituindo "seu-usuario" pelo seu nome de usuário do PythonAnywhere e ajustando o caminho se necessário:

```python
import sys
import os

# Adicionar o diretório do projeto ao path
path = '/home/seu-usuario/flashcard_app'
if path not in sys.path:
    sys.path.append(path)

# Definir variáveis de ambiente (opcional)
os.environ['DATABASE_PATH'] = '/home/seu-usuario/flashcard_app/flashcards.db'

# Importar a aplicação Flask
from wsgi import app as application
```

4. Salve o arquivo

### 8. Configurar arquivos estáticos

1. Na seção "Static files" da página de configuração da aplicação web, adicione:
   - URL: `/static/`
   - Directory: `/home/seu-usuario/flashcard_app/static`

### 9. Recarregar a aplicação web

1. Clique no botão "Reload" na parte superior da página de configuração da aplicação web

### 10. Acessar a aplicação

1. Sua aplicação estará disponível em:
   ```
   https://seu-usuario.pythonanywhere.com
   ```
   (Substitua "seu-usuario" pelo seu nome de usuário do PythonAnywhere)

## Solução de Problemas

### Verificar logs de erro

Se a aplicação não estiver funcionando corretamente:

1. No painel do PythonAnywhere, clique na guia "Web"
2. Role até a seção "Logs"
3. Verifique os logs de erro e acesso para identificar problemas

### Problemas comuns

1. **Erro 502 Bad Gateway**:
   - Verifique se o arquivo WSGI está configurado corretamente
   - Verifique se todas as dependências foram instaladas

2. **Arquivos estáticos não carregam**:
   - Verifique se a configuração de arquivos estáticos está correta

3. **Erro no banco de dados**:
   - Verifique se o banco de dados foi inicializado corretamente
   - Verifique se o caminho do banco de dados está correto no arquivo WSGI

## Manutenção

### Atualizar a aplicação

Para atualizar a aplicação após fazer alterações no código:

1. Faça upload dos arquivos atualizados ou, se estiver usando Git, faça pull das alterações
2. No painel do PythonAnywhere, clique na guia "Web"
3. Clique no botão "Reload" para reiniciar a aplicação

### Backup do banco de dados

Para fazer backup do banco de dados:

1. No console Bash, execute:
   ```bash
   cp ~/flashcard_app/flashcards.db ~/flashcards_backup_$(date +%Y%m%d).db
   ```

Este comando criará uma cópia do banco de dados com a data atual no nome do arquivo.