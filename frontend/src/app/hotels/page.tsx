"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import LoadingSpinner from "@/components/LoadingSpinner";
import { hotelAPI } from "@/lib/api";
import type { Hotel, CreateHotel } from "@/types";

export default function HotelsPage() {
  const router = useRouter();
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingHotelId, setEditingHotelId] = useState<number | null>(null);
  const [formData, setFormData] = useState<CreateHotel>({
    name: "",
    location: "",
    description: "",
  });

  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    } else {
      loadHotels();
    }
  }, []);

  const loadHotels = async () => {
    try {
      setLoading(true);
      const data = await hotelAPI.getAll();
      setHotels(data.results);
      setError("");
    } catch (err: any) {
      setError("Failed to load hotels");
    } finally {
      setLoading(false);
    }
  };

  const openEditModal = (hotel: Hotel) => {
    setEditingHotelId(hotel.id);
    setFormData({
      name: hotel.name,
      location: hotel.location,
      description: hotel.description || "",
    });
    setShowCreateModal(true);
  };

  const openCreateModal = () => {
    setEditingHotelId(null);
    setFormData({ name: "", location: "", description: "" });
    setShowCreateModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingHotelId) {
        await hotelAPI.update(editingHotelId, formData);
      } else {
        await hotelAPI.create(formData);
      }
      setShowCreateModal(false);
      setEditingHotelId(null);
      setFormData({ name: "", location: "", description: "" });
      loadHotels();
    } catch (err: any) {
      setError(err.response?.data?.detail || (editingHotelId ? "Failed to update hotel" : "Failed to create hotel"));
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this hotel?")) return;

    try {
      await hotelAPI.delete(id);
      loadHotels();
    } catch (err: any) {
      setError("Failed to delete hotel");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Hotels</h1>
          <button
            onClick={openCreateModal}
            className="btn btn-primary"
          >
            + Add Hotel
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <LoadingSpinner />
        ) : hotels.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">
              No hotels found. Create your first hotel!
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {hotels.map((hotel) => (
              <div
                key={hotel.id}
                className="card hover:shadow-lg transition-shadow"
              >
                <div className="flex justify-between items-start mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">
                    {hotel.name}
                  </h2>
                </div>
                <p className="text-gray-600 mb-2">
                  <span className="font-medium">Location:</span>{" "}
                  {hotel.location}
                </p>
                {hotel.description && (
                  <p className="text-gray-600 mb-4">{hotel.description}</p>
                )}
                <div className="flex space-x-2 mt-4">
                  <Link
                    href={`/hotels/${hotel.id}`}
                    className="btn btn-primary flex-1 text-center"
                  >
                    View Details
                  </Link>
                  <button
                    onClick={() => openEditModal(hotel)}
                    className="btn btn-secondary"
                  >
                    Update
                  </button>
                  <button
                    onClick={() => handleDelete(hotel.id)}
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

      {/* Create Hotel Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">{editingHotelId ? "Update Hotel" : "Add New Hotel"}</h2>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name *
                  </label>
                  <input
                    type="text"
                    required
                    className="input"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Location *
                  </label>
                  <input
                    type="text"
                    required
                    className="input"
                    value={formData.location}
                    onChange={(e) =>
                      setFormData({ ...formData, location: e.target.value })
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
                    value={formData.description}
                    onChange={(e) =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                  />
                </div>
              </div>
              <div className="flex space-x-3 mt-6">
                <button type="submit" className="btn btn-primary flex-1">
                  {editingHotelId ? "Update Hotel" : "Create Hotel"}
                </button>
                <button
                  type="button"
                  onClick={() => { setShowCreateModal(false); setEditingHotelId(null); }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
