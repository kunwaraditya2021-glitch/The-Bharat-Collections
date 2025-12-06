// Component Loader for Navbar and Footer
// This script loads reusable HTML components into pages

(function () {
    'use strict';

    /**
     * Load a component from a file and inject it into a target element
     * @param {string} componentPath - Path to the component HTML file
     * @param {string} targetId - ID of the element to inject the component into
     */
    async function loadComponent(componentPath, targetId) {
        try {
            const response = await fetch(componentPath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.innerHTML = html;
            } else {
                console.error(`Target element with ID "${targetId}" not found`);
            }
        } catch (error) {
            console.error(`Failed to load component: ${componentPath}`, error);
        }
    }

    /**
     * Initialize components when DOM is ready
     */
    function initializeComponents() {
        // Load navbar and footer components
        loadComponent('/templates/components/navbar.html', 'navbar-placeholder');
        loadComponent('/templates/components/footer.html', 'footer-placeholder');
    }

    // Load components when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeComponents);
    } else {
        // DOM already loaded
        initializeComponents();
    }
})();
