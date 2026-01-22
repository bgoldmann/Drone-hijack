# Stripe Payment Integration Guide

Comprehensive guide for integrating Stripe payments, subscriptions, and webhooks in Cursor IDE. Covers Next.js, FastAPI, and serverless function integration patterns.

## Overview

Stripe provides:
- **Payment Processing**: Credit cards, digital wallets, bank transfers
- **Subscriptions**: Recurring billing and subscription management
- **Checkout**: Pre-built payment forms
- **Webhooks**: Real-time event notifications
- **Billing Portal**: Self-service customer portal
- **Invoicing**: Automated invoice generation

## Setup & Installation

### Install Stripe SDKs

#### Next.js (JavaScript/TypeScript)

```bash
npm install stripe @stripe/stripe-js
```

#### FastAPI (Python)

```bash
pip install stripe
```

### Environment Variables

```bash
# .env.local (Next.js) / .env (FastAPI)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Production
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Critical**: Never expose secret keys in frontend code. Only use publishable keys client-side.

### Initialize Stripe Client

#### Next.js (Server-side)

```typescript
// lib/stripe/server.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
  typescript: true,
});
```

#### Next.js (Client-side)

```typescript
// lib/stripe/client.ts
import { loadStripe } from '@stripe/stripe-js';

export const getStripe = () => {
  return loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);
};
```

#### FastAPI (Python)

```python
# lib/stripe/client.py
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
```

## One-Time Payments

### Stripe Checkout (Recommended)

#### Create Checkout Session

```typescript
// app/api/checkout/route.ts (Next.js App Router)
import { stripe } from '@/lib/stripe/server';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { amount, currency = 'usd', successUrl, cancelUrl } = await request.json();
    
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price_data: {
            currency,
            product_data: {
              name: 'Product Name',
            },
            unit_amount: amount, // Amount in cents
          },
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: successUrl || `${request.headers.get('origin')}/success`,
      cancel_url: cancelUrl || `${request.headers.get('origin')}/cancel`,
    });
    
    return NextResponse.json({ sessionId: session.id, url: session.url });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}
```

#### Redirect to Checkout

```typescript
// Client component or page
'use client';

import { useRouter } from 'next/navigation';

export function CheckoutButton({ amount }: { amount: number }) {
  const router = useRouter();
  
  const handleCheckout = async () => {
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: amount * 100, // Convert to cents
        successUrl: `${window.location.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
        cancelUrl: `${window.location.origin}/cancel`,
      }),
    });
    
    const { url } = await response.json();
    if (url) {
      window.location.href = url;
    }
  };
  
  return <button onClick={handleCheckout}>Checkout</button>;
}
```

### Payment Elements (Custom Form)

```typescript
// app/checkout/page.tsx
'use client';

import { Elements } from '@stripe/react-stripe-js';
import { PaymentElement } from '@stripe/react-stripe-js';
import { getStripe } from '@/lib/stripe/client';

export default function CheckoutPage() {
  const stripePromise = getStripe();
  
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm />
    </Elements>
  );
}

function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!stripe || !elements) return;
    
    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/success`,
      },
    });
    
    if (error) {
      console.error(error.message);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button type="submit" disabled={!stripe}>
        Pay
      </button>
    </form>
  );
}
```

## Subscriptions

### Create Subscription

```typescript
// app/api/subscriptions/create/route.ts
import { stripe } from '@/lib/stripe/server';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { customerId, priceId } = await request.json();
    
    const subscription = await stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      payment_settings: { save_default_payment_method: 'on_subscription' },
      expand: ['latest_invoice.payment_intent'],
    });
    
    return NextResponse.json({
      subscriptionId: subscription.id,
      clientSecret: subscription.latest_invoice.payment_intent.client_secret,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}
```

### Checkout for Subscriptions

```typescript
// app/api/checkout/subscription/route.ts
export async function POST(request: NextRequest) {
  const { priceId, customerEmail } = await request.json();
  
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    customer_email: customerEmail,
    line_items: [
      {
        price: priceId,
        quantity: 1,
      },
    ],
    success_url: `${request.headers.get('origin')}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${request.headers.get('origin')}/pricing`,
    metadata: {
      // Add custom metadata
    },
  });
  
  return NextResponse.json({ url: session.url });
}
```

### Manage Subscription

```typescript
// app/api/subscriptions/update/route.ts
export async function POST(request: NextRequest) {
  const { subscriptionId, newPriceId } = await request.json();
  
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  
  const updatedSubscription = await stripe.subscriptions.update(subscriptionId, {
    items: [{
      id: subscription.items.data[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'create_prorations', // Prorate charges
  });
  
  return NextResponse.json({ subscription: updatedSubscription });
}
```

### Cancel Subscription

```typescript
// app/api/subscriptions/cancel/route.ts
export async function POST(request: NextRequest) {
  const { subscriptionId } = await request.json();
  
  const subscription = await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true, // Cancel at end of billing period
    // Or cancel immediately:
    // cancel_at_period_end: false,
  });
  
  return NextResponse.json({ subscription });
}
```

## Customers

### Create Customer

```typescript
// app/api/customers/create/route.ts
export async function POST(request: NextRequest) {
  const { email, name, metadata } = await request.json();
  
  const customer = await stripe.customers.create({
    email,
    name,
    metadata, // Link to your user ID
  });
  
  return NextResponse.json({ customerId: customer.id });
}
```

### Retrieve Customer

```typescript
// app/api/customers/[customerId]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { customerId: string } }
) {
  const customer = await stripe.customers.retrieve(params.customerId);
  return NextResponse.json({ customer });
}
```

## Webhooks

### Webhook Endpoint

```typescript
// app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe/server';
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature')!;
  
  let event: Stripe.Event;
  
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (error: any) {
    return NextResponse.json(
      { error: `Webhook Error: ${error.message}` },
      { status: 400 }
    );
  }
  
  // Handle the event
  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object as Stripe.Checkout.Session;
      // Fulfill the purchase
      await handleCheckoutCompleted(session);
      break;
      
    case 'customer.subscription.created':
    case 'customer.subscription.updated':
      const subscription = event.data.object as Stripe.Subscription;
      // Update subscription status
      await handleSubscriptionUpdate(subscription);
      break;
      
    case 'customer.subscription.deleted':
      const deletedSubscription = event.data.object as Stripe.Subscription;
      // Cancel subscription access
      await handleSubscriptionDeleted(deletedSubscription);
      break;
      
    case 'invoice.payment_succeeded':
      const invoice = event.data.object as Stripe.Invoice;
      // Grant access or extend subscription
      await handlePaymentSucceeded(invoice);
      break;
      
    case 'invoice.payment_failed':
      const failedInvoice = event.data.object as Stripe.Invoice;
      // Notify customer of payment failure
      await handlePaymentFailed(failedInvoice);
      break;
      
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }
  
  return NextResponse.json({ received: true });
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  // Fulfill order, grant access, etc.
  const customerId = session.customer as string;
  // Your business logic here
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const customerId = subscription.customer as string;
  const status = subscription.status;
  // Update subscription status in your database
}
```

### FastAPI Webhook Handler

```python
# app/api/webhooks/stripe.py
from fastapi import APIRouter, Request, HTTPException
import stripe
import os

router = APIRouter()
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event.type == "checkout.session.completed":
        session = event.data.object
        # Handle checkout completion
        await handle_checkout_completed(session)
    
    elif event.type == "customer.subscription.updated":
        subscription = event.data.object
        await handle_subscription_update(subscription)
    
    return {"status": "success"}
```

### Webhook Testing

```bash
# Install Stripe CLI
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
```

## Payment Methods

### Save Payment Method

```typescript
// app/api/payment-methods/create/route.ts
export async function POST(request: NextRequest) {
  const { customerId, paymentMethodId } = await request.json();
  
  const paymentMethod = await stripe.paymentMethods.attach(paymentMethodId, {
    customer: customerId,
  });
  
  // Set as default
  await stripe.customers.update(customerId, {
    invoice_settings: {
      default_payment_method: paymentMethodId,
    },
  });
  
  return NextResponse.json({ paymentMethod });
}
```

### List Payment Methods

```typescript
// app/api/payment-methods/list/route.ts
export async function GET(request: NextRequest) {
  const customerId = request.nextUrl.searchParams.get('customerId');
  
  const paymentMethods = await stripe.paymentMethods.list({
    customer: customerId!,
    type: 'card',
  });
  
  return NextResponse.json({ paymentMethods: paymentMethods.data });
}
```

## Billing Portal

### Create Billing Portal Session

```typescript
// app/api/billing-portal/route.ts
export async function POST(request: NextRequest) {
  const { customerId, returnUrl } = await request.json();
  
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: returnUrl || `${request.headers.get('origin')}/account`,
  });
  
  return NextResponse.json({ url: session.url });
}
```

### Redirect to Billing Portal

```typescript
'use client';

export function BillingPortalButton({ customerId }: { customerId: string }) {
  const handlePortal = async () => {
    const response = await fetch('/api/billing-portal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customerId }),
    });
    
    const { url } = await response.json();
    window.location.href = url;
  };
  
  return <button onClick={handlePortal}>Manage Billing</button>;
}
```

## Products & Prices

### Create Product

```typescript
// app/api/products/create/route.ts
export async function POST(request: NextRequest) {
  const { name, description, price, currency = 'usd', recurring } = await request.json();
  
  const product = await stripe.products.create({
    name,
    description,
  });
  
  const priceData: Stripe.PriceCreateParams = {
    product: product.id,
    unit_amount: price * 100,
    currency,
  };
  
  if (recurring) {
    priceData.recurring = {
      interval: recurring.interval, // 'month' or 'year'
    };
  }
  
  const stripePrice = await stripe.prices.create(priceData);
  
  return NextResponse.json({
    productId: product.id,
    priceId: stripePrice.id,
  });
}
```

## Best Practices

### 1. Idempotency Keys

Prevent duplicate operations:

```typescript
import { randomBytes } from 'crypto';

const idempotencyKey = randomBytes(16).toString('hex');

const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'usd',
}, {
  idempotencyKey,
});
```

### 2. Error Handling

```typescript
try {
  const session = await stripe.checkout.sessions.create({...});
} catch (error: any) {
  if (error.type === 'StripeCardError') {
    // Card declined
    console.error('Card error:', error.message);
  } else if (error.type === 'StripeRateLimitError') {
    // Too many requests
    console.error('Rate limit error');
  } else if (error.type === 'StripeInvalidRequestError') {
    // Invalid parameters
    console.error('Invalid request:', error.message);
  } else {
    // Other errors
    console.error('Error:', error.message);
  }
}
```

### 3. Metadata

Use metadata to link Stripe objects to your database:

```typescript
const customer = await stripe.customers.create({
  email,
  metadata: {
    userId: user.id, // Link to your user ID
    plan: 'pro',
  },
});
```

### 4. Webhook Security

Always verify webhook signatures:

```typescript
// Critical: Always verify webhook signatures
const event = stripe.webhooks.constructEvent(
  body,
  signature,
  process.env.STRIPE_WEBHOOK_SECRET!
);
```

### 5. Test Mode vs Live Mode

```typescript
// Use test keys during development
const stripe = new Stripe(
  process.env.NODE_ENV === 'production'
    ? process.env.STRIPE_SECRET_KEY_LIVE!
    : process.env.STRIPE_SECRET_KEY_TEST!
);
```

### 6. Subscription Status Handling

```typescript
// Map Stripe subscription status to your app
const STATUS_MAP = {
  'active': 'active',
  'canceled': 'canceled',
  'past_due': 'past_due',
  'unpaid': 'unpaid',
  'trialing': 'trialing',
  'incomplete': 'incomplete',
  'incomplete_expired': 'incomplete_expired',
  'paused': 'paused',
} as const;
```

## Common Patterns

### Subscription Status Check

```typescript
// app/api/subscriptions/status/route.ts
export async function GET(request: NextRequest) {
  const customerId = request.nextUrl.searchParams.get('customerId');
  
  const subscriptions = await stripe.subscriptions.list({
    customer: customerId!,
    status: 'active',
    limit: 1,
  });
  
  const hasActiveSubscription = subscriptions.data.length > 0;
  
  return NextResponse.json({ hasActiveSubscription });
}
```

### Usage-Based Billing

```typescript
// Record usage for metered billing
export async function recordUsage(
  subscriptionItemId: string,
  quantity: number,
  timestamp: number = Math.floor(Date.now() / 1000)
) {
  await stripe.subscriptionItems.createUsageRecord(subscriptionItemId, {
    quantity,
    timestamp,
  });
}
```

### Refunds

```typescript
// app/api/refunds/create/route.ts
export async function POST(request: NextRequest) {
  const { paymentIntentId, amount, reason } = await request.json();
  
  const refund = await stripe.refunds.create({
    payment_intent: paymentIntentId,
    amount: amount ? amount * 100 : undefined, // Full refund if not specified
    reason, // 'duplicate', 'fraudulent', 'requested_by_customer'
  });
  
  return NextResponse.json({ refund });
}
```

## Checklist for Stripe Integration

Before deploying Stripe integration:

- [ ] Secret keys never exposed in frontend code
- [ ] Webhook signatures verified
- [ ] Error handling for all Stripe API calls
- [ ] Idempotency keys used for critical operations
- [ ] Metadata links Stripe objects to your database
- [ ] Webhook events handled (payment succeeded/failed, subscription updates)
- [ ] Test mode vs live mode properly configured
- [ ] Subscription status synced with your database
- [ ] Customer portal configured for subscription management
- [ ] Payment method securely stored and managed
- [ ] Refund process defined and tested
- [ ] Tax handling configured (if applicable)
