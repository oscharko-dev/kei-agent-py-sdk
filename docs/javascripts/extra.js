// Extra JavaScript für KEI-Agent SDK Dokumentation

document.addEventListener('DOMContentLoaded', function() {
    // Code Copy Functionality Enhancement
    enhanceCodeBlocks();

    // API Signature Highlighting
    highlightAPISignatures();

    // Interactive Examples
    setupInteractiveExamples();

    // Search Enhancement
    enhanceSearch();

    // Navigation Enhancement
    enhanceNavigation();

    // Performance Monitoring
    setupPerformanceMonitoring();
});

/**
 * Erweitert Code-Blöcke mit zusätzlicher Funktionalität
 */
function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll('.highlight');

    codeBlocks.forEach(block => {
        // Sprache-Label hinzufügen
        const code = block.querySelector('code');
        if (code && code.className) {
            const language = code.className.match(/language-(\w+)/);
            if (language) {
                const label = document.createElement('div');
                label.className = 'code-language-label';
                label.textContent = language[1].toUpperCase();
                label.style.cssText = `
                    position: absolute;
                    top: 0.5rem;
                    right: 0.5rem;
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 0.25rem 0.5rem;
                    border-radius: 4px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    z-index: 10;
                `;
                block.style.position = 'relative';
                block.appendChild(label);
            }
        }

        // Zeilen-Nummern für längere Code-Blöcke
        const lines = block.textContent.split('\n').length;
        if (lines > 10) {
            addLineNumbers(block);
        }
    });
}

/**
 * Fügt Zeilen-Nummern zu Code-Blöcken hinzu
 */
function addLineNumbers(codeBlock) {
    const pre = codeBlock.querySelector('pre');
    if (!pre) return;

    const code = pre.querySelector('code');
    if (!code) return;

    const lines = code.textContent.split('\n');
    const lineNumbers = document.createElement('div');
    lineNumbers.className = 'line-numbers';
    lineNumbers.style.cssText = `
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3rem;
        background: #f8f9fa;
        border-right: 1px solid #e9ecef;
        padding: 1rem 0.5rem;
        font-family: 'Roboto Mono', monospace;
        font-size: 0.8rem;
        color: #6c757d;
        user-select: none;
        overflow: hidden;
    `;

    for (let i = 1; i <= lines.length; i++) {
        const lineNumber = document.createElement('div');
        lineNumber.textContent = i;
        lineNumber.style.lineHeight = '1.5';
        lineNumbers.appendChild(lineNumber);
    }

    codeBlock.style.position = 'relative';
    pre.style.paddingLeft = '4rem';
    codeBlock.insertBefore(lineNumbers, pre);
}

/**
 * Hebt API-Signaturen hervor
 */
function highlightAPISignatures() {
    const signatures = document.querySelectorAll('.api-signature');

    signatures.forEach(sig => {
        const text = sig.textContent;

        // Syntax-Highlighting für Python
        let highlighted = text
            .replace(/\b(async|def|class|import|from|return|await|if|else|try|except|finally|with|as)\b/g,
                     '<span class="keyword">$1</span>')
            .replace(/\b(str|int|float|bool|Dict|List|Optional|Union|Any|Callable|Awaitable)\b/g,
                     '<span class="type">$1</span>')
            .replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\s*(?=:)/g,
                     '<span class="parameter">$1</span>');

        sig.innerHTML = highlighted;
    });
}

/**
 * Richtet interaktive Beispiele ein
 */
function setupInteractiveExamples() {
    const examples = document.querySelectorAll('.code-example');

    examples.forEach(example => {
        const runButton = document.createElement('button');
        runButton.textContent = '▶ Beispiel ausführen';
        runButton.className = 'run-example-btn';
        runButton.style.cssText = `
            background: #1976d2;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-top: 0.5rem;
            transition: background 0.2s;
        `;

        runButton.addEventListener('click', function() {
            showExampleOutput(example);
        });

        runButton.addEventListener('mouseenter', function() {
            this.style.background = '#1565c0';
        });

        runButton.addEventListener('mouseleave', function() {
            this.style.background = '#1976d2';
        });

        example.appendChild(runButton);
    });
}

/**
 * Zeigt Beispiel-Output an
 */
function showExampleOutput(example) {
    let output = example.querySelector('.example-output');

    if (!output) {
        output = document.createElement('div');
        output.className = 'example-output';
        output.style.cssText = `
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: 'Roboto Mono', monospace;
            font-size: 0.9rem;
        `;
        example.appendChild(output);
    }

    // Simuliere Code-Ausführung
    output.innerHTML = '<div style="color: #28a745;">✅ Beispiel erfolgreich ausgeführt</div>';

    // Simuliere realistische Ausgabe basierend auf Code-Inhalt
    const code = example.querySelector('code');
    if (code) {
        const codeText = code.textContent;

        if (codeText.includes('plan_task')) {
            output.innerHTML += '<div>Plan erstellt: plan-abc123</div>';
        }

        if (codeText.includes('execute_action')) {
            output.innerHTML += '<div>Aktion ausgeführt: action-def456</div>';
        }

        if (codeText.includes('health_check')) {
            output.innerHTML += '<div>System Status: healthy</div>';
        }

        if (codeText.includes('get_available_protocols')) {
            output.innerHTML += '<div>Verfügbare Protokolle: [RPC, STREAM, BUS, MCP]</div>';
        }
    }
}

/**
 * Erweitert die Suchfunktionalität
 */
function enhanceSearch() {
    const searchInput = document.querySelector('[data-md-component="search-query"]');

    if (searchInput) {
        // Suchvorschläge hinzufügen
        const suggestions = [
            'UnifiedKeiAgentClient',
            'plan_task',
            'execute_action',
            'health_check',
            'ProtocolType',
            'SecurityConfig',
            'enterprise logging',
            'input validation',
            'multi-protocol'
        ];

        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();

            if (query.length > 2) {
                const matches = suggestions.filter(s =>
                    s.toLowerCase().includes(query)
                );

                showSearchSuggestions(matches, this);
            }
        });
    }
}

/**
 * Zeigt Suchvorschläge an
 */
function showSearchSuggestions(suggestions, input) {
    let suggestionBox = document.querySelector('.search-suggestions');

    if (!suggestionBox) {
        suggestionBox = document.createElement('div');
        suggestionBox.className = 'search-suggestions';
        suggestionBox.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 1000;
            max-height: 200px;
            overflow-y: auto;
        `;
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(suggestionBox);
    }

    suggestionBox.innerHTML = '';

    suggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.textContent = suggestion;
        item.style.cssText = `
            padding: 0.5rem 1rem;
            cursor: pointer;
            border-bottom: 1px solid #f0f0f0;
        `;

        item.addEventListener('click', function() {
            input.value = suggestion;
            suggestionBox.style.display = 'none';
            input.dispatchEvent(new Event('input'));
        });

        item.addEventListener('mouseenter', function() {
            this.style.background = '#f5f5f5';
        });

        item.addEventListener('mouseleave', function() {
            this.style.background = 'white';
        });

        suggestionBox.appendChild(item);
    });

    suggestionBox.style.display = suggestions.length > 0 ? 'block' : 'none';
}

/**
 * Erweitert die Navigation
 */
function enhanceNavigation() {
    // Scroll-to-Top Button
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '↑';
    scrollButton.className = 'scroll-to-top';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        background: #1976d2;
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        opacity: 0;
        transition: opacity 0.3s;
        z-index: 1000;
    `;

    scrollButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    document.body.appendChild(scrollButton);

    // Zeige Button bei Scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollButton.style.opacity = '1';
        } else {
            scrollButton.style.opacity = '0';
        }
    });

    // Aktuelle Sektion hervorheben
    highlightCurrentSection();
}

/**
 * Hebt die aktuelle Sektion in der Navigation hervor
 */
function highlightCurrentSection() {
    const sections = document.querySelectorAll('h2[id], h3[id]');
    const navLinks = document.querySelectorAll('.md-nav__link');

    function updateActiveSection() {
        let current = '';

        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100) {
                current = section.id;
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active-section');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active-section');
                link.style.fontWeight = '600';
                link.style.color = '#1976d2';
            }
        });
    }

    window.addEventListener('scroll', updateActiveSection);
    updateActiveSection();
}

/**
 * Richtet Performance-Monitoring ein
 */
function setupPerformanceMonitoring() {
    // Page Load Performance
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`📊 Dokumentation geladen in ${loadTime.toFixed(2)}ms`);

        // Zeige Performance-Info in der Konsole
        if (performance.getEntriesByType) {
            const navigation = performance.getEntriesByType('navigation')[0];
            if (navigation) {
                console.log('📈 Performance Metrics:', {
                    'DNS Lookup': `${(navigation.domainLookupEnd - navigation.domainLookupStart).toFixed(2)}ms`,
                    'TCP Connect': `${(navigation.connectEnd - navigation.connectStart).toFixed(2)}ms`,
                    'Request': `${(navigation.responseStart - navigation.requestStart).toFixed(2)}ms`,
                    'Response': `${(navigation.responseEnd - navigation.responseStart).toFixed(2)}ms`,
                    'DOM Processing': `${(navigation.domContentLoadedEventEnd - navigation.responseEnd).toFixed(2)}ms`,
                    'Total Load Time': `${(navigation.loadEventEnd - navigation.navigationStart).toFixed(2)}ms`
                });
            }
        }
    });

    // User Interaction Tracking
    let interactionCount = 0;

    document.addEventListener('click', function(e) {
        interactionCount++;

        // Track clicks on important elements
        if (e.target.matches('a[href^="#"]')) {
            console.log(`🔗 Interne Navigation: ${e.target.getAttribute('href')}`);
        }

        if (e.target.matches('.md-nav__link')) {
            console.log(`📖 Dokumentations-Navigation: ${e.target.textContent.trim()}`);
        }

        if (e.target.matches('code, .highlight')) {
            console.log('💻 Code-Block Interaktion');
        }
    });

    // Session Summary
    window.addEventListener('beforeunload', function() {
        const sessionTime = performance.now();
        console.log(`📋 Session Summary:`, {
            'Session Duration': `${(sessionTime / 1000).toFixed(2)}s`,
            'Interactions': interactionCount,
            'Page': document.title
        });
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export für mögliche externe Verwendung
window.KEIDocsEnhancements = {
    enhanceCodeBlocks,
    highlightAPISignatures,
    setupInteractiveExamples,
    enhanceSearch,
    enhanceNavigation
};
