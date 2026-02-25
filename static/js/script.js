

(function() {
    'use strict';

    // Wait for DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        
        
        /**
         * Show toast notification
         */
        function showToast(message, type = 'info', duration = 3000) {
            const container = document.getElementById('toast-container');
            if (!container) return;
            
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = message;
            
            container.appendChild(toast);
            
            setTimeout(() => {
                toast.classList.add('hiding');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }
        
        /**
         * Debounce function
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

        
        const searchInput = document.querySelector('.search-input');
        const searchForm = document.querySelector('.search-form');
        const searchButton = document.querySelector('.search-button');
        
        if (searchInput) {
            // Add visual feedback on input
            searchInput.addEventListener('input', debounce(function(e) {
                const value = e.target.value.trim();
                
                if (value.length > 0) {
                    searchInput.style.borderColor = '#667eea';
                } else {
                    searchInput.style.borderColor = '#e0e0e0';
                }
            }, 300));
            
            // Clear button functionality (optional)
            if (searchInput.value) {
                searchInput.style.paddingRight = '35px';
                
                const clearBtn = document.createElement('span');
                clearBtn.innerHTML = '×';
                clearBtn.style.cssText = `
                    position: absolute;
                    right: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    cursor: pointer;
                    font-size: 24px;
                    color: #999;
                    font-weight: bold;
                `;
                
                const wrapper = searchInput.parentElement;
                wrapper.style.position = 'relative';
                wrapper.appendChild(clearBtn);
                
                clearBtn.addEventListener('click', () => {
                    searchInput.value = '';
                    searchForm.submit();
                });
            }
        }
        
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                if (searchButton) {
                    searchButton.textContent = '🔄 Searching...';
                    searchButton.disabled = true;
                }
            });
        }

        
        
        const images = document.querySelectorAll('.item-image');
        
        images.forEach(img => {
            // Handle successful load
            img.addEventListener('load', function() {
                this.classList.add('loaded');
            });
            
            // Handle broken images
            img.addEventListener('error', function() {
                this.src = '/static/images/no-image.png';
                this.classList.add('loaded');
                console.warn('Failed to load image:', this.dataset.src || this.src);
            });
            
            // If image is already loaded (cached)
            if (img.complete) {
                img.classList.add('loaded');
            }
        });

        
        const itemCards = document.querySelectorAll('.item-card');
        
        if ('IntersectionObserver' in window) {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach((entry, index) => {
                    if (entry.isIntersecting) {
                        // Stagger animation
                        setTimeout(() => {
                            entry.target.classList.add('visible');
                        }, index * 100);
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            itemCards.forEach(card => {
                observer.observe(card);
            });
        } else {
            // Fallback for browsers without IntersectionObserver
            itemCards.forEach(card => {
                card.classList.add('visible');
            });
        }

        
        const claimButtons = document.querySelectorAll('.claim-btn');
        
        claimButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                const itemTitle = this.dataset.itemTitle || 'this item';
                
                const confirmed = confirm(
                    `Are you sure you want to claim "${itemTitle}"?\n\n` +
                    `You will be redirected to submit your claim details.`
                );
                
                if (!confirmed) {
                    e.preventDefault();
                } else {
                    // Add loading state
                    this.textContent = 'Processing...';
                    this.style.opacity = '0.6';
                    this.style.pointerEvents = 'none';
                }
            });
        });

        
        const paginationLinks = document.querySelectorAll('.pagination-link');
        
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Add loading feedback
                this.textContent = this.textContent.includes('Previous') ? 
                    '⏪ Loading...' : 'Loading... ⏩';
                
                // Smooth scroll to top
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        });


        document.addEventListener('keydown', function(e) {
            // Focus search on "/" key
            if (e.key === '/' && searchInput && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
                showToast('Search focused - Start typing!', 'info', 2000);
            }
            
            // Clear search on Escape
            if (e.key === 'Escape' && searchInput && document.activeElement === searchInput) {
                searchInput.value = '';
                searchInput.blur();
            }
        });

        
        
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('q');
        
        if (searchQuery && searchQuery.trim()) {
            showToast(`Showing results for: "${searchQuery}"`, 'info', 4000);
            
            // Highlight search terms in titles and descriptions
            const highlightText = (element, query) => {
                if (!element) return;
                
                const text = element.textContent;
                const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
                
                if (regex.test(text)) {
                    element.innerHTML = text.replace(
                        regex, 
                        '<mark>$1</mark>'
                    );
                }
            };
            
            const escapeRegex = (str) => {
                return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            };
            
            itemCards.forEach(card => {
                const title = card.querySelector('.item-title');
                const description = card.querySelector('.item-description');
                
                highlightText(title, searchQuery);
                highlightText(description, searchQuery);
            });
        }

        
        const viewButtons = document.querySelectorAll('.btn-primary');
        
        viewButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (this.href) {
                    // Add subtle loading state
                    this.style.opacity = '0.8';
                }
            });
        });

        
        if ('loading' in HTMLImageElement.prototype) {
            // Browser supports lazy loading natively
            images.forEach(img => {
                img.loading = 'lazy';
            });
        } else {
            // Fallback for older browsers
            const lazyLoadObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                        }
                        lazyLoadObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => lazyLoadObserver.observe(img));
        }

        
        
        if (window.performance && console.log) {
            window.addEventListener('load', () => {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                
                console.log(`✅ Lost Items page loaded in ${pageLoadTime}ms`);
                console.log(`📦 ${itemCards.length} items displayed`);
            });
        }

        
        
        // Add aria-labels to buttons
        claimButtons.forEach(btn => {
            const itemTitle = btn.dataset.itemTitle;
            btn.setAttribute('aria-label', `Claim ${itemTitle}`);
        });
        
        // Announce search results to screen readers
        if (searchQuery) {
            const announcement = document.createElement('div');
            announcement.setAttribute('role', 'status');
            announcement.setAttribute('aria-live', 'polite');
            announcement.className = 'sr-only';
            announcement.textContent = `Search results for ${searchQuery}. ${itemCards.length} items found.`;
            document.body.appendChild(announcement);
        }

        
        console.log('✅ Lost Items page enhanced with JavaScript!');
        console.log('🔍 Press "/" to focus search');
        console.log(`📋 ${itemCards.length} items loaded`);
        
    });

})();