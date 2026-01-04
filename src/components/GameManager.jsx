import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, RefreshCw, CheckCircle, XCircle, MapPin } from 'lucide-react';
import RoadCard from './RoadCard';
import { generateRound } from '../lib/gameLogic';

function GameManager({ onExit }) {
    const [roundData, setRoundData] = useState(null);
    const [roundResult, setRoundResult] = useState(null); // { correct: bool, picked: 'left'|'right' }
    const [score, setScore] = useState(0);
    const [streak, setStreak] = useState(0);
    const [roundsPlayed, setRoundsPlayed] = useState(0);

    useEffect(() => {
        loadNewRound();
    }, []);

    const loadNewRound = async () => {
        setRoundData(null); // Show loading state if needed
        const newRound = await generateRound();
        setRoundData(newRound);
        setRoundResult(null);
    };

    const handleChoice = (choice) => { // 'left' or 'right'
        if (roundResult) return;

        const leftRisk = roundData.left.riskScore;
        const rightRisk = roundData.right.riskScore;

        // Safer means LOWER risk
        const isLeftSafer = leftRisk < rightRisk;
        const correct = (choice === 'left' && isLeftSafer) || (choice === 'right' && !isLeftSafer);

        setRoundResult({
            correct,
            picked: choice,
            leftSafer: isLeftSafer
        });

        if (correct) {
            setScore(s => s + 100 + (streak * 10)); // Bonus for streak
            setStreak(s => s + 1);
        } else {
            setStreak(0);
        }
        setRoundsPlayed(r => r + 1);
    };

    if (!roundData) return <div>Loading...</div>;

    return (
        <div style={{ width: '100%', maxWidth: '900px' }}>
            {/* HUD */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '2rem',
                padding: '1rem',
                background: 'rgba(0,0,0,0.2)',
                borderRadius: '12px'
            }}>
                <div style={{ display: 'flex', gap: '1.5rem' }}>
                    <StatBadge icon={<Trophy size={18} />} label="Score" value={score} />
                    <StatBadge icon={<CheckCircle size={18} />} label="Streak" value={streak} color="var(--accent-safe)" />
                </div>
                <button
                    onClick={onExit}
                    style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}
                >
                    Exit Game
                </button>
            </div>

            {/* Mission Context */}
            <div style={{
                textAlign: 'center',
                marginBottom: '2rem',
                padding: '0.8rem',
                background: 'linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent)',
                borderTop: '1px solid var(--glass-border)',
                borderBottom: '1px solid var(--glass-border)'
            }}>
                <div style={{ color: 'var(--accent-primary)', fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.3rem' }}>
                    Current Mission
                </div>
                <div style={{ fontSize: '1.2rem', fontWeight: '500', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                    <MapPin size={18} /> {roundData.mission}
                </div>
            </div>

            {/* Game Area */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr auto 1fr',
                gap: '2rem',
                alignItems: 'center'
            }}>
                <RoadCard
                    scenario={roundData.left}
                    onClick={() => handleChoice('left')}
                    disabled={!!roundResult}
                    showResult={!!roundResult}
                    isWinner={roundResult ? (roundResult.leftSafer) : false}
                />

                {/* VS / Result Divider */}
                <div style={{ textAlign: 'center', minWidth: '80px' }}>
                    <AnimatePresence mode="wait">
                        {!roundResult ? (
                            <motion.div
                                key="vs"
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                                style={{ fontSize: '1.5rem', fontWeight: '800', color: 'var(--text-secondary)' }}
                            >
                                VS
                            </motion.div>
                        ) : (
                            <motion.div
                                key="result"
                                initial={{ scale: 0 }} animate={{ scale: 1 }}
                                style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}
                            >
                                {roundResult.correct ? (
                                    <CheckCircle size={48} color="var(--accent-safe)" />
                                ) : (
                                    <XCircle size={48} color="var(--accent-danger)" />
                                )}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                <RoadCard
                    scenario={roundData.right}
                    onClick={() => handleChoice('right')}
                    disabled={!!roundResult}
                    showResult={!!roundResult}
                    isWinner={roundResult ? (!roundResult.leftSafer) : false}
                />
            </div>

            {/* Next Round Action */}
            <AnimatePresence>
                {roundResult && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{
                            marginTop: '3rem',
                            textAlign: 'center',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '1rem'
                        }}
                    >
                        <div style={{ fontSize: '1.2rem', fontWeight: '600' }}>
                            {roundResult.correct ? "Great Choice! You prioritized safety." : "Oops! The higher risk was hidden."}
                        </div>

                        <button
                            onClick={loadNewRound}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '0.5rem',
                                backgroundColor: 'var(--text-primary)',
                                color: 'var(--bg-app)',
                                padding: '0.8rem 2rem',
                                borderRadius: '50px',
                                fontSize: '1rem',
                                fontWeight: '700',
                                boxShadow: 'var(--shadow-glow)'
                            }}
                        >
                            <RefreshCw size={18} /> Next Scenario
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

const StatBadge = ({ icon, label, value, color }) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span style={{ color: color || 'var(--text-secondary)' }}>{icon}</span>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginRight: '0.3rem' }}>{label}</span>
        <span style={{ fontSize: '1.1rem', fontWeight: '700' }}>{value}</span>
    </div>
);

export default GameManager;
