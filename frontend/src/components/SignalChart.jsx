import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';

function SignalChart() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSignals();
    const interval = setInterval(fetchSignals, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchSignals = async () => {
    try {
      const response = await axios.get('/api/signals');
      setSignals(response.data.signals || []);
    } catch (error) {
      console.error('Error fetching signals:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Carregando gráficos...</div>;
  }
  const chartData = useMemo(() => {
    if (!signals || signals.length === 0) return [];

    // Group signals by hour for trend analysis
    const hourlyData = signals.reduce((acc, signal) => {
      const date = new Date(signal.timestamp);
      const hour = date.getHours();
      const key = `${hour}:00`;
      
      if (!acc[key]) {
        acc[key] = {
          time: key,
          buy: 0,
          sell: 0,
          totalConfidence: 0,
          count: 0
        };
      }
      
      if (signal.action === 'buy' || signal.action === 'compra') {
        acc[key].buy += 1;
      } else {
        acc[key].sell += 1;
      }
      
      acc[key].totalConfidence += signal.confidence || 0;
      acc[key].count += 1;
      
      return acc;
    }, {});

    return Object.values(hourlyData).map(item => ({
      ...item,
      avgConfidence: item.count > 0 ? Math.round(item.totalConfidence / item.count) : 0
    })).sort((a, b) => {
      const timeA = parseInt(a.time.split(':')[0]);
      const timeB = parseInt(b.time.split(':')[0]);
      return timeA - timeB;
    });
  }, [signals]);

  const symbolData = useMemo(() => {
    if (!signals || signals.length === 0) return [];

    const symbolStats = signals.reduce((acc, signal) => {
      const symbol = signal.symbol;
      if (!acc[symbol]) {
        acc[symbol] = {
          symbol,
          count: 0,
          totalConfidence: 0,
          buy: 0,
          sell: 0
        };
      }
      
      acc[symbol].count += 1;
      acc[symbol].totalConfidence += signal.confidence || 0;
      
      if (signal.action === 'buy' || signal.action === 'compra') {
        acc[symbol].buy += 1;
      } else {
        acc[symbol].sell += 1;
      }
      
      return acc;
    }, {});

    return Object.values(symbolStats).map(item => ({
      ...item,
      avgConfidence: Math.round(item.totalConfidence / item.count)
    })).sort((a, b) => b.count - a.count);
  }, [signals]);

  const confidenceDistribution = useMemo(() => {
    if (!signals || signals.length === 0) return [];

    const ranges = [
      { name: '0-50%', min: 0, max: 50, count: 0, color: '#ff6b6b' },
      { name: '51-70%', min: 51, max: 70, count: 0, color: '#ffd93d' },
      { name: '71-85%', min: 71, max: 85, count: 0, color: '#6bcf7f' },
      { name: '86-100%', min: 86, max: 100, count: 0, color: '#4ecdc4' }
    ];

    signals.forEach(signal => {
      const confidence = signal.confidence || 0;
      const range = ranges.find(r => confidence >= r.min && confidence <= r.max);
      if (range) range.count += 1;
    });

    return ranges.filter(range => range.count > 0);
  }, [signals]);

  if (!signals || signals.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
        <p>Nenhum dado disponível para exibir gráficos.</p>
        <p>Os gráficos aparecerão quando houver sinais de trading.</p>
      </div>
    );
  }

  return (
    <div>
      {/* Signal Trend by Time */}
      <div style={{ marginBottom: '3rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#333' }}>Distribuição de Sinais por Horário</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip 
              formatter={(value, name) => [
                value, 
                name === 'buy' ? 'Compra' : name === 'sell' ? 'Venda' : 'Confiança Média'
              ]}
              labelFormatter={(label) => `Horário: ${label}`}
            />
            <Legend 
              formatter={(value) => 
                value === 'buy' ? 'Sinais de Compra' : 
                value === 'sell' ? 'Sinais de Venda' : 
                'Confiança Média (%)'
              }
            />
            <Bar dataKey="buy" fill="#28a745" name="buy" />
            <Bar dataKey="sell" fill="#dc3545" name="sell" />
            <Line 
              type="monotone" 
              dataKey="avgConfidence" 
              stroke="#667eea" 
              strokeWidth={3}
              name="avgConfidence"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Symbol Performance */}
      <div style={{ marginBottom: '3rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#333' }}>Performance por Ativo</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={symbolData.slice(0, 8)} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="symbol" type="category" width={80} />
            <Tooltip 
              formatter={(value, name) => [
                value, 
                name === 'count' ? 'Total de Sinais' : 
                name === 'avgConfidence' ? 'Confiança Média (%)' :
                name === 'buy' ? 'Sinais de Compra' : 'Sinais de Venda'
              ]}
            />
            <Legend />
            <Bar dataKey="count" fill="#667eea" name="count" />
            <Bar dataKey="avgConfidence" fill="#ffd93d" name="avgConfidence" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Confidence Distribution */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
        <div>
          <h3 style={{ marginBottom: '1rem', color: '#333' }}>Distribuição de Confiança</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={confidenceDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, count }) => `${name}: ${count}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {confidenceDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value} sinais`, 'Quantidade']} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div>
          <h3 style={{ marginBottom: '1rem', color: '#333' }}>Resumo Estatístico</h3>
          <div style={{ background: '#f8f9fa', padding: '1.5rem', borderRadius: '8px' }}>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Total de Sinais:</strong> {signals.length}
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Ativos Únicos:</strong> {new Set(signals.map(s => s.symbol)).size}
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Confiança Média:</strong> {
                Math.round(signals.reduce((acc, s) => acc + (s.confidence || 0), 0) / signals.length)
              }%
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Sinais de Alta Confiança (>80%):</strong> {
                signals.filter(s => (s.confidence || 0) > 80).length
              }
            </div>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Proporção Compra/Venda:</strong> {
                signals.filter(s => s.action === 'buy' || s.action === 'compra').length
              }/{
                signals.filter(s => s.action === 'sell' || s.action === 'venda').length
              }
            </div>
            <div>
              <strong>Último Sinal:</strong> {
                signals.length > 0 ? new Date(signals[0].timestamp).toLocaleString('pt-BR') : 'N/A'
              }
            </div>
          </div>
        </div>
      </div>

      {/* Recent Signals Timeline */}
      <div style={{ marginTop: '3rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#333' }}>Timeline dos Últimos Sinais</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={signals.slice(0, 20).reverse()}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={(value) => new Date(value).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
            />
            <YAxis domain={[0, 100]} />
            <Tooltip 
              formatter={(value) => [`${value}%`, 'Confiança']}
              labelFormatter={(value) => `Horário: ${new Date(value).toLocaleString('pt-BR')}`}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="confidence" 
              stroke="#667eea" 
              strokeWidth={2}
              dot={{ fill: '#667eea', strokeWidth: 2, r: 4 }}
              name="Nível de Confiança (%)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default SignalChart;