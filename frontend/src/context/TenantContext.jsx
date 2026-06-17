import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";
import api from "../api/axios";

const TenantContext = createContext();

export const TenantProvider = ({ children }) => {
  const [tenantId, setTenantId] =
    useState("");
  const [tenants, setTenants] =
    useState([]);
  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const loadTenants = async () => {
      try {
        const res = await api.get(
          "/tenants/"
        );
        setTenants(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadTenants();
  }, []);

  return (
    <TenantContext.Provider
      value={{
        tenantId,
        setTenantId,
        tenants,
        loading
      }}
    >
      {children}
    </TenantContext.Provider>
  );
};

export const useTenant = () =>
  useContext(TenantContext);
