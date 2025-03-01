import { atom } from 'nanostores';

// Store for search results
export const searchResults = atom([]);
export const hasSearched = atom(false);

// Clear search results
export function clearSearchResults() {
    searchResults.set([]);
    hasSearched.set(false);
}

// Update search results
export function updateSearchResults(results) {
    searchResults.set(results || []);
    hasSearched.set(true);
}