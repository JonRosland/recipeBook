import { atom } from 'nanostores';

/**
 * @typedef {Object} Ingredient
 * @property {string} name
 * @property {number} quantity
 * @property {string} unit
 */

/**
 * @typedef {Object} Recipe
 * @property {string} recipeName
 * @property {string} origin
 * @property {string} category
 * @property {number} portion
 * @property {string} region
 * @property {Ingredient[]} ingredients
 * @property {string[]} steps
 * @property {string[]} notes
 */

// Initialize recipe store with default empty recipe
export const recipeStore = atom({
    recipeName: "",
    origin: "",
    category: "",
    portion: 0,
    region: "",
    ingredients: [],
    steps: [],
    notes: [],
    time: "",
    favorite: false
});

/**
 * Update a specific element in the recipe store
 * @param {string} element - Property to update
 * @param {any} newValue - New value to set
 */
export function updateRecipeStore(element, newValue) {
    const currentState = recipeStore.get();

    // Special handling for portion to ensure it's an integer
    if (element === 'portion') {
        const portionValue = parseInt(newValue) || 0;
        const updatedState = { ...currentState, [element]: portionValue };
        recipeStore.set(updatedState);
        return;
    }

    if (Array.isArray(currentState[element])) {
        const updatedArray = [...currentState[element], newValue];
        const updatedState = { ...currentState, [element]: updatedArray };
        recipeStore.set(updatedState);
    } else {
        const updatedState = { ...currentState, [element]: newValue };
        recipeStore.set(updatedState);
    }
}

/**
 * Swap positions of two elements in an array
 * @param {string} element - Array property name
 * @param {number} index1 - First index
 * @param {number} index2 - Second index
 */
export function swapElementsStore(element, index1, index2) {
    const currentState = recipeStore.get();

    if (Array.isArray(currentState[element]) &&
        index1 >= 0 && index1 < currentState[element].length &&
        index2 >= 0 && index2 < currentState[element].length) {

        const newArray = [...currentState[element]];
        [newArray[index1], newArray[index2]] = [newArray[index2], newArray[index1]];

        const updatedState = { ...currentState, [element]: newArray };
        recipeStore.set(updatedState);
    }
}

/**
 * Delete an element from an array
 * @param {string} element - Array property name
 * @param {number} index - Index to delete
 */
export function deleteElementStore(element, index) {
    const currentState = recipeStore.get();

    if (Array.isArray(currentState[element]) &&
        index >= 0 && index < currentState[element].length) {

        const updatedArray = [
            ...currentState[element].slice(0, index),
            ...currentState[element].slice(index + 1)
        ];

        const updatedState = { ...currentState, [element]: updatedArray };
        recipeStore.set(updatedState);
    }
}