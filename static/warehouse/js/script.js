let lastScrollTop = 0; // To track the last scroll position
const headerMenu = document.querySelector('.header-menu'); // Select the header-menu element
const navToggle = document.getElementById('nav-toggle'); // Select the nav-toggle button
const overlay = document.getElementById('overlay'); // Select the overlay
const SCROLL_THRESHOLD = 100; // Distance threshold for hiding
let hasScrolledPastThreshold = false; // Track if user has scrolled past threshold
let hideTimeout = null; // Timeout ID for hiding animation

// Function to handle responsive behavior
function updateHeaderVisibility() {
    const screenWidth = window.innerWidth;

    if (screenWidth < 768) {
        // On smaller screens, hide the header-menu and show nav-toggle
        headerMenu.style.display = 'none';
        navToggle.style.display = 'block';
    } else {
        // On larger screens, show the header-menu and hide nav-toggle
        headerMenu.style.display = 'flex';
        navToggle.style.display = 'none';
        overlay.style.display = 'none'; // Ensure overlay is hidden
        headerMenu.style.transform = 'translateY(0)'; // Reset position
        headerMenu.style.opacity = '1'; // Reset opacity
    }
}


// Nav-toggle click behavior
navToggle.addEventListener('click', () => {
    overlay.style.display = 'flex'; // Show overlay
    navToggle.style.display = 'none'; // Hide nav-toggle while overlay is visible
});

// Close-btn click behavior
document.getElementById('close-btn').addEventListener('click', () => {
    overlay.style.display = 'none'; // Hide overlay
    navToggle.style.display = 'block'; // Show nav-toggle again
});

// Resize behavior for header-menu and nav-toggle
window.addEventListener('resize', () => {
    updateHeaderVisibility();
    // Reset scroll tracking variables to avoid conflicts
    hasScrolledPastThreshold = false;
    lastScrollTop = window.scrollY;
});

// Initial setup on page load
updateHeaderVisibility();
