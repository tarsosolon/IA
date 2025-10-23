document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    // Funcionalidade para mostrar/ocultar senha
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.type === 'password' ? 'text' : 'password';
        passwordInput.type = type;
        togglePassword.querySelector('.eye-icon').style.opacity = type === 'password' ? '0.7' : '1';
    });

    // Credenciais de teste
    const testCredentials = {
        username: 'usuario',
        password: 'senha123'
    };

    // Função para exibir mensagem
    const showMessage = (text, isSuccess) => {
        messageDiv.textContent = text;
        messageDiv.className = isSuccess ? 'success' : 'error';
    };

    // Manipulador do formulário de login
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Validação das credenciais
        if (username === testCredentials.username && password === testCredentials.password) {
            showMessage('Login realizado com sucesso!', true);
            // Salva o usuário na sessão e redireciona
            sessionStorage.setItem('username', username);
            setTimeout(() => {
                window.location.href = 'hello.html';
            }, 1500);
        } else {
            showMessage('Usuário ou senha incorretos!', false);
        }
    });
});