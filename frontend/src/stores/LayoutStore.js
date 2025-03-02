import { atom } from 'nanostores';

// Initialize with a sensible default for SSR
export const isDesktop = atom(false);
export const viewportWidth = atom(0);

// Define the breakpoint for desktop (min-width in pixels)
const DESKTOP_BREAKPOINT = 1024;

// Update the store when the document is available (client-side only)
if (typeof window !== 'undefined') {
    // Initialize based on current viewport
    const updateLayout = () => {
        const width = window.innerWidth;
        viewportWidth.set(width);
        isDesktop.set(width >= DESKTOP_BREAKPOINT);
    };
    
    // Set initial value
    updateLayout();
    
    // Update on resize
    window.addEventListener('resize', updateLayout);
}

/**
 * Custom hook to use in Svelte components
 * Returns a function that takes a desktop and mobile value and returns the appropriate one
 */
export function createResponsiveValue(desktopStore) {
    return function useResponsiveValue(desktopValue, mobileValue) {
        return desktopStore.get() ? desktopValue : mobileValue;
    };
}