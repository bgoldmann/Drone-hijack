# Google Services Integration Guide

Comprehensive guide for integrating Google services and APIs in applications. Covers Google Cloud Platform (GCP), Google Analytics, Google Maps, Google OAuth, Google Drive, and other Google services.

## Overview

This guide covers integration with various Google services commonly used in web and mobile applications. Includes authentication, API usage, best practices, and common patterns.

## Google Cloud Platform (GCP)

### Setup and Authentication

#### Service Account (Server-side)

```typescript
// Install: npm install google-auth-library
import { GoogleAuth } from 'google-auth-library';

const auth = new GoogleAuth({
  keyFilename: 'path/to/service-account-key.json',
  scopes: ['https://www.googleapis.com/auth/cloud-platform'],
});

const client = await auth.getClient();
```

#### OAuth 2.0 Client (User Authentication)

```typescript
// Install: npm install googleapis
import { google } from 'googleapis';

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);

// Generate auth URL
const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: ['https://www.googleapis.com/auth/userinfo.email'],
});

// Exchange code for tokens
const { tokens } = await oauth2Client.getToken(code);
oauth2Client.setCredentials(tokens);
```

### Google Cloud Storage

```typescript
import { Storage } from '@google-cloud/storage';

const storage = new Storage({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: 'path/to/service-account-key.json',
});

const bucket = storage.bucket('my-bucket');

// Upload file
async function uploadFile(filePath: string, destFileName: string) {
  await bucket.upload(filePath, {
    destination: destFileName,
    metadata: {
      cacheControl: 'public, max-age=31536000',
    },
  });
}

// Generate signed URL
async function getSignedUrl(fileName: string, expiresIn: number = 3600) {
  const file = bucket.file(fileName);
  const [url] = await file.getSignedUrl({
    action: 'read',
    expires: Date.now() + expiresIn * 1000,
  });
  return url;
}

// Download file
async function downloadFile(fileName: string, destPath: string) {
  await bucket.file(fileName).download({ destination: destPath });
}
```

### Google Cloud Firestore

```typescript
import { Firestore } from '@google-cloud/firestore';

const db = new Firestore({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: 'path/to/service-account-key.json',
});

// Create document
async function createDocument(collection: string, data: any, docId?: string) {
  const docRef = docId 
    ? db.collection(collection).doc(docId)
    : db.collection(collection).doc();
  
  await docRef.set(data);
  return docRef.id;
}

// Read document
async function getDocument(collection: string, docId: string) {
  const doc = await db.collection(collection).doc(docId).get();
  if (!doc.exists) return null;
  return { id: doc.id, ...doc.data() };
}

// Query documents
async function queryDocuments(collection: string, filters: any[]) {
  let query: any = db.collection(collection);
  
  for (const filter of filters) {
    query = query.where(filter.field, filter.operator, filter.value);
  }
  
  const snapshot = await query.get();
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
}

// Update document
async function updateDocument(collection: string, docId: string, data: any) {
  await db.collection(collection).doc(docId).update(data);
}

// Delete document
async function deleteDocument(collection: string, docId: string) {
  await db.collection(collection).doc(docId).delete();
}
```

## Google OAuth 2.0

### Server-side OAuth Flow

#### Next.js API Route

```typescript
// app/api/auth/google/route.ts
import { google } from 'googleapis';
import { NextResponse } from 'next/server';

const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI
);

// Step 1: Initiate OAuth
export async function GET(request: Request) {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: [
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile',
    ],
    prompt: 'consent', // Force consent screen to get refresh token
  });

  return NextResponse.redirect(authUrl);
}

// Step 2: Handle callback
// app/api/auth/google/callback/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  if (!code) {
    return NextResponse.json({ error: 'No code provided' }, { status: 400 });
  }

  const { tokens } = await oauth2Client.getToken(code);
  oauth2Client.setCredentials(tokens);

  // Get user info
  const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
  const { data } = await oauth2.userinfo.get();

  // Store tokens and user info (in session, database, etc.)
  // ...

  return NextResponse.redirect('/dashboard');
}
```

### Client-side OAuth (Google Identity Services)

```typescript
// Install: npm install @react-oauth/google
import { GoogleOAuthProvider, useGoogleLogin } from '@react-oauth/google';

function GoogleLoginButton() {
  const login = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      // Exchange code for user info
      const response = await fetch('/api/auth/google/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: tokenResponse.code }),
      });
      
      const userData = await response.json();
      // Handle user data
    },
    flow: 'auth-code', // Use authorization code flow
  });

  return <button onClick={() => login()}>Sign in with Google</button>;
}

// App setup
function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID!}>
      <GoogleLoginButton />
    </GoogleOAuthProvider>
  );
}
```

## Google Analytics

### Google Analytics 4 (GA4) Integration

#### Client-side (gtag)

```html
<!-- In HTML head -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

#### Next.js Integration

```typescript
// lib/analytics.ts
export const GA_TRACKING_ID = process.env.NEXT_PUBLIC_GA_ID!;

export function pageview(url: string) {
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('config', GA_TRACKING_ID, {
      page_path: url,
    });
  }
}

export function event(action: string, category: string, label?: string, value?: number) {
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
}

// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          strategy="afterInteractive"
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
        />
        <Script
          id="google-analytics"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${GA_TRACKING_ID}');
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Server-side Analytics (Measurement Protocol)

```typescript
async function trackServerEvent(eventName: string, params: any) {
  const measurementId = process.env.GA4_MEASUREMENT_ID;
  const apiSecret = process.env.GA4_API_SECRET;

  await fetch(
    `https://www.google-analytics.com/mp/collect?measurement_id=${measurementId}&api_secret=${apiSecret}`,
    {
      method: 'POST',
      body: JSON.stringify({
        client_id: generateClientId(),
        events: [
          {
            name: eventName,
            params: params,
          },
        ],
      }),
    }
  );
}
```

## Google Maps

### Google Maps JavaScript API

```typescript
// Install: npm install @react-google-maps/api
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '400px',
};

const center = {
  lat: 37.7749,
  lng: -122.4194,
};

function MapComponent() {
  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!}>
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={center}
        zoom={10}
      >
        <Marker position={center} />
      </GoogleMap>
    </LoadScript>
  );
}
```

### Geocoding API

```typescript
// Server-side geocoding
async function geocodeAddress(address: string) {
  const response = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${process.env.GOOGLE_MAPS_API_KEY}`
  );

  const data = await response.json();
  if (data.results && data.results.length > 0) {
    return data.results[0].geometry.location;
  }
  return null;
}

// Reverse geocoding
async function reverseGeocode(lat: number, lng: number) {
  const response = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${process.env.GOOGLE_MAPS_API_KEY}`
  );

  const data = await response.json();
  if (data.results && data.results.length > 0) {
    return data.results[0].formatted_address;
  }
  return null;
}
```

### Places API

```typescript
// Autocomplete
async function getPlaceAutocomplete(input: string) {
  const response = await fetch(
    `https://maps.googleapis.com/maps/api/place/autocomplete/json?input=${encodeURIComponent(input)}&key=${process.env.GOOGLE_MAPS_API_KEY}`
  );

  const data = await response.json();
  return data.predictions.map((prediction: any) => ({
    placeId: prediction.place_id,
    description: prediction.description,
  }));
}

// Place details
async function getPlaceDetails(placeId: string) {
  const response = await fetch(
    `https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&fields=name,formatted_address,geometry,rating,photos&key=${process.env.GOOGLE_MAPS_API_KEY}`
  );

  const data = await response.json();
  return data.result;
}
```

## Google Drive API

### Upload to Google Drive

```typescript
import { google } from 'googleapis';

async function uploadToDrive(filePath: string, fileName: string) {
  const drive = google.drive({ version: 'v3', auth: oauth2Client });

  const fileMetadata = {
    name: fileName,
  };

  const media = {
    mimeType: 'application/pdf',
    body: fs.createReadStream(filePath),
  };

  const response = await drive.files.create({
    requestBody: fileMetadata,
    media: media,
    fields: 'id',
  });

  return response.data.id;
}
```

### Share Google Drive File

```typescript
async function shareDriveFile(fileId: string, email: string, role: string = 'reader') {
  const drive = google.drive({ version: 'v3', auth: oauth2Client });

  await drive.permissions.create({
    fileId: fileId,
    requestBody: {
      role: role, // 'reader', 'writer', 'commenter'
      type: 'user',
      emailAddress: email,
    },
  });
}
```

### List Drive Files

```typescript
async function listDriveFiles(query?: string) {
  const drive = google.drive({ version: 'v3', auth: oauth2Client });

  const response = await drive.files.list({
    q: query, // e.g., "mimeType='application/pdf'"
    pageSize: 10,
    fields: 'nextPageToken, files(id, name, mimeType, size)',
  });

  return response.data.files;
}
```

## Google Sheets API

### Read from Google Sheets

```typescript
import { google } from 'googleapis';

async function readSheet(spreadsheetId: string, range: string) {
  const sheets = google.sheets({ version: 'v4', auth: oauth2Client });

  const response = await sheets.spreadsheets.values.get({
    spreadsheetId: spreadsheetId,
    range: range, // e.g., 'Sheet1!A1:D10'
  });

  return response.data.values;
}
```

### Write to Google Sheets

```typescript
async function writeSheet(spreadsheetId: string, range: string, values: any[][]) {
  const sheets = google.sheets({ version: 'v4', auth: oauth2Client });

  await sheets.spreadsheets.values.update({
    spreadsheetId: spreadsheetId,
    range: range,
    valueInputOption: 'RAW',
    requestBody: {
      values: values,
    },
  });
}
```

### Create Spreadsheet

```typescript
async function createSpreadsheet(title: string) {
  const sheets = google.sheets({ version: 'v4', auth: oauth2Client });

  const response = await sheets.spreadsheets.create({
    requestBody: {
      properties: {
        title: title,
      },
    },
  });

  return response.data.spreadsheetId;
}
```

## Google Cloud Pub/Sub

### Publish Messages

```typescript
import { PubSub } from '@google-cloud/pubsub';

const pubsub = new PubSub({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: 'path/to/service-account-key.json',
});

async function publishMessage(topicName: string, data: any) {
  const topic = pubsub.topic(topicName);
  const dataBuffer = Buffer.from(JSON.stringify(data));

  const messageId = await topic.publishMessage({ data: dataBuffer });
  return messageId;
}
```

### Subscribe to Messages

```typescript
async function subscribeToTopic(topicName: string, subscriptionName: string) {
  const topic = pubsub.topic(topicName);
  const subscription = topic.subscription(subscriptionName);

  subscription.on('message', (message) => {
    const data = JSON.parse(message.data.toString());
    // Process message
    console.log('Received message:', data);
    
    // Acknowledge message
    message.ack();
  });
}
```

## Google Cloud Functions

### Deploy Cloud Function

```typescript
// functions/index.ts
import { onRequest } from 'firebase-functions/v2/https';

export const helloWorld = onRequest((request, response) => {
  response.json({
    message: 'Hello from Firebase Cloud Functions!',
    timestamp: new Date().toISOString(),
  });
});

// Deploy: firebase deploy --only functions
```

### Cloud Function with Express

```typescript
import * as functions from 'firebase-functions';
import * as express from 'express';

const app = express();

app.get('/api/users', async (req, res) => {
  // Your logic
  const users = await getUsers();
  res.json(users);
});

export const api = functions.https.onRequest(app);
```

## Google Search Console API

### Query Search Console Data

```typescript
import { google } from 'googleapis';

async function getSearchConsoleData(siteUrl: string, startDate: string, endDate: string) {
  const searchconsole = google.searchconsole({ version: 'v1', auth: oauth2Client });

  const response = await searchconsole.searchanalytics.query({
    siteUrl: siteUrl,
    requestBody: {
      startDate: startDate, // YYYY-MM-DD
      endDate: endDate,
      dimensions: ['query', 'page'],
      rowLimit: 10,
    },
  });

  return response.data.rows;
}
```

## Google Calendar API

### Create Calendar Event

```typescript
import { google } from 'googleapis';

async function createCalendarEvent(
  summary: string,
  startTime: Date,
  endTime: Date,
  attendees?: string[]
) {
  const calendar = google.calendar({ version: 'v3', auth: oauth2Client });

  const event = {
    summary: summary,
    start: {
      dateTime: startTime.toISOString(),
      timeZone: 'America/Los_Angeles',
    },
    end: {
      dateTime: endTime.toISOString(),
      timeZone: 'America/Los_Angeles',
    },
    attendees: attendees?.map(email => ({ email })),
    reminders: {
      useDefault: false,
      overrides: [
        { method: 'email', minutes: 24 * 60 },
        { method: 'popup', minutes: 10 },
      ],
    },
  };

  const response = await calendar.events.insert({
    calendarId: 'primary',
    requestBody: event,
  });

  return response.data;
}
```

### List Calendar Events

```typescript
async function listCalendarEvents(timeMin: Date, timeMax: Date) {
  const calendar = google.calendar({ version: 'v3', auth: oauth2Client });

  const response = await calendar.events.list({
    calendarId: 'primary',
    timeMin: timeMin.toISOString(),
    timeMax: timeMax.toISOString(),
    maxResults: 10,
    singleEvents: true,
    orderBy: 'startTime',
  });

  return response.data.items;
}
```

## Google Translate API

### Translate Text

```typescript
import { Translate } from '@google-cloud/translate/build/src/v2';

const translate = new Translate({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: 'path/to/service-account-key.json',
});

async function translateText(text: string, targetLanguage: string) {
  const [translation] = await translate.translate(text, targetLanguage);
  return translation;
}

// Detect language
async function detectLanguage(text: string) {
  const [detection] = await translate.detect(text);
  return detection.language;
}

// Batch translate
async function translateBatch(texts: string[], targetLanguage: string) {
  const [translations] = await translate.translate(texts, targetLanguage);
  return translations;
}
```

## Environment Variables

```bash
# .env.local or .env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback

# Google Cloud Platform
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# APIs
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-maps-api-key
GOOGLE_MAPS_API_KEY=your-maps-api-key-server
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GA4_API_SECRET=your-api-secret
```

## Best Practices

### 1. API Key Security

```typescript
// Public keys (client-side) - OK to expose
const publicKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

// Private keys (server-side) - NEVER expose
const privateKey = process.env.GOOGLE_CLIENT_SECRET;

// Restrict API keys in Google Cloud Console
// - HTTP referrers for Maps API
// - Application restrictions for OAuth
```

### 2. Rate Limiting

```typescript
// Implement rate limiting for Google API calls
class GoogleAPIRateLimiter {
  private requests: Map<string, number[]> = new Map();

  async checkLimit(apiName: string, limit: number, windowMs: number) {
    const now = Date.now();
    const requests = this.requests.get(apiName) || [];
    const recent = requests.filter(time => now - time < windowMs);

    if (recent.length >= limit) {
      const oldest = Math.min(...recent);
      const waitTime = windowMs - (now - oldest);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }

    this.requests.set(apiName, [...recent, now]);
  }
}
```

### 3. Error Handling

```typescript
import { GoogleAuthError } from 'google-auth-library';

async function safeGoogleAPICall(apiCall: () => Promise<any>) {
  try {
    return await apiCall();
  } catch (error: any) {
    if (error.code === 401) {
      // Re-authenticate
      await refreshAuthToken();
      return await apiCall();
    } else if (error.code === 429) {
      // Rate limit - retry with backoff
      await new Promise(resolve => setTimeout(resolve, 1000));
      return await apiCall();
    } else {
      throw error;
    }
  }
}
```

### 4. Token Refresh

```typescript
oauth2Client.on('tokens', (tokens) => {
  if (tokens.refresh_token) {
    // Store refresh token securely
    saveRefreshToken(tokens.refresh_token);
  }
  
  // Update access token
  oauth2Client.setCredentials(tokens);
});

async function refreshAccessToken() {
  const { credentials } = await oauth2Client.refreshAccessToken();
  oauth2Client.setCredentials(credentials);
  return credentials;
}
```

## Common Patterns

### Google OAuth Wrapper

```typescript
class GoogleAuthService {
  private oauth2Client: any;

  constructor() {
    this.oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );
  }

  getAuthUrl() {
    return this.oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
      ],
    });
  }

  async getTokens(code: string) {
    const { tokens } = await this.oauth2Client.getToken(code);
    this.oauth2Client.setCredentials(tokens);
    return tokens;
  }

  async getUserInfo() {
    const oauth2 = google.oauth2({ version: 'v2', auth: this.oauth2Client });
    const { data } = await oauth2.userinfo.get();
    return data;
  }
}
```

### Service Account Singleton

```typescript
import { GoogleAuth } from 'google-auth-library';

class GoogleCloudService {
  private static instance: GoogleCloudService;
  private auth: GoogleAuth;

  private constructor() {
    this.auth = new GoogleAuth({
      keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
      scopes: ['https://www.googleapis.com/auth/cloud-platform'],
    });
  }

  static getInstance() {
    if (!GoogleCloudService.instance) {
      GoogleCloudService.instance = new GoogleCloudService();
    }
    return GoogleCloudService.instance;
  }

  async getAuthClient() {
    return await this.auth.getClient();
  }
}
```

## Checklist for Google Services Integration

Before deploying Google services integration:

- [ ] API keys stored in environment variables
- [ ] OAuth credentials configured in Google Cloud Console
- [ ] API keys restricted (HTTP referrers, IPs, etc.)
- [ ] Service account keys secured (not in git)
- [ ] Required APIs enabled in Google Cloud Console
- [ ] Error handling for authentication failures
- [ ] Token refresh logic implemented (OAuth)
- [ ] Rate limiting implemented
- [ ] API quotas monitored
- [ ] Billing alerts configured
- [ ] Client-side vs server-side keys properly separated
- [ ] CORS configured correctly for client-side APIs

## Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google API Client Libraries](https://cloud.google.com/apis/docs/client-libraries-explained)
- [OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
- [Google API Explorer](https://developers.google.com/apis-explorer)
