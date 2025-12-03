# PRD - FlashCard_App: Plataforma de Aprendizado de Idiomas

**Product Requirements Document**  
**Versão 1.0**  
**Data: 02/12/2025**  
**Autor: Assistente AI**  
**Repositório Base: [https://github.com/allansbraga/FlashCard_App](https://github.com/allansbraga/FlashCard_App)**[11]

***

## 1. Visão Geral do Produto

### 1.1 Resumo Executivo
Plataforma web de aprendizado de idiomas baseada em técnicas comprovadas (SRS, Shadowing, Gamificação) que segmenta experiências por usuário. Expande o FlashCard_App existente para cobrir **listening, speaking e writing** com flashcards avançados, shadow conversation, exercícios interativos e tracking de progresso.

**Objetivo Central**: Melhorar 40% listening, 30% speaking e 25% writing em 12 semanas de uso diário (15-30 min).

### 1.2 Proposta de Valor
- **Estudantes**: Progresso mensurável com técnicas científicas
- **Diferencial**: Combina 4 pilares linguísticos em uma plataforma
- **Escalável**: Flask + SQLite atual → PostgreSQL futuro

***

## 2. Funcionalidades Atuais (Análise do Repositório)[11]

| Componente | Descrição | Status |
|------------|-----------|--------|
| **app.py** | Flask app principal | ✅ Funcional |
| **models.py** | Modelos SQLite Flashcards | ✅ Básico |
| **templates/static** | Interface web responsiva | ✅ Deploy PythonAnywhere |
| **Scripts** | Deploy, init_db, flashcards | ✅ Automatizados |

**Limitações Atuais**: Sem autenticação, single-user, flashcards básicos.

***

## 3. Novos Módulos Funcionais

### 3.1 Autenticação e Segmentação por Usuário

#### 3.1.1 Funcionalidades
```
- Registro/Login (email + senha)
- Perfil: idioma nativo, idiomas-alvo, nível (A1-C2)
- Dashboard pessoal com métricas
- Multi-tenant: flashcards/atividades por usuário
```

#### 3.1.2 Banco de Dados
```sql
USERS: id, email, senha_hash, idioma_nativo, created_at
STUDENT_PROGRESS: user_id, skill, score, last_session, streak_days
```

#### 3.1.3 Tech Stack
```
Flask-Login + Flask-SQLAlchemy
JWT para API futura
```

**Critérios de Aceitação**: 95% taxa de login bem-sucedido, <2s carregamento.

***

### 3.2 FlashCards Avançados (SRS - SM-2 Algorithm)

#### 3.2.1 Modos de Estudo
| Modo | Descrição | Dificuldade |
|------|-----------|-------------|
| **Vocabulário** | Palavra + tradução + contexto | ⭐⭐ |
| **Frases** | Frase completa + gap-fill | ⭐⭐⭐ |
| **Áudio** | Ouvir + escrever palavra | ⭐⭐⭐⭐ |
| **Produção** | Ver imagem/palavra → traduzir | ⭐⭐⭐⭐⭐ |
| **Revisão** | SRS intervals (1, 3, 7, 14, 30 dias) | Dinâmico |

#### 3.2.2 Algoritmo SRS (SuperMemo-2)
```
Ease Factor (EF): 2.5 inicial
Intervalo = Intervalo anterior × EF
Se errar: reset para 1 dia
```

**Critérios**: 80% retenção após 30 dias.[1]

***

### 3.3 Shadow Conversation (Speaking)

#### 3.3.1 Funcionalidades Principais
```
1. Vídeos curtos (30-90s) com legendas trilíngues
2. Highlights automáticos (pausas naturais)
3. Player com: pause → repeat → record → compare
4. Feedback: volume, clareza, pronúncia
```

#### 3.3.2 Interface
```
[Video Player]
[Legenda PT] [Legenda EN] [Legenda Áudio]
[▶ Repeat] [🎤 Record] [🔊 Compare] [⭐ Dificuldade]
```

#### 3.3.3 Dados Estruturados
```json
{
  "video_id": 123,
  "segments": [
    {"start": 2.5, "end": 4.0, "text_pt": "Olá", "text_en": "Hello"},
    {"start": 5.2, "end": 7.1, "text_pt": "Tudo bem?", "text_en": "How are you?"}
  ]
}
```

**Tech**: FFmpeg para segmentação + Web Audio API.[3]

***

### 3.4 Listening (Estilo Duolingo)

#### 3.4.1 Tipos de Exercícios (5)
| Tipo | Descrição | Skills |
|------|-----------|--------|
| **Complete frase** | Audio → "[Eu sou] brasileiro" | Listening + Vocab |
| **Múltipla escolha** | Audio → A) casa B) gato C) carro | Listening |
| **Ditado** | Audio → Escrever frase completa | Listening + Spelling |
| **True/False** | Audio → Statement correto? | Listening + Comprehension |
| **Sequência** | Audio → Ordenar palavras | Listening + Grammar |

#### 3.4.2 Adaptive Difficulty
```
Acertos 4/5 → +10% dificuldade
Erros 2/5 → -15% dificuldade
```

***

### 3.5 Writing (Produção Escrita)

#### 3.5.1 Tipos de Exercícios
```
1. Complete frases (gap-fill)
2. Escreva tradução
3. Redação curta (50 palavras)
4. Correção gramatical automática
5. Feedback: vocabulário, conectores, coerência
```

#### 3.5.2 Integração LanguageTool
```
API gratuita: https://languagetool.org
Correge: grammar, spelling, style
Score: 0-100 por texto
```

***

### 3.6 Dashboard de Progresso

#### 3.6.1 Métricas por Skill
| Skill | Métricas | Meta Semanal |
|-------|----------|--------------|
| **Listening** | Acertos %, tempo reação | 75% acertos |
| **Speaking** | Clareza score, palavras/min | >70% clareza |
| **Writing** | Erros/100 palavras | <5 erros |
| **Vocab** | Cartões maduros | +50 novos |

#### 3.6.2 Gamificação
```
- Pontos diários: 100 pontos/sessão
- Streak: +50/dia consecutivo
- Badges: 7 dias, 1000 pontos, 80% listening
- Leaderboard (opcional)
```

***

## 4. Plano de Implementação (24 Semanas)

| Fase | Semanas | Entregáveis | Responsável |
|------|---------|-------------|-------------|
| **1** | 1-4 | Autenticação + perfis | Backend |
| **2** | 5-8 | FlashCards SRS | Fullstack |
| **3** | 9-12 | Shadow Conversation | Frontend Heavy |
| **4** | 13-16 | Listening Exercises | Fullstack |
| **5** | 17-20 | Writing + Progress | Backend |
| **6** | 21-24 | Gamificação + Polish | Full Team |

**Stack Técnico Final**:
```
Backend: Flask 3.x + SQLAlchemy + APScheduler (SRS)
Frontend: HTMX + Alpine.js + HTMX-Forms
DB: SQLite → PostgreSQL (scale)
Audio: Web Audio API + FFmpeg
Deploy: PythonAnywhere → Railway/Docker
```

***

## 5. Critérios de Sucesso (KPIs)

| Métrica | Meta 3 Meses | Meta 6 Meses |
|---------|--------------|--------------|
| **DAU** | 50 usuários | 500 usuários |
| **Retention D7** | 40% | 60% |
| **Sessão Média** | 20 min | 30 min |
| **NPS** | >40 | >60 |
| **Listening Gain** | +25% | +40% |

***

## 6. Próximos Passos

1. **Copie este Markdown** para `FlashCard_PRD.md`
2. **Converta para DOCX**: Use [markdownlivepreview.dev/tools/markdown-to-word][3]
3. **Implemente Fase 1** (Autenticação): 4 semanas
4. **Teste com 10 usuários** antes Fase 2

***

**Pronto para Download!**  
Copie todo conteúdo → Salve como `.md` → Converta em [CloudConvert]  ou [Markdown to Word]  → Abra no Word/Google Docs.[2][3]

**Tempo estimado de desenvolvimento**: 6 meses (1 dev full-time).[11]