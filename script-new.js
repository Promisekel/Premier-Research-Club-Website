/**
 * Premier Research Club - Main JavaScript Module
 * 
 * Modern ES6+ implementation with Firebase integration
 * Handles all frontend interactions, animations, and data management
 * 
 * Features:
 * - Navigation and responsive menu
 * - Form handling with Firebase integration
 * - File upload to Firebase Storage
 * - Dynamic project loading from Firestore
 * - Scroll animations and effects
 * - Notification system
 * 
 * @author Premier Research Club Development Team
 * @version 1.0.0
 */

import { 
    submitContactForm, 
    submitProject, 
    getProjects, 
    uploadFile, 
    formatFileSize, 
    validateEmail,
    showNotification 
} from './firebase.js';

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Debounce function to limit execution rate
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

/**
 * Smooth scroll to element with offset
 * @param {string} targetId - ID of target element
 */
const scrollToSection = (targetId) => {
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
};

/**
 * Check if element is in viewport
 * @param {Element} element - Element to check
 * @returns {boolean} True if element is in viewport
 */
const isInViewport = (element) => {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

// =============================================================================
// NAVIGATION SYSTEM
// =============================================================================

class NavigationManager {
    constructor() {
        this.navbar = document.getElementById('navbar');
        this.hamburger = document.getElementById('hamburger');
        this.navMenu = document.getElementById('nav-menu');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.isMenuOpen = false;
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.handleScroll();
        this.setActiveLink();
    }

    bindEvents() {
        // Mobile menu toggle
        if (this.hamburger) {
            this.hamburger.addEventListener('click', () => this.toggleMobileMenu());
        }

        // Navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });

        // Scroll events
        window.addEventListener('scroll', debounce(() => this.handleScroll(), 10));
        window.addEventListener('scroll', debounce(() => this.setActiveLink(), 10));

        // Close mobile menu on resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isMenuOpen) {
                this.closeMobileMenu();
            }
        });
    }

    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;
        
        if (this.hamburger) {
            this.hamburger.classList.toggle('active');
        }
        
        if (this.navMenu) {
            this.navMenu.classList.toggle('active');
        }

        // Prevent body scroll when menu is open
        document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';
    }

    closeMobileMenu() {
        this.isMenuOpen = false;
        
        if (this.hamburger) {
            this.hamburger.classList.remove('active');
        }
        
        if (this.navMenu) {
            this.navMenu.classList.remove('active');
        }

        document.body.style.overflow = '';
    }

    handleNavClick(e) {
        e.preventDefault();
        const href = e.target.getAttribute('href');
        
        if (href && href.startsWith('#')) {
            const targetId = href.substring(1);
            scrollToSection(targetId);
            
            // Close mobile menu after navigation
            if (this.isMenuOpen) {
                this.closeMobileMenu();
            }
        }
    }

    handleScroll() {
        // Add scrolled class to navbar
        if (this.navbar) {
            if (window.scrollY > 50) {
                this.navbar.classList.add('scrolled');
            } else {
                this.navbar.classList.remove('scrolled');
            }
        }
    }

    setActiveLink() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                this.navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
}

// =============================================================================
// SCROLL PROGRESS INDICATOR
// =============================================================================

class ScrollProgress {
    constructor() {
        this.progressBar = document.getElementById('scroll-progress');
        this.init();
    }

    init() {
        if (this.progressBar) {
            window.addEventListener('scroll', () => this.updateProgress());
        }
    }

    updateProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        this.progressBar.style.width = `${scrollPercent}%`;
    }
}

// =============================================================================
// LOADING SCREEN MANAGER
// =============================================================================

class LoadingManager {
    constructor() {
        this.loadingScreen = document.getElementById('loading-screen');
        this.init();
    }

    init() {
        if (this.loadingScreen) {
            window.addEventListener('load', () => {
                setTimeout(() => this.hideLoadingScreen(), 1500);
            });
        }
    }

    hideLoadingScreen() {
        if (this.loadingScreen) {
            this.loadingScreen.style.opacity = '0';
            setTimeout(() => {
                this.loadingScreen.style.display = 'none';
            }, 500);
        }
    }
}

// =============================================================================
// TYPING ANIMATION
// =============================================================================

class TypingAnimation {
    constructor(element, texts, speed = 150) {
        this.element = element;
        this.texts = texts;
        this.speed = speed;
        this.textIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.init();
    }

    init() {
        if (this.element) {
            this.type();
        }
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

// =============================================================================
// ANIMATED COUNTER
// =============================================================================

class AnimatedCounter {
    constructor() {
        this.counters = document.querySelectorAll('.stat-number[data-target]');
        this.init();
    }

    init() {
        if (this.counters.length > 0) {
            this.observeCounters();
        }
    }

    observeCounters() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    this.animateCounter(entry.target);
                    entry.target.dataset.animated = 'true';
                }
            });
        }, { threshold: 0.5 });

        this.counters.forEach(counter => {
            observer.observe(counter);
        });
    }

    animateCounter(counter) {
        const target = parseInt(counter.dataset.target);
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

// =============================================================================
// BACK TO TOP BUTTON
// =============================================================================

class BackToTopButton {
    constructor() {
        this.button = document.getElementById('back-to-top');
        this.init();
    }

    init() {
        if (this.button) {
            window.addEventListener('scroll', () => this.toggleVisibility());
            this.button.addEventListener('click', () => this.scrollToTop());
        }
    }

    toggleVisibility() {
        if (window.scrollY > 300) {
            this.button.classList.add('visible');
        } else {
            this.button.classList.remove('visible');
        }
    }

    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// =============================================================================
// FORM HANDLERS
// =============================================================================

class FormManager {
    constructor() {
        this.contactForm = document.getElementById('contact-form');
        this.projectForm = document.getElementById('project-form');
        this.newsletterForm = document.getElementById('newsletter-form');
        this.fileInput = document.getElementById('project-file');
        this.fileUploadArea = document.getElementById('file-upload-area');
        this.filePreview = document.getElementById('file-preview');
        this.removeFileBtn = document.getElementById('remove-file');
        this.selectedFile = null;
        
        this.init();
    }

    init() {
        this.bindContactForm();
        this.bindProjectForm();
        this.bindNewsletterForm();
        this.bindFileUpload();
    }

    bindContactForm() {
        if (this.contactForm) {
            this.contactForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleContactSubmission(e);
            });
        }
    }

    bindProjectForm() {
        if (this.projectForm) {
            this.projectForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleProjectSubmission(e);
            });
        }
    }

    bindNewsletterForm() {
        if (this.newsletterForm) {
            this.newsletterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleNewsletterSubmission(e);
            });
        }
    }

    bindFileUpload() {
        if (this.fileUploadArea && this.fileInput) {
            // Click to upload
            this.fileUploadArea.addEventListener('click', () => {
                this.fileInput.click();
            });

            // Drag and drop
            this.fileUploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                this.fileUploadArea.style.borderColor = 'var(--color-primary)';
                this.fileUploadArea.style.backgroundColor = 'var(--color-gray-50)';
            });

            this.fileUploadArea.addEventListener('dragleave', () => {
                this.fileUploadArea.style.borderColor = 'var(--color-gray-300)';
                this.fileUploadArea.style.backgroundColor = 'transparent';
            });

            this.fileUploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                this.fileUploadArea.style.borderColor = 'var(--color-gray-300)';
                this.fileUploadArea.style.backgroundColor = 'transparent';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleFileSelection(files[0]);
                }
            });

            // File input change
            this.fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileSelection(e.target.files[0]);
                }
            });

            // Remove file button
            if (this.removeFileBtn) {
                this.removeFileBtn.addEventListener('click', () => {
                    this.clearFileSelection();
                });
            }
        }
    }

    handleFileSelection(file) {
        // Validate file
        const maxSize = 5 * 1024 * 1024; // 5MB
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];

        if (file.size > maxSize) {
            showNotification('File size exceeds 5MB limit', 'error');
            return;
        }

        if (!allowedTypes.includes(file.type)) {
            showNotification('File type not allowed. Please upload images or PDF files.', 'error');
            return;
        }

        this.selectedFile = file;
        this.showFilePreview(file);
    }

    showFilePreview(file) {
        if (this.filePreview) {
            const fileName = this.filePreview.querySelector('.file-name');
            const fileSize = this.filePreview.querySelector('.file-size');

            if (fileName) fileName.textContent = file.name;
            if (fileSize) fileSize.textContent = formatFileSize(file.size);

            this.fileUploadArea.querySelector('.file-upload-placeholder').style.display = 'none';
            this.filePreview.style.display = 'flex';
        }
    }

    clearFileSelection() {
        this.selectedFile = null;
        if (this.fileInput) this.fileInput.value = '';
        if (this.filePreview) this.filePreview.style.display = 'none';
        if (this.fileUploadArea) {
            this.fileUploadArea.querySelector('.file-upload-placeholder').style.display = 'block';
        }
    }

    async handleContactSubmission(e) {
        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject') || 'Contact Form Submission',
            message: formData.get('message')
        };

        // Validation
        if (!data.name || !data.email || !data.message) {
            showNotification('Please fill in all required fields', 'error');
            return;
        }

        if (!validateEmail(data.email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }

        const submitBtn = document.getElementById('contact-submit-btn');
        const originalText = submitBtn.innerHTML;
        
        try {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            submitBtn.disabled = true;

            await submitContactForm(data);
            
            showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
            e.target.reset();
        } catch (error) {
            console.error('Contact form error:', error);
            showNotification(error.message || 'Failed to send message. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    async handleProjectSubmission(e) {
        const formData = new FormData(e.target);
        const data = {
            title: formData.get('title'),
            description: formData.get('description')
        };

        // Validation
        if (!data.title || !data.description) {
            showNotification('Please fill in all required fields', 'error');
            return;
        }

        const submitBtn = document.getElementById('submit-project-btn');
        const originalText = submitBtn.innerHTML;
        
        try {
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            submitBtn.disabled = true;

            let fileData = null;
            
            // Upload file if selected
            if (this.selectedFile) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading file...';
                fileData = await uploadFile(this.selectedFile, 'projects');
            }

            // Submit project data
            const projectData = {
                ...data,
                fileUrl: fileData?.downloadURL || null,
                fileName: fileData?.originalName || null,
                fileType: fileData?.fileType || null
            };

            await submitProject(projectData);
            
            showNotification('Project submitted successfully! It will be reviewed and published soon.', 'success');
            e.target.reset();
            this.clearFileSelection();
            
            // Refresh projects list
            const projectsManager = new ProjectsManager();
            projectsManager.loadProjects();
            
        } catch (error) {
            console.error('Project submission error:', error);
            showNotification(error.message || 'Failed to submit project. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    handleNewsletterSubmission(e) {
        const formData = new FormData(e.target);
        const email = formData.get('email');

        if (!validateEmail(email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }

        // In a real implementation, you would submit this to your newsletter service
        showNotification('Thank you for subscribing to our newsletter!', 'success');
        e.target.reset();
    }
}

// =============================================================================
// PROJECTS MANAGER
// =============================================================================

class ProjectsManager {
    constructor() {
        this.projectsGrid = document.getElementById('projects-grid');
        this.init();
    }

    init() {
        if (this.projectsGrid) {
            this.loadProjects();
        }
    }

    async loadProjects() {
        try {
            // Show loading state
            this.showLoadingState();
            
            const projects = await getProjects();
            
            if (projects.length === 0) {
                this.showEmptyState();
            } else {
                this.renderProjects(projects);
            }
        } catch (error) {
            console.error('Error loading projects:', error);
            this.showErrorState();
        }
    }

    showLoadingState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-loading">
                <div class="loading-spinner"></div>
                <p>Loading projects...</p>
            </div>
        `;
    }

    showEmptyState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-empty">
                <p>No projects available yet. Be the first to submit a project!</p>
                <a href="#submit-project" class="btn btn--primary">Submit Project</a>
            </div>
        `;
    }

    showErrorState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-error">
                <p>Failed to load projects. Please try again later.</p>
                <button class="btn btn--secondary" onclick="location.reload()">Retry</button>
            </div>
        `;
    }

    renderProjects(projects) {
        const projectsHTML = projects.map(project => this.createProjectCard(project)).join('');
        this.projectsGrid.innerHTML = projectsHTML;
    }

    createProjectCard(project) {
        const statusClass = this.getStatusClass(project.status);
        const hasFile = project.fileUrl && project.fileName;
        
        return `
            <div class="project-card">
                ${project.fileUrl && project.fileType?.startsWith('image') ? `
                    <div class="project-image">
                        <img src="${project.fileUrl}" alt="${project.title}" loading="lazy">
                        <div class="project-status ${statusClass}">${project.status || 'Pending'}</div>
                    </div>
                ` : `
                    <div class="project-header">
                        <div class="project-status ${statusClass}">${project.status || 'Pending'}</div>
                    </div>
                `}
                <div class="project-content">
                    <h3 class="project-title">${this.escapeHtml(project.title)}</h3>
                    <p class="project-description">${this.escapeHtml(project.description)}</p>
                    ${hasFile ? `
                        <div class="project-file">
                            <a href="${project.fileUrl}" target="_blank" rel="noopener" class="file-link">
                                <i class="fas fa-${project.fileType?.includes('pdf') ? 'file-pdf' : 'image'}"></i>
                                View ${project.fileType?.includes('pdf') ? 'Document' : 'Image'}
                            </a>
                        </div>
                    ` : ''}
                    <div class="project-meta">
                        <small>Submitted on ${this.formatDate(project.timestamp?.toDate?.() || new Date())}</small>
                    </div>
                </div>
            </div>
        `;
    }

    getStatusClass(status) {
        switch (status?.toLowerCase()) {
            case 'active': return 'status-active';
            case 'completed': return 'status-completed';
            case 'pending': return 'status-pending';
            default: return 'status-pending';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    }
}

// =============================================================================
// NOTIFICATION SYSTEM
// =============================================================================

class NotificationManager {
    constructor() {
        this.container = document.getElementById('notification-container');
        this.init();
    }

    init() {
        // Override the global showNotification function
        window.showNotification = (message, type = 'info') => {
            this.show(message, type);
        };
    }

    show(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.textContent = message;
        
        if (this.container) {
            this.container.appendChild(notification);
        } else {
            document.body.appendChild(notification);
        }
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            this.remove(notification);
        }, 5000);
        
        // Allow manual close
        notification.addEventListener('click', () => {
            this.remove(notification);
        });
    }

    remove(notification) {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }
}

// =============================================================================
// MAGNETIC HOVER EFFECTS
// =============================================================================

class MagneticEffects {
    constructor() {
        this.elements = document.querySelectorAll('.btn--magnetic');
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

// =============================================================================
// INITIALIZATION
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers and components
    new NavigationManager();
    new ScrollProgress();
    new LoadingManager();
    new AnimatedCounter();
    new BackToTopButton();
    new FormManager();
    new ProjectsManager();
    new NotificationManager();
    new MagneticEffects();
    
    // Initialize typing animation
    const typingElement = document.getElementById('typing-text');
    if (typingElement) {
        const texts = ['Advancing Knowledge', 'Driving Innovation', 'Building Future', 'Making Impact'];
        new TypingAnimation(typingElement, texts, 150);
    }
    
    console.log('Premier Research Club website initialized successfully!');
});

// =============================================================================
// EXPORT FOR TESTING
// =============================================================================

export {
    NavigationManager,
    ScrollProgress,
    LoadingManager,
    TypingAnimation,
    AnimatedCounter,
    BackToTopButton,
    FormManager,
    ProjectsManager,
    NotificationManager,
    MagneticEffects,
    debounce,
    scrollToSection,
    isInViewport
};
