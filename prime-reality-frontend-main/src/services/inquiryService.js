import api from "./api";

// inquiry API
// buyer seller ko inquiry send karega

export const createInquiry = async (inquiryData) => {
  const response = await api.post("/inquiries", inquiryData);

  return response.data;
};