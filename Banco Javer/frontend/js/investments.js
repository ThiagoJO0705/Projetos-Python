document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const API = "http://127.0.0.1:8003";

    if (!token) window.location.href = 'index.html';

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
            const analysis = await walletRes.json();
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
            
        // Highlights (Destaques)
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

        tbody.innerHTML = investments.map(inv => {
            const analysisData = portfolioItems.find(i => i.ticker === inv.asset.ticker) || {};
            const roi = analysisData.roi_pct || 0;
            return `
                <tr>
                    <td>
                        <div style="display:flex; align-items:center; gap:10px">
                            <div class="asset-icon">${inv.asset.ticker[0]}</div>
                            <div><strong>${inv.asset.ticker}</strong><br><small>${inv.asset.name}</small></div>
                        </div>
                    </td>
                    <td><span class="type-badge">${inv.asset.type}</span></td>
                    <td>${parseFloat(inv.quantity).toFixed(2)}</td>
                    <td>R$ ${parseFloat(inv.purchase_price).toFixed(2)}</td>
                    <td>R$ ${parseFloat(inv.current_value_brl).toFixed(2)}</td>
                    <td><span class="roi-badge ${roi >= 0 ? 'positive' : 'negative'}">${roi.toFixed(2)}%</span></td>
                    <td>
                        <button class="btn-eye" onclick="viewDetails('${inv.id}')"><i class="fas fa-search-plus"></i></button>
                    </td>
                </tr>
            `;
        }).join('');
        
        document.getElementById('assets-count').innerText = `${investments.length} ativos na carteira`;
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

    // --- FUNÇÕES DE GRÁFICOS (Suas originais preservadas) ---

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
                    plugins: { legend: { display: false } },
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
                    fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94a3b8', maxTicksLimit: 8 } },
                    y: { grid: { color: 'rgba(0,0,0,0.03)' }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    };

    const renderBenchmarkChart = (marketData) => {
        const ctx = document.getElementById('chart-benchmark').getContext('2d');
        const bench = marketData.market_benchmark_comparison;
        const myYield = parseFloat(bench.portfolio_yield.replace('%', ''));
        const marketYield = parseFloat(bench.market_yield.replace('%', ''));

        if (chartBench) chartBench.destroy();
        chartBench = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [marketData.asset_info.ticker, 'Ibovespa'],
                datasets: [{
                    data: [myYield, marketYield],
                    backgroundColor: ['#a6cfc0', '#0a173d'],
                    borderRadius: 8, barPercentage: 0.5
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { ticks: { callback: (v) => v + '%' } } }
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
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    // --- CONTROLES DE EVENTOS ---

    const setupEvolutionUI = (analysis) => {
        const select = document.getElementById('ticker-evolution-select');
        const activeTickers = [...new Set(analysis.portfolio_summary.portfolio_items
            .filter(item => item.current_value > 0).map(item => item.ticker))];

        select.innerHTML = activeTickers.map(t => `<option value="${t}">${t}</option>`).join('');
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
            const res = await fetch(`${API}/analytics/market/comparison/${ticker}?period=${currentPeriod}`, { 
                headers: { 'Authorization': `Bearer ${token}` } 
            });
            const data = await res.json();
            renderEvolutionChart(data);
            renderBenchmarkChart(data);
        } catch (err) {
            showToast("Erro ao carregar dados de mercado.");
        } finally {
            hideLoader();
        }
    }

    // --- MODAIS E TRANSAÇÕES (ORDENS) ---

    window.openModal = (id) => document.getElementById(id).style.display = 'flex';
    window.closeModal = (id) => document.getElementById(id).style.display = 'none';

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

    loadAllInvestmentsData();
});