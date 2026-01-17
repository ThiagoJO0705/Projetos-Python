document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const btnLogin = document.querySelector('.btn-login');

    const showToast = (message, type = 'error') => {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <span style="margin-left:15px; cursor:pointer; opacity:0.7" onclick="this.parentElement.remove()">✕</span>
        `;
        container.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    };

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) return "O e-mail é obrigatório.";
        if (!re.test(email)) return "Formato de e-mail inválido.";
        return "";
    };

    const updateFieldUI = (input, errorId, msg) => {
        const errorSpan = document.getElementById(errorId);
        if (msg) {
            input.classList.add('error');
            errorSpan.innerText = msg;
            errorSpan.classList.add('active');
        } else {
            input.classList.remove('error');
            errorSpan.innerText = "";
            errorSpan.classList.remove('active');
        }
    };

    emailInput.addEventListener('input', () => {
        updateFieldUI(emailInput, 'email-error', validateEmail(emailInput.value.trim()));
    });

    passwordInput.addEventListener('input', () => {
        const msg = passwordInput.value ? "" : "A senha é obrigatória.";
        updateFieldUI(passwordInput, 'password-error', msg);
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = emailInput.value.trim();
        const password = passwordInput.value;
        const emailErr = validateEmail(email);
        const passErr = password ? "" : "A senha é obrigatória.";

        if (emailErr || passErr) {
            updateFieldUI(emailInput, 'email-error', emailErr);
            updateFieldUI(passwordInput, 'password-error', passErr);
            showToast("Verifique os campos destacados.");
            return;
        }

        btnLogin.disabled = true;
        const originalText = btnLogin.innerText;
        btnLogin.innerText = "AUTENTICANDO...";

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/signin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('refresh_token', data.refresh_token);
                const meResponse = await fetch('http://127.0.0.1:8000/auth/me', {
                    method: 'GET',
                    headers: { 'Authorization': `Bearer ${data.access_token}` }
                });

                const userData = await meResponse.json();

                if (meResponse.ok) {
                    localStorage.setItem('user_name', userData.name);
                    
                    showToast(`Bem-vindo, ${userData.name}!`, "success");
                    btnLogin.innerText = "REDIRECIONANDO...";
                    btnLogin.style.background = "var(--success-mint)";
                    setTimeout(() => {
                        if (userData.is_admin) {
                            window.location.href = 'admin.html';
                        } else {
                            window.location.href = 'dashboard.html';
                        }
                    }, 1000);

                } else {
                    showToast("Erro ao validar perfil do usuário.");
                    btnLogin.disabled = false;
                    btnLogin.innerText = originalText;
                }

            } else {
                showToast(data.detail || "E-mail ou senha incorretos.");
                btnLogin.disabled = false;
                btnLogin.innerText = originalText;
            }

        } catch (error) {
            showToast("Não foi possível conectar ao servidor JAVER.");
            btnLogin.disabled = false;
            btnLogin.innerText = originalText;
        }
    });
});