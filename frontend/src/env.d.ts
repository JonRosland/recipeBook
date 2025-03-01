/// <reference types="astro/client" />

interface ImportMetaEnv {
    readonly PUBLIC_API_URL: string;
    readonly PUBLIC_ENABLE_FAVORITES: string;
    readonly PUBLIC_ENABLE_SEARCH: string;
    readonly PUBLIC_THEME: string;
    readonly PUBLIC_ITEMS_PER_PAGE: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}