import sqlite3
import os

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    return sqlite3.connect('flashcards.db')

def create_category_if_not_exists(category_name, description=""):
    """Cria uma categoria se ela não existir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
    category = cursor.fetchone()
    
    if not category:
        cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
        ''', (category_name, description))
        category_id = cursor.lastrowid
        print(f"✓ Categoria '{category_name}' criada com ID {category_id}")
    else:
        category_id = category[0]
        print(f"✓ Categoria '{category_name}' já existe com ID {category_id}")
    
    conn.commit()
    conn.close()
    return category_id

def add_flashcard_if_not_exists(category_id, front_content, back_content):
    """Adiciona um flashcard se ele não existir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica se o flashcard já existe
    cursor.execute('''
        SELECT id FROM flashcards 
        WHERE category_id = ? AND front_content = ?
    ''', (category_id, front_content))
    
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute('''
            INSERT INTO flashcards (category_id, front_content, back_content, difficulty_level, review_count)
            VALUES (?, ?, ?, 1, 0)
        ''', (category_id, front_content, back_content))
        print(f"✓ Adicionado: {front_content}")
        added = True
    else:
        print(f"- Já existe: {front_content}")
        added = False
    
    conn.commit()
    conn.close()
    return added

def deploy_all_flashcards():
    """Implanta todos os flashcards com contexto no PythonAnywhere"""
    print("🚀 Iniciando implantação dos flashcards no PythonAnywhere...")
    
    # Criar categoria
    category_id = create_category_if_not_exists(
        "English Class", 
        "Flashcards para aprender inglês com phrasal verbs, tempos verbais e vocabulário"
    )
    
    # Lista completa de flashcards com contexto
    flashcards = [
        # Phrasal Verbs com contexto
        ("I give up because this task is too complicated", "Eu desisto porque esta tarefa é muito complicada"),
        ("I look forward to meeting you next week", "Estou ansioso para te encontrar na próxima semana"),
        ("We ran out of coffee this morning", "Ficamos sem café esta manhã"),
        ("Don't put off your homework until tomorrow", "Não adie sua lição de casa para amanhã"),
        ("She gets along with her coworkers very well", "Ela se dá muito bem com seus colegas de trabalho"),
        ("He turned down the job offer yesterday", "Ele recusou a oferta de emprego ontem"),
        ("Please don't bring up that topic again", "Por favor, não traga esse tópico novamente"),
        ("I came across an interesting article today", "Encontrei um artigo interessante hoje"),
        ("Can you figure out this math problem?", "Você consegue resolver este problema de matemática?"),
        ("She takes after her mother in personality", "Ela puxou a mãe na personalidade"),
        ("My car broke down on the highway", "Meu carro quebrou na estrada"),
        ("They called off the meeting due to rain", "Eles cancelaram a reunião devido à chuva"),
        ("Please carry on with your presentation", "Por favor, continue com sua apresentação"),
        ("Let's check out that new restaurant tonight", "Vamos conferir aquele restaurante novo hoje à noite"),
        ("Feel free to drop by my office anytime", "Sinta-se à vontade para passar no meu escritório a qualquer hora"),
        
        # Present Perfect com contexto
        ("I have lived in this city for five years", "Eu moro nesta cidade há cinco anos"),
        ("She has worked at this company since 2020", "Ela trabalha nesta empresa desde 2020"),
        ("They have traveled to many countries together", "Eles viajaram para muitos países juntos"),
        ("We have studied English for three months", "Estudamos inglês há três meses"),
        ("He has finished his homework already", "Ele já terminou sua lição de casa"),
        ("You have seen this movie before, haven't you?", "Você já viu este filme antes, não é?"),
        ("I have never been to Japan, but I'd love to go", "Nunca estive no Japão, mas adoraria ir"),
        ("She has already eaten lunch, so she's not hungry", "Ela já almoçou, então não está com fome"),
        ("They have just arrived at the airport", "Eles acabaram de chegar ao aeroporto"),
        ("We have known each other since childhood", "Nos conhecemos desde a infância"),
        
        # Past Perfect com contexto
        ("I had finished my work before the meeting started", "Eu tinha terminado meu trabalho antes da reunião começar"),
        ("They had arrived at the party before we got there", "Eles tinham chegado à festa antes de chegarmos lá"),
        ("She had studied French before moving to Paris", "Ela tinha estudado francês antes de se mudar para Paris"),
        ("We had eaten dinner before the movie began", "Tínhamos jantado antes do filme começar"),
        ("He had left the office when I called him", "Ele tinha saído do escritório quando eu liguei para ele"),
        ("You had seen that documentary before we watched it together", "Você tinha visto aquele documentário antes de assistirmos juntos"),
        ("I had never visited Europe until last summer", "Nunca tinha visitado a Europa até o verão passado"),
        ("They had already decided to move before the announcement", "Eles já tinham decidido se mudar antes do anúncio"),
        
        # Travel Vocabulary com contexto
        ("The airport was very crowded during the holiday season", "O aeroporto estava muito lotado durante a temporada de férias"),
        ("Don't forget to print your boarding pass before the flight", "Não esqueça de imprimir seu cartão de embarque antes do voo"),
        ("The departure gate for flight 205 is B12", "O portão de embarque para o voo 205 é B12"),
        ("Meet me at the baggage claim area after you land", "Me encontre na área de retirada de bagagem depois que você pousar"),
        ("We had to wait in line at customs for an hour", "Tivemos que esperar na fila da alfândega por uma hora"),
        ("Passport control was surprisingly quick today", "O controle de passaporte foi surpreendentemente rápido hoje"),
        ("I made a hotel reservation for three nights", "Fiz uma reserva de hotel por três noites"),
        ("We ordered room service because we were too tired to go out", "Pedimos serviço de quarto porque estávamos muito cansados para sair"),
        ("The Eiffel Tower is the most famous tourist attraction in Paris", "A Torre Eiffel é a atração turística mais famosa de Paris"),
        ("I need to find a currency exchange office at the airport", "Preciso encontrar uma casa de câmbio no aeroporto"),
        ("Travel insurance is essential for international trips", "Seguro viagem é essencial para viagens internacionais"),
        ("Our travel itinerary includes visits to five different cities", "Nosso roteiro de viagem inclui visitas a cinco cidades diferentes"),
        ("We spent the whole day sightseeing in the old town", "Passamos o dia todo fazendo turismo na cidade antiga"),
        ("I bought a beautiful souvenir for my sister", "Comprei uma lembrança linda para minha irmã"),
        
        # Business Vocabulary com contexto
        ("The board meeting is scheduled for 2 PM today", "A reunião da diretoria está marcada para 14h hoje"),
        ("We need to meet the project deadline by Friday", "Precisamos cumprir o prazo do projeto até sexta-feira"),
        ("The marketing budget for this quarter has been approved", "O orçamento de marketing para este trimestre foi aprovado"),
        ("The company's profit increased by 15% this year", "O lucro da empresa aumentou 15% este ano"),
        ("Our monthly revenue exceeded expectations", "Nossa receita mensal superou as expectativas"),
        ("The new investment will help expand our operations", "O novo investimento ajudará a expandir nossas operações"),
        ("All stakeholders must approve the new policy", "Todos os interessados devem aprovar a nova política"),
        ("The quarterly report shows positive growth trends", "O relatório trimestral mostra tendências de crescimento positivas"),
        ("Our market share has grown significantly this year", "Nossa participação no mercado cresceu significativamente este ano"),
        ("The business plan needs to be revised before presentation", "O plano de negócios precisa ser revisado antes da apresentação"),
        ("We need to improve our cash flow management", "Precisamos melhorar nossa gestão de fluxo de caixa"),
        ("The ROI on this project is expected to be 25%", "O ROI deste projeto deve ser de 25%"),
        ("Networking events are great for building business relationships", "Eventos de networking são ótimos para construir relacionamentos comerciais"),
        ("Her presentation impressed all the clients", "Sua apresentação impressionou todos os clientes"),
        ("The contract negotiation took longer than expected", "A negociação do contrato demorou mais do que esperado"),
        ("Our partnership with that company has been very successful", "Nossa parceria com aquela empresa tem sido muito bem-sucedida"),
        ("The merger between the two companies was announced yesterday", "A fusão entre as duas empresas foi anunciada ontem"),
        ("The acquisition will strengthen our market position", "A aquisição fortalecerá nossa posição no mercado"),
        ("Outsourcing IT services helped reduce operational costs", "Terceirizar serviços de TI ajudou a reduzir custos operacionais"),
        ("Human Resources is handling the recruitment process", "Recursos Humanos está cuidando do processo de recrutamento"),
        
        # Travel Phrases com contexto
        ("Excuse me, where is the nearest ATM? I need to withdraw some cash", "Com licença, onde fica o caixa eletrônico mais próximo? Preciso sacar dinheiro"),
        ("How much does it cost to take a taxi to the city center?", "Quanto custa pegar um táxi para o centro da cidade?"),
        ("Can you recommend a good restaurant that serves local cuisine?", "Você pode recomendar um bom restaurante que serve culinária local?"),
        ("I'd like to book a table for two at 7 PM tonight", "Gostaria de reservar uma mesa para dois às 19h hoje à noite"),
        ("Excuse me, where is the bathroom? I really need to use it", "Com licença, onde fica o banheiro? Preciso muito usá-lo"),
        ("Could you help me with directions to the train station?", "Você poderia me ajudar com direções para a estação de trem?"),
        ("I'm looking for a taxi to take me to the airport", "Estou procurando um táxi para me levar ao aeroporto"),
        ("What time does the museum open on Sundays?", "Que horas o museu abre aos domingos?"),
        ("Is there Wi-Fi available in this hotel lobby?", "Há Wi-Fi disponível no lobby deste hotel?"),
        ("I need to exchange money before I go shopping", "Preciso trocar dinheiro antes de ir às compras"),
        
        # Business Phrases com contexto
        ("Let's schedule a meeting to discuss the new project proposal", "Vamos agendar uma reunião para discutir a nova proposta de projeto"),
        ("I'll get back to you on that after I check with my team", "Vou te retornar sobre isso depois que verificar com minha equipe"),
        ("Could you send me the proposal by email before tomorrow?", "Você poderia me enviar a proposta por email antes de amanhã?"),
        ("We need to meet the deadline or we'll lose the client", "Precisamos cumprir o prazo ou perderemos o cliente"),
        ("Let's think outside the box to find a creative solution", "Vamos pensar fora da caixa para encontrar uma solução criativa"),
        ("Great! It sounds like we're on the same page about this", "Ótimo! Parece que estamos na mesma página sobre isso"),
        ("Let's touch base next week to see how the project is progressing", "Vamos nos falar na próxima semana para ver como o projeto está progredindo"),
        ("I'll keep you in the loop about any important updates", "Vou te manter informado sobre quaisquer atualizações importantes"),
        ("We need to cut costs without compromising quality", "Precisamos cortar custos sem comprometer a qualidade"),
        ("The project is on track to be completed ahead of schedule", "O projeto está no caminho certo para ser concluído antes do prazo")
    ]
    
    print(f"\n📚 Adicionando {len(flashcards)} flashcards...")
    
    added_count = 0
    for front, back in flashcards:
        if add_flashcard_if_not_exists(category_id, front, back):
            added_count += 1
    
    print(f"\n🎉 Implantação concluída!")
    print(f"📊 Estatísticas:")
    print(f"   • Total de flashcards: {len(flashcards)}")
    print(f"   • Novos flashcards adicionados: {added_count}")
    print(f"   • Flashcards já existentes: {len(flashcards) - added_count}")
    
    if added_count > 0:
        print(f"\n✅ {added_count} novos flashcards foram adicionados ao banco de dados!")
    else:
        print(f"\n✅ Todos os flashcards já estavam no banco de dados!")
    
    print(f"\n🔗 Agora você pode acessar sua aplicação no PythonAnywhere e ver todos os flashcards contextualizados!")

if __name__ == "__main__":
    deploy_all_flashcards()