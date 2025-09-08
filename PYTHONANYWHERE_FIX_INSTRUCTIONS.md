# 🔧 Instruções para Corrigir Traduções no PythonAnywhere

## Problema Identificado
As traduções dos flashcards não foram aplicadas no PythonAnywhere porque as correções foram feitas apenas localmente.

## Solução: Aplicar Correções no PythonAnywhere

### Passo 1: Acessar o Console do PythonAnywhere
1. Faça login no [PythonAnywhere](https://www.pythonanywhere.com)
2. Vá para a aba **"Consoles"**
3. Abra um **"Bash console"**

### Passo 2: Navegar para o Diretório do Projeto
```bash
cd ~/FlashCard_App
```

### Passo 3: Atualizar o Código do GitHub
```bash
git pull origin main
```

### Passo 4: Verificar se os Novos Arquivos Foram Baixados
```bash
ls -la *.py
```
Você deve ver os arquivos:
- `deploy_fixes_to_pythonanywhere.py`
- `fix_flashcard_translations.py`

### Passo 5: Executar o Script de Correção
```bash
python3 deploy_fixes_to_pythonanywhere.py
```

### Passo 6: Recarregar a Aplicação Web
1. Vá para a aba **"Web"** no PythonAnywhere
2. Clique no botão **"Reload"** da sua aplicação
3. Aguarde alguns segundos para o reload completar

### Passo 7: Testar as Correções
1. Acesse sua aplicação web
2. Vá para a categoria "English Class"
3. Teste alguns flashcards para verificar se as traduções estão corretas

## Exemplo do que Você Deve Ver

**Antes (incorreto):**
- Frase: "I give up because this task is too complicated"
- Tradução: "Desistir"

**Depois (correto):**
- Frase: "I give up because this task is too complicated"
- Tradução: "Eu desisto porque esta tarefa é muito complicada"

## Verificação de Sucesso

O script `deploy_fixes_to_pythonanywhere.py` irá:
1. ✅ Verificar o estado atual das traduções
2. 🔄 Aplicar as correções necessárias
3. 📊 Mostrar quantos flashcards foram atualizados
4. ✅ Confirmar que as correções foram aplicadas

## Solução de Problemas

### Se o comando `git pull` falhar:
```bash
git reset --hard HEAD
git pull origin main
```

### Se o script Python falhar:
1. Verifique se você está no diretório correto: `pwd`
2. Verifique se o arquivo existe: `ls -la deploy_fixes_to_pythonanywhere.py`
3. Tente executar com python: `python deploy_fixes_to_pythonanywhere.py`

### Se as traduções ainda não aparecerem:
1. Limpe o cache do navegador (Ctrl+F5 ou Cmd+Shift+R)
2. Tente acessar em uma aba anônima/privada
3. Aguarde alguns minutos e tente novamente

## Contato
Se você encontrar algum problema, verifique:
1. Se o script foi executado sem erros
2. Se a aplicação foi recarregada corretamente
3. Se você está testando a categoria "English Class"

---

**Nota:** Este processo corrige 90 flashcards com traduções completas em português brasileiro.