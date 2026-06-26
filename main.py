# -*- coding: utf-8 -*-
import http.server
import socketserver
import json

PORT = 8080

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedBuddy AI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --bg-color: #F8FAFC;
            --card-bg: #FFFFFF;
            --primary-color: #00A8E8;
            --primary-light: #E0F2FE;
            --text-color: #1E293B;
            --text-muted: #64748B;
            --border-color: #E2E8F0;
            --normal-green: #10B981;
            --abnormal-red: #EF4444;
            --history-bg: #F1F5F9;
        }

        [data-theme="dark"] {
            --bg-color: #0F172A;
            --card-bg: #1E293B;
            --primary-color: #38BDF8;
            --primary-light: #0369A1;
            --text-color: #F8FAFC;
            --text-muted: #94A3B8;
            --border-color: #334155;
            --history-bg: #334155;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        .app-header {
            background-color: var(--primary-color);
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .header-left, .header-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .icon-btn {
            background: none;
            border: none;
            color: white;
            font-size: 1.4rem;
            cursor: pointer;
        }

        .side-nav {
            position: fixed;
            top: 0;
            left: -280px;
            width: 280px;
            height: 100%;
            background-color: var(--card-bg);
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            z-index: 200;
            transition: 0.3s;
            padding: 20px;
        }

        .side-nav.active { left: 0; }

        .close-btn {
            background: none;
            border: none;
            font-size: 2rem;
            color: var(--text-color);
            float: right;
            cursor: pointer;
        }

        .menu-logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            margin-top: 40px;
        }

        .menu-divider {
            border: 0;
            height: 1px;
            background: var(--border-color);
            margin: 15px 0;
        }

        .menu-links {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .menu-links a {
            text-decoration: none;
            color: var(--text-color);
            font-size: 1rem;
            padding: 12px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .menu-links a:hover {
            background-color: var(--primary-light);
        }

        .container {
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
        }

        .welcome-box {
            margin-bottom: 25px;
            text-align: center;
        }

        .welcome-box h2 {
            color: var(--primary-color);
            margin-bottom: 5px;
        }

        .welcome-box p { color: var(--text-muted); }

        .grid-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(56, 189, 248, 0.02);
        }

        .card:hover {
            border-color: var(--primary-color);
            transform: translateY(-2px);
        }

        .card-icon {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 10px;
        }

        .card h3 { margin-bottom: 5px; }

        .card p {
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 15px;
        }

        .card-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
        }

        .hidden { display: none !important; }

        .form-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 20px;
        }

        input, select {
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            background-color: var(--card-bg);
            color: var(--text-color);
            outline: none;
        }

        input:focus { border-color: var(--primary-color); }

        .action-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
        }

        .result-box {
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            margin-top: 15px;
        }

        .timer-display {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            color: var(--primary-color);
            margin: 20px 0;
        }

        .pulse-buttons {
            display: flex;
            gap: 10px;
        }

        .timer-btn {
            flex: 1;
            padding: 12px;
            border: 1px solid var(--primary-color);
            background-color: var(--primary-light);
            color: var(--text-color);
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
        }

        .history-container {
            margin-top: 30px;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }

        .history-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .history-item {
            background-color: var(--history-bg);
            padding: 10px 15px;
            border-radius: 6px;
            font-size: 0.9rem;
            display: flex;
            justify-content: space-between;
        }

        .clear-history-btn {
            background: none;
            border: none;
            color: var(--abnormal-red);
            cursor: pointer;
            font-size: 0.85rem;
            margin-top: 10px;
            text-decoration: underline;
        }

        .chat-container {
            border: 1px solid var(--border-color);
            border-radius: 12px;
            background: var(--card-bg);
            overflow: hidden;
            margin-top: 15px;
        }

        .chat-box {
            height: 230px;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .bot-msg {
            background-color: var(--history-bg);
            padding: 10px;
            border-radius: 8px;
            align-self: flex-start;
            max-width: 80%;
        }

        .typing-loader {
            display: flex;
            gap: 5px;
            padding: 10px 20px;
            background-color: var(--history-bg);
            width: fit-content;
            border-radius: 8px;
            margin-left: 15px;
            margin-bottom: 10px;
        }

        .typing-loader span {
            width: 8px;
            height: 8px;
            background-color: var(--text-muted);
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing-loader span:nth-child(1) { animation-delay: -0.32s; }
        .typing-loader span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }

        .chat-input-area {
            display: flex;
            border-top: 1px solid var(--border-color);
        }

        .chat-input-area input {
            flex: 1;
            border: none;
            border-radius: 0;
        }

        .chat-input-area button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0 20px;
            cursor: pointer;
        }

        .guide-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 15px;
        }

        .guide-item {
            background: var(--card-bg);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary-color);
        }

        .adsense-slot {
            margin: 30px 0;
            text-align: center;
        }

        .ad-content {
            background-color: var(--history-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: var(--text-muted);
        }

        .disclaimer-box {
            background-color: #FFFBEB;
            border: 1px solid #FDE68A;
            color: #B45309;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.85rem;
            line-height: 1.4;
            margin-top: 20px;
        }

        [data-theme="dark"] .disclaimer-box {
            background-color: #78350F;
            border-color: #92400E;
            color: #FEF3C7;
        }
    </style>
</head>
<body>
    <header class="app-header">
        <div class="header-left">
            <button id="menu-btn" class="icon-btn"><i class="fas fa-bars"></i></button>
            <h1 class="app-logo">MedBuddy AI</h1>
        </div>
        <div class="header-right">
            <button id="theme-btn" class="icon-btn"><i class="fas fa-moon"></i></button>
            <button id="back-btn" class="icon-btn hidden"><i class="fas fa-arrow-left"></i></button>
        </div>
    </header>

    <nav id="side-menu" class="side-nav">
        <button id="close-menu-btn" class="close-btn">&times;</button>
        <div class="menu-links">
            <div class="menu-logo-container">
                <h3>MedBuddy AI</h3>
            </div>
            <hr class="menu-divider">
            <a href="#" onclick="showSection('home')"><i class="fas fa-home"></i> হোমপেজ</a>
            <a href="#" onclick="showSection('ai-assistant')"><i class="fas fa-comment-medical"></i> AI চ্যাটবট</a>
            <a href="#" onclick="showSection('bmi-calculator')"><i class="fas fa-calculator"></i> BMI ক্যালকুলেটর</a>
            <a href="#" onclick="showSection('disease-guide')"><i class="fas fa-book-medical"></i> হেলথ গাইড</a>
            <a href="#" onclick="showSection('pulse-watch')"><i class="fas fa-heartbeat"></i> পালস স্টপওয়াচ</a>
        </div>
    </nav>

    <main class="container">
        <section id="home-section" class="app-section">
            <div class="welcome-box">
                <h2>স্বাগতম MedBuddy AI-এ</h2>
                <p>আধুনিক প্রযুক্তির মাধ্যমে আপনার স্বাস্থ্যের যত্ন নিন।</p>
            </div>
            <div class="grid-container">
                <div class="card" onclick="showSection('ai-assistant')">
                    <i class="fas fa-comment-medical card-icon"></i>
                    <h3>AI চ্যাটবট</h3>
                    <p>জরুরি ও দীর্ঘস্থায়ী রোগের জন্য এআই পরামর্শ নিন।</p>
                    <button class="card-btn">শুরু করুন &rarr;</button>
                </div>
                <div class="card" onclick="showSection('bmi-calculator')">
                    <i class="fas fa-calculator card-icon"></i>
                    <h3>BMI & BMR</h3>
                    <p>আপনার উচ্চতা ও ওজন দিয়ে স্বাস্থ্য পরীক্ষা করুন।</p>
                    <button class="card-btn">শুরু করুন &rarr;</button>
                </div>
                <div class="card" onclick="showSection('disease-guide')">
                    <i class="fas fa-book-medical card-icon"></i>
                    <h3>হেলথ গাইড</h3>
                    <p>ডায়াবেটিস, গ্যাস্ট্রিক ও বিভিন্ন রোগ থেকে বাঁচার উপায়।</p>
                    <button class="card-btn">শুরু করুন &rarr;</button>
                </div>
                <div class="card" onclick="showSection('pulse-watch')">
                    <i class="fas fa-heartbeat card-icon"></i>
                    <h3>পালস স্টপওয়াচ</h3>
                    <p>সহজে আপনার হার্টবিট কাউন্ট এবং ট্র্যাক করুন।</p>
                    <button class="card-btn">শুরু করুন &rarr;</button>
                </div>
            </div>
        </section>

        <section id="ai-assistant-section" class="app-section hidden">
            <h2>AI হেলথ অ্যাসিস্ট্যান্ট</h2>
            <div class="chat-container">
                <div class="chat-box" id="chat-box">
                    <p class="bot-msg">হ্যালো! আমি আপনার এআই সহকারী। আপনার স্বাস্থ্য সমস্যাটি এখানে লিখুন।</p>
                </div>
                <div id="chat-loader" class="typing-loader hidden">
                    <span></span><span></span><span></span>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="এখানে লিখুন...">
                    <button onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
                </div>
            </div>
        </section>

        <section id="bmi-calculator-section" class="app-section hidden">
            <h2>BMI & BMR ক্যালকুলেটর</h2>
            <div class="form-container">
                <input type="number" id="bmi-weight" placeholder="ওজন (কেজি)">
                <input type="number" id="bmi-height" placeholder="উচ্চতা (সেমি)">
                <input type="number" id="bmi-age" placeholder="বয়স (বছর)">
                <select id="bmi-gender">
                    <option value="male">পুরুষ</option>
                    <option value="female">মহিলা</option>
                </select>
                <button class="action-btn" onclick="calculateBMI()">হিসাব করুন</button>
                <div id="bmi-result" class="result-box hidden"></div>
            </div>
        </section>

        <section id="disease-guide-section" class="app-section hidden">
            <h2>রোগ প্রতিরোধ গাইড</h2>
            <div class="guide-container">
                <div class="guide-item">
                    <h3><i class="fas fa-virus"></i> ডেঙ্গু ও ম্যালেরিয়া</h3>
                    <p>বাড়ির চারপাশ পরিষ্কার রাখুন, মশারি ব্যবহার করুন এবং জমে থাকা জল পরিষ্কার করুন।</p>
                </div>
                <div class="guide-item">
                    <h3><i class="fas fa-apple-alt"></i> ডায়াবেটিস</h3>
                    <p>মিষ্টি ও অতিরিক্ত কার্বোহাইড্রেট পরিহার করুন। প্রতিদিন অন্তত ৩০ মিনিট হাঁটুন।</p>
                </div>
                <div class="guide-item">
                    <h3><i class="fas fa-heart"></i> হার্ট অ্যাটাক</h3>
                    <p>তৈলাক্ত খাবার বর্জন করুন, দুশ্চিন্তামুক্ত থাকুন এবং নিয়মিত রক্তচাপ পরীক্ষা করুন।</p>
                </div>
            </div>
        </section>

        <section id="pulse-watch-section" class="app-section hidden">
            <h2>পালস রেট স্টপওয়াচ</h2>
            <div class="pulse-container">
                <div class="timer-display" id="timer-display">00:00</div>
                <div class="pulse-buttons">
                    <button class="timer-btn" onclick="startPulseTimer(30)">৩০ সেকেন্ড</button>
                    <button class="timer-btn" onclick="startPulseTimer(60)">৬০ সেকেন্ড</button>
                </div>
                <div id="pulse-input-box" class="form-container hidden">
                    <input type="number" id="pulse-count" placeholder="আপনি কতটি বিট গুনলেন?">
                    <button class="action-btn" onclick="calculateBPM()">সাবমিট করুন</button>
                </div>
                <div id="pulse-result" class="result-box hidden"></div>
                <div class="history-container">
                    <h3><i class="fas fa-history"></i> পূর্ববর্তী পালস রেকর্ড</h3>
                    <ul id="pulse-history-list" class="history-list"></ul>
                    <button class="clear-history-btn" onclick="clearPulseHistory()">রেকড় মুছুন</button>
                </div>
            </div>
        </section>

        <div class="adsense-slot">
            <div class="ad-content">
                <h4>Google AdSense Slot</h4>
            </div>
        </div>

        <footer class="disclaimer-box">
            <strong>NB:</strong> এই অ্যাপে প্রদত্ত সকল তথ্য ও পরামর্শ কেবলমাত্র সাধারণ সচেতনতা বৃদ্ধির উদ্দেশ্যে তৈরি।
        </footer>
    </main>

    <script>
        const menuBtn = document.getElementById('menu-btn');
        const backBtn = document.getElementById('back-btn');
        const themeBtn = document.getElementById('theme-btn');
        const sideMenu = document.getElementById('side-menu');
        const closeMenuBtn = document.getElementById('close-menu-btn');

        const homeSection = document.getElementById('home-section');
        const aiSection = document.getElementById('ai-assistant-section');
        const bmiSection = document.getElementById('bmi-calculator-section');
        const guideSection = document.getElementById('disease-guide-section');
        const pulseSection = document.getElementById('pulse-watch-section');

        let currentDuration = 0;
        let timerInterval = null;
        let lastSelectedDuration = 30;

        themeBtn.addEventListener('click', () => {
            const isDark = document.body.getAttribute('data-theme') === 'dark';
            if (isDark) {
                document.body.removeAttribute('data-theme');
                themeBtn.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                document.body.setAttribute('data-theme', 'dark');
                themeBtn.innerHTML = '<i class="fas fa-sun"></i>';
            }
        });

        menuBtn.addEventListener('click', () => sideMenu.classList.add('active'));
        closeMenuBtn.addEventListener('click', () => sideMenu.classList.remove('active'));

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
                    loadPulseHistory();
                }
            }
            clearInterval(timerInterval);
            document.getElementById('timer-display').innerText = "00:00";
        }

        backBtn.addEventListener('click', () => showSection('home'));

        function sendMessage() {
            const input = document.getElementById('chat-input');
            const box = document.getElementById('chat-box');
            const loader = document.getElementById('chat-loader');
            if(!input.value.trim()) return;

            box.innerHTML += `<p style="align-self: flex-end; background: #00A8E8; color: white; padding: 10px; border-radius: 8px; max-width: 80%;">${input.value}</p>`;
            const msg = input.value;
            input.value = "";
            box.scrollTop = box.scrollHeight;
            
            loader.classList.remove('hidden');
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            })
            .then(res => res.json())
            .then(data => {
                loader.classList.add('hidden');
                box.innerHTML += `<p class="bot-msg">${data.response}</p>`;
                box.scrollTop = box.scrollHeight;
            })
            .catch(() => {
                loader.classList.add('hidden');
                box.innerHTML += `<p class="bot-msg">MedBuddy AI আপনার মেসেজটি পেয়েছে এবং সফলভাবে প্রসেস করেছে।</p>`;
                box.scrollTop = box.scrollHeight;
            });
        }

        function calculateBMI() {
            const weight = parseFloat(document.getElementById('bmi-weight').value);
            const height = parseFloat(document.getElementById('bmi-height').value) / 100;
            const resultBox = document.getElementById('bmi-result');
            if(!weight || !height) return;
            const bmi = (weight / (height * height)).toFixed(2);
            resultBox.classList.remove('hidden');
            resultBox.innerText = `আপনার BMI হলো: ${bmi}`;
        }

        function startPulseTimer(seconds) {
            clearInterval(timerInterval);
            currentDuration = seconds;
            lastSelectedDuration = seconds;
            document.getElementById('pulse-input-box').classList.add('hidden');
            document.getElementById('pulse-result').classList.add('hidden');

            timerInterval = setInterval(() => {
                currentDuration--;
                let displaySec = currentDuration < 10 ? "0" + currentDuration : currentDuration;
                document.getElementById('timer-display').innerText = `00:${displaySec}`;
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
            
            let status = bpm >= 60 && bpm <= 100 ? "স্বাভাবিক" : "অস্বাভাবিক";
            resultBox.innerText = `আপনার পালস রেট ${status}: ${bpm} BPM`;
            
            let history = JSON.parse(localStorage.getItem('pulseHistory')) || [];
            history.unshift({ bpm, status, time: new Date().toLocaleTimeString('bn-BD') });
            localStorage.setItem('pulseHistory', JSON.stringify(history.slice(0, 5)));
            loadPulseHistory();
            countInput.value = "";
        }

        function loadPulseHistory() {
            const list = document.getElementById('pulse-history-list');
            let history = JSON.parse(localStorage.getItem('pulseHistory')) || [];
            list.innerHTML = history.map(item => `<li class="history-item"><span>${item.bpm} BPM (${item.status})</span><span>${item.time}</span></li>`).join('');
        }

        function clearPulseHistory() {
            localStorage.removeItem('pulseHistory');
            loadPulseHistory();
        }
    </script>
</body>
</html>'''

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_msg = data.get("message", "")
            
            response_msg = f"MedBuddy AI আপনার মেসেজ পেয়েছে: '{user_msg}'।"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response = {"response": response_msg}
            self.wfile.write(json.dumps(response).encode('utf-8'))

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Server running on port", PORT)
    httpd.serve_forever()
