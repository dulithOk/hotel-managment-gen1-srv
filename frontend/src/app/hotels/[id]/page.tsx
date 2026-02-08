"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import LoadingSpinner from "@/components/LoadingSpinner";
import { hotelAPI, roomTypeAPI, rateAdjustmentAPI } from "@/lib/api";
import type {
  CreateRoomType,
  RoomType,
  CreateRateAdjustment,
  RateAdjustment,
  HotelDetails,
} from "@/types";

export default function HotelDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const router = useRouter();
  const hotelId = parseInt(params.id);

  const [hotel, setHotel] = useState<HotelDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [showRoomModal, setShowRoomModal] = useState(false);
  const [editingRoomId, setEditingRoomId] = useState<number | null>(null);
  const [showAdjustmentModal, setShowAdjustmentModal] = useState(false);
  const [selectedRoomType, setSelectedRoomType] = useState<RoomType | null>(
    null,
  );
  const [adjustmentHistory, setAdjustmentHistory] = useState<RateAdjustment[]>(
    [],
  );

  const [roomFormData, setRoomFormData] = useState<CreateRoomType>({
    hotel_id: hotelId,
    name: "",
    description: "",
    base_rate: 0,
  });

  const [adjustmentFormData, setAdjustmentFormData] =
    useState<CreateRateAdjustment>({
      room_type_id: 0,
      adjustment_amount: 0,
      effective_date: new Date().toISOString().slice(0, 16),
      reason: "",
    });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    } else {
      loadHotel();
    }
  }, [hotelId]);

  const loadHotel = async () => {
    try {
      setLoading(true);
      const data = await hotelAPI.getById(hotelId);
      setHotel(data.results);
      setError("");
    } catch (err: any) {
      setError("Failed to load hotel details");
    } finally {
      setLoading(false);
    }
  };

  const openCreateRoomModal = () => {
    setEditingRoomId(null);
    setRoomFormData({
      hotel_id: hotelId,
      name: "",
      description: "",
      base_rate: 0,
    });
    setShowRoomModal(true);
  };

  const openEditRoomModal = (room: RoomType) => {
    setEditingRoomId(room.id);
    setRoomFormData({
      hotel_id: hotelId,
      name: room.name,
      description: room.description || "",
      base_rate: room.base_rate,
    });
    setShowRoomModal(true);
  };

  const handleSubmitRoom = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingRoomId) {
        await roomTypeAPI.update(editingRoomId, {
          name: roomFormData.name,
          description: roomFormData.description,
          base_rate: roomFormData.base_rate,
        });
      } else {
        await roomTypeAPI.create(roomFormData);
      }
      setShowRoomModal(false);
      setEditingRoomId(null);
      setRoomFormData({
        hotel_id: hotelId,
        name: "",
        description: "",
        base_rate: 0,
      });
      loadHotel();
    } catch (err: any) {
      setError(err.response?.data?.detail || (editingRoomId ? "Failed to update room type" : "Failed to create room type"));
    }
  };

  const handleDeleteRoom = async (roomId: number) => {
    if (!confirm("Are you sure you want to delete this room type?")) return;

    try {
      await roomTypeAPI.delete(roomId);
      loadHotel();
    } catch (err: any) {
      setError("Failed to delete room type");
    }
  };

  const openAdjustmentModal = async (roomType: RoomType) => {
    setSelectedRoomType(roomType);
    setAdjustmentFormData({
      room_type_id: roomType.id,
      adjustment_amount: 0,
      effective_date: new Date().toISOString().slice(0, 16),
      reason: "",
    });

    // Load adjustment history
    try {
      const history = await rateAdjustmentAPI.getHistory(roomType.id);
      setAdjustmentHistory(history);
    } catch (err) {
      setAdjustmentHistory([]);
    }

    setShowAdjustmentModal(true);
  };

  const handleCreateAdjustment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await rateAdjustmentAPI.create(adjustmentFormData);
      setShowAdjustmentModal(false);
      loadHotel();
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "Failed to create rate adjustment",
      );
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <LoadingSpinner />
      </div>
    );
  }

  if (!hotel) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-red-600">Hotel not found</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={() => router.push("/hotels")}
          className="text-primary-600 hover:text-primary-700 mb-4 flex items-center"
        >
          ← Back to Hotels
        </button>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <div className="card mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {hotel.name}
          </h1>
          <p className="text-gray-600 mb-1">
            <span className="font-medium">Location:</span> {hotel.location}
          </p>
          {hotel.description && (
            <p className="text-gray-600">{hotel.description}</p>
          )}
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Room Types</h2>
          <button
            onClick={openCreateRoomModal}
            className="btn btn-primary"
          >
            + Add Room Type
          </button>
        </div>

        {hotel.room_types.length === 0 ? (
          <div className="text-center py-12 card">
            <p className="text-gray-500">
              No room types yet. Add your first room type!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {hotel.room_types.map((room) => (
              <div key={room.id} className="card">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {room.name}
                </h3>
                {room.description && (
                  <p className="text-gray-600 mb-3">{room.description}</p>
                )}
                <div className="space-y-2 mb-4">
                  <p className="text-gray-700">
                    <span className="font-medium">Base Rate:</span> $
                    {room.base_rate.toFixed(2)}
                  </p>
                  <p className="text-gray-700">
                    <span className="font-medium">Effective Rate:</span>{" "}
                    <span className="text-lg font-bold text-primary-600">
                      ${room.effective_rate.toFixed(2)}
                    </span>
                  </p>
                  {room.effective_rate !== room.base_rate && (
                    <p className="text-sm text-green-600">
                      (+${(room.effective_rate - room.base_rate).toFixed(2)}{" "}
                      adjustment applied)
                    </p>
                  )}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => openAdjustmentModal(room)}
                    className="btn btn-primary flex-1"
                  >
                    Adjust Rate
                  </button>
                  <button
                    onClick={() => openEditRoomModal(room)}
                    className="btn btn-secondary"
                  >
                    Update
                  </button>
                  <button
                    onClick={() => handleDeleteRoom(room.id)}
                    className="btn btn-danger"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Room Type Modal */}
      {showRoomModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">{editingRoomId ? "Update Room Type" : "Add Room Type"}</h2>
            <form onSubmit={handleSubmitRoom}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name *
                  </label>
                  <input
                    type="text"
                    required
                    className="input"
                    value={roomFormData.name}
                    onChange={(e) =>
                      setRoomFormData({ ...roomFormData, name: e.target.value })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Base Rate ($) *
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    required
                    className="input"
                    value={roomFormData.base_rate || ""}
                    onChange={(e) =>
                      setRoomFormData({
                        ...roomFormData,
                        base_rate: parseFloat(e.target.value),
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    className="input"
                    rows={3}
                    value={roomFormData.description}
                    onChange={(e) =>
                      setRoomFormData({
                        ...roomFormData,
                        description: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn btn-primary flex-1">
                  {editingRoomId ? "Update Room Type" : "Create Room Type"}
                </button>
                <button
                  type="button"
                  onClick={() => { setShowRoomModal(false); setEditingRoomId(null); }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Rate Adjustment Modal */}
      {showAdjustmentModal && selectedRoomType && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 my-8">
            <h2 className="text-2xl font-bold mb-4">
              Adjust Rate - {selectedRoomType.name}
            </h2>

            <div className="bg-gray-50 p-4 rounded-lg mb-6">
              <p className="text-sm text-gray-600">
                Current Base Rate: ${selectedRoomType.base_rate.toFixed(2)}
              </p>
              <p className="text-sm text-gray-600">
                Current Effective Rate: $
                {selectedRoomType.effective_rate.toFixed(2)}
              </p>
            </div>

            <form onSubmit={handleCreateAdjustment} className="mb-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Adjustment Amount ($) *
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    className="input"
                    placeholder="Enter positive or negative amount"
                    value={adjustmentFormData.adjustment_amount || ""}
                    onChange={(e) =>
                      setAdjustmentFormData({
                        ...adjustmentFormData,
                        adjustment_amount: parseFloat(e.target.value),
                      })
                    }
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Positive for increase, negative for decrease
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Effective Date *
                  </label>
                  <input
                    type="datetime-local"
                    required
                    className="input"
                    value={adjustmentFormData.effective_date}
                    onChange={(e) =>
                      setAdjustmentFormData({
                        ...adjustmentFormData,
                        effective_date: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Reason *
                  </label>
                  <textarea
                    required
                    className="input"
                    rows={2}
                    placeholder="e.g., High season pricing, Holiday premium"
                    value={adjustmentFormData.reason}
                    onChange={(e) =>
                      setAdjustmentFormData({
                        ...adjustmentFormData,
                        reason: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn btn-primary flex-1">
                  Apply Adjustment
                </button>
                <button
                  type="button"
                  onClick={() => setShowAdjustmentModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>

            {/* Adjustment History */}
            {adjustmentHistory.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3">
                  Adjustment History
                </h3>
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {adjustmentHistory.map((adj) => (
                    <div
                      key={adj.id}
                      className="bg-gray-50 p-3 rounded border border-gray-200"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-medium text-gray-900">
                            {adj.adjustment_amount >= 0 ? "+" : ""}$
                            {adj.adjustment_amount.toFixed(2)}
                          </p>
                          <p className="text-sm text-gray-600">{adj.reason}</p>
                        </div>
                        <div className="text-right text-sm text-gray-500">
                          <p>
                            {new Date(adj.effective_date).toLocaleDateString()}
                          </p>
                          <p>
                            {new Date(adj.effective_date).toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
