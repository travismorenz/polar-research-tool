export const login = (input) =>
  fetch("/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(input),
  }).then((res) => res.json());

export const logout = () =>
  fetch("/api/logout", {
    method: "POST",
    credentials: "include",
  });

export const register = (input) =>
  fetch("/api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(input),
  }).then((res) => res.json());
