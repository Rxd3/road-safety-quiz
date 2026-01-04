import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, AlertTriangle } from 'lucide-react';
import GameManager from './components/GameManager';

function App() {
  const [gameState, setGameState] = useState('start'); // start, playing, gameover

  return (
    <div className="app-container" style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>
      <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-gradient"
          style={{ fontSize: '2.5rem', fontWeight: '800', marginBottom: '0.5rem' }}
        >
          Road Safety Quiz
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{ color: 'var(--text-secondary)' }}
        >
          Test your intuition. Which road is safer?
        </motion.p>
      </header>

      <main>
        {gameState === 'start' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-panel"
            style={{ padding: '3rem', textAlign: 'center' }}
          >
            <ShieldCheck size={64} color="var(--accent-primary)" style={{ marginBottom: '1.5rem' }} />
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Ready to drive?</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem', lineHeight: '1.6' }}>
              You will see two road scenarios. Use the data to pick the safest one.<br />
              Earn points for correct answers.
            </p>
            <button
              onClick={() => setGameState('playing')}
              style={{
                backgroundColor: 'var(--accent-primary)',
                color: 'white',
                padding: '1rem 2.5rem',
                borderRadius: '8px',
                fontSize: '1.1rem',
                fontWeight: '600',
                boxShadow: 'var(--shadow-glow)'
              }}
              onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
              onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
            >
              Start Game
            </button>
          </motion.div>
        )}

        {gameState === 'playing' && (
          <GameManager onExit={() => setGameState('start')} />
        )}
      </main>
    </div>
  );
}



export default App;
