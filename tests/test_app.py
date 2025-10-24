# Script de teste que simula a lógica do front-end (usersDB, ordenação, paginação, ativar/desativar, excluir)
# e a função de validação de CPF baseada no código JS do projeto.

from math import ceil

ITEMS_PER_PAGE = 20

# Implementação da validação de CPF (portada do JS)
def validate_cpf(cpf):
    cpf = ''.join([c for c in cpf if c.isdigit()])
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    # primeiro dígito
    s = 0
    for i in range(9):
        s += int(cpf[i]) * (10 - i)
    rest = 11 - (s % 11)
    digit1 = 0 if rest >= 10 else rest
    # segundo dígito
    s = 0
    for i in range(10):
        s += int(cpf[i]) * (11 - i)
    rest = 11 - (s % 11)
    digit2 = 0 if rest >= 10 else rest
    return digit1 == int(cpf[9]) and digit2 == int(cpf[10])

# Simulação do usersDB do front-end
class UsersDB:
    def __init__(self):
        self.users = []

    def get_users(self):
        return list(self.users)

    def save_user(self, user):
        # verifica CPF único (comparação exata como no front-end)
        if any(u['cpf'] == user['cpf'] for u in self.users):
            raise ValueError('CPF já cadastrado')
        user_copy = dict(user)
        user_copy.setdefault('active', True)
        self.users.append(user_copy)

    def update_user(self, cpf, updates):
        for i, u in enumerate(self.users):
            if u['cpf'] == cpf:
                self.users[i] = {**u, **updates}
                return

    def delete_user(self, cpf):
        self.users = [u for u in self.users if u['cpf'] != cpf]

    def sorted_by_name(self):
        return sorted(self.users, key=lambda x: x['name'])

    def paginated(self, page):
        sorted_users = self.sorted_by_name()
        total_pages = ceil(len(sorted_users) / ITEMS_PER_PAGE) if sorted_users else 1
        page = max(1, min(page, total_pages))
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        return sorted_users[start:end], len(sorted_users), total_pages


# Test runner

def run_tests():
    db = UsersDB()

    # Teste validação CPF com um CPF conhecido válido e inválido
    valid_cpf_formatted = '032.842.134-06'  # citado anteriormente como válido
    invalid_cpf = '123.456.789-00'

    assert validate_cpf(valid_cpf_formatted) == True, 'CPF válido falhou na validação'
    assert validate_cpf(invalid_cpf) == False, 'CPF inválido passou na validação'

    # Dados de teste
    user1 = {
        'cpf': '123.456.789-09',
        'name': 'Maria da Silva Santos',
        'birthDate': '1990-05-15',
        'address': 'Rua das Flores, 123 - Centro',
        'phone': '(11) 98765-4321'
    }

    user2 = {
        'cpf': '987.654.321-00',
        'name': 'Antonio Pereira Lima',
        'birthDate': '1985-10-20',
        'address': 'Avenida Brasil, 500 - Jardim América',
        'phone': '(11) 91234-5678'
    }

    # Salvar usuários
    db.save_user(user1)
    db.save_user(user2)

    # Verifica que ambos foram salvos
    all_users = db.get_users()
    assert len(all_users) == 2, f'Esperado 2 usuários, encontrado {len(all_users)}'

    # Verifica ordenação por nome (Antonio antes de Maria)
    sorted_users = db.sorted_by_name()
    assert sorted_users[0]['name'].startswith('Antonio'), 'Ordenação por nome incorreta'

    # Paginação: página 1 deve conter ambos (menos que 20)
    page_users, total_count, total_pages = db.paginated(1)
    assert total_count == 2, f'Contador total incorreto: {total_count}'
    assert len(page_users) == 2, f'Número de itens na página incorreto: {len(page_users)}'
    assert total_pages == 1, f'Número de páginas incorreto: {total_pages}'

    # Ativar/Desativar: desativar user1
    db.update_user(user1['cpf'], {'active': False})
    u1 = next((u for u in db.get_users() if u['cpf'] == user1['cpf']), None)
    assert u1 is not None and u1.get('active') == False, 'Falha ao desativar usuário'

    # Reativar
    db.update_user(user1['cpf'], {'active': True})
    u1 = next((u for u in db.get_users() if u['cpf'] == user1['cpf']), None)
    assert u1 is not None and u1.get('active') == True, 'Falha ao reativar usuário'

    # Excluir user2
    db.delete_user(user2['cpf'])
    remaining = db.get_users()
    assert len(remaining) == 1 and remaining[0]['cpf'] == user1['cpf'], 'Falha ao excluir usuário'

    print('Todos os testes passaram com sucesso.')


if __name__ == '__main__':
    try:
        run_tests()
    except AssertionError as e:
        print('Teste falhou:', e)
        raise SystemExit(1)
    except Exception as e:
        print('Erro durante os testes:', e)
        raise SystemExit(2)
