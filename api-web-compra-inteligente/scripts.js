let usuarioLogado = null;
let editId = null;
let editUsuarioCpf = null;
let baseUrl = `http://localhost:5000`;



function login() {
    const cpf = document.getElementById('loginCpf').value;
    const senha = document.getElementById('loginSenha').value;

    if(!cpf || !senha) {
        return alert('Informe CPF e Senha');
    }

    fetch(`${baseUrl}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cpf: cpf, senha: senha})
    })
    .then(res => {
        if(!res.ok) throw new Error('CPF e/ou senha Inválido(s)');
        return res.json();
    })
    .then(data => {
        localStorage.setItem('token', data.access_token);

        usuarioLogado = user,
        cpfLogado = cpf;
        localStorage.setItem('usuario', user);
        localStorage.setItem('cpf', cpf);

        showApp();
    })
    .catch(err => alert(err.message));
}

function register() {
    const user = document.getElementById('registerUser').value;
    const cpf = document.getElementById('registerCpf').value;
    const email = document.getElementById('registerEmail').value;
    const dataNascimento = document.getElementById('registerDataNasc').value;
    const dataISO = new Date(dataNascimento).toISOString();
    const senha = document.getElementById('registerSenha').value;

    if (!user || !cpf) return alert('Informe nome e CPF');

    fetch(`${baseUrl}/usuarios/cadastrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: user, cpf: cpf, email: email, data_nascimento: dataISO, senha: senha })
    })
    .then(res => {
        if (!res.ok) throw new Error('Usuário já existe');
        alert('Usuário criado com sucesso');
        document.getElementById('registerUser').value = '';
        document.getElementById('registerCpf').value = '';
        document.getElementById('registerEmail').value = '';
        document.getElementById('registerDataNasc').value = '';
        document.getElementById('registerSenha').value = '';
        toggleRegister();
    })
    .catch(err => alert(err.message));
}

function toggleRegister() {
    document.getElementById('registerBox').classList.toggle('d-none');
}

function logout() {
    localStorage.removeItem('usuario');
    localStorage.removeItem('cpf');
    usuarioLogado = null;
    cpfLogado = null;
    location.reload();
}