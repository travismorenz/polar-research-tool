export default () =>
  fetch("/api/logout", {
    method: "POST",
    credentials: "include",
  });
