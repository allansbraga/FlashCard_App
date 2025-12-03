import random
from models import User, Flashcard

def run():
    u = User()
    f = Flashcard()
    for i in range(1, 11):
        email = f"tester{i}@example.com"
        res = u.create_user(email, 'password', 'Português')
        if not res.get('success'):
            continue
        uid = res['id']
        vocab = [('Hello','Olá'), ('Thanks','Obrigado'), ('Bye','Tchau')]
        for front, back in vocab:
            f.add_flashcard(front, back, None, user_id=uid)
    print('seeded')

if __name__ == '__main__':
    run()