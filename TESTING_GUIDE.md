# Guia de Teste do FlashCard App em Produção

Este guia fornece instruções para testar o FlashCard App após a implantação no PythonAnywhere ou em outra plataforma de hospedagem.

## Checklist de Teste

### 1. Verificação Inicial

- [ ] Acesse a URL da aplicação (ex: `https://seu-usuario.pythonanywhere.com`)
- [ ] Verifique se a página inicial carrega corretamente
- [ ] Verifique se o CSS e JavaScript estão carregando corretamente

### 2. Teste de Categorias

- [ ] Acesse a página de categorias
- [ ] Crie uma nova categoria
- [ ] Verifique se a categoria aparece na lista
- [ ] Edite a categoria
- [ ] Verifique se as alterações foram salvas
- [ ] Exclua a categoria (se aplicável)

### 3. Teste de Flashcards

- [ ] Acesse a página de flashcards
- [ ] Crie um novo flashcard
- [ ] Verifique se o flashcard aparece na lista
- [ ] Edite o flashcard
- [ ] Verifique se as alterações foram salvas
- [ ] Exclua o flashcard (se aplicável)

### 4. Teste de Revisão

- [ ] Acesse a página de revisão
- [ ] Verifique se os flashcards aparecem para revisão
- [ ] Teste a funcionalidade de virar o cartão
- [ ] Avalie um flashcard
- [ ] Verifique se o próximo flashcard aparece
- [ ] Complete uma sessão de revisão

### 5. Teste de Responsividade

- [ ] Teste a aplicação em um dispositivo móvel ou usando as ferramentas de desenvolvedor do navegador
- [ ] Verifique se a interface se adapta a diferentes tamanhos de tela
- [ ] Teste a navegação em dispositivos móveis

### 6. Teste de Desempenho

- [ ] Verifique o tempo de carregamento das páginas
- [ ] Teste a aplicação com vários flashcards e categorias
- [ ] Verifique se não há erros no console do navegador

## Solução de Problemas

### Problemas de Carregamento de Página

1. Verifique os logs de erro no PythonAnywhere
2. Verifique se todos os arquivos estáticos estão sendo carregados corretamente
3. Verifique se o banco de dados foi inicializado corretamente

### Problemas de Funcionalidade

1. Verifique se o JavaScript está funcionando corretamente
2. Verifique se as requisições AJAX estão sendo processadas corretamente
3. Verifique se o banco de dados está sendo atualizado corretamente

### Problemas de Desempenho

1. Verifique se há consultas ao banco de dados ineficientes
2. Verifique se os arquivos estáticos estão sendo carregados eficientemente
3. Considere otimizar o código se necessário

## Relatório de Teste

Ao concluir os testes, crie um relatório com as seguintes informações:

1. Data e hora do teste
2. Versão da aplicação testada
3. Ambiente de teste (navegador, dispositivo, etc.)
4. Resultados dos testes (sucesso/falha)
5. Problemas encontrados
6. Sugestões de melhoria

Este relatório ajudará a acompanhar o progresso da aplicação e identificar áreas que precisam de atenção.