// ARQV30 Enhanced v2.0 - Analysis JavaScript
// Sistema aprimorado de análise com Gemini 2.5 Pro e relatórios consolidados

class AnalysisManager {
    constructor() {
        this.currentAnalysis = null;
        this.consolidatedReports = [];
        this.progressTracker = null;
        
        this.init();
    }

    init() {
        this.setupAnalysisHandlers();
        this.setupReportHandlers();
        this.checkSystemCapabilities();
    }

    setupAnalysisHandlers() {
        // Handler para análise aprimorada
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.executeEnhancedAnalysis();
            });
        }
    }

    setupReportHandlers() {
        // Handlers para relatórios consolidados
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('download-report-btn')) {
                const reportType = e.target.dataset.reportType;
                const sessionId = e.target.dataset.sessionId;
                this.downloadConsolidatedReport(reportType, sessionId);
            }
            
            if (e.target.classList.contains('view-report-btn')) {
                const reportType = e.target.dataset.reportType;
                const sessionId = e.target.dataset.sessionId;
                this.viewConsolidatedReport(reportType, sessionId);
            }
        });
    }

    async executeEnhancedAnalysis() {
        try {
            // Valida formulário
            if (!this.validateEnhancedForm()) {
                this.showError('Por favor, corrija os erros no formulário.');
                return;
            }

            // Coleta dados
            const formData = this.collectEnhancedFormData();
            
            console.log('🚀 Iniciando análise ultra-avançada:', formData);

            // Mostra progresso aprimorado
            this.showEnhancedProgress();

            // Executa análise
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                this.currentAnalysis = result;
                this.hideProgress();
                await this.displayEnhancedResults(result);
                this.showSuccess('Análise ultra-avançada concluída com sucesso!');
                
                // Carrega relatórios consolidados
                await this.loadConsolidatedReports(formData.session_id);
                
            } else {
                throw new Error(result.message || 'Erro na análise');
            }

        } catch (error) {
            console.error('❌ Erro na análise:', error);
            this.hideProgress();
            this.showError('Erro na análise: ' + error.message);
        }
    }

    validateEnhancedForm() {
        const form = document.getElementById('analysisForm');
        const requiredFields = form.querySelectorAll('[required]');
        
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.highlightFieldError(field, 'Campo obrigatório');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });

        // Validação específica do segmento
        const segmento = document.getElementById('segmento');
        if (segmento && segmento.value.trim().length < 3) {
            this.highlightFieldError(segmento, 'Segmento deve ter pelo menos 3 caracteres');
            isValid = false;
        }

        return isValid;
    }

    collectEnhancedFormData() {
        const form = document.getElementById('analysisForm');
        const formData = new FormData(form);
        
        const data = {
            session_id: this.generateSessionId(),
            timestamp: new Date().toISOString(),
            analysis_type: 'ultra_advanced',
            ai_preference: 'gemini_2_5_pro'
        };
        
        // Coleta dados do formulário
        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                if (['preco', 'objetivo_receita', 'orcamento_marketing'].includes(key)) {
                    data[key] = parseFloat(value) || 0;
                } else {
                    data[key] = value.trim();
                }
            }
        }

        // Adiciona arquivos enviados se houver
        if (window.uploadManager) {
            data.uploaded_files = window.uploadManager.getUploadedFiles();
        }

        return data;
    }

    showEnhancedProgress() {
        const progressArea = document.getElementById('progressArea');
        const resultsArea = document.getElementById('resultsArea');
        
        if (progressArea) {
            progressArea.style.display = 'block';
            progressArea.scrollIntoView({ behavior: 'smooth' });
            
            // Atualiza textos para análise aprimorada
            const currentStep = document.getElementById('currentStep');
            if (currentStep) {
                currentStep.textContent = 'Iniciando análise ultra-avançada com Gemini 2.5 Pro...';
            }
        }
        
        if (resultsArea) {
            resultsArea.style.display = 'none';
        }

        // Atualiza botão
        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-magic fa-spin"></i> <span>Analisando com IA Avançada...</span>';
        }

        // Inicia tracking de progresso aprimorado
        this.startEnhancedProgressTracking();
    }

    async startEnhancedProgressTracking() {
        try {
            // Mensagens de progresso aprimoradas
            const enhancedMessages = [
                '🔍 Executando pesquisa inteligente massiva...',
                '🧠 Sintetizando conteúdo com IA avançada...',
                '🚀 Analisando com Gemini 2.5 Pro...',
                '⚡ Gerando componentes ultra-robustos...',
                '🧠 Criando drivers mentais customizados...',
                '🎭 Desenvolvendo provas visuais inovadoras...',
                '🛡️ Construindo sistema anti-objeção avançado...',
                '🎯 Arquitetando pré-pitch revolucionário...',
                '🔮 Gerando predições futuras avançadas...',
                '📊 Consolidando relatórios premium...',
                '💾 Salvando relatórios localmente...',
                '📋 Gerando múltiplos formatos...',
                '✅ Análise ultra-avançada concluída!'
            ];

            let currentStep = 0;
            
            this.progressInterval = setInterval(() => {
                if (currentStep < enhancedMessages.length) {
                    this.updateEnhancedProgressUI({
                        current_step: currentStep + 1,
                        total_steps: enhancedMessages.length,
                        current_message: enhancedMessages[currentStep],
                        percentage: ((currentStep + 1) / enhancedMessages.length) * 100
                    });
                    currentStep++;
                } else {
                    clearInterval(this.progressInterval);
                }
            }, 3000); // A cada 3 segundos

        } catch (error) {
            console.error('❌ Erro no tracking de progresso:', error);
        }
    }

    updateEnhancedProgressUI(progress) {
        // Atualiza barra de progresso
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = progress.percentage + '%';
        }

        // Atualiza mensagem atual
        const currentStep = document.getElementById('currentStep');
        if (currentStep) {
            currentStep.textContent = progress.current_message;
        }

        // Atualiza contador
        const stepCounter = document.getElementById('stepCounter');
        if (stepCounter) {
            stepCounter.textContent = `${progress.current_step}/${progress.total_steps}`;
        }

        // Adiciona efeitos visuais
        this.addProgressVisualEffects(progress);
    }

    addProgressVisualEffects(progress) {
        // Adiciona efeitos visuais baseados no progresso
        const progressContainer = document.querySelector('.progress-container');
        if (progressContainer) {
            // Remove classes anteriores
            progressContainer.classList.remove('phase-research', 'phase-ai', 'phase-components', 'phase-consolidation');
            
            // Adiciona classe baseada na fase
            if (progress.current_step <= 3) {
                progressContainer.classList.add('phase-research');
            } else if (progress.current_step <= 6) {
                progressContainer.classList.add('phase-ai');
            } else if (progress.current_step <= 10) {
                progressContainer.classList.add('phase-components');
            } else {
                progressContainer.classList.add('phase-consolidation');
            }
        }
    }

    async displayEnhancedResults(analysis) {
        console.log('📊 Exibindo resultados ultra-avançados:', analysis);
        
        const resultsArea = document.getElementById('resultsArea');
        if (resultsArea) {
            resultsArea.style.display = 'block';
            resultsArea.scrollIntoView({ behavior: 'smooth' });
        }

        // Exibe componentes aprimorados
        await this.displayUltraRobustAvatar(analysis.avatar_ultra_detalhado);
        await this.displayEnhancedInsights(analysis.insights_exclusivos);
        await this.displayAdvancedMetrics(analysis.metricas_kpis_ultra_avancados);
        await this.displayInnovativeComponents(analysis);
        
        // Exibe metadados aprimorados
        this.displayEnhancedMetadata(analysis.metadata);
        
        // Configura downloads de relatórios
        this.setupReportDownloads(analysis);
    }

    async displayUltraRobustAvatar(avatar) {
        if (!avatar) return;

        const container = document.getElementById('avatarResults');
        if (!container) return;

        const demografico = avatar.perfil_demografico || {};
        const psicografico = avatar.perfil_psicografico || {};
        const comportamental = avatar.analise_comportamental_avancada || {};
        const dores = avatar.dores_viscerais || [];
        const desejos = avatar.desejos_secretos || [];

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-user-astronaut"></i> Avatar Ultra-Robusto (${Object.keys(demografico).length + Object.keys(psicografico).length} atributos)</h4>
                    <div class="quality-indicator">
                        <span class="quality-badge ultra-premium">ULTRA PREMIUM</span>
                    </div>
                </div>
                <div class="result-section-content">
                    <div class="avatar-grid">
                        <div class="avatar-card enhanced">
                            <h5><i class="fas fa-chart-bar"></i> Perfil Demográfico Detalhado</h5>
                            ${Object.entries(demografico).map(([key, value]) => `
                                <div class="avatar-item enhanced">
                                    <span class="avatar-label">${this.formatLabel(key)}</span>
                                    <span class="avatar-value">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div class="avatar-card enhanced">
                            <h5><i class="fas fa-brain"></i> Perfil Psicográfico Avançado</h5>
                            ${Object.entries(psicografico).map(([key, value]) => `
                                <div class="avatar-item enhanced">
                                    <span class="avatar-label">${this.formatLabel(key)}</span>
                                    <span class="avatar-value">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    ${comportamental.padroes_decisao ? `
                        <div class="avatar-card enhanced">
                            <h5><i class="fas fa-cogs"></i> Análise Comportamental Avançada</h5>
                            <div class="behavioral-analysis">
                                <div class="behavior-item">
                                    <strong>Padrões de Decisão:</strong>
                                    <ul>${comportamental.padroes_decisao.map(p => `<li>${p}</li>`).join('')}</ul>
                                </div>
                                <div class="behavior-item">
                                    <strong>Triggers Emocionais:</strong>
                                    <ul>${comportamental.triggers_emocionais?.map(t => `<li>${t}</li>`).join('') || '<li>Analisando...</li>'}</ul>
                                </div>
                            </div>
                        </div>
                    ` : ''}
                    
                    <div class="avatar-grid">
                        <div class="avatar-card enhanced">
                            <h5><i class="fas fa-heart-broken"></i> Dores Viscerais (${dores.length})</h5>
                            <ul class="insight-list enhanced">
                                ${dores.map((dor, index) => `
                                    <li class="insight-item enhanced">
                                        <span class="insight-number">${index + 1}</span>
                                        <span class="insight-text">${dor}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                        
                        <div class="avatar-card enhanced">
                            <h5><i class="fas fa-star"></i> Desejos Secretos (${desejos.length})</h5>
                            <ul class="insight-list enhanced">
                                ${desejos.map((desejo, index) => `
                                    <li class="insight-item enhanced">
                                        <span class="insight-number">${index + 1}</span>
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

    async displayEnhancedInsights(insights) {
        if (!insights || !Array.isArray(insights)) return;

        const container = document.getElementById('insightsResults');
        if (!container) return;

        // Se insights são objetos aprimorados
        const isEnhanced = insights.length > 0 && typeof insights[0] === 'object';

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-lightbulb"></i> Insights Ultra-Robustos (${insights.length})</h4>
                    <div class="quality-indicators">
                        <span class="quality-badge premium">DADOS REAIS</span>
                        <span class="quality-badge enhanced">ULTRA PREMIUM</span>
                    </div>
                </div>
                <div class="result-section-content">
                    <div class="insights-showcase enhanced">
                        ${insights.map((insight, index) => {
                            if (isEnhanced) {
                                return `
                                    <div class="insight-card enhanced" data-priority="${insight.prioridade || 5}">
                                        <div class="insight-header">
                                            <div class="insight-number">${insight.id || index + 1}</div>
                                            <div class="insight-meta">
                                                <span class="insight-category">${insight.categoria || 'Mercado'}</span>
                                                <span class="insight-priority priority-${this.getPriorityClass(insight.prioridade || 5)}">${insight.prioridade || 5}/10</span>
                                            </div>
                                        </div>
                                        <div class="insight-content">${insight.insight_original || insight.insight || insight}</div>
                                        ${insight.acionabilidade ? `
                                            <div class="insight-actionability">
                                                <strong>Acionabilidade:</strong> ${insight.acionabilidade.score || 'N/A'}/10
                                                <div class="implementation-steps">
                                                    ${insight.acionabilidade.passos_implementacao?.map(passo => `<div class="step">${passo}</div>`).join('') || ''}
                                                </div>
                                            </div>
                                        ` : ''}
                                        ${insight.impacto_estimado ? `
                                            <div class="insight-impact">
                                                <strong>Impacto:</strong> <span class="impact-${insight.impacto_estimado.toLowerCase()}">${insight.impacto_estimado}</span>
                                            </div>
                                        ` : ''}
                                    </div>
                                `;
                            } else {
                                return `
                                    <div class="insight-card">
                                        <div class="insight-number">${index + 1}</div>
                                        <div class="insight-content">${insight}</div>
                                    </div>
                                `;
                            }
                        }).join('')}
                    </div>
                </div>
            </div>
        `;

        // Adiciona interatividade aos insights aprimorados
        if (isEnhanced) {
            this.addInsightInteractivity();
        }
    }

    async displayAdvancedMetrics(metrics) {
        if (!metrics) return;

        const container = document.getElementById('metricsResults');
        if (!container) return;

        const projecoes = metrics.projecoes_financeiras || {};
        const kpis = metrics.kpis_principais || [];

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-chart-line"></i> Métricas e KPIs Ultra-Avançados</h4>
                </div>
                <div class="result-section-content">
                    <div class="metrics-dashboard">
                        <div class="financial-projections">
                            <h5>💰 Projeções Financeiras Detalhadas</h5>
                            <div class="projections-grid">
                                ${this.renderFinancialScenario('Conservador', projecoes.cenario_conservador)}
                                ${this.renderFinancialScenario('Realista', projecoes.cenario_realista)}
                                ${this.renderFinancialScenario('Otimista', projecoes.cenario_otimista)}
                            </div>
                        </div>
                        
                        <div class="kpis-section">
                            <h5>📊 KPIs Principais</h5>
                            <div class="kpis-grid">
                                ${kpis.map(kpi => `
                                    <div class="kpi-card">
                                        <div class="kpi-name">${kpi.metrica || 'Métrica'}</div>
                                        <div class="kpi-target">${kpi.objetivo || 'N/A'}</div>
                                        <div class="kpi-frequency">${kpi.frequencia || 'N/A'}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        
                        ${metrics.framework_metricas_avancado ? `
                            <div class="advanced-metrics">
                                <h5>⚡ Framework de Métricas Avançado</h5>
                                <div class="framework-grid">
                                    <div class="framework-item">
                                        <strong>Leading Indicators:</strong>
                                        <ul>${metrics.framework_metricas_avancado.metricas_leading?.map(m => `<li>${m}</li>`).join('') || '<li>Carregando...</li>'}</ul>
                                    </div>
                                    <div class="framework-item">
                                        <strong>Lagging Indicators:</strong>
                                        <ul>${metrics.framework_metricas_avancado.metricas_lagging?.map(m => `<li>${m}</li>`).join('') || '<li>Carregando...</li>'}</ul>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    async displayInnovativeComponents(analysis) {
        // Exibe componentes inovadores se disponíveis
        const innovativeComponents = [
            'analise_ecossistema',
            'ia_aplicada', 
            'sustentabilidade_esg',
            'experiencia_cliente_360',
            'inovacao_disruptiva'
        ];

        for (const componentName of innovativeComponents) {
            if (analysis[componentName]) {
                await this.displayInnovativeComponent(componentName, analysis[componentName]);
            }
        }
    }

    async displayInnovativeComponent(componentName, componentData) {
        const container = document.getElementById('innovativeResults') || this.createInnovativeContainer();
        
        const componentTitle = this.formatComponentTitle(componentName);
        const componentIcon = this.getComponentIcon(componentName);

        const componentHtml = `
            <div class="result-section innovative">
                <div class="result-section-header">
                    <h4><i class="${componentIcon}"></i> ${componentTitle}</h4>
                    <span class="innovation-badge">INOVADOR</span>
                </div>
                <div class="result-section-content">
                    ${this.formatInnovativeComponentContent(componentData)}
                </div>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', componentHtml);
    }

    async loadConsolidatedReports(sessionId) {
        try {
            const response = await fetch(`/api/list_consolidated_reports/${sessionId}`);
            const result = await response.json();

            if (response.ok && result.reports) {
                this.consolidatedReports = result.reports;
                this.displayConsolidatedReportsSection(result.reports, sessionId);
            }

        } catch (error) {
            console.error('❌ Erro ao carregar relatórios consolidados:', error);
        }
    }

    displayConsolidatedReportsSection(reports, sessionId) {
        const container = document.getElementById('reportsResults') || this.createReportsContainer();

        const reportsHtml = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-file-alt"></i> Relatórios Consolidados (${reports.length})</h4>
                </div>
                <div class="result-section-content">
                    <div class="reports-grid">
                        ${reports.map(report => `
                            <div class="report-card">
                                <div class="report-icon">
                                    <i class="${this.getReportIcon(report.type)}"></i>
                                </div>
                                <div class="report-info">
                                    <h6>${this.getReportTitle(report.type)}</h6>
                                    <p>${this.getReportDescription(report.type)}</p>
                                    <div class="report-meta">
                                        <span class="report-size">${this.formatFileSize(report.size)}</span>
                                        <span class="report-date">${new Date(report.created).toLocaleDateString('pt-BR')}</span>
                                    </div>
                                </div>
                                <div class="report-actions">
                                    <button class="btn-secondary download-report-btn" 
                                            data-report-type="${report.type}" 
                                            data-session-id="${sessionId}">
                                        <i class="fas fa-download"></i> Download
                                    </button>
                                    ${report.type === 'dashboard' ? `
                                        <button class="btn-secondary view-report-btn" 
                                                data-report-type="${report.type}" 
                                                data-session-id="${sessionId}">
                                            <i class="fas fa-eye"></i> Visualizar
                                        </button>
                                    ` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = reportsHtml;
    }

    async downloadConsolidatedReport(reportType, sessionId) {
        try {
            this.showInfo(`Baixando relatório ${this.getReportTitle(reportType)}...`);

            const response = await fetch(`/api/download_consolidated_report/${reportType}/${sessionId}`);

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${this.getReportTitle(reportType)}_${new Date().toISOString().slice(0, 10)}.${this.getReportExtension(reportType)}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                this.showSuccess(`Relatório ${this.getReportTitle(reportType)} baixado com sucesso!`);
            } else {
                throw new Error('Erro ao baixar relatório');
            }

        } catch (error) {
            console.error('❌ Erro ao baixar relatório:', error);
            this.showError('Erro ao baixar relatório: ' + error.message);
        }
    }

    async viewConsolidatedReport(reportType, sessionId) {
        if (reportType === 'dashboard') {
            // Abre dashboard em nova aba
            const url = `/api/download_consolidated_report/${reportType}/${sessionId}`;
            window.open(url, '_blank');
        }
    }

    displayEnhancedMetadata(metadata) {
        if (!metadata) return;

        const container = document.getElementById('metadataResults');
        if (!container) return;

        container.innerHTML = `
            <div class="result-section">
                <div class="result-section-header">
                    <h4><i class="fas fa-info-circle"></i> Metadados da Análise Ultra-Avançada</h4>
                </div>
                <div class="result-section-content">
                    <div class="metadata-grid enhanced">
                        <div class="metadata-item premium">
                            <span class="metadata-label">IA Principal</span>
                            <span class="metadata-value">${metadata.ai_provider_primary || 'N/A'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">IA Fallback</span>
                            <span class="metadata-value">${metadata.ai_provider_fallback || 'N/A'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Tempo de Processamento</span>
                            <span class="metadata-value">${metadata.processing_time_formatted || 'N/A'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Score de Qualidade</span>
                            <span class="metadata-value quality-score">${metadata.quality_score || 0}%</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Relatórios Gerados</span>
                            <span class="metadata-value">${metadata.consolidated_reports || 0}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Dados Brutos Filtrados</span>
                            <span class="metadata-value">${metadata.raw_data_filtered ? '✅ SIM' : '❌ NÃO'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Backup Local</span>
                            <span class="metadata-value">${metadata.local_backup?.success ? '✅ GARANTIDO' : '❌ FALHOU'}</span>
                        </div>
                        <div class="metadata-item premium">
                            <span class="metadata-label">Pipeline</span>
                            <span class="metadata-value">${metadata.pipeline_version || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Métodos auxiliares
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    formatLabel(key) {
        return key.replace(/_/g, ' ')
                 .replace(/\b\w/g, l => l.toUpperCase());
    }

    getPriorityClass(priority) {
        if (priority >= 8) return 'high';
        if (priority >= 6) return 'medium';
        return 'low';
    }

    formatComponentTitle(componentName) {
        const titles = {
            'analise_ecossistema': 'Análise de Ecossistema',
            'ia_aplicada': 'IA Aplicada',
            'sustentabilidade_esg': 'Sustentabilidade e ESG',
            'experiencia_cliente_360': 'Experiência do Cliente 360°',
            'inovacao_disruptiva': 'Inovação Disruptiva'
        };
        return titles[componentName] || componentName;
    }

    getComponentIcon(componentName) {
        const icons = {
            'analise_ecossistema': 'fas fa-network-wired',
            'ia_aplicada': 'fas fa-robot',
            'sustentabilidade_esg': 'fas fa-leaf',
            'experiencia_cliente_360': 'fas fa-user-friends',
            'inovacao_disruptiva': 'fas fa-rocket'
        };
        return icons[componentName] || 'fas fa-cog';
    }

    getReportIcon(reportType) {
        const icons = {
            'executive': 'fas fa-crown',
            'technical': 'fas fa-cogs',
            'implementation': 'fas fa-tasks',
            'dashboard': 'fas fa-chart-bar',
            'insights': 'fas fa-lightbulb',
            'roi': 'fas fa-dollar-sign',
            'contingency': 'fas fa-shield-alt',
            'monitoring': 'fas fa-eye'
        };
        return icons[reportType] || 'fas fa-file';
    }

    getReportTitle(reportType) {
        const titles = {
            'executive': 'Relatório Executivo Premium',
            'technical': 'Análise Técnica Detalhada',
            'implementation': 'Guia de Implementação',
            'dashboard': 'Dashboard Interativo',
            'insights': 'Relatório de Insights',
            'roi': 'Análise de ROI',
            'contingency': 'Plano de Contingência',
            'monitoring': 'Sistema de Monitoramento'
        };
        return titles[reportType] || 'Relatório';
    }

    getReportDescription(reportType) {
        const descriptions = {
            'executive': 'Resumo executivo com descobertas-chave e recomendações estratégicas',
            'technical': 'Análise técnica completa com todos os componentes detalhados',
            'implementation': 'Roadmap detalhado de implementação com cronograma e recursos',
            'dashboard': 'Dashboard visual interativo com métricas em tempo real',
            'insights': 'Insights prioritizados com análise de impacto e acionabilidade',
            'roi': 'Projeções financeiras detalhadas e análise de retorno sobre investimento',
            'contingency': 'Cenários de risco e planos de resposta detalhados',
            'monitoring': 'KPIs, alertas e sistema de acompanhamento contínuo'
        };
        return descriptions[reportType] || 'Relatório especializado';
    }

    getReportExtension(reportType) {
        if (reportType === 'dashboard') return 'html';
        if (reportType === 'technical') return 'json';
        return 'md';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    renderFinancialScenario(scenarioName, scenarioData) {
        if (!scenarioData) return '';

        return `
            <div class="scenario-card scenario-${scenarioName.toLowerCase()}">
                <h6>${scenarioName}</h6>
                <div class="scenario-metrics">
                    <div class="metric">
                        <span class="metric-label">Receita Mensal</span>
                        <span class="metric-value">${scenarioData.receita_mensal || 'N/A'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Clientes/Mês</span>
                        <span class="metric-value">${scenarioData.clientes_mes || 'N/A'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Ticket Médio</span>
                        <span class="metric-value">${scenarioData.ticket_medio || 'N/A'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Margem</span>
                        <span class="metric-value">${scenarioData.margem_lucro || 'N/A'}</span>
                    </div>
                </div>
            </div>
        `;
    }

    createInnovativeContainer() {
        const resultsContent = document.querySelector('.results-content');
        if (resultsContent) {
            const container = document.createElement('div');
            container.id = 'innovativeResults';
            container.className = 'result-container';
            resultsContent.appendChild(container);
            return container;
        }
        return null;
    }

    createReportsContainer() {
        const resultsContent = document.querySelector('.results-content');
        if (resultsContent) {
            const container = document.createElement('div');
            container.id = 'reportsResults';
            container.className = 'result-container';
            resultsContent.appendChild(container);
            return container;
        }
        return null;
    }

    formatInnovativeComponentContent(componentData) {
        if (!componentData || typeof componentData !== 'object') {
            return '<p>Dados do componente não disponíveis</p>';
        }

        let html = '<div class="innovative-content">';
        
        for (const [key, value] of Object.entries(componentData)) {
            html += `
                <div class="innovative-item">
                    <h6>${this.formatLabel(key)}</h6>
                    ${Array.isArray(value) ? 
                        `<ul>${value.map(item => `<li>${item}</li>`).join('')}</ul>` :
                        `<p>${value}</p>`
                    }
                </div>
            `;
        }
        
        html += '</div>';
        return html;
    }

    addInsightInteractivity() {
        // Adiciona filtros por categoria
        const insightsContainer = document.querySelector('.insights-showcase.enhanced');
        if (insightsContainer) {
            const filterControls = document.createElement('div');
            filterControls.className = 'insight-filters';
            filterControls.innerHTML = `
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="all">Todos</button>
                    <button class="filter-btn" data-filter="Oportunidade">Oportunidades</button>
                    <button class="filter-btn" data-filter="Risco">Riscos</button>
                    <button class="filter-btn" data-filter="Tendência">Tendências</button>
                    <button class="filter-btn" data-filter="Estratégia">Estratégias</button>
                </div>
            `;
            
            insightsContainer.parentNode.insertBefore(filterControls, insightsContainer);
            
            // Adiciona event listeners para filtros
            filterControls.addEventListener('click', (e) => {
                if (e.target.classList.contains('filter-btn')) {
                    this.filterInsights(e.target.dataset.filter);
                    
                    // Atualiza botões ativos
                    filterControls.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                    e.target.classList.add('active');
                }
            });
        }
    }

    filterInsights(category) {
        const insightCards = document.querySelectorAll('.insight-card.enhanced');
        
        insightCards.forEach(card => {
            if (category === 'all') {
                card.style.display = 'block';
            } else {
                const cardCategory = card.querySelector('.insight-category')?.textContent;
                card.style.display = cardCategory === category ? 'block' : 'none';
            }
        });
    }

    async checkSystemCapabilities() {
        try {
            // Verifica capacidades do sistema aprimorado
            const response = await fetch('/api/app_status');
            const status = await response.json();

            this.updateSystemCapabilities(status);

        } catch (error) {
            console.error('❌ Erro ao verificar capacidades:', error);
        }
    }

    updateSystemCapabilities(status) {
        const capabilitiesContainer = document.getElementById('systemCapabilities');
        if (capabilitiesContainer) {
            const geminiAvailable = status.services?.ai_providers?.details?.gemini?.available || false;
            const groqAvailable = status.services?.ai_providers?.details?.groq?.available || false;

            capabilitiesContainer.innerHTML = `
                <div class="capabilities-grid">
                    <div class="capability-item ${geminiAvailable ? 'available' : 'unavailable'}">
                        <i class="fas fa-brain"></i>
                        <span>Gemini 2.5 Pro</span>
                        <span class="status">${geminiAvailable ? 'Disponível' : 'Indisponível'}</span>
                    </div>
                    <div class="capability-item ${groqAvailable ? 'available' : 'unavailable'}">
                        <i class="fas fa-rocket"></i>
                        <span>Groq Fallback</span>
                        <span class="status">${groqAvailable ? 'Disponível' : 'Indisponível'}</span>
                    </div>
                    <div class="capability-item available">
                        <i class="fas fa-file-alt"></i>
                        <span>Relatórios Consolidados</span>
                        <span class="status">Ativo</span>
                    </div>
                    <div class="capability-item available">
                        <i class="fas fa-shield-alt"></i>
                        <span>Backup Local</span>
                        <span class="status">Garantido</span>
                    </div>
                </div>
            `;
        }
    }

    hideProgress() {
        const progressArea = document.getElementById('progressArea');
        if (progressArea) {
            progressArea.style.display = 'none';
        }

        const analyzeBtn = document.getElementById('analyzeBtn');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('loading');
            analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> <span>Gerar Análise Ultra-Avançada</span>';
        }

        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    highlightFieldError(field, message) {
        field.classList.add('error');
        
        // Remove erro anterior
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }

        // Adiciona novo erro
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        field.parentNode.appendChild(errorElement);
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'error');
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
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; color: inherit; cursor: pointer; font-size: 18px;">&times;</button>
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
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    window.analysisManager = new AnalysisManager();
    console.log('🚀 Analysis Manager Ultra-Avançado inicializado');
});