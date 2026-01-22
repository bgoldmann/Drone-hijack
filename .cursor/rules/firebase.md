# Firebase Development Guide

Comprehensive guide for using Firebase in Cursor IDE for authentication, Firestore database operations, storage, Cloud Functions, and real-time features. Covers integration with Next.js and other frameworks.

## Overview

Firebase provides:
- **Authentication**: Built-in auth with multiple providers
- **Firestore**: NoSQL document database with real-time sync
- **Storage**: File storage with CDN
- **Cloud Functions**: Serverless functions
- **Realtime Database**: Legacy real-time database (optional)
- **Hosting**: Static and dynamic hosting

## Setup & Installation

### Install Firebase SDK

```bash
# For web projects
npm install firebase

# For Next.js
npm install firebase
```

### Initialize Firebase

```typescript
// lib/firebase/config.ts
import { initializeApp, getApps, FirebaseApp } from 'firebase/app';
import { getAuth, Auth } from 'firebase/auth';
import { getFirestore, Firestore } from 'firebase/firestore';
import { getStorage, FirebaseStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

// Initialize Firebase (prevent duplicate initialization)
const app: FirebaseApp = getApps().length === 0 
  ? initializeApp(firebaseConfig) 
  : getApps()[0];

export const auth: Auth = getAuth(app);
export const db: Firestore = getFirestore(app);
export const storage: FirebaseStorage = getStorage(app);
export default app;
```

### Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
```

**Important**: All Firebase client config variables should be prefixed with `NEXT_PUBLIC_` for Next.js.

## Authentication

### Email/Password Authentication

#### Sign Up

```typescript
import { createUserWithEmailAndPassword, updateProfile } from 'firebase/auth';
import { auth } from '@/lib/firebase/config';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function signUp(email: string, password: string, displayName?: string) {
  // Create user account
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  const user = userCredential.user;

  // Update profile if display name provided
  if (displayName) {
    await updateProfile(user, { displayName });
  }

  // Create user document in Firestore
  await setDoc(doc(db, 'users', user.uid), {
    email: user.email,
    displayName: displayName || null,
    createdAt: new Date(),
  });

  return user;
}
```

#### Sign In

```typescript
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '@/lib/firebase/config';

export async function signIn(email: string, password: string) {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
}
```

#### Sign Out

```typescript
import { signOut } from 'firebase/auth';
import { auth } from '@/lib/firebase/config';

export async function signOutUser() {
  await signOut(auth);
}
```

### Google Authentication

```typescript
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth, db } from '@/lib/firebase/config';
import { doc, setDoc, getDoc } from 'firebase/firestore';

const provider = new GoogleAuthProvider();

export async function signInWithGoogle() {
  const userCredential = await signInWithPopup(auth, provider);
  const user = userCredential.user;

  // Create or update user document
  const userDocRef = doc(db, 'users', user.uid);
  const userDoc = await getDoc(userDocRef);

  if (!userDoc.exists()) {
    await setDoc(userDocRef, {
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      createdAt: new Date(),
    });
  }

  return user;
}
```

### Get Current User

#### Client Component Hook

```typescript
'use client';

import { useEffect, useState } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth } from '@/lib/firebase/config';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return { user, loading };
}
```

#### Server Component (Next.js)

```typescript
// For server components, you'll need to pass the user as a prop
// or use Firebase Admin SDK on the server

import { cookies } from 'next/headers';
import { auth } from '@/lib/firebase/config';

// Note: For server-side auth, use Firebase Admin SDK
// See Cloud Functions section for Admin SDK usage
```

### Password Reset

```typescript
import { sendPasswordResetEmail } from 'firebase/auth';
import { auth } from '@/lib/firebase/config';

export async function resetPassword(email: string) {
  await sendPasswordResetEmail(auth, email, {
    url: `${window.location.origin}/auth/login`,
  });
}
```

## Firestore Database

### Reading Data

#### Get Single Document

```typescript
import { doc, getDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function getUser(userId: string) {
  const userDocRef = doc(db, 'users', userId);
  const userDoc = await getDoc(userDocRef);

  if (!userDoc.exists()) {
    return null;
  }

  return { id: userDoc.id, ...userDoc.data() };
}
```

#### Get Collection

```typescript
import { collection, getDocs, query, orderBy, where } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function getPosts() {
  const postsRef = collection(db, 'posts');
  const q = query(postsRef, where('published', '==', true), orderBy('createdAt', 'desc'));
  
  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data(),
  }));
}
```

#### Real-time Listener

```typescript
'use client';

import { useEffect, useState } from 'react';
import { collection, query, where, onSnapshot, orderBy } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export function usePosts(userId?: string) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const postsRef = collection(db, 'posts');
    let q = query(postsRef, orderBy('createdAt', 'desc'));

    if (userId) {
      q = query(postsRef, where('userId', '==', userId), orderBy('createdAt', 'desc'));
    }

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const postsData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data(),
      }));
      setPosts(postsData);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [userId]);

  return { posts, loading };
}
```

### Writing Data

#### Add Document

```typescript
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function createPost(postData: {
  title: string;
  content: string;
  userId: string;
}) {
  const postsRef = collection(db, 'posts');
  
  const docRef = await addDoc(postsRef, {
    ...postData,
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
    published: false,
  });

  return docRef.id;
}
```

#### Update Document

```typescript
import { doc, updateDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function updatePost(postId: string, updates: Partial<Post>) {
  const postRef = doc(db, 'posts', postId);
  
  await updateDoc(postRef, {
    ...updates,
    updatedAt: serverTimestamp(),
  });
}
```

#### Delete Document

```typescript
import { doc, deleteDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function deletePost(postId: string) {
  const postRef = doc(db, 'posts', postId);
  await deleteDoc(postRef);
}
```

#### Set Document (Create or Update)

```typescript
import { doc, setDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function setUserProfile(userId: string, profileData: UserProfile) {
  const userRef = doc(db, 'users', userId);
  
  await setDoc(userRef, {
    ...profileData,
    updatedAt: serverTimestamp(),
  }, { merge: true }); // merge: true prevents overwriting existing fields
}
```

### Advanced Queries

```typescript
import { collection, query, where, orderBy, limit, startAfter, getDocs } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

// Pagination
export async function getPostsPaginated(lastDoc?: DocumentSnapshot, pageSize: number = 10) {
  const postsRef = collection(db, 'posts');
  let q = query(
    postsRef,
    where('published', '==', true),
    orderBy('createdAt', 'desc'),
    limit(pageSize)
  );

  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }

  const snapshot = await getDocs(q);
  const posts = snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data(),
  }));

  return {
    posts,
    lastDoc: snapshot.docs[snapshot.docs.length - 1],
    hasMore: snapshot.docs.length === pageSize,
  };
}

// Complex filtering
export async function searchPosts(searchTerm: string) {
  const postsRef = collection(db, 'posts');
  const q = query(
    postsRef,
    where('published', '==', true),
    where('title', '>=', searchTerm),
    where('title', '<=', searchTerm + '\uf8ff'), // Prefix match
    limit(20)
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data(),
  }));
}
```

### Transactions

```typescript
import { runTransaction, doc } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function transferFunds(fromUserId: string, toUserId: string, amount: number) {
  await runTransaction(db, async (transaction) => {
    const fromUserRef = doc(db, 'users', fromUserId);
    const toUserRef = doc(db, 'users', toUserId);
    
    const fromUserDoc = await transaction.get(fromUserRef);
    const toUserDoc = await transaction.get(toUserRef);

    if (!fromUserDoc.exists() || !toUserDoc.exists()) {
      throw new Error('User not found');
    }

    const fromUserBalance = fromUserDoc.data().balance || 0;
    const toUserBalance = toUserDoc.data().balance || 0;

    if (fromUserBalance < amount) {
      throw new Error('Insufficient funds');
    }

    transaction.update(fromUserRef, { balance: fromUserBalance - amount });
    transaction.update(toUserRef, { balance: toUserBalance + amount });
  });
}
```

### Batch Operations

```typescript
import { writeBatch, doc } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

export async function batchUpdatePosts(postIds: string[], updates: Partial<Post>) {
  const batch = writeBatch(db);

  postIds.forEach((postId) => {
    const postRef = doc(db, 'posts', postId);
    batch.update(postRef, updates);
  });

  await batch.commit();
}
```

## Firebase Storage

### Upload Files

```typescript
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { storage } from '@/lib/firebase/config';

export async function uploadFile(file: File, path: string) {
  const storageRef = ref(storage, path);
  
  // Upload file
  await uploadBytes(storageRef, file);
  
  // Get download URL
  const downloadURL = await getDownloadURL(storageRef);
  
  return downloadURL;
}

// Example usage
export async function uploadUserAvatar(userId: string, file: File) {
  const fileExt = file.name.split('.').pop();
  const fileName = `${userId}.${fileExt}`;
  const path = `avatars/${fileName}`;
  
  return await uploadFile(file, path);
}
```

### Delete Files

```typescript
import { ref, deleteObject } from 'firebase/storage';
import { storage } from '@/lib/firebase/config';

export async function deleteFile(path: string) {
  const storageRef = ref(storage, path);
  await deleteObject(storageRef);
}
```

### Get Download URL

```typescript
import { ref, getDownloadURL } from 'firebase/storage';
import { storage } from '@/lib/firebase/config';

export async function getFileURL(path: string) {
  const storageRef = ref(storage, path);
  return await getDownloadURL(storageRef);
}
```

### List Files

```typescript
import { ref, listAll } from 'firebase/storage';
import { storage } from '@/lib/firebase/config';

export async function listUserFiles(userId: string) {
  const folderRef = ref(storage, `users/${userId}`);
  const result = await listAll(folderRef);
  
  return {
    items: result.items.map(item => item.name),
    prefixes: result.prefixes.map(prefix => prefix.name),
  };
}
```

## Security Rules

### Firestore Security Rules

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Helper function to check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }

    // Helper function to check if user owns the document
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }

    // Users collection
    match /users/{userId} {
      // Anyone can read user profiles
      allow read: if true;
      
      // Only the user can update their own profile
      allow update: if isOwner(userId);
      
      // Only authenticated users can create profiles
      allow create: if isAuthenticated() && request.auth.uid == userId;
    }

    // Posts collection
    match /posts/{postId} {
      // Published posts are publicly readable
      allow read: if resource.data.published == true || isOwner(resource.data.userId);
      
      // Only post owner can create/update/delete
      allow create: if isAuthenticated() && request.auth.uid == request.resource.data.userId;
      allow update, delete: if isAuthenticated() && isOwner(resource.data.userId);
    }

    // Comments collection (subcollection)
    match /posts/{postId}/comments/{commentId} {
      allow read: if true;
      allow create: if isAuthenticated();
      allow update, delete: if isAuthenticated() && isOwner(resource.data.userId);
    }
  }
}
```

### Storage Security Rules

```javascript
// storage.rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Avatars: users can upload/update their own avatar
    match /avatars/{userId}/{fileName} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == userId;
    }

    // Posts: authenticated users can upload, public read
    match /posts/{postId}/{fileName} {
      allow read: if true;
      allow write: if request.auth != null;
    }

    // Private files: only owner can access
    match /users/{userId}/private/{fileName} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Cloud Functions (Firebase Admin SDK)

### Setup Firebase Admin

```bash
npm install firebase-admin
```

```typescript
// lib/firebase/admin.ts (Server-side only)
import { initializeApp, getApps, cert, ServiceAccount } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';

if (!getApps().length) {
  initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
    } as ServiceAccount),
  });
}

export const adminAuth = getAuth();
export const adminDb = getFirestore();
```

### Server-Side Authentication Verification

```typescript
import { adminAuth } from '@/lib/firebase/admin';

export async function verifyIdToken(idToken: string) {
  try {
    const decodedToken = await adminAuth.verifyIdToken(idToken);
    return decodedToken;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// Next.js API route example
export async function GET(request: Request) {
  const idToken = request.headers.get('Authorization')?.split('Bearer ')[1];
  
  if (!idToken) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const decodedToken = await verifyIdToken(idToken);
    // Use decodedToken.uid for user operations
    return Response.json({ userId: decodedToken.uid });
  } catch (error) {
    return Response.json({ error: 'Invalid token' }, { status: 401 });
  }
}
```

### Server-Side Firestore Operations

```typescript
import { adminDb } from '@/lib/firebase/admin';

export async function getUserServer(userId: string) {
  const userDoc = await adminDb.collection('users').doc(userId).get();
  
  if (!userDoc.exists) {
    return null;
  }

  return { id: userDoc.id, ...userDoc.data() };
}
```

## Best Practices

### 1. Index Management

Firestore requires composite indexes for complex queries. Create them via:
- Firebase Console → Firestore → Indexes
- Or automatically via error messages in development

```javascript
// Example index needed for:
// query(where('status', '==', 'published'), orderBy('createdAt', 'desc'))
// Created automatically when error occurs in development
```

### 2. Use Server Timestamps

Always use `serverTimestamp()` for timestamps:

```typescript
import { serverTimestamp } from 'firebase/firestore';

await setDoc(docRef, {
  createdAt: serverTimestamp(), // ✅ Correct
  // createdAt: new Date(), // ❌ Wrong - uses client time
});
```

### 3. Optimize Real-time Listeners

```typescript
// ✅ Good: Clean up listeners
useEffect(() => {
  const unsubscribe = onSnapshot(collectionRef, callback);
  return () => unsubscribe();
}, []);

// ❌ Bad: Memory leak
useEffect(() => {
  onSnapshot(collectionRef, callback);
  // No cleanup!
}, []);
```

### 4. Handle Offline Persistence

```typescript
import { enableIndexedDbPersistence } from 'firebase/firestore';
import { db } from '@/lib/firebase/config';

// Enable offline persistence (one time)
enableIndexedDbPersistence(db).catch((err) => {
  if (err.code == 'failed-precondition') {
    console.warn('Multiple tabs open, persistence can only be enabled in one tab');
  } else if (err.code == 'unimplemented') {
    console.warn('Browser does not support persistence');
  }
});
```

### 5. Error Handling

```typescript
import { doc, getDoc } from 'firebase/firestore';
import { FirestoreError } from 'firebase/firestore';

export async function getUserSafe(userId: string) {
  try {
    const userDoc = await getDoc(doc(db, 'users', userId));
    if (!userDoc.exists()) {
      return null;
    }
    return { id: userDoc.id, ...userDoc.data() };
  } catch (error) {
    if (error instanceof FirestoreError) {
      if (error.code === 'permission-denied') {
        console.error('Permission denied');
      } else {
        console.error('Firestore error:', error.message);
      }
    }
    throw error;
  }
}
```

### 6. Pagination Best Practices

```typescript
// Use cursor-based pagination (recommended)
export async function getPostsCursor(lastDoc?: DocumentSnapshot) {
  const postsRef = collection(db, 'posts');
  let q = query(
    postsRef,
    orderBy('createdAt', 'desc'),
    limit(10)
  );

  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }

  const snapshot = await getDocs(q);
  return {
    posts: snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })),
    lastDoc: snapshot.docs[snapshot.docs.length - 1],
  };
}
```

## Common Patterns

### User Profile Pattern

```typescript
// Create profile on signup
export async function createUserProfile(user: User) {
  const userRef = doc(db, 'users', user.uid);
  await setDoc(userRef, {
    email: user.email,
    displayName: user.displayName,
    photoURL: user.photoURL,
    createdAt: serverTimestamp(),
  });
}
```

### Counter Pattern (using transactions)

```typescript
export async function incrementLikeCount(postId: string) {
  const postRef = doc(db, 'posts', postId);
  
  await runTransaction(db, async (transaction) => {
    const postDoc = await transaction.get(postRef);
    if (!postDoc.exists()) {
      throw new Error('Post not found');
    }
    
    const currentLikes = postDoc.data().likes || 0;
    transaction.update(postRef, { likes: currentLikes + 1 });
  });
}
```

### Denormalization Pattern

```typescript
// Store user info in posts for faster queries (denormalization)
export async function createPost(postData: { title: string; content: string; userId: string }) {
  const userDoc = await getDoc(doc(db, 'users', postData.userId));
  const userData = userDoc.data();

  await addDoc(collection(db, 'posts'), {
    ...postData,
    authorName: userData?.displayName, // Denormalized
    authorPhoto: userData?.photoURL,   // Denormalized
    createdAt: serverTimestamp(),
  });
}
```

## Checklist for Firebase Integration

Before committing Firebase-related code:

- [ ] Environment variables configured and documented
- [ ] Firestore security rules implemented and tested
- [ ] Storage security rules implemented and tested
- [ ] Real-time listeners properly cleaned up (unsubscribe)
- [ ] Server timestamps used instead of client Date
- [ ] Error handling for all Firebase operations
- [ ] Composite indexes created for complex queries
- [ ] Offline persistence enabled if needed
- [ ] Firebase Admin SDK used only server-side
- [ ] Authentication state properly managed
- [ ] File uploads have size/type validation
- [ ] Security rules tested in Firebase Console