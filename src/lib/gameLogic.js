
export const CONDITIONS = {
    SPEED: [30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
    ROAD_TYPE: ['Highway', 'Urban', 'Rural'],
    WEATHER: [
        { type: 'Clear', risk: 0, icon: 'sun' },
        { type: 'Rain', risk: 15, icon: 'cloud-rain' },
        { type: 'Fog', risk: 25, icon: 'cloud-fog' },
        { type: 'Snow', risk: 20, icon: 'snowflake' }
    ],
    LIGHTING: [
        { type: 'Day', risk: 0, icon: 'sun' },
        { type: 'Night', risk: 20, icon: 'moon' },
        { type: 'Dusk', risk: 10, icon: 'sunset' }
    ]
};

export const MISSIONS = [
    "Urgent medical delivery to the city hospital.",
    "Transporting fragile cargo across the state.",
    "Family road trip to the mountains.",
    "Late night commute home after a double shift.",
    "Escaping a sudden zombie outbreak.",
    "High-speed pursuit of a fugitive."
];

export function generateScenario() {
    const speed = CONDITIONS.SPEED[Math.floor(Math.random() * CONDITIONS.SPEED.length)];
    const weather = CONDITIONS.WEATHER[Math.floor(Math.random() * CONDITIONS.WEATHER.length)];
    const lighting = CONDITIONS.LIGHTING[Math.floor(Math.random() * CONDITIONS.LIGHTING.length)];
    const roadType = CONDITIONS.ROAD_TYPE[Math.floor(Math.random() * CONDITIONS.ROAD_TYPE.length)];
    const curvature = parseFloat(Math.random().toFixed(2)); // 0.00 to 1.00

    return {
        id: Math.random().toString(36).substr(2, 9),
        speed,
        weather,
        lighting,
        roadType,
        curvature,
        riskScore: calculateRisk(speed, weather, lighting, roadType, curvature)
    };
}

function calculateRisk(speed, weather, lighting, roadType, curvature) {
    let score = 10; // Base risk

    // Speed factor
    // Higher speed = higher risk, but context matters.
    score += (speed * 0.4);

    // Road Type Context
    if (roadType === 'Highway') {
        score -= 10; // Highways are generally safer design-wise
        if (curvature > 0.6) score += 15; // But dangerous if curvy
    } else if (roadType === 'Urban') {
        score += 5; // Traffic density risk
        if (speed > 50) score += 20; // High speed in urban is very dangerous
    } else if (roadType === 'Rural') {
        score += 10; // Unpredictable
        if (lighting.type === 'Night') score += 15; // Very dark
        if (curvature > 0.5) score += curvature * 20; // Winding rural roads
    }

    // Curvature Factor (Linear)
    score += curvature * 30;

    // Environmental
    score += weather.risk;
    score += lighting.risk;

    // Multipliers
    if (weather.type !== 'Clear' && curvature > 0.7) score += 10;
    if (weather.type === 'Snow' && speed > 60) score += 20;

    return Math.min(99, Math.max(1, Math.round(score)));
}

export async function fetchRisk(scenario) {
    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                speed: scenario.speed,
                roadType: scenario.roadType,
                curvature: scenario.curvature,
                weather: scenario.weather.type,
                lighting: scenario.lighting.type
            })
        });
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        return data.riskScore;
    } catch (e) {
        console.error("API Error:", e);
        return 50; // Fallback
    }
}

export async function generateRound() {
    let left = generateScenario();
    let right = generateScenario();
    const mission = MISSIONS[Math.floor(Math.random() * MISSIONS.length)];

    // Fetch real risks
    left.riskScore = await fetchRisk(left);
    right.riskScore = await fetchRisk(right);

    // Ensure they aren't identical in risk
    let retries = 0;
    while (Math.abs(left.riskScore - right.riskScore) < 5 && retries < 3) {
        right = generateScenario();
        right.riskScore = await fetchRisk(right);
        retries++;
    }

    return { left, right, mission };
}
