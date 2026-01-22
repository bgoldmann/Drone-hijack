# Coinbase Commerce Integration Guide

Comprehensive guide for integrating Coinbase Commerce for cryptocurrency payments in Cursor IDE. Covers charge creation, webhooks, payment verification, and best practices.

## Overview

Coinbase Commerce provides:
- **Cryptocurrency Payments**: Accept BTC, ETH, and other cryptocurrencies
- **Charge API**: Create payment charges
- **Webhooks**: Real-time payment notifications
- **Payment Pages**: Hosted checkout pages
- **Direct API Integration**: Custom payment flows

## Setup & Configuration

### API Keys

```bash
# .env.local (Next.js) / .env (FastAPI)
COINBASE_COMMERCE_API_KEY=your-api-key
COINBASE_COMMERCE_WEBHOOK_SECRET=your-webhook-secret

# Production
COINBASE_COMMERCE_API_KEY=live-api-key
COINBASE_COMMERCE_WEBHOOK_SECRET=live-webhook-secret
```

### Install SDK

```bash
# JavaScript/TypeScript
npm install coinbase-commerce-node

# Python
pip install coinbasecommerce
```

## Creating Charges

### Next.js API Route

```typescript
// app/api/coinbase/create-charge/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { Client, resources } from 'coinbase-commerce-node';

const client = Client.init(process.env.COINBASE_COMMERCE_API_KEY!);
const { Charge } = resources;

export async function POST(request: NextRequest) {
  try {
    const { amount, currency = 'USD', metadata } = await request.json();
    
    const chargeData = {
      name: 'Product Purchase',
      description: 'Purchase description',
      local_price: {
        amount: amount.toString(),
        currency: currency.toUpperCase(),
      },
      pricing_type: 'fixed_price',
      metadata: {
        orderId: metadata?.orderId,
        userId: metadata?.userId,
        ...metadata,
      },
    };
    
    const charge = await Charge.create(chargeData);
    
    return NextResponse.json({
      chargeId: charge.id,
      hostedUrl: charge.hosted_url,
      code: charge.code,
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 400 }
    );
  }
}
```

### FastAPI Endpoint

```python
# app/api/coinbase.py
from fastapi import APIRouter, HTTPException
from coinbasecommerce.client import Client
from coinbasecommerce.resources import Charge
import os

router = APIRouter()
client = Client(api_key=os.environ.get("COINBASE_COMMERCE_API_KEY"))

@router.post("/coinbase/create-charge")
async def create_charge(amount: float, currency: str = "USD", metadata: dict = None):
    try:
        charge_data = {
            "name": "Product Purchase",
            "description": "Purchase description",
            "local_price": {
                "amount": str(amount),
                "currency": currency.upper(),
            },
            "pricing_type": "fixed_price",
            "metadata": metadata or {},
        }
        
        charge = Charge.create(**charge_data)
        
        return {
            "charge_id": charge.id,
            "hosted_url": charge.hosted_url,
            "code": charge.code,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Client-Side Usage

```typescript
'use client';

export function PayButton({ amount, orderId }: { amount: number; orderId: string }) {
  const handlePayment = async () => {
    const response = await fetch('/api/coinbase/create-charge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount,
        currency: 'USD',
        metadata: { orderId },
      }),
    });
    
    const { hostedUrl } = await response.json();
    
    // Redirect to Coinbase Commerce hosted page
    window.location.href = hostedUrl;
  };
  
  return <button onClick={handlePayment}>Pay with Crypto</button>;
}
```

## Retrieving Charges

### Check Charge Status

```typescript
// app/api/coinbase/check-charge/route.ts
import { Client, resources } from 'coinbase-commerce-node';

const client = Client.init(process.env.COINBASE_COMMERCE_API_KEY!);
const { Charge } = resources;

export async function GET(request: NextRequest) {
  const chargeId = request.nextUrl.searchParams.get('chargeId');
  
  if (!chargeId) {
    return NextResponse.json({ error: 'Charge ID required' }, { status: 400 });
  }
  
  try {
    const charge = await Charge.retrieve(chargeId);
    
    return NextResponse.json({
      id: charge.id,
      code: charge.code,
      status: charge.timeline?.[charge.timeline.length - 1]?.status,
      pricing: charge.pricing,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}
```

## Webhooks

### Webhook Endpoint (Next.js)

```typescript
// app/api/coinbase/webhook/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import { resources } from 'coinbase-commerce-node';

const { Charge } = resources;

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('x-cc-webhook-signature');
  
  if (!signature) {
    return NextResponse.json({ error: 'No signature' }, { status: 400 });
  }
  
  // Verify webhook signature
  const hmac = crypto.createHmac('sha256', process.env.COINBASE_COMMERCE_WEBHOOK_SECRET!);
  const digest = hmac.update(body).digest('hex');
  
  if (digest !== signature) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }
  
  const event = JSON.parse(body);
  
  // Handle different event types
  switch (event.type) {
    case 'charge:created':
      await handleChargeCreated(event.data);
      break;
      
    case 'charge:confirmed':
      await handleChargeConfirmed(event.data);
      break;
      
    case 'charge:failed':
      await handleChargeFailed(event.data);
      break;
      
    case 'charge:delayed':
      await handleChargeDelayed(event.data);
      break;
      
    case 'charge:pending':
      await handleChargePending(event.data);
      break;
      
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }
  
  return NextResponse.json({ received: true });
}

async function handleChargeConfirmed(charge: any) {
  // Fulfill order, grant access, etc.
  const orderId = charge.metadata?.orderId;
  const userId = charge.metadata?.userId;
  
  // Update order status
  await updateOrderStatus(orderId, 'paid');
  
  // Grant access or send confirmation
  await grantAccess(userId, orderId);
}

async function handleChargeFailed(charge: any) {
  // Handle failed payment
  const orderId = charge.metadata?.orderId;
  await updateOrderStatus(orderId, 'failed');
}
```

### Webhook Endpoint (FastAPI)

```python
# app/api/coinbase_webhook.py
from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
import os
import json

router = APIRouter()
WEBHOOK_SECRET = os.environ.get("COINBASE_COMMERCE_WEBHOOK_SECRET")

@router.post("/coinbase/webhook")
async def webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("x-cc-webhook-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="No signature")
    
    # Verify signature
    hmac_obj = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    )
    digest = hmac_obj.hexdigest()
    
    if digest != signature:
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    event = json.loads(body)
    charge = event.get("data")
    
    # Handle events
    if event["type"] == "charge:confirmed":
        await handle_charge_confirmed(charge)
    elif event["type"] == "charge:failed":
        await handle_charge_failed(charge)
    
    return {"received": True}
```

## Payment Verification

### Verify Payment Status

```typescript
// lib/coinbase/verify.ts
import { Client, resources } from 'coinbase-commerce-node';

const client = Client.init(process.env.COINBASE_COMMERCE_API_KEY!);
const { Charge } = resources;

export async function verifyPayment(chargeId: string): Promise<boolean> {
  try {
    const charge = await Charge.retrieve(chargeId);
    
    // Get latest status from timeline
    const latestStatus = charge.timeline?.[charge.timeline.length - 1]?.status;
    
    return latestStatus === 'COMPLETED';
  } catch (error) {
    console.error('Error verifying payment:', error);
    return false;
  }
}
```

## Best Practices

### 1. Always Verify Webhooks

Never trust webhooks without signature verification:

```typescript
function verifyWebhookSignature(body: string, signature: string): boolean {
  const hmac = crypto.createHmac('sha256', process.env.COINBASE_COMMERCE_WEBHOOK_SECRET!);
  const digest = hmac.update(body).digest('hex');
  return digest === signature;
}
```

### 2. Use Metadata

Store order/user IDs in charge metadata:

```typescript
const charge = await Charge.create({
  // ... other fields
  metadata: {
    orderId: 'order-123',
    userId: 'user-456',
  },
});
```

### 3. Handle All Status Types

- `NEW`: Charge created
- `PENDING`: Payment pending
- `COMPLETED`: Payment confirmed
- `EXPIRED`: Charge expired
- `UNRESOLVED`: Payment unresolved
- `RESOLVED`: Previously unresolved, now resolved

### 4. Idempotency

Handle duplicate webhook events:

```typescript
async function handleChargeConfirmed(charge: any) {
  const chargeId = charge.id;
  
  // Check if already processed
  const existingOrder = await db.order.findFirst({
    where: { coinbaseChargeId: chargeId, status: 'paid' },
  });
  
  if (existingOrder) {
    return; // Already processed
  }
  
  // Process payment
  await fulfillOrder(charge);
}
```

### 5. Error Handling

```typescript
try {
  const charge = await Charge.create(chargeData);
} catch (error: any) {
  if (error.type === 'api_error') {
    // API error - retry logic
  } else if (error.type === 'invalid_request_error') {
    // Invalid request - fix and retry
  } else {
    // Other errors
  }
}
```

## Checklist for Coinbase Commerce

Before deploying:

- [ ] API keys stored in environment variables
- [ ] Webhook signatures verified
- [ ] All event types handled (confirmed, failed, etc.)
- [ ] Idempotency checks for webhook processing
- [ ] Error handling for API calls
- [ ] Metadata used to link charges to orders/users
- [ ] Payment verification before granting access
- [ ] Test mode tested before going live
