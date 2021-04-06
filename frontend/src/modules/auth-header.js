export default function authHeader() {
  const token = localStorage.getItem("user");
  const config = {
    headers: {
      Authorization: `JWT ${token}`,
    },
  };
  return config;
}
