export default () =>
  fetch("http://localhost:8080/logout", {
    method: "POST",
    credentials: "include",
  });
