# Design Doc: Sentinel View Counter (Shields.io Endpoint)

## Overview
A dynamic, serverless view counter for the GitHub Portfolio README, designed to showcase architectural and security skills while matching the "Tokyonight" aesthetic of the existing portfolio stats.

## User Intent
- Implement a custom page view counter using the Shields.io Endpoint Badge.
- Host the backend on Vercel.
- Use Upstash Redis for data persistence.
- Match the aesthetic of the existing "Tokyonight" theme stats.

## Architecture

### 1. Data Flow
1. **Request**: GitHub README loads -> Shields.io requests data from the Vercel endpoint.
2. **Processing**: Vercel Serverless Function (Node.js) receives the request.
3. **Storage**: Vercel function calls `INCR` on Upstash Redis to record the hit.
4. **Response**: Vercel returns a JSON object formatted for Shields.io.
5. **Display**: Shields.io renders the SVG badge with the updated count.

### 2. Tech Stack
-   **Frontend**: Shields.io Endpoint Badge.
-   **Backend**: Vercel Serverless Functions.
-   **Database**: Upstash Redis (REST API).
-   **Language**: JavaScript (Node.js).

### 3. Design & Style (Tokyonight)
-   **Label**: `SENTINEL VIEWS`
-   **Label Color**: `#1a1b26` (Dark Navy)
-   **Message Color**: `#7aa2f7` (Tokyonight Blue)
-   **Style**: `for-the-badge` (to match existing badges)
-   **Logo**: `security-gate` or `eye` (optional).

## Implementation Plan (Brief)
1.  Initialize a new Vercel project structure locally.
2.  Install `ioredis` or use `@upstash/redis` to interact with the database.
3.  Create the `api/views.js` endpoint.
4.  Configure Vercel environment variables (Upstash URL and Token).
5.  Deploy to Vercel.
6.  Update `README.md` with the new badge link.

## Security Considerations
-   **Secrets Management**: Upstash credentials will be stored in Vercel Environment Variables, NEVER committed to GitHub.
-   **Read-Only/Write-Only**: Since the endpoint is public, it will only have permission to increment the specific `view_count` key.

## Success Criteria
-   The badge displays a count that increments on (uncached) refreshes.
-   The aesthetic matches the existing GitHub Readme Stats.
-   The logic is documented and verifiable in the repository.
