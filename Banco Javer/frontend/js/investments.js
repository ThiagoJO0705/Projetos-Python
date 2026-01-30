const showLoader = () => document.getElementById('loading-overlay').style.display = 'flex';
const hideLoader = () => document.getElementById('loading-overlay').style.display = 'none';
const showToast = (msg, type='error') => {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
};

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const API = "http://127.0.0.1:8003";

    if (!token) window.location.href = 'index.html';

    let charts = {};

    // 1. CARREGAMENTO INICIAL (Net Worth, Analytics, Investments Me, Projection)
    const init = async () => {
        showLoader();
        try {
            // [Endpoint 11] Net Worth
            const nwRes = await fetch(`${API}/analytics/calculations/net-worth/me`, { headers: { 'Authorization': `Bearer ${token}` } });
            const nw = await nwRes.json();
            document.getElementById('total-net-worth').innerText = `R$ ${nw.total_net_worth.toLocaleString('pt-BR')}`;
            document.getElementById('usd-rate-info').innerText = `Câmbio: R$ ${nw.usd_rate}`;

            // [Endpoint 9] Wallet Analysis
            const anRes = await fetch(`${API}/analytics/wallet/me`, { headers: { 'Authorization': `Bearer ${token}` } });
            const analysis = await anRes.json();
            document.getElementById('investor-profile').innerText = analysis.customer_info.profile;

            // [Endpoint 1] Investments Me
            const invRes = await fetch(`${API}/investments/me`, { headers: { 'Authorization': `Bearer ${token}` } });
            const investments = await invRes.json();

            // [Endpoint 10] Projection
            const projRes = await fetch(`${API}/analytics/calculations/projection/me`, { headers: { 'Authorization': `Bearer ${token}` } });
            const projection = await projRes.json();

            renderCharts(analysis, projection);
            renderTable(investments);

        } catch (e) { showToast("Sua carteira está vazia ou a API 8003 está offline."); }
        finally { hideLoader(); }
    };

    // 2. BUSCA DE MERCADO (Endpoints 6 e 7)
    window.searchMarket = async () => {
        const query = document.getElementById('market-search').value;
        if(!query) return;
        showLoader();
        try {
            // Tenta buscar por Nome primeiro [Endpoint 7]
            const res = await fetch(`${API}/assets/search/name/${query}`);
            const data = await res.json();
            renderSearchResults(data);
        } catch (e) {
            // Se falhar, tenta por Ticker [Endpoint 6]
            try {
                const res = await fetch(`${API}/assets/search/ticker/${query}`);
                const data = await res.json();
                renderSearchResults([data]);
            } catch (err) { showToast("Ativo não encontrado."); }
        } finally { hideLoader(); }
    };

    const renderSearchResults = (results) => {
        const div = document.getElementById('search-results');
        div.innerHTML = results.map(r => `
            <div class="search-item card">
                <div>
                    <strong>${r.ticker || r.symbol}</strong>
                    <p>${r.name}</p>
                </div>
                <button class="btn-buy-small" onclick="prepBuy('${r.ticker}')">Comprar</button>
            </div>
        `).join('');
    };

    // 3. COMPRA (Endpoint 2)
    window.prepBuy = (ticker) => {
        window.currentTicker = ticker;
        document.getElementById('buy-asset-name').innerText = `Ativo selecionado: ${ticker}`;
        openModal('modal-buy');
    };

    document.getElementById('btn-confirm-buy').onclick = async () => {
        const qty = document.getElementById('buy-qty').value;
        showLoader();
        const res = await fetch(`${API}/investments/buy`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker: window.currentTicker, quantity: parseFloat(qty) })
        });
        if(res.ok) location.reload();
        else { const d = await res.json(); showToast(d.detail); hideLoader(); }
    };

    // 4. REGISTRO ANTIGO (Endpoint 3)
    document.getElementById('btn-confirm-reg').onclick = async () => {
        const payload = {
            ticker: document.getElementById('reg-ticker').value,
            quantity: document.getElementById('reg-qty').value,
            purchase_price: document.getElementById('reg-price').value,
            purchase_date: document.getElementById('reg-date').value
        };
        showLoader();
        const res = await fetch(`${API}/investments/register`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if(res.ok) location.reload();
        else { const d = await res.json(); showToast(d.detail); hideLoader(); }
    };

    // 5. VENDA / UPDATE (Endpoint 4)
    window.sellAsset = async (id, currentQty) => {
        const qty = prompt(`Quantas cotas deseja vender? (Máx: ${currentQty})`);
        if(!qty || qty > currentQty) return;
        showLoader();
        const res = await fetch(`${API}/investments/${id}`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: currentQty - parseFloat(qty) })
        });
        if(res.ok) location.reload();
        else hideLoader();
    };

    const renderCharts = (analysis, projection) => {
        // [Gráficos usando dados dinâmicos do Wallet Analysis]
        const ctxPie = document.getElementById('chart-allocation').getContext('2d');
        new Chart(ctxPie, { type: 'doughnut', data: { labels: Object.keys(analysis.charts.allocation_by_type), datasets: [{ data: Object.values(analysis.charts.allocation_by_type), backgroundColor: ['#0a173d', '#f3681e', '#a6cfc0', '#fce210'] }] } });

        const ctxBar = document.getElementById('chart-performance').getContext('2d');
        new Chart(ctxBar, { type: 'bar', data: { labels: Object.keys(analysis.charts.profit_loss_by_ticker), datasets: [{ label: '%', data: Object.values(analysis.charts.profit_loss_by_ticker), backgroundColor: '#f3681e' }] } });

        const ctxLine = document.getElementById('chart-projection').getContext('2d');
        new Chart(ctxLine, { type: 'line', data: { labels: ['Mês 0', 'Mês 6', 'Mês 12'], datasets: [{ label: 'Renda Fixa', data: [projection.current_value, projection.current_value * 1.05, projection.projected_value], borderColor: '#a6cfc0', fill: true }] } });
    };

    const renderTable = (investments) => {
        const list = document.getElementById('investment-list');
        list.innerHTML = investments.map(inv => `
            <div class="asset-item">
                <div class="asset-info">
                    <strong>${inv.asset.ticker}</strong>
                    <span>${inv.quantity} cotas | Médio: R$ ${inv.purchase_price}</span>
                </div>
                <div class="asset-values">
                    <span>R$ ${inv.current_value_brl}</span>
                    <button class="btn-sell" onclick="sellAsset('${inv.id}', ${inv.quantity})">Vender</button>
                </div>
            </div>
        `).join('');
    };

    init();
});

function openModal(id) { document.getElementById(id).style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }