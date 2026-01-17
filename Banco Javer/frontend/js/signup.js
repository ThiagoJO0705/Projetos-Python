document.addEventListener('DOMContentLoaded', () => {

    const signupForm = document.getElementById('signup-form');
    const btnSignup = document.getElementById('btn-finalizar');
    const inputs = ['name', 'email', 'cpf', 'phone', 'password'];
    const showToast = (message, type = 'error') => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <span style="margin-left:15px; cursor:pointer; font-weight:bold" onclick="this.parentElement.remove()">✕</span>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    };

    const validationRules = {
        name: (val) => val.trim().split(' ').length < 2 ? "Insira nome e sobrenome" : "",
        email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val) ? "" : "E-mail inválido",
        cpf: (val) => val.replace(/\D/g, '').length !== 11 ? "CPF deve ter 11 números" : "",
        phone: (val) => val.replace(/\D/g, '').length < 10 ? "Telefone inválido" : "",
        password: (val) => val.length < 4 ? "Mínimo 4 caracteres" : ""
    };

    const updateFieldUI = (id, errorMessage) => {
        const input = document.getElementById(id);
        const errorSpan = document.getElementById(`${id}-error`);
        if (!input || !errorSpan) return;

        if (errorMessage) {
            input.classList.add('error');
            errorSpan.innerText = errorMessage;
            errorSpan.style.opacity = "1";
        } else {
            input.classList.remove('error');
            errorSpan.innerText = "";
            errorSpan.style.opacity = "0";
        }
    };

    inputs.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => {
                const error = validationRules[id](el.value);
                updateFieldUI(id, error);
            });
        }
    });

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        const payload = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            cpf: document.getElementById('cpf').value.replace(/\D/g, ''),
            phone_number: document.getElementById('phone').value.replace(/\D/g, ''),
            password: document.getElementById('password').value
        };

        let hasErrors = false;
        for (let key in payload) {
            const fieldId = key === 'phone_number' ? 'phone' : key;
            const errorMsg = validationRules[fieldId](document.getElementById(fieldId).value);
            if (errorMsg) {
                updateFieldUI(fieldId, errorMsg);
                hasErrors = true;
            }
        }

        if (hasErrors) {
            showToast("Preencha os campos em vermelho.");
            return;
        }

        btnSignup.disabled = true;
        btnSignup.innerText = "PROCESSANDO...";

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                showToast("CONTA CRIADA! Redirecionando...", "success");
                btnSignup.style.background = "#a6cfc0"; 
                btnSignup.innerText = "CONTA CRIADA!";
                setTimeout(() => {
                    window.location.href = "index.html"; 
                }, 2500);

            } else {
                showToast(data.detail || "Erro ao processar cadastro.");
                btnSignup.disabled = false;
                btnSignup.innerText = "FINALIZAR CADASTRO";
            }

        } catch (error) {
            showToast("Erro de conexão. O servidor está ligado?");
            btnSignup.disabled = false;
            btnSignup.innerText = "FINALIZAR CADASTRO";
        }
    });
});