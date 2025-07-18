import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SignalChart from './SignalChart';

function VIPArea({ user, onLogout }) {
  const [signals, setSignals] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [signalsRes, statsRes] = await Promise.all([
        axios.get('/api/signals'),
        axios.get('/api/stats')
      ]);
      setSignals(signalsRes.data.signals || []);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };
  const [customSignal, setCustomSignal] = useState({
    ativo: '',
    direcao: 'compra',
    horario: '',
    preco: '',
    confianca: '',
    indicadores: '',
    detalhes: ''
  });
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCustomSignal(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmitSignal = async (e) => {
    e.preventDefault();
    setSending(true);
    setMessage('');

    try {
      const signalData = {
        ...customSignal,
        preco: customSignal.preco ? parseFloat(customSignal.preco) : null,
        confianca: customSignal.confianca ? parseFloat(customSignal.confianca) : null,
        indicadores: customSignal.indicadores.split(',').map(i => i.trim()).filter(i => i),
        horario: customSignal.horario || new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
      };

      await axios.post('/api/signal', signalData);
      setMessage('Sinal personalizado enviado com sucesso!');
      
      // Reset form
      setCustomSignal({
        ativo: '',
        direcao: 'compra',
        horario: '',
        preco: '',
        confianca: '',
        indicadores: '',
        detalhes: ''
      });

      // Refresh page after 2 seconds to show new signal
      setTimeout(() => {
        window.location.reload();
      }, 2000);

    } catch (error) {
      setMessage('Erro ao enviar sinal: ' + (error.response?.data?.message || error.message));
    } finally {
      setSending(false);
    }
  };

  const exportSignals = async () => {
    try {
      const response = await axios.get('/api/signals');
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
      
      const exportFileDefaultName = `thomaztrade-signals-${new Date().toISOString().split('T')[0]}.json`;
      
      const linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
      
      setMessage('Sinais exportados com sucesso!');
    } catch (error) {
      setMessage('Erro ao exportar sinais');
    }
  };

  // VIP Analytics
  const vipStats = {
    todaySignals: signals.filter(s => {
      const today = new Date().toDateString();
      return new Date(s.timestamp).toDateString() === today;
    }).length,
    highConfidenceSignals: signals.filter(s => s.confidence > 80).length,
    profitableSignals: signals.filter(s => s.confidence > 70).length,
    avgDailySignals: Math.round(signals.length / Math.max(1, Math.ceil((Date.now() - new Date(signals[signals.length - 1]?.timestamp || Date.now()).getTime()) / (1000 * 60 * 60 * 24))))
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <h2>Carregando ThomazTrade...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="header">
        <h1>ThomazTrade</h1>
        <p>Sistema Automatizado de Sinais de Trading</p>
        <div style={{ marginTop: '1rem' }}>
          <span>Bem-vindo, {user.email}</span>
          {user.is_vip && <span style={{ marginLeft: '10px', background: 'gold', color: 'black', padding: '2px 8px', borderRadius: '12px', fontSize: '0.8em' }}>VIP</span>}
          <button 
            onClick={onLogout}
            className="btn btn-secondary"
            style={{ marginLeft: '15px', padding: '5px 15px', fontSize: '0.9em' }}
          >
            Sair
          </button>
        </div>
      </header>

      {/* Statistics Dashboard */}
      <div className="card">
        <h2>Dashboard de Estatísticas</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{stats.total_signals || 0}</h3>
            <p>Total de Sinais</p>
          </div>
          <div className="stat-card">
            <h3>{stats.buy_signals || 0}</h3>
            <p>Sinais de Compra</p>
          </div>
          <div className="stat-card">
            <h3>{stats.sell_signals || 0}</h3>
            <p>Sinais de Venda</p>
          </div>
          <div className="stat-card">
            <h3>{stats.avg_confidence || 0}%</h3>
            <p>Confiança Média</p>
          </div>
        </div>
      </div>

      {/* Signal Chart */}
      <div className="card">
        <h2>Gráfico de Sinais</h2>
        <SignalChart signals={signals} />
      </div>

      {/* Recent Signals */}
      <div className="card">
        <h2>Sinais Recentes</h2>
        {signals.length === 0 ? (
          <p>Nenhum sinal encontrado</p>
        ) : (
          <div>
            {signals.slice(0, 10).map((signal, index) => (
              <div key={index} className={`signal-item ${signal.action === 'sell' || signal.action === 'venda' ? 'sell' : ''}`}>
                <div className="signal-meta">
                  <div className="signal-symbol">{signal.symbol}</div>
                  <div className={`signal-action ${signal.action === 'sell' || signal.action === 'venda' ? 'sell' : 'buy'}`}>
                    {signal.action === 'buy' || signal.action === 'compra' ? 'COMPRAR' : 'VENDER'}
                  </div>
                </div>
                <div className="signal-details">
                  <strong>Preço:</strong> ${signal.price?.toFixed(2) || 'N/A'} | 
                  <strong> Confiança:</strong> {signal.confidence?.toFixed(1) || 0}% | 
                  <strong> Horário:</strong> {new Date(signal.timestamp).toLocaleString('pt-BR')}
                </div>
                {signal.indicators && (
                  <div className="signal-details">
                    <strong>Indicadores:</strong> {Array.isArray(signal.indicators) ? signal.indicators.join(', ') : signal.indicators}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {user.is_vip && (
        <div className="card" style={{ background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)', border: '3px solid gold' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 style={{ margin: 0, color: '#8b4513' }}>Área VIP</h2>
            <span style={{ marginLeft: '10px', background: 'gold', color: 'black', padding: '5px 12px', borderRadius: '15px', fontSize: '0.9em', fontWeight: 'bold' }}>
              PREMIUM
            </span>
          </div>

      {message && (
        <div className={message.includes('sucesso') ? 'success' : 'error'}>
          {message}
        </div>
      )}

      {/* VIP Statistics */}
      <div style={{ marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#8b4513' }}>Estatísticas Avançadas VIP</h3>
        <div className="stats-grid">
          <div className="stat-card" style={{ borderLeft: '4px solid gold' }}>
            <h3 style={{ color: '#b8860b' }}>{vipStats.todaySignals}</h3>
            <p>Sinais Hoje</p>
          </div>
          <div className="stat-card" style={{ borderLeft: '4px solid gold' }}>
            <h3 style={{ color: '#b8860b' }}>{vipStats.highConfidenceSignals}</h3>
            <p>Alta Confiança (>80%)</p>
          </div>
          <div className="stat-card" style={{ borderLeft: '4px solid gold' }}>
            <h3 style={{ color: '#b8860b' }}>{vipStats.profitableSignals}</h3>
            <p>Sinais Promissores</p>
          </div>
          <div className="stat-card" style={{ borderLeft: '4px solid gold' }}>
            <h3 style={{ color: '#b8860b' }}>{vipStats.avgDailySignals}</h3>
            <p>Média Diária</p>
          </div>
        </div>
      </div>

      {/* Custom Signal Form */}
      <div style={{ marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#8b4513' }}>Enviar Sinal Personalizado</h3>
        <form onSubmit={handleSubmitSignal} style={{ background: 'rgba(255,255,255,0.7)', padding: '1.5rem', borderRadius: '8px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div className="form-group">
              <label>Ativo:</label>
              <input
                type="text"
                name="ativo"
                value={customSignal.ativo}
                onChange={handleInputChange}
                placeholder="Ex: BTC/USD, PETR4"
                required
              />
            </div>
            
            <div className="form-group">
              <label>Direção:</label>
              <select
                name="direcao"
                value={customSignal.direcao}
                onChange={handleInputChange}
                style={{ width: '100%', padding: '0.8rem', border: '2px solid #ddd', borderRadius: '6px' }}
              >
                <option value="compra">Compra</option>
                <option value="venda">Venda</option>
              </select>
            </div>

            <div className="form-group">
              <label>Horário:</label>
              <input
                type="time"
                name="horario"
                value={customSignal.horario}
                onChange={handleInputChange}
              />
            </div>

            <div className="form-group">
              <label>Preço:</label>
              <input
                type="number"
                name="preco"
                value={customSignal.preco}
                onChange={handleInputChange}
                step="0.01"
                placeholder="Opcional"
              />
            </div>

            <div className="form-group">
              <label>Confiança (%):</label>
              <input
                type="number"
                name="confianca"
                value={customSignal.confianca}
                onChange={handleInputChange}
                min="0"
                max="100"
                placeholder="0-100"
              />
            </div>

            <div className="form-group">
              <label>Indicadores:</label>
              <input
                type="text"
                name="indicadores"
                value={customSignal.indicadores}
                onChange={handleInputChange}
                placeholder="RSI, MACD, etc (separados por vírgula)"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Detalhes:</label>
            <textarea
              name="detalhes"
              value={customSignal.detalhes}
              onChange={handleInputChange}
              rows="3"
              style={{ width: '100%', padding: '0.8rem', border: '2px solid #ddd', borderRadius: '6px', resize: 'vertical' }}
              placeholder="Análise adicional ou comentários..."
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-success"
            disabled={sending}
            style={{ width: '100%' }}
          >
            {sending ? 'Enviando...' : 'Enviar Sinal Personalizado'}
          </button>
        </form>
      </div>

      {/* VIP Tools */}
      <div>
        <h3 style={{ marginBottom: '1rem', color: '#8b4513' }}>Ferramentas VIP</h3>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button 
            onClick={exportSignals}
            className="btn"
            style={{ background: '#28a745' }}
          >
            📊 Exportar Sinais
          </button>
          
          <button 
            onClick={() => window.open('/api/signals', '_blank')}
            className="btn"
            style={{ background: '#17a2b8' }}
          >
            🔗 API Endpoints
          </button>
          
          <button 
            onClick={() => setMessage('Análise de performance em desenvolvimento...')}
            className="btn"
            style={{ background: '#6f42c1' }}
          >
            📈 Análise Performance
          </button>
        </div>
      </div>

      {/* VIP Features List */}
      <div style={{ marginTop: '2rem', padding: '1rem', background: 'rgba(255,255,255,0.8)', borderRadius: '8px' }}>
        <h4 style={{ color: '#8b4513', marginBottom: '1rem' }}>Recursos Exclusivos VIP:</h4>
        <ul style={{ listStyle: 'none', padding: 0, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '0.5rem' }}>
          <li>⭐ Sinais personalizados</li>
          <li>📊 Estatísticas avançadas</li>
          <li>📈 Análise de performance</li>
          <li>💾 Exportação de dados</li>
          <li>🔄 Acesso completo à API</li>
          <li>🎯 Sinais de alta confiança</li>
          <li>📱 Notificações prioritárias</li>
          <li>🛠️ Ferramentas avançadas</li>
        </ul>
      </div>
    </div>
  );
}

export default VIPArea;