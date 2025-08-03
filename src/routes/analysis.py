#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Rotas de Análise
Endpoints para análise de mercado ultra-detalhada
"""

import os
import logging
import time
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, session, send_file
from services.enhanced_analysis_pipeline import enhanced_analysis_pipeline
from services.quality_assurance_manager import quality_assurance_manager
from services.ai_manager import ai_manager
from services.production_search_manager import production_search_manager
from services.attachment_service import attachment_service
from database import db_manager
from routes.progress import get_progress_tracker, update_analysis_progress
from services.auto_save_manager import auto_save_manager, salvar_etapa, salvar_erro
from services.consolidated_report_generator import consolidated_report_generator
from services.gemini_2_5_client import gemini_25_client

logger = logging.getLogger(__name__)

# Cria blueprint
analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_market():
    """Endpoint principal para análise de mercado"""
    
    try:
        start_time = time.time()
        logger.info("🚀 Iniciando análise de mercado aprimorada")
        
        # Coleta dados da requisição
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Dados não fornecidos',
                'message': 'Envie os dados da análise no corpo da requisição'
            }), 400
        
        # Validação básica
        if not data.get('segmento'):
            return jsonify({
                'error': 'Segmento obrigatório',
                'message': 'O campo "segmento" é obrigatório para análise'
            }), 400
        
        # Adiciona session_id se não fornecido
        if not data.get('session_id'):
            data['session_id'] = f"session_{int(time.time())}_{os.urandom(4).hex()}"
        
        # Inicia sessão de salvamento automático
        session_id = data['session_id']
        auto_save_manager.iniciar_sessao(session_id)
        
        # Salva dados de entrada imediatamente
        salvar_etapa("requisicao_analise", {
            "input_data": data,
            "timestamp": datetime.now().isoformat(),
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', '')
        }, categoria="analise_completa")
        
        # Inicia rastreamento de progresso
        progress_tracker = get_progress_tracker(session_id)
        
        # Função de callback para progresso
        def progress_callback(step: int, message: str, details: str = None):
            update_analysis_progress(session_id, step, message, details)
            # Salva progresso também
            salvar_etapa("progresso", {
                "step": step,
                "message": message,
                "details": details
            }, categoria="logs")
        
        # Log dos dados recebidos
        logger.info(f"📊 Dados recebidos: Segmento={data.get('segmento')}, Produto={data.get('produto')}")
        
        # Prepara query de pesquisa se não fornecida
        if not data.get('query'):
            segmento = data.get('segmento', '')
            produto = data.get('produto', '')
            if produto:
                data['query'] = f"mercado {segmento} {produto} Brasil tendências oportunidades 2024"
            else:
                data['query'] = f"análise mercado {segmento} Brasil dados estatísticas crescimento"
        
        logger.info(f"🔍 Query de pesquisa: {data['query']}")
        
        # Salva query preparada
        salvar_etapa("query_preparada", {"query": data['query']}, categoria="pesquisa_web")
        
        # Executa análise aprimorada com pipeline
        logger.info("🚀 Executando análise aprimorada...")
        try:
            # Usa o pipeline aprimorado com Gemini 2.5 Pro
            analysis_result = enhanced_analysis_pipeline.execute_complete_analysis(
                data,
                session_id=session_id,
                progress_callback=progress_callback
            )
            
            # Salva resultado da análise imediatamente
            salvar_etapa("analise_resultado", analysis_result, categoria="analise_completa")
            
            # Gera relatórios consolidados
            if progress_callback:
                progress_callback(11, "📊 Gerando relatórios consolidados...")
            
            consolidated_reports = consolidated_report_generator.generate_consolidated_reports(
                analysis_result, session_id
            )
            
            # Adiciona informações dos relatórios ao resultado
            analysis_result['relatorios_consolidados'] = consolidated_reports
            
            # Validação de qualidade ultra-rigorosa
            logger.info("🔍 Executando garantia de qualidade...")
            quality_validation = quality_assurance_manager.validate_complete_analysis(analysis_result)
            
            # Salva validação
            salvar_etapa("validacao_qualidade", quality_validation, categoria="analise_completa")
            
            if not quality_validation['valid']:
                logger.error(f"❌ Análise rejeitada: {quality_validation['errors']}")
                salvar_erro("validacao_falha", Exception("Análise rejeitada por baixa qualidade"), contexto=quality_validation)
                
                # Consolida dados parciais
                dados_parciais = auto_save_manager.consolidar_sessao(session_id)
                
                return jsonify({
                    'error': 'Análise de baixa qualidade rejeitada',
                    'message': 'Análise não atende critérios de qualidade ultra-rigorosos',
                    'quality_report': quality_validation,
                    'recommendations': quality_validation['recommendations'],
                    'dados_parciais': dados_parciais,
                    'session_id': session_id,
                    'timestamp': datetime.now().isoformat()
                }), 422
            
            # Remove dados brutos do relatório final
            clean_analysis = quality_assurance_manager.filter_raw_data_comprehensive(analysis_result)
            
            # Adiciona informações dos relatórios consolidados
            clean_analysis['relatorios_consolidados'] = analysis_result.get('relatorios_consolidados', {})
            
            # Salva análise limpa
            salvar_etapa("analise_limpa", clean_analysis, categoria="analise_completa")
            
            logger.info(f"✅ Análise validada com score {quality_validation['quality_score']:.1f}%")
            
        except Exception as e:
            logger.error(f"❌ Pipeline de análise falhou: {str(e)}")
            salvar_erro("pipeline_analise", e, contexto=data)
            
            # Recupera dados salvos automaticamente
            try:
                dados_recuperados = auto_save_manager.consolidar_sessao(session_id)
                logger.info(f"🔄 Dados recuperados automaticamente: {dados_recuperados}")
                
                return jsonify({
                    'error': 'Pipeline falhou mas dados preservados',
                    'message': str(e),
                    'dados_preservados': True,
                    'session_id': session_id,
                    'relatorio_parcial': dados_recuperados,
                    'timestamp': datetime.now().isoformat(),
                    'recommendation': 'Dados preservados - configure APIs e tente novamente'
                }), 206  # Partial Content
                
            except Exception as recovery_error:
                logger.error(f"❌ Falha na recuperação automática: {recovery_error}")
            
            return jsonify({
                'error': 'Falha crítica na análise',
                'message': str(e),
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Configure APIs e execute novamente',
                'session_id': session_id,
                'dados_preservados': f'Verifique relatorios_intermediarios/{session_id}',
                'debug_info': {
                    'input_data': {
                        'segmento': data.get('segmento'),
                        'produto': data.get('produto'),
                        'query': data.get('query')
                    },
                    'ai_status': ai_manager.get_provider_status(),
                    'search_status': production_search_manager.get_provider_status()
                }
            }), 500
        
        # Verifica se a análise foi bem-sucedida
        if not clean_analysis or not isinstance(clean_analysis, dict):
            logger.error("❌ Análise limpa inválida")
            salvar_erro("analise_limpa_invalida", Exception("Análise limpa inválida"))
            return jsonify({
                'error': 'Análise final inválida',
                'message': 'Falha na limpeza da análise',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'recommendation': 'Verifique logs e tente novamente'
            }), 500
        
        # Marca progresso como completo
        progress_tracker.complete()
        
        # Salva no banco de dados
        try:
            logger.info("💾 Salvando análise no banco de dados...")
            db_record = db_manager.create_analysis({
                'segmento': data.get('segmento'),
                'produto': data.get('produto'),
                'publico': data.get('publico'),
                'preco': data.get('preco'),
                'objetivo_receita': data.get('objetivo_receita'),
                'orcamento_marketing': data.get('orcamento_marketing'),
                'prazo_lancamento': data.get('prazo_lancamento'),
                'concorrentes': data.get('concorrentes'),
                'dados_adicionais': data.get('dados_adicionais'),
                'query': data.get('query'),
                'status': 'completed',
                'session_id': session_id,
                **clean_analysis  # Inclui análise limpa
            })
            
            if db_record:
                if db_record.get('local_only'):
                    clean_analysis['local_only'] = True
                    clean_analysis['local_files'] = db_record.get('local_files')
                    logger.info(f"✅ Análise salva localmente: {len(db_record['local_files']['files'])} arquivos")
                else:
                    clean_analysis['database_id'] = db_record['id']
                    clean_analysis['local_files'] = db_record.get('local_files')
                    logger.info(f"✅ Análise salva: Supabase ID {db_record['id']} + arquivos locais")
                
                # Salva confirmação do banco
                salvar_etapa("banco_salvo", {
                    "database_id": db_record.get('id'),
                    "local_files": db_record.get('local_files', {})
                }, categoria="analise_completa")
            else:
                logger.warning("⚠️ Falha ao salvar análise")
                salvar_erro("banco_falha", Exception("Falha ao salvar no banco"))
                clean_analysis['database_warning'] = "Falha ao salvar no banco"
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar no banco: {str(e)}")
            salvar_erro("banco_erro", e)
            clean_analysis['database_warning'] = f"Erro no banco: {str(e)}"
        
        # Consolida sessão final
        try:
            relatorio_consolidado = auto_save_manager.consolidar_sessao(session_id)
            clean_analysis['relatorio_consolidado'] = relatorio_consolidado
            logger.info(f"📋 Relatório consolidado gerado: {relatorio_consolidado}")
        except Exception as e:
            logger.error(f"❌ Erro ao consolidar sessão: {e}")
        
        # Calcula tempo de processamento
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Adiciona metadados finais
        if 'metadata' not in clean_analysis:
            clean_analysis['metadata'] = {}
        
        clean_analysis['metadata'].update({
            'processing_time_seconds': processing_time,
            'processing_time_formatted': f"{int(processing_time // 60)}m {int(processing_time % 60)}s",
            'request_timestamp': datetime.now().isoformat(),
            'session_id': data.get('session_id'),
            'pipeline_version': '2.0_enhanced',
            'quality_assured': True,
            'raw_data_filtered': True,
            'simulation_free': True,
            'input_data': {
                'segmento': data.get('segmento'),
                'produto': data.get('produto'),
                'query': data.get('query')
            },
            'quality_score': quality_validation.get('quality_score', 0)
        })
        
        # Salva resposta final
        salvar_etapa("resposta_final", clean_analysis, categoria="analise_completa")
        
        logger.info(f"✅ Análise concluída em {processing_time:.2f} segundos")
        
        return jsonify(clean_analysis)
        
    except Exception as e:
        logger.error(f"❌ Erro crítico na análise: {str(e)}", exc_info=True)
        
        # Remove progresso em caso de erro
        try:
            if 'session_id' in locals() and session_id in get_progress_tracker.__globals__.get('progress_sessions', {}):
                del get_progress_tracker.__globals__['progress_sessions'][session_id]
        except:
            pass  # Ignora erros de limpeza
        
        return jsonify({
            'error': 'Erro na análise',
            'message': str(e),
            'timestamp': datetime.now().isoformat(),
            'recommendation': 'Configure todas as APIs necessárias antes de tentar novamente',
            'session_id': locals().get('session_id', 'unknown'),
            'debug_info': {
                'input_data': {
                    'segmento': data.get('segmento') if 'data' in locals() else 'unknown',
                    'produto': data.get('produto') if 'data' in locals() else 'unknown'
                },
                'ai_status': ai_manager.get_provider_status(),
                'search_status': production_search_manager.get_provider_status()
            }
        }), 500

@analysis_bp.route('/status', methods=['GET'])
def get_analysis_status():
    """Retorna status dos sistemas de análise"""
    
    try:
        # Status dos provedores de IA
        ai_status = ai_manager.get_provider_status()
        
        # Status dos provedores de busca
        search_status = production_search_manager.get_provider_status()
        
        # Status do banco de dados
        db_status = db_manager.test_connection()
        
        # Status geral
        total_ai_available = len([p for p in ai_status.values() if p['available']])
        total_search_available = len([p for p in search_status.values() if p['available']])
        
        overall_status = "healthy" if (total_ai_available > 0 and total_search_available > 0 and db_status) else "degraded"
        
        return jsonify({
            'status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'systems': {
                'ai_providers': {
                    'status': 'healthy' if total_ai_available > 0 else 'error',
                    'available_count': total_ai_available,
                    'total_count': len(ai_status),
                    'providers': ai_status
                },
                'search_providers': {
                    'status': 'healthy' if total_search_available > 0 else 'error',
                    'available_count': total_search_available,
                    'total_count': len(search_status),
                    'providers': search_status
                },
                'database': {
                    'status': 'healthy' if db_status else 'error',
                    'connected': db_status
                },
                'content_extraction': {
                    'status': 'healthy',
                    'available': True
                }
            },
            'capabilities': {
                'multi_ai_fallback': total_ai_available > 1,
                'multi_search_fallback': total_search_available > 1,
                'real_time_search': total_search_available > 0,
                'content_extraction': True,
                'database_storage': db_status
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@analysis_bp.route('/reset_providers', methods=['POST'])
def reset_providers():
    """Reset contadores de erro dos provedores"""
    
    try:
        data = request.get_json() or {}
        provider_type = data.get('type')  # 'ai' ou 'search'
        provider_name = data.get('provider')  # nome específico do provedor
        
        if provider_type == 'ai':
            ai_manager.reset_provider_errors(provider_name)
            message = f"Reset erros do provedor de IA: {provider_name}" if provider_name else "Reset erros de todos os provedores de IA"
        elif provider_type == 'search':
            production_search_manager.reset_provider_errors(provider_name)
            message = f"Reset erros do provedor de busca: {provider_name}" if provider_name else "Reset erros de todos os provedores de busca"
        else:
            # Reset todos
            ai_manager.reset_provider_errors()
            production_search_manager.reset_provider_errors()
            message = "Reset erros de todos os provedores"
        
        logger.info(f"🔄 {message}")
        
        return jsonify({
            'success': True,
            'message': message,
            'ai_status': ai_manager.get_provider_status(),
            'search_status': production_search_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao resetar provedores: {str(e)}")
        return jsonify({
            'error': 'Erro ao resetar provedores',
            'message': str(e)
        }), 500

@analysis_bp.route('/test_search', methods=['POST'])
def test_search():
    """Testa sistema de busca"""
    
    try:
        data = request.get_json()
        query = data.get('query', 'teste mercado digital Brasil')
        max_results = min(int(data.get('max_results', 5)), 10)
        
        logger.info(f"🧪 Testando busca: {query}")
        
        # Testa busca
        results = production_search_manager.search_with_fallback(query, max_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'results_count': len(results),
            'results': results,
            'provider_status': production_search_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no teste de busca: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de busca',
            'message': str(e)
        }), 500

@analysis_bp.route('/test_extraction', methods=['POST'])
def test_extraction():
    """Testa sistema de extração de conteúdo"""
    
    try:
        data = request.get_json()
        test_url = data.get('url', 'https://g1.globo.com/tecnologia/')
        
        logger.info(f"🧪 Testando extração: {test_url}")
        
        # Importa extrator de produção
        from services.production_content_extractor import production_content_extractor
        
        # Testa extração segura
        extraction_result = production_content_extractor.safe_extract_content(test_url)
        
        if extraction_result['success']:
            return jsonify({
                'success': True,
                'url': test_url,
                'content_length': extraction_result['metadata']['content_length'],
                'content_preview': extraction_result['content'][:500] + '...' if len(extraction_result['content']) > 500 else extraction_result['content'],
                'validation': extraction_result['validation'],
                'metadata': extraction_result['metadata'],
                'extractor_stats': production_content_extractor.get_extraction_stats(),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'url': test_url,
                'error': extraction_result['error'],
                'metadata': extraction_result['metadata'],
                'extractor_stats': production_content_extractor.get_extraction_stats(),
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Erro no teste de extração: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de extração',
            'message': str(e)
        }), 500

@analysis_bp.route('/extractor_stats', methods=['GET'])
def get_extractor_stats():
    """Obtém estatísticas dos extratores"""
    
    try:
        from services.production_content_extractor import production_content_extractor
        stats = production_content_extractor.get_extraction_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas dos extratores',
            'message': str(e)
        }), 500

@analysis_bp.route('/reset_extractors', methods=['POST'])
def reset_extractors():
    """Reset estatísticas dos extratores"""
    
    try:
        data = request.get_json() or {}
        extractor_name = data.get('extractor')
        
        # Import serviços
        from services.production_content_extractor import production_content_extractor
        
        production_content_extractor.reset_extractor_stats(extractor_name)
        
        message = f"Reset estatísticas do extrator: {extractor_name}" if extractor_name else "Reset estatísticas de todos os extratores"
        
        return jsonify({
            'success': True,
            'message': message,
            'stats': production_content_extractor.get_extraction_stats(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao resetar extratores: {str(e)}")
        return jsonify({
            'error': 'Erro ao resetar extratores',
            'message': str(e)
        }), 500

@analysis_bp.route('/validate_analysis', methods=['POST'])
def validate_analysis():
    """Valida qualidade de uma análise"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados da análise não fornecidos'
            }), 400
        
        # Valida análise
        validation_result = quality_assurance_manager.validate_complete_analysis(data)
        
        # Gera relatório
        quality_report = quality_assurance_manager.generate_quality_report(data)
        
        return jsonify({
            'validation': validation_result,
            'quality_report': quality_report,
            'can_generate_pdf': quality_assurance_manager.should_generate_pdf(data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na validação: {str(e)}")
        return jsonify({
            'error': 'Erro na validação da análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/analyze_simple', methods=['POST'])
def analyze_simple():
    """Endpoint alternativo mais simples para análise"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['segmento', 'produto', 'publico']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos obrigatórios: {", ".join(missing_fields)}'
            }), 400
        
        logger.info(f"🚀 Iniciando análise: {data.get('segmento')} - {data.get('produto')}")
        
        # Usar o engine de análise existente
        from services.enhanced_analysis_engine import enhanced_analysis_engine
        
        # Gerar análise completa
        analysis_result = enhanced_analysis_engine.generate_complete_analysis(data)
        
        if not analysis_result:
            return jsonify({
                'success': False,
                'error': 'Falha na geração da análise'
            }), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@analysis_bp.route('/test_ai', methods=['POST'])
def test_ai():
    """Testa sistema de IA"""
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Gere um breve resumo sobre o mercado digital brasileiro em 2024.')
        
        logger.info("🧪 Testando Gemini 2.5 Pro...")
        
        # Testa Gemini 2.5 Pro primeiro
        if gemini_25_client.is_available():
            try:
                response = gemini_25_client.generate_ultra_analysis(prompt, max_tokens=500)
                provider_used = 'gemini-2.5-pro'
            except Exception as e:
                logger.warning(f"⚠️ Gemini 2.5 Pro falhou: {e}")
                # Fallback para sistema padrão
                response = ai_manager.generate_analysis(prompt, max_tokens=500)
                provider_used = 'fallback_system'
        else:
            response = ai_manager.generate_analysis(prompt, max_tokens=500)
            provider_used = 'fallback_system'
        
        return jsonify({
            'success': bool(response),
            'prompt': prompt,
            'response': response,
            'response_length': len(response) if response else 0,
            'provider_used': provider_used,
            'gemini_25_available': gemini_25_client.is_available(),
            'provider_status': ai_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no teste de IA: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de IA',
            'message': str(e)
        }), 500

@analysis_bp.route('/upload_attachment', methods=['POST'])
def upload_attachment():
    """Upload e processamento de anexos"""
    
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400
        
        file = request.files['file']
        session_id = request.form.get('session_id', f"session_{int(time.time())}")
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nome de arquivo vazio'
            }), 400
        
        # Processa anexo
        result = attachment_service.process_attachment(file, session_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro no upload de anexo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno no processamento do anexo',
            'message': str(e)
        }), 500

@analysis_bp.route('/list_analyses', methods=['GET'])
def list_analyses():
    """Lista análises salvas"""
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        analyses = db_manager.list_analyses(limit, offset)
        
        return jsonify({
            'success': True,
            'analyses': analyses,
            'count': len(analyses),
            'limit': limit,
            'offset': offset,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar análises: {str(e)}")
        return jsonify({
            'error': 'Erro ao listar análises',
            'message': str(e)
        }), 500

@analysis_bp.route('/get_analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Obtém análise específica"""
    
    try:
        analysis = db_manager.get_analysis(analysis_id)
        
        if analysis:
            return jsonify({
                'success': True,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Análise não encontrada'
            }), 404
            
    except Exception as e:
        logger.error(f"Erro ao obter análise {analysis_id}: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Obtém estatísticas do sistema"""
    
    try:
        db_stats = db_manager.get_stats()
        ai_status = ai_manager.get_provider_status()
        search_status = production_search_manager.get_provider_status()
        
        return jsonify({
            'database_stats': db_stats,
            'ai_providers': ai_status,
            'search_providers': search_status,
            'system_health': {
                'ai_available': len([p for p in ai_status.values() if p['available']]),
                'search_available': len([p for p in search_status.values() if p['available']]),
                'database_connected': db_manager.test_connection()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas',
            'message': str(e)
        }), 500

@analysis_bp.route('/download_consolidated_report/<report_type>/<session_id>', methods=['GET'])
def download_consolidated_report(report_type, session_id):
    """Download de relatório consolidado específico"""
    
    try:
        from pathlib import Path
        
        reports_dir = Path("relatorios_consolidados")
        
        # Busca arquivo do relatório
        pattern = f"analise_{session_id[:8]}*_{report_type}.*"
        matching_files = list(reports_dir.glob(pattern))
        
        if not matching_files:
            return jsonify({
                'error': 'Relatório não encontrado',
                'report_type': report_type,
                'session_id': session_id
            }), 404
        
        # Pega o arquivo mais recente
        latest_file = max(matching_files, key=lambda f: f.stat().st_mtime)
        
        return send_file(
            latest_file,
            as_attachment=True,
            download_name=latest_file.name
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao baixar relatório: {e}")
        return jsonify({
            'error': 'Erro ao baixar relatório',
            'message': str(e)
        }), 500

@analysis_bp.route('/list_consolidated_reports/<session_id>', methods=['GET'])
def list_consolidated_reports(session_id):
    """Lista relatórios consolidados de uma sessão"""
    
    try:
        from pathlib import Path
        
        reports_dir = Path("relatorios_consolidados")
        
        if not reports_dir.exists():
            return jsonify({
                'reports': [],
                'total': 0,
                'session_id': session_id
            })
        
        # Busca relatórios da sessão
        pattern = f"analise_{session_id[:8]}*"
        matching_files = list(reports_dir.glob(pattern))
        
        reports = []
        for file_path in matching_files:
            reports.append({
                'name': file_path.name,
                'type': _extract_report_type(file_path.name),
                'size': file_path.stat().st_size,
                'created': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                'download_url': f"/api/download_consolidated_report/{_extract_report_type(file_path.name)}/{session_id}"
            })
        
        # Ordena por data de criação
        reports.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'reports': reports,
            'total': len(reports),
            'session_id': session_id,
            'reports_directory': str(reports_dir)
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar relatórios: {e}")
        return jsonify({
            'error': 'Erro ao listar relatórios',
            'message': str(e)
        }), 500

def _extract_report_type(filename: str) -> str:
    """Extrai tipo de relatório do nome do arquivo"""
    if 'executivo' in filename:
        return 'executive'
    elif 'tecnico' in filename:
        return 'technical'
    elif 'implementacao' in filename:
        return 'implementation'
    elif 'dashboard' in filename:
        return 'dashboard'
    elif 'insights' in filename:
        return 'insights'
    elif 'roi' in filename:
        return 'roi'
    elif 'contingencia' in filename:
        return 'contingency'
    elif 'monitoramento' in filename:
        return 'monitoring'
    elif 'indice' in filename:
        return 'index'
    else:
        return 'unknown'