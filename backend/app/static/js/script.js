/* -------------------------------------------------------------------------- */
/* Application Logic                                                          */
/* -------------------------------------------------------------------------- */

// Function to handle splash screen removal
function initApp() {
    const splashScreen = document.getElementById('splash-screen');
    const appContent = document.getElementById('app-content');
    const body = document.body;
    const logoContainer = document.getElementById('logo-container');

    // Check if already initialized to prevent double execution
    if (!splashScreen || splashScreen.classList.contains('fade-out')) return;

    // Trigger Animation
    if (logoContainer) {
        // Reset state
        logoContainer.classList.remove('active');

        // Start animation with slight delay
        setTimeout(() => {
            logoContainer.classList.add('active');
        }, 100);
    }

    // Wait for animation to complete (approx 2500ms total)
    setTimeout(() => {
        // Fade out splash screen
        splashScreen.classList.add('fade-out');

        // Reveal app content
        appContent.classList.remove('opacity-0');

        // Enable scrolling
        body.classList.remove('overflow-hidden');

        // Cleanup splash screen from DOM after transition ends
        setTimeout(() => {
            if (splashScreen.parentNode) {
                splashScreen.parentNode.removeChild(splashScreen);
            }
        }, 700);
    }, 2800);
}

// 1. Run on DOMContentLoaded
document.addEventListener('DOMContentLoaded', initApp);

// 2. Fallback: Run on window load (safe guard)
window.addEventListener('load', initApp);


/* -------------------------------------------------------------------------- */
/* Mobile Menu & Form Logic                                                   */
/* -------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {

    // --- Mobile Menu Logic ---
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    function toggleMenu() {
        mobileMenu.classList.toggle('open');
    }

    if (menuBtn) {
        menuBtn.addEventListener('click', toggleMenu);
    }

    // Close menu when a link is clicked
    mobileLinks.forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    // --- Contact Form Logic ---
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = contactForm.querySelector('button');
            const originalText = btn.innerText;
            const successMsg = document.getElementById('success-msg');

            // Disable button and show loading state
            btn.disabled = true;
            btn.innerText = 'Sending...';

            // Simulate API call
            // Perform Fetch API call
            const formData = {
                name: contactForm.querySelector('input[placeholder="John Doe"]').value,
                email: contactForm.querySelector('input[type="email"]').value,
                project_type: contactForm.querySelector('select').value,
                message: contactForm.querySelector('textarea').value
            };

            fetch('/api/quote', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
                .then(res => {
                    if (res.ok) {
                        res.json().then(data => {
                            successMsg.classList.remove('hidden');
                            successMsg.innerHTML = `Quote Request Received!<br>Your Ticket ID is <span class="font-mono font-bold text-white bg-slate-800 px-2 py-1 rounded">${data.ticket_id}</span><br><span class="text-sm">Save this ID to check your status.</span>`;
                            contactForm.reset();
                            btn.innerText = 'Sent!';
                            btn.classList.add('bg-green-600');
                            // Do not auto-hide immediately so user can copy ID
                            setTimeout(() => {
                                btn.disabled = false;
                                btn.innerText = originalText;
                                btn.classList.remove('bg-green-600');
                            }, 3000);
                        });
                    } else {
                        alert('Something went wrong. Please try again.');
                        btn.disabled = false;
                        btn.innerText = originalText;
                    }
                })
                .catch(err => {
                    console.error(err);
                    btn.disabled = false;
                    btn.innerText = originalText;
                });
        });
    }

    // --- Typewriter Logic ---
    const typewriterElement = document.getElementById('typewriter-text');
    const textsToType = ["Your Ultimate Software Solution", "Attendance + Exams + Fees", "Built for Teachers & Students"];
    let textIndex = 0;
    const typingSpeed = 100;
    const deletingSpeed = 50;
    const pauseBeforeDelete = 2000;
    const pauseBeforeType = 500;

    function typeWriter(text, i, fnCallback) {
        if (i < text.length) {
            typewriterElement.innerHTML = text.substring(0, i + 1);
            setTimeout(() => {
                typeWriter(text, i + 1, fnCallback);
            }, typingSpeed);
        } else if (typeof fnCallback == 'function') {
            setTimeout(fnCallback, pauseBeforeDelete);
        }
    }

    function deleteWriter(text, i, fnCallback) {
        if (i >= 0) {
            typewriterElement.innerHTML = text.substring(0, i);
            setTimeout(() => {
                deleteWriter(text, i - 1, fnCallback);
            }, deletingSpeed);
        } else if (typeof fnCallback == 'function') {
            setTimeout(fnCallback, pauseBeforeType);
        }
    }

    function startTypewriterLoop() {
        const currentText = textsToType[textIndex];
        typeWriter(currentText, 0, () => {
            deleteWriter(currentText, currentText.length, () => {
                textIndex = (textIndex + 1) % textsToType.length;
                startTypewriterLoop();
            });
        });
    }

    if (typewriterElement) {
        setTimeout(startTypewriterLoop, 2500);
    }

    // --- Modal Logic ---
    window.openModal = function () {
        const modal = document.getElementById('trial-modal');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }

    window.closeModal = function () {
        const modal = document.getElementById('trial-modal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = '';

            const form = document.getElementById('lead-form');
            const successMsg = document.getElementById('lead-success');
            if (successMsg) successMsg.classList.add('hidden');
            if (form) {
                form.reset();
                form.classList.remove('hidden');
            }
        }
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });



    // Handle Trial Form Submission
    const leadForm = document.getElementById('lead-form');
    if (leadForm) {
        leadForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = leadForm.querySelector('button[type="submit"]');
            const originalText = btn.innerText;

            btn.disabled = true;
            btn.innerText = 'Processing...';

            setTimeout(() => {
                const formData = new FormData(leadForm);
                const data = {};
                formData.forEach((value, key) => data[key] = value);
                console.log('Lead Captured:', data);

                // Hide form, show success
                leadForm.classList.add('hidden');
                btn.disabled = false;
                btn.innerText = originalText;

                const successMsg = document.getElementById('lead-success');
                if (successMsg) successMsg.classList.remove('hidden');

                // Redirect to Pathshala page after delay
                setTimeout(() => {
                    window.location.href = 'pathshala.html';
                }, 2000);
            }, 1000);
        });
    }


    // --- Newsletter Subscription Logic ---
    const newsletterForm = document.querySelector('section.py-20 form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = newsletterForm.querySelector('button');
            const input = newsletterForm.querySelector('input');
            const originalText = btn.innerText;

            btn.disabled = true;
            btn.innerText = '...';

            fetch('/api/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: input.value })
            })
                .then(res => res.json())
                .then(data => {
                    btn.innerText = 'Done';
                    input.value = '';
                    setTimeout(() => {
                        btn.disabled = false;
                        btn.innerText = originalText;
                    }, 2000);
                })
                .catch(err => {
                    btn.disabled = false;
                    btn.innerText = originalText;
                });
        });
    }

});
document.addEventListener('DOMContentLoaded', () => {
    const dashboardImg = document.getElementById('dashboard-slider');

    // List of images for the slider
    // NOTE: Add your additional image filenames here
    const images = [
        '/static/images/teacher-dashboard.png',
        '/static/images/admin-dashboard.png',
        '/static/images/student-dashboard.png',
        '/static/images/mobile-install.png'
    ];

    let currentIndex = 0;

    // Function to change image with fade effect
    function changeImage() {
        if (!dashboardImg || images.length <= 1) return;

        // Fade out
        dashboardImg.style.opacity = '0';

        setTimeout(() => {
            currentIndex = (currentIndex + 1) % images.length;
            dashboardImg.src = images[currentIndex];

            // Fade in
            dashboardImg.onload = () => {
                dashboardImg.style.opacity = '1';
            };
        }, 400); // Matches the CSS transition duration
    }

    // Start the slider if we have images
    if (images.length > 1) {
        setInterval(changeImage, 4000); // Change every 4 seconds
    }

    // --- Counter Animation Logic ---
    const counters = document.querySelectorAll('.counter');

    const animateCounter = (counter) => {
        const target = +counter.getAttribute('data-target');
        const suffix = counter.getAttribute('data-suffix') || '';
        const duration = 2000; // Animation duration in ms
        const increment = target / (duration / 16); // 60fps

        let current = 0;

        const updateCounter = () => {
            current += increment;

            if (current < target) {
                // Handle integer vs float display
                if (Number.isInteger(target)) {
                    counter.innerText = Math.ceil(current) + suffix;
                } else {
                    counter.innerText = current.toFixed(1) + suffix;
                }
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target + suffix;
            }
        };

        updateCounter();
    };

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                animateCounter(counter);
                observer.unobserve(counter); // Only animate once
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });

    // --- Scroll Reveal Logic ---
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserverOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px" // Trigger slightly before element is fully in view
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealObserverOptions);

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
});