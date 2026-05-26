import React, { useState } from "react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  async function submit(e) {
    e.preventDefault();
    await fetch("/api/auth/forgot-password", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ email })
    });
    setSent(true);
  }

  return (
    <div>
      <h2>Forgot password</h2>
      {sent ? (
        <p>If that email exists, a reset link was sent.</p>
      ) : (
        <form onSubmit={submit}>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" required />
          <button type="submit">Send reset link</button>
        </form>
      )}
    </div>
  );
}
