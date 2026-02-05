document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const API = "http://127.0.0.1:8003";

    if (!token) window.location.href = 'index.html';

    let globalUsdRate = 1;
    let lastAnalysisData = null

    // Variáveis de controle dos gráficos (Preservadas)
    let chartAlloc = null;
    let chartPerf = null;
    let chartEvol = null;
    let chartBench = null;
    let chartProj = null;
    let currentPeriod = '1y';

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

            updateKPIs(netWorth, analysis);
            renderTrending(trending);
            renderInventoryTable(myInvestments, analysis);

            if (walletRes.ok && analysis.charts) {
                renderCharts(analysis, projection, null, myInvestments);

                const activeTickers = analysis.portfolio_summary.portfolio_items
                    .filter(item => item.current_value > 0);

                if (activeTickers.length > 0) {
                    setupEvolutionUI(analysis, myInvestments);
                    updateMarketCharts(activeTickers[0].ticker);
                }
            } else {
                showToast("Sua carteira está vazia. Adicione ativos.", "success");
            }
        } catch (err) {
            console.error("ERRO NO LOAD:", err);
            showToast("Erro ao conectar com o Gateway de Investimentos.");
        } finally {
            hideLoader();
        }
    };

    // --- FUNÇÕES DE INTERFACE (UI) ---

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
                <small>Melhor Performance</small>
                <p style="color: #059669"><strong>${analysis.highlights.best_performer.ticker}</strong> (+R$ ${analysis.highlights.best_performer.profit.toFixed(2)})</p>
            </div>
            <div class="highlight-item">
                <small>Maior Queda</small>
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

    function renderTrending(trending) {
        const container = document.getElementById('trending-list');
        if (!trending || trending.length === 0) {
            container.innerHTML = `<span class="trend-item">PETR4.SA</span><span class="trend-item">VALE3.SA</span><span class="trend-item">BTC-USD</span>`;
            return;
        }
        container.innerHTML = trending.map(t => `<span class="trend-item" onclick="setSearch('${t.ticker}')">${t.ticker}</span>`).join('');
    }

    // --- LÓGICA DE BUSCA (Debounce) ---
    let searchTimeout;
    window.handleSearch = async (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.toUpperCase();
        const resultsDiv = document.getElementById('search-results');

        if (query.length < 2) {
            resultsDiv.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(async () => {
            try {
                const res = await fetch(`${API}/assets/search/ticker/${query}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const data = await res.json();

                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `
                    <div class="search-item" onclick="prepareTrade('${data.ticker}', ${data.current_price})">
                        <strong>${data.ticker}</strong> - ${data.name} 
                        <span style="float:right; color:#059669">R$ ${data.current_price}</span>
                    </div>
                `;
            } catch (err) {
                resultsDiv.innerHTML = `<div class="search-item">Ativo não encontrado</div>`;
            }
        }, 600);
    };

    // --- GRÁFICOS ---

    const renderCharts = (analysis, projection, marketData, myInvestments) => {
        renderAllocationChart(analysis.charts);
        renderPerformanceChart(analysis, analysis.charts);
        renderProjectionChart(projection);
    };

    function renderAllocationChart(chartData) {
        const ctxPie = document.getElementById('chart-allocation').getContext('2d');
        const allocationArray = chartData.allocation_by_type;
        const labelsAlloc = allocationArray.map(item => item.type);
        const valuesAlloc = allocationArray.map(item => item.current_value_brl);
        const totalValue = valuesAlloc.reduce((a, b) => a + b, 0);

        function createGradient(ctx, color1, color2) {
            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, color1);
            gradient.addColorStop(1, color2);
            return gradient;
        }

        const gradientColors = [
            createGradient(ctxPie, '#0a173d', '#1e3a8a'),
            createGradient(ctxPie, '#f3681e', '#ff8c00'),
            createGradient(ctxPie, '#a6cfc0', '#2dd4bf'),
            createGradient(ctxPie, '#fce210', '#ffd700'),
        ];

        if (chartAlloc) chartAlloc.destroy();
        chartAlloc = new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: labelsAlloc,
                datasets: [{
                    data: valuesAlloc,
                    backgroundColor: gradientColors,
                    hoverOffset: 20, borderWidth: 0, borderRadius: 2, spacing: 5
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '75%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#444', usePointStyle: true, font: { size: 12, weight: '600' },
                            generateLabels: (chart) => chart.data.labels.map((label, i) => ({
                                text: `${label} (${((valuesAlloc[i] / totalValue) * 100).toFixed(0)}%)`,
                                fillStyle: gradientColors[i], strokeStyle: gradientColors[i], lineWidth: 0, index: i
                            }))
                        }
                    }
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
    };

    const renderBenchmarkChart = (marketData) => {
        const ctx = document.getElementById('chart-benchmark').getContext('2d');
        const bench = marketData.market_benchmark_comparison;
        const myYield = typeof bench.portfolio_yield === 'string' ? parseFloat(bench.portfolio_yield.replace('%', '')) : bench.portfolio_yield;
        const marketYield = typeof bench.market_yield === 'string' ? parseFloat(bench.market_yield.replace('%', '')) : bench.market_yield;
        const labelAtivo = marketData.asset_info.ticker;
        if (chartBench) chartBench.destroy();
        chartBench = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [labelAtivo, 'Ibovespa'],
                datasets: [{
                    data: [myYield, marketYield],
                    backgroundColor: [
                        labelAtivo === 'Minha Carteira' ? '#f3681e' : '#a6cfc0',
                        '#0a173d'
                    ],
                    borderRadius: 8,
                    barPercentage: 0.5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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
                            label: (ctx) => ` Rendimento: ${ctx.raw.toFixed(2)}%`
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: { callback: (v) => v + '%' }
                    }
                }
            }
        });
    };

    function renderProjectionChart(projection) {
        const ctxProj = document.getElementById('chart-projection').getContext('2d');
        document.getElementById('projection-info').innerText = `Taxa: ${projection.annual_rate} (Perfil ${projection.profile})`;

        if (chartProj) chartProj.destroy();
        chartProj = new Chart(ctxProj, {
            type: 'bar',
            data: {
                labels: ['Hoje', '12 Meses'],
                datasets: [{
                    data: [projection.initial_assets, projection.projected_value],
                    backgroundColor: ['#0a173d', '#2dd4bf'],
                    borderRadius: 10, barPercentage: 0.6
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
                            label: (ctx) => ` Valor: R$ ${ctx.raw.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { callback: (v) => 'R$ ' + v.toLocaleString('pt-BR') }
                    }
                }
            }
        });
    }

    const setupEvolutionUI = (analysis) => {
        const select = document.getElementById('ticker-evolution-select');
        const activeTickers = [...new Set(analysis.portfolio_summary.portfolio_items
            .filter(item => item.current_value > 0).map(item => item.ticker))];

        // Adiciona "Minha Carteira" como primeira opção e depois os tickers
        let options = `<option value="GLOBAL">Minha Carteira (Total)</option>`;
        options += activeTickers.map(t => `<option value="${t}">${t}</option>`).join('');

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
            const periodToFetch = (ticker === 'GLOBAL') ? '1y' : currentPeriod;
            const res = await fetch(`${API}/analytics/market/comparison/${tickerToFetch}?period=${periodToFetch}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            if (ticker === 'GLOBAL') {
                const globalYield = lastAnalysisData.portfolio_summary.global_yield_pct;
                const globalBenchmark = {
                    asset_info: { ticker: "Minha Carteira" },
                    market_benchmark_comparison: {
                        portfolio_yield: `${globalYield.toFixed(2)}%`,
                        market_yield: data.market_benchmark_comparison.market_yield // Mantém o Ibov do período
                    }
                };
                renderBenchmarkChart(globalBenchmark)
                document.getElementById('chart-evolution').style.opacity = "0.3";
            } else {
                document.getElementById('chart-evolution').style.opacity = "1";
                renderEvolutionChart(data);
                renderBenchmarkChart(data);
            }
        } catch (err) {
            showToast("Erro ao carregar dados de mercado.");
        } finally {
            hideLoader();
        }
    }

    // --- MODAIS ---

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
            const exchangeRate = (typeof globalUsdRate !== 'undefined' && globalUsdRate > 0) ? globalUsdRate : 1;
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
        document.getElementById('search-results').style.display = 'none';
        openModal('modal-buy');
    };

    window.executeTrade = async (type) => {
        const ticker = document.getElementById('buy-ticker').value;
        const quantity = document.getElementById('buy-qty').value;

        if (!ticker || !quantity) return showToast("Preencha todos os campos");

        showLoader();
        try {
            const res = await fetch(`${API}/investments/buy`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ticker, quantity: parseFloat(quantity) })
            });

            if (res.ok) {
                showToast("Ordem executada com sucesso!", "success");
                closeModal('modal-buy');
                loadAllInvestmentsData();
            } else {
                const err = await res.json();
                showToast(err.detail || "Erro na transação");
            }
        } catch (err) {
            showToast("Erro de conexão");
        } finally {
            hideLoader();
        }
    };

    // --- LÓGICA DE VENDA ---

    window.openSellModal = (id, ticker, currentQty) => {
        document.getElementById('sell-investment-id').value = id;
        document.getElementById('sell-current-qty').value = currentQty;
        document.getElementById('sell-qty-input').value = "";

        document.getElementById('sell-asset-info').innerHTML = `
            <p style="font-size: 12px; color: #64748b; margin-bottom: 5px;">Ativo Selecionado</p>
            <p><strong>${ticker}</strong></p>
            <p style="font-size: 13px;">Quantidade em Carteira: <strong>${parseFloat(currentQty).toFixed(8)}</strong></p>
        `;

        window.openModal('modal-sell');
    };

    window.executeSell = async () => {
        const id = document.getElementById('sell-investment-id').value;
        const currentQty = parseFloat(document.getElementById('sell-current-qty').value);
        const qtyToSell = parseFloat(document.getElementById('sell-qty-input').value);

        if (isNaN(qtyToSell) || qtyToSell <= 0) {
            return showToast("Informe uma quantidade válida para venda.");
        }

        if (qtyToSell > currentQty) {
            return showToast("Você não pode vender mais do que possui.");
        }

        const newTotalQuantity = currentQty - qtyToSell;

        showLoader();
        try {
            const res = await fetch(`${API}/investments/${id}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quantity: newTotalQuantity })
            });

            if (res.ok) {
                showToast(qtyToSell === currentQty ? "Ativo totalmente vendido!" : "Venda parcial realizada!", "success");
                window.closeModal('modal-sell');
                loadAllInvestmentsData();
            } else {
                const err = await res.json();
                showToast(err.detail || "Erro ao processar venda.");
            }
        } catch (err) {
            console.error("ERRO NA VENDA:", err);
            showToast("Erro de conexão com o servidor.");
        } finally {
            hideLoader();
        }
    };

    loadAllInvestmentsData();
});