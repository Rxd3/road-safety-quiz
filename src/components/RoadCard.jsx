import React from 'react';
import { motion } from 'framer-motion';
import { Sun, Moon, CloudRain, CloudFog, Snowflake, Navigation, Zap, AlertTriangle } from 'lucide-react';

const icons = {
    'sun': Sun,
    'moon': Moon,
    'cloud-rain': CloudRain,
    'cloud-fog': CloudFog,
    'snowflake': Snowflake,
    'sunset': Sun // Fallback/reuse
};

function RoadCard({ scenario, onClick, disabled, showResult, isWinner }) {
    const WeatherIcon = icons[scenario.weather.icon] || Sun;

    return (
        <motion.div
            whileHover={!disabled ? { scale: 1.02, y: -5 } : {}}
            whileTap={!disabled ? { scale: 0.98 } : {}}
            className={`glass-panel roadway-card ${isWinner ? 'winner-card' : ''}`}
            onClick={onClick}
            style={{
                padding: '2rem',
                cursor: disabled ? 'default' : 'pointer',
                position: 'relative',
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem',
                minHeight: '320px',
                border: showResult
                    ? (isWinner ? '2px solid var(--accent-safe)' : '2px solid var(--accent-danger)')
                    : '1px solid var(--glass-border)',
                transition: 'border-color 0.3s'
            }}
        >
            {/* Header Visual */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '1rem',
                paddingBottom: '1rem',
                borderBottom: '1px solid var(--glass-border)'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <WeatherIcon size={28} color="var(--accent-primary)" />
                    <span style={{ fontSize: '1.2rem', fontWeight: '600' }}>{scenario.weather.type}</span>
                </div>
                <div style={{
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                }}>
                    {scenario.lighting.type === 'Night' ? <Moon size={16} /> : <Sun size={16} />}
                    {scenario.lighting.type}
                </div>
            </div>

            {/* Stats */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem', flex: 1 }}>
                <StatRow
                    label="Speed Limit"
                    value={`${scenario.speed} mph`}
                    highlight={false}
                    icon={<Zap size={18} />}
                />
                <StatRow
                    label="Road Type"
                    value={scenario.roadType}
                    highlight={false}
                    icon={<Navigation size={18} />}
                />
                <StatRow
                    label="Curvature"
                    value={(scenario.curvature * 100).toFixed(0) + '%'}
                    highlight={false}
                    icon={<AlertTriangle size={18} />}
                />
            </div>

            {/* Result Overlay (Risk Score) */}
            {showResult && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    style={{
                        marginTop: '1rem',
                        padding: '1rem',
                        backgroundColor: isWinner ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                        borderRadius: '8px',
                        textAlign: 'center',
                        border: `1px solid ${isWinner ? 'var(--accent-safe)' : 'var(--accent-danger)'}`
                    }}
                >
                    <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Predicted Risk</div>
                    <div style={{
                        fontSize: '2rem',
                        fontWeight: '800',
                        color: isWinner ? 'var(--accent-safe)' : 'var(--accent-danger)'
                    }}>
                        {Math.round(scenario.riskScore)}%
                    </div>
                </motion.div>
            )}

            {/* Button Prompt */}
            {!showResult && (
                <div style={{
                    marginTop: 'auto',
                    textAlign: 'center',
                    color: 'var(--text-accent)',
                    fontSize: '0.9rem',
                    fontWeight: '600',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase'
                }}>
                    Select Route
                </div>
            )}
        </motion.div>
    );
}

const StatRow = ({ label, value, highlight, icon }) => (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)' }}>
            {icon}
            <span>{label}</span>
        </div>
        <span style={{
            fontWeight: '600',
            color: highlight ? 'var(--accent-danger)' : 'var(--text-primary)'
        }}>
            {value}
        </span>
    </div>
);

export default RoadCard;
