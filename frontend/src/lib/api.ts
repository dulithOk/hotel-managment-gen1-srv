import axios from "axios";
import type {
  AuthResponse,
  LoginCredentials,
  Hotel,
  CreateHotel,
  RoomType,
  CreateRoomType,
  RateAdjustment,
  CreateRateAdjustment,
  GetHotelsResponse,
  GetHotelResponse,
} from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>("/user/login", credentials);
    return response.data;
  },
};

// Hotel API
export const hotelAPI = {
  getAll: async (): Promise<GetHotelsResponse> => {
    const response = await api.get<GetHotelsResponse>("/hotels");
    return response.data;
  },

  getById: async (id: number): Promise<GetHotelResponse> => {
    const response = await api.get<GetHotelResponse>(`/hotels/${id}`);
    return response.data;
  },

  create: async (hotel: CreateHotel): Promise<Hotel> => {
    const response = await api.post<Hotel>("/hotels", hotel);
    return response.data;
  },

  update: async (id: number, hotel: Partial<CreateHotel>): Promise<Hotel> => {
    const response = await api.put<Hotel>(`/hotels/${id}`, hotel);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/hotels/${id}`);
  },
};

// RoomType API
export const roomTypeAPI = {
  getAll: async (hotelId?: number): Promise<RoomType[]> => {
    const params = hotelId ? { hotel_id: hotelId } : {};
    const response = await api.get<RoomType[]>("/room-types", { params });
    return response.data;
  },

  create: async (roomType: CreateRoomType): Promise<RoomType> => {
    const response = await api.post<RoomType>("/room-types", roomType);
    return response.data;
  },

  update: async (
    id: number,
    roomType: Partial<Omit<CreateRoomType, "hotel_id">>,
  ): Promise<RoomType> => {
    const response = await api.put<RoomType>(`/room-types/${id}`, roomType);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/room-types/${id}`);
  },
};

// RateAdjustment API
export const rateAdjustmentAPI = {
  getHistory: async (roomTypeId: number): Promise<RateAdjustment[]> => {
    const response = await api.get<RateAdjustment[]>("/rate-adjustments", {
      params: { room_type_id: roomTypeId },
    });
    return response.data;
  },

  create: async (adjustment: CreateRateAdjustment): Promise<RateAdjustment> => {
    const response = await api.post<RateAdjustment>(
      "/rate-adjustments",
      adjustment,
    );
    return response.data;
  },
};

export default api;
