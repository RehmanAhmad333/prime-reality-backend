import api from "./api";

// property APIs
// listing/detail/filter later yahan connect honge

export const getProperties = async (params = {}) => {
  const response = await api.get("/properties", {
    params,
  });

  return response.data;
};

export const getPropertyById = async (id) => {
  const response = await api.get(`/properties/${id}`);

  return response.data;
};