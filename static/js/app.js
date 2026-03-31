/**
 * Kinshuk Garg Neural Intelligence — Frontend Application Logic
 * =============================================================
 * Handles form interaction, API uplink, and 3D glass physics.
 */

// ──────────────────────────────────────────────
// CONSTANTS & STATE
// ──────────────────────────────────────────────
const API_BASE = '';
const state = {
    bedrooms: 3,
    bathrooms: 2,
    stories: 2,
    parking: 1,
    furnishingstatus: 'semi-furnished',
    modelInfo: null,
};

// ──────────────────────────────────────────────
// INITIALIZATION
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initSelectors();
    initForm();
    initScrollReveal();
    initCounters();
    initTiltPhysics();
    loadLocations();
    loadModelInfo();
});

// ──────────────────────────────────────────────
// GLASS PHYSICS (Vanilla Tilt)
// ──────────────────────────────────────────────
function initTiltPhysics() {
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".glass-card"), {
            max: 20,
            speed: 400,
            glare: true,
            "max-glare": 0.1,
            scale: 1.05
        });

        VanillaTilt.init(document.querySelectorAll(".glass-panel"), {
            max: 5,
            speed: 1000,
            glare: true,
            "max-glare": 0.05,
        });
    }
}

// ──────────────────────────────────────────────
// NAVBAR SCROLL EFFECT
// ──────────────────────────────────────────────
function initNavbar() {
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 30);
    });
}

// ──────────────────────────────────────────────
// BUTTON SELECTORS (CYBER BUTTONS)
// ──────────────────────────────────────────────
function initSelectors() {
    document.querySelectorAll('.btn-selector').forEach(selector => {
        const field = selector.dataset.field;
        selector.querySelectorAll('.selector-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                // Remove active from siblings
                selector.querySelectorAll('.selector-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state[field] = btn.dataset.value;
            });
        });
    });
}

// ──────────────────────────────────────────────
// FORM SUBMISSION (UPLINK)
// ──────────────────────────────────────────────
function initForm() {
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitPrediction();
    });
}

async function submitPrediction() {
    const btn = document.getElementById('predict-btn');
    btn.classList.add('loading');

    const payload = {
        location: document.getElementById('location').value,
        area: parseFloat(document.getElementById('area').value),
        bedrooms: parseInt(state.bedrooms),
        bathrooms: parseInt(state.bathrooms),
        stories: parseInt(state.stories),
        parking: parseInt(state.parking),
        furnishingstatus: state.furnishingstatus,
        property_age: parseInt(document.getElementById('property_age').value),
        mainroad: document.getElementById('mainroad').checked ? 1 : 0,
        guestroom: document.getElementById('guestroom').checked ? 1 : 0,
        basement: document.getElementById('basement').checked ? 1 : 0,
        hotwaterheating: document.getElementById('hotwaterheating').checked ? 1 : 0,
        airconditioning: document.getElementById('airconditioning').checked ? 1 : 0,
        prefarea: document.getElementById('prefarea').checked ? 1 : 0,
    };

    try {
        const res = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await res.json();

        if (data.success) {
            showResult(data, payload);
        } else {
            alert('Compute Warning: ' + (data.error || 'Anomaly detected.'));
        }
    } catch (err) {
        alert('Network Anomaly: ' + err.message);
    } finally {
        btn.classList.remove('loading');
    }
}

// ──────────────────────────────────────────────
// SHOW PREDICTION RESULT (SLOT ANIMATION)
// ──────────────────────────────────────────────
function showResult(data, payload) {
    const placeholder = document.getElementById('result-placeholder');
    const content = document.getElementById('result-content');

    placeholder.classList.add('hidden');
    content.classList.remove('hidden');

    // Slot Machine Price Counter
    animatePriceSlot(document.getElementById('price-amount'), data.predicted_price);

    // Price range bounds
    document.getElementById('price-low').textContent = data.formatted_range.low;
    document.getElementById('price-high').textContent = data.formatted_range.high;

    // Animate Scanner Bar
    setTimeout(() => {
        document.getElementById('range-fill').style.width = '100%';
    }, 400);

    // Details Ledger
    document.getElementById('detail-location').textContent = payload.location;
    document.getElementById('detail-area').textContent = `${payload.area.toLocaleString()} Sq.Ft`;
    document.getElementById('detail-config').textContent = `${payload.bedrooms} BR, ${payload.bathrooms} BA`;
    document.getElementById('detail-age').textContent = payload.property_age === 0 ? 'NEURAL INIT' : `T-${payload.property_age} Cycles`;

    // Scroll to result on mobile
    if (window.innerWidth < 1024) {
        document.getElementById('result-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function resetForm() {
    const placeholder = document.getElementById('result-placeholder');
    const content = document.getElementById('result-content');

    content.classList.add('hidden');
    placeholder.classList.remove('hidden');

    // Reset range scanner
    document.getElementById('range-fill').style.width = '0%';
}

// ──────────────────────────────────────────────
// SCROLL REVEAL (INTERSECTION OBSERVER)
// ──────────────────────────────────────────────
function initScrollReveal() {
    const revealTargets = document.querySelectorAll('.fade-up, .slide-left, .slide-right, .slide-up');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Don't unobserve if we want repeat animations, but standard is unobserve
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    revealTargets.forEach(el => {
        observer.observe(el);
    });
}

// ──────────────────────────────────────────────
// HARDWARE DECELERATING COUNTERS 
// ──────────────────────────────────────────────
function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                let targetNum = el.dataset.target;
                
                if (targetNum === "95") {
                    // It's the R2 counter. If model was loaded, we update it.
                    if (state.modelInfo) {
                        const bestModel = state.modelInfo.best_model;
                        const bestR2 = state.modelInfo.model_results[bestModel].r2;
                        targetNum = Math.round(bestR2 * 100).toString();
                    }
                }
                
                animateStatCounter(el, parseInt(targetNum));
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(c => observer.observe(c));
}

function animateStatCounter(el, target) {
    const duration = 2500;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 5); // Intense ease-out
        el.textContent = Math.round(target * eased);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// Slot Machine Style Price Animator
function animatePriceSlot(el, target) {
    const duration = 2000;
    const start = performance.now();
    const characters = '0123456789';

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        
        const current = Math.round(target * eased);
        const targetStr = current.toLocaleString('en-IN');
        
        if (progress < 1) {
            // Scramble random numbers into string length
            let scrambled = '';
            for(let i=0; i<targetStr.length; i++) {
                if (targetStr[i] === ',') {
                    scrambled += ',';
                } else if (Math.random() > progress) {
                    scrambled += characters[Math.floor(Math.random() * characters.length)];
                } else {
                    scrambled += targetStr[i];
                }
            }
            el.textContent = scrambled;
            requestAnimationFrame(update);
        } else {
            el.textContent = target.toLocaleString('en-IN');
        }
    }
    requestAnimationFrame(update);
}


// ──────────────────────────────────────────────
// LOAD LOCATIONS
// ──────────────────────────────────────────────
async function loadLocations() {
    try {
        const res = await fetch(`${API_BASE}/api/locations`);
        const data = await res.json();

        if (data.success) {
            const select = document.getElementById('location');
            select.innerHTML = '<option value="">Select Vector Location...</option>';
            data.locations.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = `${loc.toUpperCase()} [ACTIVE]`;
                select.appendChild(opt);
            });
            
            // Auto select for better UX in demo
            if (data.locations.length > 0) {
                setTimeout(() => { select.value = data.locations[0]; }, 500);
            }
        }
    } catch (err) {
        console.error('Core Logic Error:', err);
        const select = document.getElementById('location');
        select.innerHTML = '<option value="Whitefield">WHITEFIELD [FALLBACK LOCAL]</option>';
    }
}


// ──────────────────────────────────────────────
// LOAD MODEL DATA & TELEMETRY
// ──────────────────────────────────────────────
async function loadModelInfo() {
    try {
        const res = await fetch(`${API_BASE}/api/model-info`);
        const data = await res.json();

        if (data.success) {
            state.modelInfo = data;
            renderModelCards(data);
            renderFeatureImportance(data.feature_importance);
        }
    } catch (err) {
        console.error('DB Init Error:', err);
    }
}

function renderModelCards(data) {
    const grid = document.getElementById('models-grid');
    grid.innerHTML = '';
    const order = ['Linear Regression', 'Decision Tree', 'Random Forest'];

    order.forEach((name, idx) => {
        const metrics = data.model_results[name];
        const isBest = name === data.best_model;
        const delay = idx * 0.2; // Staggered entry

        const card = document.createElement('div');
        // Add fade-up and inline delay for staggering
        card.className = `model-card glass-panel fade-up ${isBest ? 'best' : ''}`;
        card.style.transitionDelay = `${delay}s`;
        
        card.innerHTML = `
            ${isBest ? '<span class="best-badge glitch-badge" data-text="OPTIMIZED_NODE">OPTIMIZED_NODE</span>' : ''}
            <div class="model-name glow-text">${name}</div>
            
            <div class="metric-row">
                <span class="metric-name">Convergence (R²)</span>
                <span class="metric-value${isBest ? ' highlight' : ''}">${metrics.r2.toFixed(4)}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Mean Error (MAE)</span>
                <span class="metric-value">₹${formatNum(metrics.mae)}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Sq Root Error (RMSE)</span>
                <span class="metric-value">₹${formatNum(metrics.rmse)}</span>
            </div>
            <div class="metric-row">
                <span class="metric-name">Cross Validate Matrix</span>
                <span class="metric-value">${metrics.cv_mean.toFixed(4)}</span>
            </div>
        `;
        grid.appendChild(card);
    });
    
    // Quick trick to trigger observer for dynamically added elements
    setTimeout(() => {
        const obs = new IntersectionObserver(ents => {
            ents.forEach(e => { if (e.isIntersecting) e.target.classList.add('is-visible'); });
        });
        document.querySelectorAll('.model-card').forEach(c => obs.observe(c));
    }, 100);
}

function renderFeatureImportance(importances) {
    const chart = document.getElementById('importance-chart');
    chart.innerHTML = '';
    const entries = Object.entries(importances).sort((a, b) => b[1] - a[1]);
    const maxVal = Math.max(...entries.map(([, v]) => v));

    entries.forEach(([feature, value], i) => {
        const pct = (value / maxVal) * 100;
        const tier = i < 3 ? 'top' : i < 7 ? 'mid' : 'low';

        const bar = document.createElement('div');
        bar.className = `importance-bar`;
        bar.innerHTML = `
            <span class="importance-label">${formatFeatureName(feature)}</span>
            <div class="importance-track">
                <div class="importance-fill ${tier}" style="width: 0%"></div>
            </div>
            <span class="importance-value glow-text">${(value * 100).toFixed(1)}%</span>
        `;
        chart.appendChild(bar);

        // Slide the physics bar
        setTimeout(() => {
            bar.querySelector('.importance-fill').style.width = pct + '%';
        }, 500 + i * 150);
    });
}

// ──────────────────────────────────────────────
// UTILITIES
// ──────────────────────────────────────────────
function formatNum(num) {
    if (num >= 10000000) return (num / 10000000).toFixed(2) + ' Cr';
    if (num >= 100000)   return (num / 100000).toFixed(2) + ' L';
    if (num >= 1000)     return (num / 1000).toFixed(1) + 'K';
    return num.toLocaleString();
}

function formatFeatureName(name) {
    const map = {
        'area': 'Scale Vector',
        'bedrooms': 'Topology (Beds)',
        'bathrooms': 'Hydration Units',
        'stories': 'Vertical Stacks',
        'mainroad': 'Grid Access',
        'guestroom': 'Auxiliary Node',
        'basement': 'Sub-Level',
        'hotwaterheating': 'Thermal Unit',
        'airconditioning': 'Cooling Node',
        'parking': 'Transport Dock',
        'prefarea': 'Premium Zone',
        'furnishingstatus': 'Asset Status',
        'location': 'Geo-Matrix',
        'property_age': 'Cycle Decay',
        'total_rooms': 'Total Capacity',
    };
    return map[name] || name.toUpperCase();
}
