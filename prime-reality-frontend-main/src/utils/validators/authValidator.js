// auth validation
// frontend validation yahan handle hogi

export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return regex.test(email);
};

export const validatePassword = (password) => {
  // minimum 8 characters
  // uppercase + lowercase + number + special character

  const regex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  return regex.test(password);
};