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

    const showToast = (message, type = 'error') => {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span>${message}</span><span style="margin-left:15px; cursor:pointer; font-weight:bold" onclick="this.parentElement.remove()">✕</span>`;
        container.appendChild(toast);
        setTimeout(() => { toast.classList.add('hiding'); setTimeout(() => toast.remove(), 500); }, 4000);
    };

    const loadDashboard = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            if (response.ok) {
                userId = data.id;
                currentBalance = parseFloat(data.account_balance);
                nameEl.innerText = data.name;
                balanceEl.innerText = `R$ ${currentBalance.toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                scoreEl.innerText = data.score;
                const percent = Math.min((data.score / 10000) * 100, 100);
                scoreBar.style.width = `${percent}%`;
                
                document.getElementById('profile-name').value = data.name;
                document.getElementById('profile-email').value = data.email;
                document.getElementById('profile-phone').value = data.phone_number;
                loadStatement();
            } else {
                localStorage.clear();
                window.location.href = 'index.html';
            }
        } catch (err) { showToast("Erro de conexão com o Banco JAVER."); }
    };

    window.loadStatement = async () => {
        statementList.innerHTML = '<p style="padding:20px; text-align:center; opacity:0.6;">Sincronizando extrato...</p>';
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/statement', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const list = await res.json();
            renderStatement(list);
        } catch (err) { statementList.innerHTML = '<p style="padding:20px; color:var(--error-red)">Erro ao carregar histórico.</p>'; }
    };

    const renderStatement = (transactions) => {
        if (!transactions || transactions.length === 0) {
            statementList.innerHTML = '<div style="padding:40px; text-align:center; color:#999;">Nenhuma movimentação encontrada.</div>';
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
        try {
            const res = await fetch(`http://127.0.0.1:8000/banking/deposit?deposit_value=${val}`, {
                method: 'POST', headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) { showToast("Dinheiro depositado!", "success"); closeModal('modal-deposit'); loadDashboard(); }
        } catch (e) { showToast("Erro no servidor."); }
    };

    document.getElementById('btn-confirm-pix').onclick = async () => {
        const key = document.getElementById('pix-key').value;
        const amount = parseFloat(document.getElementById('pix-amount').value);
        if (amount > currentBalance) return showToast("Saldo insuficiente.");
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/pix', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ pix_key: key, pix_amount: amount })
            });
            if (res.ok) { showToast("Pix enviado!", "success"); closeModal('modal-pix'); loadDashboard(); }
            else { const d = await res.json(); showToast(d.detail); }
        } catch (e) { showToast("Erro de conexão."); }
    };

    document.getElementById('btn-confirm-payment').onclick = async () => {
        const desc = document.getElementById('pay-desc').value;
        const amount = parseFloat(document.getElementById('pay-amount').value);
        const method = document.getElementById('pay-method').value;
        if (amount > currentBalance) return showToast("Saldo insuficiente.");
        try {
            const res = await fetch('http://127.0.0.1:8000/banking/payment', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount, method, description: desc })
            });
            if (res.ok) { showToast("Pagamento aprovado!", "success"); closeModal('modal-payment'); loadDashboard(); }
        } catch (e) { showToast("Erro no processamento."); }
    };

    document.getElementById('btn-save-profile').onclick = async () => {
        const payload = {
            name: document.getElementById('profile-name').value,
            email: document.getElementById('profile-email').value,
            phone_number: document.getElementById('profile-phone').value
        };
        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/${userId}`, {
                method: 'PATCH',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) { showToast("Perfil atualizado!", "success"); closeModal('modal-profile'); loadDashboard(); }
        } catch (e) { showToast("Erro ao atualizar."); }
    };

    document.getElementById('btn-confirm-close').onclick = async () => {
        if (currentBalance > 0) {
            showToast(`Ação negada. Retire seu saldo de R$ ${currentBalance.toFixed(2)} antes de encerrar.`, "error");
            closeModal('modal-close-account');
            return;
        }

        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/disable/${userId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.ok) {
                localStorage.clear();
                window.location.href = 'index.html'; 
            } else {
                const data = await res.json();
                showToast(data.detail || "Erro ao processar encerramento.");
            }
        } catch (e) { showToast("Servidor indisponível."); }
    };

    const btnToggle = document.getElementById('btn-toggle-balance');
    const eyeIcon = document.getElementById('eye-icon');
    let isVisible = localStorage.getItem('hide_balance') !== 'true';

    const updateVisibility = () => {
        if (isVisible) { balanceEl.classList.remove('blur-active'); eyeIcon.className = "fa-regular fa-eye"; }
        else { balanceEl.classList.add('blur-active'); eyeIcon.className = "fa-regular fa-eye-slash"; }
    };

    btnToggle.onclick = () => { isVisible = !isVisible; localStorage.setItem('hide_balance', !isVisible); updateVisibility(); };
    
    document.getElementById('btn-logout').onclick = () => {
        localStorage.clear();
        window.location.href = 'index.html';
    };

    loadDashboard();
    updateVisibility();
});

function openModal(id) { document.getElementById(id).style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }