import React from 'react';
import './index.css';
import Header from './Header.js';
import Footer from './Footer.js';
import InputCard from './InputCard.js';

import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://1844f50f3ae7ae2715be1d9b381b397b@o4506784279298048.ingest.us.sentry.io/4508249368690688",
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
  // Tracing
  tracesSampleRate: 1.0, //  Capture 100% of the transactions
  // Set 'tracePropagationTargets' to control for which URLs distributed tracing should be enabled
  tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],
  // Session Replay
  replaysSessionSampleRate: 0.1, // This sets the sample rate at 10%. You may want to change it to 100% while in development and then sample at a lower rate in production.
  replaysOnErrorSampleRate: 1.0, // If you're not already sampling the entire session, change the sample rate to 100% when sampling sessions where errors occur.
});

function App() {


  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        <div className="container mx-auto p-4">
          <InputCard />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
