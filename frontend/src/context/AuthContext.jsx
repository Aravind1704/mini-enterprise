import {
  createContext,
  useContext,
  useState,
  useEffect
} from "react";

import api from "../api/axios";

const AuthContext = createContext();

export const AuthProvider = ({
  children
}) => {

  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  // =====================================
  // LOGIN
  // =====================================

  const login = async (
    email,
    password
  ) => {

    const response =
      await api.post(
        "/auth/login",
        {
          email,
          password
        }
      );

    const {
      access_token,
      refresh_token
    } = response.data;

    // SAVE TOKENS

    localStorage.setItem(
      "access_token",
      access_token
    );

    localStorage.setItem(
      "refresh_token",
      refresh_token
    );

    // GET USER

    const me =
      await api.get("/auth/me");

    setUser(me.data);

    localStorage.setItem(
      "user",
      JSON.stringify(me.data)
    );

    return me.data;
  };


  // =====================================
  // LOGOUT
  // =====================================

  const logout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "refresh_token"
    );

    localStorage.removeItem(
      "user"
    );

    setUser(null);
  };


  // =====================================
  // AUTO LOGIN
  // =====================================

  useEffect(() => {

    const initialize =
      async () => {

      try {

        const token =
          localStorage.getItem(
            "access_token"
          );

        if (!token) {

          setLoading(false);

          return;
        }

        // FETCH USER

        const response =
          await api.get("/auth/me");

        setUser(response.data);

      } catch (error) {

        console.log(
          "Auth restore failed"
        );

        logout();
      }

      setLoading(false);
    };

    initialize();

  }, []);


  return (

    <AuthContext.Provider
      value={{
        user,
        setUser,
        login,
        logout,
        loading,
        isAuthenticated: !!user
      }}
    >

      {children}

    </AuthContext.Provider>
  );
};

export const useAuth = () =>
  useContext(AuthContext);