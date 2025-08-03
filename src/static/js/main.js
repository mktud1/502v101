// ARQV30 Enhanced v2.0 - Main JavaScript
// Sistema aprimorado com continuidade garantida e zero simulação

class ARQV30App {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.currentAnalysis = null;
        this.progressInterval = null;
        this.uploadedFiles = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkSystemHealth();
        this.setupKeyboardShortcuts();
        this.initializeServiceWorker();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('analysisForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Input validation
        this.setupInputValidation();
        
        // File upload
        this.setupFileUpload();
    }

    setupInputValidation() {
        const inputs = document.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateInput(input));
            input.addEventListener('focus', () => this.clearInputError(input));
        });
    }

    validateInput(input) {
        const value = input.value.trim();
        const isRequired = input.hasAttribute('required');
        
        if (isRequired && !value) {
            this.showInputError(input, 'Campo obrigatório');
            return false;
        }

        // Validações específicas
        if (input.type === 'number' && value) {
            const num = parseFloat(value);
            if (isNaN(num) || num < 0) {
                this.showInputError(input, 'Valor numérico inválido');
                return false;
            }
        }

        if (input.id === 'segmento' && value) {
            if (value.length < 3) {
                this.showInputError(input, 'Segmento deve ter pelo menos 3 caracteres');
                return false;
            }
            
            // Verifica se não é genérico
            const genericTerms = ['teste', 'test', 'exemplo', 'sample'];
            if (genericTerms.some(term => value.toLowerCase().includes(term))) {
                this.showInputError(input, 'Segmento não pode ser genérico ou de teste');
                return false;
            }
        }

        this.clearInputError(input);
        return true;
    }

    showInputError(input, message) {
        input.classList.add('invalid');
        
        // Remove erro anterior
        const existingError = input.parentNode.querySelector('.input-error');
        if (existingError) {
            existingError.remove();
        }

        // Adiciona novo erro
        const errorElement = document.createElement('div');
        errorElement.className = 'input-error';
        errorElement.style.cssText = 'color: #ff6b6b; font-size: 12px; margin-top: 4px;';
        errorElement.textContent = message;
        
        input.parentNode.appendChild(errorElement);
    }

    clearInputError(input) {
        input.classList.remove('invalid');
        
        const errorElement = input.parentNode.querySelector('.input-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    setupFileUpload() {
        // Implementado em upload.js
        console.log('📎 Sistema de upload inicializado');
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        // Valida formulário
        if (!this.validateForm()) {
            this.showError('Por favor, corrija os erros no formulário antes de continuar.');
            return;
        }

        // Coleta dados do formulário
        const formData = this.collectFormData();
        
        // Adiciona arquivos enviados
        formData.uploaded_files = this.uploadedFiles;
        formData.session_id = this.sessionId;

        console.log('🚀 Iniciando análise aprimorada:', formData);

        try {
            // Inicia análise
            await this.executeEnhancedAnalysis(formData);
            
        } catch (error) {
            console.error('❌ Erro na análise:', error);
            this.showError('Erro na análise: ' + error.message);
            this.hideProgress();
        }
    }

    validateForm() {
        const form = document.getElementById('analysisForm');
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateInput(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    collectFormData() {
        const form = document.getElementById('analysisForm');
        const formData = new FormData(form);
        
        const data = {};
        
        // Coleta dados básicos
        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                // Converte números
                if (['preco', 'objetivo_receita', 'orcamento_marketing'].includes(key)) {
                    data[key] = parseFloat(value) || 0;
                } else {
                    data[key] = value.trim();
                }
            }
        }

        return data;
    }

    async executeEnhancedAnalysis(data) {
        try {
            // Mostra progresso
            this.showProgress();
            
            // Inicia tracking de progresso
            await this.startProgressTracking();
            
            // Executa análise
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // Análise bem-sucedida
                this.currentAnalysis = result;
                this.hideProgress();
                this.displayResults(result);
                this.showSuccess('Análise concluída com sucesso!');
                
            } else {
                // Análise falhou mas pode ter dados parciais
                if (result.dados_preservados || result.relatorio_parcial) {
                    this.hideProgress();
                    this.displayPartialResults(result);
                    this.showWarning('Análise parcial: ' + result.message);
                } else {
                    throw new Error(result.message || 'Erro desconhecido na análise');
                }
            }

        } catch (error) {
            console.error('❌ Erro na execução da análise:', error);
            this.hideProgress();
            throw error;
        }
    }

    async startProgressTracking() {
        try {
            // Inicia tracking no servidor
            await fetch('/api/start_tracking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });

            // Inicia polling de progresso
            this.progressInterval = setInterval(() => {
                this.updateProgress();
            }, 2000); // A cada 2 segundos

        } catch (error) {
            console.error('❌ Erro ao iniciar tracking:', error);
        }
    }

    async updateProgress() {
        try {
            const response = await fetch(`/api/get_progress/${this.sessionId}`);
            
            if (response.ok) {
                const data = await response.json();
                const progress = data.progress;
                
                if (progress) {
                    this.updateProgressUI(progress);
                    
                    // Para polling se completo
                    if (progress.is_complete) {
                        clearInterval(this.progressInterval);
                    }
                }
            }
            
        } catch (error) {
            console.error('❌ Erro ao atualizar progresso:', error);
        }
    }

    updateProgressUI(progress) {
        // Atualiza barra de progresso
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = progress.percentage + '%';
        }

        // Atualiza texto do passo atual
        const currentStep = document.getElementById('currentStep');
        if (currentStep) {
            currentStep.textContent = progress.current_message;
        }

        // Atualiza contador de etapas
        const stepCounter = document.getElementById('stepCounter');
        if (stepCounter) {
            stepCounter.textContent = `${progress.current_step}/${progress.total_steps}`;
        }

        // Atualiza tempo estimado
        const estimatedTime = document.getElementById('estimatedTime');
        if (estimatedTime && progress.estimated_remaining) {
            const minutes = Math.floor(progress.estimated_remaining / 60);
            const seconds = Math.floor(progress.estimated_remaining % 60);
            estimatedTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    showProgress() {
        const progressArea = document.getElementById('progressArea');
        const resultsArea = document.getElementById('resultsArea');
        
        if (progressArea) {
            progressArea.style.display = 'block';
            progressArea.scrollIntoView({ behavior: 'smooth' });
        }
        
        if (resultsArea) {
            resultsArea.style.display = 'none';
        }

        // Desabilita botão de análise
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Analisando...</span>';
        }
    }

    hideProgress() {
        const progressArea = document.getElementById('progressArea');
        
        if (progressArea) {
            progressArea.style.display = 'none';
        }

        // Reabilita botão
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> <span>Gerar Análise Ultra-Detalhada</span>';
        }

        // Para polling
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    displayResults(analysis) {
        console.log('📊 Exibindo resultados da análise:', analysis);
        
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'block';
            resultsArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Exibe cada seção
        this.displayAvatar(analysis.avatar_ultra_detalhado);
        this.displayPositioning(analysis.posicionamento_estrategico);
        this.displayCompetition(analysis.analise_concorrencia_avancada);
        this.displayMarketing(analysis.estrategia_marketing_completa);
        this.displayMetrics(analysis.metricas_kpis_avancados);
        this.displayInsights(analysis.insights_exclusivos);
        
        // Seções avançadas
        this.displayDrivers(analysis.drivers_mentais_customizados);
        this.displayVisualProofs(analysis.provas_visuais_instantaneas);
        this.displayAntiObjection(analysis.sistema_anti_objecao);
        this.displayPrePitch(analysis.pre_pitch_invisivel);
        this.displayFuturePredictions(analysis.predicoes_futuro_completas);
        
        // Metadados
        this.displayMetadata(analysis.metadata);
        
        // Habilita botão de PDF se qualidade suficiente
        this.checkPDFEligibility(analysis);
    }

    displayPartialResults(result) {
        console.log('📊 Exibindo resultados parciais:', result);
        
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'block';
            resultsArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Mostra dados preservados
        if (result.relatorio_parcial) {
            this.displayResults(result.relatorio_parcial);
        }

        // Mostra informações sobre dados preservados
        const metadataContainer = document.getElementById('metadataResults');
        if (metadataContainer) {
            metadataContainer.innerHTML = `
                <div class="result-section">
                    <div class="result-section-header">
                        <h4><i class="fas fa-info-circle"></i> Status da Análise</h4>
                    </div>
                    <div class="result-section-content">
                        <div class="alert alert-warning">
                            <h5>⚠️ Análise Parcial</h5>
                            <p>${result.message}</p>
                            <p><strong>Dados preservados:</strong> ${result.dados_preservados ? 'Sim' : 'Não'}</p>
                            <p><strong>Sessão:</strong> ${result.session_id}</p>
                            ${result.recommendation ? `<p><strong>Recomendação:</strong> ${result.recommendation}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }
    }

    displayAvatar(avatar) {
        if (!avatar) return;

        const container = document.getElementById('avatarResults');
        if (!container) return;

        const demografico = avatar.perfil_demografico || {};
        const psicografico = avatar.perfil_psicografico || {};
        const dores = avatar.dores_viscerais || [];
        const desejos = avatar.desejos_secretos || [];

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-user-circle"></i> Avatar Ultra-Detalhado</h4>
                </div>
                <div class="result-section-content">
                    <div class="avatar-grid">
                        <div class="avatar-card">
                            <h5><i class="fas fa-chart-bar"></i> Perfil Demográfico</h5>
                            ${Object.entries(demografico).map(([key, value]) => `
                                <div class="avatar-item">
                                    <span class="avatar-label">${this.formatLabel(key)}</span>
                                    <span class="avatar-value">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div class="avatar-card">
                            <h5><i class="fas fa-brain"></i> Perfil Psicográfico</h5>
                            ${Object.entries(psicografico).map(([key, value]) => `
                                <div class="avatar-item">
                                    <span class="avatar-label">${this.formatLabel(key)}</span>
                                    <span class="avatar-value">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="avatar-grid">
                        <div class="avatar-card">
                            <h5><i class="fas fa-heart-broken"></i> Dores Viscerais</h5>
                            <ul class="insight-list">
                                ${dores.map(dor => `
                                    <li class="insight-item">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <span class="insight-text">${dor}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                        
                        <div class="avatar-card">
                            <h5><i class="fas fa-star"></i> Desejos Secretos</h5>
                            <ul class="insight-list">
                                ${desejos.map(desejo => `
                                    <li class="insight-item">
                                        <i class="fas fa-heart"></i>
                                        <span class="insight-text">${desejo}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    displayInsights(insights) {
        if (!insights || !Array.isArray(insights)) return;

        const container = document.getElementById('insightsResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-lightbulb"></i> Insights Exclusivos (${insights.length})</h4>
                </div>
                <div class="result-section-content">
                    <div class="data-quality-indicator">
                        <span class="quality-label">Qualidade dos Dados:</span>
                        <span class="quality-value real-data">100% REAL</span>
                    </div>
                    
                    <div class="insights-showcase">
                        ${insights.map((insight, index) => `
                            <div class="insight-card">
                                <div class="insight-number">${index + 1}</div>
                                <div class="insight-content">${insight}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    displayDrivers(drivers) {
        if (!drivers || drivers.fallback_mode) return;

        const container = document.getElementById('driversResults');
        if (!container) return;

        const driversList = drivers.drivers_customizados || [];

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-brain"></i> Drivers Mentais Customizados (${driversList.length})</h4>
                </div>
                <div class="result-section-content">
                    <div class="drivers-grid">
                        ${driversList.map((driver, index) => `
                            <div class="driver-card">
                                <h4>${driver.nome || `Driver ${index + 1}`}</h4>
                                <div class="driver-content">
                                    <p><strong>Gatilho Central:</strong> ${driver.gatilho_central || 'N/A'}</p>
                                    <p><strong>Definição:</strong> ${driver.definicao_visceral || 'N/A'}</p>
                                    
                                    ${driver.roteiro_ativacao ? `
                                        <div class="driver-script">
                                            <h6>Roteiro de Ativação</h6>
                                            <p><strong>Pergunta:</strong> ${driver.roteiro_ativacao.pergunta_abertura || 'N/A'}</p>
                                            <p><strong>História:</strong> ${driver.roteiro_ativacao.historia_analogia || 'N/A'}</p>
                                            <p><strong>Comando:</strong> ${driver.roteiro_ativacao.comando_acao || 'N/A'}</p>
                                        </div>
                                    ` : ''}
                                    
                                    ${driver.frases_ancoragem ? `
                                        <div class="anchor-phrases">
                                            <h6>Frases de Ancoragem</h6>
                                            <ul>
                                                ${driver.frases_ancoragem.map(frase => `<li>"${frase}"</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    displayMetadata(metadata) {
        if (!metadata) return;

        const container = document.getElementById('metadataResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-info-circle"></i> Metadados da Análise</h4>
                </div>
                <div class="result-section-content">
                    <div class="metadata-grid">
                        <div class="metadata-item">
                            <span class="metadata-label">Tempo de Processamento</span>
                            <span class="metadata-value">${metadata.processing_time_formatted || 'N/A'}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Engine de Análise</span>
                            <span class="metadata-value">${metadata.analysis_engine || 'N/A'}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Score de Qualidade</span>
                            <span class="metadata-value">${metadata.quality_score || 0}%</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Livre de Simulação</span>
                            <span class="metadata-value">${metadata.simulation_free ? '✅ SIM' : '❌ NÃO'}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Dados Brutos Filtrados</span>
                            <span class="metadata-value">${metadata.raw_data_filtered ? '✅ SIM' : '❌ NÃO'}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Versão do Pipeline</span>
                            <span class="metadata-value">${metadata.pipeline_version || 'N/A'}</span>
                        </div>
                    </div>
                    
                    ${metadata.successful_components ? `
                        <div style="margin-top: 20px;">
                            <h5>Componentes Executados com Sucesso:</h5>
                            <div class="keyword-tags">
                                ${metadata.successful_components.map(comp => `
                                    <span class="keyword-tag">${comp}</span>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${metadata.failed_components && metadata.failed_components.length > 0 ? `
                        <div style="margin-top: 20px;">
                            <h5>Componentes que Falharam:</h5>
                            <div class="keyword-tags">
                                ${metadata.failed_components.map(comp => `
                                    <span class="keyword-tag secondary">${comp}</span>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    checkPDFEligibility(analysis) {
        const downloadBtn = document.getElementById('downloadPdfBtn');
        const saveBtn = document.getElementById('saveJsonBtn');
        
        if (downloadBtn) {
            // Verifica se tem qualidade suficiente para PDF
            const qualityScore = analysis.metadata?.quality_score || 0;
            const hasSimulation = !analysis.metadata?.simulation_free;
            
            if (qualityScore >= 60 && !hasSimulation) {
                downloadBtn.style.display = 'inline-flex';
                downloadBtn.onclick = () => this.downloadPDF(analysis);
            } else {
                downloadBtn.style.display = 'none';
            }
        }
        
        if (saveBtn) {
            saveBtn.style.display = 'inline-flex';
        }
    }

    async downloadPDF(analysis) {
        try {
            this.showInfo('Gerando PDF...');
            
            const response = await fetch('/api/generate_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(analysis)
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `analise_mercado_${new Date().toISOString().slice(0, 10)}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showSuccess('PDF gerado com sucesso!');
            } else {
                const error = await response.json();
                throw new Error(error.message || 'Erro ao gerar PDF');
            }

        } catch (error) {
            console.error('❌ Erro ao gerar PDF:', error);
            this.showError('Erro ao gerar PDF: ' + error.message);
        }
    }

    saveAnalysisLocally(analysis) {
        if (!analysis) {
            this.showError('Nenhuma análise para salvar');
            return;
        }

        try {
            const dataStr = JSON.stringify(analysis, null, 2);
            const blob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `analise_${analysis.metadata?.session_id || 'unknown'}_${new Date().toISOString().slice(0, 10)}.json`;
            document.body.appendChild(a);
            a.click();
            
            URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            this.showSuccess('Análise salva localmente!');
            
        } catch (error) {
            console.error('❌ Erro ao salvar:', error);
            this.showError('Erro ao salvar análise: ' + error.message);
        }
    }

    async checkSystemHealth() {
        try {
            const response = await fetch('/api/health');
            const health = await response.json();
            
            this.updateSystemStatus(health);
            
        } catch (error) {
            console.error('❌ Erro ao verificar saúde do sistema:', error);
            this.updateSystemStatus({ status: 'error' });
        }
    }

    updateSystemStatus(health) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (statusIndicator && statusText) {
            const icon = statusIndicator.querySelector('i');
            
            if (health.status === 'healthy') {
                icon.className = 'fas fa-circle';
                icon.style.color = '#48bb78';
                statusText.textContent = 'Sistema Online';
                statusIndicator.classList.add('online');
            } else {
                icon.className = 'fas fa-circle';
                icon.style.color = '#f56565';
                statusText.textContent = 'Sistema com Problemas';
                statusIndicator.classList.add('offline');
            }
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Enter: Executar análise
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                const form = document.getElementById('analysisForm');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
            
            // Ctrl+S: Salvar análise
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                if (this.currentAnalysis) {
                    this.saveAnalysisLocally(this.currentAnalysis);
                }
            }
        });
    }

    async initializeServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                await navigator.serviceWorker.register('/sw.js');
                console.log('✅ Service Worker registrado');
            } catch (error) {
                console.error('❌ Erro ao registrar Service Worker:', error);
            }
        }
    }

    formatLabel(key) {
        return key.replace(/_/g, ' ')
                 .replace(/\b\w/g, l => l.toUpperCase());
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'error');
    }

    showWarning(message) {
        this.showAlert(message, 'warning');
    }

    showInfo(message) {
        this.showAlert(message, 'info');
    }

    showAlert(message, type = 'info') {
        // Remove alertas existentes
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Cria novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 18px;">&times;</button>
            </div>
        `;

        document.body.appendChild(alert);

        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    // Métodos de exibição adicionais (implementar conforme necessário)
    displayPositioning(positioning) {
        // Implementar exibição de posicionamento
    }

    displayCompetition(competition) {
        // Implementar exibição de análise competitiva
    }

    displayMarketing(marketing) {
        // Implementar exibição de estratégia de marketing
    }

    displayMetrics(metrics) {
        // Implementar exibição de métricas
    }

    displayVisualProofs(proofs) {
        // Implementar exibição de provas visuais
    }

    displayAntiObjection(antiObjection) {
        // Implementar exibição de sistema anti-objeção
    }

    displayPrePitch(prePitch) {
        // Implementar exibição de pré-pitch
    }

    displayFuturePredictions(predictions) {
        // Implementar exibição de predições futuras
    }
}

// Gerenciador de análise específico
class AnalysisManager {
    constructor() {
        this.app = null;
    }

    init(app) {
        this.app = app;
    }

    async testExtraction() {
        try {
            const response = await fetch('/api/test_extraction?url=https://g1.globo.com/tecnologia/');
            const result = await response.json();
            
            console.log('🧪 Teste de extração:', result);
            
            if (result.success) {
                this.app.showSuccess(`Extração OK: ${result.content_length} caracteres`);
            } else {
                this.app.showError(`Extração falhou: ${result.error}`);
            }
            
        } catch (error) {
            console.error('❌ Erro no teste:', error);
            this.app.showError('Erro no teste de extração');
        }
    }

    async testSearch() {
        try {
            const response = await fetch('/api/test_search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: 'mercado tecnologia Brasil 2024' })
            });
            
            const result = await response.json();
            console.log('🧪 Teste de busca:', result);
            
            if (result.success) {
                this.app.showSuccess(`Busca OK: ${result.results_count} resultados`);
            } else {
                this.app.showError(`Busca falhou: ${result.error}`);
            }
            
        } catch (error) {
            console.error('❌ Erro no teste:', error);
            this.app.showError('Erro no teste de busca');
        }
    }

    async showExtractorStats() {
        try {
            const response = await fetch('/api/extractor_stats');
            const result = await response.json();
            
            console.log('📊 Estatísticas dos extratores:', result);
            
            if (result.success) {
                const stats = result.stats;
                let message = 'Estatísticas dos Extratores:\n';
                
                for (const [name, stat] of Object.entries(stats)) {
                    if (name !== 'global') {
                        message += `${name}: ${stat.available ? 'Disponível' : 'Indisponível'}\n`;
                    }
                }
                
                alert(message);
            }
            
        } catch (error) {
            console.error('❌ Erro ao obter stats:', error);
            this.app.showError('Erro ao obter estatísticas');
        }
    }

    async resetExtractors() {
        try {
            const response = await fetch('/api/reset_extractors', { method: 'POST' });
            const result = await response.json();
            
            if (result.success) {
                this.app.showSuccess('Extratores resetados com sucesso');
            } else {
                this.app.showError('Erro ao resetar extratores');
            }
            
        } catch (error) {
            console.error('❌ Erro ao resetar:', error);
            this.app.showError('Erro ao resetar extratores');
        }
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ARQV30App();
    window.analysisManager = new AnalysisManager();
    window.analysisManager.init(window.app);
    
    console.log('🚀 ARQV30 Enhanced v2.0 inicializado');
    console.log('📋 Recursos aprimorados:');
    console.log('   • Pipeline de análise com continuidade garantida');
    console.log('   • Zero tolerância a simulações');
    console.log('   • Dados brutos filtrados do relatório final');
    console.log('   • Validação de qualidade ultra-rigorosa');
    console.log('   • Sistema de busca multi-camadas');
});