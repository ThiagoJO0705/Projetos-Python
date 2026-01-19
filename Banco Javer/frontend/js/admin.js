document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) window.location.href = 'index.html';
    const customersList = document.getElementById('customers-list');
    const btnFilter = document.getElementById('btn-filter');
    const modalEdit = document.getElementById('modal-edit');
    const editForm = document.getElementById('edit-form');
    const btnSaveEdit = document.getElementById('btn-save-edit');
    let originalData = {};
    const showToast = (message, type = 'error') => {
        const container = document.getElementById('toast-container');
        if (!container) return;
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

    const updateModalUI = (field, msg) => {
        const input = document.getElementById(`edit-${field}`);
        const errorSpan = document.getElementById(`edit-${field}-error`);
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

    ['edit-cpf', 'edit-phone'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '');
            });
        }
    });

    ['name', 'email', 'cpf', 'phone'].forEach(field => {
        const el = document.getElementById(`edit-${field}`);
        if (el) {
            el.addEventListener('input', (e) => {
                updateModalUI(field, validate[field](e.target.value));
            });
        }
    });

    const showSkeleton = () => {
        customersList.innerHTML = Array(5).fill(`
            <tr class="skeleton-row">
                <td colspan="7"><div class="skeleton-line"></div></td>
            </tr>
        `).join('');
    };

    const loadCustomers = async () => {
        showSkeleton();

        const name = document.getElementById('search-name').value;
        const status = document.getElementById('filter-status').value;
        const isAdmin = document.getElementById('filter-admin').value; 
        let params = new URLSearchParams();
        if (name) params.append('name', name);
        if (status) params.append('is_active', status);
        if (isAdmin) params.append('is_admin', isAdmin);

        try {
            const response = await fetch(`http://127.0.0.1:8000/admin/customers?${params.toString()}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const customers = await response.json();
            
            setTimeout(() => renderTable(customers), 600);
        } catch (err) {
            showToast("Erro ao conectar com o Banco JAVER.");
        }
    };

    const renderTable = (customers) => {
        if (!customers || customers.length === 0) {
            customersList.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:50px; color:var(--text-muted)">Nenhum cliente encontrado.</td></tr>';
            return;
        }

        customersList.innerHTML = customers.map(c => `
            <tr>
                <td style="font-weight:700; color:var(--text-muted)">#${c.id}</td>
                <td>
                    <div style="font-weight:700">${c.name} ${c.is_admin ? '<span style="color:var(--secondary-orange); font-size:10px; margin-left:5px;">(ADM)</span>' : ''}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted)">${c.email}</div>
                </td>
                <td>${c.cpf}</td>
                <td style="font-weight:700">R$ ${parseFloat(c.account_balance).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
                <td><b style="color:var(--secondary-orange)">${c.score}</b></td>
                <td>
                    <span class="status-badge ${c.is_active ? 'active' : 'inactive'}">
                        ${c.is_active ? '● ATIVO' : '○ INATIVO'}
                    </span>
                </td>
                <td class="actions-cell">
                    <button onclick='openEditModal(${JSON.stringify(c)})' class="action-btn edit">✎ Editar</button>
                    ${c.is_active 
                        ? `<button onclick="handleDisable(${c.id}, ${c.account_balance})" class="action-btn disable">✕ Desativar</button>`
                        : `<button onclick="handleActivate(${c.id})" class="action-btn activate">✓ Ativar</button>`
                    }
                </td>
            </tr>
        `).join('');
    };

    window.openEditModal = (c) => {
        originalData = { 
            name: c.name, 
            email: c.email, 
            cpf: c.cpf, 
            phone_number: c.phone_number ,
            is_admin: c.is_admin
        };

        document.getElementById('edit-id').value = c.id;
        document.getElementById('edit-name').value = c.name;
        document.getElementById('edit-email').value = c.email;
        document.getElementById('edit-cpf').value = c.cpf;
        document.getElementById('edit-phone').value = c.phone_number;
        document.getElementById('edit-is-admin').checked = c.is_admin;
        
        modalEdit.style.display = 'flex';
    };

    window.closeModal = () => {
        modalEdit.style.display = 'none';
        ['name', 'email', 'cpf', 'phone'].forEach(f => updateModalUI(f, ""));
    };

    editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const id = document.getElementById('edit-id').value;
        const currentData = {
            name: document.getElementById('edit-name').value.trim(),
            email: document.getElementById('edit-email').value.trim(),
            cpf: document.getElementById('edit-cpf').value.replace(/\D/g, ''),
            phone_number: document.getElementById('edit-phone').value.replace(/\D/g, ''),
            is_admin: document.getElementById('edit-is-admin').checked
        };

        let hasErrors = false;
        ['name', 'email', 'cpf', 'phone'].forEach(f => {
            const val = (f === 'cpf' || f === 'phone') ? currentData[f === 'phone' ? 'phone_number' : 'cpf'] : currentData[f];
            const msg = validate[f](val);
            if (msg) { updateModalUI(f, msg); hasErrors = true; }
        });
        if (hasErrors) return;

        const payload = {};
        if (currentData.name !== originalData.name) payload.name = currentData.name;
        if (currentData.email !== originalData.email) payload.email = currentData.email;
        if (currentData.cpf !== originalData.cpf) payload.cpf = currentData.cpf;
        if (currentData.phone_number !== originalData.phone_number) payload.phone_number = currentData.phone_number;
        if (currentData.is_admin !== originalData.is_admin) payload.is_admin = currentData.is_admin;

        if (Object.keys(payload).length === 0) {
            showToast("Nenhuma alteração detectada.");
            closeModal();
            return;
        }

        btnSaveEdit.disabled = true;
        btnSaveEdit.innerText = "SALVANDO...";

        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/${id}`, {
                method: 'PATCH',
                headers: { 
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                showToast("Dados atualizados com sucesso!", "success");
                closeModal();
                loadCustomers();
            } else {
                const errData = await res.json();
                showToast(errData.detail || "Erro ao atualizar.");
            }
        } catch (err) {
            showToast("Erro de conexão.");
        } finally {
            btnSaveEdit.disabled = false;
            btnSaveEdit.innerText = "Salvar Alterações";
        }
    });

    let customerIdToDisable = null;

    window.handleDisable = (id, balance) => {
        if (parseFloat(balance) > 0) {
            showToast(`BLOQUEADO: Saldo de R$ ${balance}. Zere a conta antes de desativar.`, "error");
            return;
        }

        customerIdToDisable = id;
        document.getElementById('modal-confirm').style.display = 'flex';
    };

    window.closeConfirmModal = () => {
        document.getElementById('modal-confirm').style.display = 'none';
        customerIdToDisable = null;
    };

    document.getElementById('btn-confirm-disable').onclick = async () => {
        if (!customerIdToDisable) return;

        try {
            const res = await fetch(`http://127.0.0.1:8000/admin/customers/disable/${customerIdToDisable}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.ok) {
                showToast("Usuário desativado com sucesso!", "success");
                closeConfirmModal();
                loadCustomers(); 
            } else {
                showToast("Erro ao tentar desativar o usuário.");
            }
        } catch (err) {
            showToast("Erro de conexão com o servidor.");
        }
    };

    window.handleActivate = async (id) => {
        const res = await fetch(`http://127.0.0.1:8000/admin/customer/activate/${id}`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            showToast("Conta reativada com sucesso!", "success");
            loadCustomers();
        }
    };

    document.getElementById('btn-logout').onclick = () => {
        localStorage.clear();
        window.location.href = 'index.html';
    };

    btnFilter.onclick = loadCustomers;
    document.getElementById('admin-display-name').innerText = localStorage.getItem('user_name') || 'Admin';
    loadCustomers();
});