#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar flashcards de inglês com traduções em português brasileiro
Foco: phrasal verbs, past/present perfect, vocabulário de viagem e negócios
"""

import sqlite3
import os

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    db_path = os.path.join(os.path.dirname(__file__), 'flashcards.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_category_if_not_exists(category_name):
    """Cria a categoria se ela não existir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica se a categoria já existe
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category = cursor.fetchone()
    
    if category:
        category_id = category['id']
    else:
        # Cria a categoria
        cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)',
                      (category_name, f'Flashcards para aprender {category_name}'))
        category_id = cursor.lastrowid
        conn.commit()
    
    conn.close()
    return category_id

def add_flashcard(category_id, front, back):
    """Adiciona um flashcard ao banco de dados"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO flashcards (category_id, front_content, back_content, difficulty_level, review_count)
        VALUES (?, ?, ?, 1, 0)
    ''', (category_id, front, back))
    
    conn.commit()
    conn.close()

def create_english_flashcards():
    """Cria flashcards de inglês organizados por temas"""
    
    # Criar categoria "English Class"
    category_id = create_category_if_not_exists("English Class")
    
    # Phrasal Verbs
    phrasal_verbs = [
        ("Give up", "Desistir"),
        ("Look after", "Cuidar de"),
        ("Put off", "Adiar"),
        ("Turn down", "Recusar / Diminuir o volume"),
        ("Come across", "Encontrar por acaso"),
        ("Break down", "Quebrar / Ter um colapso"),
        ("Set up", "Estabelecer / Configurar"),
        ("Take off", "Decolar / Tirar (roupa)"),
        ("Run out of", "Ficar sem"),
        ("Get along with", "Se dar bem com"),
        ("Look forward to", "Aguardar ansiosamente"),
        ("Carry out", "Executar / Realizar"),
        ("Bring up", "Criar (filhos) / Mencionar"),
        ("Call off", "Cancelar"),
        ("Figure out", "Descobrir / Entender")
    ]
    
    # Present Perfect
    present_perfect = [
        ("I have lived here for 5 years", "Eu moro aqui há 5 anos"),
        ("She has just arrived", "Ela acabou de chegar"),
        ("Have you ever been to Brazil?", "Você já esteve no Brasil?"),
        ("We have already finished the project", "Nós já terminamos o projeto"),
        ("They haven't seen the movie yet", "Eles ainda não viram o filme"),
        ("I have never tried sushi", "Eu nunca experimentei sushi"),
        ("He has worked here since 2020", "Ele trabalha aqui desde 2020"),
        ("Have you done your homework?", "Você fez sua lição de casa?"),
        ("She has lost her keys", "Ela perdeu suas chaves"),
        ("We have been friends for years", "Somos amigos há anos")
    ]
    
    # Past Perfect
    past_perfect = [
        ("I had finished work before he arrived", "Eu tinha terminado o trabalho antes dele chegar"),
        ("She had already left when I called", "Ela já tinha saído quando eu liguei"),
        ("They had never seen snow before", "Eles nunca tinham visto neve antes"),
        ("Had you met him before the party?", "Você o tinha conhecido antes da festa?"),
        ("We had been waiting for an hour", "Nós tínhamos estado esperando por uma hora"),
        ("He had studied English for 3 years", "Ele tinha estudado inglês por 3 anos"),
        ("I had forgotten my wallet at home", "Eu tinha esquecido minha carteira em casa"),
        ("She had lived in Paris before moving here", "Ela tinha morado em Paris antes de se mudar para cá")
    ]
    
    # Travel Vocabulary
    travel_vocab = [
        ("Airport", "Aeroporto"),
        ("Boarding pass", "Cartão de embarque"),
        ("Check-in", "Fazer check-in"),
        ("Departure gate", "Portão de embarque"),
        ("Baggage claim", "Esteira de bagagem"),
        ("Customs", "Alfândega"),
        ("Passport control", "Controle de passaporte"),
        ("Hotel reservation", "Reserva de hotel"),
        ("Room service", "Serviço de quarto"),
        ("Tourist attraction", "Atração turística"),
        ("Currency exchange", "Câmbio de moeda"),
        ("Travel insurance", "Seguro viagem"),
        ("Itinerary", "Roteiro"),
        ("Sightseeing", "Turismo / Passeio turístico"),
        ("Souvenir", "Lembrança / Souvenir")
    ]
    
    # Business Vocabulary
    business_vocab = [
        ("Meeting", "Reunião"),
        ("Deadline", "Prazo final"),
        ("Budget", "Orçamento"),
        ("Profit", "Lucro"),
        ("Revenue", "Receita"),
        ("Investment", "Investimento"),
        ("Stakeholder", "Parte interessada"),
        ("Quarterly report", "Relatório trimestral"),
        ("Market share", "Participação no mercado"),
        ("Business plan", "Plano de negócios"),
        ("Cash flow", "Fluxo de caixa"),
        ("ROI (Return on Investment)", "Retorno sobre investimento"),
        ("Networking", "Fazer contatos profissionais"),
        ("Presentation", "Apresentação"),
        ("Negotiation", "Negociação"),
        ("Partnership", "Parceria"),
        ("Merger", "Fusão"),
        ("Acquisition", "Aquisição"),
        ("Outsourcing", "Terceirização"),
        ("Human Resources", "Recursos Humanos")
    ]
    
    # Travel Phrases
    travel_phrases = [
        ("Where is the nearest ATM?", "Onde fica o caixa eletrônico mais próximo?"),
        ("How much does it cost?", "Quanto custa?"),
        ("Can you recommend a good restaurant?", "Você pode recomendar um bom restaurante?"),
        ("I'd like to book a table for two", "Gostaria de reservar uma mesa para dois"),
        ("Excuse me, where is the bathroom?", "Com licença, onde fica o banheiro?"),
        ("Could you help me with directions?", "Você poderia me ajudar com direções?"),
        ("I'm looking for a taxi", "Estou procurando um táxi"),
        ("What time does the museum open?", "Que horas o museu abre?"),
        ("Is there Wi-Fi available?", "Há Wi-Fi disponível?"),
        ("I need to exchange money", "Preciso trocar dinheiro")
    ]
    
    # Business Phrases
    business_phrases = [
        ("Let's schedule a meeting", "Vamos agendar uma reunião"),
        ("I'll get back to you on that", "Vou retornar sobre isso"),
        ("Could you send me the proposal?", "Você poderia me enviar a proposta?"),
        ("We need to meet the deadline", "Precisamos cumprir o prazo"),
        ("Let's think outside the box", "Vamos pensar fora da caixa"),
        ("We're on the same page", "Estamos na mesma página"),
        ("Let's touch base next week", "Vamos nos falar na próxima semana"),
        ("I'll keep you in the loop", "Vou te manter informado"),
        ("We need to cut costs", "Precisamos cortar custos"),
        ("The project is on track", "O projeto está no caminho certo")
    ]
    
    # Adicionar todos os flashcards
    all_flashcards = (
        phrasal_verbs + present_perfect + past_perfect + 
        travel_vocab + business_vocab + travel_phrases + business_phrases
    )
    
    print(f"Criando {len(all_flashcards)} flashcards na categoria 'English Class'...")
    
    for front, back in all_flashcards:
        add_flashcard(category_id, front, back)
        print(f"✓ Adicionado: {front}")
    
    print(f"\n🎉 Sucesso! {len(all_flashcards)} flashcards criados!")
    print("\nFlashcards organizados por tema:")
    print(f"• Phrasal Verbs: {len(phrasal_verbs)}")
    print(f"• Present Perfect: {len(present_perfect)}")
    print(f"• Past Perfect: {len(past_perfect)}")
    print(f"• Travel Vocabulary: {len(travel_vocab)}")
    print(f"• Business Vocabulary: {len(business_vocab)}")
    print(f"• Travel Phrases: {len(travel_phrases)}")
    print(f"• Business Phrases: {len(business_phrases)}")

if __name__ == "__main__":
    create_english_flashcards()