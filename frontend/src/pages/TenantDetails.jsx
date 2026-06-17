import React, {
  useEffect,
  useState
} from "react";

import { useParams } from "react-router-dom";

import axios from "../api/axios";
import PageLayout from "../components/PageLayout";

export default function TenantDetails() {

  const { id } = useParams();

  const [tenant, setTenant] =
    useState(null);

  useEffect(() => {

    const loadTenant = async () => {

      try {

        const res = await axios.get(
          `/tenants/${id}`
        );

        setTenant(res.data);

      } catch (err) {

        console.error(err);

      }
    };

    loadTenant();

  }, [id]);

  if (!tenant) {

    return (
      <PageLayout>
        <p>Loading...</p>
      </PageLayout>
    );
  }

  return (

    <PageLayout>

      <div className="bg-white p-8 rounded-2xl border">

        <h1 className="text-3xl font-bold mb-8">
          Tenant Details
        </h1>

        <div className="grid grid-cols-2 gap-6">

          <div>
            <b>Name</b>
            <p>{tenant.name}</p>
          </div>

          <div>
            <b>Email</b>
            <p>{tenant.contact_email}</p>
          </div>

          <div>
            <b>Phone</b>
            <p>{tenant.phone || "-"}</p>
          </div>

          <div>
            <b>Industry</b>
            <p>{tenant.industry || "-"}</p>
          </div>

          <div>
            <b>Status</b>
            <p>{tenant.status}</p>
          </div>

          <div>
            <b>Slug</b>
            <p>{tenant.slug}</p>
          </div>

        </div>

      </div>

    </PageLayout>

  );
}