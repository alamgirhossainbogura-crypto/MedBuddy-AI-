// Navigation Elements
const menuBtn = document.getElementById('menu-btn');
const backBtn = document.getElementById('back-btn');
const sideMenu = document.getElementById('side-menu');
const closeMenuBtn = document.getElementById('close-menu-btn');

// Sections
const homeSection = document.getElementById('home-section');
const aiSection = document.getElementById('ai-assistant-section');
const bmiSection = document.getElementById('bmi-calculator-section');
const guideSection = document.getElementById('disease-guide-section');
const pulseSection = document.getElementById('pulse-watch-section');

let currentDuration = 0;
let timerInterval = null;
let lastSelectedDuration = 30; // ডিফল্ট ৩০ সেকেন্ড ট্র্যাক রাখার জন্য

// Hamburger Menu Toggle
menuBtn.addEventListener('click', () => sideMenu.classList.add('active'));
closeMenuBtn.addEventListener('click', () => sideMenu.classList.remove('active'));

// Universal Section Switcher
function showSection(sectionName) {
    sideMenu.classList.remove('active');
    
    // Hide all
    homeSection.classList.add('hidden');
    aiSection.classList.add('hidden');
    bmiSection.classList.add('hidden');
    guideSection.classList.add('hidden');
    pulseSection.classList.add('hidden');
    
    // Show selected
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
        if(sectionName === 'pulse-watch') pulseSection.classList.remove('hidden');
    }
    // Stop timer if navigating away
    clearInterval(timerInterval);
    document.getElementById('timer-display').innerText = "00:00";
}

// Back Button Event
backBtn.addEventListener('click', () => showSection('home'));

// 1. DUMMY AI CHAT FUNCTION
function sendMessage() {
    const input = document.getElementById('chat-input');
    const box = document.getElementById('chat-box');
    if(!input.value.trim()) return;

    box.innerHTML += `<p style="align-self: flex-end; background: #00A8E8; color: white; padding: 10px; border-radius: 8px; max-width: 80%;">${input.value}</p>`;
    input.value = "";
    
    setTimeout(() => {
        box.innerHTML += `<p class="bot-msg">আপনার প্রম্পটটি সফল হয়েছে। (ব্যাকএন্ডে Gemini API কানেক্ট করলে এখানে রিয়েল অ্যানসার আসবে।)</p>`;
        box.scrollTop = box.scrollHeight;
    }, 1000);
}

// 2. BMI CALCULATOR FUNCTION
function calculateBMI() {
    const weight = parseFloat(document.getElementById('bmi-weight').value);
    const height = parseFloat(document.getElementById('bmi-height').value) / 100;
    const resultBox = document.getElementById('bmi-result');
    
    if(!weight || !height) return;
    const bmi = (weight / (height * height)).toFixed(2);
    
    resultBox.classList.remove('hidden');
    resultBox.style.backgroundColor = "var(--primary-light)";
    resultBox.style.color = "var(--primary-color)";
    resultBox.innerText = `আপনার BMI হলো: ${bmi}`;
}

// 4. PULSE RATE STOPWATCH & COLOR LOGIC
function startPulseTimer(seconds) {
    clearInterval(timerInterval);
    currentDuration = seconds;
    lastSelectedDuration = seconds; // ট্র্যাক রাখা হচ্ছে ৩০ নাকি ৬০
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
    const count = parseInt(document.getElementById('pulse-count').value);
    const resultBox = document.getElementById('pulse-result');
    if(!count) return;

    // ইউজার ৩০ সেকেন্ড সিলেক্ট করলে ২ দিয়ে গুণ হবে, ৬০ সেকেন্ড হলে যা গুনেছে তাই থাকবে
    let bpm = (lastSelectedDuration === 30) ? count * 2 : count;

    resultBox.classList.remove('hidden');
    
    // কন্ডিশনাল কালার লজিক (স্বাভাবিক = সবুজ, অস্বাভাবিক = লাল)
    if(bpm >= 60 && bpm <= 100) {
        resultBox.style.backgroundColor = "rgba(16, 185, 129, 0.1)";
        resultBox.style.color = "var(--normal-green)";
        resultBox.style.border = "1px solid var(--normal-green)";
        resultBox.innerText = `আপনার পালস রেট স্বাভাবিক: ${bpm} BPM`;
    } else {
        resultBox.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
        resultBox.style.color = "var(--abnormal-red)";
        resultBox.style.border = "1px solid var(--abnormal-red)";
        resultBox.innerText = `আপনার পালস রেট অস্বাভাবিক: ${bpm} BPM! চিকিৎসকের পরামর্শ নিন।`;
    }
}
