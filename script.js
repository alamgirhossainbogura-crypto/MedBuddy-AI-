// Navigation & Core Elements
const menuBtn = document.getElementById('menu-btn');
const backBtn = document.getElementById('back-btn');
const themeBtn = document.getElementById('theme-btn');
const sideMenu = document.getElementById('side-menu');
const closeMenuBtn = document.getElementById('close-menu-btn');

// App Sections
const homeSection = document.getElementById('home-section');
const aiSection = document.getElementById('ai-assistant-section');
const bmiSection = document.getElementById('bmi-calculator-section');
const guideSection = document.getElementById('disease-guide-section');
const pulseSection = document.getElementById('pulse-watch-section');

let currentDuration = 0;
let timerInterval = null;
let lastSelectedDuration = 30;

// 2. Real-Time Dark Mode Toggle Logic
themeBtn.addEventListener('click', () => {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    if (isDark) {
        document.body.removeAttribute('data-theme');
        themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', 'light');
    } else {
        document.body.setAttribute('data-theme', 'dark');
        themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem('theme', 'dark');
    }
});

// Load Cached Theme on Startup
if (localStorage.getItem('theme') === 'dark') {
    document.body.setAttribute('data-theme', 'dark');
    themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
}

// Drawer Toggle Handlers
menuBtn.addEventListener('click', () => sideMenu.classList.add('active'));
closeMenuBtn.addEventListener('click', () => sideMenu.classList.remove('active'));

// Universal Component App Routing Switcher
function showSection(sectionName) {
    sideMenu.classList.remove('active');
    
    homeSection.classList.add('hidden');
    aiSection.classList.add('hidden');
    bmiSection.classList.add('hidden');
    guideSection.classList.add('hidden');
    pulseSection.classList.add('hidden');
    
    if(sectionName === 'home') {
        homeSection.classList.remove('hidden');
        backBtn.classList.add('hidden');
        menuBtn.classList.remove('hidden');
    } else {
        backBtn.classList.remove('hidden');
        menuBtn.classList.add('hidden');
        
        if(sectionName === 'ai-assistant') aiSection.classList.remove('hidden');
        if(sectionName === 'bmi-calculator') bmiSection.classList.remove('hidden');
        if(sectionName === 'disease-guide') guideSection.classList.remove('hidden');
        if(sectionName === 'pulse-watch') {
            pulseSection.classList.remove('hidden');
            loadPulseHistory(); // ওপেন করার সময় হিস্ট্রি লোড হবে
        }
    }
    clearInterval(timerInterval);
    document.getElementById('timer-display').innerText = "00:00";
}

backBtn.addEventListener('click', () => showSection('home'));

// 1. AI CHAT WINDOW WITH 4. TYPING LOADER ANIMATION
function sendMessage() {
    const input = document.getElementById('chat-input');
    const box = document.getElementById('chat-box');
    const loader = document.getElementById('chat-loader');
    if(!input.value.trim()) return;

    box.innerHTML += `<p style="align-self: flex-end; background: #00A8E8; color: white; padding: 10px; border-radius: 8px; max-width: 80%;">${input.value}</p>`;
    const userMsg = input.value;
    input.value = "";
    box.scrollTop = box.scrollHeight;
    
    // শো লোডার অ্যানিমেশন
    loader.classList.remove('hidden');
    box.scrollTop = box.scrollHeight;
    
    setTimeout(() => {
        // লোডার হাইড করুন
        loader.classList.add('hidden');
        box.innerHTML += `<p class="bot-msg">MedBuddy AI আপনার মেসেজটি পেয়েছে। ব্যাকএন্ডে Gemini API কানেক্ট করলে এখানে মূল রেসপন্স আসবে।</p>`;
        box.scrollTop = box.scrollHeight;
    }, 1500); // ১.৫ সেকেন্ডের রিয়েলস্টিক ডিলে
}

// 2. HEALTH BODY MASS CALCULATORS
function calculateBMI() {
    const weight = parseFloat(document.getElementById('bmi-weight').value);
    const height = parseFloat(document.getElementById('bmi-height').value) / 100;
    const resultBox = document.getElementById('bmi-result');
    
    if(!weight || !height) return;
    const bmi = (weight / (height * height)).toFixed(2);
    
    resultBox.classList.remove('hidden');
    resultBox.style.backgroundColor = "var(--primary-light)";
    resultBox.style.color = "var(--text-color)";
    resultBox.innerText = `আপনার BMI হলো: ${bmi}`;
}

// 4. HEARTBEAT PULSE METERS
function startPulseTimer(seconds) {
    clearInterval(timerInterval);
    currentDuration = seconds;
    lastSelectedDuration = seconds;
    const display = document.getElementById('timer-display');
    document.getElementById('pulse-input-box').classList.add('hidden');
    document.getElementById('pulse-result').classList.add('hidden');

    timerInterval = setInterval(() => {
        currentDuration--;
        let displaySec = currentDuration < 10 ? "0" + currentDuration : currentDuration;
        display.innerText = `00:${displaySec}`;

        if(currentDuration <= 0) {
            clearInterval(timerInterval);
            document.getElementById('pulse-input-box').classList.remove('hidden');
        }
    }, 1000);
}

function calculateBPM() {
    const countInput = document.getElementById('pulse-count');
    const count = parseInt(countInput.value);
    const resultBox = document.getElementById('pulse-result');
    if(!count) return;

    let bpm = (lastSelectedDuration === 30) ? count * 2 : count;
    resultBox.classList.remove('hidden');
    
    let status = "";
    if(bpm >= 60 && bpm <= 100) {
        resultBox.style.backgroundColor = "rgba(16, 185, 129, 0.1)";
        resultBox.style.color = "var(--normal-green)";
        resultBox.style.border = "1px solid var(--normal-green)";
        resultBox.innerText = `আপনার পালস রেট স্বাভাবিক: ${bpm} BPM`;
        status = "স্বাভাবিক";
    } else {
        resultBox.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
        resultBox.style.color = "var(--abnormal-red)";
        resultBox.style.border = "1px solid var(--abnormal-red)";
        resultBox.innerText = `আপনার পালস রেট অস্বাভাবিক: ${bpm} BPM! চিকিৎসকের পরামর্শ নিন।`;
        status = "অস্বাভাবিক";
    }

    // 3. Save to Pulse Local Storage History Logs
    savePulseRecord(bpm, status);
    countInput.value = "";
}

// Local Storage History Management
function savePulseRecord(bpm, status) {
    let history = JSON.parse(localStorage.getItem('pulseHistory')) || [];
    const now = new Date();
    const timeString = now.toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' });
    
    history.unshift({ bpm, status, time: timeString });
    if(history.length > 5) history.pop(); // শেষ ৫টি রেকর্ড রাখবে
    
    localStorage.setItem('pulseHistory', JSON.stringify(history));
    loadPulseHistory();
}

function loadPulseHistory() {
    const list = document.getElementById('pulse-history-list');
    let history = JSON.parse(localStorage.getItem('pulseHistory')) || [];
    list.innerHTML = "";
    
    if(history.length === 0) {
        list.innerHTML = `<li class="history-item" style="color:var(--text-muted)">কোনো রেকর্ড পাওয়া যায়নি</li>`;
        return;
    }

    history.forEach(item => {
        const color = item.status === "স্বাভাবিক" ? "var(--normal-green)" : "var(--abnormal-red)";
        list.innerHTML += `
            <li class="history-item">
                <span><i class="fas fa-heartbeat" style="color:${color}"></i> ${item.bpm} BPM (${item.status})</span>
                <span style="color:var(--text-muted); font-size:0.8rem">${item.time}</span>
            </li>
        `;
    });
}

function clearPulseHistory() {
    localStorage.removeItem('pulseHistory');
    loadPulseHistory();
}
