/**
 * Premier Research Club - JavaScript Functionality
 * 
 * This file contains all JavaScript functionality for the website.
 * It follows unobtrusive JavaScript principles by keeping all JavaScript
 * separate from HTML and using event listeners instead of inline handlers.
 * 
 * Features included:
 * - Responsive navigation menu
 * - Smooth scrolling
 * - Form validation and submission
 * - Scroll-triggered animations
 * - Interactive elements
 */

// ==================================================
// UTILITY FUNCTIONS
// ==================================================

/**
 * Utility function to add event listeners to multiple elements
 * @param {NodeList|Array} elements - Elements to add listeners to
 * @param {string} event - Event type (e.g., 'click', 'scroll')
 * @param {function} handler - Event handler function
 */
function addEventListeners(elements, event, handler) {
    elements.forEach(element => {
        element.addEventListener(event, handler);
    });
}

/**
 * Utility function to debounce function calls
 * Prevents excessive function calls during events like scroll or resize
 * @param {function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {function} Debounced function
 */
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

/**
 * Utility function to check if element is in viewport
 * @param {Element} element - Element to check
 * @returns {boolean} True if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Smooth scroll to element with offset for fixed navbar
 * @param {string} targetId - ID of target element
 */
function scrollToSection(targetId) {
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
        const navbar = document.getElementById('navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : 70;
        const targetPosition = targetElement.offsetTop - navbarHeight;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
}

// Make scrollToSection available globally for button onclick handlers
window.scrollToSection = scrollToSection;

// ==================================================
// NAVIGATION FUNCTIONALITY
// ==================================================

/**
 * Navigation class to handle all navigation-related functionality
 */
class Navigation {
    constructor() {
        this.navbar = document.getElementById('navbar');
        this.hamburger = document.getElementById('hamburger');
        this.navMenu = document.getElementById('nav-menu');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.isMenuOpen = false;
        
        this.init();
    }
    
    /**
     * Initialize navigation functionality
     */
    init() {
        // Add event listeners
        if (this.hamburger) {
            this.hamburger.addEventListener('click', () => this.toggleMobileMenu());
        }
        
        // Add click listeners to navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
        
        // Handle scroll events for navbar styling and active link highlighting
        window.addEventListener('scroll', debounce(() => this.handleScroll(), 10));
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => this.handleOutsideClick(e));
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    /**
     * Toggle mobile menu open/closed
     */
    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;
        
        if (this.hamburger) {
            this.hamburger.classList.toggle('active', this.isMenuOpen);
        }
        
        if (this.navMenu) {
            this.navMenu.classList.toggle('active', this.isMenuOpen);
        }
        
        // Prevent body scroll when menu is open
        document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';
    }
    
    /**
     * Handle navigation link clicks
     * @param {Event} e - Click event
     */
    handleNavClick(e) {
        const href = e.target.getAttribute('href');
        
        // Handle internal links (starting with #)
        if (href && href.startsWith('#')) {
            e.preventDefault();
            const targetId = href.substring(1);
            scrollToSection(targetId);
            
            // Close mobile menu after clicking link
            if (this.isMenuOpen) {
                this.toggleMobileMenu();
            }
        }
    }
    
    /**
     * Handle scroll events for navbar styling and active link highlighting
     */
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class to navbar for styling
        if (this.navbar) {
            this.navbar.classList.toggle('scrolled', scrollTop > 50);
        }
        
        // Highlight active navigation link based on scroll position
        this.updateActiveNavLink();
        
        // Show/hide back to top button
        this.updateBackToTopButton();
    }
    
    /**
     * Update active navigation link based on current scroll position
     */
    updateActiveNavLink() {
        const sections = document.querySelectorAll('section[id]');
        const navbarHeight = this.navbar ? this.navbar.offsetHeight : 70;
        
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navbarHeight - 100;
            const sectionHeight = section.offsetHeight;
            
            if (window.pageYOffset >= sectionTop && 
                window.pageYOffset < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Update active class on navigation links
        this.navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }
    
    /**
     * Show/hide back to top button based on scroll position
     */
    updateBackToTopButton() {
        const backToTopButton = document.getElementById('back-to-top');
        if (backToTopButton) {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            backToTopButton.classList.toggle('show', scrollTop > 300);
        }
    }
    
    /**
     * Handle clicks outside mobile menu to close it
     * @param {Event} e - Click event
     */
    handleOutsideClick(e) {
        if (this.isMenuOpen && 
            !this.navMenu.contains(e.target) && 
            !this.hamburger.contains(e.target)) {
            this.toggleMobileMenu();
        }
    }
    
    /**
     * Handle window resize events
     */
    handleResize() {
        // Close mobile menu on resize to desktop size
        if (window.innerWidth > 768 && this.isMenuOpen) {
            this.toggleMobileMenu();
        }
    }
}

// ==================================================
// FORM VALIDATION AND SUBMISSION
// ==================================================

/**
 * Form handler class for contact form validation and submission
 */
class FormHandler {
    constructor() {
        this.contactForm = document.getElementById('contact-form');
        this.newsletterForm = document.getElementById('newsletter-form');
        
        this.init();
    }
    
    /**
     * Initialize form functionality
     */
    init() {
        if (this.contactForm) {
            this.contactForm.addEventListener('submit', (e) => this.handleContactSubmit(e));
        }
        
        if (this.newsletterForm) {
            this.newsletterForm.addEventListener('submit', (e) => this.handleNewsletterSubmit(e));
        }
    }
    
    /**
     * Handle contact form submission
     * @param {Event} e - Submit event
     */
    handleContactSubmit(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this.contactForm);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };
        
        // Validate form
        const validation = this.validateContactForm(data);
        
        if (validation.isValid) {
            this.submitContactForm(data);
        } else {
            this.showValidationErrors(validation.errors);
        }
    }
    
    /**
     * Validate contact form data
     * @param {Object} data - Form data
     * @returns {Object} Validation result
     */
    validateContactForm(data) {
        const errors = {};
        let isValid = true;
        
        // Name validation
        if (!data.name || data.name.trim().length < 2) {
            errors.name = 'Please enter your full name (at least 2 characters)';
            isValid = false;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!data.email || !emailRegex.test(data.email)) {
            errors.email = 'Please enter a valid email address';
            isValid = false;
        }
        
        // Message validation
        if (!data.message || data.message.trim().length < 10) {
            errors.message = 'Please enter a message (at least 10 characters)';
            isValid = false;
        }
        
        return { isValid, errors };
    }
    
    /**
     * Show validation errors on form
     * @param {Object} errors - Validation errors
     */
    showValidationErrors(errors) {
        // Clear previous errors
        this.clearFormErrors();
        
        // Show new errors
        Object.keys(errors).forEach(field => {
            const input = document.getElementById(field);
            const errorElement = document.getElementById(`${field}-error`);
            
            if (input) {
                input.classList.add('error');
            }
            
            if (errorElement) {
                errorElement.textContent = errors[field];
                errorElement.classList.add('show');
            }
        });
    }
    
    /**
     * Clear form validation errors
     */
    clearFormErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        const inputElements = document.querySelectorAll('.form-group input, .form-group textarea');
        
        errorElements.forEach(element => {
            element.classList.remove('show');
            element.textContent = '';
        });
        
        inputElements.forEach(element => {
            element.classList.remove('error');
        });
    }
    
    /**
     * Submit contact form (simulation - replace with actual submission logic)
     * @param {Object} data - Form data
     */
    async submitContactForm(data) {
        const submitButton = this.contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Show loading state
            submitButton.innerHTML = '<span class="loading"></span> Sending...';
            submitButton.disabled = true;
            
            // Simulate API call (replace with actual submission)
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Show success message
            this.showSuccessMessage('Thank you for your message! We\'ll get back to you soon.');
            
            // Reset form
            this.contactForm.reset();
            this.clearFormErrors();
            
        } catch (error) {
            // Show error message
            this.showErrorMessage('Sorry, there was an error sending your message. Please try again.');
            console.error('Form submission error:', error);
        } finally {
            // Reset button state
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }
    
    /**
     * Handle newsletter form submission
     * @param {Event} e - Submit event
     */
    async handleNewsletterSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.newsletterForm);
        const email = formData.get('email');
        
        if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            this.showErrorMessage('Please enter a valid email address');
            return;
        }
        
        const submitButton = this.newsletterForm.querySelector('button[type="submit"]');
        const originalHTML = submitButton.innerHTML;
        
        try {
            // Show loading state
            submitButton.innerHTML = '<span class="loading"></span>';
            submitButton.disabled = true;
            
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Show success message
            this.showSuccessMessage('Thank you for subscribing to our newsletter!');
            this.newsletterForm.reset();
            
        } catch (error) {
            this.showErrorMessage('Sorry, there was an error with your subscription. Please try again.');
            console.error('Newsletter submission error:', error);
        } finally {
            // Reset button state
            submitButton.innerHTML = originalHTML;
            submitButton.disabled = false;
        }
    }
    
    /**
     * Show success message
     * @param {string} message - Success message
     */
    showSuccessMessage(message) {
        this.showMessage(message, 'success');
    }
    
    /**
     * Show error message
     * @param {string} message - Error message
     */
    showErrorMessage(message) {
        this.showMessage(message, 'error');
    }
    
    /**
     * Show message to user
     * @param {string} message - Message text
     * @param {string} type - Message type (success, error)
     */
    showMessage(message, type) {
        // Create message element
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        
        // Style the message
        Object.assign(messageElement.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '8px',
            color: 'white',
            backgroundColor: type === 'success' ? '#10b981' : '#ef4444',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
            zIndex: '9999',
            maxWidth: '300px',
            fontSize: '14px',
            fontWeight: '500'
        });
        
        // Add to page
        document.body.appendChild(messageElement);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 5000);
    }
}

// ==================================================
// SCROLL ANIMATIONS
// ==================================================

/**
 * Scroll animation handler for fade-in effects
 */
class ScrollAnimations {
    constructor() {
        this.animatedElements = document.querySelectorAll('.mission-card, .project-card, .benefit-item');
        this.observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        this.init();
    }
    
    /**
     * Initialize scroll animations
     */
    init() {
        // Use Intersection Observer for better performance
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver(
                (entries) => this.handleIntersection(entries),
                this.observerOptions
            );
            
            this.animatedElements.forEach(element => {
                this.observer.observe(element);
            });
        } else {
            // Fallback for older browsers
            window.addEventListener('scroll', debounce(() => this.handleScrollFallback(), 50));
        }
    }
    
    /**
     * Handle intersection observer entries
     * @param {Array} entries - Intersection observer entries
     */
    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                this.observer.unobserve(entry.target);
            }
        });
    }
    
    /**
     * Fallback scroll handler for older browsers
     */
    handleScrollFallback() {
        this.animatedElements.forEach(element => {
            if (isInViewport(element) && !element.classList.contains('fade-in-up')) {
                element.classList.add('fade-in-up');
            }
        });
    }
}

// ==================================================
// INTERACTIVE ELEMENTS
// ==================================================

/**
 * Handler for interactive elements and user experience enhancements
 */
class InteractiveElements {
    constructor() {
        this.init();
    }
    
    /**
     * Initialize interactive elements
     */
    init() {
        this.setupBackToTop();
        this.setupProjectCards();
        this.setupScrollIndicator();
    }
    
    /**
     * Setup back to top button
     */
    setupBackToTop() {
        const backToTopButton = document.getElementById('back-to-top');
        
        if (backToTopButton) {
            backToTopButton.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }
    
    /**
     * Setup project card interactions
     */
    setupProjectCards() {
        const projectCards = document.querySelectorAll('.project-card');
        
        projectCards.forEach(card => {
            const learnMoreBtn = card.querySelector('.btn-learn-more');
            
            if (learnMoreBtn) {
                learnMoreBtn.addEventListener('click', () => {
                    const projectTitle = card.querySelector('.project-title').textContent;
                    this.showProjectDetails(projectTitle);
                });
            }
        });
    }
    
    /**
     * Setup scroll indicator in hero section
     */
    setupScrollIndicator() {
        const scrollIndicator = document.querySelector('.scroll-indicator');
        
        if (scrollIndicator) {
            scrollIndicator.addEventListener('click', () => {
                scrollToSection('about');
            });
        }
    }
    
    /**
     * Show project details (placeholder - replace with actual modal or page navigation)
     * @param {string} projectTitle - Title of the project
     */
    showProjectDetails(projectTitle) {
        // For now, just show an alert. In a real application, this would open a modal
        // or navigate to a detailed project page
        alert(`Learn more about: ${projectTitle}\n\nThis would typically open a detailed project page or modal with more information about the research project.`);
    }
}

// ==================================================
// ADDITIONAL MODERN EFFECTS
// ==================================================

// Scroll Progress Indicator
class ScrollProgress {
    constructor() {
        this.createProgressBar();
        this.updateProgress();
        window.addEventListener('scroll', () => this.updateProgress());
    }

    createProgressBar() {
        let progressBar = document.querySelector('.scroll-progress');
        if (!progressBar) {
            progressBar = document.createElement('div');
            progressBar.className = 'scroll-progress';
            document.body.appendChild(progressBar);
        }
        this.progressBar = progressBar;
    }

    updateProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        this.progressBar.style.width = scrollPercent + '%';
    }
}

// Loading Screen with Enhanced Animation
class LoadingScreen {
    constructor() {
        this.loadingScreen = document.querySelector('.loading-screen');
        if (this.loadingScreen) {
            this.hideAfterLoad();
        }
    }

    hideAfterLoad() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.loadingScreen.style.opacity = '0';
                setTimeout(() => {
                    this.loadingScreen.style.display = 'none';
                }, 500);
            }, 1500);
        });
    }
}

// Magnetic Effect for Interactive Elements
class MagneticEffect {
    constructor() {
        this.elements = document.querySelectorAll('.magnetic');
        this.init();
    }

    init() {
        this.elements.forEach(element => {
            element.addEventListener('mousemove', (e) => this.handleMouseMove(e, element));
            element.addEventListener('mouseleave', (e) => this.handleMouseLeave(e, element));
        });
    }

    handleMouseMove(e, element) {
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const strength = 0.2;
        element.style.transform = `translate(${x * strength}px, ${y * strength}px) scale(1.05)`;
    }

    handleMouseLeave(e, element) {
        element.style.transform = 'translate(0px, 0px) scale(1)';
    }
}

// Animated Counter for Statistics
class AnimatedCounter {
    constructor() {
        this.counters = document.querySelectorAll('.stat-number');
        this.init();
    }

    init() {
        this.observeCounters();
    }

    observeCounters() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    this.animateCounter(entry.target);
                    entry.target.dataset.animated = 'true';
                }
            });
        });

        this.counters.forEach(counter => {
            observer.observe(counter);
        });
    }

    animateCounter(counter) {
        const target = parseInt(counter.textContent.replace(/\D/g, ''));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            const suffix = counter.textContent.replace(/\d/g, '');
            counter.textContent = Math.floor(current) + suffix;
        }, 16);
    }
}

// Enhanced Project Cards with 3D Effects
class ProjectCards3D {
    constructor() {
        this.cards = document.querySelectorAll('.project-card');
        this.init();
    }

    init() {
        this.cards.forEach(card => {
            card.addEventListener('mousemove', (e) => this.handleMouseMove(e, card));
            card.addEventListener('mouseleave', (e) => this.handleMouseLeave(e, card));
        });
    }

    handleMouseMove(e, card) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
    }

    handleMouseLeave(e, card) {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
    }
}

// ==================================================
// INITIALIZATION
// ==================================================

/**
 * Initialize all functionality when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all components
    new Navigation();
    new FormHandler();
    new ScrollAnimations();
    new InteractiveElements();
    new LoadingScreen();
    new ScrollProgress();
    new MagneticEffect();
    new AnimatedCounter();
    new ProjectCards3D();
    
    // Console message for developers
    console.log('🔬 Premier Research Club website loaded successfully!');
    console.log('Built with HTML, CSS, and vanilla JavaScript following best practices.');
});

// ==================================================
// ERROR HANDLING
// ==================================================

/**
 * Global error handler for unhandled JavaScript errors
 */
window.addEventListener('error', (event) => {
    console.error('JavaScript error:', event.error);
    
    // In a production environment, you might want to send error reports
    // to a logging service here
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Prevent the default browser behavior
    event.preventDefault();
});

// ==================================================
// PERFORMANCE OPTIMIZATION
// ==================================================

/**
 * Lazy load images for better performance
 */
if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

/**
 * Preload critical resources
 */
document.addEventListener('DOMContentLoaded', () => {
    // Preload important images
    const criticalImages = [
        'assets/images/hero-research.jpg',
        'assets/images/about-team.jpg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
});

// ==================================================
// ACCESSIBILITY ENHANCEMENTS
// ==================================================

/**
 * Keyboard navigation support
 */
document.addEventListener('keydown', (e) => {
    // Handle escape key to close mobile menu
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('nav-menu');
        if (navMenu && navMenu.classList.contains('active')) {
            const hamburger = document.getElementById('hamburger');
            if (hamburger) {
                hamburger.click();
            }
        }
    }
});

/**
 * Announce page changes to screen readers
 * @param {string} message - Message to announce
 */
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        scrollToSection,
        debounce,
        isInViewport
    };
}

// ==================================================
// MODERN PARTICLE SYSTEM
// ==================================================

class ParticleSystem {
    constructor(container) {
        this.container = container;
        this.particles = [];
        this.particleCount = 50;
        this.init();
    }

    init() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particle-container';
        this.container.appendChild(particleContainer);

        for (let i = 0; i < this.particleCount; i++) {
            this.createParticle(particleContainer);
        }
    }

    createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        
        const size = 2 + Math.random() * 4;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.opacity = 0.3 + Math.random() * 0.7;
        
        container.appendChild(particle);
        this.particles.push(particle);
    }
}

// ==================================================
// TYPING ANIMATION
// ==================================================

class TypingAnimation {
    constructor(element, texts, speed = 100) {
        this.element = element;
        this.texts = texts;
        this.speed = speed;
        this.textIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.init();
    }

    init() {
        this.element.classList.add('typing-text');
        this.type();
    }

    type() {
        const currentText = this.texts[this.textIndex];
        
        if (this.isDeleting) {
            this.element.textContent = currentText.substring(0, this.charIndex - 1);
            this.charIndex--;
        } else {
            this.element.textContent = currentText.substring(0, this.charIndex + 1);
            this.charIndex++;
        }

        let typeSpeed = this.speed;

        if (this.isDeleting) {
            typeSpeed /= 2;
        }

        if (!this.isDeleting && this.charIndex === currentText.length) {
            typeSpeed = 2000;
            this.isDeleting = true;
        } else if (this.isDeleting && this.charIndex === 0) {
            this.isDeleting = false;
            this.textIndex = (this.textIndex + 1) % this.texts.length;
            typeSpeed = 500;
        }

        setTimeout(() => this.type(), typeSpeed);
    }
}

// ==================================================
// SCROLL REVEAL SYSTEM
// ==================================================

class ScrollRevealSystem {
    constructor() {
        this.elements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
        this.init();
    }

    init() {
        this.revealElements();
        window.addEventListener('scroll', debounce(() => this.revealElements(), 10));
    }

    revealElements() {
        this.elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('active');
            }
        });
    }
}

// ==================================================
// INITIALIZE MODERN EFFECTS
// ==================================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize scroll reveal system
    new ScrollRevealSystem();
    
    // Initialize particle system for hero section
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        new ParticleSystem(heroSection);
    }
    
    // Initialize typing animation for hero title
    const heroTitle = document.querySelector('.hero-title .accent-text');
    if (heroTitle) {
        const texts = ['Advancing Knowledge', 'Driving Innovation', 'Building Future', 'Making Impact'];
        new TypingAnimation(heroTitle, texts, 150);
    }
    
    // Add glassmorphism classes to existing elements
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.classList.add('glass');
    });
    
    const missionCards = document.querySelectorAll('.mission-card');
    missionCards.forEach(card => {
        card.classList.add('glass', 'reveal');
    });
    
    // Add reveal animations to sections
    const aboutSection = document.querySelector('.about');
    if (aboutSection) {
        const elements = aboutSection.querySelectorAll('.mission-card, .about-img, .stat-item');
        elements.forEach(el => el.classList.add('reveal'));
    }
    
    const projectsSection = document.querySelector('.projects');
    if (projectsSection) {
        const cards = projectsSection.querySelectorAll('.project-card');
        cards.forEach((card, index) => {
            card.classList.add(index % 2 === 0 ? 'reveal-left' : 'reveal-right');
        });
    }
    
    // Add magnetic effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.classList.add('magnetic', 'neon-glow');
    });
    
    // Add floating animation to hero image
    const heroImage = document.querySelector('.hero-img');
    if (heroImage) {
        heroImage.classList.add('floating');
    }
    
    // Add pulse glow to CTA buttons
    const ctaButtons = document.querySelectorAll('.btn-primary');
    ctaButtons.forEach(button => {
        button.classList.add('pulse-glow');
    });
});
