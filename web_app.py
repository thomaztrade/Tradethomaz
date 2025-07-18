#!/usr/bin/env python3
"""
ThomazTrade Web Application
Flask web interface for user management and signal viewing
"""

from flask import Flask, request, jsonify, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
from src.signal_history import SignalHistory

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thomaztrade_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thomaztrade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_vip = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_vip': self.is_vip,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

# Initialize signal history
signal_history = SignalHistory()

@app.route('/')
def home():
    """Main dashboard page"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ThomazTrade - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem; text-align: center; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .btn { background: #3498db; color: white; padding: 0.8rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .signal { padding: 1rem; border-left: 4px solid #27ae60; margin: 1rem 0; background: #f8f9fa; }
        .signal.sell { border-left-color: #e74c3c; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .stat { text-align: center; padding: 1rem; background: #3498db; color: white; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 ThomazTrade Dashboard</h1>
        <p>Sistema Automatizado de Sinais de Trading</p>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Status do Sistema</h2>
            <div class="stats">
                <div class="stat">
                    <h3 id="total-signals">-</h3>
                    <p>Total de Sinais</p>
                </div>
                <div class="stat">
                    <h3 id="buy-signals">-</h3>
                    <p>Sinais de Compra</p>
                </div>
                <div class="stat">
                    <h3 id="sell-signals">-</h3>
                    <p>Sinais de Venda</p>
                </div>
                <div class="stat">
                    <h3 id="avg-confidence">-</h3>
                    <p>Confiança Média</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>Sinais Recentes</h2>
            <div id="recent-signals">
                <p>Carregando sinais...</p>
            </div>
        </div>
        
        <div class="card">
            <h2>Acesso</h2>
            <a href="/api/register" class="btn">Registrar Usuário</a>
            <a href="/api/login" class="btn">Fazer Login</a>
            <a href="/api/signals" class="btn">Ver Sinais (API)</a>
        </div>
    </div>

    <script>
        // Load statistics
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-signals').textContent = data.total_signals;
                document.getElementById('buy-signals').textContent = data.buy_signals;
                document.getElementById('sell-signals').textContent = data.sell_signals;
                document.getElementById('avg-confidence').textContent = data.avg_confidence + '%';
            });

        // Load recent signals
        fetch('/api/signals')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('recent-signals');
                if (data.signals && data.signals.length > 0) {
                    container.innerHTML = data.signals.map(signal => `
                        <div class="signal ${signal.action}">
                            <strong>${signal.symbol}</strong> - 
                            ${signal.action === 'buy' ? '🟢 COMPRAR' : '🔴 VENDER'} - 
                            $${signal.price.toFixed(2)} 
                            (${signal.confidence.toFixed(1)}% confiança)
                            <br><small>${signal.timestamp}</small>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<p>Nenhum sinal encontrado</p>';
                }
            });
    </script>
</body>
</html>
    ''')

@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template_string('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>ThomazTrade - Registro</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; }
        input { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 1rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <h1>Registro ThomazTrade</h1>
    <form id="registerForm">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" required>
        </div>
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" required>
        </div>
        <button type="submit">Registrar</button>
    </form>
    <div id="message"></div>
    <a href="/">← Voltar ao Dashboard</a>

    <script>
        document.getElementById('registerForm').onsubmit = function(e) {
            e.preventDefault();
            fetch('/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value
                })
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'message ' + (data.message.includes('sucesso') ? 'success' : 'error');
                messageDiv.textContent = data.message;
            });
        };
    </script>
</body>
</html>
        ''')
    
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email já cadastrado'}), 400

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template_string('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>ThomazTrade - Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; }
        input { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 1rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .message { padding: 1rem; margin: 1rem 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <h1>Login ThomazTrade</h1>
    <form id="loginForm">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" required>
        </div>
        <div class="form-group">
            <label for="password">Senha:</label>
            <input type="password" id="password" required>
        </div>
        <button type="submit">Entrar</button>
    </form>
    <div id="message"></div>
    <a href="/">← Voltar ao Dashboard</a>

    <script>
        document.getElementById('loginForm').onsubmit = function(e) {
            e.preventDefault();
            fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value
                })
            })
            .then(response => response.json())
            .then(data => {
                const messageDiv = document.getElementById('message');
                messageDiv.className = 'message ' + (data.message.includes('sucesso') ? 'success' : 'error');
                messageDiv.textContent = data.message;
                if (data.message.includes('sucesso')) {
                    setTimeout(() => window.location.href = '/', 1500);
                }
            });
        };
    </script>
</body>
</html>
        ''')
    
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    user.last_login = datetime.utcnow()
    db.session.commit()
    session['user_id'] = user.id
    
    return jsonify({
        'message': 'Login realizado com sucesso', 
        'is_vip': user.is_vip,
        'user': user.to_dict()
    })

@app.route('/api/signals', methods=['GET'])
def get_signals():
    """Get recent trading signals from the bot"""
    try:
        # Get recent signals from signal history
        recent_signals = signal_history.get_recent_signals(limit=10)
        
        # Format signals for API response
        formatted_signals = []
        for signal in recent_signals:
            formatted_signals.append({
                'symbol': signal.get('symbol', 'Unknown'),
                'action': signal.get('action', 'unknown'),
                'price': float(signal.get('price', 0)),
                'confidence': float(signal.get('confidence', 0)),
                'timestamp': signal.get('timestamp', ''),
                'indicators': signal.get('indicators', []),
                'details': signal.get('details', '')
            })
        
        return jsonify({
            'signals': formatted_signals,
            'count': len(formatted_signals),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'signals': [],
            'count': 0,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get trading statistics"""
    try:
        stats = signal_history.get_signal_stats(days=7)
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'total_signals': 0,
            'buy_signals': 0,
            'sell_signals': 0,
            'symbols': [],
            'avg_confidence': 0.0,
            'error': str(e)
        })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users (admin only)"""
    if 'user_id' not in session:
        return jsonify({'message': 'Login necessário'}), 401
    
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'count': len(users)
    })

@app.route('/api/user/<int:user_id>/vip', methods=['POST'])
def toggle_vip(user_id):
    """Toggle VIP status for a user"""
    if 'user_id' not in session:
        return jsonify({'message': 'Login necessário'}), 401
    
    user = User.query.get_or_404(user_id)
    user.is_vip = not user.is_vip
    db.session.commit()
    
    return jsonify({
        'message': f'Status VIP {"ativado" if user.is_vip else "desativado"} para {user.email}',
        'user': user.to_dict()
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")
        print("Starting ThomazTrade Web Application...")
        print("Access the dashboard at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)