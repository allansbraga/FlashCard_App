#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para aplicar as correções de tradução no PythonAnywhere
Este script deve ser executado no console do PythonAnywhere
"""

import sqlite3
import os

def connect_to_database():
    """Conecta ao banco de dados SQLite"""
    db_path = 'flashcards.db'
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        print(f"✅ Conectado ao banco de dados: {db_path}")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def check_current_translations():
    """Verifica as traduções atuais no banco"""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Busca algumas traduções para verificar o estado atual
        cursor.execute("""
            SELECT f.front, f.back 
            FROM flashcards f
            JOIN categories c ON f.category_id = c.id
            WHERE c.name = 'English Class'
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        
        print("\n📋 Traduções atuais (primeiras 5):")
        print("-" * 80)
        for i, (front, back) in enumerate(results, 1):
            print(f"{i}. {front}")
            print(f"   → {back}")
            print()
        
        # Verifica se há traduções incorretas (apenas palavras-chave)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM flashcards f
            JOIN categories c ON f.category_id = c.id
            WHERE c.name = 'English Class'
            AND LENGTH(f.back) < 20
        """)
        
        short_translations = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM flashcards f
            JOIN categories c ON f.category_id = c.id
            WHERE c.name = 'English Class'
        """)
        
        total_flashcards = cursor.fetchone()[0]
        
        print(f"📊 Estatísticas:")
        print(f"   Total de flashcards: {total_flashcards}")
        print(f"   Traduções curtas (possivelmente incorretas): {short_translations}")
        print(f"   Traduções completas: {total_flashcards - short_translations}")
        
        if short_translations > 0:
            print(f"\n⚠️  Há {short_translations} traduções que precisam ser corrigidas!")
            return True
        else:
            print(f"\n✅ Todas as traduções parecem estar corretas!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar traduções: {e}")
        return False
    finally:
        conn.close()

def apply_translation_fixes():
    """Aplica as correções de tradução"""
    conn = connect_to_database()
    if not conn:
        return
    
    # Dicionário com as traduções corretas
    correct_translations = {
        "I give up because this task is too complicated": "Eu desisto porque esta tarefa é muito complicada",
        "He turned down the job offer yesterday": "Ele recusou a oferta de emprego ontem",
        "She looks after her elderly parents every weekend": "Ela cuida dos pais idosos todos os fins de semana",
        "We ran out of milk this morning": "Ficamos sem leite esta manhã",
        "They put off the meeting until next week": "Eles adiaram a reunião para a próxima semana",
        "I came across an interesting article today": "Encontrei um artigo interessante hoje",
        "She gets along well with her colleagues": "Ela se dá bem com os colegas",
        "We need to figure out this problem together": "Precisamos resolver este problema juntos",
        "He brought up an important point in the discussion": "Ele levantou um ponto importante na discussão",
        "They called off the event due to bad weather": "Eles cancelaram o evento devido ao mau tempo",
        "I have lived in this city for five years": "Eu moro nesta cidade há cinco anos",
        "She has just finished her homework": "Ela acabou de terminar sua lição de casa",
        "We have never been to Japan before": "Nunca estivemos no Japão antes",
        "They have already seen this movie twice": "Eles já viram este filme duas vezes",
        "He has worked here since 2020": "Ele trabalha aqui desde 2020",
        "I had studied English before moving to Canada": "Eu havia estudado inglês antes de me mudar para o Canadá",
        "She had already left when I arrived": "Ela já havia saído quando cheguei",
        "We had been waiting for an hour before the bus came": "Estávamos esperando há uma hora antes do ônibus chegar",
        "They had finished dinner by the time we got there": "Eles haviam terminado o jantar quando chegamos lá",
        "He had never traveled abroad until last year": "Ele nunca havia viajado para o exterior até o ano passado",
        "Where is the nearest airport?": "Onde fica o aeroporto mais próximo?",
        "I need to check in for my flight": "Preciso fazer o check-in do meu voo",
        "How much does this ticket cost?": "Quanto custa esta passagem?",
        "Can you help me with my luggage?": "Você pode me ajudar com minha bagagem?",
        "What time does the train leave?": "Que horas o trem parte?",
        "I would like to book a hotel room": "Gostaria de reservar um quarto de hotel",
        "Is breakfast included in the price?": "O café da manhã está incluído no preço?",
        "Where can I find a taxi?": "Onde posso encontrar um táxi?",
        "Do you have any recommendations for restaurants?": "Você tem alguma recomendação de restaurantes?",
        "I'm lost, can you give me directions?": "Estou perdido, você pode me dar direções?",
        "We need to schedule a meeting with the client": "Precisamos agendar uma reunião com o cliente",
        "Could you please send me the quarterly report?": "Você poderia me enviar o relatório trimestral?",
        "I'll follow up on this matter tomorrow": "Vou acompanhar este assunto amanhã",
        "Let's discuss the budget for next year": "Vamos discutir o orçamento para o próximo ano",
        "The deadline for this project is next Friday": "O prazo para este projeto é na próxima sexta-feira",
        "We should focus on improving customer satisfaction": "Devemos focar em melhorar a satisfação do cliente",
        "I need to review the contract before signing": "Preciso revisar o contrato antes de assinar",
        "Can we reschedule the presentation for next week?": "Podemos reagendar a apresentação para a próxima semana?",
        "The sales team exceeded their targets this quarter": "A equipe de vendas superou suas metas neste trimestre",
        "We're launching a new product line next month": "Estamos lançando uma nova linha de produtos no próximo mês",
        "How are you doing today?": "Como você está hoje?",
        "What do you do for a living?": "O que você faz da vida?",
        "Nice to meet you!": "Prazer em conhecê-lo!",
        "Could you repeat that, please?": "Você poderia repetir isso, por favor?",
        "I don't understand what you mean": "Não entendo o que você quer dizer",
        "That sounds like a great idea": "Isso parece uma ótima ideia",
        "I completely agree with you": "Concordo completamente com você",
        "Let me think about it for a moment": "Deixe-me pensar sobre isso por um momento",
        "Would you like to grab some coffee?": "Gostaria de tomar um café?",
        "Thank you so much for your help": "Muito obrigado pela sua ajuda",
        "I'm sorry, but I have to disagree": "Desculpe, mas tenho que discordar",
        "That's exactly what I was thinking": "É exatamente isso que eu estava pensando",
        "Could you explain that in more detail?": "Você poderia explicar isso com mais detalhes?",
        "I'm not sure I follow your reasoning": "Não tenho certeza se entendo seu raciocínio",
        "Let's take a break and continue later": "Vamos fazer uma pausa e continuar mais tarde",
        "I appreciate your patience with me": "Agradeço sua paciência comigo",
        "Would it be possible to extend the deadline?": "Seria possível estender o prazo?",
        "I'm looking forward to hearing from you": "Estou ansioso para ouvir de você",
        "Please feel free to contact me anytime": "Sinta-se à vontade para me contatar a qualquer momento",
        "I hope everything works out well for you": "Espero que tudo dê certo para você"
    }
    
    try:
        cursor = conn.cursor()
        updates_made = 0
        
        print("\n🔄 Aplicando correções de tradução...")
        print("-" * 50)
        
        for front_text, correct_translation in correct_translations.items():
            # Verifica se o flashcard existe e precisa de correção
            cursor.execute("""
                SELECT f.id, f.back 
                FROM flashcards f
                JOIN categories c ON f.category_id = c.id
                WHERE c.name = 'English Class' AND f.front = ?
            """, (front_text,))
            
            result = cursor.fetchone()
            if result:
                flashcard_id, current_translation = result
                
                # Só atualiza se a tradução atual for diferente da correta
                if current_translation != correct_translation:
                    cursor.execute("""
                        UPDATE flashcards 
                        SET back = ? 
                        WHERE id = ?
                    """, (correct_translation, flashcard_id))
                    
                    updates_made += 1
                    print(f"✅ Atualizado: {front_text[:50]}...")
        
        conn.commit()
        
        print(f"\n🎉 Correções aplicadas com sucesso!")
        print(f"📊 Total de flashcards atualizados: {updates_made}")
        
        if updates_made == 0:
            print("ℹ️  Todas as traduções já estavam corretas.")
        
    except Exception as e:
        print(f"❌ Erro ao aplicar correções: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Função principal"""
    print("🚀 Verificando e corrigindo traduções no PythonAnywhere")
    print("=" * 60)
    
    # Primeiro verifica o estado atual
    needs_fixes = check_current_translations()
    
    if needs_fixes:
        print("\n🔧 Aplicando correções...")
        apply_translation_fixes()
        
        print("\n🔍 Verificando novamente após correções...")
        check_current_translations()
    
    print("\n✅ Processo concluído!")
    print("\n📝 Próximos passos:")
    print("   1. Recarregue sua aplicação web no PythonAnywhere")
    print("   2. Teste os flashcards para verificar as traduções")
    print("   3. As mudanças devem aparecer imediatamente")

if __name__ == "__main__":
    main()