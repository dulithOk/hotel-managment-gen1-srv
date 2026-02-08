export interface User {
  username: string;
  email: string;
}

export interface ApiResponse<T> {
  is_error: boolean;
  message: string;
  results: T;
  status_code: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResult {
  access_token: string;
  token_type: string;
}

export interface AuthResponse {
  is_error: boolean;
  message: string;
  results: LoginResult;
  status_code: number;
}

export interface Hotel {
  id: number;
  name: string;
  location: string;
  description?: string;
  created_at: string;
}

export type GetHotelsResponse = ApiResponse<Hotel[]>;

export interface RoomType {
  id: number;
  hotel_id: number;
  name: string;
  description?: string;
  base_rate: number;
  effective_rate: number;
  created_at: string;
}

export interface HotelDetails {
  id: number;
  name: string;
  location: string;
  description: string;
  created_at: string;
  room_types: RoomType[];
}

export type GetHotelResponse = ApiResponse<HotelDetails>;

export interface RateAdjustment {
  id: number;
  room_type_id: number;
  adjustment_amount: number;
  effective_date: string;
  reason: string;
  created_at: string;
}

export interface CreateHotel {
  name: string;
  location: string;
  description?: string;
}

export interface CreateRoomType {
  hotel_id: number;
  name: string;
  description?: string;
  base_rate: number;
}

export interface CreateRateAdjustment {
  room_type_id: number;
  adjustment_amount: number;
  effective_date: string;
  reason: string;
}
