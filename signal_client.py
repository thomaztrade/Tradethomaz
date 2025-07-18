#!/usr/bin/env python3
"""
ThomazTrade Signal Client
Utility for sending trading signals to the ThomazTrade API
"""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

class ThomazTradeClient:
    """Client for interacting with ThomazTrade API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        
    def enviar_sinal_api(self, ativo: str, direcao: str, horario: str, 
                        preco: Optional[float] = None, 
                        confianca: Optional[float] = None,
                        indicadores: Optional[list] = None,
                        detalhes: Optional[str] = None) -> bool:
        """
        Envia sinal de trading para a API
        
        Args:
            ativo: Nome do ativo (ex: BTC/USD, PETR4)
            direcao: 'compra' ou 'venda'
            horario: Horário do sinal (ex: '14:30')
            preco: Preço opcional
            confianca: Nível de confiança (0-100)
            indicadores: Lista de indicadores usados
            detalhes: Detalhes adicionais
            
        Returns:
            True se sucesso, False se erro
        """
        url = f'{self.base_url}/api/signal'
        payload = {
            'ativo': ativo,
            'direcao': direcao,
            'horario': horario
        }
        
        # Adicionar campos opcionais
        if preco is not None:
            payload['preco'] = preco
        if confianca is not None:
            payload['confianca'] = confianca
        if indicadores:
            payload['indicadores'] = indicadores
        if detalhes:
            payload['detalhes'] = detalhes
            
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                print(f'✅ Sinal enviado com sucesso! ID: {result.get("id")}')
                return True
            else:
                print(f'❌ Erro ao enviar sinal: {response.text}')
                return False
                
        except requests.exceptions.ConnectionError:
            print('❌ Erro: Não foi possível conectar ao servidor ThomazTrade')
            return False
        except requests.exceptions.Timeout:
            print('❌ Erro: Timeout na conexão')
            return False
        except Exception as e:
            print(f'❌ Erro inesperado: {str(e)}')
            return False
    
    def obter_sinais(self, limite: int = 10) -> list:
        """
        Obtém sinais recentes da API
        
        Args:
            limite: Número máximo de sinais a retornar
            
        Returns:
            Lista de sinais ou lista vazia se erro
        """
        try:
            url = f'{self.base_url}/api/signals'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('signals', [])[:limite]
            else:
                print(f'❌ Erro ao obter sinais: {response.status_code}')
                return []
                
        except Exception as e:
            print(f'❌ Erro ao obter sinais: {str(e)}')
            return []
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas dos sinais
        
        Returns:
            Dicionário com estatísticas ou vazio se erro
        """
        try:
            url = f'{self.base_url}/api/stats'
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'❌ Erro ao obter estatísticas: {response.status_code}')
                return {}
                
        except Exception as e:
            print(f'❌ Erro ao obter estatísticas: {str(e)}')
            return {}
    
    def registrar_usuario(self, email: str, senha: str) -> bool:
        """
        Registra novo usuário
        
        Args:
            email: Email do usuário
            senha: Senha do usuário
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            url = f'{self.base_url}/api/register'
            payload = {'email': email, 'password': senha}
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 201:
                print('✅ Usuário registrado com sucesso!')
                return True
            else:
                result = response.json()
                print(f'❌ Erro no registro: {result.get("message")}')
                return False
                
        except Exception as e:
            print(f'❌ Erro no registro: {str(e)}')
            return False
    
    def fazer_login(self, email: str, senha: str) -> bool:
        """
        Faz login do usuário
        
        Args:
            email: Email do usuário
            senha: Senha do usuário
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            url = f'{self.base_url}/api/login'
            payload = {'email': email, 'password': senha}
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f'✅ Login realizado com sucesso! VIP: {result.get("is_vip")}')
                return True
            else:
                result = response.json()
                print(f'❌ Erro no login: {result.get("message")}')
                return False
                
        except Exception as e:
            print(f'❌ Erro no login: {str(e)}')
            return False
    
    def testar_conexao(self) -> bool:
        """
        Testa conexão com a API
        
        Returns:
            True se conexão OK, False se erro
        """
        try:
            url = f'{self.base_url}/health'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print('✅ Conexão com ThomazTrade API: OK')
                return True
            else:
                print('❌ Conexão com ThomazTrade API: Erro')
                return False
                
        except Exception as e:
            print(f'❌ Erro na conexão: {str(e)}')
            return False

def enviar_sinal_api(ativo: str, direcao: str, horario: str, 
                    base_url: str = "http://localhost:5000"):
    """
    Função simples para compatibilidade com código existente
    """
    client = ThomazTradeClient(base_url)
    return client.enviar_sinal_api(ativo, direcao, horario)

# Exemplos de uso
if __name__ == "__main__":
    print("🚀 ThomazTrade Signal Client")
    print("=" * 40)
    
    # Inicializar cliente
    client = ThomazTradeClient()
    
    # Testar conexão
    if not client.testar_conexao():
        print("❌ Não foi possível conectar ao servidor ThomazTrade")
        exit(1)
    
    # Exemplo 1: Enviar sinal simples
    print("\n📤 Enviando sinal simples...")
    client.enviar_sinal_api("PETR4", "compra", "15:30")
    
    # Exemplo 2: Enviar sinal completo
    print("\n📤 Enviando sinal completo...")
    client.enviar_sinal_api(
        ativo="BTC/USD",
        direcao="venda", 
        horario="15:45",
        preco=45800.50,
        confianca=85.5,
        indicadores=["RSI", "MACD"],
        detalhes="Sinal baseado em análise técnica"
    )
    
    # Exemplo 3: Obter sinais recentes
    print("\n📥 Obtendo sinais recentes...")
    sinais = client.obter_sinais(5)
    for i, sinal in enumerate(sinais, 1):
        print(f"{i}. {sinal['symbol']} - {sinal['action']} ({sinal['confidence']}%)")
    
    # Exemplo 4: Obter estatísticas
    print("\n📊 Estatísticas:")
    stats = client.obter_estatisticas()
    if stats:
        print(f"Total de sinais: {stats.get('total_signals', 0)}")
        print(f"Sinais de compra: {stats.get('buy_signals', 0)}")
        print(f"Sinais de venda: {stats.get('sell_signals', 0)}")
        print(f"Confiança média: {stats.get('avg_confidence', 0)}%")