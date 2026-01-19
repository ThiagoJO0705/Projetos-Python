document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) window.location.href = 'index.html';
    const balanceEl = document.getElementById('balance-value');
    const scoreEl = document.getElementById('score-value');
    const scoreBar = document.getElementById('score-bar');
    const nameEl = document.getElementById('display-user-name');
    const statementList = document.getElementById('statement-list');
    let currentBalance = 0;
    let userId = null;
    let originalProfileData = {}; 

    const showToast = (message, type = 'error') => {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span>${message}</span><span style="margin-left:15px; cursor:pointer; font-weight:bold" onclick="this.parentElement.remove()">✕</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 500);
        }, 4000);
    };

    const showLoader = () => {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'flex';
    };

    const hideLoader = () => {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';
    };

    const validate = {
        name: (v) => {
            const regex = /^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$/; 
            if (v.trim().split(' ').length < 2) return "Insira nome e sobrenome";
            if (!regex.test(v)) return "O nome não pode conter números ou símbolos";
            return "";
        },
        email: (v) => {
            const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            return regex.test(v) ? "" : "E-mail inválido";
        },
        cpf: (v) => {
            const nums = v.replace(/\D/g, '');
            return nums.length !== 11 ? "CPF deve ter 11 números" : "";
        },
        phone: (v) => {
            const nums = v.replace(/\D/g, '');
            return (nums.length < 10 || nums.length > 11) ? "Telefone inválido" : "";
        }
    };

    const updateFieldUI = (id, msg) => {
        const input = document.getElementById(id);
        const errorSpan = document.getElementById(`${id}-error`);
        if (!input || !errorSpan) return;

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

    ['profile-cpf', 'profile-phone'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '');
            });
        }
    });

    ['profile-name', 'profile-email', 'profile-cpf', 'profile-phone'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', (e) => {
                const type = id.split('-')[1];
                updateFieldUI(id, validate[type](e.target.value));
            });
        }
    });

    const loadDashboard = async () => {
        showLoader();
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();

            if (response.ok) {
                userId = data.id;
                currentBalance = parseFloat(data.account_balance);
                
                originalProfileData = {
                    name: data.name,
                    email: data.email,
                    cpf: data.cpf,
                    phone_number: data.phone_number
                };

                nameEl.innerText = data.name;
                balanceEl.innerText = `R$ ${currentBalance.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                scoreEl.innerText = data.score;
                const percent = Math.min((data.score / 10000) * 100, 100);
                scoreBar.style.width = `${percent}%`;

                document.getElementById('profile-name').value = data.name;
                document.getElementById('profile-email').value = data.email;
                document.getElementById('profile-cpf').value = data.cpf;
                document.getElementById('profile-phone').value = data.phone_number;
                loadStatement();
            } else {
                localStorage.clear();
                window.location.href = 'index.html';
            }
        } catch (err) {
            showToast("Erro ao sincronizar com o Banco JAVER.");
        } finally {
            hideLoader();
        }
    };

    window.loadStatement = async () => {
        statementList.innerHTML = '<p style="padding:20px; text-align:center; opacity:0.6;">Sincronizando extrato...</p>';
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/statement', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const list = await res.json();
            renderStatement(list);
        } catch (err) {
            statementList.innerHTML = '<p style="padding:20px; color:var(--error-red)">Erro ao carregar histórico.</p>';
        }
    };

    const renderStatement = (transactions) => {
        if (!transactions || transactions.length === 0) {
            statementList.innerHTML = '<div style="padding:40px; text-align:center; color:#999;"><i class="fa-solid fa-receipt" style="font-size:2rem; margin-bottom:10px; display:block;"></i>Nenhuma movimentação encontrada.</div>';
            return;
        }

        statementList.innerHTML = transactions.map(t => `
            <div class="statement-item">
                <div style="display:flex; align-items:center;">
                    <i class="fa-solid ${t.direction === 'CREDIT' ? 'fa-circle-plus credit' : 'fa-circle-minus debit'}" style="margin-right:15px; font-size:1.2rem;"></i>
                    <div class="st-info">
                        <h4>${t.description || t.type}</h4>
                        <small>${new Date(t.created_at).toLocaleString('pt-BR')}</small>
                    </div>
                </div>
                <div class="st-value ${t.direction === 'CREDIT' ? 'credit' : 'debit'}">
                    ${t.direction === 'CREDIT' ? '+' : '-'} R$ ${parseFloat(t.amount).toFixed(2)}
                </div>
            </div>
        `).join('');
    };

    document.getElementById('btn-confirm-deposit').onclick = async () => {
        const val = document.getElementById('deposit-amount').value;
        if (!val || val <= 0) return showToast("Valor inválido.");
        showLoader();
        try {
            const res = await fetch(`http://127.0.0.1:8000/banking/deposit?deposit_value=${val}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                showToast("Depósito realizado!", "success");
                closeModal('modal-deposit');
                await loadDashboard();
            } else {
                const err = await res.json();
                showToast(err.detail || "Erro no depósito.");
            }
        } catch (e) { showToast("Erro no servidor."); 
        } finally {
            hideLoader(); 
        }
    };

    document.getElementById('btn-confirm-pix').onclick = async () => {
        const key = document.getElementById('pix-key').value;
        const amount = parseFloat(document.getElementById('pix-amount').value);

        if (isNaN(amount) || !key) return showToast("Verifique os dados.");
        if (amount <= 0) return showToast("Saldo deve ser positivo.")
        if (amount > currentBalance) return showToast("Saldo insuficiente.");
        showLoader();
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/pix', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ pix_key: key, pix_amount: amount })
            });
            if (res.ok) {
                showToast("Pix enviado!", "success");
                closeModal('modal-pix');
                await loadDashboard();
            } else {
                const d = await res.json();
                showToast(d.detail);
            }
        } catch (e) { showToast("Erro de conexão."); 
        } finally {
            hideLoader(); 
        }
    };

    document.getElementById('btn-confirm-payment').onclick = async () => {
        const desc = document.getElementById('pay-desc').value;
        const amount = parseFloat(document.getElementById('pay-amount').value);
        const method = document.getElementById('pay-method').value;

        if (!desc) return showToast("A descrição não pode ser vazia.")
        if (isNaN(amount)) return showToast("Dados inválidos.");
        if (amount <= 0) return showToast("O Valor deve ser positivo.")
        if (amount > currentBalance) return showToast("Saldo insuficiente.");
        showLoader();
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/payment', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount, method, description: desc })
            });
            if (res.ok) {
                showToast("Pagamento realizado!", "success");
                closeModal('modal-payment');
                await loadDashboard();
            }
        } catch (e) { showToast("Erro no processamento."); 
        } finally {
            hideLoader(); 
        }
    };

    document.getElementById('btn-save-profile').onclick = async () => {
        const currentData = {
            name: document.getElementById('profile-name').value.trim(),
            email: document.getElementById('profile-email').value.trim(),
            cpf: document.getElementById('profile-cpf').value.replace(/\D/g, ''),
            phone_number: document.getElementById('profile-phone').value.replace(/\D/g, '')
        };

        const nameErr = validate.name(currentData.name);
        const emailErr = validate.email(currentData.email);
        const cpfErr = validate.cpf(currentData.cpf);
        const phoneErr = validate.phone(currentData.phone_number);
        
        updateFieldUI('profile-name', nameErr);
        updateFieldUI('profile-email', emailErr);
        updateFieldUI('profile-cpf', cpfErr);
        updateFieldUI('profile-phone', phoneErr);

        if (nameErr || emailErr || cpfErr || phoneErr) {
            showToast("Corrija os campos em vermelho.");
            return;
        }

        const payload = {};
        if (currentData.name !== originalProfileData.name) payload.name = currentData.name;
        if (currentData.email !== originalProfileData.email) payload.email = currentData.email;
        if (currentData.cpf !== originalProfileData.cpf) payload.cpf = currentData.cpf;
        if (currentData.phone_number !== originalProfileData.phone_number) payload.phone_number = currentData.phone_number;

        if (Object.keys(payload).length === 0) {
            closeModal('modal-profile');
            return;
        }
        showLoader();
        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/${userId}`, {
                method: 'PATCH',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                showToast("Perfil atualizado!", "success");
                closeModal('modal-profile');
                await loadDashboard();
            } else {
                const d = await res.json();
                showToast(d.detail || "Erro ao atualizar.");
            }
        } catch (e) { showToast("Erro ao conectar."); 
        } finally {
            hideLoader(); 
        }
    };

    document.getElementById('btn-confirm-close').onclick = async () => {
        if (currentBalance > 0) {
            showToast(`Erro: Retire seu saldo de R$ ${currentBalance.toFixed(2)} primeiro.`, "error");
            closeModal('modal-close-account');
            return;
        }
        showLoader();
        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/disable/${userId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                localStorage.clear();
                window.location.href = 'index.html'; 
            }
        } catch (e) { showToast("Erro no servidor."); 
        } finally {
            hideLoader(); 
        }
    };

    const btnToggle = document.getElementById('btn-toggle-balance');
    const eyeIcon = document.getElementById('eye-icon');
    let isVisible = localStorage.getItem('hide_balance') !== 'true';

    const updateVisibility = () => {
        if (isVisible) {
            balanceEl.classList.remove('blur-active');
            eyeIcon.className = "fa-regular fa-eye";
        } else {
            balanceEl.classList.add('blur-active');
            eyeIcon.className = "fa-regular fa-eye-slash";
        }
    };

    btnToggle.onclick = () => {
        isVisible = !isVisible;
        localStorage.setItem('hide_balance', !isVisible);
        updateVisibility();
    };

    document.getElementById('btn-logout').onclick = () => {
        localStorage.clear();
        window.location.href = 'index.html';
    };

    loadDashboard();
    updateVisibility();
});

function openModal(id) { document.getElementById(id).style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }