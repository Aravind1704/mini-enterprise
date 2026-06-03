import React, {
  useState
} from "react";

import {
  useParams
} from "react-router-dom";

import axios from "../api/axios";

export default function ChannelMembers() {

  const { channelId } =
    useParams();

  const [userId, setUserId] =
    useState("");

  const joinChannel = async () => {

    try {

      await axios.post(
        `/channels/${channelId}/join?user_id=${userId}`
      );

      alert(
        "User joined channel"
      );

      setUserId("");

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }
  };

  const leaveChannel = async () => {

    try {

      await axios.post(
        `/channels/${channelId}/leave?user_id=${userId}`
      );

      alert(
        "User left channel"
      );

      setUserId("");

    } catch (err) {

      alert(
        err.response?.data?.detail
      );

    }
  };

  return (
    <div className="p-6">

      <div className="bg-white p-6 rounded shadow max-w-xl">

        <h1 className="text-3xl font-bold mb-6">
          Channel Members
        </h1>

        <input
          className="w-full border p-3 rounded mb-4"
          placeholder="User ID"
          value={userId}
          onChange={(e) =>
            setUserId(
              e.target.value
            )
          }
        />

        <div className="flex gap-4">

          <button
            onClick={joinChannel}
            className="bg-green-600 text-white px-5 py-2 rounded"
          >
            Join Channel
          </button>

          <button
            onClick={leaveChannel}
            className="bg-red-600 text-white px-5 py-2 rounded"
          >
            Leave Channel
          </button>

        </div>

      </div>

    </div>
  );
}