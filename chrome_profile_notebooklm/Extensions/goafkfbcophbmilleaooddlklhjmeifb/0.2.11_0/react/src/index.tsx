import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = document.createElement("div");
root.className = "container";
document.body.appendChild(root);
const rootDiv = ReactDOM.createRoot(root);

const options = {
  api_host: process.env.REACT_APP_PUBLIC_POSTHOG_HOST,
  options: {
    persistence: "localStorage",
  },
};

rootDiv.render(
  <React.StrictMode>
    {/*<PostHogProvider
      apiKey={process.env.REACT_APP_PUBLIC_POSTHOG_KEY}
      options={options}
    >*/}
    <App />
    {/*</PostHogProvider>*/}
  </React.StrictMode>
);
