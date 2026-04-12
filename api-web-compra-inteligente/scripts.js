let usuarioLogado = null;
let editId = null;
let editUsuarioCpf = null;
let baseUrl = `http://localhost:5000`;

console.log("scripts.js carregado com sucesso");

function login() {
    const cpf = document.getElementById('loginCpf').value;
    const senha = document.getElementById('loginSenha').value;

    if (!cpf || !senha) {
        return Swal.fire({
            title: 'Campos Obrigatórios',
            text: 'Por favor, informe o CPF e a Senha.',
            icon: 'warning',
            confirmButtonColor: '#3085d6'
        });
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
        sessionStorage.setItem('token', data.access_token);
        sessionStorage.setItem('cpf', cpf);

        usuarioLogado = cpf;

        Swal.fire({
            title: 'Bem-vindo!',
            text: 'Login realizado com sucesso.',
            icon: 'success',
            timer: 1500,
            showConfirmButton: false
        }).then(() => {
            showApp();
        });
    })
    .catch(err => {
        Swal.fire({
            title: 'Erro de Login',
            text: err.message,
            icon: 'error',
            confirmButtonColor: '#d33',
            confirmButtonText: 'Tentar novamente'
        });
    });
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

function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);

    if(input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🔒';
    } else {
        input.type = 'password';
        btn.textContent = '👁️';
    }
}

function logout() {
    Swal.fire({
        title: 'Sair do Sistema?',
        text: "Você precisará fazer login novamente para acessar as predições.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#28a745', // Verde (combinando com seu card)
        cancelButtonColor: '#dc3545',  // Vermelho
        confirmButtonText: 'Sim, sair!',
        cancelButtonText: 'Cancelar',
        reverseButtons: true // Coloca o "Sim" na direita, padrão de UX
    }).then((result) => {
        if (result.isConfirmed) {
            // Se o usuário confirmou, limpa tudo
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('cpf');
            
            // Garantindo que não sobrou nada no localStorage de testes antigos
            localStorage.removeItem('token');
            localStorage.removeItem('cpf');

            usuarioLogado = null;
            
            // Redireciona ou recarrega
            location.reload();
        }
    });
}

function showApp() {
    document.getElementById("loginView").classList.add("d-none");
    document.getElementById("appView").classList.remove("d-none");
    document.getElementById("mainNavbar").classList.remove("d-none");
    document.getElementById("secao-info").classList.remove("d-none");
}

function predizer() {
    const token = sessionStorage.getItem('token');

    if (!token) {
        return alert('Usuário não autenticado');
    }

    // Captura dos dados do formulário
    const payload = {
        age: Number(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        device_type: document.getElementById("device_type").value,
        previous_purchases: Number(document.getElementById("previous_purchases").value),
        returning_user: Number(document.getElementById("returning_user").value),
        discount_seen: Number(document.getElementById("discount_seen").value),
        ad_clicked: Number(document.getElementById("ad_clicked").value),
        cart_items: Number(document.getElementById("cart_items").value)
    };

    // Chamada ao backend
    fetch(`${baseUrl}/predicao/predizer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    })
    .then(res => {
        // Tratamento de erro específico para o status 422 (validação do Schema)
        if (res.status === 422) {
            throw new Error("Erro de validação: Verifique se todos os campos foram preenchidos corretamente.");
        }
        if (!res.ok) {
            throw new Error("Erro na predição. Verifique sua conexão ou autenticação.");
        }
        return res.json();
    })
    .then(data => {
        renderResultado(data, payload);
        setTimeout(() => {
            const cardResultado = document.getElementById("resultadoCard");
            cardResultado.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }, 100);
    })
    .catch(err => {
        console.error("Erro no processo de predição:", err);
        alert(err.message);
    });
}

function gerarDicaPersonalizada(payload, data) {
    const label = data.faixa_conversao;
    const { cart_items, discount_seen, ad_clicked, previous_purchases } = payload;

    // Caso 1: Probabilidade Alta, mas tem poucos itens
    if (label.includes("Alta") && cart_items < 2) {
        return "O cliente tem interesse! Que tal uma promoção 'Leve 2, Pague 1' em produtos similares para aumentar o ticket médio?";
    }

    // Caso 2: Já viu desconto e a chance ainda é moderada/baixa
    if (discount_seen === 1 && (label.includes("moderada") || label.includes("Baixa"))) {
        return "O desconto anterior não foi suficiente. Ofereça um cupom exclusivo de 'Primeira Compra' ou frete grátis por tempo limitado.";
    }

    // Caso 3: Veio de anúncio, mas a chance é baixa
    if (ad_clicked === 1 && label.includes("Baixa")) {
        return "O anúncio atraiu o cliente, mas o produto não convenceu. Sugira os 'Mais Vendidos' da categoria para manter o interesse.";
    }

    // Caso 4: Cliente fiel (compras anteriores) com chance moderada
    if (previous_purchases > 0 && label.includes("moderada")) {
        return "Este é um cliente recorrente! Ofereça um bônus de fidelidade ou acesso antecipado à nova coleção.";
    }

    // Caso 5: Chance Extremamente Alta
    if (label.includes("extremamente alta")) {
        return "Conversão iminente! Remova qualquer barreira: destaque o checkout rápido e a garantia de devolução.";
    }

    return "Foque em engajamento: convide o usuário a assinar a newsletter para receber novidades.";
}

function renderResultado(data, payload) {
    const card = document.getElementById("resultadoCard");
    const titulo = document.getElementById("resultadoTitulo");
    const probTexto = document.getElementById("resultadoProb");
    const dicaContainer = document.getElementById("dicaTexto"); // Certifique-se de ter esse ID no HTML

    // Reset de classes
    card.className = "card mt-4";

    const label = data.faixa_conversao;
    const percentual = (data.probabilidade_compra * 100).toFixed(2);

    titulo.innerText = label;
    probTexto.innerText = `Probabilidade estimada de compra: ${percentual}%`;

    // Inserção da Dica Estratégica
    const dicaSugestao = gerarDicaPersonalizada(payload, data);
    if (dicaContainer) {
        dicaContainer.innerHTML = `<strong>Estratégia Sugerida:</strong> ${dicaSugestao}`;
    }

    // Lógica de cores
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
    const token = sessionStorage.getItem('token');
    const cpf = sessionStorage.getItem('cpf');

    if (token && cpf) {
        usuarioLogado = cpf;
        showApp();
    }
};