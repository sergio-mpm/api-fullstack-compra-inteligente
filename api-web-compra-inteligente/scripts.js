let usuarioLogado = null;
let editId = null;
let editUsuarioCpf = null;
let baseUrl = `http://localhost:5000`;

console.log("scripts.js carregado com sucesso");


function login() {
    const cpf = document.getElementById('loginCpf').value;
    const senha = document.getElementById('loginSenha').value;

    if (!cpf || !senha) {
        return alert('Informe CPF e Senha');
    }

    fetch(`${baseUrl}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cpf, senha })
    })
    .then(res => {
        if (!res.ok) throw new Error('CPF e/ou senha inválido(s)');
        return res.json();
    })
    .then(data => {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('cpf', cpf);

        usuarioLogado = cpf;

        showApp();
    })
    .catch(err => alert(err.message));
}

function register() {
    console.log("baseUrl:", baseUrl)
    const user = document.getElementById('registerUser').value;
    const cpf = document.getElementById('registerCpf').value;
    const email = document.getElementById('registerEmail').value;
    const senha = document.getElementById('registerSenha').value;

    if (!user || !cpf) return alert('Informe nome e CPF');

    fetch(`${baseUrl}/usuarios/cadastrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome: user, cpf: cpf, email: email, senha: senha })
    })
    .then(res => {
        if (!res.ok) throw new Error('Usuário já existe');
        alert('Usuário criado com sucesso');
        document.getElementById('registerUser').value = '';
        document.getElementById('registerCpf').value = '';
        document.getElementById('registerEmail').value = '';
        document.getElementById('registerSenha').value = '';
        toggleRegister();
    })
    .catch(err => alert(err.message));
}

function toggleRegister() {
    document.getElementById('registerBox').classList.toggle('d-none');
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('cpf');
    usuarioLogado = null;
    location.reload();
}

function showApp() {
    document.getElementById("loginView").classList.add("d-none");
    document.getElementById("appView").classList.remove("d-none");
    document.getElementById("mainNavbar").classList.remove("d-none");
}

function predizer() {
    const token = localStorage.getItem('token');

    if (!token) {
        return alert('Usuário não autenticado');
    }

    const payload = {
        age: Number(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        device_type: document.getElementById("device_type").value,
        time_on_site: Number(document.getElementById("time_on_site").value),
        pages_viewed: Number(document.getElementById("pages_viewed").value),
        previous_purchases: Number(document.getElementById("previous_purchases").value),
        cart_items: Number(document.getElementById("cart_items").value),
        returning_user: Number(document.getElementById("returning_user").value)
    };

    fetch(`${baseUrl}/predicao/predizer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro na predição");
        return res.json();
    })
    .then(data => {
    renderResultado(data);
    })
    .catch(err => alert(err.message));
}

function renderResultado(data) {
    const card = document.getElementById("resultadoCard");
    const titulo = document.getElementById("resultadoTitulo");
    const prob = document.getElementById("resultadoProb");

    // Remove classes antigas
    card.className = "card mt-4";

    const label = data.label;
    const percentual = (data.probabilidade_compra * 100).toFixed(2);

    titulo.innerText = label;
    prob.innerText = `Probabilidade estimada de compra: ${percentual}%`;

    if (label.includes("extremamente alta")) {
        card.classList.add("card-extrema");
    } else if (label.includes("Alta chance")) {
        card.classList.add("card-alta");
    } else if (label.includes("moderada")) {
        card.classList.add("card-media");
    } else if (label.includes("Baixa chance")) {
        card.classList.add("card-baixa");
    } else {
        card.classList.add("card-muito-baixa");
    }

    card.classList.remove("d-none");
}

window.onload = () => {
    const token = localStorage.getItem('token');
    const cpf = localStorage.getItem('cpf');

    if (token && cpf) {
        usuarioLogado = cpf;
        showApp();
    }
};