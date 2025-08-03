#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Corrected Ultra Detailed Analysis Engine
Motor de análise ultra-detalhado CORRIGIDO - Elimina simulações e fallbacks
"""

import time
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from services.ai_manager import ai_manager
from services.ultra_robust_search_manager import ultra_robust_search_manager
from services.enhanced_pre_pitch_architect import enhanced_pre_pitch_architect
from services.mental_drivers_architect import mental_drivers_architect
from services.visual_proofs_generator import visual_proofs_generator
from services.anti_objection_system import anti_objection_system
from services.future_prediction_engine import future_prediction_engine
from services.auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class CorrectedUltraDetailedAnalysisEngine:
    """Motor de análise ultra-detalhado CORRIGIDO - Zero tolerância a simulações"""
    
    def __init__(self):
        """Inicializa o motor corrigido"""
        self.strict_quality_thresholds = {
            'min_sources': 8,
            'min_content_length': 15000,
            'min_quality_score': 75.0,
            'min_unique_domains': 5,
            'min_successful_extractions': 6
        }
        
        self.component_requirements = {
            'pesquisa_web_massiva': {'required': True, 'fallback': False},
            'avatar_ultra_detalhado': {'required': True, 'fallback': False},
            'drivers_mentais_customizados': {'required': True, 'fallback': False},
            'provas_visuais_sugeridas': {'required': True, 'fallback': False},
            'sistema_anti_objecao': {'required': True, 'fallback': False},
            'pre_pitch_invisivel': {'required': True, 'fallback': False},
            'predicoes_futuro_completas': {'required': False, 'fallback': False}
        }
        
        logger.info("🚀 Corrected Ultra Detailed Analysis Engine inicializado - ZERO SIMULAÇÃO")
    
    def generate_corrected_gigantic_analysis(
        self, 
        data: Dict[str, Any],
        session_id: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Gera análise GIGANTE corrigida - FALHA se dados insuficientes"""
        
        start_time = time.time()
        logger.info(f"🚀 INICIANDO ANÁLISE GIGANTE CORRIGIDA para {data.get('segmento')}")
        
        # Inicia sessão
        session_id = session_id or auto_save_manager.iniciar_sessao()
        
        # Salva início
        salvar_etapa("analise_gigante_iniciada", {
            "input_data": data,
            "session_id": session_id,
            "thresholds": self.strict_quality_thresholds,
            "start_time": start_time
        }, categoria="analise_completa")
        
        if progress_callback:
            progress_callback(1, "🔍 Validando dados de entrada com critérios rigorosos...")
        
        # VALIDAÇÃO RIGOROSA - FALHA SE INSUFICIENTE
        validation_result = self._validate_input_data_strict(data)
        if not validation_result['valid']:
            error_msg = f"DADOS INSUFICIENTES: {validation_result['message']}"
            salvar_erro("validacao_rigorosa", ValueError(error_msg), contexto=data)
            raise Exception(error_msg)
        
        try:
            # FASE 1: PESQUISA WEB ULTRA-ROBUSTA
            if progress_callback:
                progress_callback(2, "🌐 Executando pesquisa web ultra-robusta...")
            
            research_data = self._execute_ultra_robust_research(data, progress_callback)
            
            # VALIDAÇÃO RIGOROSA DA PESQUISA
            if not self._validate_research_quality_strict(research_data):
                error_msg = "PESQUISA INSUFICIENTE: Não foi possível coletar dados reais de qualidade suficiente"
                salvar_erro("pesquisa_insuficiente", ValueError(error_msg), contexto=research_data.get('statistics', {}))
                raise Exception(error_msg)
            
            # FASE 2: ANÁLISE COM IA RIGOROSA
            if progress_callback:
                progress_callback(4, "🤖 Executando análise com IA - critérios rigorosos...")
            
            ai_analysis = self._execute_strict_ai_analysis(data, research_data)
            
            # VALIDAÇÃO RIGOROSA DA IA
            if not self._validate_ai_response_strict(ai_analysis):
                error_msg = "IA INSUFICIENTE: Análise gerada não atende critérios de qualidade"
                salvar_erro("ia_insuficiente", ValueError(error_msg), contexto={"ai_response_length": len(str(ai_analysis))})
                raise Exception(error_msg)
            
            # FASE 3: COMPONENTES AVANÇADOS COM VALIDAÇÃO RIGOROSA
            advanced_components = {}
            
            # Drivers Mentais
            if progress_callback:
                progress_callback(6, "🧠 Gerando drivers mentais - sem fallbacks...")
            
            drivers_result = self._generate_strict_mental_drivers(ai_analysis, data)
            if drivers_result['success']:
                advanced_components['drivers_mentais_customizados'] = drivers_result['data']
            else:
                error_msg = f"DRIVERS MENTAIS FALHARAM: {drivers_result['error']}"
                salvar_erro("drivers_falharam", ValueError(error_msg))
                raise Exception(error_msg)
            
            # Provas Visuais
            if progress_callback:
                progress_callback(7, "🎭 Gerando provas visuais - sem simulações...")
            
            provas_result = self._generate_strict_visual_proofs(ai_analysis, data)
            if provas_result['success']:
                advanced_components['provas_visuais_sugeridas'] = provas_result['data']
            else:
                error_msg = f"PROVAS VISUAIS FALHARAM: {provas_result['error']}"
                salvar_erro("provas_falharam", ValueError(error_msg))
                raise Exception(error_msg)
            
            # Sistema Anti-Objeção
            if progress_callback:
                progress_callback(8, "🛡️ Construindo sistema anti-objeção rigoroso...")
            
            anti_obj_result = self._generate_strict_anti_objection(ai_analysis, data)
            if anti_obj_result['success']:
                advanced_components['sistema_anti_objecao'] = anti_obj_result['data']
            else:
                error_msg = f"ANTI-OBJEÇÃO FALHOU: {anti_obj_result['error']}"
                salvar_erro("anti_objecao_falhou", ValueError(error_msg))
                raise Exception(error_msg)
            
            # Pré-Pitch Corrigido
            if progress_callback:
                progress_callback(9, "🎯 Arquitetando pré-pitch - versão corrigida...")
            
            pre_pitch_result = self._generate_corrected_pre_pitch(advanced_components, ai_analysis, data)
            if pre_pitch_result['success']:
                advanced_components['pre_pitch_invisivel'] = pre_pitch_result['data']
            else:
                error_msg = f"PRÉ-PITCH FALHOU: {pre_pitch_result['error']}"
                salvar_erro("pre_pitch_falhou", ValueError(error_msg))
                raise Exception(error_msg)
            
            # Predições do Futuro
            if progress_callback:
                progress_callback(10, "🔮 Gerando predições do futuro...")
            
            future_result = self._generate_strict_future_predictions(data, research_data)
            if future_result['success']:
                advanced_components['predicoes_futuro_completas'] = future_result['data']
            else:
                logger.warning(f"⚠️ Predições do futuro falharam: {future_result['error']}")
                # Predições são opcionais
            
            # FASE 4: CONSOLIDAÇÃO FINAL RIGOROSA
            if progress_callback:
                progress_callback(12, "✨ Consolidando análise com validação final...")
            
            final_analysis = self._consolidate_strict_analysis(
                data, research_data, ai_analysis, advanced_components
            )
            
            # VALIDAÇÃO FINAL ULTRA-RIGOROSA
            final_validation = self._validate_final_analysis_ultra_strict(final_analysis)
            if not final_validation['valid']:
                error_msg = f"ANÁLISE FINAL INVÁLIDA: {final_validation['errors']}"
                salvar_erro("analise_final_invalida", ValueError(error_msg), contexto=final_validation)
                # CORREÇÃO: Falha explícita sem fallback
                logger.error("❌ Análise final rejeitada por baixa qualidade")
                raise Exception(f"ANÁLISE REJEITADA: {error_msg}")
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Adiciona metadados finais
            final_analysis['metadata'] = {
                'processing_time_seconds': processing_time,
                'processing_time_formatted': f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
                'analysis_engine': 'ARQV30 Enhanced v2.0 - CORRECTED GIGANTE',
                'generated_at': datetime.utcnow().isoformat(),
                'quality_score': final_validation['quality_score'],
                'validation_passed': True,
                'simulation_free_guarantee': True,
                'fallback_free_guarantee': True,
                'strict_quality_enforced': True,
                'components_generated': len(advanced_components),
                'research_sources': research_data.get('statistics', {}).get('successful_extractions', 0),
                'total_content_analyzed': research_data.get('statistics', {}).get('total_content_length', 0)
            }
            
            # Salva análise final
            salvar_etapa("analise_gigante_final", final_analysis, categoria="analise_completa")
            
            if progress_callback:
                progress_callback(13, "🎉 Análise GIGANTE corrigida concluída!")
            
            logger.info(f"✅ Análise GIGANTE corrigida concluída - Score: {final_validation['quality_score']:.1f} - Tempo: {processing_time:.2f}s")
            return final_analysis
            
        except Exception as e:
            logger.error(f"❌ FALHA CRÍTICA na análise GIGANTE corrigida: {str(e)}")
            salvar_erro("analise_gigante_falha_critica", e, contexto=data)
            
            # NÃO GERA FALLBACK - FALHA EXPLICITAMENTE
            raise Exception(f"ANÁLISE ULTRA-DETALHADA FALHOU: {str(e)}. Configure todas as APIs e execute novamente.")
    
    def _validate_input_data_strict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validação rigorosa dos dados de entrada"""
        
        errors = []
        
        # Campos obrigatórios
        required_fields = ['segmento']
        for field in required_fields:
            if not data.get(field) or len(str(data[field]).strip()) < 3:
                errors.append(f"Campo obrigatório inválido: {field}")
        
        # Validações específicas
        segmento = data.get('segmento', '').strip()
        if len(segmento) < 5:
            errors.append("Segmento deve ter pelo menos 5 caracteres")
        
        # Verifica se não é teste genérico
        generic_terms = ['teste', 'test', 'exemplo', 'sample']
        if any(term in segmento.lower() for term in generic_terms):
            errors.append("Segmento não pode ser genérico ou de teste")
        
        return {
            'valid': len(errors) == 0,
            'message': '; '.join(errors) if errors else 'Dados válidos',
            'errors': errors
        }
    
    def _execute_ultra_robust_research(
        self, 
        data: Dict[str, Any], 
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Executa pesquisa ultra-robusta com múltiplas camadas"""
        
        logger.info("🌐 INICIANDO PESQUISA ULTRA-ROBUSTA")
        
        # Prepara query principal
        main_query = data.get('query') or self._generate_intelligent_main_query(data)
        
        # Salva query principal
        salvar_etapa("query_principal", {"query": main_query}, categoria="pesquisa_web")
        
        if progress_callback:
            progress_callback(2, f"🔍 Executando busca ultra-robusta: {main_query[:50]}...")
        
        # Executa busca ultra-robusta
        search_result = ultra_robust_search_manager.execute_comprehensive_search(
            main_query, 
            data, 
            max_results=60,  # Aumentado para máxima cobertura
            require_high_quality=True
        )
        
        # Salva resultado da busca
        salvar_etapa("busca_ultra_robusta", search_result, categoria="pesquisa_web")
        
        logger.info(f"✅ Pesquisa ultra-robusta: {search_result['statistics']['successful_extractions']} extrações bem-sucedidas")
        
        return search_result
    
    def _validate_research_quality_strict(self, research_data: Dict[str, Any]) -> bool:
        """Validação rigorosa da qualidade da pesquisa"""
        
        stats = research_data.get('statistics', {})
        
        # Critérios rigorosos
        successful_extractions = stats.get('successful_extractions', 0)
        total_content_length = stats.get('total_content_length', 0)
        unique_domains = stats.get('unique_domains', 0)
        avg_quality_score = stats.get('avg_quality_score', 0)
        
        # Verifica cada critério
        criteria_met = []
        
        if successful_extractions >= self.strict_quality_thresholds['min_sources']:
            criteria_met.append('sources')
        else:
            logger.error(f"❌ Fontes insuficientes: {successful_extractions} < {self.strict_quality_thresholds['min_sources']}")
        
        if total_content_length >= self.strict_quality_thresholds['min_content_length']:
            criteria_met.append('content_length')
        else:
            logger.error(f"❌ Conteúdo insuficiente: {total_content_length} < {self.strict_quality_thresholds['min_content_length']}")
        
        if unique_domains >= self.strict_quality_thresholds['min_unique_domains']:
            criteria_met.append('unique_domains')
        else:
            logger.error(f"❌ Domínios insuficientes: {unique_domains} < {self.strict_quality_thresholds['min_unique_domains']}")
        
        if avg_quality_score >= self.strict_quality_thresholds['min_quality_score']:
            criteria_met.append('quality_score')
        else:
            logger.error(f"❌ Qualidade insuficiente: {avg_quality_score:.1f} < {self.strict_quality_thresholds['min_quality_score']}")
        
        # Deve atender TODOS os critérios
        all_criteria_met = len(criteria_met) == 4
        
        logger.info(f"📊 Validação rigorosa: {len(criteria_met)}/4 critérios atendidos")
        
        return all_criteria_met
    
    def _execute_strict_ai_analysis(
        self, 
        data: Dict[str, Any], 
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Executa análise com IA com critérios rigorosos"""
        
        # Prepara contexto de pesquisa
        search_context = self._prepare_comprehensive_search_context(research_data)
        
        # Constrói prompt rigoroso
        prompt = self._build_strict_analysis_prompt(data, search_context)
        
        logger.info("🤖 Executando análise rigorosa com IA...")
        
        # Executa com IA
        ai_response = ai_manager.generate_analysis(prompt, max_tokens=8192)
        
        if not ai_response:
            raise Exception("IA NÃO RESPONDEU: Nenhum provedor de IA disponível")
        
        # Processa resposta com validação rigorosa
        processed_analysis = self._process_ai_response_ultra_strict(ai_response, data)
        
        return processed_analysis
    
    def _prepare_comprehensive_search_context(self, research_data: Dict[str, Any]) -> str:
        """Prepara contexto abrangente da pesquisa"""
        
        extracted_content = research_data.get('extracted_content', [])
        
        if not extracted_content:
            raise Exception("NENHUM CONTEÚDO EXTRAÍDO: Pesquisa falhou completamente")
        
        # Filtra apenas conteúdo de alta qualidade
        high_quality_content = [
            content for content in extracted_content 
            if (content['success'] and 
                content.get('quality_validation', {}).get('score', 0) >= 70)
        ]
        
        if len(high_quality_content) < 5:
            raise Exception(f"CONTEÚDO DE BAIXA QUALIDADE: Apenas {len(high_quality_content)} fontes de alta qualidade")
        
        # Ordena por qualidade
        high_quality_content.sort(
            key=lambda x: x.get('quality_validation', {}).get('score', 0), 
            reverse=True
        )
        
        # Constrói contexto
        context = "PESQUISA ULTRA-ROBUSTA EXECUTADA COM SUCESSO:\n\n"
        
        for i, content_item in enumerate(high_quality_content[:15], 1):
            quality_score = content_item.get('quality_validation', {}).get('score', 0)
            content_length = len(content_item.get('content', ''))
            
            context += f"--- FONTE DE ALTA QUALIDADE {i}: {content_item.get('search_title', 'Sem título')} ---\n"
            context += f"URL: {content_item.get('url', '')}\n"
            context += f"Qualidade: {quality_score:.1f}% | Tamanho: {content_length} chars\n"
            context += f"Método: {content_item.get('extraction_strategy', 'unknown')}\n"
            context += f"Conteúdo: {content_item.get('content', '')[:2500]}\n\n"
        
        # Adiciona estatísticas rigorosas
        stats = research_data.get('statistics', {})
        context += f"\n=== ESTATÍSTICAS DA PESQUISA ULTRA-ROBUSTA ===\n"
        context += f"Fontes de alta qualidade analisadas: {len(high_quality_content)}\n"
        context += f"Total de extrações bem-sucedidas: {stats.get('successful_extractions', 0)}\n"
        context += f"Domínios únicos: {stats.get('unique_domains', 0)}\n"
        context += f"Conteúdo total extraído: {stats.get('total_content_length', 0):,} caracteres\n"
        context += f"Qualidade média: {stats.get('avg_quality_score', 0):.1f}%\n"
        context += f"Camadas de busca utilizadas: {len(research_data.get('layer_performance', {}))}\n"
        context += f"Garantia de qualidade: RIGOROSA - Sem simulações ou fallbacks\n"
        
        return context
    
    def _build_strict_analysis_prompt(self, data: Dict[str, Any], search_context: str) -> str:
        """Constrói prompt rigoroso para análise"""
        
        prompt = f"""
# ANÁLISE ULTRA-RIGOROSA - ARQV30 ENHANCED v2.0 CORRIGIDO

Você é o DIRETOR SUPREMO DE ANÁLISE DE MERCADO com 30+ anos de experiência e ZERO TOLERÂNCIA a dados simulados.

## DADOS REAIS DO PROJETO:
- **Segmento**: {data.get('segmento', 'Não informado')}
- **Produto/Serviço**: {data.get('produto', 'Não informado')}
- **Público-Alvo**: {data.get('publico', 'Não informado')}
- **Preço**: R$ {data.get('preco', 'Não informado')}
- **Objetivo de Receita**: R$ {data.get('objetivo_receita', 'Não informado')}

{search_context}

## INSTRUÇÕES ULTRA-RIGOROSAS:

1. Use EXCLUSIVAMENTE dados da pesquisa acima
2. NUNCA use placeholders, templates ou dados genéricos
3. NUNCA use frases como "customizado para", "baseado em", "específico para"
4. Se não houver dados suficientes para uma seção, OMITA a seção
5. Seja ULTRA-ESPECÍFICO com dados reais, números, percentuais
6. REJEITE qualquer tentação de simular ou inventar dados

## FORMATO OBRIGATÓRIO:
```json
{{
  "avatar_ultra_detalhado": {{
    "nome_ficticio": "Nome específico baseado em dados reais da pesquisa",
    "perfil_demografico": {{
      "idade": "Faixa etária específica com dados reais encontrados",
      "genero": "Distribuição real encontrada na pesquisa",
      "renda": "Faixa de renda real baseada em dados da pesquisa",
      "escolaridade": "Nível educacional real identificado",
      "localizacao": "Regiões reais identificadas na pesquisa",
      "profissao": "Ocupações reais encontradas nos dados"
    }},
    "perfil_psicografico": {{
      "personalidade": "Traços reais identificados na pesquisa",
      "valores": "Valores reais encontrados nos dados",
      "interesses": "Interesses reais identificados",
      "comportamento_compra": "Processo real documentado na pesquisa",
      "influenciadores": "Influenciadores reais identificados",
      "medos_profundos": "Medos reais documentados",
      "aspiracoes_secretas": "Aspirações reais encontradas"
    }},
    "dores_viscerais": [
      "Lista de 10-15 dores REAIS específicas encontradas na pesquisa"
    ],
    "desejos_secretos": [
      "Lista de 10-15 desejos REAIS identificados nos dados"
    ],
    "objecoes_reais": [
      "Lista de 8-12 objeções REAIS específicas encontradas"
    ],
    "linguagem_interna": {{
      "frases_dor": ["Frases REAIS encontradas na pesquisa"],
      "frases_desejo": ["Frases REAIS de desejo identificadas"],
      "vocabulario_especifico": ["Palavras REAIS específicas do segmento"],
      "tom_comunicacao": "Tom REAL identificado na pesquisa"
    }}
  }},
  
  "escopo": {{
    "posicionamento_mercado": "Posicionamento REAL baseado na análise competitiva encontrada",
    "proposta_valor": "Proposta REAL baseada em gaps identificados na pesquisa",
    "diferenciais_competitivos": [
      "Lista de diferenciais REAIS únicos identificados"
    ],
    "mensagem_central": "Mensagem REAL que resume os achados",
    "nicho_especifico": "Nicho REAL mais específico identificado",
    "estrategia_oceano_azul": "Estratégia REAL para mercado sem concorrência",
    "ancoragem_preco": "Estratégia REAL de ancoragem baseada nos dados"
  }},
  
  "analise_concorrencia_detalhada": [
    {{
      "nome": "Nome REAL do concorrente encontrado na pesquisa",
      "analise_swot": {{
        "forcas": ["Forças REAIS identificadas na pesquisa"],
        "fraquezas": ["Fraquezas REAIS encontradas"],
        "oportunidades": ["Oportunidades REAIS identificadas"],
        "ameacas": ["Ameaças REAIS documentadas"]
      }},
      "estrategia_marketing": "Estratégia REAL observada na pesquisa",
      "posicionamento": "Posicionamento REAL identificado",
      "vulnerabilidades": ["Vulnerabilidades REAIS específicas"],
      "share_mercado_estimado": "Participação REAL estimada com base nos dados"
    }}
  ],
  
  "estrategia_palavras_chave": {{
    "palavras_primarias": [
      "15-20 palavras-chave REAIS identificadas na pesquisa"
    ],
    "palavras_secundarias": [
      "25-35 palavras-chave REAIS secundárias encontradas"
    ],
    "long_tail": [
      "30-50 palavras-chave REAIS de cauda longa específicas"
    ],
    "oportunidades_seo": "Oportunidades REAIS específicas identificadas"
  }},
  
  "insights_exclusivos": [
    "Lista de 20-30 insights ULTRA-ESPECÍFICOS e REAIS baseados EXCLUSIVAMENTE nos dados da pesquisa"
  ]
}}
```

CRÍTICO: Use APENAS dados REAIS da pesquisa. NUNCA invente, simule ou use templates.
Se não houver dados suficientes para uma seção, OMITA completamente.
"""
        
        return prompt
    
    def _process_ai_response_ultra_strict(self, ai_response: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta da IA com validação ultra-rigorosa"""
        
        try:
            # Extrai JSON
            clean_text = ai_response.strip()
            
            if "```json" in clean_text:
                start = clean_text.find("```json") + 7
                end = clean_text.rfind("```")
                clean_text = clean_text[start:end].strip()
            elif "```" in clean_text:
                start = clean_text.find("```") + 3
                end = clean_text.rfind("```")
                clean_text = clean_text[start:end].strip()
            
            # Parse JSON
            analysis = json.loads(clean_text)
            
            # VALIDAÇÃO ULTRA-RIGOROSA
            validation_result = self._validate_ai_content_ultra_strict(analysis)
            
            if not validation_result['valid']:
                raise Exception(f"IA RETORNOU DADOS INVÁLIDOS: {validation_result['errors']}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON inválido da IA: {str(e)}")
            raise Exception("IA RETORNOU JSON INVÁLIDO: Não foi possível processar resposta")
    
    def _validate_ai_content_ultra_strict(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validação ultra-rigorosa do conteúdo da IA"""
        
        errors = []
        
        # Verifica estrutura obrigatória
        required_sections = ['avatar_ultra_detalhado', 'escopo', 'insights_exclusivos']
        
        for section in required_sections:
            if section not in analysis:
                errors.append(f"Seção obrigatória ausente: {section}")
                continue
            
            if not analysis[section]:
                errors.append(f"Seção obrigatória vazia: {section}")
        
        # Validação específica do avatar
        if 'avatar_ultra_detalhado' in analysis:
            avatar = analysis['avatar_ultra_detalhado']
            
            if not avatar.get('perfil_demografico'):
                errors.append("Perfil demográfico ausente no avatar")
            
            dores = avatar.get('dores_viscerais', [])
            if not dores or len(dores) < 8:
                errors.append(f"Dores insuficientes: {len(dores)} < 8")
            
            desejos = avatar.get('desejos_secretos', [])
            if not desejos or len(desejos) < 8:
                errors.append(f"Desejos insuficientes: {len(desejos)} < 8")
        
        # Validação dos insights
        if 'insights_exclusivos' in analysis:
            insights = analysis['insights_exclusivos']
            
            if not insights or len(insights) < 15:
                errors.append(f"Insights insuficientes: {len(insights) if insights else 0} < 15")
            
            # CORREÇÃO: Validação rigorosa de profundidade dos insights
            if insights:
                superficial_count = 0
                for insight in insights:
                    if (len(insight) < 50 or 
                        'superficial' in insight.lower() or
                        'genérico' in insight.lower() or
                        'baseado em' in insight.lower()):
                        superficial_count += 1
                
                if superficial_count > len(insights) * 0.2:  # Máximo 20% superficiais
                    errors.append(f"Muitos insights superficiais: {superficial_count}/{len(insights)}")
        
        # Verifica indicadores de simulação
        analysis_str = json.dumps(analysis, ensure_ascii=False).lower()
        
        forbidden_phrases = [
            'customizado para', 'baseado em', 'específico para', 'exemplo de',
            'n/a', 'não informado', 'dados não disponíveis', 'informação não encontrada'
        ]
        
        found_forbidden = []
        for phrase in forbidden_phrases:
            if phrase in analysis_str:
                found_forbidden.append(phrase)
        
        if found_forbidden:
            errors.append(f"Frases proibidas encontradas: {found_forbidden[:3]}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'quality_score': max(0, 100 - (len(errors) * 15))
        }
    
    def _validate_ai_response_strict(self, ai_analysis: Dict[str, Any]) -> bool:
        """Validação rigorosa da resposta da IA"""
        
        validation = self._validate_ai_content_ultra_strict(ai_analysis)
        return validation['valid']
    
    def _generate_strict_mental_drivers(self, ai_analysis: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera drivers mentais com critérios rigorosos"""
        
        try:
            avatar_data = ai_analysis.get('avatar_ultra_detalhado', {})
            
            if not avatar_data or not avatar_data.get('dores_viscerais'):
                return {
                    'success': False,
                    'error': 'Avatar insuficiente para gerar drivers mentais'
                }
            
            drivers_system = mental_drivers_architect.generate_complete_drivers_system(avatar_data, data)
            
            # Validação rigorosa dos drivers
            if not self._validate_drivers_strict(drivers_system):
                return {
                    'success': False,
                    'error': 'Drivers gerados não atendem critérios de qualidade'
                }
            
            return {
                'success': True,
                'data': drivers_system
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_strict_visual_proofs(self, ai_analysis: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera provas visuais com critérios rigorosos"""
        
        try:
            avatar_data = ai_analysis.get('avatar_ultra_detalhado', {})
            
            # Extrai conceitos para prova
            concepts = self._extract_proof_concepts_strict(ai_analysis, data)
            
            if not concepts or len(concepts) < 5:
                return {
                    'success': False,
                    'error': 'Conceitos insuficientes para provas visuais'
                }
            
            visual_proofs = visual_proofs_generator.generate_complete_proofs_system(concepts, avatar_data, data)
            
            # Validação rigorosa das provas
            if not self._validate_visual_proofs_strict(visual_proofs):
                return {
                    'success': False,
                    'error': 'Provas visuais não atendem critérios de qualidade'
                }
            
            return {
                'success': True,
                'data': visual_proofs
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_strict_anti_objection(self, ai_analysis: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sistema anti-objeção com critérios rigorosos"""
        
        try:
            avatar_data = ai_analysis.get('avatar_ultra_detalhado', {})
            objections = avatar_data.get('objecoes_reais', [])
            
            if not objections or len(objections) < 5:
                return {
                    'success': False,
                    'error': 'Objeções insuficientes para sistema anti-objeção'
                }
            
            anti_objection_system_result = anti_objection_system.generate_complete_anti_objection_system(
                objections, avatar_data, data
            )
            
            # Validação rigorosa do sistema
            if not self._validate_anti_objection_strict(anti_objection_system_result):
                return {
                    'success': False,
                    'error': 'Sistema anti-objeção não atende critérios de qualidade'
                }
            
            return {
                'success': True,
                'data': anti_objection_system_result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_corrected_pre_pitch(
        self, 
        advanced_components: Dict[str, Any], 
        ai_analysis: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera pré-pitch usando versão corrigida"""
        
        try:
            drivers_data = advanced_components.get('drivers_mentais_customizados', {})
            avatar_data = ai_analysis.get('avatar_ultra_detalhado', {})
            
            # Usa o arquiteto aprimorado
            pre_pitch_system = enhanced_pre_pitch_architect.generate_enhanced_pre_pitch_system(
                drivers_data, avatar_data, data
            )
            
            # Validação rigorosa do pré-pitch
            if not self._validate_pre_pitch_strict(pre_pitch_system):
                return {
                    'success': False,
                    'error': 'Pré-pitch não atende critérios de qualidade'
                }
            
            return {
                'success': True,
                'data': pre_pitch_system
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_strict_future_predictions(self, data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera predições do futuro com critérios rigorosos"""
        
        try:
            future_predictions = future_prediction_engine.predict_market_future(
                data.get('segmento', 'negócios'), data, horizon_months=36
            )
            
            # Validação das predições
            if not self._validate_future_predictions_strict(future_predictions):
                return {
                    'success': False,
                    'error': 'Predições não atendem critérios de qualidade'
                }
            
            return {
                'success': True,
                'data': future_predictions
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _consolidate_strict_analysis(
        self,
        data: Dict[str, Any],
        research_data: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        advanced_components: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Consolida análise com critérios rigorosos"""
        
        consolidated = {
            "projeto_dados": data,
            "pesquisa_web_massiva": {
                "estatisticas": research_data.get('statistics', {}),
                "quality_validation": research_data.get('quality_validation', {}),
                "layer_performance": research_data.get('layer_performance', {}),
                "fontes": [
                    {
                        'url': content.get('url', ''),
                        'title': content.get('search_title', ''),
                        'quality_score': content.get('quality_validation', {}).get('score', 0),
                        'extraction_method': content.get('extraction_strategy', '')
                    }
                    for content in research_data.get('extracted_content', [])
                    if content['success']
                ]
            },
            **ai_analysis,  # Inclui avatar, escopo, etc.
            **advanced_components,  # Inclui todos os componentes avançados
            "consolidacao_timestamp": datetime.now().isoformat(),
            "strict_validation_passed": True,
            "simulation_free_certified": True,
            "fallback_free_certified": True
        }
        
        return consolidated
    
    def _validate_final_analysis_ultra_strict(self, final_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validação final ultra-rigorosa"""
        
        errors = []
        warnings = []
        
        # Verifica componentes obrigatórios
        required_components = [
            'projeto_dados', 'pesquisa_web_massiva', 'avatar_ultra_detalhado',
            'escopo', 'insights_exclusivos', 'drivers_mentais_customizados',
            'provas_visuais_sugeridas', 'sistema_anti_objecao', 'pre_pitch_invisivel'
        ]
        
        for component in required_components:
            if component not in final_analysis:
                errors.append(f"Componente obrigatório ausente: {component}")
            elif not final_analysis[component]:
                errors.append(f"Componente obrigatório vazio: {component}")
        
        # Verifica qualidade da pesquisa
        pesquisa_stats = final_analysis.get('pesquisa_web_massiva', {}).get('estatisticas', {})
        
        if pesquisa_stats.get('successful_extractions', 0) < self.strict_quality_thresholds['min_sources']:
            errors.append("Pesquisa com fontes insuficientes")
        
        if pesquisa_stats.get('total_content_length', 0) < self.strict_quality_thresholds['min_content_length']:
            errors.append("Pesquisa com conteúdo insuficiente")
        
        # Verifica qualidade dos insights
        insights = final_analysis.get('insights_exclusivos', [])
        if len(insights) < 15:
            errors.append(f"Insights insuficientes: {len(insights)} < 15")
        
        # Calcula score de qualidade
        quality_score = 100 - (len(errors) * 10) - (len(warnings) * 5)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'quality_score': max(quality_score, 0),
            'components_validated': len(required_components) - len(errors)
        }
    
    def _generate_intelligent_main_query(self, data: Dict[str, Any]) -> str:
        """Gera query principal inteligente"""
        
        segmento = data.get('segmento', '')
        produto = data.get('produto', '')
        
        if produto:
            return f"mercado {segmento} {produto} Brasil 2024 análise dados estatísticas oportunidades"
        else:
            return f"análise mercado {segmento} Brasil 2024 dados estatísticas crescimento tendências"
    
    def _extract_proof_concepts_strict(self, ai_analysis: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
        """Extrai conceitos para prova com critérios rigorosos"""
        
        concepts = []
        
        # Extrai do avatar
        avatar = ai_analysis.get('avatar_ultra_detalhado', {})
        
        dores = avatar.get('dores_viscerais', [])
        if dores:
            concepts.extend(dores[:6])  # Top 6 dores
        
        desejos = avatar.get('desejos_secretos', [])
        if desejos:
            concepts.extend(desejos[:6])  # Top 6 desejos
        
        # Extrai do escopo
        escopo = ai_analysis.get('escopo', {})
        diferenciais = escopo.get('diferenciais_competitivos', [])
        if diferenciais:
            concepts.extend(diferenciais[:4])  # Top 4 diferenciais
        
        # Filtra conceitos válidos (não genéricos)
        valid_concepts = []
        for concept in concepts:
            if (concept and 
                len(concept) > 30 and 
                not any(forbidden in concept.lower() for forbidden in [
                    'customizado para', 'baseado em', 'específico para', 'exemplo de'
                ])):
                valid_concepts.append(concept)
        
        return valid_concepts[:12]  # Máximo 12 conceitos
    
    def _validate_drivers_strict(self, drivers_system: Dict[str, Any]) -> bool:
        """Validação rigorosa dos drivers"""
        
        if not drivers_system or drivers_system.get('fallback_mode'):
            return False
        
        drivers = drivers_system.get('drivers_customizados', [])
        if not drivers or len(drivers) < 3:
            return False
        
        # Verifica cada driver
        for driver in drivers:
            if not isinstance(driver, dict):
                return False
            
            if not driver.get('nome') or len(driver['nome']) < 10:
                return False
            
            roteiro = driver.get('roteiro_ativacao', {})
            if not roteiro or not roteiro.get('historia_analogia'):
                return False
            
            historia = roteiro['historia_analogia']
            if len(historia) < 150:
                return False
            
            # Verifica se não é genérica
            if any(forbidden in historia.lower() for forbidden in [
                'customizado para', 'história customizada', 'baseado em'
            ]):
                return False
        
        return True
    
    def _validate_visual_proofs_strict(self, visual_proofs: List[Dict[str, Any]]) -> bool:
        """Validação rigorosa das provas visuais"""
        
        if not visual_proofs or len(visual_proofs) < 3:
            return False
        
        for proof in visual_proofs:
            if not isinstance(proof, dict):
                return False
            
            if not proof.get('nome') or not proof.get('experimento'):
                return False
            
            if len(proof.get('experimento', '')) < 100:
                return False
            
            materiais = proof.get('materiais', [])
            if not materiais or len(materiais) < 3:
                return False
        
        return True
    
    def _validate_anti_objection_strict(self, anti_objection_system: Dict[str, Any]) -> bool:
        """Validação rigorosa do sistema anti-objeção"""
        
        if not anti_objection_system or anti_objection_system.get('fallback_mode'):
            return False
        
        objecoes_universais = anti_objection_system.get('objecoes_universais', {})
        if not objecoes_universais or len(objecoes_universais) < 3:
            return False
        
        scripts = anti_objection_system.get('scripts_personalizados', {})
        if not scripts or len(scripts) < 3:
            return False
        
        return True
    
    def _validate_pre_pitch_strict(self, pre_pitch_system: Dict[str, Any]) -> bool:
        """Validação rigorosa do pré-pitch"""
        
        if not pre_pitch_system or pre_pitch_system.get('status') == 'EMERGENCY_MODE':
            return False
        
        orchestration = pre_pitch_system.get('orquestracao_emocional', {})
        if not orchestration:
            return False
        
        scripts = pre_pitch_system.get('roteiros_detalhados', {})
        if not scripts or len(scripts) < 3:
            return False
        
        # Verifica se não é fallback
        if pre_pitch_system.get('fallback_mode'):
            return False
        
        return True
    
    def _validate_future_predictions_strict(self, future_predictions: Dict[str, Any]) -> bool:
        """Validação rigorosa das predições"""
        
        if not future_predictions:
            return False
        
        required_sections = ['tendencias_atuais', 'cenarios_futuros', 'oportunidades_emergentes']
        
        for section in required_sections:
            if section not in future_predictions:
                return False
            
            if not future_predictions[section]:
                return False
        
        return True

# Instância global corrigida
corrected_ultra_detailed_analysis_engine = CorrectedUltraDetailedAnalysisEngine()