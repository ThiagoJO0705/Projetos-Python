document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const API = "http://127.0.0.1:8003";

    if (!token) window.location.href = 'index.html';

    // --- VARIÁVEIS GLOBAIS DE CONTROLE ---
    let globalUsdRate = 1;
    let lastAnalysisData = null;
    let currentPeriod = '1y';

    // Instâncias dos Gráficos
    let chartAlloc = null;
    let chartPerf = null;
    let chartEvol = null;
    let chartBench = null;
    let chartProj = null;

    // --- UTILITÁRIOS ---
    const showToast = (msg, type = 'error') => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `<span>${msg}</span><span style="margin-left:15px; cursor:pointer" onclick="this.parentElement.remove()">✕</span>`;
        container.appendChild(toast);
        setTimeout(() => { toast.classList.add('hiding'); setTimeout(() => toast.remove(), 500); }, 4000);
    };

    const showLoader = () => document.getElementById('loading-overlay').style.display = 'flex';
    const hideLoader = () => document.getElementById('loading-overlay').style.display = 'none';

    // --- CARREGAMENTO PRINCIPAL ---
    const loadAllInvestmentsData = async () => {
        showLoader();
        try {
            const headers = { 'Authorization': `Bearer ${token}` };
            const [netWorthRes, walletRes, projRes, invRes, trendingRes] = await Promise.all([
                fetch(`${API}/analytics/calculations/net-worth/me`, { headers }),
                fetch(`${API}/analytics/wallet/me`, { headers }),
                fetch(`${API}/analytics/calculations/projection/me`, { headers }),
                fetch(`${API}/investments/me`, { headers }),
                fetch(`${API}/assets/trending`, { headers }).catch(() => null)
            ]);

            const netWorth = await netWorthRes.json();
            globalUsdRate = netWorth.usd_rate || 1;
            const analysis = await walletRes.json();
            lastAnalysisData = analysis;
            const projection = await projRes.json();
            const myInvestments = await invRes.json();
            const trending = trendingRes ? await trendingRes.json() : [];

            // Atualiza Componentes
            updateKPIs(netWorth, analysis);
            renderTrending(trending);
            renderInventoryTable(myInvestments, analysis);

            if (walletRes.ok && analysis.charts) {
                renderCharts(analysis, projection);
                setupEvolutionUI(analysis);
                updateMarketCharts('GLOBAL');
            } else {
                showToast("Sua carteira está vazia. Adicione ativos.", "success");
            }
        } catch (err) {
            console.error("ERRO NO LOAD:", err);
            showToast("Erro ao conectar com o servidor.");
        } finally {
            hideLoader();
        }
    };

    // --- INTERFACE (KPIs e TABELA) ---

    function updateKPIs(netWorth, analysis) {
        document.getElementById('total-net-worth').innerText =
            new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(netWorth.total_net_worth);

        document.getElementById('javer-balance-info').innerText =
            `Saldo Banco: R$ ${netWorth.javer_account_balance.toLocaleString('pt-BR')}`;

        document.getElementById('usd-rate').innerText = `R$ ${netWorth.usd_rate.toFixed(2)}`;

        const yieldPct = analysis.portfolio_summary.global_yield_pct;
        const yieldElem = document.getElementById('global-yield');
        yieldElem.innerText = `${yieldPct.toFixed(2)}%`;
        yieldElem.className = yieldPct >= 0 ? 'yield-positive' : 'yield-negative';

        document.getElementById('global-profit-brl').innerText =
            `R$ ${analysis.portfolio_summary.total_profit_loss.toLocaleString('pt-BR')}`;

        const highlightsDiv = document.getElementById('highlights-content');
        highlightsDiv.innerHTML = `
            <div class="highlight-item">
                <small>Melhor Ativo</small>
                <p style="color: #059669"><strong>${analysis.highlights.best_performer.ticker}</strong> (+R$ ${analysis.highlights.best_performer.profit.toFixed(2)})</p>
            </div>
            <div class="highlight-item">
                <small>Pior Ativo</small>
                <p style="color: #ea580c"><strong>${analysis.highlights.worst_performer.ticker}</strong> (R$ ${analysis.highlights.worst_performer.profit.toFixed(2)})</p>
            </div>
        `;
    }

    function renderInventoryTable(investments, analysis) {
        const tbody = document.getElementById('inventory-table-body');
        const portfolioItems = analysis.portfolio_summary.portfolio_items;
        const activeInvestments = investments.filter(inv => inv.is_active === true);
        tbody.innerHTML = activeInvestments.map(inv => {
            const summaryItem = portfolioItems.find(i => i.ticker === inv.asset.ticker && i.current_value > 0);
            const roi = summaryItem ? summaryItem.roi_pct : 0;
            let pPrice = parseFloat(inv.purchase_price);
            let cPrice = parseFloat(inv.asset.current_price);
            if (inv.asset.currency === 'USD') {
                cPrice = cPrice * globalUsdRate;
            }

            return `
        <tr>
            <td>
                <div style="display:flex; align-items:center; gap:10px">
                    <div class="asset-icon">${inv.asset.ticker[0]}</div>
                    <div><strong>${inv.asset.ticker}</strong><br><small>${inv.asset.name}</small></div>
                </div>
            </td>
            <td><span class="badge">${inv.asset.currency === 'USD' ? 'USD ➔ BRL' : 'BRL'}</span></td>
            <td>${parseFloat(inv.quantity).toFixed(8)}</td>
            <td>R$ ${pPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
            <td>R$ ${cPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
            <td><span class="roi-badge ${roi >= 0 ? 'positive' : 'negative'}">${roi.toFixed(2)}%</span></td>
            <td style="display: flex; gap: 5px;">
                <button class="btn-eye" title="Detalhes" onclick="viewDetails('${inv.id}')"><i class="fas fa-search-plus"></i></button>
                <button class="btn-eye" title="Vender" style="background: #fee2e2; color: #ef4444; border-radius: 20%;" onclick="openSellModal('${inv.id}', '${inv.asset.ticker}', ${inv.quantity})">
                    <i class="fas fa-hand-holding-usd"></i>
                </button>
            </td>
        </tr>
    `;
        }).join('');

        document.getElementById('assets-count').innerText = `${activeInvestments.length} ativos na carteira`;
    }

    // --- BUSCA E TRENDING ---
    let searchTimeout;
    window.handleSearch = async (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        const resultsDiv = document.getElementById('search-results');

        if (query.length < 2) {
            resultsDiv.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(async () => {
            try {
                const res = await fetch(`${API}/assets/search/name/${query}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const data = await res.json();

                if (data.length > 0) {
                    resultsDiv.style.display = 'block';
                    resultsDiv.innerHTML = data.map(asset => `
                        <div class="search-result-item" onclick="quickTrade('${asset.ticker}')">
                            <div class="asset-info">
                                <b>${asset.ticker}</b><br>
                                <span>${asset.name}</span>
                            </div>
                            <div class="asset-price">
                                R$ ${parseFloat(asset.current_price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                            </div>
                        </div>
                    `).join('');
                }
            } catch (err) { console.error(err); }
        }, 500);
    };

    window.quickTrade = async (ticker) => {
        document.getElementById('search-results').style.display = 'none';
        showLoader();
        try {
            const res = await fetch(`${API}/assets/search/ticker/${ticker}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            window.prepareTrade(data.ticker, data.current_price);
        } catch (err) { showToast("Erro ao buscar ativo."); }
        finally { hideLoader(); }
    };

    function renderTrending(trending) {
        const container = document.getElementById('trending-list');
        const list = (trending && trending.length > 0) ? trending : [{ ticker: 'AAPL' }, { ticker: 'PETR4.SA' }, { ticker: 'BTC-USD' }];
        container.innerHTML = list.map(t => `<span class="trend-badge" onclick="quickTrade('${t.ticker}')">${t.ticker}</span>`).join('');
    }

    // --- GRÁFICOS  ---

    const renderCharts = (analysis, projection) => {
        renderAllocationChart(analysis.charts);
        renderPerformanceChart(analysis, analysis.charts);
        renderProjectionChart(projection);
    };

    function renderAllocationChart(chartData) {
        const ctxPie = document.getElementById('chart-allocation').getContext('2d');
        const valuesAlloc = chartData.allocation_by_type.map(item => item.current_value_brl);
        const labelsAlloc = chartData.allocation_by_type.map(item => item.type);
        const total = valuesAlloc.reduce((a, b) => a + b, 0);

        if (chartAlloc) chartAlloc.destroy();
        chartAlloc = new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: labelsAlloc,
                datasets: [{
                    data: valuesAlloc,
                    backgroundColor: ['#0a173d', '#f3681e', '#a6cfc0', '#fce210'],
                    borderWidth: 0, cutout: '75%'
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'right', labels: { usePointStyle: true, font: { weight: '600' } } }
                }
            }
        });
    }

    function renderPerformanceChart(analysis, chartData) {
        const ctxBar = document.getElementById('chart-performance').getContext('2d');
        const activeTickers = [...new Set(analysis.portfolio_summary.portfolio_items.filter(item => item.current_value > 0).map(item => item.ticker))];
        const perfData = chartData.profit_loss_by_ticker.filter(item => activeTickers.includes(item.ticker));
        if (perfData.length > 0) {
            const labelsPerf = perfData.map(item => item.ticker);
            const valuesPerf = perfData.map(item => item.profit_loss_brl);
            const gradLucro = ctxBar.createLinearGradient(0, 0, 0, 400);
            gradLucro.addColorStop(0, '#2dd4bf'); gradLucro.addColorStop(1, '#059669');
            const gradPrej = ctxBar.createLinearGradient(0, 0, 0, 400);
            gradPrej.addColorStop(0, '#fb923c'); gradPrej.addColorStop(1, '#ea580c');
            if (chartPerf) chartPerf.destroy();
            chartPerf = new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: labelsPerf,
                    datasets: [{
                        data: valuesPerf,
                        backgroundColor: valuesPerf.map(v => v >= 0 ? gradLucro : gradPrej),
                        borderRadius: 8, borderSkipped: false, barPercentage: 0.5
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1e293b',
                            padding: 12,
                            callbacks: {
                                label: (ctx) => ` Lucro/Prejuízo: R$ ${ctx.raw.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                            }
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#64748b', font: { weight: '600' } } },
                        y: { beginAtZero: true, grid: { color: 'rgba(226, 232, 240, 0.6)', drawBorder: false } }
                    }
                }
            });
        }
    }

    const renderEvolutionChart = (marketData) => {
        const ctx = document.getElementById('chart-evolution').getContext('2d');
        const historyLabels = marketData.chart_data.map(d => d.date);
        const historyPrices = marketData.chart_data.map(d => d.price);

        if (chartEvol) chartEvol.destroy();

        chartEvol = new Chart(ctx, {
            type: 'line',
            data: {
                labels: historyLabels,
                datasets: [{
                    type: 'line', label: 'Preço de Mercado', data: historyPrices,
                    borderColor: '#a6cfc0', backgroundColor: 'rgba(166, 207, 192, 0.1)',
                    fill: true, tension: 0.4, pointRadius: 0, pointHitRadius: 20, borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#1e293b',
                        padding: 12,
                        titleFont: { size: 12, family: 'Inter' },
                        bodyFont: { size: 14, family: 'Inter', weight: 'bold' },
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                let value = context.parsed.y;
                                return ` Preço: R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', maxTicksLimit: 12 }
                    },
                    y: {
                        grid: { color: 'rgba(0,0,0,0.03)' },
                        ticks: {
                            color: '#94a3b8',
                            callback: (value) => 'R$ ' + value.toLocaleString('pt-BR')
                        }
                    }
                }
            }
        });
    }

    function renderBenchmarkChart(marketData) {
        const ctx = document.getElementById('chart-benchmark').getContext('2d');
        const bench = marketData.market_benchmark_comparison;
        const myY = typeof bench.portfolio_yield === 'string' ? parseFloat(bench.portfolio_yield.replace('%', '')) : bench.portfolio_yield;
        const mkY = typeof bench.market_yield === 'string' ? parseFloat(bench.market_yield.replace('%', '')) : bench.market_yield;
        const label = marketData.asset_info.ticker;

        if (chartBench) chartBench.destroy();
        chartBench = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [label, 'Ibovespa'],
                datasets: [{
                    data: [myY, mkY],
                    backgroundColor: [label === 'Minha Carteira' ? '#f3681e' : '#a6cfc0', '#0a173d'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: { legend: { display: false } },
                scales: { y: { ticks: { callback: v => v + '%' } } }
            }
        });
    }

    function renderProjectionChart(projection) {
        const ctxProj = document.getElementById('chart-projection').getContext('2d');
        document.getElementById('projection-info').innerText = `Taxa: ${projection.annual_rate} (${projection.profile})`;

        if (chartProj) chartProj.destroy();
        chartProj = new Chart(ctxProj, {
            type: 'bar',
            data: {
                labels: ['Hoje', '12 Meses'],
                datasets: [{
                    data: [projection.initial_assets, projection.projected_value],
                    backgroundColor: ['#0a173d', '#2dd4bf'],
                    borderRadius: 10
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: { legend: { display: false } },
                scales: { y: { ticks: { callback: v => 'R$ ' + v.toLocaleString('pt-BR') } } }
            }
        });
    }

    // --- LOGICA DE MERCADO E BENCHMARK ---
    const setupEvolutionUI = (analysis) => {
        const select = document.getElementById('ticker-evolution-select');
        const tickers = [...new Set(analysis.portfolio_summary.portfolio_items.filter(i => i.current_value > 0).map(i => i.ticker))];
        let options = `<option value="GLOBAL">Minha Carteira (Total)</option>`;
        options += tickers.map(t => `<option value="${t}">${t}</option>`).join('');
        select.innerHTML = options;
        select.onchange = () => updateMarketCharts(select.value);
        document.querySelectorAll('.btn-period').forEach(btn => {
            btn.onclick = (e) => {
                document.querySelectorAll('.btn-period').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                currentPeriod = e.target.dataset.period;
                updateMarketCharts(select.value);
            };
        });
    };

    async function updateMarketCharts(ticker) {
        if (!ticker) return;
        showLoader();
        try {
            const tickerToFetch = (ticker === 'GLOBAL') ? 'PETR4.SA' : ticker;
            const res = await fetch(`${API}/analytics/market/comparison/${tickerToFetch}?period=${currentPeriod}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();

            if (ticker === 'GLOBAL') {
                const globalYield = lastAnalysisData.portfolio_summary.global_yield_pct;
                const globalBench = {
                    asset_info: { ticker: "Minha Carteira" },
                    market_benchmark_comparison: {
                        portfolio_yield: globalYield,
                        market_yield: data.market_benchmark_comparison.market_yield
                    }
                };
                renderBenchmarkChart(globalBench);
                document.getElementById('chart-evolution').style.opacity = "0.2";
            } else {
                document.getElementById('chart-evolution').style.opacity = "1";
                renderEvolutionChart(data);
                renderBenchmarkChart(data);
            }
        } catch (err) { console.error(err); }
        finally { hideLoader(); }
    }

    // --- MODAIS E OPERAÇÕES (COMPRA/VENDA/DETALHES) ---

    window.openModal = (id) => document.getElementById(id).style.display = 'flex';
    window.closeModal = (id) => document.getElementById(id).style.display = 'none';
    window.viewDetails = async (id) => {
        const detailsDiv = document.getElementById('details-content');
        detailsDiv.innerHTML = `
        <div style="display:flex; flex-direction:column; align-items:center; padding:30px; gap:15px;">
            <div class="loader-mini"></div>
            <p style="color: #64748b; font-size: 14px; font-weight: 500;">Buscando dados no Yahoo Finance...</p>
        </div>`;
        window.openModal('modal-details');

        try {
            const token = localStorage.getItem('access_token');
            const API = "http://127.0.0.1:8003";
            const res = await fetch(`${API}/investments/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!res.ok) throw new Error("Não foi possível localizar este investimento.");
            const data = await res.json();
            const isUsd = data.asset.currency === 'USD';
            const qty = parseFloat(data.quantity) || 0;
            let unitPurchasePrice = parseFloat(data.purchase_price) || 0;
            let unitCurrentPrice = parseFloat(data.asset.current_price) || 0;
            if (isUsd) {
                unitCurrentPrice = unitCurrentPrice * exchangeRate;
            }
            const totalValue = data.current_value_brl ? parseFloat(data.current_value_brl) : (qty * unitCurrentPrice);
            detailsDiv.innerHTML = `
            <div class="details-grid">
                <div class="detail-item">
                    <label>Ticker</label>
                    <p><strong>${data.asset.ticker}</strong></p>
                </div>
                <div class="detail-item">
                    <label>Nome do Ativo</label>
                    <p>${data.asset.name}</p>
                </div>
                <div class="detail-item">
                    <label>Quantidade</label>
                    <p>${qty.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 8 })}</p>
                </div>
                <div class="detail-item">
                    <label>Moeda Base</label>
                    <p>${data.asset.currency} ${isUsd ? '🇺🇸' : '🇧🇷'}</p>
                </div>
                <div class="detail-item">
                    <label>Compra (Unitário em BRL)</label>
                    <p>R$ ${unitPurchasePrice.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                </div>
                <div class="detail-item">
                    <label>Mercado (Unitário em BRL)</label>
                    <p>R$ ${unitCurrentPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                </div>
                
                <div class="detail-item highlight-total" style="grid-column: span 2;">
                    <label>Patrimônio Total Atualizado (BRL)</label>
                    <p><strong>R$ ${totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong></p>
                </div>

                <div class="detail-item">
                    <label>Data da Aplicação</label>
                    <p>${new Date(data.application_date).toLocaleDateString('pt-BR')}</p>
                </div>

                ${isUsd ? `
                <div class="conversion-info" style="grid-column: span 2;">
                    <i class="fas fa-info-circle"></i>
                    Ativo dolarizado. Conversão realizada automaticamente com a cotação atual de <strong>R$ ${exchangeRate.toFixed(2)}</strong>.
                </div>
                ` : ''}
            </div>

            <style>
                .details-grid { 
                    display: grid; 
                    grid-template-columns: 1fr 1fr; 
                    gap: 15px; 
                    margin-top: 10px; 
                }
                .detail-item label { 
                    display: block;
                    font-size: 10px; 
                    color: #64748b; 
                    text-transform: uppercase; 
                    font-weight: 800; 
                    margin-bottom: 2px;
                    letter-spacing: 0.5px;
                }
                .detail-item p { 
                    font-size: 15px; 
                    color: #0a173d; 
                    margin: 0;
                    font-weight: 500;
                }
                .highlight-total {
                    background: #f8fafc;
                    padding: 15px;
                    border-radius: 12px;
                    border-left: 5px solid #f3681e;
                    margin-top: 10px;
                }
                .highlight-total p {
                    font-size: 22px;
                    color: #0a173d;
                }
                .conversion-info {
                    margin-top: 15px;
                    background: #fffbeb;
                    color: #92400e;
                    padding: 12px;
                    border-radius: 8px;
                    font-size: 12px;
                    border: 1px solid #fef3c7;
                    line-height: 1.4;
                }
                .loader-mini {
                    width: 25px;
                    height: 25px;
                    border: 3px solid #f3f3f3;
                    border-top: 3px solid #f3681e;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>`;

        } catch (err) {
            console.error("Erro ao carregar detalhes:", err);
            detailsDiv.innerHTML = `
            <div style="text-align:center; padding: 20px;">
                <i class="fas fa-times-circle" style="font-size: 40px; color: #ef4444; margin-bottom: 15px;"></i>
                <p style="color: #ef4444; font-weight: bold;">Erro ao carregar detalhes</p>
                <p style="font-size: 13px; color: #64748b; margin-top: 5px;">${err.message}</p>
            </div>`;
        }
    };

    window.prepareTrade = (ticker, price) => {
        document.getElementById('buy-ticker').value = ticker;
        openModal('modal-buy');
    };

    window.executeTrade = async () => {
        const ticker = document.getElementById('buy-ticker').value;
        const quantity = document.getElementById('buy-qty').value;
        showLoader();
        try {
            const res = await fetch(`${API}/investments/buy`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticker, quantity: parseFloat(quantity) })
            });
            if (res.ok) { showToast("Compra realizada!", "success"); closeModal('modal-buy'); loadAllInvestmentsData(); }
            else { const e = await res.json(); showToast(e.detail); }
        } finally { hideLoader(); }
    };

    window.openSellModal = (id, ticker, currentQty) => {
        document.getElementById('sell-investment-id').value = id;
        document.getElementById('sell-current-qty').value = currentQty;
        document.getElementById('sell-asset-info').innerHTML = `Vender <b>${ticker}</b> (Disponível: ${currentQty})`;
        openModal('modal-sell');
    };

    window.executeSell = async () => {
        const id = document.getElementById('sell-investment-id').value;
        const currentQty = parseFloat(document.getElementById('sell-current-qty').value);
        const qtyToSell = parseFloat(document.getElementById('sell-qty-input').value);
        const newTotal = currentQty - qtyToSell;

        if (newTotal < 0) return showToast("Quantidade insuficiente.");
        showLoader();
        try {
            const res = await fetch(`${API}/investments/${id}`, {
                method: 'PATCH',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ quantity: newTotal })
            });
            if (res.ok) { showToast("Venda realizada!", "success"); closeModal('modal-sell'); loadAllInvestmentsData(); }
        } finally { hideLoader(); }
    };

    loadAllInvestmentsData();
});