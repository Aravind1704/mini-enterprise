import { useEffect } from "react";

import {
  useNavigate,
  useSearchParams
} from "react-router-dom";

export default function OAuthSuccess() {

  const navigate = useNavigate();

  const [searchParams] =
    useSearchParams();

  useEffect(() => {

    const accessToken =
      searchParams.get("access_token");

    const refreshToken =
      searchParams.get("refresh_token");

    if (
      accessToken &&
      refreshToken
    ) {

      localStorage.setItem(
        "access_token",
        accessToken
      );

      localStorage.setItem(
        "refresh_token",
        refreshToken
      );

      navigate("/dashboard");

    } else {

      navigate("/login");
    }

  }, [navigate, searchParams]);

  return (
    <div>
      Logging in...
    </div>
  );
}