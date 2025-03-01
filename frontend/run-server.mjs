// Entry point for Deno server
import { handle } from './dist/server/entry.mjs';

// Load environment variables
const PORT = parseInt(Deno.env.get("PORT") || "8085");
const BASE_PATH = Deno.env.get("BASE_PATH") || "/";

// Docker internal network backend URL (container to container communication)
const BACKEND_URL = Deno.env.get("SERVER_API_URL") || "http://backend:6088/api/";
console.log(`Starting server on port ${PORT}`);
console.log(`Backend URL: ${BACKEND_URL}`);

// Add more debugging
console.log(`Environment variables loaded:`);
console.log(`- SERVER_API_URL: ${Deno.env.get("SERVER_API_URL") || "not set"}`);
console.log(`- PUBLIC_API_URL: ${Deno.env.get("PUBLIC_API_URL") || "not set"}`);
console.log(`- PORT: ${PORT}`);
console.log(`- BASE_PATH: ${BASE_PATH}`);

// Create a request handler
async function handleRequest(request) {
    const url = new URL(request.url);
    
    // API Proxy - intercept all /api/ requests and forward them to the backend
    if (url.pathname.startsWith('/api/')) {
        try {
            console.log(`Proxying API request: ${request.method} ${url.pathname} -> ${BACKEND_URL}`);
            
            // Handle OPTIONS requests for CORS preflight
            if (request.method === 'OPTIONS') {
                console.log(`Handling CORS preflight request for ${url.pathname}`);
                return new Response(null, {
                    status: 204, // No content
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
                        'Access-Control-Max-Age': '86400', // 24 hours
                    }
                });
            }
            
            // The backend API already includes "/api/" in its base URL
            // So we need to be careful not to duplicate it
            let apiPath = url.pathname.slice(5); // Remove the leading '/api/'
            
            // For the root API endpoint, don't add another slash
            const backendUrl = apiPath ? `${BACKEND_URL}${apiPath}${url.search}` : BACKEND_URL;
            
            console.log(`Full backend URL: ${backendUrl}`);
            
            // Create the headers object to forward
            const headers = new Headers(request.headers);
            
            // Handle request body differently based on content type and method
            let requestBody = undefined;
            if (request.method !== 'GET' && request.method !== 'HEAD') {
                const contentType = request.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    // For JSON content, get the text and keep it as text to prevent encoding issues
                    requestBody = await request.text();
                    console.log(`JSON Request payload: ${requestBody}`);
                } else {
                    // For other content types, use blob
                    requestBody = await request.blob();
                }
            }
            
            // Forward the request to the backend
            const proxyRequest = new Request(backendUrl, {
                method: request.method,
                headers: headers,
                body: requestBody,
            });
            
            // Send the request to the backend through Docker network
            const backendResponse = await fetch(proxyRequest);
            
            console.log(`Backend response status: ${backendResponse.status}`);
            
            // Create new headers without the Content-Encoding header to avoid issues
            const newHeaders = new Headers();
            backendResponse.headers.forEach((value, key) => {
                if (key.toLowerCase() !== 'content-encoding') {
                    newHeaders.set(key, value);
                }
            });
            
            // Ensure CORS headers are properly set
            newHeaders.set('Access-Control-Allow-Origin', '*');
            newHeaders.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
            newHeaders.set('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
            
            // Forward the response back to the client
            return new Response(backendResponse.body, {
                status: backendResponse.status,
                statusText: backendResponse.statusText,
                headers: newHeaders,
            });
        } catch (error) {
            console.error(`Error proxying API request: ${error.message}`);
            return new Response(`API Proxy Error: ${error.message}`, { status: 500 });
        }
    }

    // For static files in the client directory
    if (url.pathname.startsWith(BASE_PATH)) {
        try {
            // Handle root path
            if (url.pathname === BASE_PATH || url.pathname === BASE_PATH + '/') {
                // Let the SSR handler deal with the root path
                // This falls through to the SSR handler below
            } else {
                const staticPath = url.pathname.replace(BASE_PATH, '/');
                let filePath = `./dist/client${staticPath}`;
                
                // Special case for favicon
                if (staticPath === '/favicon.svg') {
                    filePath = './dist/client/icons/favicon.svg';
                }

                try {
                    const file = await Deno.readFile(filePath);

                    // Basic MIME type mapping
                    const extension = filePath.split('.').pop() || '';
                    const mimeTypes = {
                        'html': 'text/html',
                        'css': 'text/css',
                        'js': 'text/javascript',
                        'mjs': 'text/javascript',
                        'json': 'application/json',
                        'png': 'image/png',
                        'jpg': 'image/jpeg',
                        'jpeg': 'image/jpeg',
                        'svg': 'image/svg+xml',
                        'ico': 'image/x-icon',
                    };

                    const contentType = mimeTypes[extension] || 'text/plain';

                    return new Response(file, {
                        status: 200,
                        headers: {
                            'Content-Type': contentType,
                        },
                    });
                } catch (error) {
                    console.log(`File not found: ${filePath}, falling back to SSR`);
                    // File not found, proceed to SSR handler
                }
            }
        } catch (error) {
            console.error("Error serving static file:", error);
        }
    }

    // Pass to Astro SSR handler for dynamic routes
    try {
        // Create context with environment variables for SSR
        const envVars = {
            // IMPORTANT: Use relative URL for PUBLIC_API_URL 
            // This is what client-side code will use
            PUBLIC_API_URL: '/api/',
            // For server-side rendering, use the internal Docker URL
            SERVER_API_URL: BACKEND_URL,
            PUBLIC_ENABLE_FAVORITES: Deno.env.get("PUBLIC_ENABLE_FAVORITES") || "true",
            PUBLIC_ENABLE_SEARCH: Deno.env.get("PUBLIC_ENABLE_SEARCH") || "true",
            PUBLIC_THEME: Deno.env.get("PUBLIC_THEME") || "light",
            PUBLIC_ITEMS_PER_PAGE: Deno.env.get("PUBLIC_ITEMS_PER_PAGE") || "12",
        };

        return await handle(request, { env: envVars });
    } catch (error) {
        console.error("Error in SSR handler:", error);
        return new Response("Server Error", { status: 500 });
    }
}

// Start the server
Deno.serve({ port: PORT, hostname: "0.0.0.0" }, handleRequest);