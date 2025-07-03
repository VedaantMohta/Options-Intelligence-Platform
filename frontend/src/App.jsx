import React, { useState } from 'react';
import Plot from 'react-plotly.js';

// --- Reusable UI Components for a Clean Look ---
const Input = ({ label, id, ...props }) => (
    <div>
        <label htmlFor={id} className="block text-sm font-medium text-gray-400 mb-2">{label}</label>
        <input id={id} className="w-full bg-gray-700 border-gray-600 text-white rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 p-3 text-base transition" {...props} />
    </div>
);

const Select = ({ label, id, children, ...props }) => (
    <div className="relative">
        <label htmlFor={id} className="block text-sm font-medium text-gray-400 mb-2">{label}</label>
        <select id={id} className="w-full bg-gray-700 border-gray-600 text-white rounded-md shadow-sm focus:ring-cyan-500 focus:border-cyan-500 p-3 text-base appearance-none" {...props}>
            {children}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 top-7 flex items-center px-2 text-gray-400">
            <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.25 4.25a.75.75 0 01-1.06 0L5.23 8.27a.75.75 0 01.02-1.06z" clipRule="evenodd" />
            </svg>
        </div>
    </div>
);

const Button = ({ children, onClick, isLoading, ...props }) => (
    <button
        onClick={onClick}
        disabled={isLoading}
        className={`w-full bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 px-4 rounded-md shadow-lg transition transform focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-cyan-500 ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'}`}
        {...props}
    >
        {isLoading ? 'Loading...' : children}
    </button>
);

const Loader = () => (
    <div className="flex justify-center items-center h-full">
        <div className="w-16 h-16 border-4 border-t-transparent border-cyan-400 rounded-full animate-spin"></div>
    </div>
);

// --- Main Application Component ---
export default function App() {
    // State to manage the current step of the wizard
    const [step, setStep] = useState(1);
    
    // State for UI status (loading, errors)
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // State for user inputs
    const [ticker, setTicker] = useState('AAPL');
    const [expiration, setExpiration] = useState('2025-09-19');
    const [selectedStrike, setSelectedStrike] = useState('');
    const [optionType, setOptionType] = useState('call');

    // State for data fetched from the backend
    const [strikes, setStrikes] = useState([]);
    const [details, setDetails] = useState(null);
    const [heatmapData, setHeatmapData] = useState(null);

    // --- API Fetching Logic ---
    const fetchStrikes = async () => {
        if (!ticker || !expiration) return;
        setIsLoading(true);
        setError('');
        try {
            const response = await fetch(`/options/strikes?ticker=${ticker}&expiration_date=${expiration}`);
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to fetch strikes.');
            }
            const data = await response.json();
            setStrikes(data.strikes);
            if (data.strikes.length > 0) {
                setSelectedStrike(data.strikes[0]);
                setStep(2);
            } else {
                setError('No strikes found for this ticker and expiration date.');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
    
    const fetchDetailsAndHeatmap = async () => {
        if (!selectedStrike) return;
        setIsLoading(true);
        setError('');
        setDetails(null);
        setHeatmapData(null);

        try {
            const detailsPromise = fetch(`/options/contract-details?ticker=${ticker}&expiration_date=${expiration}&strike_price=${selectedStrike}&option_type=${optionType}`);
            const heatmapPromise = fetch('/options/heatmap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticker, strike_price: parseFloat(selectedStrike), expiration_date: expiration, option_type: optionType })
            });

            const [detailsResponse, heatmapResponse] = await Promise.all([detailsPromise, heatmapPromise]);

            if (!detailsResponse.ok || !heatmapResponse.ok) {
                throw new Error('An error occurred while fetching data for the heatmap.');
            }

            const detailsData = await detailsResponse.json();
            const heatmapResult = await heatmapResponse.json();

            setDetails(detailsData);
            setHeatmapData(heatmapResult);
            setStep(3);

        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };


    // --- Conditional Rendering Logic ---
    const renderStepContent = () => {
        if (isLoading) return <Loader />;

        switch (step) {
            case 1:
                return (
                    <div className="space-y-6 animate-fade-in">
                        <h3 className="text-xl font-semibold text-cyan-300">Step 1: Select Ticker & Expiration</h3>
                        <Input label="Ticker" id="ticker" value={ticker} onChange={(e) => setTicker(e.target.value.toUpperCase())} placeholder="e.g., AAPL" />
                        <Input label="Expiration (YYYY-MM-DD)" id="expiration" value={expiration} onChange={(e) => setExpiration(e.target.value)} placeholder="e.g., 2025-09-19"/>
                        <Button onClick={fetchStrikes} isLoading={isLoading}>Fetch Available Strikes</Button>
                    </div>
                );
            case 2:
                return (
                     <div className="space-y-6 animate-fade-in">
                        <h3 className="text-xl font-semibold text-cyan-300">Step 2: Select Strike & Type</h3>
                        <Select label="Strike Price" id="strike" value={selectedStrike} onChange={(e) => setSelectedStrike(e.target.value)}>
                            {strikes.map(s => <option key={s} value={s}>{s.toFixed(2)}</option>)}
                        </Select>
                         <Select label="Option Type" id="optionType" value={optionType} onChange={(e) => setOptionType(e.target.value)}>
                            <option value="call">Call</option>
                            <option value="put">Put</option>
                        </Select>
                        <Button onClick={fetchDetailsAndHeatmap} isLoading={isLoading}>Generate 3D Surface</Button>
                        <button onClick={() => { setStep(1); setError(''); }} className="text-sm text-gray-400 hover:text-white w-full mt-2">Back</button>
                    </div>
                );
            case 3:
                 return (
                    <div className="animate-fade-in">
                         <h3 className="text-xl font-semibold text-cyan-300 mb-4">Results for {ticker} ${parseFloat(selectedStrike).toFixed(2)} {optionType.toUpperCase()}</h3>
                         <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center mb-6 p-4 bg-gray-900/50 rounded-lg">
                            <div>
                                <p className="text-base text-gray-400">Underlying Price</p>
                                <p className="text-3xl font-semibold text-white">${details?.underlying_price.toFixed(2)}</p>
                            </div>
                             <div>
                                <p className="text-base text-gray-400">Live Option Price</p>
                                <p className="text-3xl font-semibold text-white">${details?.option_price.toFixed(2)}</p>
                            </div>
                            <div>
                                <p className="text-base text-gray-400">35D Hist. Volatility</p>
                                <p className="text-3xl font-semibold text-white">{(details?.volatility * 100).toFixed(2)}%</p>
                            </div>
                        </div>
                        {heatmapData && (
                            <Plot
                                data={[{
                                    z: heatmapData.prices,
                                    x: heatmapData.stock_price_axis,
                                    y: heatmapData.time_axis,
                                    type: 'surface',
                                    colorscale: 'Viridis',
                                    contours: {
                                        z: { show: true, usecolormap: true, highlightcolor: "#42f462", project: { z: true } }
                                    }
                                }]}
                                layout={{
                                    title: { text: `Theoretical Price Surface`, font: { color: '#e5e7eb', size: 18 }},
                                    scene: {
                                        // --- THIS IS THE CORRECTED STRUCTURE ---
                                        xaxis: { title: { text: 'Stock Price ($)' }, titlefont: { color: '#9ca3af' }, tickfont: { color: '#9ca3af' }, gridcolor: 'rgba(255,255,255,0.1)'},
                                        yaxis: { title: { text: 'Time to Expiration (Days)' }, titlefont: { color: '#9ca3af' }, tickfont: { color: '#9ca3af' }, gridcolor: 'rgba(255,255,255,0.1)'},
                                        zaxis: { title: { text: 'Option Price ($)' }, titlefont: { color: '#9ca3af' }, tickfont: { color: '#9ca3af' }, gridcolor: 'rgba(255,255,255,0.1)'}
                                    },
                                    paper_bgcolor: 'transparent',
                                    plot_bgcolor: 'transparent',
                                    autosize: true,
                                }}
                                useResizeHandler={true}
                                className="w-full h-[550px]"
                            />
                        )}
                        <button onClick={() => { setStep(2); setError(''); }} className="text-sm text-gray-400 hover:text-white w-full mt-4">Back to Strike Selection</button>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="bg-gray-900 text-white flex items-center justify-center min-h-screen p-4 font-sans">
            <div className="w-full max-w-5xl bg-gray-800 rounded-2xl shadow-2xl p-8 md:p-10">
                <div className="text-center mb-10">
                    <h1 className="text-4xl md:text-5xl font-bold text-cyan-400">Options Intelligence Platform</h1>
                    <p className="text-gray-400 mt-3 text-lg">Interactive 3D Pricing Surface</p>
                </div>

                <div className="bg-gray-900/50 rounded-lg p-8 min-h-[700px] ring-1 ring-white/10 flex flex-col justify-center">
                    {renderStepContent()}
                    {error && <p className="text-red-400 text-center mt-4 text-lg animate-fade-in">{error}</p>}
                </div>
            </div>
        </div>
    );
}
