import React, { useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";
  const [pw, setPw] = useState("");
  const [ok, setOk] = useState(false);

  async function submit(e) {
    e.preventDefault();
    const res = await fetch("/api/auth/reset-password", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ token, new_password: pw })
    });
    if (res.ok) setOk(true);
    else {
      const data = await res.json();
      alert(data.detail || "Failed to reset password");
    }
  }

  return (
    <div>
      <h2>Reset password</h2>
      {ok ? (
        <p>Password reset successfully. You can now log in.</p>
      ) : (
        <form onSubmit={submit}>
          <input type="password" value={pw} onChange={e=>setPw(e.target.value)} placeholder="New password" minLength={8} required />
          <button type="submit">Reset</button>
        </form>
      )}
    </div>
  );
}
